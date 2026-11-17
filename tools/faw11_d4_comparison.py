"""Synthetic-only FAW11/D4 comparison admission and deterministic reference baseline.

No model calls, learned labels, clinical truth or executable ConText/classifier
implementations are supplied by this adapter. D3 is replayed in the privileged
compartment; arm-facing inputs exclude future evidence and reference labels.
"""

from __future__ import annotations

import re
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw10_d3_decision_view import assemble_decision_packet
from tools.json_shapes import JsonObject, is_array, require_object

Partition = Literal["train", "development", "test"]
Kind = Literal["observation", "outcome", "appraisal", "patient_family_concern"]
Method = Literal[
    "regex", "token_section_context", "linear_classifier", "structured_generation"
]
_METHODS: tuple[Method, ...] = (
    "regex",
    "token_section_context",
    "linear_classifier",
    "structured_generation",
)
_KINDS: tuple[Kind, ...] = (
    "observation",
    "outcome",
    "appraisal",
    "patient_family_concern",
)
_FAMILY = re.compile(r"\b(family|mother|father|patient|parent)\b", re.IGNORECASE)
_CONCERN = re.compile(
    r"\b(concern|concerns|worried|worry|complain|reported|raised)\b", re.IGNORECASE
)
_OUTCOME = re.compile(r"\b(result|outcome|harm|death|injury)\b", re.IGNORECASE)
_APPRAISAL = re.compile(r"\b(appraisal|review|preventab|judgement|conclusion)\w*", re.IGNORECASE)


class D4Event(TypedDict):
    event_id: str
    source_id: str
    source_version: int
    source_sha256: str
    start_byte: int
    end_byte: int
    text: str


class D4View(TypedDict):
    schema_version: Literal["faw11-d4-view-1.0"]
    root_family_id: str
    partition: Partition
    case_id: str
    recipient_id: str
    cutoff_utc: str
    view_fingerprint: str
    event_count: int
    family_concern_labels_in_model_input: Literal[False]
    events: list[D4Event]


class Prediction(TypedDict):
    view_fingerprint: str
    event_id: str
    predicted_kind: Kind | None


class D4Receipt(TypedDict):
    schema_version: Literal["faw11-d4-comparison-1.0"]
    status: Literal["incomplete_unqualified"]
    dataset: Literal["caller-declared-synthetic-only"]
    input_scope: Literal["d3-replayed-recipient-cutoff"]
    independent_test_families: int
    eligible_test_events: int
    compared_methods: list[str]
    scores: dict[str, JsonObject]
    view_manifest_fingerprint: str
    paired_comparison_admissible: Literal[False]
    model_executed: Literal[False]
    clinical_qualification: Literal["none"]
    model_qualification: Literal["none"]
    limitations: list[str]


def _text(value: object, field: str) -> str:
    if type(value) is not str or not value or len(value) > 128:
        raise ValueError(f"{field} must be a bounded identifier")
    value.encode("utf-8")
    return value


def _partition(value: object) -> Partition:
    if value == "train":
        return "train"
    if value == "development":
        return "development"
    if value == "test":
        return "test"
    raise ValueError("unsupported study partition")


def _kind(value: object) -> Kind:
    if value == "observation":
        return "observation"
    if value == "outcome":
        return "outcome"
    if value == "appraisal":
        return "appraisal"
    if value == "patient_family_concern":
        return "patient_family_concern"
    raise ValueError("unsupported reference or prediction kind")


def _method(value: object) -> Method:
    if value == "regex":
        return "regex"
    if value == "token_section_context":
        return "token_section_context"
    if value == "linear_classifier":
        return "linear_classifier"
    if value == "structured_generation":
        return "structured_generation"
    raise ValueError("unsupported comparator")


def _rows(value: object, name: str, maximum: int) -> list[JsonObject]:
    if not is_array(value) or len(value) > maximum:
        raise ValueError(f"{name} must be a bounded list")
    return [require_object(row, context=name) for row in value]


def _fields(row: JsonObject, expected: set[str]) -> None:
    if set(row) != expected:
        raise ValueError("invalid comparison record fields")


