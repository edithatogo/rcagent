from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from tools.autonomy_harness import (
    DECISION_REQUIRED_FIELDS,
    Lease,
    WorkItem,
    classify_lease,
    deterministic_run_id,
    freshness_status,
    paths_conflict,
    recovery_action,
    select_decision,
    select_next_ready,
    validate_decision_packet,
)


def item(
    item_id: str,
    *,
    status: str = "ready",
    lane: str = "independent",
    priority: int = 1,
    criticality: int = 1,
    dependencies: tuple[str, ...] = (),
    owned_paths: tuple[str, ...] | None = None,
    blocker: str | None = None,
) -> WorkItem:
    return WorkItem(
        id=item_id,
        track_id="track-01",
        status=status,
        lane=lane,
        priority=priority,
        criticality=criticality,
        dependencies=dependencies,
        owned_paths=owned_paths or (f"src/{item_id}",),
        blocker=blocker,
    )


def test_run_id_is_stable_and_revision_bound() -> None:
    first = deterministic_run_id("track", "task", "abc")
    assert first == deterministic_run_id("track", "task", "abc")
    assert first != deterministic_run_id("track", "task", "def")


def test_selection_uses_evidence_state_dependencies_and_priority() -> None:
    items = [
        item("blocked", criticality=9, blocker="credential"),
        item("dependency", criticality=8, dependencies=("missing",)),
        item("low", priority=2),
        item("critical", criticality=2),
    ]
    assert select_next_ready(items, completed=set()) == items[-1]


def test_selection_respects_lane_and_owned_path_conflicts() -> None:
    active = [item("active", status="active", owned_paths=("src/shared",))]
    conflict = item("conflict", criticality=3, owned_paths=("src/shared/file.py",))
    independent = item("free", criticality=2, owned_paths=("docs/free.md",))
    assert select_next_ready([conflict, independent], completed=set(), active=active) == independent
    assert select_next_ready(
        [independent], completed=set(), active=active, lane_limits={"independent": 1}
    ) is None


def test_path_validation_rejects_escape() -> None:
    assert paths_conflict(["src"], ["src/file.py"])
    with pytest.raises(ValueError, match="non-escaping"):
        paths_conflict(["../secret"], ["src"])


def test_lease_states_fail_closed() -> None:
    now = datetime(2026, 8, 29, tzinfo=UTC)
    held = Lease("owner", "run", "/tmp/worktree", now + timedelta(minutes=5), now)
    stale = Lease("owner", "run", "/tmp/worktree", now, now - timedelta(minutes=5))
    assert classify_lease(None, now=now) == "off"
    assert classify_lease(held, now=now, expected_owner="owner") == "held"
    assert classify_lease(stale, now=now) == "stale"
    assert classify_lease(held, now=now, expected_owner="other") == "inconsistent"
    with pytest.raises(ValueError, match="timezone-aware"):
        classify_lease(held, now=datetime(2026, 8, 29))


@pytest.mark.parametrize(
    ("kind", "attempts", "expected"),
    [
        ("transient", 0, "retry"),
        ("transient", 2, "failed_safe"),
        ("deterministic", 1, "repair"),
        ("deterministic", 2, "failed_safe"),
        ("external", 0, "blocked_external"),
        ("decision", 0, "decision_needed"),
        ("material_risk", 0, "circuit_breaker"),
    ],
)
def test_recovery_is_bounded(kind: str, attempts: int, expected: str) -> None:
    assert recovery_action(kind, attempts) == expected


def test_decision_packet_contract() -> None:
    packet = {field: "recorded" for field in DECISION_REQUIRED_FIELDS}
    assert validate_decision_packet(packet) == []
    packet["safe_default"] = ""
    assert validate_decision_packet(packet) == ["safe_default"]


def test_decision_engagement_is_deduplicated_and_one_at_a_time() -> None:
    packets = [
        {"decision_id": "B", "status": "decision_needed", "wake_condition": "owner response"},
        {"decision_id": "A", "status": "proposed", "wake_condition": "owner response"},
        {"decision_id": "A", "status": "proposed", "wake_condition": "duplicate"},
        {"decision_id": "C", "status": "complete"},
    ]
    assert select_decision(packets) == packets[1]


def test_freshness_fails_closed() -> None:
    now = datetime(2026, 8, 29, tzinfo=UTC)
    assert freshness_status(now - timedelta(days=1), timedelta(days=2), now=now) == "current"
    assert freshness_status(now - timedelta(days=3), timedelta(days=2), now=now) == "stale"
    with pytest.raises(ValueError, match="timezone-aware"):
        freshness_status(datetime(2026, 8, 28), timedelta(days=2), now=now)
