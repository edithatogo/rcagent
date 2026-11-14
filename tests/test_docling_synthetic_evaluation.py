from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools import json_shapes
from tools.docling_synthetic_evaluation import (
    REQUIRED_CLASSES,
    load_evaluation,
    main,
    validate_evaluation,
)


def cases(value: json_shapes.JsonObject) -> list[json_shapes.JsonObject]:
    entries = value["cases"]
    assert json_shapes.is_array(entries)
    return [
        json_shapes.require_object(entry, context="stored evaluation case") for entry in entries
    ]


def test_evaluation_is_synthetic_bounded_and_complete() -> None:
    value = load_evaluation()
    assert validate_evaluation(value) == []
    assert {case["class"] for case in cases(value)} == REQUIRED_CLASSES
    adapter = json_shapes.require_object(value["adapter"], context="stored adapter")
    boundary = json_shapes.require_object(value["execution_boundary"], context="stored boundary")
    assert adapter["portable_core_dependency"] is False
    assert boundary["network"] == "disabled during evaluation"
    assert [case["state"] for case in cases(value)].count("measured_contract") == 1


def test_missing_provenance_and_unsafe_boundary_fail_closed() -> None:
    value = deepcopy(load_evaluation())
    output = json_shapes.require_object(cases(value)[0]["output"], context="stored output")
    output.pop("region")
    boundary = json_shapes.require_object(value["execution_boundary"], context="stored boundary")
    boundary["remote_code"] = "allowed"
    errors = validate_evaluation(value)
    assert any("region and confidence" in error for error in errors)
    assert any("remote_code" in error for error in errors)
    assert any("receipt hash mismatch" in error for error in errors)


def test_malformed_evaluation_reports_all_fail_closed_states(tmp_path: Path) -> None:
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="must be an object"):
        load_evaluation(path)
    value = load_evaluation()
    value["cases"] = "invalid"
    assert "cases must be an array" in validate_evaluation(value)
    value = load_evaluation()
    case = cases(value)[0]
    case["state"] = "enabled"
    case.pop("source")
    case["output"] = "invalid"
    value["cases"] = [case, case, 3]
    errors = validate_evaluation(value)
    assert "case identifiers must be unique" in errors
    assert "case must be an object" in errors
    assert any("invalid state" in error for error in errors)
    assert any("missing source" in error for error in errors)


@pytest.mark.parametrize("field", ["execution_boundary", "class", "id", "state"])
def test_rehashed_malformed_fields_return_errors(field: str) -> None:
    value = load_evaluation()
    if field == "execution_boundary":
        value[field] = None
    else:
        cases(value)[0][field] = []
    unsigned = {key: item for key, item in value.items() if key != "receipt_sha256"}
    value["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    errors = validate_evaluation(value)
    assert errors
    assert errors == sorted(errors)
    assert "receipt hash mismatch" not in errors


def test_cli_validate_report_and_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
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
