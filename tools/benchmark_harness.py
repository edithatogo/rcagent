"""Deterministic, privacy-safe benchmark contracts and receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
import tracemalloc
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "evaluation/benchmark/registry.json"
SCHEMA_PATH = ROOT / "conductor/schemas/benchmark-harness.schema.json"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return _read_json(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_registry(registry: dict[str, Any], root: Path = ROOT) -> list[str]:
    schema = _read_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in validator.iter_errors(registry)
    ]
    for key in ("dependencies", "metrics", "hard_gates", "cases", "suites"):
        ids = [
            item["id"]
            for item in registry.get(key, [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        errors.extend(f"{key}: duplicate id {value!r}" for value in sorted(set(ids)) if ids.count(value) > 1)

    fixture_cases: dict[str, dict[str, Any]] = {}
    for case in registry.get("cases", []):
        if not isinstance(case, dict):
            continue
        path = root / str(case.get("path", ""))
        if not path.is_file():
            errors.append(f"cases: missing fixture {case.get('path')!r}")
            continue
        if _sha256(path) != case.get("sha256"):
            errors.append(f"cases: checksum mismatch for {case.get('id')!r}")
        try:
            fixture = _read_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"cases: invalid fixture {case.get('path')!r}: {exc}")
            continue
        for item in fixture.get("cases", []):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                fixture_cases[item["id"]] = item
        if case.get("id") not in fixture_cases:
            errors.append(f"cases: fixture has no case {case.get('id')!r}")
        if case.get("activation_status") == "pending_owner_decision":
            if not case.get("decision_id"):
                errors.append(f"cases: pending case {case.get('id')!r} requires decision_id")
            if case.get("promotion_eligible") is not False:
                errors.append(f"cases: pending case {case.get('id')!r} cannot be promotion eligible")

    case_ids = {case.get("id") for case in registry.get("cases", []) if isinstance(case, dict)}
    for suite in registry.get("suites", []):
        if not isinstance(suite, dict):
            continue
        for case_id in suite.get("case_ids", []):
            if case_id not in case_ids:
                errors.append(f"suites: unknown case {case_id!r}")
        pending: set[str] = {
            case["id"]
            for case in registry.get("cases", [])
            if isinstance(case, dict)
            and isinstance(case.get("id"), str)
            and case.get("activation_status") != "active"
        }
        included_pending = pending.intersection(suite.get("case_ids", []))
        if included_pending:
            errors.append(f"suites: pending cases cannot run: {sorted(included_pending)!r}")

    required_gate_categories = {"privacy", "security", "clinical-safety", "cultural-safety", "harmful-output"}
    represented = {gate.get("category") for gate in registry.get("hard_gates", []) if isinstance(gate, dict)}
    for category in sorted(required_gate_categories - represented):
        errors.append(f"hard_gates: missing {category!r}")
    for legacy in registry.get("legacy_map", []):
        if not isinstance(legacy, dict):
            continue
        for relative in legacy.get("source_paths", []):
            if not (root / relative).is_file():
                errors.append(f"legacy_map: missing source {relative!r}")
    return sorted(errors)


def run_suite(registry: dict[str, Any], suite_id: str) -> dict[str, Any]:
    errors = validate_registry(registry)
    if errors:
        raise ValueError("invalid registry: " + "; ".join(errors))
    suite = next((item for item in registry["suites"] if item["id"] == suite_id), None)
    if suite is None:
        raise ValueError(f"unknown suite {suite_id!r}")
    started = time.perf_counter()
    cpu_started = time.process_time()
    tracemalloc.start()
    by_id: dict[str, dict[str, Any]] = {}
    for case_meta in registry["cases"]:
        fixture = _read_json(ROOT / case_meta["path"])
        by_id.update({case["id"]: case for case in fixture["cases"]})
    results: list[dict[str, Any]] = []
    for case_id in suite["case_ids"]:
        case = by_id[case_id]
        expected, candidate = case["expected"], case["candidate"]
        required_evidence = set(expected["evidence_ids"])
        required_claims = set(expected["claim_types"])
        evidence_recall = len(required_evidence.intersection(candidate["evidence_ids"])) / len(required_evidence)
        claim_coverage = len(required_claims.intersection(candidate["claim_types"])) / len(required_claims)
        privacy_count = len(candidate["privacy_violations"])
        safety_count = len(candidate["safety_violations"])
        abstention_correct = candidate["abstained"] is expected["must_abstain"]
        passed = evidence_recall == 1 and claim_coverage == 1 and abstention_correct and not privacy_count and not safety_count
        results.append({"case_id": case_id, "evidence_recall": evidence_recall, "claim_type_coverage": claim_coverage, "abstention_correct": abstention_correct, "privacy_violations": privacy_count, "safety_violations": safety_count, "passed": passed})
    elapsed = time.perf_counter() - started
    cpu_seconds = time.process_time() - cpu_started
    fixture_paths = sorted({case["path"] for case in registry["cases"] if case["id"] in suite["case_ids"]})
    context_bytes = sum((ROOT / path).stat().st_size for path in fixture_paths)
    _, peak_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    receipt: dict[str, Any] = {
        "schema_version": "1.0", "benchmark_version": registry["benchmark_version"],
        "suite_id": suite_id, "runner": suite["runner"], "network": suite["network"],
        "execution_manifest": {"model":"none-deterministic-contract", "runtime":f"Python {platform.python_version()}", "prompt":"none", "retrieval":"fixture identifiers only", "tools":[], "device":platform.platform(), "seed":0, "sampling":"none", "retries":0, "timeout":"not applicable", "sandbox":"no external execution"},
        "registry_sha256": _sha256(REGISTRY_PATH), "fixture_sha256": {path: _sha256(ROOT / path) for path in fixture_paths},
        "results": results, "summary": {"case_count": len(results), "passed": sum(item["passed"] for item in results), "promotion_status": "eligible_for_human_review" if all(item["passed"] for item in results) else "blocked", "external_cost": {"amount": 0, "currency": "AUD"}},
        "device_observations": {"latency_ms": round(elapsed * 1000, 3), "throughput_cases_s": round(len(results) / elapsed, 3), "peak_ram_bytes": peak_ram, "context_bytes": context_bytes, "cpu_seconds_energy_proxy": round(cpu_seconds, 6)},
        "limitations": ["deterministic structural baseline only", "no clinical gold standard", "no generative model comparator", "no external publication approval"]
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    return receipt


def render_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = ["# Deterministic benchmark report", "", f"- Suite: `{result['suite_id']}`", f"- Cases passed: {summary['passed']}/{summary['case_count']}", f"- Promotion state: `{summary['promotion_status']}`", f"- Receipt SHA-256: `{result['receipt_sha256']}`", "", "## Boundaries", ""]
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(["", "This internal report is not an approved model ranking, clinical judgement, operational threshold, or publication.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    run = sub.add_parser("run")
    run.add_argument("--suite", default="regression")
    run.add_argument("--output", type=Path)
    report = sub.add_parser("report")
    report.add_argument("--result", type=Path, required=True)
    report.add_argument("--output", type=Path)
    args = parser.parse_args()
    registry = load_registry()
    if args.command == "validate":
        errors = validate_registry(registry)
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            return 1
        print("Benchmark registry validation passed.")
        return 0
    if args.command == "run":
        result = run_suite(registry, args.suite)
        output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    else:
        result = _read_json(args.result)
        output = render_report(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
