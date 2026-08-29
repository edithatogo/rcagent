from __future__ import annotations

from copy import deepcopy

import pytest

from tools.docling_synthetic_evaluation import (
    REQUIRED_CLASSES,
    load_evaluation,
    main,
    validate_evaluation,
)


def test_evaluation_is_synthetic_bounded_and_complete() -> None:
    value = load_evaluation()
    assert validate_evaluation(value) == []
    assert {case["class"] for case in value["cases"]} == REQUIRED_CLASSES
    assert value["adapter"]["portable_core_dependency"] is False
    assert value["execution_boundary"]["network"] == "disabled during evaluation"
    assert [case["state"] for case in value["cases"]].count("measured_contract") == 1


def test_missing_provenance_and_unsafe_boundary_fail_closed() -> None:
    value = deepcopy(load_evaluation())
    value["cases"][0]["output"].pop("region")
    value["execution_boundary"]["remote_code"] = "allowed"
    errors = validate_evaluation(value)
    assert any("region and confidence" in error for error in errors)
    assert any("remote_code" in error for error in errors)
    assert any("receipt hash mismatch" in error for error in errors)


def test_malformed_evaluation_reports_all_fail_closed_states(tmp_path) -> None:
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="must be an object"):
        load_evaluation(path)
    value = load_evaluation()
    value["cases"] = "invalid"
    assert "cases must be an array" in validate_evaluation(value)
    value = load_evaluation()
    case = value["cases"][0]
    case["state"] = "enabled"
    case.pop("source")
    case["output"] = "invalid"
    value["cases"] = [case, case, 3]
    errors = validate_evaluation(value)
    assert "case identifiers must be unique" in errors
    assert "case must be an object" in errors
    assert any("invalid state" in error for error in errors)
    assert any("missing source" in error for error in errors)


def test_cli_validate_report_and_error(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["docling", "validate"])
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["docling", "report"])
    assert main() == 0
    assert '"profile_id": "documents-ocr"' in capsys.readouterr().out
    monkeypatch.setattr(
        "tools.docling_synthetic_evaluation.load_evaluation",
        lambda: {"cases": "invalid"},
    )
    monkeypatch.setattr("sys.argv", ["docling", "validate"])
    assert main() == 1
    assert "ERROR:" in capsys.readouterr().out
