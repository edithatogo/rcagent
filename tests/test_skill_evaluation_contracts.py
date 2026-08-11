from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
EVAL_ROOT = ROOT / "evaluations/skills/rca-investigation"


def _load(name: str) -> dict:
    return json.loads((EVAL_ROOT / name).read_text(encoding="utf-8"))


def test_trigger_partitions_and_thresholds_are_fail_closed() -> None:
    data = _load("trigger-cases.json")
    cases = data["cases"]
    assert data["thresholds"] == {
        "minimum_trials": 3,
        "positive_rate": 1.0,
        "negative_rate": 0.0,
    }
    partitions = {case["partition"] for case in cases}
    assert {"train", "held_out", "regression_exposed"}.issubset(partitions)
    assert {case["expected"] for case in cases} == {"trigger", "no_trigger"}
    assert len({case["id"] for case in cases}) == len(cases)


def test_output_contract_blocks_unavailable_and_requires_hard_assertions() -> None:
    data = _load("output-cases.json")
    aggregation = data["aggregation"]
    assert aggregation["all_hard_assertions_required"] is True
    assert aggregation["unavailable_is_pass"] is False
    assert aggregation["preserve_raw_observations"] is True
    assert all(case["assertions"] for case in data["cases"])
    assert len({case["id"] for case in data["cases"]}) == len(data["cases"])
