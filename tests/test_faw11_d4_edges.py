"""Focused admission, comparator and command-surface branch regressions for D4."""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256

import pytest

from tools import faw11_d4_comparison as d4
from tools import workbench
from tools.faw10_d3_decision_view import generate_receipt as generate_d3_receipt
from tools.json_shapes import JsonObject, is_array, require_object


def _case() -> JsonObject:
    source = generate_d3_receipt()
    inputs = source["inputs"]
    assert is_array(inputs)
    return deepcopy(require_object(inputs[0], context="synthetic D3 case"))


def _scenario() -> tuple[
    JsonObject, d4.D4View, list[JsonObject], list[JsonObject], list[JsonObject]
]:
    case = _case()
    view = d4.make_view(case, "family-root-1", "test")
    study: list[JsonObject] = [
        {"root_family_id": "family-root-1", "partition": "test", "case": case}
    ]
    references: list[JsonObject] = [
        {
            "view_fingerprint": view["view_fingerprint"],
            "event_id": "concern",
            "expected_kind": "patient_family_concern",
            "reference_origin": "independently_authored_synthetic",
        }
    ]
    arms: list[JsonObject] = [
        {
            "method": "regex",
            "status": "executed",
            "revision": "regex-synthetic-test",
            "predictions": d4.regex_predictions(case, view),
            "measured_resources": None,
        }
    ]
    for name in ("token_section_context", "linear_classifier", "structured_generation"):
        arms.append({"method": name, "status": "unavailable", "reason": "not run"})
    return case, view, study, references, arms


@pytest.mark.parametrize("partition", ["train", "development"])
def test_non_test_partition_is_allowed_as_input_without_test_label_scoring(
    partition: str,
) -> None:
    case = _case()
    assert d4.make_view(case, "family-root", partition)["partition"] == partition
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(
            [{"root_family_id": "family-root", "partition": partition, "case": case}],
            [],
            [],
        )


@pytest.mark.parametrize("invalid", ["holdout", "", None, 7])
def test_unknown_partition_rejected(invalid: object) -> None:
    with pytest.raises(ValueError, match="invalid or inadmissible D4 view"):
        d4.make_view(_case(), "family", invalid)


@pytest.mark.parametrize("invalid", ["", "x" * 129, None, 9])
def test_invalid_family_identity_rejected(invalid: object) -> None:
    with pytest.raises(ValueError, match="invalid or inadmissible D4 view"):
        d4.make_view(_case(), invalid, "test")


@pytest.mark.parametrize("kind", ["observation", "outcome", "appraisal", "patient_family_concern"])
def test_all_fixed_reference_labels_are_explicitly_scored(kind: str) -> None:
    _, _, study, refs, arms = _scenario()
    refs[0]["expected_kind"] = kind
    result = d4.compare_arms(study, refs, arms)
    score = require_object(result["scores"]["regex"], context="score")
    assert score["eligible"] == 1
    assert score["correct"] == int(kind == "patient_family_concern")


@pytest.mark.parametrize("kind", ["wrong-kind", "unk", 17, None])
def test_unrecognised_reference_label_rejected(kind: object) -> None:
    _, _, study, refs, arms = _scenario()
    refs[0]["expected_kind"] = kind
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


@pytest.mark.parametrize("method", ["not-a-method", None, 0])
def test_invalid_method_disposition_rejected(method: object) -> None:
    _, _, study, refs, arms = _scenario()
    arms[0]["method"] = method
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


@pytest.mark.parametrize("status", ["maybe", None, 3])
def test_unknown_method_execution_status_rejected(status: object) -> None:
    _, _, study, refs, arms = _scenario()
    arms[0]["status"] = status
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_resource_claims_are_rejected_without_independent_execution_proof() -> None:
    _, _, study, refs, arms = _scenario()
    arms[0]["measured_resources"] = {"wall_ms": 1}
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_missing_method_and_duplicate_method_are_rejected() -> None:
    _, _, study, refs, arms = _scenario()
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms[:-1])
    arms[-1]["method"] = "regex"
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_missing_or_duplicated_reference_is_not_counted_as_a_correct_case() -> None:
    _, _, study, refs, arms = _scenario()
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, [], arms)
    refs.append(deepcopy(refs[0]))
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_wrong_reference_origin_rejected_even_with_correct_label() -> None:
    _, _, study, refs, arms = _scenario()
    refs[0]["reference_origin"] = "generated_from_predictions"
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_duplicate_test_view_and_empty_study_rejected() -> None:
    _, _, study, refs, arms = _scenario()
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms([], refs, arms)
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms([*study, *study], refs, arms)


