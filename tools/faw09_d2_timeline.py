"""Assemble explicitly linked synthetic evidence into a bounded partial order.

Clock roles and event linkage are caller-declared annotations, not semantic
inferences. D0 proves exact source identity; this module preserves unresolved
clocks and conflicting accounts without choosing an event's point time.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from graphlib import CycleError, TopologicalSorter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw07_d0_demo import SourceObservation, SpanObservation, inspect_case
from tools.faw09_d2_clock import ClockInterpretation, interpret_clock
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
VIEW = "synthetic-d2-timeline-only"
RULE_VERSION = "faw09-d2-rules-1.0"
LINKAGE = "caller-declared-synthetic-annotations"
IMPLEMENTATION_FILES = (
    "tools/faw09_d2_timeline.py",
    "tools/faw09_d2_clock.py",
    "tools/workbench.py",
    "tools/faw07_d0_demo.py",
    "tools/evidence_core.py",
    "tools/json_shapes.py",
)
ClockKind = Literal["event", "recording", "availability"]
IntervalRelation = Literal["before", "after", "same_reported_time", "overlap_or_touch", "unknown"]
Order = Literal["before", "after", "same_reported_time", "unknown", "inconsistent"]
SummaryStatus = Literal["known", "ambiguous", "conflicting", "unknown", "unresolved"]


class UTCWindow(TypedDict):
    start: str
    end: str


class ClockSummary(TypedDict):
    assertion_ids: list[str]
    active_assertion_ids: list[str]
    status: SummaryStatus
    reasons: list[str]
    disagreement: bool
    windows: list[UTCWindow] | None


class ClockAssertion(TypedDict):
    id: str
    binding_id: str
    event_id: str
    kind: ClockKind
    recipient_id: str | None
    evidence: SpanObservation
    interpretation: ClockInterpretation
    active: bool
    superseded_by: list[str]


class Assertion(TypedDict):
    text: str
    actor: None
    subject: None
    polarity: Literal["not_interpreted"]


class Availability(TypedDict):
    recipient_id: str
    clock: ClockSummary


class TimelineEvent(TypedDict):
    id: str
    binding_id: str
    evidence: SpanObservation
    assertion: Assertion
    event_time: ClockSummary
    recording_time: ClockSummary
    availability: list[Availability]


class Relation(TypedDict):
    id: str
    binding_id: str
    before_event_id: str
    after_event_id: str
    evidence: SpanObservation


class Amendment(TypedDict):
    id: str
    binding_id: str
    earlier_clock_id: str
    later_clock_id: str
    evidence: SpanObservation


class Edge(TypedDict):
    before_event_id: str
    after_event_id: str
    kind: Literal["asserted", "interval"]
    support_ids: list[str]


class Pair(TypedDict):
    left_event_id: str
    right_event_id: str
    interval_relation: IntervalRelation
    order: Order
    basis: list[str]


class Consistency(TypedDict):
    status: Literal["consistent", "inconsistent"]
    cycle_event_ids: list[str]
    infeasible_event_ids: list[str]


class D2CaseObservation(TypedDict):
    schema_version: Literal["faw09-d2-case-1.0"]
    case_id: str
    permitted_view: str
    linkage_basis: str
    rule_version: str
    source_admission: Literal["verified-full-source-witnesses-not-events"]
    sources: list[SourceObservation]
    recipients: list[str]
    events: list[TimelineEvent]
    clock_assertions: list[ClockAssertion]
    relations: list[Relation]
    amendments: list[Amendment]
    edges: list[Edge]
    pairs: list[Pair]
    consistency: Consistency
    display_order: list[str] | None
    display_order_is_temporal_evidence: Literal[False]
    event_count: int


class D2Receipt(TypedDict):
    schema_version: Literal["faw09-d2-receipt-1.0"]
    input_schema_version: Literal["faw09-d2-input-1.0"]
    rule_version: str
    generator_version: Literal["faw09-d2-generator-1.0"]
    task: Literal["FAW09/D2"]
    dataset: Literal["generated-synthetic-only"]
    command: str
    byte_coordinate_system: Literal["utf8-zero-based-half-open"]
    source_hash_algorithm: Literal["sha256"]
    inputs: list[JsonObject]
    input_fingerprint: str
    permitted_view: str
    linkage_basis: str
    privacy_mode: Literal["fully_local"]
    dependency_lock_sha256: str
    implementation_files: dict[str, str]
    case_count: int
    event_count: int
    clock_assertion_count: int
    cases: list[D2CaseObservation]
    limitations: list[str]
    output_fingerprint: str


_CASE_KEYS = {
    "case_id",
    "permitted_view",
    "sources",
    "recipients",
    "events",
    "clocks",
    "relations",
    "amendments",
}
_SPAN_KEYS = {
    "case_id",
    "source_id",
    "source_version",
    "source_sha256",
    "coordinate_system",
    "start_byte",
    "end_byte",
    "text",
}
_FIELDS = {
    "events": {"id", "evidence"},
    "clocks": {"id", "event_id", "kind", "recipient_id", "evidence"},
    "relations": {"id", "before_event_id", "after_event_id", "evidence"},
    "amendments": {"id", "earlier_clock_id", "later_clock_id", "evidence"},
}


def _dictionary(value: object) -> TypeGuard[dict[object, object]]:
    """Narrow only the container; keys and domain fields remain unvalidated."""
    return isinstance(value, dict)


def _object(value: object, keys: set[str], label: str) -> JsonObject:
    if not _dictionary(value):
        raise ValueError(f"{label} must be a string-keyed object")
    if len(value) != len(keys):
        raise ValueError(f"{label} fields must be exactly {sorted(keys)}")
    row = require_object(value, context=label)
    if set(row) != keys:
        raise ValueError(f"{label} fields must be exactly {sorted(keys)}")
    return row


def _text(value: object, label: str, limit: int = 128) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be nonempty text")
    if len(value) > limit:
        raise ValueError(f"{label} exceeds {limit} characters")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{label} must be UTF-8 encodable") from exc
    return value


def _integer(value: object, label: str, minimum: int) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer at least {minimum}")
    return value


def _array(value: object, label: str, limit: int) -> list[object]:
    if not is_array(value):
        raise ValueError(f"{label} must be an array")
    if len(value) > limit:
        raise ValueError(f"{label} exceeds {limit} entries")
    return value


def _rows(values: list[object], category: str) -> dict[str, JsonObject]:
    rows: dict[str, JsonObject] = {}
    for value in values:
        row = _object(value, _FIELDS[category], category)
        identity = _text(row["id"], f"{category} id")
        if identity in rows:
            raise ValueError(f"duplicate {category} identity: {identity}")
        rows[identity] = row
    return dict(sorted(rows.items()))


def _sources(
    values: list[object], case_id: str
) -> tuple[list[JsonObject], list[SourceObservation]]:
    rows: list[JsonObject] = []
    witnesses: list[JsonObject] = []
    for value in values:
        row = _object(
            value, {"id", "version", "case_id", "state", "content", "fingerprint"}, "source"
        )
        sid = _text(row["id"], "source id")
        source_case = _text(row["case_id"], "source case_id")
        version = _integer(row["version"], "source version", 1)
        if _text(row["state"], "source state") != "present":
            raise ValueError("D2 requires present sources")
        content = _text(row["content"], "source content", 65_536)
        size = len(content.encode("utf-8"))
        if size > 65_536:
            raise ValueError("source content exceeds 65536 UTF-8 bytes")
        digest = _text(row["fingerprint"], "source fingerprint", 71)
        rows.append(row)
        witnesses.append(
            {
                "id": f"source:{sid}:{version}",
                "case_id": source_case,
                "source_id": sid,
                "source_version": version,
                "source_sha256": digest,
                "coordinate_system": "utf8-byte",
                "start_byte": 0,
                "end_byte": size,
                "text": content,
            }
        )
    admitted = inspect_case({"case_id": case_id, "sources": rows, "evidence": witnesses})
    if admitted["status"] != "accepted":
        raise ValueError("D2 source admission failed: " + "; ".join(admitted["errors"]))
    summaries = sorted(admitted["sources"], key=lambda item: (item["source_id"], item["version"]))
    return rows, summaries


def _span(value: object, identity: str, *, clock: bool) -> JsonObject:
    row = _object(value, _SPAN_KEYS, "evidence")
    for key in ("case_id", "source_id", "source_sha256", "coordinate_system"):
        _text(row[key], f"evidence {key}")
    _integer(row["source_version"], "evidence source_version", 1)
    _integer(row["start_byte"], "evidence start_byte", 0)
    _integer(row["end_byte"], "evidence end_byte", 0)
    text = _text(
        row["text"], "clock expression" if clock else "evidence text", 512 if clock else 65_536
    )
    if len(text.encode("utf-8")) > (512 if clock else 65_536):
        raise ValueError("evidence text exceeds UTF-8 byte limit")
    return {**row, "id": identity}


def _kind(value: object) -> ClockKind:
    value = _text(value, "clock kind")
    if value == "event":
        return "event"
    if value == "recording":
        return "recording"
    if value == "availability":
        return "availability"
    raise ValueError("clock kind must be event, recording or availability")


def _reference(row: JsonObject, key: str, known: set[str], label: str) -> str:
    value = _text(row[key], key)
    if value not in known:
        raise ValueError(f"unknown {label}: {value}")
    return value


def _binding(case_id: str, category: str, row: JsonObject) -> str:
    return fingerprint([case_id, VIEW, RULE_VERSION, LINKAGE, category, row])


def _clock_assertions(
    case_id: str,
    rows: dict[str, JsonObject],
    spans: dict[str, SpanObservation],
) -> list[ClockAssertion]:
    result: list[ClockAssertion] = []
    for identity, row in rows.items():
        recipient = row["recipient_id"]
        span = spans[f"clocks:{identity}"]
        result.append(
            {
                "id": identity,
                "binding_id": _binding(case_id, "clocks", row),
                "event_id": _text(row["event_id"], "event_id"),
                "kind": _kind(row["kind"]),
                "recipient_id": _text(recipient, "recipient_id") if recipient is not None else None,
                "evidence": span,
                "interpretation": interpret_clock(span["text"]),
                "active": True,
                "superseded_by": [],
            }
        )
    return result


def _amendments(
    case_id: str,
    rows: dict[str, JsonObject],
    spans: dict[str, SpanObservation],
    clocks: list[ClockAssertion],
) -> list[Amendment]:
    index = {clock["id"]: clock for clock in clocks}
    result: list[Amendment] = []
    for identity, row in rows.items():
        old_id = _text(row["earlier_clock_id"], "earlier_clock_id")
        new_id = _text(row["later_clock_id"], "later_clock_id")
        old, new = index[old_id], index[new_id]
        evidence = spans[f"amendments:{identity}"]
        same_domain = (old["event_id"], old["kind"], old["recipient_id"]) == (
            new["event_id"],
            new["kind"],
            new["recipient_id"],
        )
        a, b = old["evidence"], new["evidence"]
        if (
            not same_domain
            or a["source_id"] != b["source_id"]
            or a["source_version"] >= b["source_version"]
        ):
            raise ValueError(
                "amendment requires same clock domain/source and increasing source version"
            )
        if (evidence["source_id"], evidence["source_version"]) != (
            b["source_id"],
            b["source_version"],
        ):
            raise ValueError("amendment evidence must belong to the later source version")
        old["active"] = False
        old["superseded_by"] = sorted(set(old["superseded_by"]) | {new_id})
        result.append(
            {
                "id": identity,
                "binding_id": _binding(case_id, "amendments", row),
                "earlier_clock_id": old_id,
                "later_clock_id": new_id,
                "evidence": evidence,
            }
        )
    return result


def _summary(
    clocks: list[ClockAssertion], event: str, kind: ClockKind, recipient: str | None = None
) -> ClockSummary:
    selected = [
        clock
        for clock in clocks
        if (clock["event_id"], clock["kind"], clock["recipient_id"]) == (event, kind, recipient)
    ]
    active = [clock for clock in selected if clock["active"]]
    result: ClockSummary = {
        "assertion_ids": [clock["id"] for clock in selected],
        "active_assertion_ids": [clock["id"] for clock in active],
        "status": "unknown",
        "reasons": ["no_assertion"],
        "disagreement": False,
        "windows": None,
    }
    if not active:
        return result
    sets: list[set[tuple[str, str]]] = []
    reasons: set[str] = set()
    unresolved = False
    ambiguous = False
    for clock in active:
        interpreted = clock["interpretation"]
        reason = interpreted["reason"]
        if reason is not None:
            reasons.add(reason)
        if interpreted["status"] not in ("resolved", "ambiguous"):
            unresolved = True
            continue
        windows: set[tuple[str, str]] = set()
        for window in interpreted["windows"]:
            start, end = window["utc_start"], window["utc_end"]
            if start is None or end is None:
                raise ValueError("resolved clock lacks UTC bounds")
            windows.add((start, end))
        sets.append(windows)
        ambiguous = ambiguous or interpreted["status"] == "ambiguous"
    disagreement = any(windows != sets[0] for windows in sets[1:])
    if disagreement:
        reasons.add("conflicting_clock_assertions")
    result["disagreement"] = disagreement
    result["reasons"] = sorted(reasons)
    if unresolved:
        result["status"] = "unresolved"
        return result
    union: set[tuple[str, str]] = set()
    for windows in sets:
        union.update(windows)
    combined = sorted(union)
    result["windows"] = [{"start": start, "end": end} for start, end in combined]
    result["status"] = (
        "conflicting"
        if disagreement
        else "ambiguous"
        if ambiguous or len(combined) > 1
        else "known"
    )
    return result


def _interval_relation(left: ClockSummary, right: ClockSummary) -> IntervalRelation:
    a, b = left["windows"], right["windows"]
    if not a or not b:
        return "unknown"
    if max(item["end"] for item in a) < min(item["start"] for item in b):
        return "before"
    if max(item["end"] for item in b) < min(item["start"] for item in a):
        return "after"
    if len(a) == len(b) == 1 and a[0]["start"] == a[0]["end"] == b[0]["start"] == b[0]["end"]:
        return "same_reported_time"
    if any(x["start"] <= y["end"] and y["start"] <= x["end"] for x in a for y in b):
        return "overlap_or_touch"
    return "unknown"


def _seconds(value: str) -> int:
    stamp = datetime.fromisoformat(value)
    return stamp.toordinal() * 86400 + stamp.hour * 3600 + stamp.minute * 60 + stamp.second


def _feasibility(
    order: list[str],
    predecessors: dict[str, list[str]],
    events: dict[str, TimelineEvent],
) -> list[str]:
    earliest: dict[str, int | None] = {}
    failures: list[str] = []
    for event_id in order:
        previous = [
            value + 1
            for predecessor in predecessors[event_id]
            if (value := earliest[predecessor]) is not None
        ]
        threshold = max(previous) if previous else None
        windows = events[event_id]["event_time"]["windows"]
        if windows is None:
            # None is abstract negative infinity. Integers can exceed the
            # datetime calendar for an unknown clock; no chosen time is exported.
            earliest[event_id] = threshold
            continue
        bounds = [(_seconds(window["start"]), _seconds(window["end"])) for window in windows]
        candidates = [
            start if threshold is None else max(start, threshold)
            for start, end in bounds
            if threshold is None or threshold <= end
        ]
        if candidates:
            earliest[event_id] = min(candidates)
        else:
            failures.append(event_id)
            earliest[event_id] = threshold
    return sorted(failures)


def _ordering(
    events: list[TimelineEvent],
    relations: list[Relation],
) -> tuple[list[Edge], list[Pair], Consistency, list[str] | None]:
    index = {event["id"]: event for event in events}
    edges: list[Edge] = [
        {
            "before_event_id": row["before_event_id"],
            "after_event_id": row["after_event_id"],
            "kind": "asserted",
            "support_ids": [row["id"]],
        }
        for row in relations
    ]
    interval_pairs: list[tuple[str, str, IntervalRelation]] = []
    for left, right in combinations(index, 2):
        a, b = index[left]["event_time"], index[right]["event_time"]
        relation = _interval_relation(a, b)
        interval_pairs.append((left, right, relation))
        if relation in ("before", "after"):
            edges.append(
                {
                    "before_event_id": left if relation == "before" else right,
                    "after_event_id": right if relation == "before" else left,
                    "kind": "interval",
                    "support_ids": sorted(a["active_assertion_ids"] + b["active_assertion_ids"]),
                }
            )
    edges.sort(
        key=lambda row: (
            row["before_event_id"],
            row["after_event_id"],
            row["kind"],
            row["support_ids"],
        )
    )
    reach: dict[str, set[str]] = {identity: set() for identity in index}
    for edge in edges:
        reach[edge["before_event_id"]].add(edge["after_event_id"])
    predecessors = {
        identity: sorted(before for before, after in reach.items() if identity in after)
        for identity in index
    }
    for middle in index:
        for before in index:
            if middle in reach[before]:
                reach[before].update(reach[middle])
    cycle_ids = sorted(identity for identity in index if identity in reach[identity])
    display: list[str] | None = []
    sorter = TopologicalSorter(predecessors)
    try:
        sorter.prepare()
    except CycleError:
        display = None
    else:
        while sorter.is_active():
            ready = sorted(sorter.get_ready())
            display.extend(ready)
            sorter.done(*ready)
    infeasible = _feasibility(display, predecessors, index) if display is not None else []
    consistent = not cycle_ids and not infeasible
    if not consistent:
        display = None
    pairs: list[Pair] = []
    for left, right, relation in interval_pairs:
        order: Order = "unknown"
        basis: list[str] = []
        if not consistent:
            order = "inconsistent"
        elif right in reach[left] or left in reach[right]:
            before, after = (left, right) if right in reach[left] else (right, left)
            order = "before" if before == left else "after"
            basis = sorted(
                {
                    edge["kind"]
                    for edge in edges
                    if (edge["before_event_id"], edge["after_event_id"]) == (before, after)
                }
            ) or ["transitive"]
        elif relation == "same_reported_time":
            order = "same_reported_time"
            basis = ["interval"]
        pairs.append(
            {
                "left_event_id": left,
                "right_event_id": right,
                "interval_relation": relation,
                "order": order,
                "basis": basis,
            }
        )
    consistency: Consistency = {
        "status": "consistent" if consistent else "inconsistent",
        "cycle_event_ids": cycle_ids,
        "infeasible_event_ids": infeasible,
    }
    return edges, pairs, consistency, display


def assemble_timeline(case: object) -> D2CaseObservation:
    """Admit every binding, retain clock assertions, then check a partial order."""
    record = _object(case, _CASE_KEYS, "D2 case")
    case_id = _text(record["case_id"], "case_id")
    if _text(record["permitted_view"], "permitted_view") != VIEW:
        raise ValueError("D2 requires the synthetic-d2-timeline-only permitted view")
    limits = {
        "sources": 32,
        "recipients": 16,
        "events": 16,
        "clocks": 32,
        "relations": 32,
        "amendments": 16,
    }
    arrays = {key: _array(record[key], key, limit) for key, limit in limits.items()}
    if sum(len(arrays[key]) for key in _FIELDS) > 64:
        raise ValueError("D2 exceeds 64 domain spans")
    recipients = sorted(_text(value, "recipient") for value in arrays["recipients"])
    if len(set(recipients)) != len(recipients):
        raise ValueError("duplicate recipient identity")
    source_rows, sources = _sources(arrays["sources"], case_id)
    rows = {key: _rows(arrays[key], key) for key in _FIELDS}
    event_ids, clock_ids = set(rows["events"]), set(rows["clocks"])
    for row in rows["clocks"].values():
        _reference(row, "event_id", event_ids, "event")
        kind = _kind(row["kind"])
        if kind == "availability":
            _reference(row, "recipient_id", set(recipients), "recipient")
        elif row["recipient_id"] is not None:
            raise ValueError("event/recording clocks require a null recipient_id")
    for row in rows["relations"].values():
        _reference(row, "before_event_id", event_ids, "event")
        _reference(row, "after_event_id", event_ids, "event")
    for row in rows["amendments"].values():
        _reference(row, "earlier_clock_id", clock_ids, "clock")
        _reference(row, "later_clock_id", clock_ids, "clock")
    evidence = [
        _span(row["evidence"], f"{category}:{identity}", clock=category == "clocks")
        for category, group in rows.items()
        for identity, row in group.items()
    ]
    verified = (
        inspect_case({"case_id": case_id, "sources": source_rows, "evidence": evidence})
        if evidence
        else None
    )
    if verified is not None and verified["status"] != "accepted":
        raise ValueError("D2 span admission failed: " + "; ".join(verified["errors"]))
    spans = (
        {span["evidence_id"]: span for span in verified["spans"]} if verified is not None else {}
    )
    clocks = _clock_assertions(case_id, rows["clocks"], spans)
    amendments = _amendments(case_id, rows["amendments"], spans, clocks)
    events: list[TimelineEvent] = []
    for identity, row in rows["events"].items():
        span = spans[f"events:{identity}"]
        events.append(
            {
                "id": identity,
                "binding_id": _binding(case_id, "events", row),
                "evidence": span,
                "assertion": {
                    "text": span["text"],
                    "actor": None,
                    "subject": None,
                    "polarity": "not_interpreted",
                },
                "event_time": _summary(clocks, identity, "event"),
                "recording_time": _summary(clocks, identity, "recording"),
                "availability": [
                    {
                        "recipient_id": recipient,
                        "clock": _summary(clocks, identity, "availability", recipient),
                    }
                    for recipient in recipients
                ],
            }
        )
    relations: list[Relation] = [
        {
            "id": identity,
            "binding_id": _binding(case_id, "relations", row),
            "before_event_id": _text(row["before_event_id"], "before_event_id"),
            "after_event_id": _text(row["after_event_id"], "after_event_id"),
            "evidence": spans[f"relations:{identity}"],
        }
        for identity, row in rows["relations"].items()
    ]
    edges, pairs, consistency, display = _ordering(events, relations)
    return {
        "schema_version": "faw09-d2-case-1.0",
        "case_id": case_id,
        "permitted_view": VIEW,
        "linkage_basis": LINKAGE,
        "rule_version": RULE_VERSION,
        "source_admission": "verified-full-source-witnesses-not-events",
        "sources": sources,
        "recipients": recipients,
        "events": events,
        "clock_assertions": clocks,
        "relations": relations,
        "amendments": amendments,
        "edges": edges,
        "pairs": pairs,
        "consistency": consistency,
        "display_order": display,
        "display_order_is_temporal_evidence": False,
        "event_count": len(events),
    }


def verify_timeline(case: object, result: object) -> bool:
    """Check deterministic replay, separately from independent semantic tests."""
    expected = canonical_bytes(assemble_timeline(case))
    try:
        return canonical_bytes(result) == expected
    except (TypeError, ValueError, RecursionError, UnicodeError):
        return False


def _demo_span(case_id: str, text: str, quote: str, version: int = 1) -> JsonObject:
    start = text.index(quote)
    return {
        "case_id": case_id,
        "source_id": "source-a",
        "source_version": version,
        "source_sha256": "sha256:" + sha256(text.encode("utf-8")).hexdigest(),
        "coordinate_system": "utf8-byte",
        "start_byte": len(text[:start].encode("utf-8")),
        "end_byte": len(text[: start + len(quote)].encode("utf-8")),
        "text": quote,
    }


def _synthetic_cases() -> list[JsonObject]:
    """Fixed input-only demonstrations, with no oracle labels or metrics."""
    examples = (
        ("2026-11-17T09:00:00+10:00", "2026-11-17T10:00:00+10:00"),
        ("2026-11-17T09:00Z", "2026-11-17T09:00:30Z"),
        ("2026-11-17T09:00:00Z", "2026-11-17T19:00:00+10:00"),
        ("2026-11-01T01:30 America/New_York", "2026-11-01T06:00:00Z"),
        ("2026-11-01T01:30:00-04:00 or 2026-11-01T01:30:00-05:00", "2026-11-01T06:00:00Z"),
        ("2026-11-17T09:00:00Z to 2026-11-17T11:00:00Z", "2026-11-17T10:00:00Z"),
        ("unknown", "unknown"),
        ("2026-11-17T09:00:00Z", "2026-11-17T09:00:00Z"),
        ("unknown", "unknown"),
        ("2026-11-17T09:00:00Z", "2026-11-17T10:00:00Z"),
    )
    cases: list[JsonObject] = []
    for number, expressions in enumerate(examples, 1):
        case_id = f"d2-example-{number:02}"
        text = "\n".join(
            f"Event {index}: {expression}" for index, expression in enumerate(expressions)
        )
        text += "\nRecorded: 2026-11-18T10:00:00Z\nAvailable: 2026-11-17T11:00:00Z\nEvent 0 before Event 1.\nEvent 1 before Event 0."
        digest = "sha256:" + sha256(text.encode("utf-8")).hexdigest()

        events: list[JsonObject] = [
            {"id": f"event-{i}", "evidence": _demo_span(case_id, text, f"Event {i}")}
            for i in range(2)
        ]
        clocks: list[JsonObject] = [
            {
                "id": f"clock-{i}",
                "event_id": f"event-{i}",
                "kind": "event",
                "recipient_id": None,
                "evidence": _demo_span(case_id, text, expression),
            }
            for i, expression in enumerate(expressions)
        ]
        other_clocks: list[JsonObject] = [
            {
                "id": "recording-0",
                "event_id": "event-0",
                "kind": "recording",
                "recipient_id": None,
                "evidence": _demo_span(case_id, text, "2026-11-18T10:00:00Z"),
            },
            {
                "id": "availability-0",
                "event_id": "event-0",
                "kind": "availability",
                "recipient_id": "clinician-a",
                "evidence": _demo_span(case_id, text, "2026-11-17T11:00:00Z"),
            },
        ]
        clocks.extend(other_clocks)
        relations: list[JsonObject] = []
        if number in (7, 8, 9):
            relations.append(
                {
                    "id": "before",
                    "before_event_id": "event-0",
                    "after_event_id": "event-1",
                    "evidence": _demo_span(case_id, text, "Event 0 before Event 1"),
                }
            )
        if number == 9:
            relations.append(
                {
                    "id": "reverse",
                    "before_event_id": "event-1",
                    "after_event_id": "event-0",
                    "evidence": _demo_span(case_id, text, "Event 1 before Event 0"),
                }
            )
        sources: list[JsonObject] = [
            {
                "id": "source-a",
                "version": 1,
                "case_id": case_id,
                "state": "present",
                "content": text,
                "fingerprint": digest,
            }
        ]
        amendments: list[JsonObject] = []
        if number == 10:
            corrected = (
                "Event 0 corrected to 2026-11-17T11:00:00Z; replaces the original event clock."
            )
            sources.append(
                {
                    "id": "source-a",
                    "version": 2,
                    "case_id": case_id,
                    "state": "present",
                    "content": corrected,
                    "fingerprint": "sha256:" + sha256(corrected.encode("utf-8")).hexdigest(),
                }
            )
            clocks.append(
                {
                    "id": "clock-0-amended",
                    "event_id": "event-0",
                    "kind": "event",
                    "recipient_id": None,
                    "evidence": _demo_span(case_id, corrected, "2026-11-17T11:00:00Z", 2),
                }
            )
            amendments.append(
                {
                    "id": "amendment-0",
                    "earlier_clock_id": "clock-0",
                    "later_clock_id": "clock-0-amended",
                    "evidence": _demo_span(
                        case_id, corrected, "replaces the original event clock", 2
                    ),
                }
            )
        cases.append(
            {
                "case_id": case_id,
                "permitted_view": VIEW,
                "sources": sources,
                "recipients": ["clinician-a", "clinician-b"],
                "events": events,
                "clocks": clocks,
                "relations": relations,
                "amendments": amendments,
            }
        )
    return cases


def generate_receipt() -> D2Receipt:
    """Bind inspectable synthetic inputs/results to the current code and lock."""
    inputs = _synthetic_cases()
    cases = [assemble_timeline(case) for case in inputs]
    receipt: D2Receipt = {
        "schema_version": "faw09-d2-receipt-1.0",
        "input_schema_version": "faw09-d2-input-1.0",
        "rule_version": RULE_VERSION,
        "generator_version": "faw09-d2-generator-1.0",
        "task": "FAW09/D2",
        "dataset": "generated-synthetic-only",
        "command": "uv run --no-sync python -m tools.workbench d2-demo",
        "byte_coordinate_system": "utf8-zero-based-half-open",
        "source_hash_algorithm": "sha256",
        "inputs": inputs,
        "input_fingerprint": fingerprint(inputs),
        "permitted_view": VIEW,
        "linkage_basis": LINKAGE,
        "privacy_mode": "fully_local",
        "dependency_lock_sha256": "sha256:" + sha256((ROOT / "uv.lock").read_bytes()).hexdigest(),
        "implementation_files": {
            path: "sha256:" + sha256((ROOT / path).read_bytes()).hexdigest()
            for path in IMPLEMENTATION_FILES
        },
        "case_count": len(cases),
        "event_count": sum(case["event_count"] for case in cases),
        "clock_assertion_count": sum(len(case["clock_assertions"]) for case in cases),
        "cases": cases,
        "limitations": [
            "Caller-declared synthetic event and clock linkage; no semantic entailment or automatic event extraction.",
            "Inclusive possible-time windows on a one-second grid, not activity durations or physical simultaneity.",
            "Named zones and missing offsets remain unresolved; no host timezone or default anchor.",
            "Graph closure and feasibility do not infer every relation obtainable by pruning alternatives.",
            "Availability is not proof of reading, understanding or D3 decision-time entitlement.",
            "Finite visible development examples; no model, held-out or clinical qualification.",
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
            raise OSError("incomplete D2 receipt write")
        sys.stdout.buffer.flush()
    except (OSError, ValueError) as exc:
        print(f"D2 receipt failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
