"""FAW11/D4 synthetic comparison contract: test-first, no model qualification."""

from __future__ import annotations

from copy import deepcopy

import pytest

from tools.faw10_d3_decision_view import generate_receipt
from tools.faw11_d4_comparison import (
    compare_arms,
    make_view,
    regex_predictions,
)


def _case() -> dict[str, object]:
    sample = generate_receipt()["inputs"][0]
    return deepcopy(sample)


def _study(raw: dict[str, object] | None = None) -> list[dict[str, object]]:
    return [
        {
            "root_family_id": "independent-synthetic-root-01",
            "partition": "test",
            "case": _case() if raw is None else raw,
        }
    ]


def _reference(view: dict[str, object]) -> list[dict[str, object]]:
    events = view["events"]
    assert isinstance(events, list)
    return [
        {
            "view_fingerprint": view["view_fingerprint"],
            "event_id": event["event_id"],
            "expected_kind": "patient_family_concern",
            "reference_origin": "independently_authored_synthetic",
        }
        for event in events
    ]


def _arms(view: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            "method": "regex",
            "status": "executed",
            "revision": "faw11-d4-regex-1.0",
            "predictions": regex_predictions(view),
            "measured_resources": None,
        },
        *[
            {
                "method": name,
                "status": "unavailable",
                "reason": "no pinned runtime, model or labelled-resource admission",
            }
            for name in (
                "token_section_context",
                "linear_classifier",
                "structured_generation",
            )
        ],
    ]


def test_model_view_contains_only_d3_visible_evidence_not_labels() -> None:
    view = make_view(_case(), "independent-synthetic-root-01", "test")
    assert view["case_id"] == "d3-synthetic"
    assert view["event_count"] == 1
    assert view["family_concern_labels_in_model_input"] is False
    assert view["events"][0]["event_id"] == "concern"
    rendered = str(view)
    assert "patient_family_concern" not in rendered
    assert "Later test result" not in rendered
    assert "changed the outcome" not in rendered
    assert "speaker_role" not in rendered
    assert "source_entitlement_basis" not in rendered


def test_future_label_change_cannot_change_d4_view() -> None:
    original = _case()
    future_modified = deepcopy(original)
    labels = future_modified["labels"]
    assert isinstance(labels, list)
    labels[1] = {"event_id": "result", "kind": "appraisal", "speaker_role": None}
    before = make_view(original, "root-01", "test")
    after = make_view(future_modified, "root-01", "test")
    assert before == after


def test_comparison_reports_actual_denominators_and_all_missing_arms() -> None:
    study = _study()
    view = make_view(study[0]["case"], "independent-synthetic-root-01", "test")
    outcome = compare_arms(study, _reference(view), _arms(view))
    assert outcome["schema_version"] == "faw11-d4-comparison-1.0"
    assert outcome["status"] == "incomplete_unqualified"
    assert outcome["independent_test_families"] == 1
    assert outcome["eligible_test_events"] == 1
    assert outcome["model_executed"] is False
    scores = outcome["scores"]
    assert scores["regex"]["covered"] == 1
    assert scores["regex"]["correct"] == 1
    assert scores["regex"]["accuracy_full_denominator"] == 1.0
    assert scores["regex"]["macro_f1"] == 0.25
    for method in (
        "token_section_context",
        "linear_classifier",
        "structured_generation",
    ):
        assert scores[method]["status"] == "unavailable"
        assert scores[method]["covered"] == 0
        assert scores[method]["accuracy_full_denominator"] is None


def test_abstentions_are_not_successes_or_excluded_from_denominator() -> None:
    study = _study()
    view = make_view(study[0]["case"], "independent-synthetic-root-01", "test")
    arms = _arms(view)
    arms[0]["predictions"] = [
        {
            "view_fingerprint": view["view_fingerprint"],
            "event_id": "concern",
            "predicted_kind": None,
        }
    ]
    scores = compare_arms(study, _reference(view), arms)["scores"]
    assert scores["regex"]["covered"] == 0
    assert scores["regex"]["abstentions"] == 1
    assert scores["regex"]["correct"] == 0
    assert scores["regex"]["accuracy_full_denominator"] == 0.0
    assert scores["regex"]["macro_f1"] == 0.0
    assert scores["regex"]["accuracy_covered_only"] is None


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "future", "unknown"])
def test_rejects_incomplete_duplicate_or_cross_view_predictions(mutation: str) -> None:
    study = _study()
    view = make_view(study[0]["case"], "independent-synthetic-root-01", "test")
    arms = _arms(view)
    predictions = arms[0]["predictions"]
    assert isinstance(predictions, list)
    if mutation == "missing":
        predictions.clear()
    elif mutation == "duplicate":
        predictions.append(deepcopy(predictions[0]))
    elif mutation == "future":
        predictions.append(
            {
                "view_fingerprint": view["view_fingerprint"],
                "event_id": "result",
                "predicted_kind": "outcome",
            }
        )
    else:
        predictions[0]["view_fingerprint"] = "sha256:stale"
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        compare_arms(study, _reference(view), arms)


def test_no_root_family_leakage_across_partitions() -> None:
    raw = _case()
    other = deepcopy(raw)
    other["cutoff_utc"] = "2026-11-17T13:00:00Z"
    study = [
        {"root_family_id": "root", "partition": "train", "case": raw},
        {"root_family_id": "root", "partition": "test", "case": other},
    ]
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        compare_arms(study, [], [])


def test_reference_outside_actor_cutoff_is_rejected() -> None:
    study = _study()
    view = make_view(study[0]["case"], "independent-synthetic-root-01", "test")
    references = _reference(view)
    references.append(
        {
            "view_fingerprint": view["view_fingerprint"],
            "event_id": "result",
            "expected_kind": "outcome",
            "reference_origin": "independently_authored_synthetic",
        }
    )
    with pytest.raises(ValueError, match="invalid or inadmissible D4 comparison"):
        compare_arms(study, references, _arms(view))


def test_malformed_future_input_error_does_not_echo_excluded_identifier() -> None:
    raw = _case()
    timeline = raw["timeline"]
    assert isinstance(timeline, dict)
    events = timeline["events"]
    assert isinstance(events, list)
    events[1]["id"] = "SECRET-FUTURE-EVENT"
    with pytest.raises(ValueError, match="invalid or inadmissible D4 view") as caught:
        make_view(raw, "root", "test")
    assert "SECRET-FUTURE-EVENT" not in str(caught.value)


def test_no_fake_full_comparison_when_any_method_unavailable() -> None:
    study = _study()
    view = make_view(study[0]["case"], "independent-synthetic-root-01", "test")
    outcome = compare_arms(study, _reference(view), _arms(view))
    assert outcome["paired_comparison_admissible"] is False
    assert outcome["clinical_qualification"] == "none"
    assert outcome["model_qualification"] == "none"
