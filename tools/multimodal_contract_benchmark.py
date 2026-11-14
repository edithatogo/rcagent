"""Conservative non-operational benchmark for multimodal contract disclosures."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import tracemalloc
from pathlib import Path
from typing import Literal, TypedDict

from tools import json_shapes
from tools.multimodal_fabric import execution_disclosure, load_registry

ROOT = Path(__file__).parents[1]
RECEIPT = ROOT / "evaluation/multimodal/contract-benchmark-20260829.json"
THRESHOLD_MS = 2000.0
THRESHOLD_BYTES = 1_000_000


class BenchmarkResult(TypedDict):
    profile_id: str
    device_class: Literal["ci-contract"]
    elapsed_ms: float
    allocation_peak_bytes: int
    threshold_ms: float
    threshold_bytes: int
    passed: bool
    scope: str


class BenchmarkSummary(TypedDict):
    profiles: int
    passed: int


class ReceiptBody(TypedDict):
    schema_version: Literal["1.0"]
    benchmark_scope: Literal["conservative_non_operational_ci_contract"]
    results: list[BenchmarkResult]
    summary: BenchmarkSummary
    limitations: list[str]


class BenchmarkReceipt(ReceiptBody):
    receipt_sha256: str


def run() -> BenchmarkReceipt:
    registry = load_registry()
    fixtures = {item["profile_id"]: item["id"] for item in registry["fixtures"]}
    results: list[BenchmarkResult] = []
    for profile in registry["profiles"]:
        started = time.perf_counter()
        tracemalloc.start()
        disclosure = execution_disclosure(registry, profile["id"], fixtures[profile["id"]])
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed = round((time.perf_counter() - started) * 1000, 3)
        results.append(
            {
                "profile_id": profile["id"],
                "device_class": "ci-contract",
                "elapsed_ms": elapsed,
                "allocation_peak_bytes": peak,
                "threshold_ms": THRESHOLD_MS,
                "threshold_bytes": THRESHOLD_BYTES,
                "passed": elapsed <= THRESHOLD_MS
                and peak <= THRESHOLD_BYTES
                and disclosure["supported"] is False,
                "scope": "deterministic disclosure contract only; not adapter quality or runtime performance",
            }
        )
    receipt: ReceiptBody = {
        "schema_version": "1.0",
        "benchmark_scope": "conservative_non_operational_ci_contract",
        "results": results,
        "summary": {
            "profiles": len(results),
            "passed": sum(1 for item in results if item["passed"] is True),
        },
        "limitations": [
            "No framework or model benchmark",
            "Thresholds detect contract regressions only",
            "No deployment suitability claim",
        ],
    }
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    return {**receipt, "receipt_sha256": hashlib.sha256(payload).hexdigest()}


def verify(receipt: object) -> list[str]:
    if not json_shapes.is_object(receipt):
        return ["receipt must be an object"]
    errors: list[str] = []
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    digest = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if receipt.get("receipt_sha256") != digest:
        errors.append("receipt hash mismatch")
    results = receipt.get("results", [])
    if not json_shapes.is_array(results):
        return [*errors, "results must be an array"]
    profile_ids = [item.get("profile_id") for item in json_shapes.object_rows(results)]
    if any(not isinstance(profile_id, str) for profile_id in profile_ids) or {
        profile_id for profile_id in profile_ids if isinstance(profile_id, str)
    } != {item["id"] for item in load_registry()["profiles"]}:
        errors.append("profile coverage mismatch")
    for item in results:
        if not json_shapes.is_object(item):
            errors.append("benchmark result must be an object")
            continue
        elapsed = item.get("elapsed_ms")
        allocation = item.get("allocation_peak_bytes")
        valid = (
            item.get("device_class") == "ci-contract"
            and item.get("threshold_ms") == THRESHOLD_MS
            and item.get("threshold_bytes") == THRESHOLD_BYTES
            and isinstance(elapsed, (int, float))
            and not isinstance(elapsed, bool)
            and elapsed >= 0
            and elapsed <= THRESHOLD_MS
            and isinstance(allocation, int)
            and not isinstance(allocation, bool)
            and allocation >= 0
            and allocation <= THRESHOLD_BYTES
            and item.get("passed") is True
        )
        if not valid:
            errors.append(f"benchmark result failed: {item.get('profile_id')!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = run()
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if verify(receipt) else 0


if __name__ == "__main__":
    raise SystemExit(main())
