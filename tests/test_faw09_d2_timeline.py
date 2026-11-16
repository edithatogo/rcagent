"""Boundary and metamorphic tests; independent literal labels live separately."""

from __future__ import annotations

from collections import UserString
from copy import deepcopy
from datetime import date, timedelta
from hashlib import sha256

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tools.evidence_core import canonical_bytes
from tools.faw09_d2_clock import interpret_clock
from tools.faw09_d2_timeline import assemble_timeline, generate_receipt, verify_timeline
from tools.json_shapes import JsonObject, is_array, require_object


def source(text: str, version: int = 1) -> JsonObject:
    return {
        "id": "source",
        "version": version,
        "case_id": "case",
        "state": "present",
        "content": text,
        "fingerprint": "sha256:" + sha256(text.encode()).hexdigest(),
    }


def span(text: str, quote: str, version: int = 1) -> JsonObject:
    start = text.index(quote)
    return {
        "case_id": "case",
        "source_id": "source",
        "source_version": version,
        "source_sha256": "sha256:" + sha256(text.encode()).hexdigest(),
        "coordinate_system": "utf8-byte",
        "start_byte": len(text[:start].encode()),
        "end_byte": len(text[: start + len(quote)].encode()),
        "text": quote,
    }


def timeline(
    times: tuple[str, ...] = ("2026-11-17T09:00:00Z", "2026-11-17T10:00:00Z"),
) -> JsonObject:
    text = "🧪 " + "\n".join(f"event-{i}: {t}" for i, t in enumerate(times))
    events: list[JsonObject] = []
    clocks: list[JsonObject] = []
    for i, value in enumerate(times):
        events.append({"id": f"e{i}", "evidence": span(text, f"event-{i}")})
        clocks.append(
            {
                "id": f"c{i}",
                "event_id": f"e{i}",
                "kind": "event",
                "recipient_id": None,
                "evidence": span(text, value),
            }
        )
    return {
        "case_id": "case",
        "permitted_view": "synthetic-d2-timeline-only",
        "sources": [source(text)],
        "recipients": ["rn-a", "rn-b"],
        "events": events,
        "clocks": clocks,
        "relations": [],
        "amendments": [],
    }


def rows(case: JsonObject, key: str) -> list[JsonObject]:
    value = case[key]
    if not is_array(value):
        raise ValueError("test case array required")
    return [require_object(item, context="test row") for item in value]


def add_relation(case: JsonObject, before: str, after: str, rid: str = "r") -> None:
    case["relations"] = [
        *rows(case, "relations"),
        {
            "id": rid,
            "before_event_id": before,
            "after_event_id": after,
            "evidence": rows(case, "events")[0]["evidence"],
        },
    ]


def test_strict_order_and_missing_clocks() -> None:
    result = assemble_timeline(timeline())
    assert result["pairs"][0]["order"] == "before"
    assert result["consistency"]["status"] == "consistent"
    assert result["events"][0]["recording_time"]["windows"] is None
    assert all(item["clock"]["windows"] is None for item in result["events"][0]["availability"])
    assert result["display_order_is_temporal_evidence"] is False


@pytest.mark.parametrize(
    ("expression", "status", "reason"),
    [
        ("2026-11-17T09:00Z", "resolved", None),
        ("2026-11-17", "unknown", "timezone_unknown"),
        ("2026-11-17T09:00-00:00", "unknown", "offset_unknown"),
        ("2026-11-01T01:30 America/New_York", "unknown", "named_timezone_unresolved"),
        ("2026-03-08T02:30 America/New_York", "unknown", "named_timezone_unresolved"),
        ("2026-02-30T09:00Z", "invalid", "invalid_calendar_or_time"),
        ("2026-11-17T24:00Z", "invalid", "invalid_calendar_or_time"),
        ("2026-11-17T09:00+14:01", "invalid", "invalid_offset"),
        ("0001-01-01T00:00+14:00", "invalid", "utc_out_of_range"),
        ("9999-12-31T23:59-14:00", "invalid", "utc_out_of_range"),
        ("2 hours later", "unsupported", "unsupported_clock_expression"),
        ("2026-11-17T09:00:00.5Z", "unsupported", "unsupported_clock_expression"),
        ("unknown", "unknown", "explicit_unknown"),
    ],
)
def test_clock_statuses(expression: str, status: str, reason: str | None) -> None:
    result = interpret_clock(expression)
    assert result["status"] == status
    assert result["reason"] == reason