@pytest.mark.parametrize("key", ["root_family_id", "partition", "case"])
def test_study_requires_exact_fields(key: str) -> None:
    _, _, study, refs, arms = _scenario()
    del study[0][key]
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms)


def test_bounded_array_admission_rejects_non_array_and_excessive_cases() -> None:
    _, _, study, refs, arms = _scenario()
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms("not an array", refs, arms)
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study * 129, refs, arms)
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        d4.compare_arms(study, refs, arms * 2)


@pytest.mark.parametrize(
    ("text", "label"),
    [
        ("Test result demonstrates an adverse outcome", "outcome"),
        ("Independent review conclusion", "appraisal"),
        ("Patient stable", "observation"),
        ("Family reported concern", "patient_family_concern"),
    ],
)
def test_fixed_lexical_reference_arm_categories(text: str, label: str) -> None:
    # Exercise the public replay boundary, not the private, unscoped rules.
    case = _case()
    timeline = require_object(case["timeline"], context="D3 timeline")
    source_list = timeline["sources"]
    assert is_array(source_list)
    source = require_object(source_list[0], context="D3 source")
    original = source["content"]
    assert isinstance(original, str)
    previous = "Family reported persistent concern."
    updated = original.replace(previous, text)
    digest = "sha256:" + sha256(updated.encode("utf-8")).hexdigest()
    source["content"] = updated
    source["fingerprint"] = digest
    for category in ("events", "clocks", "relations", "amendments"):
        rows = timeline[category]
        assert is_array(rows)
        for item in rows:
            observation = require_object(item, context="D3 observation")
            evidence = require_object(observation["evidence"], context="source span")
            if evidence["source_id"] != "early":
                continue
            existing = evidence["text"]
            assert isinstance(existing, str)
            quote = text if existing == previous else existing
            start = updated.index(quote)
            evidence["text"] = quote
            evidence["start_byte"] = len(updated[:start].encode("utf-8"))
            evidence["end_byte"] = len(updated[: start + len(quote)].encode("utf-8"))
            evidence["source_sha256"] = digest
    label_rows = case["labels"]
    assert is_array(label_rows)
    for row in label_rows:
        category = require_object(row, context="D3 event label")
        if category["event_id"] == "concern":
            category["kind"] = label
            category["speaker_role"] = "family" if label == "patient_family_concern" else None
    view = d4.make_view(case, "family-root-1", "test")
    observed = d4.regex_predictions(case, view)
    assert observed[0]["predicted_kind"] == label


def test_demo_generator_fails_closed_when_its_source_input_disappears(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def absent_inputs() -> JsonObject:
        return {"inputs": []}

    monkeypatch.setattr(d4, "d3_generate_receipt", absent_inputs)
    with pytest.raises(ValueError, match="synthetic D3 input"):
        d4.generate_receipt()


def test_demo_generator_rejects_changed_event_fixture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actual = d4.make_view(_case(), "synthetic-demo-family-1", "test")
    actual["events"] = []

    def altered_view(_case_value: object, _root: object, _partition: object) -> d4.D4View:
        return actual

    monkeypatch.setattr(d4, "make_view", altered_view)
    with pytest.raises(ValueError, match="frozen D4 demo label"):
        d4.generate_receipt()


def test_demo_main_runs_in_current_process_and_workbench_routes_it(
    capfd: pytest.CaptureFixture[str],
) -> None:
    assert d4.main([]) == 0
    first = capfd.readouterr()
    result: object = json.loads(first.out)
    assert require_object(result, context="D4 output")["task"] == "FAW11/D4"
    assert workbench.main(["d4-demo"]) == 0
    second = capfd.readouterr()
    other: object = json.loads(second.out)
    assert require_object(other, context="workbench D4")["task"] == "FAW11/D4"


def test_demo_main_handles_output_write_failure_without_success_claim(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _ShortBuffer:
        def write(self, data: bytes) -> int:
            return len(data) - 1

        def flush(self) -> None:
            return None

    class _Stdout:
        def __init__(self) -> None:
            self.buffer = _ShortBuffer()

    monkeypatch.setattr(d4.sys, "stdout", _Stdout())
    assert d4.main([]) == 1
