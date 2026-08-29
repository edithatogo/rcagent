from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from tools import agent_panel_review
from tools.agent_panel_review import (
    CRITERIA,
    _ordinal_alpha,
    _read,
    _weighted_kappa,
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


def test_panel_cli_writes_reproducible_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "panel.json"
    submissions = [
        ROOT / "evaluation/benchmark/panel/blind-rater-a.json",
        ROOT / "evaluation/benchmark/panel/blind-rater-b.json",
        ROOT / "evaluation/benchmark/panel/blind-challenger.json",
    ]
    monkeypatch.setattr(
        sys,
        "argv",
        ["agent-panel", *(str(path) for path in submissions), "--output", str(output)],
    )
    assert agent_panel_review.main() == 0
    assert json.loads(output.read_text())["threshold_pass"] is False


def test_panel_cli_prints_receipt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    submission = ROOT / "evaluation/benchmark/panel/blind-rater-a.json"
    monkeypatch.setattr(
        sys, "argv", ["agent-panel", str(submission), str(submission), str(submission)]
    )
    monkeypatch.setattr(agent_panel_review, "aggregate", lambda values: {"threshold_pass": False})
    assert agent_panel_review.main() == 0
    assert '"threshold_pass": false' in capsys.readouterr().out


def test_panel_validators_reject_tampered_evidence(tmp_path: Path) -> None:
    invalid = tmp_path / "array.json"
    invalid.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="expected an object"):
        _read(invalid)

    submission = _submission("tampered")
    submission["ratings"][1]["model_id"] = submission["ratings"][0]["model_id"]
    submission["input_hashes"] = {key: "0" * 64 for key in submission["input_hashes"]}
    submission["ratings"][0]["criteria"].pop("uncertainty")
    submission["ratings"][0]["criteria"]["privacy"]["evidence"] = ["missing-case"]
    errors = validate_submission(submission)
    assert any("duplicate model_id" in error for error in errors)
    assert any("does not match" in error for error in errors)
    assert any("canonical rubric" in error for error in errors)
    assert any("unknown evidence" in error for error in errors)


def test_adjudication_and_governance_tampering_is_detected() -> None:
    adjudication = json.loads(
        (ROOT / "evaluation/benchmark/results/agent-panel-v1-adjudication.json").read_text()
    )
    adjudication["input_hashes"] = {}
    adjudication["instructions_sha256"] = "0" * 64
    adjudication["scores_changed"] = True
    errors = validate_adjudication(adjudication)
    assert len(errors) >= 4

    thresholds = json.loads((ROOT / "evaluation/benchmark/research-thresholds.json").read_text())
    thresholds["receipt_sha256"] = "0" * 64
    thresholds["current_observation"]["raw_agent_panel_agreement"] = 1
    thresholds["current_observation"]["ordinal_agent_panel_alpha"] = 1
    thresholds["current_observation"]["panel_gate_coverage_complete"] = True
    assert len(validate_governance_evidence(thresholds)) >= 4

    gates = json.loads(
        (ROOT / "evaluation/benchmark/results/hard-gate-evidence-v1.json").read_text()
    )
    gates["gate_evidence"].pop("security")
    assert any("five approved hard gates" in error for error in validate_governance_evidence(gates))


def test_agreement_helpers_reject_empty_or_unpaired_values() -> None:
    with pytest.raises(ValueError, match="paired"):
        _weighted_kappa([], [])
    with pytest.raises(ValueError, match="two raters"):
        _ordinal_alpha([[1]])
