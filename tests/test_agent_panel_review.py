from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools.agent_panel_review import (
    CRITERIA,
    aggregate,
    validate_adjudication,
    validate_governance_evidence,
    validate_submission,
)

ROOT = Path(__file__).parents[1]


def _submission(reviewer: str, score: int = 2) -> dict:
    criteria = {
        criterion: {
            "score": score,
            "evidence": ["incomplete-evidence"],
            "rationale": "Synthetic evidence.",
        }
        for criterion in CRITERIA
    }
    return {
        "schema_version": "1.0",
        "reviewer_id": reviewer,
        "reviewer_class": "agent",
        "role": "reproducibility_rater",
        "context_isolation": "blind_no_peer_outputs",
        "agent_revision": "test-agent",
        "tools": [],
        "network": "not_used",
        "correlated_error_limitations": "shared test fixture",
        "input_hashes": {
            "rubric_sha256": hashlib.sha256(
                (ROOT / "evaluation/benchmark/agent-panel-rubric.md").read_bytes()
            ).hexdigest(),
            "comparator_file_sha256": hashlib.sha256(
                (ROOT / "evaluation/benchmark/results/local-comparators-v1.json").read_bytes()
            ).hexdigest(),
            "comparator_receipt_sha256": json.loads(
                (ROOT / "evaluation/benchmark/results/local-comparators-v1.json").read_text()
            )["receipt_sha256"],
            "fixtures_sha256": hashlib.sha256(
                (ROOT / "evaluation/benchmark/fixtures/synthetic-cases.json").read_bytes()
            ).hexdigest(),
        },
        "ratings": [
            {
                "model_id": model,
                "criteria": deepcopy(criteria),
                "abstain": False,
                "uncertainty": "none",
                "hard_gate_flags": [],
            }
            for model in ("small", "medium", "large")
        ],
        "overall_recommendation": "conditional",
    }


def test_unanimous_panel_still_fails_incomplete_gate_coverage() -> None:
    receipt = aggregate([_submission("a"), _submission("b"), _submission("c")])
    assert receipt["threshold_pass"] is False
    assert receipt["panel_gate_coverage_complete"] is False
    assert receipt["agreement"]["raw_exact_agreement"] == 1
    assert receipt["recommendation"] == "revise_rubric_or_unsupported"


def test_hard_gate_zero_requires_matching_flag_and_blocks() -> None:
    first = _submission("a")
    first["ratings"][0]["criteria"]["privacy"]["score"] = 0
    assert validate_submission(first)
    first["ratings"][0]["hard_gate_flags"] = ["privacy"]
    receipt = aggregate([first, _submission("b"), _submission("c")])
    assert receipt["threshold_pass"] is False


def test_panel_rejects_duplicate_reviewers() -> None:
    with pytest.raises(ValueError, match="unique"):
        aggregate([_submission("a"), _submission("a"), _submission("c")])


def test_frozen_adjudication_receipt_validates() -> None:
    value = json.loads(
        (ROOT / "evaluation/benchmark/results/agent-panel-v1-adjudication.json").read_text()
    )
    assert validate_adjudication(value) == []


@pytest.mark.parametrize(
    "path",
    [
        "evaluation/benchmark/research-thresholds.json",
        "evaluation/benchmark/results/hard-gate-evidence-v1.json",
    ],
)
def test_governance_evidence_validates(path: str) -> None:
    value = json.loads((ROOT / path).read_text())
    assert validate_governance_evidence(value) == []
