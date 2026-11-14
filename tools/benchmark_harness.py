"""Deterministic, privacy-safe benchmark contracts and receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
import tracemalloc
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Literal, Protocol, TypedDict, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "evaluation/benchmark/registry.json"
SCHEMA_PATH = ROOT / "conductor/schemas/benchmark-harness.schema.json"
CASE_SCHEMA_PATH = ROOT / "conductor/schemas/benchmark-case.schema.json"


class _SchemaValidator(Protocol):
    """Non-deprecated object-validation API; the stub's other overload is untyped."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


class CaseScore(TypedDict):
    case_id: str
    evidence_recall: float
    claim_type_coverage: float
    citation_validity: float
    abstention_correct: bool
    gate_violations: dict[str, int]
    robustness_challenge_pass: bool
    passed: bool


class ExecutionManifest(TypedDict):
    model: str
    runtime: str
    prompt: str
    retrieval: str
    tools: list[str]
    device: str
    seed: int
    sampling: str
    retries: int
    timeout: str
    sandbox: str


class ExternalCost(TypedDict):
    amount: int
    currency: str


class BenchmarkSummary(TypedDict):
    case_count: int
    passed: int
    promotion_status: Literal["eligible_for_agent_panel_review", "blocked"]
    external_cost: ExternalCost


class DeviceObservations(TypedDict):
    latency_ms: float
    throughput_cases_s: float
    peak_ram_bytes: int
    storage_bytes: int
    context_bytes: int
    cpu_seconds_energy_proxy: float


class _BenchmarkFields(TypedDict):
    schema_version: Literal["1.0"]
    benchmark_version: str
    suite_id: str
    runner: str
    network: str
    execution_manifest: ExecutionManifest
    registry_sha256: str
    fixture_sha256: dict[str, str]
    results: list[CaseScore]
    summary: BenchmarkSummary
    device_observations: DeviceObservations
    limitations: list[str]


class BenchmarkReceipt(_BenchmarkFields):
    receipt_sha256: str


def _text(value: object, *, context: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{context}: expected text")
    return value


def _texts(value: object, *, context: str) -> list[str]:
    if not is_array(value) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{context}: expected an array of text")
    return [item for item in value if isinstance(item, str)]


def _read_json(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not is_object(value):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_registry(path: Path = REGISTRY_PATH) -> JsonObject:
    return _read_json(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_registry(registry: Mapping[str, object], root: Path = ROOT) -> list[str]:
    schema = _read_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    # Adapt the library method only; input values remain unchecked until validation.
    validator = cast(_SchemaValidator, Draft202012Validator(schema, format_checker=FormatChecker()))
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in validator.iter_errors(registry)
    ]
    for key in ("dependencies", "metrics", "hard_gates", "cases", "suites"):
        ids = [
            identifier
            for item in object_rows(registry.get(key, []))
            if isinstance(identifier := item.get("id"), str)
        ]
        errors.extend(
            f"{key}: duplicate id {value!r}" for value in sorted(set(ids)) if ids.count(value) > 1
        )

    case_schema = _read_json(CASE_SCHEMA_PATH)
    Draft202012Validator.check_schema(case_schema)
    case_validator = cast(_SchemaValidator, Draft202012Validator(case_schema))
    fixture_root = (root / "evaluation/benchmark/fixtures").resolve()
    fixture_cache: dict[Path, dict[str, JsonObject]] = {}
    cases = object_rows(registry.get("cases", []))
    for case in cases:
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
                identifier
                for item in object_rows(fixture.get("cases", []))
                if isinstance(identifier := item.get("id"), str)
            ]
            errors.extend(
                f"fixtures: duplicate case id {value!r}"
                for value in sorted(set(fixture_ids))
                if fixture_ids.count(value) > 1
            )
            fixture_cache[path] = {
                identifier: item
                for item in object_rows(fixture.get("cases", []))
                if isinstance(identifier := item.get("id"), str)
            }
        fixture_cases = fixture_cache.get(path, {})
        case_id = case.get("id")
        if not isinstance(case_id, str) or case_id not in fixture_cases:
            errors.append(f"cases: fixture has no case {case.get('id')!r}")
        else:
            fixture_case = fixture_cases[case_id]
            if fixture_case.get("modalities") != case.get("modalities"):
                errors.append(f"cases: modality mismatch for {case.get('id')!r}")
        if case.get("activation_status") == "pending_owner_decision":
            if not case.get("decision_id"):
                errors.append(f"cases: pending case {case.get('id')!r} requires decision_id")
            if case.get("promotion_eligible") is not False:
                errors.append(
                    f"cases: pending case {case.get('id')!r} cannot be promotion eligible"
                )

    case_ids = {identifier for case in cases if isinstance(identifier := case.get("id"), str)}
    for suite in object_rows(registry.get("suites", [])):
        suite_ids = suite.get("case_ids", [])
        if not is_array(suite_ids):
            continue
        for case_id in suite_ids:
            if not isinstance(case_id, str) or case_id not in case_ids:
                errors.append(f"suites: unknown case {case_id!r}")
        pending: set[str] = {
            identifier
            for case in cases
            if isinstance(identifier := case.get("id"), str)
            and case.get("activation_status") != "active"
        }
        included_pending = pending.intersection(item for item in suite_ids if isinstance(item, str))
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
        category
        for gate in object_rows(registry.get("hard_gates", []))
        if isinstance(category := gate.get("category"), str)
    }
    for category in sorted(required_gate_categories - represented):
        errors.append(f"hard_gates: missing {category!r}")
    for legacy in object_rows(registry.get("legacy_map", [])):
        source_paths = legacy.get("source_paths", [])
        if not is_array(source_paths):
            continue
        for relative in source_paths:
            if isinstance(relative, str) and not (root / relative).is_file():
                errors.append(f"legacy_map: missing source {relative!r}")
    return sorted(errors)


