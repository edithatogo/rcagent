from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path, PureWindowsPath

import pytest

from tools.autonomy_harness import deterministic_run_id
from tools.autonomy_state import StateStore, next_action

REVISION = "a" * 40


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    result = StateStore(tmp_path / "checkpoint.json")
    result.initialise(
        [
            {"id": "first", "phases": ["phase1", "phase2"]},
            {"id": "dependent", "phases": ["only"], "dependencies": ["first"]},
            {"id": "independent", "phases": ["only"]},
        ],
        base_revision=REVISION,
    )
    return result


def receipt(
    root: Path, instruction: dict[str, str] | None, outcome: str, name: str = "receipt.json"
) -> str:
    assert instruction is not None
    evidence = root / "synthetic-result.txt"
    evidence.write_text("Synthetic fixture result; not actual execution.\n")
    value = dict(
        instruction,
        outcome=outcome,
        artefacts=[
            {
                "path": evidence.name,
                "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
            }
        ],
    )
    (root / name).write_text(json.dumps(value))
    return name


def advance(store: StateStore, action: str = "pass") -> dict:
    state = store.load()
    instruction = next_action(state)
    assert instruction is not None
    event_id = f"event-{len(state['events'])}"
    path = receipt(store.path.parent, instruction, action, f"{event_id}.json")
    return store.advance(root=store.path.parent, event_id=event_id, action=action, receipt=path)


def ready_action(state: dict) -> dict[str, str]:
    instruction = next_action(state)
    assert instruction is not None
    return instruction


def test_phase_review_sync_and_next_track_dispatch(store: StateStore) -> None:
    assert ready_action(store.load())["phase_id"] == "phase1"
    assert ready_action(advance(store))["phase_id"] == "phase2"
    assert ready_action(advance(store))["stage"] == "review"
    assert ready_action(advance(store))["stage"] == "sync"
    state = advance(store)
    assert state["tracks"][0]["stage"] == "complete"
    assert ready_action(state)["track_id"] == "dependent"
    for _ in range(6):
        state = advance(store)
    assert next_action(state) is None


def test_review_findings_dispatch_bounded_rework(store: StateStore) -> None:
    advance(store)
    advance(store)
    assert ready_action(advance(store, "fail"))["stage"] == "rework"
    assert ready_action(advance(store))["stage"] == "review"
    advance(store, "fail")
    advance(store)
    state = advance(store, "fail")
    assert state["tracks"][0]["stage"] == "blocked_safe"
    assert ready_action(state)["track_id"] == "independent"


@pytest.mark.parametrize("action", ["waiting_external", "decision_needed"])
def test_wait_releases_dispatch_and_requires_evidence_to_resume(
    store: StateStore, action: str
) -> None:
    state = store.advance(
        root=store.path.parent,
        event_id="wait",
        action=action,
        wake_condition="verified evidence arrives",
    )
    assert ready_action(state)["track_id"] == "independent"
    expected = {
        "track_id": "first",
        "phase_id": "phase1",
        "stage": action,
        "base_revision": REVISION,
        "run_id": deterministic_run_id("first", "phase1", REVISION),
    }
    path = receipt(store.path.parent, expected, "resume")
    resumed = store.resume(root=store.path.parent, track_id="first", event_id="wake", receipt=path)
    assert ready_action(resumed)["track_id"] == "first"
    assert (
        store.resume(root=store.path.parent, track_id="first", event_id="wake", receipt=path)
        == resumed
    )


def test_resume_after_interruption_and_idempotent_event(store: StateStore) -> None:
    expected = next_action(store.load())
    path = receipt(store.path.parent, expected, "pass")
    state = store.advance(root=store.path.parent, event_id="once", action="pass", receipt=path)
    reopened = StateStore(store.path)
    assert reopened.load() == state
    assert (
        reopened.advance(root=store.path.parent, event_id="once", action="pass", receipt=path)
        == state
    )
    assert len(reopened.load()["events"]) == 1
    with pytest.raises(ValueError, match="reused"):
        reopened.advance(root=store.path.parent, event_id="once", action="fail", receipt=path)


def test_failed_atomic_write_preserves_last_checkpoint(store: StateStore, monkeypatch) -> None:
    before = store.path.read_bytes()

    def interrupted(*args):
        raise OSError("simulated interruption before replace")

    monkeypatch.setattr("tools.autonomy_state.os.replace", interrupted)
    with pytest.raises(OSError, match="interruption"):
        advance(store)
    assert store.path.read_bytes() == before
    assert not store.lock.exists()


def test_stale_or_active_lock_is_never_stolen(store: StateStore) -> None:
    store.lock.write_text("retained stale owner token")
    before = store.path.read_bytes()
    with pytest.raises(FileExistsError):
        advance(store)
    assert store.lock.read_text() == "retained stale owner token"
    assert store.path.read_bytes() == before


