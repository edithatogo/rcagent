"""Local checkpoint coordinator; never executes work or grants external authority.

Receipts bind reported outcomes to exact local artefact bytes. They do not
independently attest that tests ran, a reviewer agreed, or an authority approved.
The caller must reconcile those claims before supplying a receipt.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import NotRequired, TypedDict, TypeGuard

from tools.autonomy_harness import deterministic_run_id
from tools.json_shapes import is_array, is_object


class TrackState(TypedDict):
    id: str
    phases: list[str]
    dependencies: list[str]
    phase_index: int
    stage: str
    repairs: int
    wait_resume_stage: NotRequired[str]
    wake_condition: NotRequired[str | None]
    resume_stage: NotRequired[str]


class StateEvent(TypedDict):
    id: str
    request: dict[str, str | None]
    instruction: dict[str, str]
    receipt_sha256: str | None
    timestamp: str


class CheckpointState(TypedDict):
    schema_version: str
    base_revision: str
    tracks: list[TrackState]
    events: list[StateEvent]
    circuit_breaker: bool


class _CheckpointLease(TypedDict):
    protocol: str
    token: str
    owner: str
    run_id: str
    worktree: str
    heartbeat_at: str
    expires_at: str


class _RecoveryArtefact(TypedDict):
    path: str
    sha256: str
    role: str


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _text(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object) -> TypeGuard[list[str]]:
    return is_array(value) and all(_text(item) for item in value)


def _string_map(value: object) -> TypeGuard[dict[str, str]]:
    return is_object(value) and all(isinstance(item, str) for item in value.values())


def _is_track(value: object) -> TypeGuard[TrackState]:
    if not is_object(value):
        return False
    phases, index, repairs = value.get("phases"), value.get("phase_index"), value.get("repairs")
    if (
        not _text(value.get("id"))
        or not _texts(phases)
        or not phases
        or not _texts(value.get("dependencies"))
        or type(index) is not int
        or not 0 <= index < len(phases)
        or type(repairs) is not int
        or repairs < 0
        or not _text(value.get("stage"))
    ):
        return False
    for field in ("wait_resume_stage", "resume_stage"):
        if field in value and not _text(value[field]):
            return False
    if (
        "wake_condition" in value
        and value["wake_condition"] is not None
        and not _text(value["wake_condition"])
    ):
        return False
    if value["stage"] == "rework" and "resume_stage" not in value:
        return False
    return not (
        value["stage"] in ("waiting_external", "decision_needed")
        and ("wait_resume_stage" not in value or "wake_condition" not in value)
    )


def _is_event(value: object) -> TypeGuard[StateEvent]:
    if not is_object(value):
        return False
    request = value.get("request")
    return (
        _text(value.get("id"))
        and is_object(request)
        and all(item is None or isinstance(item, str) for item in request.values())
        and _string_map(value.get("instruction"))
        and "receipt_sha256" in value
        and (value["receipt_sha256"] is None or isinstance(value["receipt_sha256"], str))
        and _text(value.get("timestamp"))
    )


def _is_checkpoint(value: object) -> TypeGuard[CheckpointState]:
    if not is_object(value):
        return False
    tracks, events = value.get("tracks"), value.get("events")
    return (
        isinstance(value.get("schema_version"), str)
        and _text(value.get("base_revision"))
        and isinstance(value.get("circuit_breaker"), bool)
        and is_array(tracks)
        and all(_is_track(track) for track in tracks)
        and is_array(events)
        and all(_is_event(event) for event in events)
    )


def _is_lease(value: object) -> TypeGuard[_CheckpointLease]:
    return (
        is_object(value)
        and value.get("protocol") == "checkpoint-lease-v1"
        and all(
            _text(value.get(field))
            for field in ("token", "owner", "run_id", "worktree", "heartbeat_at", "expires_at")
        )
    )


def _is_recovery_artefact(value: object) -> TypeGuard[_RecoveryArtefact]:
    return is_object(value) and all(
        isinstance(value.get(field), str) for field in ("path", "sha256", "role")
    )


def confined_file(root: Path, name: object) -> Path:
    """Resolve an existing evidence file inside the root without symlink traversal."""
    if not _text(name):
        raise ValueError("evidence path must be a non-empty relative path")
    path = Path(name)
    if path.anchor or ".." in path.parts or "\\" in name or ":" in name:
        raise ValueError("evidence path must be relative and non-escaping")
    candidate = root
    for component in path.parts:
        candidate = candidate / component
        if candidate.is_symlink():
            raise ValueError("evidence paths cannot contain symlinks")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("evidence must be an existing repository file")
    return resolved


def read_bound_receipt(root: Path, name: str, expected: Mapping[str, str], outcome: str) -> str:
    """Check exact transition bindings and artefact bytes, then return the receipt hash."""
    path = confined_file(root, name)
    raw = path.read_bytes()
    receipt: object = json.loads(raw)
    if not is_object(receipt) or any(receipt.get(k) != v for k, v in expected.items()):
        raise ValueError("receipt does not match the exact run, revision, track, phase and stage")
    if receipt.get("outcome") != outcome:
        raise ValueError("receipt outcome does not match the transition")
    artefacts = receipt.get("artefacts")
    if not is_array(artefacts) or not artefacts:
        raise ValueError("receipt requires non-empty artefact evidence")
    seen: set[str] = set()
    for artefact in artefacts:
        if not is_object(artefact):
            raise ValueError("invalid artefact evidence")
        evidence = confined_file(root, artefact.get("path"))
        identity = str(evidence)
        if identity in seen or evidence == path:
            raise ValueError("duplicate or self-referential artefact evidence")
        seen.add(identity)
        data = evidence.read_bytes()
        if not data or hashlib.sha256(data).hexdigest() != artefact.get("sha256"):
            raise ValueError("artefact hash mismatch or empty evidence")
    return hashlib.sha256(raw).hexdigest()


def next_action(state: CheckpointState) -> dict[str, str] | None:
    """Return the next local instruction; blocked lanes consume no dispatch slot."""
    if state["circuit_breaker"]:
        return None
    completed = {track["id"] for track in state["tracks"] if track["stage"] == "complete"}
    for track in state["tracks"]:
        if track["stage"] in {"complete", "waiting_external", "decision_needed", "blocked_safe"}:
            continue
        if not set(track["dependencies"]).issubset(completed):
            continue
        phase = track["phases"][track["phase_index"]]
        return {
            "track_id": track["id"],
            "phase_id": phase,
            "stage": track["stage"],
            "base_revision": state["base_revision"],
            "run_id": deterministic_run_id(track["id"], phase, state["base_revision"]),
        }
    return None


class StateStore:
    """Atomic, recoverable JSON checkpoints with an exclusive local writer lock.

    Recovery requires an expired lease, exclusive advisory ownership and
    preservation of receipt-bound work. Process IDs never prove inactivity.
    """

    def __init__(self, path: Path) -> None:
        self.path = path.absolute()
        self.lock = self.path.with_name(self.path.name + ".lock")

    @contextmanager
    def _locked(self) -> Generator[None, None, None]:
        token = uuid.uuid4().hex
        fd = os.open(self.lock, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            if os.name == "posix":
                import fcntl

                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            now = datetime.now(UTC)
            lease = {
                "protocol": "checkpoint-lease-v1",
                "token": token,
                "owner": f"local-process-{os.getpid()}",
                "run_id": token,
                "worktree": str(self.path.parent.resolve()),
                "heartbeat_at": now.isoformat(),
                "expires_at": (now + timedelta(minutes=5)).isoformat(),
            }
            os.write(fd, json.dumps(lease, sort_keys=True).encode())
            os.fsync(fd)
            yield
        finally:
            owned_stat = os.fstat(fd)
            if os.name != "posix":
                os.close(fd)
            try:
                observed: object = (
                    json.loads(self.lock.read_text()) if not self.lock.is_symlink() else None
                )
                if (
                    is_object(observed)
                    and self.lock.stat().st_ino == owned_stat.st_ino
                    and observed.get("token") == token
                ):
                    self.lock.unlink()
            except (FileNotFoundError, ValueError):
                pass
            finally:
                if os.name == "posix":
                    os.close(fd)

    def recover(self, *, root: Path, receipt: str) -> Path:
        """Preserve an inactive expired lock and bound work before releasing it.

        POSIX advisory ownership proves no cooperating checkpoint writer holds
        this lock. Receipt branch/diff/log claims remain the caller's evidence.
        Other platforms require separately governed recovery.
        """
        if os.name != "posix":
            raise ValueError("automatic lock recovery is unsupported on this platform")
        import fcntl

        root = root.resolve()
        fd = os.open(self.lock, os.O_RDWR | os.O_NOFOLLOW)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_stat = os.fstat(fd)
            raw_lock = os.read(fd, 65537)
            if len(raw_lock) > 65536:
                raise ValueError("invalid lock metadata")
            lease: object = json.loads(raw_lock)
            if not _is_lease(lease):
                raise ValueError("invalid lock metadata")
            heartbeat = datetime.fromisoformat(lease["heartbeat_at"])
            expires = datetime.fromisoformat(lease["expires_at"])
            if (
                heartbeat.tzinfo is None
                or expires.tzinfo is None
                or heartbeat > expires
                or expires > datetime.now(UTC)
                or lease["worktree"] != str(self.path.parent.resolve())
            ):
                raise ValueError("lock is not an expired consistent lease")
            state = self.load()
            checkpoint_bytes = self.path.read_bytes()
            expected = {
                "base_revision": state["base_revision"],
                "lock_sha256": hashlib.sha256(raw_lock).hexdigest(),
                "checkpoint_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
                "owner": lease["owner"],
                "run_id": lease["run_id"],
                "worktree": lease["worktree"],
            }
            receipt_path = confined_file(root, receipt)
            receipt_hash = read_bound_receipt(root, receipt, expected, "recover")
            receipt_bytes = receipt_path.read_bytes()
            if hashlib.sha256(receipt_bytes).hexdigest() != receipt_hash:
                raise ValueError("recovery receipt changed")
            receipt_value: object = json.loads(receipt_bytes)
            if not is_object(receipt_value) or not is_array(
                raw_evidence := receipt_value.get("artefacts")
            ):
                raise ValueError("recovery requires branch, diff and log evidence")
            evidence: list[_RecoveryArtefact] = []
            for value in raw_evidence:
                if not _is_recovery_artefact(value):
                    raise ValueError("recovery requires branch, diff and log evidence")
                evidence.append(value)
            if {item["role"] for item in evidence} != {"branch", "diff", "log"}:
                raise ValueError("recovery requires branch, diff and log evidence")
            preserved = self.path.parent / f"{self.path.name}.recovery-{uuid.uuid4().hex}"
            preserved.mkdir(mode=0o700)
            snapshots = {
                "checkpoint.json": checkpoint_bytes,
                "lock.json": raw_lock,
                "receipt.json": receipt_bytes,
            }
            for index, item in enumerate(evidence):
                data = confined_file(root, item["path"]).read_bytes()
                if hashlib.sha256(data).hexdigest() != item["sha256"]:
                    raise ValueError("recovery evidence changed")
                snapshots[f"artefact-{index}.bin"] = data
            for name, data in snapshots.items():
                with (preserved / name).open("xb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            directory_fd = os.open(preserved, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            parent_fd = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(parent_fd)
            finally:
                os.close(parent_fd)
            current_stat = self.lock.lstat()
            if (
                self.lock.is_symlink()
                or (current_stat.st_dev, current_stat.st_ino)
                != (lock_stat.st_dev, lock_stat.st_ino)
                or self.lock.read_bytes() != raw_lock
                or self.path.read_bytes() != checkpoint_bytes
            ):
                raise ValueError("lock owner or checkpoint changed; preserved evidence retained")
            self.lock.unlink()
            parent_fd = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(parent_fd)
            finally:
                os.close(parent_fd)
            return preserved
        finally:
            os.close(fd)

    def load(self) -> CheckpointState:
        if self.path.is_symlink():
            raise ValueError("checkpoint cannot be a symlink")
        state: object = json.loads(self.path.read_text())
        if not is_object(state):
            raise ValueError("invalid checkpoint")
        expected = state.pop("checkpoint_sha256", None)
        if expected != _digest(state) or state.get("schema_version") != "1.0":
            raise ValueError("checkpoint integrity failure; preserve and reconcile")
        if not _is_checkpoint(state):
            raise ValueError("invalid checkpoint shape; preserve and reconcile")
        return state

    def _save(self, state: Mapping[str, object]) -> None:
        if self.path.is_symlink():
            raise ValueError("checkpoint cannot be a symlink")
        payload = dict(state, checkpoint_sha256=_digest(state))
        fd, name = tempfile.mkstemp(prefix=f".{self.path.name}.", dir=self.path.parent)
        temporary = Path(name)
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(payload, handle, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
            if os.name == "posix":
                directory_fd = os.open(self.path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)

    def initialise(self, plan: object, *, base_revision: object) -> CheckpointState:
        if (
            not isinstance(base_revision, str)
            or re.fullmatch(r"[0-9a-f]{40}", base_revision) is None
        ):
            raise ValueError("an exact Git revision is required")
        if not is_array(plan) or not plan:
            raise ValueError("plan cannot be empty")
        identifiers: set[str] = set()
        tracks: list[TrackState] = []
        for item in plan:
            if (
                not is_object(item)
                or not _text(identifier := item.get("id"))
                or identifier in identifiers
            ):
                raise ValueError("track identifiers must be non-empty and unique")
            phases, dependencies = item.get("phases"), item.get("dependencies", [])
            if not _texts(phases) or not phases:
                raise ValueError("each track requires named phases")
            if len(set(phases)) != len(phases):
                raise ValueError("phase identifiers must be unique")
            if not _texts(dependencies):
                raise ValueError("dependencies must be a list of identifiers")
            identifiers.add(identifier)
            tracks.append(
                {
                    "id": identifier,
                    "phases": phases,
                    "dependencies": dependencies,
                    "phase_index": 0,
                    "stage": "implement",
                    "repairs": 0,
                }
            )
        resolved: set[str] = set()
        while len(resolved) < len(tracks):
            ready = {
                t["id"] for t in tracks if set(t["dependencies"]).issubset(resolved)
            } - resolved
            if not ready:
                raise ValueError("dependency graph contains a cycle or unknown dependency")
            resolved.update(ready)
        state: CheckpointState = {
            "schema_version": "1.0",
            "base_revision": base_revision,
            "tracks": tracks,
            "events": [],
            "circuit_breaker": False,
        }
        with self._locked():
            if self.path.exists():
                raise FileExistsError("checkpoint already exists; resume without overwriting")
            self._save(state)
        return state

    def advance(
        self,
        *,
        root: Path,
        event_id: str,
        action: object,
        receipt: str | None = None,
        wake_condition: str | None = None,
    ) -> CheckpointState:
        """Persist one evidence-bound outcome and expose the next ready instruction."""
        if not _text(event_id):
            raise ValueError("event_id is required")
        if not isinstance(action, str) or action not in {
            "pass",
            "fail",
            "waiting_external",
            "decision_needed",
            "circuit_breaker",
        }:
            raise ValueError("unsupported transition")
        if action not in {"pass", "fail"} and receipt is not None:
            raise ValueError("blocked transitions cannot supply an unverified receipt")
        request: dict[str, str | None] = {
            "action": action,
            "receipt": receipt,
            "wake_condition": wake_condition,
        }
        with self._locked():
            state = self.load()
            prior = next((e for e in state["events"] if e["id"] == event_id), None)
            if prior is not None:
                if prior["request"] != request:
                    raise ValueError("event ID reused for a different transition")
                if (
                    receipt
                    and read_bound_receipt(root.resolve(), receipt, prior["instruction"], action)
                    != prior["receipt_sha256"]
                ):
                    raise ValueError("replayed receipt changed")
                return state
            current = next_action(state)
            if current is None:
                raise ValueError("no ready instruction; reconcile the retained blocked state")
            track = next(t for t in state["tracks"] if t["id"] == current["track_id"])
            receipt_hash = None
            if action in {"pass", "fail"}:
                if receipt is None:
                    raise ValueError("completion and rework require a bound receipt")
                receipt_hash = read_bound_receipt(root.resolve(), receipt, current, action)
            elif not _text(wake_condition):
                raise ValueError("blocked state requires a wake condition")
            if action == "circuit_breaker":
                state["circuit_breaker"] = True
            elif action in {"waiting_external", "decision_needed"}:
                track["wait_resume_stage"] = track["stage"]
                track["stage"] = action
                track["wake_condition"] = wake_condition
            elif action == "fail":
                track["repairs"] += 1
                track.setdefault("resume_stage", track["stage"])
                track["stage"] = "rework" if track["repairs"] <= 2 else "blocked_safe"
            elif track["stage"] == "rework":
                track["stage"] = track.pop("resume_stage")
            elif track["stage"] == "implement":
                if track["phase_index"] + 1 < len(track["phases"]):
                    track["phase_index"] += 1
                else:
                    track["stage"] = "review"
            elif track["stage"] == "review":
                track["stage"] = "sync"
            elif track["stage"] == "sync":
                track["stage"] = "complete"
            state["events"].append(
                {
                    "id": event_id,
                    "request": request,
                    "instruction": current,
                    "receipt_sha256": receipt_hash,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            )
            self._save(state)
            return state

    def resume(self, *, root: Path, track_id: str, event_id: str, receipt: str) -> CheckpointState:
        """Resume an external/decision wait only after a matching reconciliation receipt.

        Circuit breakers and exhausted rework cannot be reset through this API.
        A resume receipt records the caller's verified wake evidence, not approval
        inferred by this coordinator.
        """
        if not _text(event_id):
            raise ValueError("event_id is required")
        with self._locked():
            state = self.load()
            if state["circuit_breaker"]:
                raise ValueError("circuit breaker requires separate governed reconciliation")
            request: dict[str, str | None] = {
                "action": "resume",
                "track_id": track_id,
                "receipt": receipt,
            }
            prior = next((e for e in state["events"] if e["id"] == event_id), None)
            if prior is not None:
                if (
                    prior["request"] != request
                    or read_bound_receipt(root.resolve(), receipt, prior["instruction"], "resume")
                    != prior["receipt_sha256"]
                ):
                    raise ValueError("resume event or evidence changed")
                return state
            track = next((t for t in state["tracks"] if t["id"] == track_id), None)
            if track is None or track["stage"] not in {"waiting_external", "decision_needed"}:
                raise ValueError("track is not waiting on external evidence or a decision")
            phase = track["phases"][track["phase_index"]]
            expected = {
                "track_id": track_id,
                "phase_id": phase,
                "stage": track["stage"],
                "base_revision": state["base_revision"],
                "run_id": deterministic_run_id(track_id, phase, state["base_revision"]),
            }
            receipt_hash = read_bound_receipt(root.resolve(), receipt, expected, "resume")
            track["stage"] = track.pop("wait_resume_stage")
            track.pop("wake_condition")
            state["events"].append(
                {
                    "id": event_id,
                    "request": request,
                    "instruction": expected,
                    "receipt_sha256": receipt_hash,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            )
            self._save(state)
            return state
