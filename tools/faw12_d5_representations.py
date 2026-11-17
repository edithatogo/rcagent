"""Bounded synthetic representation comparison over a D3 decision-time packet.

Shared-source OCR and native renderings are not independent evidence. Every row
is caller-declared annotation; this is not OCR, process conformance or clinical
verification. Public errors conceal excluded source and event identifiers.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Literal, TypedDict

from tools.evidence_core import fingerprint
from tools.faw07_d0_demo import SpanObservation
from tools.faw10_d3_decision_view import assemble_decision_packet
from tools.json_shapes import is_array, require_object

RepresentationKind = Literal["native_text", "layout_ocr", "structured_log"]
RepresentationStatus = Literal["simulated_annotation", "unsupported"]


class Representation(TypedDict):
    id: str
    event_id: str
    comparison_key: str
    origin_family_id: str
    representation_kind: RepresentationKind
    status: RepresentationStatus
    value: str | None
    evidence: SpanObservation
    value_semantically_verified: Literal[False]


class Comparison(TypedDict):
    comparison_key: str
    origin_count: int
    simulated_representations: int
    unsupported_representations: int
    values: list[str]
    representation_disagreement: bool
    cross_origin_disagreement: bool
    declared_agreement_without_qualification: bool


class D5Result(TypedDict):
    schema_version: Literal["faw12-d5-representations-0.1"]
    status: Literal["synthetic_contract_only"]
    case_id: str
    recipient_id: str
    cutoff_utc: str
    d3_packet_fingerprint: str
    representations: list[Representation]
    comparisons: list[Comparison]
    ocr_executed: Literal[False]
    model_executed: Literal[False]
    independence_qualified: Literal[False]
    clinical_qualification: Literal["none"]
    result_fingerprint: str


_KEYS = {
    "id",
    "event_id",
    "comparison_key",
    "origin_family_id",
    "representation_kind",
    "status",
    "value",
}


def _text(value: object, label: str, limit: int = 128) -> str:
    if type(value) is not str or not value or len(value) > limit:
        raise ValueError(f"invalid {label}")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"invalid UTF-8 for {label}") from exc
    return value


def _kind(value: object) -> RepresentationKind:
    if type(value) is not str:
        raise ValueError("invalid representation kind")
    if value == "native_text":
        return "native_text"
    if value == "layout_ocr":
        return "layout_ocr"
    if value == "structured_log":
        return "structured_log"
    raise ValueError("unsupported representation kind")


def _status(value: object) -> RepresentationStatus:
    if type(value) is not str:
        raise ValueError("invalid representation state")
    if value == "simulated_annotation":
        return "simulated_annotation"
    if value == "unsupported":
        return "unsupported"
    raise ValueError("unsupported representation state")


def _comparison(rows: list[Representation], key: str) -> Comparison:
    observed: dict[str, set[str]] = defaultdict(set)
    simulated = 0
    unsupported = 0
    for row in rows:
        if row["status"] == "unsupported":
            unsupported += 1
            continue
        simulated += 1
        value = row["value"]
        if value is None:
            raise ValueError("simulated comparison requires text")
        observed[row["origin_family_id"]].add(value)
    values = sorted(set().union(*observed.values())) if observed else []
    within = any(len(group) > 1 for group in observed.values())
    across = (
        len(observed) > 1
        and len(values) > 1
        and any(group != observed[next(iter(observed))] for group in observed.values())
    )
    independent_agreement = len(observed) > 1 and not within and len(values) == 1
    return {
        "comparison_key": key,
        "origin_count": len(observed),
        "simulated_representations": simulated,
        "unsupported_representations": unsupported,
        "values": values,
        "representation_disagreement": within,
        "cross_origin_disagreement": across,
        "declared_agreement_without_qualification": independent_agreement,
    }


def _compare_representations(case: object, rows: object) -> D5Result:
    if not is_array(rows) or len(rows) > 64:
        raise ValueError("representations must be an array of at most 64 annotations")
    packet = assemble_decision_packet(case)
    events = {event["event_id"]: event for event in packet["events"]}
    unique_ids: set[str] = set()
    source_to_origin: dict[str, str] = {}
    result_rows: list[Representation] = []
    for value in rows:
        row = require_object(value, context="representation")
        if set(row) != _KEYS:
            raise ValueError("invalid representation keys")
        identity = _text(row["id"], "representation identity")
        if identity in unique_ids:
            raise ValueError("duplicate representation identity")
        unique_ids.add(identity)
        event_id = _text(row["event_id"], "event identity")
        if event_id not in events:
            raise ValueError("event outside admitted D3 view")
        key = _text(row["comparison_key"], "comparison key")
        origin = _text(row["origin_family_id"], "origin family")
        kind = _kind(row["representation_kind"])
        state = _status(row["status"])
        raw = row["value"]
        if state == "unsupported":
            if raw is not None:
                raise ValueError("unsupported representation may not contain a value")
            text_value = None
        else:
            text_value = _text(raw, "simulated value", 512)
            if len(text_value.encode("utf-8")) > 512:
                raise ValueError("simulated representation exceeds UTF-8 limit")
        evidence = events[event_id]["evidence"]
        digest = evidence["source_sha256"]
        previous = source_to_origin.get(digest)
        if previous is not None and previous != origin:
            raise ValueError("same source cannot declare multiple origin families")
        source_to_origin[digest] = origin
        result_rows.append(
            {
                "id": identity,
                "event_id": event_id,
                "comparison_key": key,
                "origin_family_id": origin,
                "representation_kind": kind,
                "status": state,
                "value": text_value,
                "evidence": evidence,
                "value_semantically_verified": False,
            }
        )
    result_rows.sort(key=lambda item: item["id"])
    keys = sorted({item["comparison_key"] for item in result_rows})
    summaries = [
        _comparison(
            [item for item in result_rows if item["comparison_key"] == key],
            key,
        )
        for key in keys
    ]
    result: D5Result = {
        "schema_version": "faw12-d5-representations-0.1",
        "status": "synthetic_contract_only",
        "case_id": packet["case_id"],
        "recipient_id": packet["recipient_id"],
        "cutoff_utc": packet["cutoff_utc"],
        "d3_packet_fingerprint": packet["view_fingerprint"],
        "representations": result_rows,
        "comparisons": summaries,
        "ocr_executed": False,
        "model_executed": False,
        "independence_qualified": False,
        "clinical_qualification": "none",
        "result_fingerprint": "",
    }
    result["result_fingerprint"] = fingerprint(
        {key: value for key, value in result.items() if key != "result_fingerprint"}
    )
    return result


def compare_representations(case: object, rows: object) -> D5Result:
    """Revalidate the actor/cutoff first, then reject invalid annotation claims.

    No D3 source/entitlement error detail is returned on the public interface.
    """
    try:
        return _compare_representations(case, rows)
    except (KeyError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid or unauthorized D5 representations") from None
