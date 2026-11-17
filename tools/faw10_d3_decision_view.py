"""Recipient- and cutoff-scoped synthetic decision packets over D0/D2 evidence.

Entitlement timestamps, event labels and linkage are *caller-declared synthetic
annotations*. They do not prove receipt, comprehension, clinical truth, legal
authority or semantic entailment. This module intentionally has no unscoped
retrieval, verification or rendering entrypoint.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw07_d0_demo import SpanObservation
from tools.faw09_d2_timeline import (
    ClockSummary,
    Consistency,
    Edge,
    Pair,
    TimelineEvent,
    assemble_timeline,
)
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
VIEW = "synthetic-d3-decision-only"
RULE_VERSION = "faw10-d3-rules-1.0"
LINKAGE = "caller-declared-synthetic-entitlements"
IMPLEMENTATION_FILES = (
    "tools/faw10_d3_decision_view.py",
    "tools/faw09_d2_timeline.py",
    "tools/faw09_d2_clock.py",
    "tools/faw07_d0_demo.py",
    "tools/evidence_core.py",
    "tools/json_shapes.py",
    "tools/workbench.py",
)
EvidenceKind = Literal["observation", "outcome", "appraisal", "patient_family_concern"]
Speaker = Literal["patient", "family"]


class DecisionEvent(TypedDict):
    event_id: str
    binding_id: str
    kind: EvidenceKind
    speaker_role: Speaker | None
    evidence: SpanObservation
    event_time: ClockSummary
    recording_time: ClockSummary
    availability: ClockSummary


class PartialOrder(TypedDict):
    edges: list[Edge]
    pairs: list[Pair]
    consistency: Consistency
    display_order: list[str] | None
    display_order_is_temporal_evidence: Literal[False]


class D3Packet(TypedDict):
    schema_version: Literal["faw10-d3-packet-1.0"]
    case_id: str
    permitted_view: Literal["synthetic-d3-decision-only"]
    recipient_id: str
    cutoff_utc: str
    rule_version: str
    linkage_basis: str
    source_entitlement_basis: Literal["caller-declared-not-delivery-proof"]
    event_labels_basis: Literal["caller-declared-not-semantic-verification"]
    events: list[DecisionEvent]
    event_count: int
    family_concern_status: Literal["documented_at_cutoff", "not_documented_at_cutoff"]
    family_concern_event_ids: list[str]
    partial_order: PartialOrder
    view_fingerprint: str


_PACKET_KEYS = {
    "permitted_view",
    "recipient_id",
    "cutoff_utc",
    "timeline",
    "entitlements",
    "labels",
}
_TIMELINE_KEYS = {
    "case_id",
    "permitted_view",
    "sources",
    "recipients",
    "events",
    "clocks",
    "relations",
    "amendments",
}
_ENTITLEMENT_KEYS = {
    "source_id",
    "source_version",
    "recipient_id",
    "first_available_utc",
}
_LABEL_KEYS = {"event_id", "kind", "speaker_role"}
_UTC_SECONDS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def _object(value: object, fields: set[str], label: str) -> JsonObject:
    row = require_object(value, context=label)
    if set(row) != fields:
        raise ValueError(f"{label} requires exactly {sorted(fields)}")
    return row


def _text(value: object, label: str, *, limit: int = 128) -> str:
    if not isinstance(value, str) or type(value) is not str or not value:
        raise ValueError(f"{label} must be nonempty text")
    if len(value) > limit:
        raise ValueError(f"{label} exceeds {limit} characters")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{label} is not UTF-8") from exc
    return value


def _version(value: object) -> int:
    if type(value) is not int or value < 1:
        raise ValueError("source version must be a positive integer")
    return value


def _utc(value: object) -> str:
    text = _text(value, "UTC second", limit=20)
    if not _UTC_SECONDS.fullmatch(text):
        raise ValueError("UTC second must have explicit YYYY-MM-DDTHH:MM:SSZ form")
    try:
        datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("UTC second is not a valid calendar instant") from exc
    return text


def _rows(value: object, label: str, limit: int) -> list[JsonObject]:
    if not is_array(value) or len(value) > limit:
        raise ValueError(f"{label} must be an array of at most {limit} entries")
    return [require_object(item, context=label) for item in value]


def _source_key(source: JsonObject) -> tuple[str, int]:
    return (_text(source["id"], "source id"), _version(source["version"]))


def _evidence_key(row: JsonObject) -> tuple[str, int]:
    evidence = require_object(row["evidence"], context="D3 evidence")
    return (_text(evidence["source_id"], "source id"), _version(evidence["source_version"]))


def _kind(value: object) -> EvidenceKind:
    text = _text(value, "event kind")
    if text == "observation":
        return "observation"
    if text == "outcome":
        return "outcome"
    if text == "appraisal":
        return "appraisal"
    if text == "patient_family_concern":
        return "patient_family_concern"
    raise ValueError("unsupported event kind")


def _labels(value: object, event_ids: set[str]) -> dict[str, tuple[EvidenceKind, Speaker | None]]:
    rows = _rows(value, "labels", 16)
    labels: dict[str, tuple[EvidenceKind, Speaker | None]] = {}
    for value_row in rows:
        row = _object(value_row, _LABEL_KEYS, "event label")
        event_id = _text(row["event_id"], "label event")
        if event_id not in event_ids or event_id in labels:
            raise ValueError("unknown or duplicate event label")
        kind = _kind(row["kind"])
        voice = row["speaker_role"]
        if kind == "patient_family_concern":
            if voice != "patient" and voice != "family":
                raise ValueError("patient/family concern must have a patient or family speaker")
            speaker: Speaker = "patient" if voice == "patient" else "family"
            labels[event_id] = (kind, speaker)
        else:
            if voice is not None:
                raise ValueError("non-concern labels require null speaker_role")
            labels[event_id] = (kind, None)
    if set(labels) != event_ids:
        raise ValueError("every D2 event needs an explicit D3 label")
    return labels


def _entitlements(
    value: object,
    known_sources: set[tuple[str, int]],
    recipients: set[str],
) -> dict[tuple[str, int, str], str | None]:
    rows = _rows(value, "entitlements", 512)
    result: dict[tuple[str, int, str], str | None] = {}
    for value_row in rows:
        row = _object(value_row, _ENTITLEMENT_KEYS, "source entitlement")
        key = (
            _text(row["source_id"], "source id"),
            _version(row["source_version"]),
            _text(row["recipient_id"], "entitlement recipient"),
        )
        if key[:2] not in known_sources or key[2] not in recipients or key in result:
            raise ValueError("unknown or duplicate source-version entitlement")
        available = row["first_available_utc"]
        result[key] = _utc(available) if available is not None else None
    return result


def _subset(
    original: JsonObject,
    allowed_sources: set[tuple[str, int]],
    recipient: str,
    accepted_events: set[str] | None = None,
) -> JsonObject:
    sources = [
        source
        for source in _rows(original["sources"], "D2 sources", 32)
        if _source_key(source) in allowed_sources
    ]
    events = [
        event
        for event in _rows(original["events"], "D2 events", 16)
        if _evidence_key(event) in allowed_sources
        and (accepted_events is None or _text(event["id"], "event id") in accepted_events)
    ]
    event_ids = {_text(event["id"], "event id") for event in events}
    clocks = [
        clock
        for clock in _rows(original["clocks"], "D2 clocks", 32)
        if _text(clock["event_id"], "clock event") in event_ids
        and _evidence_key(clock) in allowed_sources
        and (
            clock["kind"] != "availability"
            or clock["recipient_id"] == recipient
        )
    ]
    clock_ids = {_text(clock["id"], "clock id") for clock in clocks}
    relations = [
        relation
        for relation in _rows(original["relations"], "D2 relations", 32)
        if _text(relation["before_event_id"], "relation before") in event_ids
        and _text(relation["after_event_id"], "relation after") in event_ids
        and _evidence_key(relation) in allowed_sources
    ]
    amendments = [
        amendment
        for amendment in _rows(original["amendments"], "D2 amendments", 16)
        if _text(amendment["earlier_clock_id"], "amendment earlier") in clock_ids
        and _text(amendment["later_clock_id"], "amendment later") in clock_ids
        and _evidence_key(amendment) in allowed_sources
    ]
    return {
        "case_id": original["case_id"],
        "permitted_view": original["permitted_view"],
        "sources": sources,
        "recipients": [recipient],
        "events": events,
        "clocks": clocks,
        "relations": relations,
        "amendments": amendments,
    }


def _known_before(clock: ClockSummary, cutoff: str) -> bool:
    windows = clock["windows"]
    return (
        clock["status"] in ("known", "ambiguous", "conflicting")
        and windows is not None
        and bool(windows)
        and all(window["end"] <= cutoff for window in windows)
    )


def _eligible(
    event: TimelineEvent,
    recipient: str,
    cutoff: str,
    kind: EvidenceKind,
) -> bool:
    availability = [
        item["clock"]
        for item in event["availability"]
        if item["recipient_id"] == recipient
    ]
    if len(availability) != 1 or not _known_before(availability[0], cutoff):
        return False
    recording = event["recording_time"]
    if recording["active_assertion_ids"] and not _known_before(recording, cutoff):
        return False
    occurrence = event["event_time"]
    if occurrence["windows"] is not None and not _known_before(occurrence, cutoff):
        return False
    # An outcome or retrospective appraisal with an unknown occurrence time
    # cannot be declared contemporaneous by its availability alone.
    return kind not in ("outcome", "appraisal") or _known_before(occurrence, cutoff)


def assemble_decision_packet(case: object) -> D3Packet:
    """Build an actor/cutoff view; never return the unscoped D2 input or output."""
    record = _object(case, _PACKET_KEYS, "D3 case")
    if _text(record["permitted_view"], "view") != VIEW:
        raise ValueError("D3 requires the synthetic decision-time view")
    recipient = _text(record["recipient_id"], "recipient")
    cutoff = _utc(record["cutoff_utc"])
    timeline = _object(record["timeline"], _TIMELINE_KEYS, "D2 timeline input")

    # Full D2 admission checks every source byte, referenced span and endpoint,
    # but no full case observation escapes this function.
    admitted = assemble_timeline(timeline)
    if recipient not in admitted["recipients"]:
        raise ValueError("D3 recipient is not in the D2 case")
    known_sources = {(row["source_id"], row["version"]) for row in admitted["sources"]}
    ledger = _entitlements(record["entitlements"], known_sources, set(admitted["recipients"]))
    labels = _labels(record["labels"], {event["id"] for event in admitted["events"]})
    permitted_sources = {
        (sid, version)
        for (sid, version, actor), available in ledger.items()
        if actor == recipient and available is not None and available <= cutoff
    }

    # Project the revision ledger first. A later source version, amendment or
    # source-bound assertion is not permitted to supersede earlier knowledge.
    candidate_input = _subset(timeline, permitted_sources, recipient)
    candidates = assemble_timeline(candidate_input)
    permitted_events = {
        event["id"]
        for event in candidates["events"]
        if _eligible(event, recipient, cutoff, labels[event["id"]][0])
    }

    # Reconstruct chronology *again* on entitled events alone. Excluded nodes,
    # their relations, other-recipient clocks and contradictory future accounts
    # cannot alter display ordering, pair checks or verification.
    visible_input = _subset(timeline, permitted_sources, recipient, permitted_events)
    visible = assemble_timeline(visible_input)
    events: list[DecisionEvent] = []
    for event in visible["events"]:
        speaker = labels[event["id"]]
        availability = [
            item["clock"]
            for item in event["availability"]
            if item["recipient_id"] == recipient
        ]
        if len(availability) != 1:
            raise ValueError("D3 recipient-specific availability missing")
        events.append(
            {
                "event_id": event["id"],
                "binding_id": event["binding_id"],
                "kind": speaker[0],
                "speaker_role": speaker[1],
                "evidence": event["evidence"],
                "event_time": event["event_time"],
                "recording_time": event["recording_time"],
                "availability": availability[0],
            }
        )
    family_ids = [
        event["event_id"] for event in events if event["kind"] == "patient_family_concern"
    ]
    packet: D3Packet = {
        "schema_version": "faw10-d3-packet-1.0",
        "case_id": admitted["case_id"],
        "permitted_view": VIEW,
        "recipient_id": recipient,
        "cutoff_utc": cutoff,
        "rule_version": RULE_VERSION,
        "linkage_basis": LINKAGE,
        "source_entitlement_basis": "caller-declared-not-delivery-proof",
        "event_labels_basis": "caller-declared-not-semantic-verification",
        "events": events,
        "event_count": len(events),
        "family_concern_status": (
            "documented_at_cutoff" if family_ids else "not_documented_at_cutoff"
        ),
        "family_concern_event_ids": family_ids,
        "partial_order": {
            "edges": visible["edges"],
            "pairs": visible["pairs"],
            "consistency": visible["consistency"],
            "display_order": visible["display_order"],
            "display_order_is_temporal_evidence": False,
        },
        "view_fingerprint": "",
    }
    packet["view_fingerprint"] = fingerprint(
        {key: value for key, value in packet.items() if key != "view_fingerprint"}
    )
    return packet


def _replayed(case: object, packet: object) -> D3Packet:
    """Refuse an unbound packet on every public downstream read path."""
    expected = assemble_decision_packet(case)
    try:
        if not isinstance(packet, dict) or canonical_bytes(packet) != canonical_bytes(expected):
            raise ValueError("decision packet not bound to case/actor/cutoff")
    except (TypeError, RecursionError, UnicodeError) as exc:
        raise ValueError("invalid decision packet") from exc
    return expected


def retrieve_decision_evidence(
    case: object, packet: object, query: object
) -> list[DecisionEvent]:
    """Substring retrieval over the replayed, already-scoped event set only."""
    expected = _replayed(case, packet)
    phrase = _text(query, "query")
    return [
        event
        for event in expected["events"]
        if phrase.casefold() in event["evidence"]["text"].casefold()
    ]


def verify_decision_claim(
    case: object, packet: object, event_id: object, statement: object
) -> bool:
    """Verify exact attributed text, not its clinical or causal truth."""
    expected = _replayed(case, packet)
    identity = _text(event_id, "event_id")
    phrase = _text(statement, "statement", limit=65_536)
    return any(
        event["event_id"] == identity and event["evidence"]["text"] == phrase
        for event in expected["events"]
    )


def render_decision_packet(case: object, packet: object) -> str:
    """Render only freshly replayed, recipient-specific packet bytes."""
    return canonical_bytes(_replayed(case, packet)).decode("utf-8")


def _demo_source(case_id: str, sid: str, content: str) -> JsonObject:
    return {
        "case_id": case_id,
        "id": sid,
        "version": 1,
        "state": "present",
        "content": content,
        "fingerprint": "sha256:" + sha256(content.encode("utf-8")).hexdigest(),
    }


def _demo_span(case_id: str, sid: str, content: str, quote: str) -> JsonObject:
    start = content.index(quote)
    return {
        "case_id": case_id,
        "source_id": sid,
        "source_version": 1,
        "source_sha256": "sha256:" + sha256(content.encode("utf-8")).hexdigest(),
        "coordinate_system": "utf8-byte",
        "start_byte": len(content[:start].encode("utf-8")),
        "end_byte": len(content[: start + len(quote)].encode("utf-8")),
        "text": quote,
    }


def _synthetic_input() -> JsonObject:
    """Input-only, labelled synthetic demonstration; no independent oracle."""
    case_id = "d3-synthetic"
    early = (
        "Family reported persistent concern.\n"
        "Event 2026-11-17T08:00:00Z.\n"
        "Available 2026-11-17T09:00:00Z."
    )
    late = (
        "Later test result changed the outcome.\n"
        "Event 2026-11-17T08:30:00Z.\n"
        "Recorded 2026-11-17T12:00:00Z.\n"
        "Available 2026-11-17T12:30:00Z."
    )

    def clock(cid: str, eid: str, kind: str, sid: str, text: str, quote: str) -> JsonObject:
        return {
            "id": cid,
            "event_id": eid,
            "kind": kind,
            "recipient_id": "rn-a" if kind == "availability" else None,
            "evidence": _demo_span(case_id, sid, text, quote),
        }

    return {
        "permitted_view": VIEW,
        "recipient_id": "rn-a",
        "cutoff_utc": "2026-11-17T10:00:00Z",
        "timeline": {
            "case_id": case_id,
            "permitted_view": "synthetic-d2-timeline-only",
            "sources": [_demo_source(case_id, "early", early), _demo_source(case_id, "late", late)],
            "recipients": ["rn-a", "rn-b"],
            "events": [
                {"id": "concern", "evidence": _demo_span(case_id, "early", early, "Family reported persistent concern.")},
                {"id": "result", "evidence": _demo_span(case_id, "late", late, "Later test result changed the outcome.")},
            ],
            "clocks": [
                clock("concern-time", "concern", "event", "early", early, "2026-11-17T08:00:00Z"),
                clock("concern-av", "concern", "availability", "early", early, "2026-11-17T09:00:00Z"),
                clock("result-time", "result", "event", "late", late, "2026-11-17T08:30:00Z"),
                clock("result-record", "result", "recording", "late", late, "2026-11-17T12:00:00Z"),
                clock("result-av", "result", "availability", "late", late, "2026-11-17T12:30:00Z"),
            ],
            "relations": [],
            "amendments": [],
        },
        "entitlements": [
            {"source_id": "early", "source_version": 1, "recipient_id": "rn-a",
             "first_available_utc": "2026-11-17T09:00:00Z"},
            {"source_id": "late", "source_version": 1, "recipient_id": "rn-a",
             "first_available_utc": "2026-11-17T12:30:00Z"},
            {"source_id": "early", "source_version": 1, "recipient_id": "rn-b",
             "first_available_utc": None},
            {"source_id": "late", "source_version": 1, "recipient_id": "rn-b",
             "first_available_utc": None},
        ],
        "labels": [
            {"event_id": "concern", "kind": "patient_family_concern", "speaker_role": "family"},
            {"event_id": "result", "kind": "outcome", "speaker_role": None},
        ],
    }


def generate_receipt() -> JsonObject:
    """Auditable synthetic inputs and outputs; not an actor-facing decision packet."""
    base = _synthetic_input()
    late = {**base, "cutoff_utc": "2026-11-17T13:00:00Z"}
    other = {**base, "recipient_id": "rn-b"}
    inputs = [base, late, other]
    cases = [assemble_decision_packet(case) for case in inputs]
    receipt: JsonObject = {
        "schema_version": "faw10-d3-receipt-1.0",
        "task": "FAW10/D3",
        "dataset": "generated-synthetic-only",
        "command": "uv run --no-sync python -m tools.workbench d3-demo",
        "permitted_view": VIEW,
        "linkage_basis": LINKAGE,
        "privacy_mode": "fully_local",
        "dependency_lock_sha256": "sha256:" + sha256((ROOT / "uv.lock").read_bytes()).hexdigest(),
        "implementation_files": {
            path: "sha256:" + sha256((ROOT / path).read_bytes()).hexdigest()
            for path in IMPLEMENTATION_FILES
        },
        "inputs": inputs,
        "input_fingerprint": fingerprint(inputs),
        "case_count": len(cases),
        "visible_counts": [case["event_count"] for case in cases],
        "cases": cases,
        "limitations": [
            "Development receipt includes synthetic unscoped inputs for audit; never present it as an actor packet.",
            "Entitlement and patient/family labels are caller-declared, not independently validated delivery or semantics.",
            "Unknown availability and any possible post-cutoff window are withheld; strict time comparison uses UTC seconds.",
            "No model retrieval or clinical approval, no actual patient information and no held-out effectiveness claim.",
        ],
        "output_fingerprint": "",
    }
    receipt["output_fingerprint"] = fingerprint(
        {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    )
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        payload = canonical_bytes(generate_receipt()) + b"\n"
        if sys.stdout.buffer.write(payload) != len(payload):
            raise OSError("incomplete D3 receipt write")
        sys.stdout.buffer.flush()
    except (OSError, ValueError) as exc:
        print(f"D3 receipt failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