def test_minute_and_day_are_windows() -> None:
    minute = interpret_clock("2026-11-17T09:00+10:00")["windows"][0]
    assert minute["utc_start"] == "2026-11-16T23:00:00Z"
    assert minute["utc_end"] == "2026-11-16T23:00:59Z"
    day = interpret_clock("2026-11-17")["windows"][0]
    assert day["local_start"] == "2026-11-17T00:00:00"
    assert day["local_end"] == "2026-11-17T23:59:59"
    assert day["utc_start"] is None


@pytest.mark.parametrize(
    ("left", "right", "order"),
    [
        ("2026-11-17T09:00Z", "2026-11-17T09:00:30Z", "unknown"),
        ("2026-11-17T09:00:00Z", "2026-11-17T19:00:00+10:00", "same_reported_time"),
        ("2026-11-17T09:00:00Z to 2026-11-17T10:00:00Z", "2026-11-17T10:00:00Z", "unknown"),
        ("2026-11-17T09:00", "2026-11-17T10:00", "unknown"),
        ("2026-11-17T11:00:00Z", "2026-11-17T10:00:00Z", "after"),
    ],
)
def test_pair_windows(left: str, right: str, order: str) -> None:
    assert assemble_timeline(timeline((left, right)))["pairs"][0]["order"] == order


def test_cycle_keeps_evidence_and_withholds_order() -> None:
    case = timeline(("unknown", "unknown", "unknown"))
    for i in range(3):
        add_relation(case, f"e{i}", f"e{(i + 1) % 3}", str(i))
    result = assemble_timeline(case)
    assert result["consistency"]["cycle_event_ids"] == ["e0", "e1", "e2"]
    assert len(result["relations"]) == 3
    assert result["display_order"] is None
    assert all(pair["order"] == "inconsistent" for pair in result["pairs"])


def test_equal_time_precedence_is_infeasible() -> None:
    case = timeline(("2026-11-17T09:00:00Z",) * 2)
    add_relation(case, "e0", "e1")
    result = assemble_timeline(case)
    assert result["consistency"]["infeasible_event_ids"] == ["e1"]
    assert result["pairs"][0]["interval_relation"] == "same_reported_time"
    assert result["display_order"] is None


def test_transitive_second_resolution_infeasibility() -> None:
    case = timeline(("2026-11-17T09:00:00Z", "unknown", "2026-11-17T09:00:01Z"))
    add_relation(case, "e0", "e1", "r1")
    add_relation(case, "e1", "e2", "r2")
    result = assemble_timeline(case)
    assert result["consistency"]["infeasible_event_ids"] == ["e2"]


def test_unknown_time_can_have_asserted_order() -> None:
    case = timeline(("unknown",) * 3)
    add_relation(case, "e0", "e1", "r1")
    add_relation(case, "e1", "e2", "r2")
    result = assemble_timeline(case)
    pair = next(
        p for p in result["pairs"] if p["left_event_id"] == "e0" and p["right_event_id"] == "e2"
    )
    assert pair["order"] == "before"
    assert pair["basis"] == ["transitive"]
    assert result["events"][1]["event_time"]["windows"] is None


def test_input_permutation_and_no_mutation() -> None:
    case = timeline()
    original = deepcopy(case)
    result = assemble_timeline(case)
    assert case == original
    for key in ("sources", "events", "clocks", "recipients"):
        value = case[key]
        if is_array(value):
            case[key] = list(reversed(value))
    assert assemble_timeline(case) == result