def test_initialise_never_overwrites_checkpoint(store: StateStore) -> None:
    before = store.path.read_bytes()
    with pytest.raises(FileExistsError):
        store.initialise([{"id": "replacement", "phases": ["one"]}], base_revision=REVISION)
    assert store.path.read_bytes() == before


def test_circuit_breaker_persists_and_cannot_resume(store: StateStore) -> None:
    state = store.advance(
        root=store.path.parent,
        event_id="risk",
        action="circuit_breaker",
        wake_condition="governed risk reconciliation",
    )
    assert next_action(state) is None
    assert next_action(StateStore(store.path).load()) is None
    with pytest.raises(ValueError, match="circuit breaker"):
        store.resume(
            root=store.path.parent, track_id="first", event_id="wake", receipt="missing.json"
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("base_revision", "b" * 40),
        ("stage", "review"),
        ("track_id", "other"),
        ("run_id", "fake"),
        ("outcome", "fail"),
        ("artefacts", []),
    ],
)
def test_completion_requires_exact_bound_receipt(store: StateStore, field: str, value) -> None:
    path = receipt(store.path.parent, next_action(store.load()), "pass")
    receipt_path = store.path.parent / path
    data = json.loads(receipt_path.read_text())
    data[field] = value
    receipt_path.write_text(json.dumps(data))
    before = store.path.read_bytes()
    with pytest.raises(ValueError):
        store.advance(root=store.path.parent, event_id="bad", action="pass", receipt=path)
    assert store.path.read_bytes() == before


def test_evidence_tampering_rejects_completion_and_replay(store: StateStore) -> None:
    path = receipt(store.path.parent, next_action(store.load()), "pass")
    state = store.advance(root=store.path.parent, event_id="once", action="pass", receipt=path)
    (store.path.parent / "synthetic-result.txt").write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        store.advance(root=store.path.parent, event_id="once", action="pass", receipt=path)
    assert store.load() == state


def test_missing_receipt_and_wake_condition_fail_closed(store: StateStore) -> None:
    with pytest.raises(ValueError, match="bound receipt"):
        store.advance(root=store.path.parent, event_id="none", action="pass")
    with pytest.raises(ValueError, match="wake condition"):
        store.advance(root=store.path.parent, event_id="none", action="waiting_external")


def test_checkpoint_tampering_fails_closed(store: StateStore) -> None:
    state = json.loads(store.path.read_text())
    state["tracks"][0]["stage"] = "complete"
    store.path.write_text(json.dumps(state))
    with pytest.raises(ValueError, match="integrity"):
        store.load()


@pytest.mark.parametrize(
    "plan",
    [
        [],
        [{"id": "x", "phases": []}],
        [{"id": "x", "phases": ["one"], "dependencies": ["x"]}],
        [{"id": "x", "phases": ["one"], "dependencies": ["missing"]}],
    ],
)
def test_invalid_plan_fails_closed(tmp_path: Path, plan) -> None:
    with pytest.raises(ValueError):
        StateStore(tmp_path / "state.json").initialise(plan, base_revision=REVISION)


@pytest.mark.parametrize("wait_stage", ["waiting_external", "decision_needed"])
def test_wait_during_rework_preserves_original_stage(store: StateStore, wait_stage: str) -> None:
    advance(store)
    advance(store)
    advance(store, "fail")
    state = store.advance(
        root=store.path.parent, event_id="wait", action=wait_stage, wake_condition="new evidence"
    )
    expected = {
        "track_id": "first",
        "phase_id": "phase2",
        "stage": wait_stage,
        "base_revision": REVISION,
        "run_id": deterministic_run_id("first", "phase2", REVISION),
    }
    path = receipt(store.path.parent, expected, "resume", "resume.json")
    state = store.resume(root=store.path.parent, track_id="first", event_id="resume", receipt=path)
    assert ready_action(state)["stage"] == "rework"
    assert ready_action(advance(store))["stage"] == "review"


@pytest.mark.parametrize(
    "name", ["../outside.json", "/outside.json", "C:outside.json", "directory\\receipt.json"]
)
def test_unsafe_receipt_path_rejected(store: StateStore, name: str) -> None:
    before = store.path.read_bytes()
    with pytest.raises(ValueError, match="relative"):
        store.advance(root=store.path.parent, event_id="unsafe", action="pass", receipt=name)
    assert store.path.read_bytes() == before


def test_windows_rooted_receipt_path_is_rejected_on_any_host(tmp_path: Path, monkeypatch) -> None:
    from tools import autonomy_state

    assert not PureWindowsPath("/outside.json").is_absolute()
    monkeypatch.setattr(autonomy_state, "Path", PureWindowsPath)
    with pytest.raises(ValueError, match="relative and non-escaping"):
        autonomy_state._relative_file(tmp_path, "/outside.json")


