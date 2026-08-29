from __future__ import annotations

from copy import deepcopy

from tools.docling_synthetic_evaluation import (
    REQUIRED_CLASSES,
    load_evaluation,
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
