"""Predeclared synthetic B1 reference families; adversarial evaluation behaviour."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

import pytest

from tools.evidence_core import canonical_bytes
from tools.faw11_b1_evaluation import (
    build_case,
    context_predictions,
    evaluate_frozen,
    fit_linear,
    linear_predictions,
    load_frozen,
    validate_frozen,
)
from tools.faw11_d4_comparison import make_view
from tools.json_shapes import JsonObject, is_array, require_object


def test_frozen_manifest_is_separate_from_predictor_outputs() -> None:
    rows = load_frozen()
    assert len(rows) == 48
    assert len({row["id"] for row in rows}) == 48
    assert len({row["root_family_id"] for row in rows}) == 24
    assert [
        sum(row["partition"] == p for row in rows) for p in ("train", "development", "test")
    ] == [24, 8, 16]
    assert all(
        row["expected_kind"] in ("observation", "outcome", "appraisal", "patient_family_concern")
        for row in rows
    )
    assert {row["expected_kind"] for row in rows if row["partition"] == "test"} == {
        "observation",
        "outcome",
        "appraisal",
        "patient_family_concern",
    }


def test_generated_d3_case_has_source_identity_and_label_free_d4_input() -> None:
    row = load_frozen()[0]
    raw = build_case(row)
    view = make_view(raw, row["root_family_id"], row["partition"])
    assert view["case_id"] == row["id"]
    assert view["event_count"] == 1
    assert view["events"][0]["text"] == row["text"]
    assert "expected_kind" not in str(view)
    source = require_object(raw["timeline"], context="timeline")
    sources = source["sources"]
    assert is_array(sources)
    witness = require_object(sources[0], context="source")
    assert (
        witness["fingerprint"]
        == "sha256:" + sha256(str(witness["content"]).encode("utf-8")).hexdigest()
    )


def test_identical_test_input_never_receives_test_label_during_fitting() -> None:
    rows = load_frozen()
    train = [row for row in rows if row["partition"] == "train"]
    model = fit_linear(
        [
            (make_view(build_case(row), row["root_family_id"], "train"), row["expected_kind"])
            for row in train
        ]
    )
    chosen = next(row for row in rows if row["partition"] == "test")
    view = make_view(build_case(chosen), chosen["root_family_id"], "test")
    a = linear_predictions(model, view)
    modified = deepcopy(chosen)
    modified["expected_kind"] = "observation"
    b = linear_predictions(
        model, make_view(build_case(modified), modified["root_family_id"], "test")
    )
    assert a == b
    assert a[0]["predicted_kind"] is None or a[0]["predicted_kind"] in (
        "observation",
        "outcome",
        "appraisal",
        "patient_family_concern",
    )


def test_context_rules_conservatively_refuse_negation_and_detect_family_concern() -> None:
    rows = load_frozen()
    negation = next(
        row for row in rows if row["text"] == "No family concerns were expressed in this note."
    )
    concern = next(
        row for row in rows if row["text"] == "Mother raised concern about treatment delay."
    )
    outcome = next(
        row for row in rows if row["text"] == "Laboratory result confirmed the diagnosis."
    )
    appraisal = next(
        row for row in rows if row["text"] == "Review concluded a systems redesign was needed."
    )

    def predict(row: JsonObject) -> object:
        view = make_view(build_case(row), row["root_family_id"], row["partition"])
        return context_predictions(build_case(row), view)[0]["predicted_kind"]

    assert predict(negation) != "patient_family_concern"
    assert predict(concern) == "patient_family_concern"
    assert predict(outcome) == "outcome"
    assert predict(appraisal) == "appraisal"


def test_manifest_rejects_family_leakage_and_duplicate_case_id() -> None:
    rows = load_frozen()
    bad = deepcopy(rows)
    bad[0]["partition"] = "test"
    with pytest.raises(ValueError, match="invalid frozen B1 corpus"):
        validate_frozen(bad)
    duplicate = deepcopy(rows)
    duplicate[1]["id"] = duplicate[0]["id"]
    with pytest.raises(ValueError, match="invalid frozen B1 corpus"):
        validate_frozen(duplicate)


def test_b1_report_honestly_denominates_unavailable_generator() -> None:
    report = evaluate_frozen()
    assert report["schema_version"] == "faw11-b1-evaluation-1.0"
    assert report["scope"] == "synthetic_development_only_not_clinical_or_confirmatory"
    assert report["test_cases"] == 16
    assert report["test_root_families"] == 8
    assert report["train_cases"] == 24
    assert report["development_cases"] == 8
    assert report["model_executed"] is True  # conventional fitted linear model only
    assert report["llm_executed"] is False
    assert report["checkpoint_b_claim"] == "not_qualified"
    scores = require_object(report["scores"], context="scores")
    assert require_object(scores["regex"], context="regex")["eligible"] == 16
    assert require_object(scores["token_section_context"], context="NLP")["eligible"] == 16
    assert require_object(scores["linear_classifier"], context="linear")["eligible"] == 16
    assert (
        require_object(scores["structured_generation"], context="generator")["status"]
        == "unavailable"
    )
    metrics = require_object(report["class_metrics"], context="per-class metrics")
    for method in ("regex", "token_section_context", "linear_classifier"):
        table = require_object(metrics[method], context=method)
        for kind in ("observation", "outcome", "appraisal", "patient_family_concern"):
            row = require_object(table[kind], context=kind)
            support, tp, fn = row["support"], row["tp"], row["fn"]
            assert type(support) is int
            assert type(tp) is int
            assert type(fn) is int
            assert support == 4
            assert 0 <= tp <= support
            assert 0 <= fn <= support
    assert "sha256:" in str(report["frozen_manifest_sha256"])


def test_report_is_deterministic_and_no_oracle_labels_in_scoped_views() -> None:
    first = evaluate_frozen()
    second = evaluate_frozen()
    assert canonical_bytes(first) == canonical_bytes(second)
    manifest = load_frozen()
    row = next(item for item in manifest if item["partition"] == "test")
    view = make_view(build_case(row), row["root_family_id"], "test")
    label = row["expected_kind"]
    assert "expected_kind" not in str(view)
    assert view["events"][0]["text"] == row["text"]
    assert label in ("observation", "outcome", "appraisal", "patient_family_concern")

@pytest.mark.parametrize(
    ("source_text", "expected"),
    [
        ("No family concerns were expressed in this note.", None),
        ("The mother expressed no concerns about the care.", None),
        (
            "No family concerns were expressed; however, the mother later raised a concern.",
            "patient_family_concern",
        ),
        ("No injury was reported. A new rash developed later.", "outcome"),
        (
            "The patient did not raise concern, but later expressed worry about the delay.",
            "patient_family_concern",
        ),
    ],
)
def test_context_rules_scope_negation_within_clauses(
    source_text: str, expected: object
) -> None:
    """Negation cannot be defeated by a later synonym in the same clause."""
    row: JsonObject = {
        "id": "b1-negation-clause",
        "root_family_id": "b1-negation-clause",
        "partition": "test",
        "expected_kind": "observation",
        "text": source_text,
    }
    case = build_case(row)
    view = make_view(case, row["root_family_id"], "test")
    assert context_predictions(case, view)[0]["predicted_kind"] == expected
