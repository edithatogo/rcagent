"""Independent D2 windows, full implied orders, unknowns and evidence binding.

Literal temporal labels were frozen before either producer was read or run.
The scorer never substitutes replay equality for an independent temporal oracle.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import random
import subprocess
import sys
from collections import Counter, UserString
from copy import deepcopy
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools.faw09_d2_timeline import assemble_timeline, generate_receipt, verify_timeline

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests/fixtures/faw09_independent"
ORACLE = FIXTURES / "d2_oracle.json"
FROZEN_SHA256 = "dd3947ac70d54ccb5436040b1a190e19bba4f5b657a7b4781574eac76be13b92"
VIEW = "synthetic-d2-timeline-only"
CATEGORIES = ("events", "clocks", "relations", "amendments")
OUTPUT_CATEGORIES = {
    "events": "events",
    "clocks": "clock_assertions",
    "relations": "relations",
    "amendments": "amendments",
}
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


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _objects(value: object) -> list[ObjectMap]:
    return [mapping(row) for row in sequence(value)]


def _fixture() -> ObjectMap:
    return mapping(json.loads(ORACLE.read_text(encoding="utf-8")))


def _cases() -> list[ObjectMap]:
    return _objects(_fixture()["cases"])


def _item(identifier: str) -> ObjectMap:
    return next(row for row in _cases() if row["id"] == identifier)


def _input(identifier: str) -> ObjectMap:
    return deepcopy(mapping(_item(identifier)["input"]))


def _indexed(value: object) -> dict[str, ObjectMap]:
    return {text_value(row["id"]): row for row in _objects(value)}


def _equal(left: object, right: object) -> bool:
    return _canonical(left) == _canonical(right)


def _orders(result: ObjectMap) -> list[str]:
    orders: list[str] = []
    for pair in _objects(result.get("pairs", [])):
        if pair.get("order") == "before":
            orders.append(_canonical([pair["left_event_id"], pair["right_event_id"]]).decode())
        elif pair.get("order") == "after":
            orders.append(_canonical([pair["right_event_id"], pair["left_event_id"]]).decode())
    return orders


def _summaries(event: ObjectMap) -> dict[str, ObjectMap]:
    result = {"event": mapping(event["event_time"]), "recording": mapping(event["recording_time"])}
    for row in _objects(event["availability"]):
        result["availability:" + text_value(row["recipient_id"])] = mapping(row["clock"])
    return result


def _differences(expected: ObjectMap, result: ObjectMap) -> list[str]:
    errors: list[str] = []
    for category, output_key in (("events", "events"), ("clocks", "clock_assertions")):
        actual = _indexed(result.get(output_key, []))
        for row in _objects(expected[category]):
            identifier = text_value(row["id"])
            if identifier not in actual:
                errors.append(f"{category}:{identifier}:missing")
                continue
            for key, value in row.items():
                if key not in actual[identifier] or not _equal(actual[identifier][key], value):
                    errors.append(f"{category}:{identifier}:{key}")
    for key in ("pairs", "consistency"):
        if key not in result or not _equal(result[key], expected[key]):
            errors.append(key)
    for key, kind in (("asserted_edges", "asserted"), ("interval_edges", "interval")):
        edges = sorted(
            (row for row in _objects(result.get("edges", [])) if row["kind"] == kind),
            key=lambda row: (text_value(row["before_event_id"]), text_value(row["after_event_id"])),
        )
        if not _equal(edges, expected[key]):
            errors.append(key)
    if (result.get("display_order") is not None) != expected["display_order_present"]:
        errors.append("display_order_present")
    return errors


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def score_cases(expected_cases: list[ObjectMap], actual_cases: list[ObjectMap]) -> ObjectMap:
    """Count every expected event, clock, summary, pair and implied strict order.

    Failed/missing executions retain all denominators. The strict-order target is
    the frozen full closure, including transitive facts, never display order or
    merely the list of supplied edges. Alternative clock values remain intact.
    """
    count: Counter[str] = Counter()
    fields: Counter[str] = Counter()
    indexed: dict[str, list[ObjectMap]] = {}
    for actual in actual_cases:
        indexed.setdefault(text_value(actual["case_id"]), []).append(actual)
    for item in expected_cases:
        case = mapping(item["input"])
        expected = mapping(item["expected"])
        rows = indexed.pop(text_value(case["case_id"]), [])
        if rows and "result" in rows[0]:
            result = mapping(rows[0]["result"])
        else:
            count["execution_failures"] += 1
            result = {}
        for duplicate in rows[1:]:
            count["execution_failures"] += 1
            if "result" in duplicate:
                count["strict_order_false_positive"] += len(_orders(mapping(duplicate["result"])))
        target_orders = {
            _canonical(row).decode() for row in sequence(expected["full_implied_strict_orders"])
        }
        actual_orders = Counter(_orders(result))
        tp = sum(min(actual_orders[order], 1) for order in target_orders)
        count["expected_strict_orders"] += len(target_orders)
        count["strict_order_true_positive"] += tp
        count["strict_order_false_negative"] += len(target_orders) - tp
        count["strict_order_false_positive"] += sum(actual_orders.values()) - tp
        for category, output_key in (("events", "events"), ("clocks", "clock_assertions")):
            expected_ids = {text_value(row["id"]) for row in _objects(case[category])}
            actual_ids = Counter(
                text_value(row["id"]) for row in _objects(result.get(output_key, []))
            )
            retained = sum(min(actual_ids[identifier], 1) for identifier in expected_ids)
            count[f"expected_{category}"] += len(expected_ids)
            count[f"retained_{category}"] += retained
            count[f"extra_{category}"] += sum(actual_ids.values()) - retained
        clocks = _indexed(result.get("clock_assertions", []))
        for row in _objects(expected["clocks"]):
            interpretation = mapping(row["interpretation"])
            usable = interpretation["status"] in ("resolved", "ambiguous")
            denominator = "normalizable_clocks" if usable else "unresolved_clocks"
            count["expected_" + denominator] += 1
            observed = clocks.get(text_value(row["id"]))
            if observed is not None and _equal(observed.get("interpretation"), interpretation):
                count["correct_" + denominator] += 1
        events = _indexed(result.get("events", []))
        for event in _objects(expected["events"]):
            observed = events.get(text_value(event["id"]))
            actual_summaries = _summaries(observed) if observed is not None else {}
            for name, expected_summary in _summaries(event).items():
                count["expected_summaries"] += 1
                correct = name in actual_summaries and _equal(
                    actual_summaries[name], expected_summary
                )
                count["correct_summaries"] += correct
                if expected_summary["status"] in ("unknown", "unresolved"):
                    count["expected_unknown_summaries"] += 1
                    count["correct_unknown_summaries"] += correct
                if expected_summary["disagreement"] is True:
                    count["expected_disagreements"] += 1
                    count["correct_disagreements"] += correct
        pair_index = {
            (text_value(row["left_event_id"]), text_value(row["right_event_id"])): row
            for row in _objects(result.get("pairs", []))
        }
        for expected_pair in _objects(expected["pairs"]):
            count["expected_pairs"] += 1
            key = (
                text_value(expected_pair["left_event_id"]),
                text_value(expected_pair["right_event_id"]),
            )
            actual_pair = pair_index.get(key)
            correct = actual_pair is not None and _equal(actual_pair, expected_pair)
            count["correct_pairs"] += correct
            if expected_pair["order"] == "unknown":
                count["expected_unknown_orders"] += 1
                count["correct_unknown_orders"] += correct
        consistent = mapping(expected["consistency"])["status"] == "consistent"
        count["expected_consistent_cases" if consistent else "expected_inconsistent_cases"] += 1
        actual_consistency = result.get("consistency")
        count["correct_consistency_cases"] += _equal(actual_consistency, expected["consistency"])
        blocked = result.get("display_order") is None
        count["false_blocking"] += consistent and blocked
        count["false_acceptance"] += not consistent and not blocked
        fields.update(_differences(expected, result))
    for orphan_rows in indexed.values():
        for orphan in orphan_rows:
            count["execution_failures"] += 1
            if "result" in orphan:
                count["strict_order_false_positive"] += len(_orders(mapping(orphan["result"])))
    names = (
        "expected_events",
        "retained_events",
        "extra_events",
        "expected_clocks",
        "retained_clocks",
        "extra_clocks",
        "expected_pairs",
        "correct_pairs",
        "expected_strict_orders",
        "strict_order_true_positive",
        "strict_order_false_positive",
        "strict_order_false_negative",
        "expected_normalizable_clocks",
        "correct_normalizable_clocks",
        "expected_unresolved_clocks",
        "correct_unresolved_clocks",
        "expected_summaries",
        "correct_summaries",
        "expected_unknown_summaries",
        "correct_unknown_summaries",
        "expected_disagreements",
        "correct_disagreements",
        "expected_unknown_orders",
        "correct_unknown_orders",
        "expected_consistent_cases",
        "expected_inconsistent_cases",
        "correct_consistency_cases",
        "false_blocking",
        "false_acceptance",
        "execution_failures",
    )
    result_metrics: ObjectMap = {name: count[name] for name in names}
    result_metrics.update(
        {
            "case_count": len(expected_cases),
            "family_count": len({text_value(row["family"]) for row in expected_cases}),
            "strict_order_precision": _ratio(
                count["strict_order_true_positive"],
                count["strict_order_true_positive"] + count["strict_order_false_positive"],
            ),
            "strict_order_recall": _ratio(
                count["strict_order_true_positive"], count["expected_strict_orders"]
            ),
            "clock_normalization_recall": _ratio(
                count["correct_normalizable_clocks"], count["expected_normalizable_clocks"]
            ),
            "unresolved_clock_preservation": _ratio(
                count["correct_unresolved_clocks"], count["expected_unresolved_clocks"]
            ),
            "unknown_summary_preservation": _ratio(
                count["correct_unknown_summaries"], count["expected_unknown_summaries"]
            ),
            "disagreement_preservation": _ratio(
                count["correct_disagreements"], count["expected_disagreements"]
            ),
            "field_error_count": sum(fields.values()),
            "field_errors": dict(sorted(fields.items())),
        }
    )
    return result_metrics


def evaluate_oracle() -> ObjectMap:
    actual: list[ObjectMap] = []
    for item in _cases():
        case = deepcopy(mapping(item["input"]))
        row: ObjectMap = {"case_id": case["case_id"]}
        try:
            result = mapping(assemble_timeline(case))
            for key in ("events", "clock_assertions", "pairs", "edges"):
                _objects(result[key])
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
        ) as error:
            row["execution_error"] = {"type": type(error).__name__, "message": str(error)}
        actual.append(row)
    return {
        "oracle_sha256": hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
        "actual_cases": actual,
        "metrics": score_cases(_cases(), actual),
    }


def _source_index(case: ObjectMap) -> dict[tuple[str, int], ObjectMap]:
    index: dict[tuple[str, int], ObjectMap] = {}
    for source in _objects(case["sources"]):
        version = source["version"]
        assert isinstance(version, int)
        assert not isinstance(version, bool)
        index[(text_value(source["id"]), version)] = source
    return index


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
    for key, value in mapping(_fixture()["expected_constants"]).items():
        assert key in result
        assert _equal(result[key], value)
    assert result["case_id"] == case["case_id"]
    assert set(result) == {
        "schema_version",
        "case_id",
        "permitted_view",
        "linkage_basis",
        "rule_version",
        "source_admission",
        "sources",
        "recipients",
        "events",
        "clock_assertions",
        "relations",
        "amendments",
        "edges",
        "pairs",
        "consistency",
        "display_order",
        "display_order_is_temporal_evidence",
        "event_count",
    }
    assert result["recipients"] == sorted(
        text_value(value) for value in sequence(case["recipients"])
    )
    assert result["event_count"] == len(sequence(case["events"]))
    for category in CATEGORIES:
        inputs = _indexed(case[category])
        observed = _objects(result[OUTPUT_CATEGORIES[category]])
        assert [row["id"] for row in observed] == sorted(inputs)
        bindings: set[str] = set()
        for row in observed:
            original = inputs[text_value(row["id"])]
            identifier = text_value(row["binding_id"])
            assert identifier
            assert identifier not in bindings
            bindings.add(identifier)
            evidence = mapping(row["evidence"])
            _check_span(case, evidence)
            for field in SPAN_FIELDS:
                assert _equal(evidence[field], mapping(original["evidence"])[field])
            assert evidence["verified"] is True
            assert evidence["evidence_id"] == category + ":" + text_value(row["id"])
            for field, value in original.items():
                if field != "evidence":
                    assert _equal(row[field], value)
            if category == "events":
                assert set(row) == {
                    "id",
                    "binding_id",
                    "evidence",
                    "assertion",
                    "event_time",
                    "recording_time",
                    "availability",
                }
                assert row["assertion"] == {
                    "text": evidence["text"],
                    "actor": None,
                    "subject": None,
                    "polarity": "not_interpreted",
                }
                assert [
                    availability["recipient_id"] for availability in _objects(row["availability"])
                ] == result["recipients"]
            elif category == "clocks":
                assert set(row) == {
                    "id",
                    "binding_id",
                    "event_id",
                    "kind",
                    "recipient_id",
                    "evidence",
                    "interpretation",
                    "active",
                    "superseded_by",
                }
                assert set(mapping(row["interpretation"])) == {"status", "reason", "windows"}
                for window in _objects(mapping(row["interpretation"])["windows"]):
                    assert set(window) == {
                        "local_start",
                        "local_end",
                        "utc_start",
                        "utc_end",
                        "precision",
                        "timezone",
                    }
    sources = _source_index(case)
    summaries = _objects(result["sources"])
    assert [(row["source_id"], row["version"]) for row in summaries] == sorted(sources)
    for row in summaries:
        version = row["version"]
        assert isinstance(version, int)
        original = sources[(text_value(row["source_id"]), version)]
        raw = text_value(original["content"]).encode("utf-8")
        assert row["state"] == "present"
        assert row["case_id"] == case["case_id"]
        assert row["sha256"] == _digest(raw)
        assert row["bytes"] == len(raw)
    event_ids = sorted(text_value(row["id"]) for row in _objects(case["events"]))
    pairs = _objects(result["pairs"])
    assert [(row["left_event_id"], row["right_event_id"]) for row in pairs] == list(
        itertools.combinations(event_ids, 2)
    )
    for row in pairs:
        assert set(row) == {
            "left_event_id",
            "right_event_id",
            "interval_relation",
            "order",
            "basis",
        }
    display = result["display_order"]
    if display is None:
        assert mapping(result["consistency"])["status"] == "inconsistent"
        assert all(row["order"] == "inconsistent" for row in pairs)
    else:
        presented = [text_value(value) for value in sequence(display)]
        assert sorted(presented) == event_ids
        positions = {identifier: index for index, identifier in enumerate(presented)}
        for edge in _objects(result["edges"]):
            assert (
                positions[text_value(edge["before_event_id"])]
                < positions[text_value(edge["after_event_id"])]
            )


def test_independent_frozen_oracle_and_all_coordinates() -> None:
    assert hashlib.sha256(ORACLE.read_bytes()).hexdigest() == FROZEN_SHA256
    freeze = mapping(json.loads((FIXTURES / "freeze.json").read_text(encoding="utf-8")))
    assert freeze["oracle_sha256"] == FROZEN_SHA256
    assert freeze["producer_executions_before_freeze"] == 0
    assert freeze["production_source_read_before_freeze"] is False
    assert len(_cases()) == 34
    for item in _cases():
        case = mapping(item["input"])
        for category in CATEGORIES:
            for row in _objects(case[category]):
                _check_span(case, mapping(row["evidence"]))


@pytest.mark.parametrize("identifier", [text_value(row["id"]) for row in _cases()])
def test_independent_literal_temporal_expectations(identifier: str) -> None:
    item = _item(identifier)
    case = deepcopy(mapping(item["input"]))
    before = deepcopy(case)
    result = mapping(assemble_timeline(case))
    assert case == before
    _check_result(case, result)
    assert _differences(mapping(item["expected"]), result) == []
    assert verify_timeline(case, json.loads(_canonical(result))) is True


def test_independent_aggregate_metrics_include_full_implied_order() -> None:
    metrics = mapping(evaluate_oracle()["metrics"])
    assert metrics["case_count"] == 34
    assert metrics["family_count"] == 15
    assert metrics["expected_events"] == metrics["retained_events"] == 73
    assert metrics["expected_clocks"] == metrics["retained_clocks"] == 74
    assert metrics["expected_pairs"] == metrics["correct_pairs"] == 46
    assert metrics["expected_strict_orders"] == metrics["strict_order_true_positive"] == 12
    assert metrics["expected_normalizable_clocks"] == metrics["correct_normalizable_clocks"] == 61
    assert metrics["expected_unresolved_clocks"] == metrics["correct_unresolved_clocks"] == 13
    assert metrics["expected_summaries"] == metrics["correct_summaries"] == 158
    assert metrics["expected_unknown_summaries"] == metrics["correct_unknown_summaries"] == 105
    assert metrics["expected_disagreements"] == metrics["correct_disagreements"] == 3
    assert metrics["expected_consistent_cases"] == 29
    assert metrics["expected_inconsistent_cases"] == 5
    assert metrics["correct_consistency_cases"] == 34
    for name in (
        "strict_order_false_positive",
        "strict_order_false_negative",
        "field_error_count",
        "false_blocking",
        "false_acceptance",
        "execution_failures",
        "extra_events",
        "extra_clocks",
    ):
        assert metrics[name] == 0, metrics
    assert metrics["strict_order_precision"] == metrics["strict_order_recall"] == 1.0


def test_independent_scorer_penalizes_all_unknown_missing_and_direct_only_orders() -> None:
    missing = score_cases(_cases(), [])
    assert missing["expected_events"] == 73
    assert missing["retained_events"] == 0
    assert missing["expected_clocks"] == 74
    assert missing["execution_failures"] == 34
    assert missing["strict_order_false_negative"] == 12
    assert missing["strict_order_precision"] is None
    assert missing["strict_order_recall"] == 0
    item = _item("asserted-transitive-closure")
    expected = mapping(item["expected"])
    direct_pairs = deepcopy(_objects(expected["pairs"]))
    for pair in direct_pairs:
        if pair["basis"] == ["transitive"]:
            pair["order"] = "unknown"
            pair["basis"] = []
    result: ObjectMap = {
        "events": expected["events"],
        "clock_assertions": [],
        "pairs": direct_pairs,
        "edges": expected["asserted_edges"],
        "consistency": expected["consistency"],
        "display_order": ["A", "B", "C"],
    }
    observed = [{"case_id": mapping(item["input"])["case_id"], "result": result}]
    partial = score_cases([item], observed)
    assert partial["strict_order_true_positive"] == 2
    assert partial["strict_order_false_negative"] == 1
    for pair in direct_pairs:
        pair["order"] = "unknown"
        pair["basis"] = []
    abstained = score_cases([item], observed)
    assert abstained["strict_order_true_positive"] == 0
    assert abstained["strict_order_false_negative"] == 3
    assert abstained["strict_order_precision"] is None


def _empty_case(content: str = "Administrative synthetic source") -> ObjectMap:
    return {
        "case_id": "independent-boundary",
        "permitted_view": VIEW,
        "sources": [
            {
                "id": "note",
                "version": 1,
                "case_id": "independent-boundary",
                "state": "present",
                "content": content,
                "fingerprint": _digest(content.encode("utf-8")),
            }
        ],
        "recipients": [],
        "events": [],
        "clocks": [],
        "relations": [],
        "amendments": [],
    }


@pytest.mark.parametrize("value", [None, False, 7, "case", [], {}, range(10**100)])
def test_independent_malformed_case_containers_rejected(value: object) -> None:
    with pytest.raises(ValueError) as error:
        assemble_timeline(value)
    assert str(error.value)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("case_id", ""),
        ("case_id", True),
        ("case_id", "a" * 129),
        ("permitted_view", "clinical"),
        ("permitted_view", [VIEW]),
        ("permitted_view", UserString(VIEW)),
        ("sources", []),
        ("sources", [None]),
        ("sources", {}),
        ("sources", [None] * 33),
        ("recipients", {}),
        ("recipients", [False]),
        ("recipients", ["r", "r"]),
        ("recipients", [str(index) for index in range(17)]),
        ("events", {}),
        ("events", [None] * 17),
        ("clocks", [None] * 33),
        ("relations", [None] * 33),
        ("amendments", [None] * 17),
    ],
)
def test_independent_case_shape_type_and_count_limits(key: str, value: object) -> None:
    case = _empty_case()
    case[key] = value
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    "key",
    [
        "case_id",
        "permitted_view",
        "sources",
        "recipients",
        "events",
        "clocks",
        "relations",
        "amendments",
    ],
)
def test_independent_required_arrays_and_fields_not_defaulted(key: str) -> None:
    case = _empty_case()
    del case[key]
    with pytest.raises(ValueError):
        assemble_timeline(case)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("id", ""),
        ("id", "s" * 129),
        ("version", True),
        ("version", 0),
        ("version", "1"),
        ("case_id", "other"),
        ("state", "unknown"),
        ("state", "withdrawn"),
        ("state", UserString("present")),
        ("content", ""),
        ("content", "\ud800"),
        ("content", []),
        ("fingerprint", "sha256:" + "0" * 64),
    ],
)
def test_independent_source_admission_types_states_and_bindings(key: str, value: object) -> None:
    case = _empty_case()
    source = _objects(case["sources"])[0]
    source[key] = value
    if key == "content" and value == "":
        source["fingerprint"] = _digest(b"")
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    "category", ["case", "sources", "events", "clocks", "relations", "amendments", "evidence"]
)
def test_independent_unknown_fields_are_rejected(category: str) -> None:
    case = _input("explicit-amendment")
    if category == "case":
        target = case
    elif category == "evidence":
        target = mapping(_objects(case["events"])[0]["evidence"])
    elif category == "relations":
        case = _input("asserted-transitive-closure")
        target = _objects(case[category])[0]
    else:
        target = _objects(case[category])[0]
    target["undeclared"] = "must not disappear"
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize("category", ["sources", *CATEGORIES])
def test_independent_duplicate_domain_identities_rejected(category: str) -> None:
    case = _input(
        "explicit-amendment" if category != "relations" else "asserted-transitive-closure"
    )
    sequence(case[category]).append(deepcopy(_objects(case[category])[0]))
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("case_id", "other"),
        ("source_id", "missing"),
        ("source_version", 99),
        ("source_sha256", "sha256:" + "0" * 64),
        ("coordinate_system", "unicode-codepoint"),
        ("start_byte", -1),
        ("start_byte", True),
        ("end_byte", 65537),
        ("text", "invented"),
    ],
)
def test_independent_forged_clock_span_rejected(field: str, value: object) -> None:
    case = _input("offsets-unicode")
    mapping(_objects(case["clocks"])[0]["evidence"])[field] = value
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("event_id", "not-an-event"),
        ("event_id", "ca"),
        ("kind", "other"),
        ("kind", []),
        ("kind", UserString("event")),
        ("recipient_id", "nurse"),
    ],
)
def test_independent_clock_domain_and_enum_types_rejected(field: str, value: object) -> None:
    case = _input("offsets-unicode")
    _objects(case["clocks"])[0][field] = value
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize("recipient", [None, "unlisted", True])
def test_independent_availability_requires_listed_typed_recipient(recipient: object) -> None:
    case = _input("three-clocks-recipients")
    row = next(row for row in _objects(case["clocks"]) if row["kind"] == "availability")
    row["recipient_id"] = recipient
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    ("field", "value"),
    [("before_event_id", "missing"), ("after_event_id", "ab"), ("before_event_id", True)],
)
def test_independent_graph_endpoints_validated_before_topological_sort(
    field: str, value: object
) -> None:
    case = _input("asserted-transitive-closure")
    _objects(case["relations"])[0][field] = value
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


@pytest.mark.parametrize(
    "mutation",
    [
        "unknown-old",
        "same-clock",
        "reverse-version",
        "different-event",
        "different-kind",
        "wrong-evidence-version",
    ],
)
def test_independent_amendments_require_exact_matching_bindings(mutation: str) -> None:
    case = _input("explicit-amendment")
    amendment = _objects(case["amendments"])[0]
    clocks = _indexed(case["clocks"])
    if mutation == "unknown-old":
        amendment["earlier_clock_id"] = "missing"
    elif mutation == "same-clock":
        amendment["later_clock_id"] = amendment["earlier_clock_id"]
    elif mutation == "reverse-version":
        amendment["earlier_clock_id"], amendment["later_clock_id"] = (
            amendment["later_clock_id"],
            amendment["earlier_clock_id"],
        )
    elif mutation == "different-event":
        clocks["a-new"]["event_id"] = "B"
    elif mutation == "different-kind":
        clocks["a-new"]["kind"] = "recording"
    else:
        amendment["evidence"] = deepcopy(clocks["a-old"]["evidence"])
    with pytest.raises(ValueError) as error:
        assemble_timeline(case)
    assert str(error.value)


def test_independent_resource_bounds_no_events_and_early_total_limit() -> None:
    case = _empty_case("é" * 32768)
    result = mapping(assemble_timeline(case))
    _check_result(case, result)
    assert result["events"] == result["clock_assertions"] == result["pairs"] == []
    assert result["display_order"] == []
    with pytest.raises(ValueError):
        assemble_timeline(_empty_case("é" * 32769))
    case = _empty_case()
    source = _objects(case["sources"])[0]
    case["sources"] = [{**source, "id": f"source-{index}"} for index in range(32)]
    case["recipients"] = [f"recipient-{index}" for index in range(16)]
    result = mapping(assemble_timeline(case))
    assert len(sequence(result["sources"])) == 32
    assert len(sequence(result["recipients"])) == 16
    case = _empty_case()
    case.update({"events": [None] * 16, "clocks": [None] * 32, "relations": [None] * 17})
    with pytest.raises(ValueError, match="64"):
        assemble_timeline(case)


@pytest.mark.parametrize(
    "identifier", ["three-clocks-recipients", "amendment-chain", "asserted-transitive-closure"]
)
@given(st.integers(min_value=0, max_value=2**32 - 1))
@settings(max_examples=30, deadline=None)
def test_independent_all_input_array_permutations_preserve_canonical_case(
    identifier: str, seed: int
) -> None:
    case = _input(identifier)
    before = mapping(assemble_timeline(case))
    shuffled = deepcopy(case)
    generator = random.Random(seed)
    for key in ("sources", "recipients", *CATEGORIES):
        generator.shuffle(sequence(shuffled[key]))
    after = mapping(assemble_timeline(shuffled))
    assert _canonical(after) == _canonical(before)
    assert mapping(assemble_timeline(deepcopy(case))) == before


def test_independent_association_and_recipient_changes_rebind_without_inference() -> None:
    case = _input("offsets-unicode")
    before = mapping(assemble_timeline(case))
    _objects(case["clocks"])[0]["event_id"] = "B"
    changed = mapping(assemble_timeline(case))
    assert _indexed(changed["events"])["A"]["event_time"] == {
        "assertion_ids": [],
        "active_assertion_ids": [],
        "status": "unknown",
        "reasons": ["no_assertion"],
        "disagreement": False,
        "windows": None,
    }
    assert _objects(changed["pairs"])[0]["order"] == "unknown"
    assert (
        _indexed(changed["clock_assertions"])["ca"]["binding_id"]
        != _indexed(before["clock_assertions"])["ca"]["binding_id"]
    )
    assert verify_timeline(case, before) is False
    case = _input("three-clocks-recipients")
    before = mapping(assemble_timeline(case))
    _indexed(case["clocks"])["aa"]["recipient_id"] = "doctor"
    changed = mapping(assemble_timeline(case))
    availability = {
        text_value(row["recipient_id"]): mapping(row["clock"])
        for row in _objects(_indexed(changed["events"])["A"]["availability"])
    }
    assert availability["doctor"]["status"] == "known"
    assert availability["nurse"]["status"] == "unknown"
    assert changed["pairs"] == before["pairs"]
    assert verify_timeline(case, before) is False


def test_independent_amendment_removal_keeps_both_accounts_and_changes_order() -> None:
    case = _input("explicit-amendment")
    previous = mapping(assemble_timeline(case))
    case["amendments"] = []
    result = mapping(assemble_timeline(case))
    summary = mapping(_indexed(result["events"])["A"]["event_time"])
    assert summary["status"] == "conflicting"
    assert summary["active_assertion_ids"] == ["a-new", "a-old"]
    assert _objects(result["pairs"])[0]["order"] == "unknown"
    assert all(row["active"] is True for row in _objects(result["clock_assertions"]))
    assert verify_timeline(case, previous) is False


@pytest.mark.parametrize(
    "field",
    [
        "schema_version",
        "case_id",
        "permitted_view",
        "linkage_basis",
        "rule_version",
        "source_admission",
        "sources",
        "recipients",
        "events",
        "clock_assertions",
        "relations",
        "amendments",
        "edges",
        "pairs",
        "consistency",
        "display_order",
        "display_order_is_temporal_evidence",
        "event_count",
    ],
)
def test_independent_every_case_result_field_replay_bound(field: str) -> None:
    case = _input("three-clocks-recipients")
    result = mapping(assemble_timeline(case))
    assert verify_timeline(case, result) is True
    result[field] = {"forged": True}
    assert verify_timeline(case, result) is False


@pytest.mark.parametrize(
    "field",
    [
        "id",
        "binding_id",
        "event_id",
        "kind",
        "recipient_id",
        "evidence",
        "interpretation",
        "active",
        "superseded_by",
    ],
)
def test_independent_every_clock_assertion_field_replay_bound(field: str) -> None:
    case = _input("explicit-amendment")
    result = mapping(assemble_timeline(case))
    _objects(result["clock_assertions"])[0][field] = {"forged": True}
    assert verify_timeline(case, result) is False


def test_independent_replay_rejects_cyclic_and_unencodable_result_objects() -> None:
    case = _input("offsets-unicode")
    circular: ObjectMap = {}
    circular["loop"] = circular
    assert verify_timeline(case, circular) is False
    assert verify_timeline(case, {"bad": "\ud800"}) is False
    assert verify_timeline(case, object()) is False


def _run_demo(
    *, module: bool = False, extra: list[str] | None = None
) -> subprocess.CompletedProcess[bytes]:
    target = ["tools.faw09_d2_timeline"] if module else ["tools.workbench", "d2-demo"]
    return subprocess.run(
        [sys.executable, "-m", *target, *(extra or [])],
        cwd=ROOT,
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "ascii"},
        timeout=20,
        check=False,
    )


def test_independent_actual_cli_bytes_and_all_receipt_bindings() -> None:
    first, second, direct = _run_demo(), _run_demo(), _run_demo(module=True)
    assert first.returncode == second.returncode == direct.returncode == 0
    assert first.stderr == second.stderr == direct.stderr == b""
    assert first.stdout == second.stdout == direct.stdout
    receipt = mapping(json.loads(first.stdout))
    assert first.stdout == _canonical(receipt) + b"\n"
    assert receipt == mapping(generate_receipt())
    assert receipt["schema_version"] == "faw09-d2-receipt-1.0"
    assert receipt["permitted_view"] == VIEW
    assert receipt["rule_version"] == "faw09-d2-rules-1.0"
    assert receipt["command"] == "uv run --no-sync python -m tools.workbench d2-demo"
    inputs, results = _objects(receipt["inputs"]), _objects(receipt["cases"])
    assert receipt["case_count"] == len(inputs) == len(results)
    assert len(inputs) >= 10
    assert receipt["input_fingerprint"] == _digest(_canonical(inputs))
    unsigned = {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    assert receipt["output_fingerprint"] == _digest(_canonical(unsigned))
    assert receipt["dependency_lock_sha256"] == _digest((ROOT / "uv.lock").read_bytes())
    files = mapping(receipt["implementation_files"])
    assert set(files) == {
        "tools/faw09_d2_timeline.py",
        "tools/faw09_d2_clock.py",
        "tools/faw07_d0_demo.py",
        "tools/workbench.py",
        "tools/evidence_core.py",
        "tools/json_shapes.py",
    }
    for filename, digest in files.items():
        assert digest == _digest((ROOT / filename).read_bytes())
    index = {text_value(row["case_id"]): row for row in inputs}
    for result in results:
        case = index[text_value(result["case_id"])]
        _check_result(case, result)
        assert verify_timeline(case, result) is True
        assert "expected" not in case
        assert "expected_orders" not in case


@pytest.mark.parametrize("module", [False, True])
@pytest.mark.parametrize(
    "extra",
    [
        ["unexpected"],
        ["--case-file", "private.json"],
        ["--model", "external"],
        ["--output", "receipt.json"],
    ],
)
def test_independent_cli_accepts_only_fixed_synthetic_demo(module: bool, extra: list[str]) -> None:
    result = _run_demo(module=module, extra=extra)
    assert result.returncode != 0
    assert result.stdout == b""
