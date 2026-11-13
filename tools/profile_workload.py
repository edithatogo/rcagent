"""Deterministic synthetic evidence workload for local Scalene measurements."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import cast

from tools.evidence_core import canonical_bytes, fingerprint, validate_record

FIXTURE = Path(__file__).parents[1] / "tests/fixtures/safety-work/valid-case.json"
ITERATIONS = 300


def run_workload() -> dict[str, int | float | str]:
    """Exercise actual schema validation and provenance hashing, with no network."""
    record = cast("dict[str, object]", json.loads(FIXTURE.read_text(encoding="utf-8")))
    expected = fingerprint(record)
    started = time.perf_counter()
    for _ in range(ITERATIONS):
        errors = validate_record(record)
        if errors:
            raise ValueError(f"synthetic profiling fixture is invalid: {errors}")
        restored = cast("dict[str, object]", json.loads(canonical_bytes(record)))
        if fingerprint(restored) != expected:
            raise ValueError("synthetic profile round-trip changed the evidence hash")
    return {
        "schema_version": "1.0",
        "data_class": "synthetic",
        "workload": "schema-validation-and-provenance-round-trip",
        "iterations": ITERATIONS,
        "wall_seconds": round(time.perf_counter() - started, 6),
        "fixture_sha256": expected,
    }


if __name__ == "__main__":
    print(json.dumps(run_workload(), sort_keys=True))
