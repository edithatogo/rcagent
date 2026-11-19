"""Frozen synthetic Checkpoint-B development comparison; not clinical validation.

Data are predeclared in a separate Git commit. All algorithm inputs pass D3's
actor/cutoff projection and D4's source-version witness. Only the *train*
partition supplies labels to the deterministic linear learner; no generator,
external NLP model, network request, or independent clinical judgement runs.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from hashlib import sha256
from itertools import pairwise
from pathlib import Path
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw11_d4_comparison import (
    D4View,
    Kind,
    Prediction,
    compare_arms,
    make_view,
    regex_predictions,
)
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
_CONTEXT_RULESET_REVISION = "faw11-b1-context-style-rules-1.1"
ORACLE_PATH = ROOT / "tests/fixtures/faw11_b1_independent/frozen_cases.json"
LOCK_PATH = ROOT / "uv.lock"
_VOCABULARY = re.compile(r"[a-z]+")
_KINDS: tuple[Kind, ...] = (
    "observation",
    "outcome",
    "appraisal",
    "patient_family_concern",
)
_FAMILY = frozenset({"family", "parent", "mother", "father", "patient", "relative"})
_CONCERN = frozenset(
    {
        "concern",
        "concerns",
        "worried",
        "worry",
        "reported",
        "complained",
        "complain",
        "raised",
        "expressed",
    }
)
_OUTCOME = frozenset(
    {
        "result",
        "results",
        "outcome",
        "injury",
        "injuries",
        "harm",
        "death",
        "rash",
        "infection",
        "hypotension",
        "bleeding",
        "complication",
        "complications",
        "developed",
        "discharge",
        "discharged",
    }
)
_APPRAISAL = frozenset(
    {
        "review",
        "appraisal",
        "judgement",
        "judged",
        "concluded",
        "conclusion",
        "investigator",
        "investigation",
        "audit",
        "assessment",
        "assessed",
        "retrospective",
        "panel",
    }
)
_NEGATION = frozenset({"no", "not", "denies", "denied", "without", "absent", "never"})


class LinearModel(TypedDict):
    revision: Literal["faw11-b1-perceptron-1.0"]
    weights: dict[str, dict[str, int]]
    bias: dict[str, int]
    trained_cases: int
    training_fingerprint: str


def _text(value: object, field: str, limit: int = 256) -> str:
    if type(value) is not str or not value or len(value) > limit:
        raise ValueError(f"invalid {field}")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"invalid UTF-8 in {field}") from exc
    return value


def _kind(value: object) -> Kind:
    if type(value) is not str:
        raise ValueError("invalid class label")
    if value == "observation":
        return "observation"
    if value == "outcome":
        return "outcome"
    if value == "appraisal":
        return "appraisal"
    if value == "patient_family_concern":
        return "patient_family_concern"
    raise ValueError("invalid class label")


def _partition(value: object) -> Literal["train", "development", "test"]:
    if type(value) is not str:
        raise ValueError("invalid partition")
    if value == "train":
        return "train"
    if value == "development":
        return "development"
    if value == "test":
        return "test"
    raise ValueError("invalid partition")


def validate_frozen(value: object) -> list[JsonObject]:
    """Reject label/split contamination and malformed frozen reference records."""
    try:
        if not is_array(value) or len(value) != 48:
            raise ValueError("unexpected manifest size")
        rows: list[JsonObject] = []
        seen: set[str] = set()
        splits: dict[str, str] = {}
        family_counts: Counter[str] = Counter()
        partitions: Counter[str] = Counter()
        test_kinds: Counter[str] = Counter()
        for element in value:
            row = require_object(element, context="frozen B1 row")
            if set(row) != {"id", "root_family_id", "partition", "expected_kind", "text"}:
                raise ValueError("unexpected label fields")
            case_id = _text(row["id"], "case ID", 128)
            family = _text(row["root_family_id"], "family ID", 128)
            part = _partition(row["partition"])
            kind = _kind(row["expected_kind"])
            _text(row["text"], "synthetic evidence", 256)
            if case_id in seen:
                raise ValueError("duplicate case ID")
            if family in splits and splits[family] != part:
                raise ValueError("root family spans train and test")
            seen.add(case_id)
            splits[family] = part
            family_counts[family] += 1
            partitions[part] += 1
            if part == "test":
                test_kinds[kind] += 1
            rows.append(row)
        if (
            len(splits) != 24
            or any(count != 2 for count in family_counts.values())
            or partitions != {"train": 24, "development": 8, "test": 16}
            or test_kinds != dict.fromkeys(_KINDS, 4)
        ):
            raise ValueError("invalid family-split or target balance")
        return rows
    except (ValueError, KeyError, TypeError, UnicodeError, RecursionError):
        raise ValueError("invalid frozen B1 corpus") from None


def load_frozen() -> list[JsonObject]:
    """Read a source-controlled fixture, never generate its labels from methods."""
    try:
        content: object = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
        record = require_object(content, context="frozen B1 manifest")
        if set(record) != {
            "schema_version",
            "reference_origin",
            "safety_scope",
            "task",
            "partition_protocol",
            "freeze_date",
            "root_family_count",
            "case_count",
            "cases",
        }:
            raise ValueError("malformed manifest")
        if (
            record["schema_version"] != "faw11-b1-frozen-synthetic-labels-1.0"
            or record["root_family_count"] != 24
            or record["case_count"] != 48
        ):
            raise ValueError("wrong manifest revision")
        return validate_frozen(record["cases"])
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError):
        raise ValueError("frozen synthetic B1 labels unavailable or invalid") from None


def build_case(row: JsonObject) -> JsonObject:
    """Build one D3 source package with immutable spans, no D4 reference labels."""
    case_id = _text(row["id"], "case ID", 128)
    content_line = _text(row["text"], "source evidence", 256)
    event_time = "2026-11-17T08:00:00Z"
    recording_time = "2026-11-17T08:10:00Z"
    availability_time = "2026-11-17T08:20:00Z"
    content = (
        f"{content_line}\n"
        f"Event {event_time}\n"
        f"Recorded {recording_time}\n"
        f"Available {availability_time}"
    )
    digest = "sha256:" + sha256(content.encode("utf-8")).hexdigest()

    def span(quote: str) -> JsonObject:
        offset = content.index(quote)
        return {
            "case_id": case_id,
            "source_id": "note",
            "source_version": 1,
            "source_sha256": digest,
            "coordinate_system": "utf8-byte",
            "start_byte": len(content[:offset].encode("utf-8")),
            "end_byte": len(content[: offset + len(quote)].encode("utf-8")),
            "text": quote,
        }

    def clock(identity: str, kind: str, recipient: str | None, quote: str) -> JsonObject:
        return {
            "id": identity,
            "event_id": "event0",
            "kind": kind,
            "recipient_id": recipient,
            "evidence": span(quote),
        }

    return {
        "permitted_view": "synthetic-d3-decision-only",
        "recipient_id": "clinician-a",
        "cutoff_utc": "2026-11-17T10:00:00Z",
        "timeline": {
            "case_id": case_id,
            "permitted_view": "synthetic-d2-timeline-only",
            "sources": [
                {
                    "case_id": case_id,
                    "id": "note",
                    "version": 1,
                    "state": "present",
                    "content": content,
                    "fingerprint": digest,
                }
            ],
            "recipients": ["clinician-a"],
            "events": [{"id": "event0", "evidence": span(content_line)}],
            "clocks": [
                clock("event-time", "event", None, event_time),
                clock("record-time", "recording", None, recording_time),
                clock("availability-time", "availability", "clinician-a", availability_time),
            ],
            "relations": [],
            "amendments": [],
        },
        "entitlements": [
            {
                "source_id": "note",
                "source_version": 1,
                "recipient_id": "clinician-a",
                "first_available_utc": availability_time,
            }
        ],
        # Deliberately invariant D3 label: not the independent D4 gold label.
        "labels": [{"event_id": "event0", "kind": "observation", "speaker_role": None}],
    }


def _tokens(text: str) -> list[str]:
    return _VOCABULARY.findall(text.casefold())


def _has_nonnegated(tokens: list[str], cues: frozenset[str]) -> bool:
    """Conservatively reject any cue in a negated clause, including later synonyms."""
    present = set(tokens)
    return bool(present & cues) and not bool(present & _NEGATION)


def _context_kind(text: str) -> Kind | None:
    # Sentence and contrast boundaries reset the conservative negation scope.
    # Do not combine a negated family reference with a cue from another clause.
    clauses = [
        _tokens(fragment)
        for fragment in re.split(r"[.!?;]|\b(?:but|however|yet|nevertheless)\b", text.casefold())
    ]
    if any((set(tokens) & _FAMILY) and _has_nonnegated(tokens, _CONCERN) for tokens in clauses):
        return "patient_family_concern"
    if any(_has_nonnegated(tokens, _OUTCOME) for tokens in clauses):
        return "outcome"
    if any(_has_nonnegated(tokens, _APPRAISAL) for tokens in clauses):
        return "appraisal"
    if any(
        set(tokens) & {"recorded", "measured", "checked", "administered", "observed", "resting"}
        for tokens in clauses
    ):
        return "observation"
    return None


def context_predictions(case: object, view: D4View) -> list[Prediction]:
    """Bounded ConText-style lexical/section *rules*; not spaCy or medspaCy."""
    actual = make_view(case, view["root_family_id"], view["partition"])
    if canonical_bytes(actual) != canonical_bytes(view):
        raise ValueError("out-of-scope contextual arm view")
    return [
        {
            "view_fingerprint": actual["view_fingerprint"],
            "event_id": event["event_id"],
            "predicted_kind": _context_kind(event["text"]),
        }
        for event in actual["events"]
    ]


def _features(text: str) -> Counter[str]:
    tokens = _tokens(text)
    terms: Counter[str] = Counter(f"u:{token}" for token in tokens)
    terms.update(f"b:{left}_{right}" for left, right in pairwise(tokens))
    return terms


def _scores(model: LinearModel, features: Counter[str]) -> dict[Kind, int]:
    scores: dict[Kind, int] = {}
    for kind in _KINDS:
        weights = model["weights"][kind]
        scores[kind] = model["bias"][kind] + sum(
            weights.get(feature, 0) * count for feature, count in features.items()
        )
    return scores


def fit_linear(training: list[tuple[D4View, object]]) -> LinearModel:
    """Fit deterministic four-way sparse linear perceptron from train labels only."""
    if not training or len(training) > 128:
        raise ValueError("invalid linear training set")
    examples: list[tuple[str, Counter[str], Kind]] = []
    for view, label in training:
        if view["partition"] != "train" or len(view["events"]) != 1:
            raise ValueError("linear training requires one event per train case")
        kind = _kind(label)
        examples.append((view["case_id"], _features(view["events"][0]["text"]), kind))
    examples.sort(key=lambda item: item[0])
    model: LinearModel = {
        "revision": "faw11-b1-perceptron-1.0",
        "weights": {kind: {} for kind in _KINDS},
        "bias": dict.fromkeys(_KINDS, 0),
        "trained_cases": len(examples),
        "training_fingerprint": fingerprint(
            [
                {"case_id": case_id, "features": dict(features), "label": kind}
                for case_id, features, kind in examples
            ]
        ),
    }
    for _ in range(20):
        for _, features, truth in examples:
            scores = _scores(model, features)
            predicted = max(_KINDS, key=lambda kind: (scores[kind], -_KINDS.index(kind)))
            if predicted == truth:
                continue
            for name, count in features.items():
                predicted_weights = model["weights"][predicted]
                truth_weights = model["weights"][truth]
                predicted_weights[name] = predicted_weights.get(name, 0) - count
                truth_weights[name] = truth_weights.get(name, 0) + count
            model["bias"][truth] += 1
            model["bias"][predicted] -= 1
    return model


def linear_predictions(model: LinearModel, view: D4View) -> list[Prediction]:
    """Predict with a trained conventional classifier; tie implies abstention."""
    return [
        {
            "view_fingerprint": view["view_fingerprint"],
            "event_id": event["event_id"],
            "predicted_kind": _linear_kind(model, event["text"]),
        }
        for event in view["events"]
    ]


def _linear_kind(model: LinearModel, text: str) -> Kind | None:
    scores = _scores(model, _features(text))
    ranked = sorted(_KINDS, key=lambda kind: (-scores[kind], _KINDS.index(kind)))
    if scores[ranked[0]] <= scores[ranked[1]]:
        return None
    return ranked[0]


def _class_metrics(
    references: dict[tuple[str, str], Kind],
    predictions: list[Prediction],
) -> dict[str, JsonObject]:
    lookup = {
        (item["view_fingerprint"], item["event_id"]): item["predicted_kind"] for item in predictions
    }
    metrics: dict[str, JsonObject] = {}
    for kind in _KINDS:
        support = sum(reference == kind for reference in references.values())
        tp = sum(
            reference == kind and lookup.get(key) == kind for key, reference in references.items()
        )
        fp = sum(
            reference != kind and lookup.get(key) == kind for key, reference in references.items()
        )
        fn = support - tp
        metrics[kind] = {
            "support": support,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": tp / (tp + fp) if tp + fp else None,
            "recall": tp / support if support else None,
        }
    return metrics


def evaluate_frozen() -> JsonObject:
    """Score all admitted arms on the *predeclared* synthetic test partition.

    This is a development qualification receipt, not a clinical holdout or a
    claim that any pretrained local generative model has been executed.
    """
    rows = load_frozen()
    study: list[JsonObject] = []
    training: list[tuple[D4View, object]] = []
    test_cases: list[tuple[JsonObject, D4View, Kind]] = []
    for row in rows:
        part = _partition(row["partition"])
        case = build_case(row)
        view = make_view(case, row["root_family_id"], part)
        study.append(
            {
                "case": case,
                "root_family_id": row["root_family_id"],
                "partition": part,
            }
        )
        if part == "train":
            training.append((view, row["expected_kind"]))
        elif part == "test":
            test_cases.append((case, view, _kind(row["expected_kind"])))
    model = fit_linear(training)
    reference_rows: list[JsonObject] = []
    gold: dict[tuple[str, str], Kind] = {}
    predictions: dict[str, list[Prediction]] = {
        "regex": [],
        "token_section_context": [],
        "linear_classifier": [],
    }
    for case, view, kind in test_cases:
        for event in view["events"]:
            key = (view["view_fingerprint"], event["event_id"])
            gold[key] = kind
            reference_rows.append(
                {
                    "view_fingerprint": key[0],
                    "event_id": key[1],
                    "expected_kind": kind,
                    "reference_origin": "independently_authored_synthetic",
                }
            )
        predictions["regex"].extend(regex_predictions(case, view))
        predictions["token_section_context"].extend(context_predictions(case, view))
        predictions["linear_classifier"].extend(linear_predictions(model, view))
    arms: list[JsonObject] = []
    for name in ("regex", "token_section_context", "linear_classifier"):
        arms.append(
            {
                "method": name,
                "status": "executed",
                "revision": {
                    "regex": "faw11-d4-regex-1.0",
                    "token_section_context": _CONTEXT_RULESET_REVISION,
                    "linear_classifier": "faw11-b1-perceptron-1.0",
                }[name],
                "predictions": predictions[name],
                "measured_resources": None,
            }
        )
    arms.append(
        {
            "method": "structured_generation",
            "status": "unavailable",
            "reason": "no pinned offline local generative model, tokenizer, runtime, or execution receipt",
        }
    )
    comparison = compare_arms(study, reference_rows, arms)
    return {
        "schema_version": "faw11-b1-evaluation-1.0",
        "scope": "synthetic_development_only_not_clinical_or_confirmatory",
        "reference_origin": "separately_curated_synthetic_labels_before_predictor_implementation",
        "frozen_manifest_sha256": "sha256:" + sha256(ORACLE_PATH.read_bytes()).hexdigest(),
        "locked_dependencies_sha256": "sha256:" + sha256(LOCK_PATH.read_bytes()).hexdigest(),
        "train_cases": len(training),
        "development_cases": sum(row["partition"] == "development" for row in rows),
        "test_cases": len(test_cases),
        "test_root_families": len(
            {row["root_family_id"] for row in rows if row["partition"] == "test"}
        ),
        "model_executed": True,
        "llm_executed": False,
        "linear_model_revision": model["revision"],
        "linear_model_training_fingerprint": model["training_fingerprint"],
        "checkpoint_b_claim": "not_qualified",
        "scores": comparison["scores"],
        "class_metrics": {
            name: _class_metrics(gold, predictions[name])
            for name in ("regex", "token_section_context", "linear_classifier")
        },
        "limitations": [
            "All 48 cases and 24 semantic families are synthetic and authored for software development; references are not adjudicated clinical outcomes.",
            "The section/ConText-like arm is deterministic token/context rules, not medspaCy and not an external NLP model.",
            "The conventional classifier is a small fixed-epoch sparse perceptron trained only on 24 synthetic train cases; no scikit-learn model is claimed.",
            "No pretrained structured local generator or LLM was available and no local generative model executed.",
            "No external clinical dataset, prospective review, patient outcome or diagnostic use has been qualified.",
            "Checkpoint B remains open pending separately frozen D0-D3 and broader held-out component evidence.",
        ],
    }