def test_symlinked_receipt_rejected(store: StateStore) -> None:
    path = receipt(store.path.parent, next_action(store.load()), "pass")
    link = store.path.parent / "linked.json"
    link.symlink_to(path)
    with pytest.raises(ValueError, match="symlink"):
        store.advance(root=store.path.parent, event_id="unsafe", action="pass", receipt=link.name)


def test_wait_rejects_unused_receipt(store: StateStore) -> None:
    with pytest.raises(ValueError, match="unverified receipt"):
        store.advance(
            root=store.path.parent,
            event_id="wait",
            action="waiting_external",
            receipt="missing.json",
            wake_condition="evidence",
        )


@pytest.mark.parametrize(
    "plan,revision",
    [("plan", REVISION), (None, REVISION), ([{"id": "first", "phases": ["one"]}], None)],
)
def test_malformed_initialisation_is_value_error(tmp_path: Path, plan, revision) -> None:
    with pytest.raises(ValueError):
        StateStore(tmp_path / "state.json").initialise(plan, base_revision=revision)


def recovery_receipt(store: StateStore) -> str:
    lease = json.loads(store.lock.read_text())
    artefacts = []
    for role in ("branch", "diff", "log"):
        path = store.path.parent / f"{role}.txt"
        path.write_text(f"Synthetic {role} preservation fixture\n")
        artefacts.append(
            {
                "path": path.name,
                "role": role,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    value = {
        "outcome": "recover",
        "base_revision": REVISION,
        "owner": lease["owner"],
        "run_id": lease["run_id"],
        "worktree": lease["worktree"],
        "checkpoint_sha256": hashlib.sha256(store.path.read_bytes()).hexdigest(),
        "lock_sha256": hashlib.sha256(store.lock.read_bytes()).hexdigest(),
        "artefacts": artefacts,
    }
    path = store.path.parent / "recovery-receipt.json"
    path.write_text(json.dumps(value))
    return path.name


def stale_lock(store: StateStore) -> None:
    now = datetime.now(UTC)
    store.lock.write_text(
        json.dumps(
            {
                "protocol": "checkpoint-lease-v1",
                "token": "expired",
                "owner": "prior-owner",
                "run_id": "prior-run",
                "worktree": str(store.path.parent.resolve()),
                "heartbeat_at": (now - timedelta(minutes=10)).isoformat(),
                "expires_at": (now - timedelta(minutes=5)).isoformat(),
            }
        )
    )


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
def test_expired_inactive_lock_recovery_preserves_bound_work(store: StateStore) -> None:
    stale_lock(store)
    path = recovery_receipt(store)
    checkpoint = store.path.read_bytes()
    lock = store.lock.read_bytes()
    preserved = store.recover(root=store.path.parent, receipt=path)
    assert (preserved / "checkpoint.json").read_bytes() == checkpoint
    assert (preserved / "lock.json").read_bytes() == lock
    assert (preserved / "receipt.json").read_bytes() == (store.path.parent / path).read_bytes()
    assert len(list(preserved.glob("artefact-*.bin"))) == 3
    assert not store.lock.exists()
    assert store.path.read_bytes() == checkpoint
    assert ready_action(advance(store))["phase_id"] == "phase2"


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
def test_expired_active_writer_cannot_be_recovered(store: StateStore) -> None:
    with store._locked():
        lease = json.loads(store.lock.read_text())
        lease["heartbeat_at"] = (datetime.now(UTC) - timedelta(minutes=10)).isoformat()
        lease["expires_at"] = (datetime.now(UTC) - timedelta(minutes=5)).isoformat()
        store.lock.write_text(json.dumps(lease))
        path = recovery_receipt(store)
        with pytest.raises(BlockingIOError):
            store.recover(root=store.path.parent, receipt=path)
        assert store.lock.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
def test_recovery_rejects_replaced_lock_and_keeps_snapshot(store: StateStore, monkeypatch) -> None:
    from tools import autonomy_state

    stale_lock(store)
    path = recovery_receipt(store)
    original_read = autonomy_state._read_receipt

    def replace_owner(*args):
        result = original_read(*args)
        store.lock.unlink()
        store.lock.write_text("new owner")
        return result

    monkeypatch.setattr(autonomy_state, "_read_receipt", replace_owner)
    with pytest.raises(ValueError, match="owner or checkpoint changed"):
        store.recover(root=store.path.parent, receipt=path)
    assert store.lock.read_text() == "new owner"
    assert len(list(store.path.parent.glob("checkpoint.json.recovery-*"))) == 1


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
def test_recovery_rejects_missing_preservation_evidence(store: StateStore) -> None:
    stale_lock(store)
    path = recovery_receipt(store)
    value = json.loads((store.path.parent / path).read_text())
    value["artefacts"].pop()
    (store.path.parent / path).write_text(json.dumps(value))
    with pytest.raises(ValueError, match="branch, diff and log"):
        store.recover(root=store.path.parent, receipt=path)
    assert store.lock.exists()


def test_lease_records_owner_run_worktree_and_heartbeat(store: StateStore) -> None:
    with store._locked():
        lease = json.loads(store.lock.read_text())
        assert lease["owner"] and lease["run_id"]
        assert lease["worktree"] == str(store.path.parent.resolve())
        assert datetime.fromisoformat(lease["heartbeat_at"]) < datetime.fromisoformat(
            lease["expires_at"]
        )


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
@pytest.mark.parametrize(
    "raw",
    ["x" * 65537, "[]", "{}", "not-json"],
    ids=["oversized", "array", "empty-object", "invalid-json"],
)
def test_recovery_rejects_malformed_lock_metadata(store: StateStore, raw: str) -> None:
    store.lock.write_text(raw)
    with pytest.raises(ValueError):
        store.recover(root=store.path.parent, receipt="missing.json")
    assert store.lock.read_text() == raw


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
@pytest.mark.parametrize(
    "field,value",
    [
        ("heartbeat_at", "2026-01-01T00:00:00"),
        ("expires_at", "2026-01-01T00:00:00"),
        ("expires_at", "2099-01-01T00:00:00+00:00"),
        ("heartbeat_at", "2099-01-01T00:00:00+00:00"),
        ("worktree", "/different-worktree"),
        ("owner", ""),
    ],
)
def test_recovery_rejects_inconsistent_lease(store: StateStore, field: str, value: str) -> None:
    stale_lock(store)
    lease = json.loads(store.lock.read_text())
    lease[field] = value
    store.lock.write_text(json.dumps(lease))
    with pytest.raises(ValueError):
        store.recover(root=store.path.parent, receipt="missing.json")
    assert store.lock.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX advisory recovery contract")
@pytest.mark.parametrize(
    "changed_file,error",
    [("recovery-receipt.json", "receipt changed"), ("branch.txt", "evidence changed")],
)
def test_recovery_rechecks_evidence_before_preservation(
    store: StateStore, monkeypatch, changed_file: str, error: str
) -> None:
    from tools import autonomy_state

    stale_lock(store)
    path = recovery_receipt(store)
    original_read = autonomy_state._read_receipt

    def change_evidence(*args):
        result = original_read(*args)
        (store.path.parent / changed_file).write_text("changed after validation")
        return result

    monkeypatch.setattr(autonomy_state, "_read_receipt", change_evidence)
    with pytest.raises(ValueError, match=error):
        store.recover(root=store.path.parent, receipt=path)
    assert store.lock.exists()


@pytest.mark.parametrize("contents", [None, "invalid-json", "[]"])
def test_writer_cleanup_does_not_remove_changed_lock(
    store: StateStore, contents: str | None
) -> None:
    with store._locked():
        if contents is None:
            if os.name == "nt":
                with pytest.raises(PermissionError):
                    store.lock.unlink()
            else:
                store.lock.unlink()
        else:
            store.lock.write_text(contents)
    if contents is not None:
        assert store.lock.read_text() == contents
    else:
        assert not store.lock.exists()


@pytest.mark.parametrize(
    "artefacts",
    [
        ["invalid"],
        [{"path": "receipt.json", "sha256": "0" * 64}],
        [{"path": "", "sha256": "0" * 64}],
        [{"path": "absent.txt", "sha256": "0" * 64}],
    ],
)
def test_receipt_artefacts_reject_malformed_and_self_reference(
    store: StateStore, artefacts
) -> None:
    path = receipt(store.path.parent, next_action(store.load()), "pass")
    value = json.loads((store.path.parent / path).read_text())
    value["artefacts"] = artefacts
    (store.path.parent / path).write_text(json.dumps(value))
    with pytest.raises(ValueError):
        store.advance(root=store.path.parent, event_id="bad", action="pass", receipt=path)


def test_non_object_checkpoint_rejected(store: StateStore) -> None:
    store.path.write_text("[]")
    with pytest.raises(ValueError, match="invalid checkpoint"):
        store.load()


def test_symlink_checkpoint_cannot_be_loaded_or_overwritten(store: StateStore) -> None:
    link = store.path.parent / "linked-state.json"
    link.symlink_to(store.path.name)
    linked_store = StateStore(link)
    before = store.path.read_bytes()
    with pytest.raises(ValueError, match="symlink"):
        linked_store.load()
    with pytest.raises(ValueError, match="symlink"):
        linked_store._save(store.load())
    assert store.path.read_bytes() == before
