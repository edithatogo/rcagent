"""Extract bounded synthetic lexical observations with exact D0 byte provenance.

This grammar does not assemble events, infer clinical truth or supply missing
dates, actors or knowledge times. The CLI emits fixed, inspectable synthetic
inputs only. Independent expected labels live outside this producer.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw07_d0_demo import SourceObservation, SpanObservation, inspect_case
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
VIEW = "synthetic-d1-extraction-only"
RULE_VERSION = "faw08-d1-rules-1.0"
IMPLEMENTATION_FILES = (
    "tools/faw08_d1_extraction.py",
    "tools/workbench.py",
    "tools/faw07_d0_demo.py",
    "tools/evidence_core.py",
    "tools/json_shapes.py",
)
DateOrder = Literal["unknown", "DMY", "MDY"]
Kind = Literal[
    "date",
    "date_range",
    "time",
    "time_range",
    "quantity",
    "quantity_range",
    "relative_time",
    "assertion",
]
Status = Literal["resolved", "partial", "ambiguous", "invalid", "unsupported"]
Polarity = Literal["affirmed", "negated", "uncertain", "unknown"]


class D1Observation(TypedDict):
    observation_id: str
    case_id: str
    source_id: str
    source_version: int
    source_sha256: str
    coordinate_system: Literal["utf8-byte"]
    start_byte: int
    end_byte: int
    text: str
    kind: Kind
    status: Status
    normalized: JsonObject | None
    reason: str | None
    polarity: Polarity
    subject: str | None
    reporter: str | None
    context: SpanObservation
    anchor: SpanObservation | None
    timezone: None
    recording_time: None
    availability_time: None
    event_linkage: None
    context_reasons: list[str]
    method: Literal["deterministic-stdlib-rules"]
    rule_version: str


class D1CaseObservation(TypedDict):
    schema_version: Literal["faw08-d1-case-1.0"]
    case_id: str
    permitted_view: str
    date_order: DateOrder
    source_admission: Literal["verified-full-source-witnesses-not-observations"]
    sources: list[SourceObservation]
    observations: list[D1Observation]
    observation_count: int
    no_supported_observation: bool


class D1Receipt(TypedDict):
    schema_version: Literal["faw08-d1-receipt-1.0"]
    input_schema_version: Literal["faw08-d1-input-1.0"]
    rule_version: str
    generator_version: Literal["faw08-d1-generator-1.0"]
    task: Literal["FAW08/D1"]
    dataset: Literal["generated-synthetic-only"]
    command: str
    byte_coordinate_system: Literal["utf8-zero-based-half-open"]
    source_hash_algorithm: Literal["sha256"]
    inputs: list[JsonObject]
    input_fingerprint: str
    permitted_view: str
    privacy_mode: Literal["fully_local"]
    dependency_lock_sha256: str
    implementation_files: dict[str, str]
    case_count: int
    observation_count: int
    cases: list[D1CaseObservation]
    limitations: list[str]
    output_fingerprint: str


@dataclass(frozen=True)
class _Source:
    case_id: str
    source_id: str
    version: int
    text: str
    digest: str


@dataclass(frozen=True)
class _Anchor:
    span: SpanObservation
    local: datetime


@dataclass(frozen=True)
class _Interpretation:
    status: Status
    normalized: JsonObject | None
    reason: str | None = None


@dataclass(frozen=True)
class _Candidate:
    start: int
    end: int
    kind: Kind


def _digest(raw: bytes) -> str:
    return "sha256:" + sha256(raw).hexdigest()


def _text(row: JsonObject, key: str, *, identifier: bool = False, limit: int = 65_536) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be nonempty text")
    if identifier and len(value) > 128:
        raise ValueError(f"{key} exceeds 128 characters")
    if len(value) > limit:
        raise ValueError(f"{key} exceeds {limit} characters")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{key} must be UTF-8 encodable") from exc
    return value


def _version(row: JsonObject, key: str) -> int:
    value = row.get(key)
    if type(value) is not int or value < 1:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _evidence(source: _Source, eid: str, start: int, end: int) -> JsonObject:
    return {
        "id": eid,
        "case_id": source.case_id,
        "source_id": source.source_id,
        "source_version": source.version,
        "source_sha256": source.digest,
        "coordinate_system": "utf8-byte",
        "start_byte": len(source.text[:start].encode("utf-8")),
        "end_byte": len(source.text[:end].encode("utf-8")),
        "text": source.text[start:end],
    }


def _admit(
    record: JsonObject, case_id: str
) -> tuple[
    list[JsonObject], list[_Source], list[SourceObservation], dict[tuple[str, int], _Anchor]
]:
    raw_sources = record.get("sources")
    if not is_array(raw_sources) or not 1 <= len(raw_sources) <= 32:
        raise ValueError("sources must contain 1 to 32 objects")
    raw_anchors = record.get("anchors", [])
    if not is_array(raw_anchors) or len(raw_anchors) > 32:
        raise ValueError("anchors must be an array of at most 32 objects")
    rows: list[JsonObject] = []
    sources: list[_Source] = []
    witnesses: list[JsonObject] = []
    for index, raw in enumerate(raw_sources):
        row = require_object(raw, context="D1 source")
        sid = _text(row, "id", identifier=True)
        source_case = _text(row, "case_id", identifier=True)
        version = _version(row, "version")
        if source_case != case_id or row.get("state") != "present":
            raise ValueError("source admission requires present sources in the same case")
        content = _text(row, "content")
        if len(content) > 65_536 or len(content.encode("utf-8")) > 65_536:
            raise ValueError("source content exceeds 65536 UTF-8 bytes")
        source = _Source(case_id, sid, version, content, _text(row, "fingerprint", limit=71))
        sources.append(source)
        rows.append(row)
        witnesses.append(_evidence(source, f"source-witness-{index}", 0, len(content)))
    anchor_keys: set[tuple[str, int]] = set()
    for index, raw in enumerate(raw_anchors):
        row = require_object(raw, context="D1 anchor")
        _text(row, "case_id", identifier=True)
        _text(row, "source_sha256", limit=71)
        _text(row, "text")
        if row.get("coordinate_system") != "utf8-byte":
            raise ValueError("explicit anchor requires utf8-byte coordinates")
        key = (_text(row, "source_id", identifier=True), _version(row, "source_version"))
        if key in anchor_keys:
            raise ValueError("at most one explicit anchor per source version")
        anchor_keys.add(key)
        witnesses.append({**row, "id": f"anchor-{index}"})
    admission = inspect_case({"case_id": case_id, "sources": rows, "evidence": witnesses})
    if admission["status"] != "accepted":
        raise ValueError("source admission failed: " + "; ".join(admission["errors"]))
    anchors: dict[tuple[str, int], _Anchor] = {}
    for span in admission["spans"][len(sources) :]:
        if (
            re.fullmatch(
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}(?::[0-9]{2})?", span["text"]
            )
            is None
        ):
            raise ValueError("explicit anchor must be a local ISO date-time")
        try:
            local = datetime.fromisoformat(span["text"])
        except ValueError as exc:
            raise ValueError("explicit anchor must be a valid local ISO date-time") from exc
        anchors[(span["source_id"], span["source_version"])] = _Anchor(span, local)
    return rows, sources, admission["sources"], anchors


# Broad token recognition precedes strict interpretation: malformed/OCR tokens
# remain visible and cannot donate a valid-looking suffix to a scalar pattern.
_DIGITS = r"[0-9OoIlSB]"
_ISO = rf"{_DIGITS}{{4}}-{_DIGITS}{{1,2}}-{_DIGITS}{{1,2}}"
_CLOCK = rf"{_DIGITS}{{1,2}}:{_DIGITS}{{2}}(?::{_DIGITS}{{2}})?"
_SIGN = r"[+\-\u2212\u2013\u2014][ \t]*"
_NUMBER = rf"(?=(?:{_SIGN})?[0-9OoIlSB.,]*[0-9])(?:{_SIGN})?(?:[0-9OoIlSB]+(?:[.,][0-9OoIlSB]+)*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
_UNIT = r"(?:[A-Za-zµμ°%]+(?:[ \t]*(?:/|\u00b7|\*|\^)[ \t]*[A-Za-zµμ0-9+\-]+)*)"
_MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)
_DATE = rf"(?:{_ISO}|{_DIGITS}{{1,2}}/{_DIGITS}{{1,2}}/{_DIGITS}{{4}}|[0-9]{{1,2}}\s+(?:{'|'.join(_MONTHS)})(?:\s+[0-9]{{4}})?)"
_JOIN = r"\s*(?:\u2013|\bto\b)\s*|\s+-\s+"
_SHORT_JOIN = r"\s*(?:\u2013|-|\bto\b)\s*"
_PREFIX = r"[\w/.:,+\-\u2212\u2013\u2014]"
_LEFT = rf"(?<!{_PREFIX})"
_RIGHT = r"(?![\w/:\-]|\.[0-9])"
_T_DATE = rf"{_DIGITS}{{4}}-{_DIGITS}{{2}}-{_DIGITS}{{2}}T"
_PATTERNS: tuple[tuple[Kind, re.Pattern[str]], ...] = (
    ("date_range", re.compile(rf"{_LEFT}{_ISO}(?:{_JOIN}){_ISO}{_RIGHT}", re.IGNORECASE)),
    ("time_range", re.compile(rf"{_LEFT}{_CLOCK}{_SHORT_JOIN}{_CLOCK}{_RIGHT}", re.IGNORECASE)),
    (
        "relative_time",
        re.compile(
            rf"{_LEFT}(?:{_NUMBER}\s+(?:minutes?|hours?|days?)\s+(?:later|earlier)|yesterday|today|tomorrow)\b",
            re.IGNORECASE,
        ),
    ),
    ("date", re.compile(rf"{_LEFT}{_DATE}(?:{_RIGHT}|(?=T{_CLOCK}{_RIGHT}))", re.IGNORECASE)),
    (
        "time",
        re.compile(
            rf"(?:{_LEFT}|(?<={_T_DATE})(?<!{_PREFIX}{_T_DATE})){_CLOCK}{_RIGHT}", re.IGNORECASE
        ),
    ),
    (
        "quantity_range",
        re.compile(rf"{_LEFT}{_NUMBER}{_SHORT_JOIN}{_NUMBER}\s*{_UNIT}{_RIGHT}", re.IGNORECASE),
    ),
    ("quantity", re.compile(rf"{_LEFT}{_NUMBER}\s*{_UNIT}{_RIGHT}", re.IGNORECASE)),
    ("assertion", re.compile(r"\b(?:pain|fever|cough|rash|nausea|dizziness)\b", re.IGNORECASE)),
)
_UNITS = frozenset(
    (
        "mg",
        "g",
        "mcg",
        "µg",
        "μg",
        "kg",
        "mL",
        "L",
        "mL/h",
        "mg/kg",
        "mg/kg/h",
        "mmol/L",
        "bpm",
        "mmHg",
        "%",
        "°C",
    )
)


def _scan(text: str) -> list[_Candidate]:
    candidates: list[_Candidate] = []
    for kind, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            if any(start < item.end and end > item.start for item in candidates):
                continue
            candidates.append(_Candidate(start, end, kind))
            if len(candidates) > 32:
                raise ValueError("case exceeds 32 observations")
    return sorted(candidates, key=lambda item: (item.start, item.end, item.kind))


def _date_value(text: str, order: DateOrder) -> _Interpretation:
    if ("-" in text or "/" in text) and re.search(r"[OoIlSB]", text, re.IGNORECASE):
        return _Interpretation("unsupported", None, "ocr_corruption")
    year: int | None
    month: int
    day: int
    if "-" in text:
        year, month, day = (int(part) for part in text.split("-"))
    elif "/" in text:
        first, second, year = (int(part) for part in text.split("/"))
        possibilities: list[date] = []
        for selected in ("DMY", "MDY") if order == "unknown" else (order,):
            try:
                value = date(
                    year,
                    second if selected == "DMY" else first,
                    first if selected == "DMY" else second,
                )
            except ValueError:
                continue
            if value not in possibilities:
                possibilities.append(value)
        if not possibilities:
            return _Interpretation("invalid", None, "invalid_calendar_date")
        if len(possibilities) > 1:
            return _Interpretation(
                "ambiguous",
                {
                    "year": year,
                    "month": None,
                    "day": None,
                    "iso": None,
                    "alternatives": sorted(item.isoformat() for item in possibilities),
                },
                "ambiguous_numeric_date",
            )
        year, month, day = possibilities[0].year, possibilities[0].month, possibilities[0].day
    else:
        parts = text.lower().split()
        day, month = int(parts[0]), _MONTHS.index(parts[1]) + 1
        year = int(parts[2]) if len(parts) == 3 else None
    try:
        value = date(year if year is not None else 2000, month, day)
    except ValueError:
        return _Interpretation("invalid", None, "invalid_calendar_date")
    normalized: JsonObject = {
        "year": year,
        "month": month,
        "day": day,
        "iso": value.isoformat() if year is not None else None,
        "alternatives": [],
    }
    return _Interpretation(
        "resolved" if year is not None else "partial",
        normalized,
        None if year is not None else "missing_year",
    )


def _time_value(text: str) -> _Interpretation:
    if re.search(r"[OoIlSB]", text, re.IGNORECASE):
        return _Interpretation("unsupported", None, "ocr_corruption")
    parts = [int(part) for part in text.split(":")]
    try:
        value = time(parts[0], parts[1], parts[2] if len(parts) == 3 else 0)
    except ValueError:
        return _Interpretation("invalid", None, "invalid_clock_time")
    return _Interpretation(
        "resolved",
        {"time": value.isoformat(), "precision": "second" if len(parts) == 3 else "minute"},
    )


def _range_value(text: str, kind: Kind, order: DateOrder) -> _Interpretation:
    parts = re.split(
        _JOIN if kind == "date_range" else _SHORT_JOIN, text, maxsplit=1, flags=re.IGNORECASE
    )
    left = _date_value(parts[0], order) if kind == "date_range" else _time_value(parts[0])
    right = _date_value(parts[1], order) if kind == "date_range" else _time_value(parts[1])
    for value in (left, right):
        if value.status != "resolved":
            return _Interpretation(value.status, None, value.reason)
    key = "iso" if kind == "date_range" else "time"
    start = _text(require_object(left.normalized, context="range start"), key)
    end = _text(require_object(right.normalized, context="range end"), key)
    if end < start:
        if kind == "time_range":
            return _Interpretation("ambiguous", {"start": start, "end": end}, "range_requires_date")
        return _Interpretation("invalid", None, "reversed_range")
    return _Interpretation("resolved", {"start": start, "end": end})


def _quantity_value(text: str, kind: Kind) -> _Interpretation:
    pattern = (
        rf"({_NUMBER}){_SHORT_JOIN}({_NUMBER})\s*({_UNIT})"
        if kind == "quantity_range"
        else rf"({_NUMBER})\s*({_UNIT})"
    )
    match = re.fullmatch(pattern, text, flags=re.IGNORECASE)
    if match is None:
        raise ValueError("quantity candidate does not match the declared grammar")
    tokens, unit = match.groups()[:-1], match.groups()[-1]
    if any(len(token) > 32 for token in tokens):
        return _Interpretation("unsupported", None, "number_length_limit")
    if any(re.search(r"[OoIlSB]", token, re.IGNORECASE) for token in tokens):
        return _Interpretation("unsupported", None, "ocr_corruption")
    if any("," in token for token in tokens):
        return _Interpretation("ambiguous", None, "ambiguous_number_format")
    if any(
        re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)", token) is None for token in tokens
    ):
        return _Interpretation("unsupported", None, "unsupported_number_format")
    if unit not in _UNITS:
        return _Interpretation("unsupported", None, "unsupported_unit")
    values = [Decimal(token) for token in tokens]
    if kind == "quantity_range":
        if values[1] < values[0]:
            return _Interpretation("invalid", None, "reversed_range")
        return _Interpretation(
            "resolved", {"lower": str(values[0]), "upper": str(values[1]), "unit": unit}
        )
    return _Interpretation("resolved", {"value": str(values[0]), "unit": unit})


def _relative_value(text: str, anchor: _Anchor | None) -> _Interpretation:
    lowered = text.lower()
    day_words = {"yesterday": -1, "today": 0, "tomorrow": 1}
    if lowered in day_words:
        offset = day_words[lowered]
        try:
            local_date = (
                (anchor.local.date() + timedelta(days=offset)).isoformat() if anchor else None
            )
        except OverflowError:
            return _Interpretation("invalid", None, "relative_time_out_of_range")
        normalized: JsonObject = {"offset_days": offset, "date": local_date}
    else:
        number, unit, direction = lowered.rsplit(maxsplit=2)
        if "," in number:
            return _Interpretation("ambiguous", None, "ambiguous_number_format")
        if re.fullmatch(r"[0-9]+", number) is None:
            return _Interpretation("unsupported", None, "unsupported_number_format")
        if len(number) > 6:
            return _Interpretation("unsupported", None, "relative_offset_limit")
        seconds = int(number) * (
            60 if unit.startswith("minute") else 3600 if unit.startswith("hour") else 86400
        )
        if direction == "earlier":
            seconds = -seconds
        try:
            local_datetime = (
                (anchor.local + timedelta(seconds=seconds)).isoformat() if anchor else None
            )
        except OverflowError:
            return _Interpretation("invalid", None, "relative_time_out_of_range")
        normalized = {"offset_seconds": seconds, "local_datetime": local_datetime}
    return _Interpretation(
        "resolved" if anchor else "partial",
        normalized,
        None if anchor else "missing_explicit_anchor",
    )


def _interpret(text: str, kind: Kind, order: DateOrder, anchor: _Anchor | None) -> _Interpretation:
    if kind == "date":
        return _date_value(text, order)
    if kind == "time":
        return _time_value(text)
    if kind in ("date_range", "time_range"):
        return _range_value(text, kind, order)
    if kind in ("quantity", "quantity_range"):
        return _quantity_value(text, kind)
    if kind == "relative_time":
        return _relative_value(text, anchor)
    return _Interpretation("resolved", {"observation": text.lower()})


_BOUNDARY = re.compile(r"(?<![0-9])\.|\.(?![0-9])|[!?;\r\n]+|\b(?:but|however)\b", re.IGNORECASE)
_NEGATIVE = r"(?:did\s+not\s+receive|does\s+not\s+have|not\s+(?:received|given|administered)|denies|denied|no)"
_POSITIVE = r"(?:received|was|is|has|had|given|administered|reports)"
_ENTITY = r"(?:\[(?:Patient|Consumer|Clinician|RN)\s+[A-Za-z0-9]+\]|\b(?:patient|child|mother|father|nurse|clinician)\b)"
_ATTRIBUTION = re.compile(rf"(?P<subject>{_ENTITY})\s+(?:{_NEGATIVE}|{_POSITIVE})\b", re.IGNORECASE)
_REPORTER = re.compile(
    rf"(?P<reporter>{_ENTITY})\s+reports(?:\s+that)?\s+(?P<subject>{_ENTITY})\s+(?:{_NEGATIVE}|{_POSITIVE})\b",
    re.IGNORECASE,
)
_UNSUPPORTED_SCOPE = re.compile(
    r"\b(?:if|unless|might|may|could|would|possible|possibly|hypothetical|never|without)\b|\bnot\s+only\b",
    re.IGNORECASE,
)
_NEGATION_MARKER = re.compile(r"\b(?:no|not|deny|denies|denied|never|without)\b", re.IGNORECASE)


def _context_bounds(text: str, candidate: _Candidate) -> tuple[int, int]:
    start, end = 0, len(text)
    for boundary in _BOUNDARY.finditer(text):
        if boundary.end() <= candidate.start:
            start = boundary.end()
        elif boundary.start() >= candidate.end:
            end = boundary.start()
            break
    while start < candidate.start and text[start].isspace():
        start += 1
    while end > candidate.end and text[end - 1].isspace():
        end -= 1
    return start, end


def _entity(value: str) -> str:
    return value if value.startswith("[") else value.lower()


def _context_fields(
    prefix: str, clause: str, assertion_tail: str | None
) -> tuple[Polarity, str | None, str | None, list[str]]:
    subject: str | None = None
    reporter: str | None = None
    reporting = list(_REPORTER.finditer(prefix))
    direct = list(_ATTRIBUTION.finditer(prefix))
    if direct:
        latest = direct[-1]
        # A later actor with an unsupported predicate breaks the old relation.
        if re.search(_ENTITY, prefix[latest.end() :], re.IGNORECASE) is None:
            subject = _entity(latest["subject"])
            if reporting and reporting[-1].start("subject") == latest.start("subject"):
                reporter = _entity(reporting[-1]["reporter"])
    negations = list(_NEGATION_MARKER.finditer(prefix))
    compound_assertion = (
        assertion_tail is not None
        and re.match(
            r"\s*(?:$|,|\b(?:and|or|today|yesterday|tomorrow)\b)", assertion_tail, re.IGNORECASE
        )
        is None
    )
    if _UNSUPPORTED_SCOPE.search(clause) or len(negations) > 1 or compound_assertion:
        return "uncertain", subject, reporter, ["unsupported_assertion_scope"]
    # Only a cue immediately before this mention supplies polarity; arbitrary
    # earlier clauses or facts are not propagated into a new lexical candidate.
    if re.search(rf"\b{_NEGATIVE}\s*$", prefix, re.IGNORECASE):
        return "negated", subject, reporter, []
    if negations:
        return "uncertain", subject, reporter, ["unsupported_assertion_scope"]
    if re.search(rf"\b{_POSITIVE}\s*$", prefix, re.IGNORECASE):
        return "affirmed", subject, reporter, []
    return "unknown", subject, reporter, ["polarity_not_explicit"]


def extract_case(case: object) -> D1CaseObservation:
    """Admit bounded sources, retain lexical uncertainty and verify all spans."""
    record = require_object(case, context="D1 case")
    case_id = _text(record, "case_id", identifier=True)
    if record.get("permitted_view") != VIEW:
        raise ValueError("D1 requires the synthetic-d1-extraction-only permitted view")
    order = record.get("date_order", "unknown")
    if not isinstance(order, str) or order not in ("unknown", "DMY", "MDY"):
        raise ValueError("date_order must be unknown, DMY or MDY")
    selected_order: DateOrder = "DMY" if order == "DMY" else "MDY" if order == "MDY" else "unknown"
    source_rows, sources, summaries, anchors = _admit(record, case_id)
    pending: list[tuple[_Source, _Candidate, _Interpretation, _Anchor | None, int]] = []
    evidence: list[JsonObject] = []
    for source in sorted(sources, key=lambda item: (item.source_id, item.version)):
        for candidate in _scan(source.text):
            if len(pending) == 32:
                raise ValueError("case exceeds 32 observations")
            anchor = (
                anchors.get((source.source_id, source.version))
                if candidate.kind == "relative_time"
                else None
            )
            interpreted = _interpret(
                source.text[candidate.start : candidate.end], candidate.kind, selected_order, anchor
            )
            context_start, context_end = _context_bounds(source.text, candidate)
            index = len(pending)
            evidence.extend(
                (
                    _evidence(source, f"observation-{index}", candidate.start, candidate.end),
                    _evidence(source, f"context-{index}", context_start, context_end),
                )
            )
            pending.append((source, candidate, interpreted, anchor, context_start))
    verified = (
        inspect_case({"case_id": case_id, "sources": source_rows, "evidence": evidence})
        if evidence
        else None
    )
    if verified is not None and verified["status"] != "accepted":
        raise ValueError("extraction span admission failed: " + "; ".join(verified["errors"]))
    spans = verified["spans"] if verified is not None else []
    observations: list[D1Observation] = []
    for index, (source, candidate, interpreted, anchor, context_start) in enumerate(pending):
        span, context = spans[index * 2 : index * 2 + 2]
        polarity, subject, reporter, reasons = _context_fields(
            source.text[context_start : candidate.start],
            context["text"],
            context["text"][candidate.end - context_start :]
            if candidate.kind == "assertion"
            else None,
        )
        observation: D1Observation = {
            "observation_id": fingerprint(
                [
                    case_id,
                    source.source_id,
                    source.version,
                    source.digest,
                    span["start_byte"],
                    span["end_byte"],
                    candidate.kind,
                    RULE_VERSION,
                ]
            ),
            "case_id": case_id,
            "source_id": source.source_id,
            "source_version": source.version,
            "source_sha256": source.digest,
            "coordinate_system": "utf8-byte",
            "start_byte": span["start_byte"],
            "end_byte": span["end_byte"],
            "text": span["text"],
            "kind": candidate.kind,
            "status": interpreted.status,
            "normalized": interpreted.normalized,
            "reason": interpreted.reason,
            "polarity": polarity,
            "subject": subject,
            "reporter": reporter,
            "context": context,
            "anchor": anchor.span if anchor else None,
            "timezone": None,
            "recording_time": None,
            "availability_time": None,
            "event_linkage": None,
            "context_reasons": reasons,
            "method": "deterministic-stdlib-rules",
            "rule_version": RULE_VERSION,
        }
        observations.append(observation)
    return {
        "schema_version": "faw08-d1-case-1.0",
        "case_id": case_id,
        "permitted_view": VIEW,
        "date_order": selected_order,
        "source_admission": "verified-full-source-witnesses-not-observations",
        "sources": summaries,
        "observations": observations,
        "observation_count": len(observations),
        "no_supported_observation": not observations,
    }


def verify_extraction(case: object, result: object) -> bool:
    """Check replay consistency; this is not an independent semantic verifier."""
    expected = canonical_bytes(extract_case(case))
    try:
        return canonical_bytes(result) == expected
    except (TypeError, ValueError, RecursionError, UnicodeError):
        return False


def _synthetic_cases() -> list[JsonObject]:
    texts = (
        "At 2024-02-29 00:00, pulse was 90 bpm.",
        "On 14 March at 09:30, patient received 0.50 mg.",
        "Recorded date 03/04/2024.",
        "Observation 09:30\u201310:15; pulse was 90\u2013110 bpm.",
        "Patient did not receive 5 mg; patient received 2 mg.",
        "Mother reports patient received 5 mg. Father received 2 mg.",
        "Anchor 2024-04-14 23:30. 2 hours later, dose was 1 mg.",
        "Yesterday patient had fever.",
        "Uncorrected 2O24-04-14 and 0S:30.",
        "Administrative checklist completed.",
        "Invalid 2023-02-29 and 25:00; concentration was 5 widgets.",
        "🧪 Café e\u0301\r\nPatient denies pain; if patient has fever.",
        "Interval 2024-04-14 to 2024-04-16; rate was 5 mL/h.",
    )
    cases: list[JsonObject] = []
    for index, text in enumerate(texts):
        case_id = f"d1-example-{index + 1:02}"
        source = _Source(case_id, "source-a", 1, text, _digest(text.encode("utf-8")))
        row: JsonObject = {
            "case_id": case_id,
            "permitted_view": VIEW,
            "date_order": "unknown",
            "sources": [
                {
                    "id": source.source_id,
                    "version": source.version,
                    "case_id": case_id,
                    "state": "present",
                    "content": text,
                    "fingerprint": source.digest,
                }
            ],
        }
        if index == 6:
            row["anchors"] = [_evidence(source, "selected-anchor", 7, 23)]
        cases.append(row)
    conflict = "d1-example-14"
    cases.append(
        {
            "case_id": conflict,
            "permitted_view": VIEW,
            "sources": [
                {
                    "id": sid,
                    "version": 1,
                    "case_id": conflict,
                    "state": "present",
                    "content": text,
                    "fingerprint": _digest(text.encode("utf-8")),
                }
                for sid, text in (
                    ("source-a", "Pulse was 90 bpm."),
                    ("source-b", "Pulse was 130 bpm."),
                )
            ],
        }
    )
    return cases


def generate_receipt() -> D1Receipt:
    """Bind the fixed synthetic observations to actual inputs, rules and lock."""
    inputs = _synthetic_cases()
    cases = [extract_case(case) for case in inputs]
    receipt: D1Receipt = {
        "schema_version": "faw08-d1-receipt-1.0",
        "input_schema_version": "faw08-d1-input-1.0",
        "rule_version": RULE_VERSION,
        "generator_version": "faw08-d1-generator-1.0",
        "task": "FAW08/D1",
        "dataset": "generated-synthetic-only",
        "command": "uv run --no-sync python -m tools.workbench d1-demo",
        "byte_coordinate_system": "utf8-zero-based-half-open",
        "source_hash_algorithm": "sha256",
        "inputs": inputs,
        "input_fingerprint": fingerprint(inputs),
        "permitted_view": VIEW,
        "privacy_mode": "fully_local",
        "dependency_lock_sha256": _digest((ROOT / "uv.lock").read_bytes()),
        "implementation_files": {
            path: _digest((ROOT / path).read_bytes()) for path in IMPLEMENTATION_FILES
        },
        "case_count": len(cases),
        "observation_count": sum(case["observation_count"] for case in cases),
        "cases": cases,
        "limitations": [
            "visible synthetic development inputs only; no clinical or model qualification",
            "verified byte identity does not establish source truth or independent corroboration",
            "bounded lexical grammar is not general clinical NLP or absence-of-care detection",
            "date, clock, quantity and assertion mentions do not assemble events or chronology",
            "no recording time, availability time, timezone or recipient entitlement is inferred",
            "relative expressions resolve only against explicitly selected same-source anchors",
            "replay consistency is not independent semantic validation",
            "no external source acquisition, model invocation or network",
        ],
        "output_fingerprint": "",
    }
    receipt["output_fingerprint"] = fingerprint(
        {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    )
    return receipt


def main(argv: list[str] | None = None) -> int:
    """Emit canonical UTF-8 plus one LF; argument/read/write errors are nonzero."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        payload = canonical_bytes(generate_receipt()) + b"\n"
        if sys.stdout.buffer.write(payload) != len(payload):
            raise OSError("incomplete D1 receipt write")
        sys.stdout.buffer.flush()
    except (OSError, ValueError) as exc:
        print(f"D1 receipt failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
