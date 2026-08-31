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
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from tools.autonomy_harness import deterministic_run_id


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _relative_file(root: Path, name: Any) -> Path:
    if not _text(name):
        raise ValueError("evidence path must be a non-empty relative path")
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
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


def _read_receipt(root: Path, name: str, expected: dict[str, str], outcome: str) -> str:
    path = _relative_file(root, name)
    raw = path.read_bytes()
    receipt = json.loads(raw)
    if not isinstance(receipt, dict) or any(receipt.get(k) != v for k, v in expected.items()):
        raise ValueError("receipt does not match the exact run, revision, track, phase and stage")
    if receipt.get("outcome") != outcome:
        raise ValueError("receipt outcome does not match the transition")
    artefacts = receipt.get("artefacts")
    if not isinstance(artefacts, list) or not artefacts:
        raise ValueError("receipt requires non-empty artefact evidence")
    seen: set[str] = set()
    for artefact in artefacts:
        if not isinstance(artefact, dict):
            raise ValueError("invalid artefact evidence")
        evidence = _relative_file(root, artefact.get("path"))
        identity = str(evidence)
        if identity in seen or evidence == path:
            raise ValueError("duplicate or self-referential artefact evidence")
        seen.add(identity)
        data = evidence.read_bytes()
        if not data or hashlib.sha256(data).hexdigest() != artefact.get("sha256"):
            raise ValueError("artefact hash mismatch or empty evidence")
    return hashlib.sha256(raw).hexdigest()


def next_action(state: dict[str, Any]) -> dict[str, str] | None:
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

    def __init__(self, path: Path):
        self.path = path.absolute()
        self.lock = self.path.with_name(self.path.name + ".lock")

    @contextmanager
    def _locked(self) -> Iterator[None]:
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
                observed = json.loads(self.lock.read_text()) if not self.lock.is_symlink() else None
                if (
                    isinstance(observed, dict)
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
            lease = json.loads(raw_lock)
            if (
                not isinstance(lease, dict)
                or lease.get("protocol") != "checkpoint-lease-v1"
                or any(
                    not _text(lease.get(field))
                    for field in (
                        "token",
                        "owner",
                        "run_id",
                        "worktree",
                        "heartbeat_at",
                        "expires_at",
                    )
                )
            ):
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
            receipt_path = _relative_file(root, receipt)
            receipt_hash = _read_receipt(root, receipt, expected, "recover")
            receipt_bytes = receipt_path.read_bytes()
            if hashlib.sha256(receipt_bytes).hexdigest() != receipt_hash:
                raise ValueError("recovery receipt changed")
            evidence = json.loads(receipt_bytes)["artefacts"]
            if any(not isinstance(item.get("role"), str) for item in evidence) or {
                item["role"] for item in evidence
            } != {"branch", "diff", "log"}:
                raise ValueError("recovery requires branch, diff and log evidence")
            preserved = self.path.parent / f"{self.path.name}.recovery-{uuid.uuid4().hex}"
            preserved.mkdir(mode=0o700)
            snapshots = {
                "checkpoint.json": checkpoint_bytes,
                "lock.json": raw_lock,
                "receipt.json": receipt_bytes,
            }
            for index, item in enumerate(evidence):
                data = _relative_file(root, item["path"]).read_bytes()
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

    def load(self) -> dict[str, Any]:
        if self.path.is_symlink():
            raise ValueError("checkpoint cannot be a symlink")
        state = json.loads(self.path.read_text())
        if not isinstance(state, dict):
            raise ValueError("invalid checkpoint")
        expected = state.pop("checkpoint_sha256", None)
        if expected != _digest(state) or state.get("schema_version") != "1.0":
            raise ValueError("checkpoint integrity failure; preserve and reconcile")
        return state

    def _save(self, state: dict[str, Any]) -> None:
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

    def initialise(self, plan: list[dict[str, Any]], *, base_revision: str) -> dict[str, Any]:
        if (
            not isinstance(base_revision, str)
            or re.fullmatch(r"[0-9a-f]{40}", base_revision) is None
        ):
            raise ValueError("an exact Git revision is required")
        if not isinstance(plan, list) or not plan:
            raise ValueError("plan cannot be empty")
        identifiers: set[str] = set()
        tracks: list[dict[str, Any]] = []
        for item in plan:
            if not isinstance(item, dict) or not _text(item.get("id")) or item["id"] in identifiers:
                raise ValueError("track identifiers must be non-empty and unique")
            phases, dependencies = item.get("phases"), item.get("dependencies", [])
            if not isinstance(phases, list) or not phases or any(not _text(p) for p in phases):
                raise ValueError("each track requires named phases")
            if len(set(phases)) != len(phases):
                raise ValueError("phase identifiers must be unique")
            if not isinstance(dependencies, list) or any(not _text(d) for d in dependencies):
                raise ValueError("dependencies must be a list of identifiers")
            identifiers.add(item["id"])
            tracks.append(
                {
                    "id": item["id"],
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
        state = {
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
        action: str,
        receipt: str | None = None,
        wake_condition: str | None = None,
    ) -> dict[str, Any]:
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
        request = {"action": action, "receipt": receipt, "wake_condition": wake_condition}
        with self._locked():
            state = self.load()
            prior = next((e for e in state["events"] if e["id"] == event_id), None)
            if prior is not None:
                if prior["request"] != request:
                    raise ValueError("event ID reused for a different transition")
                if (
                    receipt
                    and _read_receipt(root.resolve(), receipt, prior["instruction"], action)
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
                receipt_hash = _read_receipt(root.resolve(), receipt, current, action)
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

    def resume(self, *, root: Path, track_id: str, event_id: str, receipt: str) -> dict[str, Any]:
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
            request = {"action": "resume", "track_id": track_id, "receipt": receipt}
            prior = next((e for e in state["events"] if e["id"] == event_id), None)
            if prior is not None:
                if (
                    prior["request"] != request
                    or _read_receipt(root.resolve(), receipt, prior["instruction"], "resume")
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
            receipt_hash = _read_receipt(root.resolve(), receipt, expected, "resume")
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
