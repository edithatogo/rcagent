from __future__ import annotations

import json
from pathlib import Path

from tools.local_model_comparator import _extract_object, _score, validate_admission


def test_extract_and_score_valid_response() -> None:
    response = _extract_object(
        '```json\n{"evidence_ids":["e1"],"claim_types":["unknown"],"abstained":true,"rationale":"Missing."}\n```'
    )
    score = _score(
        {"evidence_ids": ["e1"], "claim_types": ["unknown"], "must_abstain": True}, response
    )
    assert score["passed"] is True


def test_score_rejects_non_boolean_abstention() -> None:
    response = {
        "evidence_ids": ["e1"],
        "claim_types": ["unknown"],
        "abstained": ["person"],
        "rationale": "No.",
    }
    score = _score(
        {"evidence_ids": ["e1"], "claim_types": ["unknown"], "must_abstain": True}, response
    )
    assert score["schema_valid"] is False
    assert score["passed"] is False


def test_admission_fails_closed_without_all_size_classes(tmp_path: Path) -> None:
    manifest = json.loads(
        (Path(__file__).parents[1] / "evaluation/benchmark/comparators.json").read_text()
    )
    manifest["models"] = []
    errors = validate_admission(manifest, tmp_path)
    assert "models: exactly small, medium, and larger classes must be admitted" in errors
