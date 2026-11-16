"""Bounded explicit clock windows; no host timezone or fuzzy interpretation."""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta, timezone
from typing import Literal, TypedDict

ClockStatus = Literal["resolved", "ambiguous", "unknown", "invalid", "unsupported"]
Precision = Literal["day", "minute", "second", "range"]


class ClockWindow(TypedDict):
    local_start: str
    local_end: str
    utc_start: str | None
    utc_end: str | None
    precision: Precision
    timezone: str | None


class ClockInterpretation(TypedDict):
    status: ClockStatus
    reason: str | None
    windows: list[ClockWindow]


_STAMP = re.compile(
    r"(?P<day>[0-9]{4}-[0-9]{2}-[0-9]{2})"
    r"(?:[T ](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})(?::(?P<second>[0-9]{2}))?)?"
    r"(?P<zone>Z|[+-][0-9]{2}:[0-9]{2}| [A-Za-z_]+(?:/[A-Za-z0-9_+\-]+)+)?"
)


def _result(
    status: ClockStatus, reason: str | None, windows: list[ClockWindow] | None = None
) -> ClockInterpretation:
    return {"status": status, "reason": reason, "windows": windows or []}


def _local(value: datetime) -> str:
    return value.replace(tzinfo=None).isoformat(timespec="seconds")


def _utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _stamp(text: str) -> ClockInterpretation:
    match = _STAMP.fullmatch(text)
    if match is None:
        return _result("unsupported", "unsupported_clock_expression")
    hour, minute, second = match.group("hour", "minute", "second")
    precision: Precision = "day" if hour is None else "minute" if second is None else "second"
    try:
        start = datetime.fromisoformat(match.group("day")).replace(
            hour=int(hour or "0"), minute=int(minute or "0"), second=int(second or "0")
        )
        end = start.replace(hour=23, minute=59, second=59) if precision == "day" else start
        if precision == "minute":
            end = start.replace(second=59)
    except ValueError:
        return _result("invalid", "invalid_calendar_or_time")
    raw_zone = match.group("zone")
    zone = raw_zone.strip() if raw_zone is not None else None
    window: ClockWindow = {
        "local_start": _local(start),
        "local_end": _local(end),
        "utc_start": None,
        "utc_end": None,
        "precision": precision,
        "timezone": zone,
    }
    if zone is None:
        return _result("unknown", "timezone_unknown", [window])
    if "/" in zone:
        return _result("unknown", "named_timezone_unresolved", [window])
    if zone == "-00:00":
        return _result("unknown", "offset_unknown", [window])
    minutes = 0
    if zone != "Z":
        hours, remainder = int(zone[1:3]), int(zone[4:6])
        if hours > 14 or remainder > 59 or (hours == 14 and remainder):
            return _result("invalid", "invalid_offset", [window])
        minutes = (hours * 60 + remainder) * (-1 if zone[0] == "-" else 1)
    offset = timezone(timedelta(minutes=minutes))
    try:
        window["utc_start"] = _utc(start.replace(tzinfo=offset))
        window["utc_end"] = _utc(end.replace(tzinfo=offset))
    except OverflowError:
        # Do not retain a partially converted window at a calendar boundary.
        window["utc_start"] = None
        window["utc_end"] = None
        return _result("invalid", "utc_out_of_range", [window])
    return _result("resolved", None, [window])


def _range(text: str) -> ClockInterpretation:
    if text == "unknown":
        return _result("unknown", "explicit_unknown")
    parts = text.split(" to ")
    if len(parts) == 1:
        return _stamp(text)
    if len(parts) != 2:
        return _result("unsupported", "unsupported_clock_expression")
    first, last = (_stamp(part) for part in parts)
    if first["status"] in ("invalid", "unsupported"):
        return first
    if last["status"] in ("invalid", "unsupported"):
        return last
    left, right = first["windows"][0], last["windows"][0]
    utc_start, utc_end = left["utc_start"], right["utc_end"]
    if utc_start is not None and utc_end is not None:
        reversed_range = utc_start > utc_end
    elif utc_start is None and utc_end is None and left["timezone"] == right["timezone"]:
        reversed_range = left["local_start"] > right["local_end"]
    else:
        return _result("unsupported", "incompatible_range_timezones")
    if reversed_range:
        return _result("invalid", "reversed_range")
    window: ClockWindow = {
        "local_start": left["local_start"],
        "local_end": right["local_end"],
        "utc_start": utc_start,
        "utc_end": utc_end,
        "precision": "range",
        "timezone": left["timezone"]
        if left["timezone"] == right["timezone"]
        else f"{left['timezone']} to {right['timezone']}",
    }
    return _result("resolved" if utc_start is not None else "unknown", first["reason"], [window])


def interpret_clock(text: str) -> ClockInterpretation:
    """Preserve all alternatives; unresolved components cannot supply UTC order."""
    if len(text) > 512:
        raise ValueError("clock expression exceeds 512 bytes")
    try:
        if len(text.encode("utf-8")) > 512:
            raise ValueError("clock expression exceeds 512 bytes")
    except UnicodeEncodeError as exc:
        raise ValueError("clock expression must be UTF-8 encodable") from exc
    if text == "unknown":
        return _result("unknown", "explicit_unknown")
    alternatives = text.split(" or ")
    if len(alternatives) > 4:
        return _result("unsupported", "alternative_limit")
    interpreted = [_range(part) for part in alternatives]
    windows = [window for item in interpreted for window in item["windows"]]
    for status in ("invalid", "unsupported", "unknown"):
        for item in interpreted:
            if item["status"] == status:
                return _result(item["status"], item["reason"], windows)
    return _result("ambiguous" if len(alternatives) > 1 else "resolved", None, windows)