def test_recording_and_recipient_clocks_do_not_supply_event_time() -> None:
    case = timeline()
    clocks = rows(case, "clocks")
    clocks[0]["kind"] = "recording"
    clocks[1]["kind"] = "availability"
    clocks[1]["recipient_id"] = "rn-a"
    case["clocks"] = clocks
    result = assemble_timeline(case)
    assert result["pairs"][0]["order"] == "unknown"
    assert result["events"][0]["recording_time"]["status"] == "known"
    assert result["events"][1]["availability"][0]["clock"]["status"] == "known"
    assert result["events"][1]["availability"][1]["clock"]["status"] == "unknown"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("case_id", "other"),
        ("source_version", 2),
        ("source_sha256", "sha256:" + "0" * 64),
        ("coordinate_system", "character"),
        ("start_byte", 1),
        ("text", "forged"),
    ],
)
def test_corrupt_bindings_fail(field: str, value: object) -> None:
    case = timeline()
    events = rows(case, "events")
    evidence = require_object(events[0]["evidence"], context="test evidence")
    evidence[field] = value
    case["events"] = events
    with pytest.raises(ValueError, match="admission"):
        assemble_timeline(case)


@pytest.mark.parametrize(
    "key", ["sources", "events", "clocks", "relations", "amendments", "recipients"]
)
def test_array_overflow_rejected_before_members(key: str) -> None:
    case = timeline()
    case[key] = [None] * 65
    with pytest.raises(ValueError, match="exceeds"):
        assemble_timeline(case)


def test_unknown_graph_endpoint_and_duplicate_ids_rejected() -> None:
    case = timeline()
    add_relation(case, "e0", "absent")
    with pytest.raises(ValueError, match="unknown event"):
        assemble_timeline(case)
    case = timeline()
    events = rows(case, "events")
    case["events"] = [events[0], events[0]]
    with pytest.raises(ValueError, match="duplicate events"):
        assemble_timeline(case)


def test_withdrawal_and_unknown_keys_fail_closed() -> None:
    case = timeline()
    sources = rows(case, "sources")
    sources[0]["state"] = "withdrawn"
    case["sources"] = sources
    with pytest.raises(ValueError, match="present sources"):
        assemble_timeline(case)
    case = timeline()
    case["now"] = "2026-11-17T09:00Z"
    with pytest.raises(ValueError, match="fields"):
        assemble_timeline(case)


@pytest.mark.parametrize("field", ["permitted_view", "kind"])
def test_string_like_enum_is_not_a_json_string(field: str) -> None:
    case = timeline()
    if field == "permitted_view":
        case[field] = UserString("synthetic-d2-timeline-only")
    else:
        clocks = rows(case, "clocks")
        clocks[0][field] = UserString("event")
        case["clocks"] = clocks
    with pytest.raises(ValueError, match="nonempty text"):
        assemble_timeline(case)


def test_non_object_with_unrepresentable_length_is_rejected() -> None:
    with pytest.raises(ValueError, match="object"):
        assemble_timeline(range(1 << 100))


def test_replay_rejects_tampering_cycles_and_non_json() -> None:
    case = timeline()
    result = assemble_timeline(case)
    assert verify_timeline(case, result)
    result["pairs"][0]["order"] = "unknown"
    assert not verify_timeline(case, result)
    cycle: list[object] = []
    cycle.append(cycle)
    assert not verify_timeline(case, cycle)
    assert not verify_timeline(case, {"x": object()})
    assert not verify_timeline(case, "\ud800")


def test_demo_is_deterministic_and_replays_every_case() -> None:
    receipt = generate_receipt()
    assert canonical_bytes(receipt) == canonical_bytes(generate_receipt())
    assert receipt["case_count"] >= 6
    for case, result in zip(receipt["inputs"], receipt["cases"], strict=True):
        assert verify_timeline(case, result)


@settings(max_examples=35, deadline=None)
@given(st.dates(min_value=date(2000, 1, 2), max_value=date(2099, 12, 1)), st.integers(1, 20))
def test_uniform_day_shift_preserves_order(day: date, shift: int) -> None:
    before = timeline((f"{day.isoformat()}T09:00:00Z", f"{day.isoformat()}T10:00:00Z"))
    moved = day + timedelta(days=shift)
    after = timeline((f"{moved.isoformat()}T09:00:00Z", f"{moved.isoformat()}T10:00:00Z"))
    assert assemble_timeline(before)["pairs"] == assemble_timeline(after)["pairs"]
