"""Independent literal D1 semantics, omissions, provenance and bounded execution.

The oracle was frozen before the D1 producer existed or was imported. This module
never imports a producer fixture builder or uses a replay result as a semantic
label. Replay verification is tested separately as a consistency boundary.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools.faw08_d1_extraction import extract_case, generate_receipt, verify_extraction

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests/fixtures/faw08_independent"
ORACLE = FIXTURES / "d1_oracle.json"
FROZEN_SHA256 = "263143abe0c71bc02d7b04bd9593af3946f00c2ab64970786c922a005627aafe"
VIEW = "synthetic-d1-extraction-only"
SPAN_FIELDS = (
    "case_id",
    "source_id",
    "source_version",
    "source_sha256",
    "coordinate_system",
    "start_byte",
    "end_byte",
    "text",
)
KEY_FIELDS = (*SPAN_FIELDS[:-1], "kind")
OBSERVATION_FIELDS = {
    *SPAN_FIELDS,
    "observation_id",
    "kind",
    "status",
    "normalized",
    "reason",
    "polarity",
    "subject",
    "reporter",
    "context",
    "anchor",
    "timezone",
    "recording_time",
    "availability_time",
    "event_linkage",
    "context_reasons",
    "method",
    "rule_version",
}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _fixture() -> ObjectMap:
    return mapping(json.loads(ORACLE.read_text(encoding="utf-8")))


def _cases() -> list[ObjectMap]:
    return [mapping(row) for row in sequence(_fixture()["cases"])]


def _item(identifier: str) -> ObjectMap:
    return next(row for row in _cases() if row["id"] == identifier)


def _input(identifier: str) -> ObjectMap:
    return deepcopy(mapping(_item(identifier)["input"]))


def _objects(value: object) -> list[ObjectMap]:
    return [mapping(row) for row in sequence(value)]


def _key(observation: ObjectMap) -> str:
    return _canonical([observation.get(field) for field in KEY_FIELDS]).decode("utf-8")


def _same_field(key: str, expected: object, actual: object) -> bool:
    if key in {"context", "anchor"} and expected is not None:
        if not isinstance(actual, dict):
            return False
        expected_span = mapping(expected)
        actual_span = mapping(cast("dict[object, object]", actual))
        return all(
            name in actual_span and _canonical(actual_span[name]) == _canonical(value)
            for name, value in expected_span.items()
        )
    return _canonical(actual) == _canonical(expected)


def _field_errors(expected: ObjectMap, actual: ObjectMap) -> list[str]:
    return [
        key
        for key, value in expected.items()
        if key not in actual or not _same_field(key, value, actual[key])
    ]


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def score_cases(expected_cases: list[ObjectMap], actual_cases: list[ObjectMap]) -> ObjectMap:
    """Score the frozen denominator, retaining omissions, duplicates and failures.

    Actual rows contain ``case_id`` and either ``result`` or ``execution_error``.
    Matching is one-to-one by source binding, byte interval and lexical kind.
    Correct resolved output additionally requires every independently expected
    semantic/context field. Correct uncertainty never counts as normalization.
    """
    counters: Counter[str] = Counter()
    errors: Counter[str] = Counter()
    by_case: dict[str, list[ObjectMap]] = {}
    for actual in actual_cases:
        by_case.setdefault(text_value(actual["case_id"]), []).append(actual)
    expected_case_ids: set[str] = set()
    families: set[str] = set()
    for case in expected_cases:
        case_input = mapping(case["input"])
        case_id = text_value(case_input["case_id"])
        expected_case_ids.add(case_id)
        families.add(text_value(case["family"]))
        expected = _objects(case["expected_observations"])
        rows = by_case.pop(case_id, [])
        actual_observations: list[ObjectMap] = []
        if rows and "result" in rows[0]:
            result = mapping(rows[0]["result"])
            actual_observations = _objects(result["observations"])
        else:
            counters["execution_failures"] += 1
        for duplicate in rows[1:]:
            counters["execution_failures"] += 1
            if "result" in duplicate:
                count = len(sequence(mapping(duplicate["result"])["observations"]))
                counters["false_positive"] += count
                counters["actual_observations"] += count
        if not expected:
            counters["no_observation_cases"] += 1
            counters["no_observation_false_positives"] += len(actual_observations)
            counters["no_observation_cases_with_false_positives"] += bool(actual_observations)
        counters["actual_observations"] += len(actual_observations)
        buckets: dict[str, list[ObjectMap]] = {}
        for observed in actual_observations:
            buckets.setdefault(_key(observed), []).append(observed)
        for wanted in expected:
            counters["expected_observations"] += 1
            resolved = wanted["status"] == "resolved"
            counters["expected_resolved" if resolved else "expected_unresolved"] += 1
            matches = buckets.get(_key(wanted), [])
            if not matches:
                counters["false_negative"] += 1
                counters["false_blocking"] += resolved
                continue
            observed = matches.pop(0)
            counters["true_positive"] += 1
            differences = _field_errors(wanted, observed)
            errors.update(differences)
            if not differences:
                counters["correct_observations"] += 1
                counters["correct_resolved" if resolved else "correct_unresolved"] += 1
            if resolved and observed.get("status") != "resolved":
                counters["false_blocking"] += 1
        counters["false_positive"] += sum(len(bucket) for bucket in buckets.values())
    for orphan_rows in by_case.values():
        for orphan in orphan_rows:
            counters["execution_failures"] += 1
            if "result" in orphan:
                count = len(sequence(mapping(orphan["result"])["observations"]))
                counters["actual_observations"] += count
                counters["false_positive"] += count
    names = (
        "expected_observations",
        "actual_observations",
        "true_positive",
        "false_positive",
        "false_negative",
        "expected_resolved",
        "expected_unresolved",
        "correct_observations",
        "correct_resolved",
        "correct_unresolved",
        "false_blocking",
        "execution_failures",
        "no_observation_cases",
        "no_observation_false_positives",
        "no_observation_cases_with_false_positives",
    )
    result: ObjectMap = {name: counters[name] for name in names}
    result.update(
        {
            "case_count": len(expected_case_ids),
            "family_count": len(families),
            "precision": _ratio(
                counters["true_positive"], counters["true_positive"] + counters["false_positive"]
            ),
            "recall": _ratio(counters["true_positive"], counters["expected_observations"]),
            "normalization_recall": _ratio(
                counters["correct_resolved"], counters["expected_resolved"]
            ),
            "useful_resolved_coverage": _ratio(
                counters["correct_resolved"], counters["expected_observations"]
            ),
            "exact_annotation_coverage": _ratio(
                counters["correct_observations"], counters["expected_observations"]
            ),
            "ambiguity_recognition": _ratio(
                counters["correct_unresolved"], counters["expected_unresolved"]
            ),
            "no_observation_false_positive_case_rate": _ratio(
                counters["no_observation_cases_with_false_positives"],
                counters["no_observation_cases"],
            ),
            "field_error_count": sum(errors.values()),
            "field_errors": dict(sorted(errors.items())),
        }
    )
    return result


def evaluate_oracle() -> ObjectMap:
    """Execute only literal inputs; return raw results and independently scored errors."""
    observed: list[ObjectMap] = []
    for item in _cases():
        case = deepcopy(mapping(item["input"]))
        row: ObjectMap = {"case_id": case["case_id"]}
        try:
            result = mapping(extract_case(case))
            _objects(result["observations"])
            row["result"] = result
        except (
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            AttributeError,
            AssertionError,
            RuntimeError,
            UnicodeError,
            ArithmeticError,
        ) as exc:
            row["execution_error"] = {"type": type(exc).__name__, "message": str(exc)}
        observed.append(row)
    return {
        "oracle_sha256": hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
        "actual_cases": observed,
        "metrics": score_cases(_cases(), observed),
    }


def _source_index(case: ObjectMap) -> dict[tuple[str, int], ObjectMap]:
    result: dict[tuple[str, int], ObjectMap] = {}
    for source in _objects(case["sources"]):
        version = source["version"]
        assert isinstance(version, int)
        assert not isinstance(version, bool)
        result[(text_value(source["id"]), version)] = source
    return result


def _check_span(case: ObjectMap, span: ObjectMap) -> None:
    version = span["source_version"]
    assert isinstance(version, int)
    assert not isinstance(version, bool)
    source = _source_index(case)[(text_value(span["source_id"]), version)]
    raw = text_value(source["content"]).encode("utf-8")
    start, end = span["start_byte"], span["end_byte"]
    assert isinstance(start, int)
    assert not isinstance(start, bool)
    assert isinstance(end, int)
    assert not isinstance(end, bool)
    assert 0 <= start < end <= len(raw)
    assert raw[start:end].decode("utf-8") == span["text"]
    assert span["source_sha256"] == source["fingerprint"] == _digest(raw)
    assert span["case_id"] == source["case_id"] == case["case_id"]
    assert span["coordinate_system"] == "utf8-byte"


def _check_result(case: ObjectMap, result: ObjectMap) -> None:
    assert result["schema_version"] == "faw08-d1-case-1.0"
    assert result["case_id"] == case["case_id"]
    assert result["permitted_view"] == VIEW
    assert result["date_order"] == case.get("date_order", "unknown")
    assert result["source_admission"] == "verified-full-source-witnesses-not-observations"
    observations = _objects(result["observations"])
    assert result["observation_count"] == len(observations)
    assert result["no_supported_observation"] is (not observations)
    identifiers: set[str] = set()
    for observed in observations:
        assert set(observed) == OBSERVATION_FIELDS
        identifier = text_value(observed["observation_id"])
        assert identifier
        assert identifier not in identifiers
        identifiers.add(identifier)
        assert observed["method"] == "deterministic-stdlib-rules"
        assert observed["rule_version"] == "faw08-d1-rules-1.0"
        _check_span(case, observed)
        context = mapping(observed["context"])
        _check_span(case, context)
        assert context["verified"] is True
        start, end = observed["start_byte"], observed["end_byte"]
        context_start, context_end = context["start_byte"], context["end_byte"]
        assert isinstance(start, int)
        assert isinstance(end, int)
        assert isinstance(context_start, int)
        assert isinstance(context_end, int)
        assert context_start <= start < end <= context_end
        for field in ("source_id", "source_version", "source_sha256"):
            assert context[field] == observed[field]
        anchor = observed["anchor"]
        if anchor is not None:
            assert observed["kind"] == "relative_time"
            checked_anchor = mapping(anchor)
            _check_span(case, checked_anchor)
            assert checked_anchor["verified"] is True
            for field in ("source_id", "source_version", "source_sha256"):
                assert checked_anchor[field] == observed[field]
            assert any(
                all(checked_anchor[key] == candidate[key] for key in SPAN_FIELDS)
                for candidate in _objects(case.get("anchors", []))
            )
        for field in ("timezone", "recording_time", "availability_time", "event_linkage"):
            assert observed[field] is None
    source_index = _source_index(case)
    diagnostics = _objects(result["sources"])
    assert len(diagnostics) == len(source_index)
    for diagnostic in diagnostics:
        version = diagnostic["version"]
        assert isinstance(version, int)
        assert not isinstance(version, bool)
        source = source_index[(text_value(diagnostic["source_id"]), version)]
        raw = text_value(source["content"]).encode("utf-8")
        assert diagnostic["case_id"] == case["case_id"]
        assert diagnostic["state"] == "present"
        assert diagnostic["bytes"] == len(raw)
        assert diagnostic["sha256"] == source["fingerprint"] == _digest(raw)


def test_independent_oracle_is_frozen_complete_and_byte_faithful() -> None:
    assert hashlib.sha256(ORACLE.read_bytes()).hexdigest() == FROZEN_SHA256
    freeze = mapping(json.loads((FIXTURES / "freeze.json").read_text(encoding="utf-8")))
    assert freeze["oracle_sha256"] == FROZEN_SHA256
    assert freeze["producer_calls_before_freeze"] == 0
    assert freeze["production_source_read_before_freeze"] is False
    cases = _cases()
    assert len(cases) == 28
    for family in sequence(_fixture()["required_families"]):
        variants = {text_value(row["variant"]) for row in cases if row["family"] == family}
        assert variants == {"positive", "adverse"}
    assert sum(len(sequence(row["expected_observations"])) for row in cases) == 54
    for row in cases:
        case = mapping(row["input"])
        keys: set[str] = set()
        for expected in _objects(row["expected_observations"]):
            assert _key(expected) not in keys
            keys.add(_key(expected))
            _check_span(case, expected)
            _check_span(case, mapping(expected["context"]))
            if expected["anchor"] is not None:
                _check_span(case, mapping(expected["anchor"]))


@pytest.mark.parametrize("identifier", [text_value(row["id"]) for row in _cases()])
def test_independent_literal_expectations(identifier: str) -> None:
    item = _item(identifier)
    case = deepcopy(mapping(item["input"]))
    before = deepcopy(case)
    result = mapping(extract_case(case))
    assert case == before
    _check_result(case, result)
    score = score_cases([item], [{"case_id": case["case_id"], "result": result}])
    assert score["false_positive"] == 0, score
    assert score["false_negative"] == 0, score
    assert score["field_error_count"] == 0, score
    assert score["false_blocking"] == 0, score


def test_independent_aggregate_metrics_retain_all_denominators() -> None:
    metrics = mapping(evaluate_oracle()["metrics"])
    assert metrics["case_count"] == 28
    assert metrics["family_count"] == 14
    assert metrics["expected_observations"] == metrics["true_positive"] == 54
    assert metrics["expected_resolved"] == metrics["correct_resolved"] == 37
    assert metrics["expected_unresolved"] == metrics["correct_unresolved"] == 17
    assert metrics["precision"] == metrics["recall"] == metrics["normalization_recall"] == 1.0
    assert metrics["ambiguity_recognition"] == metrics["exact_annotation_coverage"] == 1.0
    assert metrics["useful_resolved_coverage"] == 37 / 54
    for field in (
        "false_positive",
        "false_negative",
        "field_error_count",
        "false_blocking",
        "execution_failures",
        "no_observation_false_positives",
    ):
        assert metrics[field] == 0, metrics


def test_independent_scorer_cannot_reward_all_abstention() -> None:
    actual: list[ObjectMap] = [
        {"case_id": mapping(row["input"])["case_id"], "result": {"observations": []}}
        for row in _cases()
    ]
    metrics = score_cases(_cases(), actual)
    assert metrics["expected_observations"] == metrics["false_negative"] == 54
    assert metrics["true_positive"] == metrics["correct_resolved"] == 0
    assert metrics["false_blocking"] == 37
    assert metrics["recall"] == metrics["normalization_recall"] == 0.0
    assert metrics["precision"] is None
    assert metrics["execution_failures"] == 0


def test_independent_scorer_retains_execution_failures_and_zero_denominators() -> None:
    metrics = score_cases(_cases(), [])
    assert metrics["execution_failures"] == 28
    assert metrics["false_negative"] == 54
    empty = score_cases(
        [_item("no-supported-observation")],
        [
            {
                "case_id": _input("no-supported-observation")["case_id"],
                "result": {"observations": []},
            }
        ],
    )
    for field in (
        "precision",
        "recall",
        "normalization_recall",
        "ambiguity_recognition",
        "useful_resolved_coverage",
    ):
        assert empty[field] is None


def test_independent_scorer_separates_semantics_duplicates_and_false_positives() -> None:
    item = _item("numeric-valid")
    expected = deepcopy(_objects(item["expected_observations"])[0])
    mapping(expected["normalized"])["day"] = 28
    row: ObjectMap = {
        "case_id": mapping(item["input"])["case_id"],
        "result": {"observations": [expected, expected]},
    }
    metrics = score_cases([item], [row])
    assert metrics["true_positive"] == metrics["false_positive"] == 1
    assert metrics["field_errors"] == {"normalized": 1}
    assert metrics["correct_resolved"] == 0
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 1.0
    empty_item = _item("no-supported-observation")
    row["case_id"] = mapping(empty_item["input"])["case_id"]
    empty = score_cases([empty_item], [row])
    assert empty["no_observation_false_positives"] == 2
    assert empty["no_observation_false_positive_case_rate"] == 1.0


def _make_case(
    content: str, *, case_id: str = "independent-probe", source_id: str = "note"
) -> ObjectMap:
    return {
        "case_id": case_id,
        "permitted_view": VIEW,
        "sources": [
            {
                "id": source_id,
                "version": 1,
                "case_id": case_id,
                "state": "present",
                "content": content,
                "fingerprint": _digest(content.encode("utf-8")),
            }
        ],
    }


def _replace_content(case: ObjectMap, content: str) -> None:
    source = _objects(case["sources"])[0]
    source["content"] = content
    source["fingerprint"] = _digest(content.encode("utf-8"))


def _invalid_input(name: str) -> object:
    case = _input("numeric-valid")
    source = _objects(case["sources"])[0]
    mutations: dict[str, tuple[ObjectMap, str, object]] = {
        "case-id-empty": (case, "case_id", ""),
        "case-id-limit": (case, "case_id", "c" * 129),
        "case-id-bool": (case, "case_id", True),
        "wrong-view": (case, "permitted_view", "clinical"),
        "empty-sources": (case, "sources", []),
        "source-not-object": (case, "sources", [False]),
        "sources-not-list": (case, "sources", {}),
        "source-id-empty": (source, "id", ""),
        "source-id-limit": (source, "id", "s" * 129),
        "source-cross-case": (source, "case_id", "other"),
        "version-bool": (source, "version", True),
        "version-zero": (source, "version", 0),
        "version-negative": (source, "version", -1),
        "version-float": (source, "version", 1.0),
        "version-string": (source, "version", "1"),
        "source-unknown": (source, "state", "unknown"),
        "source-withdrawn": (source, "state", "withdrawn"),
        "empty-content": (source, "content", ""),
        "nontext-content": (source, "content", 5),
        "surrogate-content": (source, "content", "\ud800"),
        "forged-fingerprint": (source, "fingerprint", "sha256:" + "0" * 64),
        "uppercase-fingerprint": (source, "fingerprint", "sha256:" + "A" * 64),
        "short-fingerprint": (source, "fingerprint", "sha256:abc"),
        "bad-date-order": (case, "date_order", "dmy"),
        "null-date-order": (case, "date_order", None),
        "anchors-not-array": (case, "anchors", {}),
        "anchors-limit-before-rows": (case, "anchors", [None] * 33),
    }
    if name in mutations:
        target, field, value = mutations[name]
        target[field] = value
        if name == "empty-content":
            source["fingerprint"] = _digest(b"")
        elif name == "case-id-limit":
            source["case_id"] = case["case_id"]
    elif name == "duplicate-source":
        sequence(case["sources"]).append(deepcopy(source))
    elif name == "source-count-limit":
        case["sources"] = [{**source, "id": f"note-{index}"} for index in range(33)]
    elif name == "source-byte-limit":
        _replace_content(case, "é" * 32769)
    elif name == "missing-fingerprint":
        del source["fingerprint"]
    elif name == "missing-view":
        del case["permitted_view"]
    else:
        raise AssertionError(f"unrecognised independent mutation: {name}")
    return case


INVALID_INPUTS = (
    "case-id-empty",
    "case-id-limit",
    "case-id-bool",
    "wrong-view",
    "missing-view",
    "empty-sources",
    "source-not-object",
    "sources-not-list",
    "source-id-empty",
    "source-id-limit",
    "source-cross-case",
    "version-bool",
    "version-zero",
    "version-negative",
    "version-float",
    "version-string",
    "source-unknown",
    "source-withdrawn",
    "empty-content",
    "nontext-content",
    "surrogate-content",
    "forged-fingerprint",
    "uppercase-fingerprint",
    "short-fingerprint",
    "missing-fingerprint",
    "bad-date-order",
    "null-date-order",
    "anchors-not-array",
    "anchors-limit-before-rows",
    "duplicate-source",
    "source-count-limit",
    "source-byte-limit",
)


@pytest.mark.parametrize("name", INVALID_INPUTS)
def test_independent_input_corruption_fails_before_observation(name: str) -> None:
    with pytest.raises(ValueError) as error:
        extract_case(_invalid_input(name))
    assert str(error.value)


@pytest.mark.parametrize("case", [None, False, 7, "case", [], {}])
def test_independent_malformed_case_container_rejected(case: object) -> None:
    with pytest.raises(ValueError) as error:
        extract_case(case)
    assert str(error.value)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("case_id", "other"),
        ("source_id", "other"),
        ("source_version", 2),
        ("source_sha256", "sha256:" + "0" * 64),
        ("coordinate_system", "unicode-codepoint"),
        ("start_byte", True),
        ("start_byte", -1),
        ("end_byte", 65537),
        ("text", "invented"),
    ],
)
def test_independent_forged_anchor_rejected(field: str, value: object) -> None:
    case = _input("relative-selected-anchor")
    _objects(case["anchors"])[0][field] = value
    with pytest.raises(ValueError) as error:
        extract_case(case)
    assert str(error.value)


def test_independent_duplicate_and_non_datetime_anchors_rejected() -> None:
    case = _input("relative-selected-anchor")
    anchor = _objects(case["anchors"])[0]
    sequence(case["anchors"]).append(deepcopy(anchor))
    with pytest.raises(ValueError) as duplicate:
        extract_case(case)
    assert str(duplicate.value)
    case = _input("relative-selected-anchor")
    anchor = _objects(case["anchors"])[0]
    raw = text_value(_objects(case["sources"])[0]["content"]).encode("utf-8")
    needle = b"2 hours later"
    start = raw.index(needle)
    anchor.update(
        {"start_byte": start, "end_byte": start + len(needle), "text": needle.decode("ascii")}
    )
    with pytest.raises(ValueError) as non_datetime:
        extract_case(case)
    assert str(non_datetime.value)


def test_independent_exact_resource_limits_and_candidate_overflow() -> None:
    case = _make_case("é" * 32768)
    assert mapping(extract_case(case))["observations"] == []
    source = _objects(_make_case("administrative")["sources"])[0]
    case = {
        "case_id": source["case_id"],
        "permitted_view": VIEW,
        "sources": [{**source, "id": f"note-{index}"} for index in range(32)],
    }
    result = mapping(extract_case(case))
    assert len(sequence(result["sources"])) == 32
    assert result["observation_count"] == 0
    accepted = mapping(extract_case(_make_case("; ".join(["fever"] * 32))))
    assert accepted["observation_count"] == 32
    with pytest.raises(ValueError) as overflow:
        extract_case(_make_case("; ".join(["fever"] * 33)))
    assert str(overflow.value)


@pytest.mark.parametrize("field", sorted(OBSERVATION_FIELDS))
def test_independent_one_field_output_tampering_rejected(field: str) -> None:
    case = _input("relative-selected-anchor")
    result = mapping(extract_case(case))
    assert verify_extraction(case, result) is True
    observed = next(
        row for row in _objects(result["observations"]) if row["kind"] == "relative_time"
    )
    replacements: ObjectMap = {
        "observation_id": "forged",
        "case_id": "other",
        "source_id": "other",
        "source_version": 2,
        "source_sha256": "sha256:" + "0" * 64,
        "coordinate_system": "unicode-codepoint",
        "start_byte": 0,
        "end_byte": 1,
        "text": "forged",
        "kind": "assertion",
        "status": "unsupported",
        "normalized": {"offset_seconds": 1, "local_datetime": None},
        "reason": "forged",
        "polarity": "negated",
        "subject": "mother",
        "reporter": "father",
        "context": {},
        "anchor": None,
        "timezone": "UTC",
        "recording_time": "2024-04-14",
        "availability_time": "2024-04-14",
        "event_linkage": "invented",
        "context_reasons": ["forged"],
        "method": "invented",
        "rule_version": "invented",
    }
    assert observed[field] != replacements[field]
    observed[field] = replacements[field]
    assert verify_extraction(case, result) is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", "other"),
        ("case_id", "other"),
        ("permitted_view", "clinical"),
        ("date_order", "MDY"),
        ("source_admission", "inferred"),
        ("sources", []),
        ("observations", []),
        ("observation_count", 999),
        ("no_supported_observation", True),
    ],
)
def test_independent_case_result_tampering_rejected(field: str, value: object) -> None:
    case = _input("numeric-valid")
    result = mapping(extract_case(case))
    assert result[field] != value
    result[field] = value
    assert verify_extraction(case, result) is False


def test_independent_source_order_repetition_versions_and_content_binding() -> None:
    case = _input("conflicting-sources")
    original = mapping(extract_case(case))
    assert mapping(extract_case(deepcopy(case))) == original
    sequence(case["sources"]).reverse()
    reversed_result = mapping(extract_case(case))
    by_id = {text_value(row["observation_id"]): row for row in _objects(original["observations"])}
    reversed_by_id = {
        text_value(row["observation_id"]): row for row in _objects(reversed_result["observations"])
    }
    assert reversed_by_id == by_id
    revised = _input("numeric-valid")
    prior = mapping(extract_case(revised))
    _objects(revised["sources"])[0]["version"] = 2
    changed = mapping(extract_case(revised))
    assert (
        _objects(prior["observations"])[0]["observation_id"]
        != _objects(changed["observations"])[0]["observation_id"]
    )
    assert verify_extraction(revised, prior) is False
    _replace_content(revised, "2024-03-01")
    assert verify_extraction(revised, changed) is False


@pytest.mark.parametrize("binding", ["case", "source", "content"])
def test_independent_identifier_binds_case_source_and_full_content(binding: str) -> None:
    case = _input("numeric-valid")
    original = mapping(extract_case(case))
    source = _objects(case["sources"])[0]
    if binding == "case":
        case["case_id"] = source["case_id"] = "independent-changed-case"
    elif binding == "source":
        source["id"] = "changed-source"
    else:
        # The observation itself keeps identical text, offsets and interpretation.
        # The source digest must still change its content-bound identifier.
        _replace_content(case, text_value(source["content"]) + " ")
    changed = mapping(extract_case(case))
    prior_observation = _objects(original["observations"])[0]
    next_observation = _objects(changed["observations"])[0]
    assert next_observation["normalized"] == prior_observation["normalized"]
    assert next_observation["observation_id"] != prior_observation["observation_id"]
    assert verify_extraction(case, original) is False


@given(
    st.lists(
        st.sampled_from(["é", "😀", "e\u0301", "\r\n", " ", "\u03b1"]), min_size=0, max_size=12
    )
)
@settings(max_examples=40, deadline=None)
def test_independent_unicode_prefix_shifts_exact_bytes(parts: list[str]) -> None:
    prefix = "".join(parts) + "\n"
    case = _make_case(prefix + "patient has fever")
    result = mapping(extract_case(case))
    _check_result(case, result)
    observed = _objects(result["observations"])
    assert len(observed) == 1
    row = observed[0]
    delta = len(prefix.encode("utf-8"))
    assert row["start_byte"] == delta + 12
    assert row["end_byte"] == delta + 17
    assert row["text"] == "fever"
    assert row["normalized"] == {"observation": "fever"}
    assert row["polarity"] == "affirmed"
    assert row["subject"] == "patient"
    assert mapping(row["context"])["text"] == "patient has fever"
    assert mapping(row["context"])["start_byte"] == delta


def test_independent_anchor_removal_and_cross_source_non_inference() -> None:
    case = _input("relative-selected-anchor")
    case["anchors"] = []
    result = mapping(extract_case(case))
    relative = [row for row in _objects(result["observations"]) if row["kind"] == "relative_time"]
    assert len(relative) == 2
    for row in relative:
        assert row["anchor"] is None
        assert row["status"] == "partial"
        assert row["reason"] == "missing_explicit_anchor"
    other = _objects(
        _make_case("2020-01-01 00:00", case_id=text_value(case["case_id"]), source_id="other")[
            "sources"
        ]
    )[0]
    sequence(case["sources"]).insert(0, other)
    after = mapping(extract_case(case))
    assert [
        row for row in _objects(after["observations"]) if row["kind"] == "relative_time"
    ] == relative


@pytest.mark.parametrize("boundary", ["; ", ". ", "\n", " but ", " however "])
def test_independent_polarity_and_attribution_stop_at_clause_boundaries(boundary: str) -> None:
    case = _make_case("mother reports patient denies fever" + boundary + "father has cough")
    result = mapping(extract_case(case))
    observed = _objects(result["observations"])
    assert len(observed) == 2
    fever, cough = observed
    assert fever["normalized"] == {"observation": "fever"}
    assert fever["polarity"] == "negated"
    assert fever["subject"] == "patient"
    assert fever["reporter"] == "mother"
    assert cough["normalized"] == {"observation": "cough"}
    assert cough["polarity"] == "affirmed"
    assert cough["subject"] == "father"
    assert cough["reporter"] is None
    assert mapping(fever["context"])["text"] == "mother reports patient denies fever"
    assert mapping(cough["context"])["text"] == "father has cough"


@pytest.mark.parametrize(
    ("raw", "normalized", "polarity", "subject", "reporter"),
    [
        ("patient received 6 mg", {"value": "6", "unit": "mg"}, "affirmed", "patient", None),
        ("patient did not receive 6 mg", {"value": "6", "unit": "mg"}, "negated", "patient", None),
        (
            "nurse reports child received 6 mg",
            {"value": "6", "unit": "mg"},
            "affirmed",
            "child",
            "nurse",
        ),
        (
            "nurse reports mother received 6 mg",
            {"value": "6", "unit": "mg"},
            "affirmed",
            "mother",
            "nurse",
        ),
    ],
)
def test_independent_number_polarity_and_attribution_changes(
    raw: str, normalized: ObjectMap, polarity: str, subject: str, reporter: str | None
) -> None:
    result = mapping(extract_case(_make_case(raw)))
    observed = _objects(result["observations"])
    assert len(observed) == 1
    row = observed[0]
    assert row["normalized"] == normalized
    assert row["polarity"] == polarity
    assert row["subject"] == subject
    assert row["reporter"] == reporter


def _run_demo(
    *, module: bool = False, extra: list[str] | None = None
) -> subprocess.CompletedProcess[bytes]:
    target = ["tools.faw08_d1_extraction"] if module else ["tools.workbench", "d1-demo"]
    return subprocess.run(
        [sys.executable, "-m", *target, *(extra or [])],
        cwd=ROOT,
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "ascii"},
        timeout=20,
        check=False,
    )


def test_independent_actual_subprocess_determinism_and_receipt_provenance() -> None:
    first = _run_demo()
    second = _run_demo()
    direct = _run_demo(module=True)
    assert first.returncode == second.returncode == direct.returncode == 0
    assert first.stderr == second.stderr == direct.stderr == b""
    assert first.stdout == second.stdout == direct.stdout
    receipt = mapping(json.loads(first.stdout))
    assert first.stdout == _canonical(receipt) + b"\n"
    assert receipt == mapping(generate_receipt())
    assert receipt["schema_version"] == "faw08-d1-receipt-1.0"
    assert receipt["rule_version"] == "faw08-d1-rules-1.0"
    assert receipt["permitted_view"] == VIEW
    assert receipt["task"] == "FAW08/D1"
    assert receipt["dataset"] == "generated-synthetic-only"
    assert receipt["command"] == "uv run --no-sync python -m tools.workbench d1-demo"
    assert receipt["limitations"]
    inputs = _objects(receipt["inputs"])
    results = _objects(receipt["cases"])
    assert receipt["case_count"] == len(inputs) == len(results)
    assert len(inputs) >= 12
    assert receipt["input_fingerprint"] == _digest(_canonical(inputs))
    unsigned = {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    assert receipt["output_fingerprint"] == _digest(_canonical(unsigned))
    assert receipt["dependency_lock_sha256"] == _digest((ROOT / "uv.lock").read_bytes())
    files = mapping(receipt["implementation_files"])
    assert set(files) == {
        "tools/faw08_d1_extraction.py",
        "tools/faw07_d0_demo.py",
        "tools/workbench.py",
        "tools/evidence_core.py",
        "tools/json_shapes.py",
    }
    for filename, digest in files.items():
        assert digest == _digest((ROOT / filename).read_bytes())
    indexed = {text_value(row["case_id"]): row for row in inputs}
    for result in results:
        case = indexed[text_value(result["case_id"])]
        _check_result(case, result)
        assert verify_extraction(case, result) is True
        assert "expected" not in case
        assert "expected_observations" not in case


@pytest.mark.parametrize("module", [False, True])
@pytest.mark.parametrize(
    "extra",
    [
        ["unexpected"],
        ["--case-file", "private.json"],
        ["--output", "receipt.json"],
        ["--model", "external"],
    ],
)
def test_independent_cli_rejects_non_demo_inputs(module: bool, extra: list[str]) -> None:
    result = _run_demo(module=module, extra=extra)
    assert result.returncode != 0
    assert result.stdout == b""