def score_case(case: Mapping[str, object]) -> CaseScore:
    expected = require_object(case["expected"], context="expected case fields")
    candidate = require_object(case["candidate"], context="candidate case fields")
    required_evidence = set(_texts(expected["evidence_ids"], context="expected evidence ids"))
    required_claims = set(_texts(expected["claim_types"], context="expected claim types"))
    candidate_evidence = _texts(candidate["evidence_ids"], context="candidate evidence ids")
    candidate_claims = _texts(candidate["claim_types"], context="candidate claim types")
    evidence_recall = len(required_evidence.intersection(candidate_evidence)) / len(
        required_evidence
    )
    claim_coverage = len(required_claims.intersection(candidate_claims)) / len(required_claims)
    gate_counts = {
        category: len(_texts(violations, context=f"{category} gate violations"))
        for category, violations in require_object(
            candidate["gate_violations"], context="candidate gate violations"
        ).items()
    }
    invalid_citations = set(candidate_evidence) - required_evidence
    citation_validity = 1 - (len(invalid_citations) / len(candidate_evidence))
    abstention_correct = candidate["abstained"] is expected["must_abstain"]
    passed = (
        evidence_recall == 1
        and claim_coverage == 1
        and citation_validity == 1
        and abstention_correct
        and not any(gate_counts.values())
    )
    return {
        "case_id": _text(case["id"], context="case id"),
        "evidence_recall": evidence_recall,
        "claim_type_coverage": claim_coverage,
        "citation_validity": citation_validity,
        "abstention_correct": abstention_correct,
        "gate_violations": gate_counts,
        "robustness_challenge_pass": passed,
        "passed": passed,
    }


def run_suite(registry: Mapping[str, object], suite_id: str) -> BenchmarkReceipt:
    errors = validate_registry(registry)
    if errors:
        raise ValueError("invalid registry: " + "; ".join(errors))
    suite = next((item for item in object_rows(registry["suites"]) if item["id"] == suite_id), None)
    if suite is None:
        raise ValueError(f"unknown suite {suite_id!r}")
    started = time.perf_counter()
    cpu_started = time.process_time()
    tracemalloc.start()
    by_id: dict[str, JsonObject] = {}
    cases = object_rows(registry["cases"])
    for case_meta in cases:
        fixture = _read_json(ROOT / _text(case_meta["path"], context="fixture path"))
        by_id.update(
            {
                _text(case["id"], context="fixture case id"): case
                for case in object_rows(fixture["cases"])
            }
        )
    results: list[CaseScore] = []
    suite_ids = _texts(suite["case_ids"], context="suite case ids")
    for case_id in suite_ids:
        results.append(score_case(by_id[case_id]))
    elapsed = time.perf_counter() - started
    cpu_seconds = time.process_time() - cpu_started
    fixture_paths = sorted(
        {_text(case["path"], context="fixture path") for case in cases if case["id"] in suite_ids}
    )
    context_bytes = sum((ROOT / path).stat().st_size for path in fixture_paths)
    _, peak_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    receipt: _BenchmarkFields = {
        "schema_version": "1.0",
        "benchmark_version": _text(registry["benchmark_version"], context="benchmark version"),
        "suite_id": suite_id,
        "runner": _text(suite["runner"], context="suite runner"),
        "network": _text(suite["network"], context="suite network"),
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
    return {**receipt, "receipt_sha256": hashlib.sha256(canonical).hexdigest()}


def verify_result(result: Mapping[str, object]) -> list[str]:
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
        (item for item in object_rows(registry["suites"]) if item["id"] == result.get("suite_id")),
        None,
    )
    if suite is None:
        errors.append("result suite is unknown")
    else:
        if result.get("runner") != suite["runner"] or result.get("network") != suite["network"]:
            errors.append("result execution contract does not match the suite")
        observations = result.get("results")
        if not is_array(observations):
            errors.append("result observations are missing")
        else:
            observed_ids = [item.get("case_id") for item in observations if is_object(item)]
            if observed_ids != suite["case_ids"]:
                errors.append("result cases do not match the suite")
            for item in observations:
                if not is_object(item):
                    errors.append("result observation is malformed")
                    continue
                gate_counts = item.get("gate_violations")
                if not is_object(gate_counts) or set(gate_counts) != {
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
                item.get("passed") is True for item in observations if is_object(item)
            )
            if not is_object(summary) or summary.get("case_count") != len(observations):
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
    if not is_object(fixture_hashes):
        errors.append("result fixture hashes are missing")
    else:
        for relative, expected_hash in fixture_hashes.items():
            if not isinstance(expected_hash, str):
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


def render_report(result: Mapping[str, object]) -> str:
    summary = require_object(result["summary"], context="result summary")
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
    lines.extend(
        f"- {item}" for item in _texts(result["limitations"], context="result limitations")
    )
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
        result: Mapping[str, object]
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
