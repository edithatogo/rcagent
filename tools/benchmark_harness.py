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
CASE_SCHEMA_PATH = ROOT / "conductor/schemas/benchmark-case.schema.json"


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
        errors.extend(
            f"{key}: duplicate id {value!r}" for value in sorted(set(ids)) if ids.count(value) > 1
        )

    case_schema = _read_json(CASE_SCHEMA_PATH)
    Draft202012Validator.check_schema(case_schema)
    case_validator = Draft202012Validator(case_schema)
    fixture_root = (root / "evaluation/benchmark/fixtures").resolve()
    fixture_cache: dict[Path, dict[str, dict[str, Any]]] = {}
    for case in registry.get("cases", []):
        if not isinstance(case, dict):
            continue
        relative = str(case.get("path", ""))
        path = (root / relative).resolve()
        try:
            path.relative_to(fixture_root)
        except ValueError:
            errors.append(f"cases: fixture path escapes the fixture directory: {relative!r}")
            continue
        if not path.is_file():
            errors.append(f"cases: missing fixture {relative!r}")
            continue
        if _sha256(path) != case.get("sha256"):
            errors.append(f"cases: checksum mismatch for {case.get('id')!r}")
        if path not in fixture_cache:
            try:
                fixture = _read_json(path)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                errors.append(f"cases: invalid fixture {relative!r}: {exc}")
                continue
            errors.extend(
                f"fixtures.{'.'.join(map(str, error.absolute_path))}: {error.message}"
                for error in case_validator.iter_errors(fixture)
            )
            fixture_ids = [
                item["id"]
                for item in fixture.get("cases", [])
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            ]
            errors.extend(
                f"fixtures: duplicate case id {value!r}"
                for value in sorted(set(fixture_ids))
                if fixture_ids.count(value) > 1
            )
            fixture_cache[path] = {
                item["id"]: item
                for item in fixture.get("cases", [])
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
        fixture_cases = fixture_cache.get(path, {})
        if case.get("id") not in fixture_cases:
            errors.append(f"cases: fixture has no case {case.get('id')!r}")
        else:
            fixture_case = fixture_cases[str(case["id"])]
            if fixture_case.get("modalities") != case.get("modalities"):
                errors.append(f"cases: modality mismatch for {case.get('id')!r}")
        if case.get("activation_status") == "pending_owner_decision":
            if not case.get("decision_id"):
                errors.append(f"cases: pending case {case.get('id')!r} requires decision_id")
            if case.get("promotion_eligible") is not False:
                errors.append(
                    f"cases: pending case {case.get('id')!r} cannot be promotion eligible"
                )

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

    required_gate_categories = {
        "privacy",
        "security",
        "clinical-safety",
        "cultural-safety",
        "harmful-output",
    }
    represented = {
        gate.get("category") for gate in registry.get("hard_gates", []) if isinstance(gate, dict)
    }
    for category in sorted(required_gate_categories - represented):
        errors.append(f"hard_gates: missing {category!r}")
    for legacy in registry.get("legacy_map", []):
        if not isinstance(legacy, dict):
            continue
        for relative in legacy.get("source_paths", []):
            if not (root / relative).is_file():
                errors.append(f"legacy_map: missing source {relative!r}")
    return sorted(errors)


def score_case(case: dict[str, Any]) -> dict[str, Any]:
    expected, candidate = case["expected"], case["candidate"]
    required_evidence = set(expected["evidence_ids"])
    required_claims = set(expected["claim_types"])
    evidence_recall = len(required_evidence.intersection(candidate["evidence_ids"])) / len(
        required_evidence
    )
    claim_coverage = len(required_claims.intersection(candidate["claim_types"])) / len(
        required_claims
    )
    gate_counts = {
        category: len(violations) for category, violations in candidate["gate_violations"].items()
    }
    invalid_citations = set(candidate["evidence_ids"]) - required_evidence
    citation_validity = 1 - (len(invalid_citations) / len(candidate["evidence_ids"]))
    abstention_correct = candidate["abstained"] is expected["must_abstain"]
    passed = (
        evidence_recall == 1
        and claim_coverage == 1
        and citation_validity == 1
        and abstention_correct
        and not any(gate_counts.values())
    )
    return {
        "case_id": case["id"],
        "evidence_recall": evidence_recall,
        "claim_type_coverage": claim_coverage,
        "citation_validity": citation_validity,
        "abstention_correct": abstention_correct,
        "gate_violations": gate_counts,
        "robustness_challenge_pass": passed,
        "passed": passed,
    }


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
        results.append(score_case(by_id[case_id]))
    elapsed = time.perf_counter() - started
    cpu_seconds = time.process_time() - cpu_started
    fixture_paths = sorted(
        {case["path"] for case in registry["cases"] if case["id"] in suite["case_ids"]}
    )
    context_bytes = sum((ROOT / path).stat().st_size for path in fixture_paths)
    _, peak_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "benchmark_version": registry["benchmark_version"],
        "suite_id": suite_id,
        "runner": suite["runner"],
        "network": suite["network"],
        "execution_manifest": {
            "model": "none-deterministic-contract",
            "runtime": f"Python {platform.python_version()}",
            "prompt": "none",
            "retrieval": "fixture identifiers only",
            "tools": [],
            "device": platform.platform(),
            "seed": 0,
            "sampling": "none",
            "retries": 0,
            "timeout": "not applicable",
            "sandbox": "no external execution",
        },
        "registry_sha256": _sha256(REGISTRY_PATH),
        "fixture_sha256": {path: _sha256(ROOT / path) for path in fixture_paths},
        "results": results,
        "summary": {
            "case_count": len(results),
            "passed": sum(item["passed"] for item in results),
            "promotion_status": "eligible_for_agent_panel_review"
            if all(item["passed"] for item in results)
            else "blocked",
            "external_cost": {"amount": 0, "currency": "AUD"},
        },
        "device_observations": {
            "latency_ms": round(elapsed * 1000, 3),
            "throughput_cases_s": round(len(results) / elapsed, 3),
            "peak_ram_bytes": peak_ram,
            "storage_bytes": context_bytes,
            "context_bytes": context_bytes,
            "cpu_seconds_energy_proxy": round(cpu_seconds, 6),
        },
        "limitations": [
            "deterministic structural baseline only",
            "no clinical gold standard",
            "no generative model comparator",
            "no external publication approval",
        ],
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    return receipt


def verify_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    recorded_hash = result.get("receipt_sha256")
    unsigned = {key: value for key, value in result.items() if key != "receipt_sha256"}
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    if recorded_hash != hashlib.sha256(canonical).hexdigest():
        errors.append("result receipt hash mismatch")
    if result.get("registry_sha256") != _sha256(REGISTRY_PATH):
        errors.append("result registry hash is stale")
    registry = load_registry()
    suite = next(
        (item for item in registry["suites"] if item["id"] == result.get("suite_id")),
        None,
    )
    if suite is None:
        errors.append("result suite is unknown")
    else:
        if result.get("runner") != suite["runner"] or result.get("network") != suite["network"]:
            errors.append("result execution contract does not match the suite")
        observations = result.get("results")
        if not isinstance(observations, list):
            errors.append("result observations are missing")
        else:
            observed_ids = [item.get("case_id") for item in observations if isinstance(item, dict)]
            if observed_ids != suite["case_ids"]:
                errors.append("result cases do not match the suite")
            for item in observations:
                if not isinstance(item, dict):
                    errors.append("result observation is malformed")
                    continue
                gate_counts = item.get("gate_violations")
                if not isinstance(gate_counts, dict) or set(gate_counts) != {
                    "privacy",
                    "security",
                    "clinical-safety",
                    "cultural-safety",
                    "harmful-output",
                }:
                    errors.append(f"result gate counts are malformed for {item.get('case_id')!r}")
                elif item.get("passed") is True and any(gate_counts.values()):
                    errors.append(f"result passes a failed hard gate for {item.get('case_id')!r}")
            summary = result.get("summary")
            passed_count = sum(
                item.get("passed") is True for item in observations if isinstance(item, dict)
            )
            if not isinstance(summary, dict) or summary.get("case_count") != len(observations):
                errors.append("result case count is inconsistent")
            elif summary.get("passed") != passed_count:
                errors.append("result pass count is inconsistent")
            elif summary.get("promotion_status") != (
                "eligible_for_agent_panel_review"
                if passed_count == len(observations)
                else "blocked"
            ):
                errors.append("result promotion status is inconsistent")
    fixture_hashes = result.get("fixture_sha256")
    if not isinstance(fixture_hashes, dict):
        errors.append("result fixture hashes are missing")
    else:
        for relative, expected_hash in fixture_hashes.items():
            if not isinstance(relative, str) or not isinstance(expected_hash, str):
                errors.append("result fixture hash entry is malformed")
                continue
            path = (ROOT / relative).resolve()
            try:
                path.relative_to((ROOT / "evaluation/benchmark/fixtures").resolve())
            except ValueError:
                errors.append(f"result fixture path escapes fixture directory: {relative!r}")
                continue
            if not path.is_file() or _sha256(path) != expected_hash:
                errors.append(f"result fixture hash mismatch: {relative!r}")
    return sorted(errors)


def render_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# Deterministic benchmark report",
        "",
        f"- Suite: `{result['suite_id']}`",
        f"- Cases passed: {summary['passed']}/{summary['case_count']}",
        f"- Promotion state: `{summary['promotion_status']}`",
        f"- Receipt SHA-256: `{result['receipt_sha256']}`",
        "",
        "## Boundaries",
        "",
    ]
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(
        [
            "",
            "This internal report is not an approved model ranking, clinical judgement, operational threshold, or publication.",
            "",
        ]
    )
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
        errors = verify_result(result)
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            return 1
        output = render_report(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
