"""Deterministic, side-effect-free autonomy and work-queue contracts."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import PurePosixPath
from typing import Any

READY = "ready"
TERMINAL = {"complete"}
LANE_CAPS = {"integration": 1, "independent": 2}
RELEASED_STATUSES = {"waiting_external", "decision_needed", "blocked_safe", "complete"}
DECISION_REQUIRED_FIELDS = {
    "decision_id",
    "question",
    "track_and_task",
    "why_now",
    "recommended_option",
    "recommendation_rationale",
    "alternatives",
    "evidence",
    "tradeoffs_risks_uncertainty_cost",
    "reversibility",
    "safe_default",
    "paused_scope",
    "continuing_work",
    "dependency_and_schedule_impact",
    "response_format",
}


@dataclass(frozen=True)
class WorkItem:
    """Machine-readable queue item independent of Markdown checkbox state."""

    id: str
    track_id: str
    status: str
    lane: str
    priority: int
    criticality: int
    dependencies: tuple[str, ...] = ()
    owned_paths: tuple[str, ...] = ()
    blocker: str | None = None


@dataclass(frozen=True)
class Lease:
    """Exact lease observation used to classify isolation state."""

    owner: str
    run_id: str
    worktree: str
    expires_at: datetime
    heartbeat_at: datetime


def deterministic_run_id(track_id: str, task_id: str, base_revision: str) -> str:
    """Return a stable non-secret run identifier for an execution attempt."""
    value = json.dumps(
        [track_id, task_id, base_revision], separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(value.encode()).hexdigest()[:20]


def _normalise_path(value: str) -> PurePosixPath:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or ":" in value
        or any(ord(character) < 32 for character in value)
        or any(part in {"", ".", ".."} or part.endswith((".", " ")) for part in value.split("/"))
    ):
        raise ValueError("owned paths must be relative and non-escaping")
    # Conservatively share ownership across case-sensitive and insensitive clients.
    return PurePosixPath(unicodedata.normalize("NFC", value).casefold())


def paths_conflict(left: Iterable[str], right: Iterable[str]) -> bool:
    """Return whether either owned-path set contains or equals the other."""
    left_paths = [_normalise_path(value) for value in left]
    right_paths = [_normalise_path(value) for value in right]
    for first in left_paths:
        for second in right_paths:
            if first == second or first in second.parents or second in first.parents:
                return True
    return False


def select_next_ready(
    items: Iterable[WorkItem],
    *,
    completed: set[str],
    active: Iterable[WorkItem] = (),
    lane_limits: dict[str, int] | None = None,
) -> WorkItem | None:
    """Select the highest-value ready item without exceeding lanes or paths."""
    limits = LANE_CAPS if lane_limits is None else lane_limits
    if any(
        lane not in LANE_CAPS or type(limit) is not int or not 0 <= limit <= LANE_CAPS[lane]
        for lane, limit in limits.items()
    ):
        raise ValueError("lane limits must respect the integration and independent caps")
    queued_items = tuple(items)
    active_items = tuple(active)
    # Validate ownership even when there are no active peers to compare with.
    for item in (*queued_items, *active_items):
        for path in item.owned_paths:
            _normalise_path(path)
    active_ids = {item.id for item in active_items}
    lane_use: dict[str, int] = {}
    for item in active_items:
        if item.status in RELEASED_STATUSES or item.blocker:
            continue
        lane_use[item.lane] = lane_use.get(item.lane, 0) + 1

    candidates: list[WorkItem] = []
    for item in queued_items:
        if item.status != READY or item.blocker or item.id in completed or item.id in active_ids:
            continue
        if not set(item.dependencies).issubset(completed):
            continue
        if lane_use.get(item.lane, 0) >= limits.get(item.lane, 0):
            continue
        if any(paths_conflict(item.owned_paths, other.owned_paths) for other in active_items):
            continue
        candidates.append(item)
    if not candidates:
        return None
    return min(candidates, key=lambda item: (-item.criticality, -item.priority, item.id))


def classify_lease(
    lease: Lease | None,
    *,
    now: datetime | None = None,
    expected_owner: str | None = None,
    expected_worktree: str | None = None,
) -> str:
    """Classify a lease as off, held, stale, or inconsistent."""
    if lease is None:
        return "off"
    observed = now or datetime.now(UTC)
    if any(
        not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None
        for value in (observed, lease.expires_at, lease.heartbeat_at)
    ):
        raise ValueError("lease timestamps and now must be timezone-aware")
    if (
        not lease.owner
        or not lease.run_id
        or not lease.worktree
        or lease.heartbeat_at > observed
        or lease.heartbeat_at > lease.expires_at
    ):
        return "inconsistent"
    if expected_owner and lease.owner != expected_owner:
        return "inconsistent"
    if expected_worktree and lease.worktree != expected_worktree:
        return "inconsistent"
    if lease.expires_at <= observed:
        return "stale"
    return "held"


def recovery_action(kind: str, attempts: int) -> str:
    """Apply the bounded recovery contract without executing a retry."""
    if attempts < 0:
        raise ValueError("attempts cannot be negative")
    if kind == "transient":
        return "retry" if attempts < 2 else "failed_safe"
    if kind == "deterministic":
        return "repair" if attempts < 2 else "failed_safe"
    if kind == "external":
        return "blocked_external"
    if kind == "decision":
        return "decision_needed"
    if kind == "material_risk":
        return "circuit_breaker"
    raise ValueError(f"unknown recovery kind: {kind}")


def validate_decision_packet(packet: dict[str, Any]) -> list[str]:
    """Return missing or empty required decision fields."""
    return sorted(
        field
        for field in DECISION_REQUIRED_FIELDS
        if field not in packet
        or packet[field] in (None, "", [], {})
        or (isinstance(packet[field], str) and not packet[field].strip())
    )


def select_decision(packets: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    """Deduplicate open decisions and return one deterministic engagement."""
    unique: dict[str, dict[str, Any]] = {}
    for packet in packets:
        decision_id = str(packet.get("decision_id", ""))
        if not decision_id or packet.get("status") not in {"proposed", "decision_needed"}:
            continue
        unique.setdefault(decision_id, packet)
    if not unique:
        return None
    return min(unique.values(), key=lambda packet: str(packet["decision_id"]))


def freshness_status(retrieved_at: datetime, max_age: timedelta, *, now: datetime) -> str:
    """Classify authoritative context without silently accepting stale state."""
    if any(
        not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None
        for value in (retrieved_at, now)
    ):
        raise ValueError("timestamps must be timezone-aware")
    if max_age.total_seconds() < 0:
        raise ValueError("max_age cannot be negative")
    if retrieved_at > now:
        raise ValueError("retrieved_at cannot be in the future")
    return "stale" if now - retrieved_at > max_age else "current"
