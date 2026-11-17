"""FAW10/D3 decision-cutoff contract: executable negative and metamorphic cases."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

import pytest

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw10_d3_decision_view import (
    assemble_decision_packet,
    generate_receipt,
    render_decision_packet,
    retrieve_decision_evidence,
    verify_decision_claim,
)
from tools.faw10_d3_decision_view import main as d3_main
from tools.json_shapes import JsonObject, is_array, require_object
from tools.workbench import main as workbench_main


def _source(case_id: str, sid: str, text: str, version: int = 1) -> JsonObject:
    return {
        "case_id": case_id,
        "id": sid,
        "version": version,
        "state": "present",
        "content": text,
        "fingerprint": "sha256:" + sha256(text.encode("utf-8")).hexdigest(),
    }


def _span(case_id: str, sid: str, text: str, quote: str, version: int = 1) -> JsonObject:
    start = text.index(quote)
    return {
        "case_id": case_id,
        "source_id": sid,
        "source_version": version,
        "source_sha256": "sha256:" + sha256(text.encode("utf-8")).hexdigest(),
        "coordinate_system": "utf8-byte",
        "start_byte": len(text[:start].encode("utf-8")),
        "end_byte": len(text[: start + len(quote)].encode("utf-8")),
        "text": quote,
    }


def _rows(value: object) -> list[JsonObject]:
    assert is_array(value)
    return [require_object(item, context="test row") for item in value]


def _append(row: JsonObject, key: str, value: JsonObject) -> None:
    contents = row[key]
    assert is_array(contents)
    contents.append(value)


def _reverse(row: JsonObject, key: str) -> None:
    contents = row[key]
    assert is_array(contents)
    contents.reverse()


def case_input() -> JsonObject:
    early = (
        "Mother raised concerns about pain.\n"
        "Event: 2026-11-17T08:00:00Z\n"
        "Recorded: 2026-11-17T08:20:00Z\n"
        "Available A: 2026-11-17T09:00:00Z\n"
        "Available B: 2026-11-17T11:00:00Z\n"
        "Early before result.\n"
        "Internal note intentionally not included."
    )
    late = (
        "Later test result confirms an adverse outcome.\n"
        "Event: 2026-11-17T08:30:00Z\n"
        "Recorded: 2026-11-17T12:00:00Z\n"
        "Available A: 2026-11-17T12:30:00Z"
    )
    case_id = "synthetic-decision-case"

    def ev(eid: str, sid: str, text: str, quote: str) -> JsonObject:
        return {"id": eid, "evidence": _span(case_id, sid, text, quote)}

    def clock(
        cid: str,
        eid: str,
        kind: str,
        recipient: str | None,
        sid: str,
        text: str,
        quote: str,
    ) -> JsonObject:
        return {
            "id": cid,
            "event_id": eid,
            "kind": kind,
            "recipient_id": recipient,
            "evidence": _span(case_id, sid, text, quote),
        }

    return {
        "permitted_view": "synthetic-d3-decision-only",
        "recipient_id": "rn-a",
        "cutoff_utc": "2026-11-17T10:00:00Z",
        "timeline": {
            "case_id": case_id,
            "permitted_view": "synthetic-d2-timeline-only",
            "sources": [_source(case_id, "a", early), _source(case_id, "b", late)],
            "recipients": ["rn-a", "rn-b"],
            "events": [
                ev("early", "a", early, "Mother raised concerns about pain."),
                ev("late", "b", late, "Later test result confirms an adverse outcome."),
            ],
            "clocks": [
                clock("early-time", "early", "event", None, "a", early, "2026-11-17T08:00:00Z"),
                clock(
                    "early-record", "early", "recording", None, "a", early, "2026-11-17T08:20:00Z"
                ),
                clock(
                    "early-a", "early", "availability", "rn-a", "a", early, "2026-11-17T09:00:00Z"
                ),
                clock(
                    "early-b", "early", "availability", "rn-b", "a", early, "2026-11-17T11:00:00Z"
                ),
                clock("late-time", "late", "event", None, "b", late, "2026-11-17T08:30:00Z"),
                clock("late-record", "late", "recording", None, "b", late, "2026-11-17T12:00:00Z"),
                clock("late-a", "late", "availability", "rn-a", "b", late, "2026-11-17T12:30:00Z"),
            ],
            "relations": [
                {
                    "id": "early-before-late",
                    "before_event_id": "early",
                    "after_event_id": "late",
                    "evidence": _span(case_id, "a", early, "Early before result."),
                }
            ],
            "amendments": [],
        },
        "entitlements": [
            {
                "source_id": "a",
                "source_version": 1,
                "recipient_id": "rn-a",
                "first_available_utc": "2026-11-17T09:00:00Z",
            },
            {
                "source_id": "a",
                "source_version": 1,
                "recipient_id": "rn-b",
                "first_available_utc": "2026-11-17T09:00:00Z",
            },
            {
                "source_id": "b",
                "source_version": 1,
                "recipient_id": "rn-a",
                "first_available_utc": "2026-11-17T12:30:00Z",
            },
            {
                "source_id": "b",
                "source_version": 1,
                "recipient_id": "rn-b",
                "first_available_utc": None,
            },
        ],
        "labels": [
            {"event_id": "early", "kind": "patient_family_concern", "speaker_role": "family"},
            {"event_id": "late", "kind": "outcome", "speaker_role": None},
        ],
    }


def test_future_result_hidden_across_all_surfaces() -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    assert [item["event_id"] for item in packet["events"]] == ["early"]
    assert packet["family_concern_status"] == "documented_at_cutoff"
    assert packet["family_concern_event_ids"] == ["early"]
    assert packet["partial_order"]["pairs"] == []
    for output in (str(packet), render_decision_packet(raw, packet)):
        assert "Later test result" not in output
        assert "adverse outcome" not in output
        assert "early-before-late" not in output
        assert "Internal note intentionally not included" not in output
    assert retrieve_decision_evidence(raw, packet, "adverse") == []
    assert [item["event_id"] for item in retrieve_decision_evidence(raw, packet, "Mother")] == [
        "early"
    ]
    assert verify_decision_claim(raw, packet, "early", "Mother raised concerns about pain.")
    assert not verify_decision_claim(
        raw, packet, "late", "Later test result confirms an adverse outcome."
    )


def test_later_cutoff_reveals_only_then_entitled_result() -> None:
    raw = case_input()
    raw["cutoff_utc"] = "2026-11-17T13:00:00Z"
    packet = assemble_decision_packet(raw)
    assert [item["event_id"] for item in packet["events"]] == ["early", "late"]
    assert packet["partial_order"]["pairs"][0]["order"] == "before"
    assert verify_decision_claim(
        raw, packet, "late", "Later test result confirms an adverse outcome."
    )


def test_actor_specific_availability_does_not_inherit_others_knowledge() -> None:
    raw = case_input()
    raw["recipient_id"] = "rn-b"
    assert assemble_decision_packet(raw)["events"] == []
    raw["cutoff_utc"] = "2026-11-17T12:00:00Z"
    assert [item["event_id"] for item in assemble_decision_packet(raw)["events"]] == ["early"]


def test_missing_availability_is_not_inferred_from_record_or_source() -> None:
    raw = case_input()
    timeline = require_object(raw["timeline"], context="timeline")
    timeline["clocks"] = [item for item in _rows(timeline["clocks"]) if item["id"] != "early-a"]
    packet = assemble_decision_packet(raw)
    assert packet["events"] == []
    assert packet["family_concern_status"] == "not_documented_at_cutoff"


def test_unknown_source_availability_is_not_inferred() -> None:
    raw = case_input()
    for entitlement in _rows(raw["entitlements"]):
        if entitlement["source_id"] == "a" and entitlement["recipient_id"] == "rn-a":
            entitlement["first_available_utc"] = None
    assert assemble_decision_packet(raw)["events"] == []


def test_future_recording_blocks_entitlement_even_if_event_time_is_early() -> None:
    raw = case_input()
    timeline = require_object(raw["timeline"], context="timeline")
    clocks = _rows(timeline["clocks"])
    early_source = require_object(_rows(timeline["sources"])[0], context="source")
    text = early_source["content"]
    assert isinstance(text, str)
    clocks.append(
        {
            "id": "conflicting-later-record",
            "event_id": "early",
            "kind": "recording",
            "recipient_id": None,
            "evidence": _span("synthetic-decision-case", "a", text, "2026-11-17T11:00:00Z"),
        }
    )
    timeline["clocks"] = clocks
    assert assemble_decision_packet(raw)["events"] == []


def test_future_outcome_mutation_does_not_change_earlier_packet() -> None:
    raw = case_input()
    baseline = canonical_bytes(assemble_decision_packet(raw))
    timeline = require_object(raw["timeline"], context="timeline")
    source_b = _rows(timeline["sources"])[1]
    original = source_b["content"]
    assert isinstance(original, str)
    revised = original.replace("an adverse outcome", "an unexpected outcome")
    source_b["content"] = revised
    source_b["fingerprint"] = "sha256:" + sha256(revised.encode("utf-8")).hexdigest()
    for event in _rows(timeline["events"]):
        if event["id"] == "late":
            event["evidence"] = _span(
                "synthetic-decision-case",
                "b",
                revised,
                "Later test result confirms an unexpected outcome.",
            )
    for clock in _rows(timeline["clocks"]):
        if clock["event_id"] == "late":
            evidence = require_object(clock["evidence"], context="clock evidence")
            quote = evidence["text"]
            assert isinstance(quote, str)
            clock["evidence"] = _span("synthetic-decision-case", "b", revised, quote)
    assert canonical_bytes(assemble_decision_packet(raw)) == baseline


def test_future_source_amendment_does_not_rewrite_prior_knowledge() -> None:
    raw = case_input()
    baseline = canonical_bytes(assemble_decision_packet(raw))
    timeline = require_object(raw["timeline"], context="timeline")
    correction = "Corrected availability: 2026-11-17T13:00:00Z"
    _append(timeline, "sources", _source("synthetic-decision-case", "a", correction, 2))
    _append(
        timeline,
        "clocks",
        {
            "id": "early-a-corrected",
            "event_id": "early",
            "kind": "availability",
            "recipient_id": "rn-a",
            "evidence": _span(
                "synthetic-decision-case", "a", correction, "2026-11-17T13:00:00Z", 2
            ),
        },
    )
    _append(
        timeline,
        "amendments",
        {
            "id": "new-version-amendment",
            "earlier_clock_id": "early-a",
            "later_clock_id": "early-a-corrected",
            "evidence": _span(
                "synthetic-decision-case", "a", correction, "Corrected availability", 2
            ),
        },
    )
    _append(
        raw,
        "entitlements",
        {
            "source_id": "a",
            "source_version": 2,
            "recipient_id": "rn-a",
            "first_available_utc": "2026-11-17T13:00:00Z",
        },
    )
    assert canonical_bytes(assemble_decision_packet(raw)) == baseline


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("cutoff_utc", "2026-11-17T10:00"),
        ("cutoff_utc", "2026-11-17T10:00:00+10:00"),
        ("cutoff_utc", "2026-02-30T10:00:00Z"),
        ("recipient_id", "unknown-recipient"),
        ("permitted_view", "public"),
        ("entitlements", "not-an-array"),
        ("labels", "not-an-array"),
    ],
)
def test_fail_closed_top_level(field: str, bad_value: object) -> None:
    raw = case_input()
    raw[field] = bad_value
    with pytest.raises(ValueError):
        assemble_decision_packet(raw)


def test_reject_forged_provenance_and_invalid_entitlement_reference() -> None:
    raw = case_input()
    timeline = require_object(raw["timeline"], context="timeline")
    _rows(timeline["sources"])[0]["fingerprint"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError):
        assemble_decision_packet(raw)
    raw = case_input()
    _rows(raw["entitlements"])[0]["source_id"] = "does-not-exist"
    with pytest.raises(ValueError):
        assemble_decision_packet(raw)


def test_reject_duplicate_entitlements_and_invalid_label_semantics() -> None:
    raw = case_input()
    _append(raw, "entitlements", deepcopy(_rows(raw["entitlements"])[0]))
    with pytest.raises(ValueError):
        assemble_decision_packet(raw)
    raw = case_input()
    _rows(raw["labels"])[0]["speaker_role"] = "other"
    with pytest.raises(ValueError):
        assemble_decision_packet(raw)


def test_packet_is_replayed_before_retrieval_verification_or_render() -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    forged = deepcopy(packet)
    forged["recipient_id"] = "rn-b"
    with pytest.raises(ValueError):
        retrieve_decision_evidence(raw, forged, "Mother")
    with pytest.raises(ValueError):
        verify_decision_claim(raw, forged, "early", "Mother raised concerns about pain.")
    with pytest.raises(ValueError):
        render_decision_packet(raw, forged)


def test_unqualified_claim_is_never_semantically_promoted() -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    assert packet["linkage_basis"] == "caller-declared-synthetic-entitlements"
    assert not verify_decision_claim(raw, packet, "early", "The mother was correct.")
    assert not verify_decision_claim(raw, packet, "late", "The event caused harm.")


def test_order_and_irrelevant_future_labels_do_not_affect_prior_packet() -> None:
    raw = case_input()
    baseline = canonical_bytes(assemble_decision_packet(raw))
    _reverse(raw, "entitlements")
    _reverse(raw, "labels")
    timeline = require_object(raw["timeline"], context="timeline")
    _reverse(timeline, "sources")
    _reverse(timeline, "events")
    _reverse(timeline, "clocks")
    assert canonical_bytes(assemble_decision_packet(raw)) == baseline


def test_downstream_failure_does_not_echo_future_source_identifiers() -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    timeline = require_object(raw["timeline"], context="timeline")
    _rows(timeline["sources"])[1]["fingerprint"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match=r"^invalid or unbound decision packet$"):
        retrieve_decision_evidence(raw, packet, "Mother")
    with pytest.raises(ValueError, match=r"^invalid or unbound decision packet$"):
        verify_decision_claim(raw, packet, "early", "Mother raised concerns about pain.")
    with pytest.raises(ValueError, match=r"^invalid or unbound decision packet$"):
        render_decision_packet(raw, packet)


def test_future_label_change_is_noninterfering_at_earlier_cutoff() -> None:
    raw = case_input()
    baseline = canonical_bytes(assemble_decision_packet(raw))
    labels = _rows(raw["labels"])
    assert labels[1]["event_id"] == "late"
    labels[1]["kind"] = "appraisal"
    assert canonical_bytes(assemble_decision_packet(raw)) == baseline


def test_future_only_cycle_does_not_affect_past_packet() -> None:
    raw = case_input()
    baseline = canonical_bytes(assemble_decision_packet(raw))
    timeline = require_object(raw["timeline"], context="timeline")
    source = _rows(timeline["sources"])[1]
    original = source["content"]
    assert isinstance(original, str)
    revised = original + "\nLate before early."
    source["content"] = revised
    source["fingerprint"] = "sha256:" + sha256(revised.encode("utf-8")).hexdigest()
    for category in ("events", "clocks"):
        for row in _rows(timeline[category]):
            evidence = require_object(row["evidence"], context="evidence")
            if evidence["source_id"] == "b":
                quote = evidence["text"]
                assert isinstance(quote, str)
                row["evidence"] = _span("synthetic-decision-case", "b", revised, quote)
    _append(
        timeline,
        "relations",
        {
            "id": "late-before-early",
            "before_event_id": "late",
            "after_event_id": "early",
            "evidence": _span("synthetic-decision-case", "b", revised, "Late before early."),
        },
    )
    assert canonical_bytes(assemble_decision_packet(raw)) == baseline
    raw["cutoff_utc"] = "2026-11-17T13:00:00Z"
    packet = assemble_decision_packet(raw)
    assert packet["partial_order"]["consistency"]["status"] == "inconsistent"
    assert packet["partial_order"]["display_order"] is None


def test_unentitled_invalid_relation_does_not_leak_future_identity_in_errors() -> None:
    raw = case_input()
    timeline = require_object(raw["timeline"], context="timeline")
    source = _rows(timeline["sources"])[1]
    content = source["content"]
    assert isinstance(content, str)
    _append(
        timeline,
        "relations",
        {
            "id": "postcutoff-relation",
            "before_event_id": "late",
            "after_event_id": "CONFIDENTIAL_FUTURE_OUTCOME",
            "evidence": _span("synthetic-decision-case", "b", content, "Later test result"),
        },
    )
    with pytest.raises(
        ValueError, match=r"^invalid or inadmissible decision packet input$"
    ) as error:
        assemble_decision_packet(raw)
    assert "CONFIDENTIAL_FUTURE_OUTCOME" not in str(error.value)


def test_synthetic_receipt_is_deterministic_and_replay_bound() -> None:
    """Exercise the actual D3 generator, not a placeholder source fixture."""
    receipt = generate_receipt()
    assert canonical_bytes(receipt) == canonical_bytes(generate_receipt())
    assert receipt["dataset"] == "generated-synthetic-only"
    assert receipt["case_count"] == 3
    assert receipt["visible_counts"] == [1, 2, 0]
    assert receipt["output_fingerprint"] == fingerprint(
        {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    )
    inputs = receipt["inputs"]
    cases = receipt["cases"]
    assert is_array(inputs)
    assert is_array(cases)
    for raw, packet in zip(inputs, cases, strict=True):
        assert canonical_bytes(assemble_decision_packet(raw)) == canonical_bytes(packet)
        assert render_decision_packet(raw, packet) == canonical_bytes(packet).decode("utf-8")
    assert "Later test result" not in render_decision_packet(inputs[0], cases[0])
    assert require_object(cases[2], context="synthetic empty D3 packet")["events"] == []


@pytest.mark.parametrize("entrypoint", ["module", "workbench"])
def test_binary_d3_entrypoints_emit_identical_provenance(
    entrypoint: str, capfdbinary: pytest.CaptureFixture[bytes]
) -> None:
    """Exercise both published CLI entrypoints and canonical-byte boundary."""
    status = d3_main([]) if entrypoint == "module" else workbench_main(["d3-demo"])
    assert status == 0
    captured = capfdbinary.readouterr()
    assert captured.out == canonical_bytes(generate_receipt()) + b"\n"
    assert captured.err == b""


@pytest.mark.parametrize(
    ("kind", "speaker", "has_concern"),
    [
        ("observation", None, False),
        ("outcome", None, False),
        ("appraisal", None, False),
        ("patient_family_concern", "patient", True),
    ],
)
def test_visible_supported_event_kinds_and_concern_speakers(
    kind: str, speaker: str | None, has_concern: bool
) -> None:
    """Each synthetic kind has an explicit speaker and decision-time disposition."""
    raw = case_input()
    first = _rows(raw["labels"])[0]
    first["kind"] = kind
    first["speaker_role"] = speaker
    packet = assemble_decision_packet(raw)
    assert packet["event_count"] == 1
    assert packet["events"][0]["kind"] == kind
    assert packet["events"][0]["speaker_role"] == speaker
    assert (packet["family_concern_status"] == "documented_at_cutoff") == has_concern


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("recipient_id", ""),
        ("recipient_id", "a" * 129),
        ("recipient_id", 42),
        ("cutoff_utc", "2026-11-17T10:00:60Z"),
        ("cutoff_utc", "2026-11-17T10:00:00"),
        ("cutoff_utc", "2026-11-17T10:00:00z"),
        ("cutoff_utc", True),
    ],
)
def test_public_input_rejects_invalid_identifiers_and_utc_seconds(
    field: str, invalid: object
) -> None:
    raw = case_input()
    raw[field] = invalid
    with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
        assemble_decision_packet(raw)


def test_public_input_rejects_non_utf8_surrogate_without_echoing_it() -> None:
    raw = case_input()
    raw["recipient_id"] = "private-" + chr(0xD800)
    with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
        assemble_decision_packet(raw)


@pytest.mark.parametrize(
    ("kind", "speaker"),
    [
        ("unsupported", None),
        ("observation", "family"),
        ("outcome", "patient"),
        ("patient_family_concern", None),
        ("patient_family_concern", "staff"),
    ],
)
def test_metadata_kind_and_speaker_validation_is_fail_closed(
    kind: str, speaker: str | None
) -> None:
    raw = case_input()
    label = _rows(raw["labels"])[0]
    label["kind"] = kind
    label["speaker_role"] = speaker
    with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
        assemble_decision_packet(raw)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("source_version", 0),
        ("source_version", True),
        ("recipient_id", "recipient-outside-case"),
        ("first_available_utc", "2026-11-17T09:00:00+00:00"),
        ("first_available_utc", "2026-02-30T09:00:00Z"),
        ("source_id", "unadmitted-source"),
    ],
)
def test_entitlement_row_requires_admitted_version_actor_and_explicit_clock(
    field: str, invalid: object
) -> None:
    raw = case_input()
    entitlement = _rows(raw["entitlements"])[0]
    entitlement[field] = invalid
    with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
        assemble_decision_packet(raw)


def test_event_labels_require_complete_unique_admitted_identifiers() -> None:
    for mutation in ("missing", "duplicate", "unknown"):
        raw = case_input()
        labels = _rows(raw["labels"])
        if mutation == "missing":
            labels.pop()
        elif mutation == "duplicate":
            labels[1]["event_id"] = "early"
        else:
            labels[1]["event_id"] = "not-an-admitted-event"
        with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
            assemble_decision_packet(raw)


@pytest.mark.parametrize("field", ["entitlements", "labels"])
def test_metadata_array_caps_are_enforced_before_mapping(field: str) -> None:
    raw = case_input()
    rows = _rows(raw[field])
    maximum = 512 if field == "entitlements" else 16
    raw[field] = [deepcopy(rows[0]) for _ in range(maximum + 1)]
    with pytest.raises(ValueError, match=r"^invalid or inadmissible decision packet input$"):
        assemble_decision_packet(raw)


def test_missing_occurrence_time_blocks_outcome_but_not_observation() -> None:
    raw = case_input()
    timeline = require_object(raw["timeline"], context="timeline")
    timeline["clocks"] = [row for row in _rows(timeline["clocks"]) if row["id"] != "early-time"]
    _rows(raw["labels"])[0]["kind"] = "outcome"
    _rows(raw["labels"])[0]["speaker_role"] = None
    assert assemble_decision_packet(raw)["events"] == []
    _rows(raw["labels"])[0]["kind"] = "observation"
    assert [item["event_id"] for item in assemble_decision_packet(raw)["events"]] == ["early"]


@pytest.mark.parametrize("query", ["", "q" * 129, 100])
def test_retrieval_rejects_invalid_queries_after_packet_replay(query: object) -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    with pytest.raises(ValueError):
        retrieve_decision_evidence(raw, packet, query)


def test_replay_rejects_malformed_packet_and_preserves_empty_actor_view() -> None:
    raw = case_input()
    packet = assemble_decision_packet(raw)
    with pytest.raises(ValueError, match=r"^invalid or unbound decision packet$"):
        render_decision_packet(raw, {"events": packet["events"]})
    raw["recipient_id"] = "rn-b"
    raw["cutoff_utc"] = "2026-11-17T08:00:00Z"
    empty = assemble_decision_packet(raw)
    assert empty["events"] == []
    assert empty["partial_order"]["display_order"] == []
    assert render_decision_packet(raw, empty) == canonical_bytes(empty).decode("utf-8")
