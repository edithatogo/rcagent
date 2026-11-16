"""Boundary and metamorphic tests for the declared D1 lexical profile."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from datetime import date
from hashlib import sha256
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tools.faw08_d1_extraction import extract_case, generate_receipt, verify_extraction
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]


def make_case(text: str, *, order: str = "unknown") -> JsonObject:
    return {
        "case_id": "test-case",
        "permitted_view": "synthetic-d1-extraction-only",
        "date_order": order,
        "sources": [
            {
                "id": "source-a",
                "case_id": "test-case",
                "version": 1,
                "state": "present",
                "content": text,
                "fingerprint": "sha256:" + sha256(text.encode()).hexdigest(),
            }
        ],
    }


def source(case: JsonObject) -> JsonObject:
    rows = case["sources"]
    assert is_array(rows)
    return require_object(rows[0], context="test source")


def anchored_case(text: str, anchor: str) -> JsonObject:
    case = make_case(text)
    start = text.index(anchor)
    case["anchors"] = [
        {
            "case_id": case["case_id"],
            "source_id": "source-a",
            "source_version": 1,
            "source_sha256": source(case)["fingerprint"],
            "coordinate_system": "utf8-byte",
            "start_byte": len(text[:start].encode()),
            "end_byte": len(text[: start + len(anchor)].encode()),
            "text": anchor,
        }
    ]
    return case


def test_explicit_unicode_date_clock_quantity_and_raw_provenance() -> None:
    text = "🧪 Café: on 2024-02-29 at 00:00, pulse was 90 bpm."
    result = extract_case(make_case(text))
    assert [row["kind"] for row in result["observations"]] == ["date", "time", "quantity"]
    assert result["observations"][0]["normalized"] == {
        "year": 2024,
        "month": 2,
        "day": 29,
        "iso": "2024-02-29",
        "alternatives": [],
    }
    assert result["observations"][1]["normalized"] == {"time": "00:00:00", "precision": "minute"}
    assert result["observations"][2]["normalized"] == {"value": "90", "unit": "bpm"}
    for row in result["observations"]:
        assert text.encode()[row["start_byte"] : row["end_byte"]].decode() == row["text"]
        assert row["source_sha256"] == "sha256:" + sha256(text.encode()).hexdigest()
        assert row["recording_time"] is row["availability_time"] is row["timezone"] is None
        assert row["event_linkage"] is None


@pytest.mark.parametrize("text", ["2023-02-29", "2024-04-31", "2024-00-15", "0000-01-01"])
def test_invalid_dates_remain_one_literal_candidate(text: str) -> None:
    rows = extract_case(make_case(text))["observations"]
    assert len(rows) == 1
    assert rows[0]["text"] == text
    assert rows[0]["status"] == "invalid"
    assert rows[0]["reason"] == "invalid_calendar_date"
    assert rows[0]["normalized"] is None


@pytest.mark.parametrize("text", ["24:00", "25:10", "12:60", "12:01:60"])
def test_invalid_clocks_do_not_roll_over(text: str) -> None:
    rows = extract_case(make_case(text))["observations"]
    assert len(rows) == 1
    assert rows[0]["status"] == "invalid"
    assert rows[0]["reason"] == "invalid_clock_time"


def test_unknown_date_order_is_not_host_locale() -> None:
    row = extract_case(make_case("03/04/2024"))["observations"][0]
    assert row["status"] == "ambiguous"
    assert row["normalized"] == {
        "year": 2024,
        "month": None,
        "day": None,
        "iso": None,
        "alternatives": ["2024-03-04", "2024-04-03"],
    }
    assert extract_case(make_case("03/04/2024", order="DMY"))["observations"][0]["normalized"] == {
        "year": 2024,
        "month": 4,
        "day": 3,
        "iso": "2024-04-03",
        "alternatives": [],
    }


def test_missing_year_stays_unknown() -> None:
    row = extract_case(make_case("14 March"))["observations"][0]
    assert row["status"] == "partial"
    assert row["reason"] == "missing_year"
    assert row["normalized"] == {
        "year": None,
        "month": 3,
        "day": 14,
        "iso": None,
        "alternatives": [],
    }


def test_ranges_are_not_scalar_substrings() -> None:
    rows = extract_case(make_case("09:00\u201310:30; dose was 1\u20132 mg"))["observations"]
    assert [row["kind"] for row in rows] == ["time_range", "quantity_range"]
    assert rows[1]["normalized"] == {"lower": "1", "upper": "2", "unit": "mg"}
    reverse = extract_case(make_case("23:00\u201300:30"))["observations"][0]
    assert reverse["status"] == "ambiguous"
    assert reverse["reason"] == "range_requires_date"


def test_negation_and_attribution_stop_at_clause_boundaries() -> None:
    rows = extract_case(make_case("Patient did not receive 4 mg; child received 9.25 mg"))[
        "observations"
    ]
    assert [row["polarity"] for row in rows] == ["negated", "affirmed"]
    assert [row["subject"] for row in rows] == ["patient", "child"]
    rows = extract_case(make_case("Nurse reports child received 1.5 mg. Mother received 2 mg"))[
        "observations"
    ]
    assert [(row["subject"], row["reporter"]) for row in rows] == [
        ("child", "nurse"),
        ("mother", None),
    ]


def test_only_explicitly_selected_anchor_resolves_relative_time() -> None:
    case = anchored_case("Anchor 2024-03-01 00:30. 2 hours earlier", "2024-03-01 00:30")
    result = extract_case(case)
    relative = result["observations"][-1]
    assert relative["normalized"] == {
        "offset_seconds": -7200,
        "local_datetime": "2024-02-29T22:30:00",
    }
    assert relative["anchor"] is not None
    assert all(row["anchor"] is None for row in result["observations"][:-1])
    del case["anchors"]
    relative = extract_case(case)["observations"][-1]
    assert relative["status"] == "partial"
    assert relative["reason"] == "missing_explicit_anchor"
    assert relative["normalized"] == {"offset_seconds": -7200, "local_datetime": None}


def test_iso_t_anchor_retains_atomic_date_and_clock_mentions() -> None:
    case = anchored_case("2024-04-14T23:30; 2 hours later", "2024-04-14T23:30")
    rows = extract_case(case)["observations"]
    assert [row["kind"] for row in rows] == ["date", "time", "relative_time"]
    assert rows[-1]["normalized"] == {
        "offset_seconds": 7200,
        "local_datetime": "2024-04-15T01:30:00",
    }


def test_later_direct_subject_does_not_inherit_earlier_reporter() -> None:
    rows = extract_case(make_case("Mother reports patient received 5 mg and father received 2 mg"))[
        "observations"
    ]
    assert [(row["subject"], row["reporter"]) for row in rows] == [
        ("patient", "mother"),
        ("father", None),
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Patient received 5 mg and mother developed fever",
        "Mother reports child has fever and father complained of pain",
    ],
)
def test_later_unsupported_actor_relation_clears_stale_attribution(text: str) -> None:
    row = extract_case(make_case(text))["observations"][-1]
    assert row["subject"] is None
    assert row["reporter"] is None


def test_conditional_after_mention_does_not_become_affirmed() -> None:
    row = extract_case(make_case("Patient has fever if the condition recurs"))["observations"][0]
    assert row["status"] == "resolved"
    assert row["polarity"] == "uncertain"
    assert row["context_reasons"] == ["unsupported_assertion_scope"]


@pytest.mark.parametrize(
    "text",
    [
        "Patient has pain-free periods",
        "Patient has fever-free periods",
        "Patient has pain medication",
    ],
)
def test_compound_assertion_is_not_an_affirmed_symptom(text: str) -> None:
    row = extract_case(make_case(text))["observations"][0]
    assert row["status"] == "resolved"
    assert row["polarity"] == "uncertain"
    assert row["context_reasons"] == ["unsupported_assertion_scope"]


@pytest.mark.parametrize(
    "text",
    ["2OOO-04-14", "OOOO-OO-OO", "2s24-04-14", "2024-0i-14", "0s:30", "0b:30", "0i:30", "0L:30"],
)
def test_ocr_candidates_never_crash_or_repair(text: str) -> None:
    rows = extract_case(make_case(text))["observations"]
    assert len(rows) == 1
    assert rows[0]["text"] == text
    assert rows[0]["status"] == "unsupported"
    assert rows[0]["reason"] == "ocr_corruption"
    assert rows[0]["normalized"] is None


@pytest.mark.parametrize("token", ["\u22125 mg", "\u20135 mg", "- 5 mg"])
def test_unsupported_sign_cannot_donate_a_positive_quantity(token: str) -> None:
    rows = extract_case(make_case(f"Patient received {token}"))["observations"]
    assert len(rows) == 1
    assert rows[0]["text"] == token
    assert rows[0]["status"] == "unsupported"
    assert rows[0]["reason"] == "unsupported_number_format"
    assert rows[0]["normalized"] is None


@pytest.mark.parametrize("token", ["2 mg / kg", "2 mg\u00b7kg", "2 mg/kg/day"])
def test_unsupported_unit_cannot_lose_its_denominator(token: str) -> None:
    rows = extract_case(make_case(f"Patient was given {token}"))["observations"]
    assert len(rows) == 1
    assert rows[0]["text"] == token
    assert rows[0]["status"] == "unsupported"
    assert rows[0]["reason"] == "unsupported_unit"
    assert rows[0]["normalized"] is None


def test_malformed_relative_number_cannot_donate_an_integer_suffix() -> None:
    token = "100,000 hours later"
    rows = extract_case(make_case(token))["observations"]
    assert len(rows) == 1
    assert rows[0]["text"] == token
    assert rows[0]["kind"] == "relative_time"
    assert rows[0]["status"] == "ambiguous"
    assert rows[0]["reason"] == "ambiguous_number_format"
    assert rows[0]["normalized"] is None


@pytest.mark.parametrize(
    "text",
    [
        "Patient never had pain",
        "Patient denies no pain",
        "Patient received 5 mg if needed",
        "Patient has fever, possibly",
        "never " * 10_000 + "had pain",
    ],
)
def test_unsupported_scope_never_collapses_to_affirmed_or_negated(text: str) -> None:
    row = extract_case(make_case(text))["observations"][-1]
    assert row["polarity"] == "uncertain"
    assert row["context_reasons"] == ["unsupported_assertion_scope"]


def test_no_observation_still_requires_source_admission() -> None:
    case = make_case("Administrative checklist completed")
    result = extract_case(case)
    assert result["observations"] == []
    assert result["observation_count"] == 0
    assert result["no_supported_observation"] is True
    assert verify_extraction(case, result)
    source(case)["fingerprint"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="source admission"):
        extract_case(case)


@pytest.mark.parametrize(
    ("key", "value"),
    [("version", True), ("case_id", "other-case"), ("state", "withdrawn"), ("state", "unknown")],
)
def test_source_boundary_failures(key: str, value: object) -> None:
    case = make_case("Dose was 1 mg")
    source(case)[key] = value
    with pytest.raises(ValueError):
        extract_case(case)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("permitted_view", "public"),
        ("date_order", "AUTO"),
        ("sources", []),
        ("anchors", [None] * 33),
    ],
)
def test_case_boundary_failures(key: str, value: object) -> None:
    case = make_case("Dose was 1 mg")
    case[key] = value
    with pytest.raises(ValueError):
        extract_case(case)


def test_overflow_never_silently_returns_a_prefix() -> None:
    with pytest.raises(ValueError, match="32 observations"):
        extract_case(make_case("Dose was 1 mg; " * 33))
    with pytest.raises(ValueError, match="65536"):
        extract_case(make_case("x" * 65_537))


def test_replay_rejects_tampering_and_unserializable_results() -> None:
    case = make_case("Patient received 1 mg")
    result = extract_case(case)
    tampered = copy.deepcopy(result)
    tampered["observations"][0]["polarity"] = "negated"
    assert not verify_extraction(case, tampered)
    assert not verify_extraction(case, {"invalid": object()})
    cyclic: JsonObject = {}
    cyclic["cycle"] = cyclic
    assert not verify_extraction(case, cyclic)
    assert not verify_extraction(case, {"invalid": "\ud800"})


@settings(max_examples=45, deadline=None)
@given(st.dates(min_value=date(2001, 1, 1), max_value=date(2099, 12, 31)))
def test_calendar_values_and_utf8_prefix_offsets(value: date) -> None:
    prefix = "🧪 Café e\u0301\r\n"
    text = prefix + value.isoformat()
    row = extract_case(make_case(text))["observations"][0]
    assert row["status"] == "resolved"
    assert row["start_byte"] == len(prefix.encode())
    assert row["end_byte"] == len(text.encode())
    normalized = row["normalized"]
    assert normalized is not None
    assert normalized["iso"] == value.isoformat()


def test_demo_subprocesses_are_canonical_and_reject_arguments() -> None:
    first = subprocess.run(
        [sys.executable, "-m", "tools.workbench", "d1-demo"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    second = subprocess.run(
        [sys.executable, "-m", "tools.faw08_d1_extraction"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    assert first.stdout == second.stdout
    assert first.stdout.endswith(b"\n")
    assert not first.stdout.endswith(b"\n\n")
    assert json.loads(first.stdout) == generate_receipt()
    invalid = subprocess.run(
        [sys.executable, "-m", "tools.faw08_d1_extraction", "--input", "private.json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    assert invalid.returncode != 0
    assert invalid.stdout == b""
