from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from tools import local_model_comparator
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


def test_comparator_cli_validate_and_run_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda manifest, root: [])
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda path: {"models": []})
    monkeypatch.setattr(
        sys, "argv", ["comparator", "--model-root", str(tmp_path), "--validate-only"]
    )
    assert local_model_comparator.main() == 0
    assert "validation passed" in capsys.readouterr().out

    output = tmp_path / "result.json"
    monkeypatch.setattr(
        local_model_comparator,
        "run",
        lambda manifest, root, repeats, timeout: {"receipt_sha256": "a" * 64},
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["comparator", "--model-root", str(tmp_path), "--output", str(output)],
    )
    assert local_model_comparator.main() == 0
    assert json.loads(output.read_text())["receipt_sha256"] == "a" * 64


def test_comparator_cli_reports_admission_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda path: {})
    monkeypatch.setattr(
        local_model_comparator, "validate_admission", lambda manifest, root: ["missing model"]
    )
    monkeypatch.setattr(sys, "argv", ["comparator", "--model-root", str(tmp_path)])
    assert local_model_comparator.main() == 1
    assert "ERROR: missing model" in capsys.readouterr().out