def _make_view(case: object, root_family_id: object, partition: object) -> D4View:
    family = _text(root_family_id, "root family")
    part = _partition(partition)
    packet = assemble_decision_packet(case)
    records: list[D4Event] = []
    for event in packet["events"]:
        evidence = event["evidence"]
        records.append(
            {
                "event_id": event["event_id"],
                "source_id": evidence["source_id"],
                "source_version": evidence["source_version"],
                "source_sha256": evidence["source_sha256"],
                "start_byte": evidence["start_byte"],
                "end_byte": evidence["end_byte"],
                "text": evidence["text"],
            }
        )
    return {
        "schema_version": "faw11-d4-view-1.0",
        "root_family_id": family,
        "partition": part,
        "case_id": packet["case_id"],
        "recipient_id": packet["recipient_id"],
        "cutoff_utc": packet["cutoff_utc"],
        "view_fingerprint": packet["view_fingerprint"],
        "event_count": len(records),
        "family_concern_labels_in_model_input": False,
        "events": records,
    }


def make_view(case: object, root_family_id: object, partition: object) -> D4View:
    """Project an actor-facing input from replayed D3; errors echo no raw evidence."""
    try:
        return _make_view(case, root_family_id, partition)
    except (KeyError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid or inadmissible D4 view") from None


def regex_predictions(case: object, view: object) -> list[Prediction]:
    """Replay case, recipient, cutoff and immutable span binding before matching."""
    try:
        received = require_object(view, context="D4 arm view")
        expected = make_view(case, received["root_family_id"], received["partition"])
        if canonical_bytes(received) != canonical_bytes(expected):
            raise ValueError("stale or unbound comparator input")
        return _regex_predictions(expected)
    except (KeyError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid or unbound D4 comparator view") from None


def _regex_predictions(view: D4View) -> list[Prediction]:
    """Fixed, weak lexical reference arm; neither model nor semantic truth."""
    predictions: list[Prediction] = []
    for event in view["events"]:
        text = event["text"]
        kind: Kind = "observation"
        if _FAMILY.search(text) and _CONCERN.search(text):
            kind = "patient_family_concern"
        elif _OUTCOME.search(text):
            kind = "outcome"
        elif _APPRAISAL.search(text):
            kind = "appraisal"
        predictions.append(
            {
                "view_fingerprint": view["view_fingerprint"],
                "event_id": event["event_id"],
                "predicted_kind": kind,
            }
        )
    return predictions


def _validate_study(
    study: object,
) -> tuple[list[D4View], set[tuple[str, str]], set[str]]:
    rows = _rows(study, "comparison cases", 128)
    if not rows:
        raise ValueError("no comparison cases")
    views: list[D4View] = []
    by_root: dict[str, Partition] = {}
    by_case: dict[str, str] = {}
    known: set[str] = set()
    expected: set[tuple[str, str]] = set()
    for row in rows:
        _fields(row, {"root_family_id", "partition", "case"})
        view = make_view(row["case"], row["root_family_id"], row["partition"])
        root = view["root_family_id"]
        part = view["partition"]
        if (root in by_root and by_root[root] != part) or (
            view["case_id"] in by_case and by_case[view["case_id"]] != root
        ):
            raise ValueError("case-family split leakage")
        if view["view_fingerprint"] in known:
            raise ValueError("repeated case view")
        by_root[root] = part
        by_case[view["case_id"]] = root
        known.add(view["view_fingerprint"])
        views.append(view)
        if part == "test":
            for event in view["events"]:
                key = (view["view_fingerprint"], event["event_id"])
                if key in expected:
                    raise ValueError("duplicate evaluation item")
                expected.add(key)
    if not expected:
        raise ValueError("no test observations")
    return views, expected, {v["root_family_id"] for v in views if v["partition"] == "test"}


def _validate_references(
    value: object, expected: set[tuple[str, str]]
) -> dict[tuple[str, str], Kind]:
    found: dict[tuple[str, str], Kind] = {}
    for row in _rows(value, "synthetic reference labels", 2048):
        _fields(row, {"view_fingerprint", "event_id", "expected_kind", "reference_origin"})
        key = (
            _text(row["view_fingerprint"], "view fingerprint"),
            _text(row["event_id"], "event id"),
        )
        if (
            key not in expected
            or key in found
            or row["reference_origin"] != "independently_authored_synthetic"
        ):
            raise ValueError("unbound, duplicated or unsupported independent reference")
        found[key] = _kind(row["expected_kind"])
    if set(found) != expected:
        raise ValueError("missing evaluation reference")
    return found


def _score(
    references: dict[tuple[str, str], Kind],
    predictions: dict[tuple[str, str], Kind | None],
) -> JsonObject:
    n = len(references)
    covered = sum(value is not None for value in predictions.values())
    correct = sum(predictions[key] == expected for key, expected in references.items())
    f1_values: list[float] = []
    for label in _KINDS:
        tp = sum(predictions[key] == label and truth == label for key, truth in references.items())
        fp = sum(predictions[key] == label and truth != label for key, truth in references.items())
        fn = sum(predictions[key] != label and truth == label for key, truth in references.items())
        denom = 2 * tp + fp + fn
        f1_values.append(2 * tp / denom if denom else 0.0)
    return {
        "status": "executed_input_only",
        "eligible": n,
        "covered": covered,
        "abstentions": n - covered,
        "correct": correct,
        "incorrect": covered - correct,
        "coverage": covered / n,
        "accuracy_full_denominator": correct / n,
        "accuracy_covered_only": correct / covered if covered else None,
        "macro_f1": sum(f1_values) / len(_KINDS),
        "resources_measured_by_harness": False,
    }


def _compare_arms(study: object, references: object, arms: object) -> D4Receipt:
    views, expected, roots = _validate_study(study)
    reference_map = _validate_references(references, expected)
    received: dict[Method, JsonObject] = {}
    for row in _rows(arms, "comparison arms", 4):
        method = _method(row.get("method"))
        if method in received:
            raise ValueError("duplicate method")
        status = row.get("status")
        if status == "unavailable":
            _fields(row, {"method", "status", "reason"})
            _text(row["reason"], "unavailability reason")
        elif status == "executed":
            _fields(row, {"method", "status", "revision", "predictions", "measured_resources"})
            _text(row["revision"], "method revision")
            # A caller's claimed measurements are not independently verified by this harness.
            if row["measured_resources"] is not None:
                raise ValueError("unverified measured resource payload")
        else:
            raise ValueError("unknown method status")
        received[method] = row
    if set(received) != set(_METHODS):
        raise ValueError("all four arms must have explicit dispositions")

    scores: dict[str, JsonObject] = {}
    for method in _METHODS:
        arm = received[method]
        if arm["status"] == "unavailable":
            scores[method] = {
                "status": "unavailable",
                "reason": arm["reason"],
                "eligible": len(expected),
                "covered": 0,
                "abstentions": None,
                "correct": None,
                "accuracy_full_denominator": None,
                "macro_f1": None,
            }
            continue
        predictions: dict[tuple[str, str], Kind | None] = {}
        for row in _rows(arm["predictions"], "arm predictions", 2048):
            _fields(row, {"view_fingerprint", "event_id", "predicted_kind"})
            key = (
                _text(row["view_fingerprint"], "view fingerprint"),
                _text(row["event_id"], "event id"),
            )
            if key not in expected or key in predictions:
                raise ValueError("prediction outside the frozen actor view or duplicated")
            value = row["predicted_kind"]
            predictions[key] = _kind(value) if value is not None else None
        if set(predictions) != expected:
            raise ValueError("missing predictions; explicit null abstention required")
        scores[method] = _score(reference_map, predictions)
    view_manifest_fingerprint = fingerprint(
        [
            {
                "root_family_id": view["root_family_id"],
                "partition": view["partition"],
                "case_id": view["case_id"],
                "view_fingerprint": view["view_fingerprint"],
            }
            for view in views
        ]
    )
    return {
        "schema_version": "faw11-d4-comparison-1.0",
        "status": "incomplete_unqualified",
        "dataset": "caller-declared-synthetic-only",
        "input_scope": "d3-replayed-recipient-cutoff",
        "independent_test_families": len(roots),
        "eligible_test_events": len(expected),
        "compared_methods": list(_METHODS),
        "scores": scores,
        "view_manifest_fingerprint": view_manifest_fingerprint,
        "paired_comparison_admissible": False,
        "model_executed": False,
        "clinical_qualification": "none",
        "model_qualification": "none",
        "limitations": [
            "References and family roots are caller-declared synthetic labels, not adjudicated clinical truth.",
            "Only the regex reference arm runs here; other methods require separately pinned local dependencies and execution.",
            "Supplied predictions are structurally checked but do not establish a model was run, any measured resource budget, or generalisation.",
            "No independent held-out validation, fairness inference, clinical authority or deployment is established.",
        ],
    }


def compare_arms(study: object, references: object, arms: object) -> D4Receipt:
    """Validate same-view comparisons while withholding raw future exception detail."""
    try:
        return _compare_arms(study, references, arms)
    except (KeyError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid or inadmissible D4 comparison") from None
