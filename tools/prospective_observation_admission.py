"""Immediate controller-owned admission, never authority reconstructed from JSON.

Private one-shot witnesses narrow the trusted capture boundary, not hostile
Python or owner access. Durable records require a later trusted custody handoff;
they cannot recreate a live witness or independently unlock scoring.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import signal
import stat
import weakref
from dataclasses import dataclass
from pathlib import Path

from tools import prospective_execution_gate as gate
from tools import prospective_runner_contract as runner
from tools import prospective_server_session as session
from tools.evaluation_preflight import _unique

MAX_RECEIPT = 32 * 1024 * 1024
MAX_JOURNAL = 256 * 1024
MAX_STREAM = 1024 * 1024
_ORIGIN = object()
_LIVE: weakref.WeakSet = weakref.WeakSet()


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical(value: object) -> bytes:
    return gate._canonical(value)


def _parse(raw: bytes) -> dict:
    try:
        result = json.loads(raw, object_pairs_hook=_unique)
        if type(result) is not dict:
            raise ValueError("invalid_owned_receipt")
        _canonical(result)
        return result
    except (ValueError, UnicodeError, RecursionError):
        raise ValueError("invalid_owned_receipt") from None


def _read(
    path: Path,
    parent: tuple[int, int],
    maximum: int,
    expected: tuple[int, int] | None = None,
    *,
    synchronize: bool = False,
) -> tuple[bytes, tuple[int, int]]:
    flags = (
        (os.O_RDWR if synchronize else os.O_RDONLY)
        | getattr(os, "O_NONBLOCK", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        descriptor = stream.fileno()
        session._reserved(path, descriptor, parent)
        info = os.fstat(descriptor)
        getuid = getattr(os, "getuid", None)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or not callable(getuid)
            or info.st_uid != getuid()
        ):
            raise ValueError("unsafe_owned_receipt")
        identity = info.st_dev, info.st_ino
        if expected is not None and identity != expected:
            raise ValueError("owned_receipt_replaced")
        if synchronize:
            os.fsync(descriptor)
        raw = stream.read(maximum + 1)
        if len(raw) > maximum:
            raise ValueError("owned_receipt_byte_limit")
        session._reserved(path, descriptor, parent)
        after = os.fstat(descriptor)
        if not stat.S_ISREG(after.st_mode) or after.st_nlink != 1 or after.st_uid != getuid():
            raise ValueError("unsafe_owned_receipt")
        return raw, identity


@dataclass(frozen=True)
class _Receipt:
    slot: str
    name: str
    identity: tuple[int, int]
    raw: bytes
    returned: bytes


@dataclass(frozen=True, eq=False, slots=True, weakref_slot=True)
class _OwnedRun:
    origin: object
    context: tuple[Path, str, str, Path, Path]
    plans: tuple[gate._Plan, gate._Plan]
    directory: Path
    parent_identity: tuple[int, int]
    journal_fd: int
    journal_identity: tuple[int, int]
    journal: bytes
    receipts: tuple[_Receipt, _Receipt]

    def __post_init__(self) -> None:
        if self.origin is not _ORIGIN:
            raise ValueError("invalid_capture_capability")

    def __reduce__(self):
        raise TypeError("capture_capability_not_serializable")

    def __copy__(self):
        raise TypeError("capture_capability_not_copyable")

    def __deepcopy__(self, memo):
        raise TypeError("capture_capability_not_copyable")


def _issue(
    context, plans, directory, parent_identity, journal_fd, journal_identity, journal, receipts
) -> _OwnedRun:
    result = _OwnedRun(
        _ORIGIN,
        context,
        plans,
        directory,
        parent_identity,
        journal_fd,
        journal_identity,
        journal,
        receipts,
    )
    _LIVE.add(result)
    return result


def _header(plans: tuple[gate._Plan, gate._Plan]) -> dict:
    evidence = plans[0].value()["evidence"]
    return {
        "type": "run_started",
        "version": "controller-journal-v1",
        "study_id": evidence["study_id"],
        "protocol_sha256": evidence["protocol_sha256"],
        "source_commit": evidence["source_commit"],
        "review_commit": evidence["review_commit"],
        "slots": [plan.value()["evidence"]["slot_id"] for plan in plans],
        "receipt_names": ["slot-1.json", "slot-2.json"],
        "retry_policy": "no-automatic-retry-or-resume",
    }


def _start(slot: str, name: str) -> dict:
    return {"type": "slot_started", "slot_id": slot, "receipt_name": name}


def _complete(receipt: _Receipt) -> dict:
    return {
        "type": "slot_captured",
        "slot_id": receipt.slot,
        "receipt_name": receipt.name,
        "receipt_sha256": _sha(receipt.raw),
        "receipt_bytes": len(receipt.raw),
    }


def _line(event: dict, index: int, previous: str) -> bytes:
    return _canonical({"sequence": index, "previous_sha256": previous, "event": event}) + b"\n"


def _journal(events: list[dict]) -> bytes:
    previous, lines = "0" * 64, []
    for index, event in enumerate(events):
        line = _line(event, index, previous)
        lines.append(line)
        previous = _sha(line)
    return b"".join(lines)


def _body(value: dict, prefix: str, maximum: int) -> bytes:
    encoded = value[prefix]
    if type(encoded) is not str or len(encoded) > 4 * ((maximum + 2) // 3):
        raise ValueError("invalid_capture_bytes")
    raw = base64.b64decode(encoded, validate=True)
    if len(raw) > maximum or base64.b64encode(raw).decode() != encoded:
        raise ValueError("invalid_capture_bytes")
    return raw


def _validate_receipt(raw: bytes, plan: gate._Plan) -> dict:
    value, expected = _parse(raw), plan.value()
    if (
        value.get("purpose") not in (None, "primary-observation")
        or "fixture" in value
        or value.get("status") != "primary_session_captured"
        or value.get("error") != "none"
        or value.get("admitted") is not False
        or value.get("study_unlocked") is not False
        or value.get("worker_joined") is not True
        or value.get("resources_removed") is not True
        or value.get("cleanup_errors") != []
        or "primary_postflight_error" in value
    ):
        raise ValueError("capture_not_admissible")
    if _canonical(value["primary_gate"]) != _canonical(expected["evidence"]) or _canonical(
        value["admission"]
    ) != _canonical(expected["admission"]):
        raise ValueError("capture_gate_mismatch")
    request = _body(value, "request_base64", runner.native.MAX_BYTES)
    if _sha(request) != expected["request"]["request"]["sha256"] or value["request_sha256"] != _sha(
        request
    ):
        raise ValueError("capture_request_mismatch")
    completion = value["completion"]
    health = value.get("health")
    if type(health) is not list or not 1 <= len(health) <= session.HEALTH_ATTEMPTS:
        raise ValueError("capture_health_incomplete")
    final_health = health[-1]
    health_body = _body(final_health, "body_base64", session.HEALTH_BYTES)
    if (
        final_health.get("status") != "http_response_captured"
        or final_health.get("error") != "none"
        or type(final_health.get("http_status")) is not int
        or final_health["http_status"] != 200
        or final_health.get("body_complete") is not True
        or type(final_health.get("body_bytes")) is not int
        or final_health["body_bytes"] != len(health_body)
        or final_health.get("body_sha256") != _sha(health_body)
        or _parse(health_body) != {"status": "ok"}
    ):
        raise ValueError("capture_health_incomplete")
    if (
        completion["status"] != "http_response_captured"
        or completion.get("transport") != "unix-domain-socket"
        or completion["error"] != "none"
        or completion["body_complete"] is not True
        or type(completion["http_status"]) is not int
        or completion["http_status"] != 200
        or completion["method"] != "POST"
        or completion["route"] != "/completion"
        or completion["request_body_sha256"] != _sha(request)
    ):
        raise ValueError("capture_http_incomplete")
    body = _body(completion, "body_base64", runner.native.MAX_BYTES)
    if (
        type(completion["body_bytes"]) is not int
        or completion["body_bytes"] != len(body)
        or completion["body_sha256"] != _sha(body)
    ):
        raise ValueError("capture_body_mismatch")
    normalized = runner.normalize_candidate(
        expected["request"],
        body,
        slot_id=expected["evidence"]["slot_id"],
        expected_slot_id=expected["evidence"]["slot_id"],
        expected_model=expected["admission"]["model_id"],
    )
    if _canonical(value["candidate"]) != _canonical(normalized) or _canonical(
        value["decoded"]
    ) != _canonical(normalized["decoded"]):
        raise ValueError("capture_normalization_mismatch")
    child = value["process"]
    if (
        child["status"] != "process_stopped"
        or child["error"] != "none"
        or child["execution_observed"] is not True
        or child["reaped"] is not True
        or child["cleanup_errors"] != []
        or type(child["pid"]) is not int
        or child["pid"] <= 0
        or type(child["returncode"]) is not int
        or child["returncode"] not in (0, -signal.SIGTERM)
    ):
        raise ValueError("capture_process_incomplete")
    streams = {}
    for name in ("stdout", "stderr"):
        data = _body(child, f"raw_{name}_base64", MAX_STREAM)
        if (
            child[f"{name}_complete"] is not True
            or child[f"{name}_truncated"] is not False
            or any(
                type(child[key]) is not int or child[key] != len(data)
                for key in (f"{name}_bytes_observed", f"{name}_bytes_retained")
            )
            or child[f"{name}_sha256"] != _sha(data)
            or child[f"{name}_retained_sha256"] != _sha(data)
        ):
            raise ValueError("capture_stream_incomplete")
        streams[name] = data
    images = session.profile.verify_loaded_images(streams["stderr"])
    pids = {
        match[1]
        for line in streams["stderr"].decode("utf-8").splitlines()
        if (match := session.core.IMAGE_LINE.fullmatch(line)) is not None
    }
    if pids != {str(child["pid"])} or value["loaded_non_system_images"] != images:
        raise ValueError("capture_loader_mismatch")
    if (
        value["source_sha256"] != session.source_pins()
        or value["profile_sha256"] != session.profile.profile_digest()
    ):
        raise ValueError("capture_source_mismatch")
    if value["arguments"] != session._fixed_arguments(
        expected["admission"], Path(value["socket_path"])
    ):
        raise ValueError("capture_arguments_mismatch")
    environment = session.profile.profile_environment()
    if value["environment_sha256"] != hashlib.sha256(
        json.dumps(environment, sort_keys=True).encode()
    ).hexdigest() or value["environment_keys"] != sorted(environment):
        raise ValueError("capture_environment_mismatch")
    return {
        "slot_id": normalized["slot_id"],
        "receipt_sha256": _sha(raw),
        "response_sha256": _sha(body),
        "content_sha256": normalized["decoded"]["content_sha256"],
    }


def _consume(owned: _OwnedRun) -> dict:
    if type(owned) is not _OwnedRun or owned not in _LIVE:
        raise ValueError("invalid_or_consumed_capture_capability")
    _LIVE.remove(owned)
    try:
        if len(owned.plans) != 2 or len(owned.receipts) != 2:
            raise ValueError("incomplete_capture_denominator")
        slots = [plan.value()["evidence"]["slot_id"] for plan in owned.plans]
        if len(set(slots)) != 2 or [row.slot for row in owned.receipts] != slots:
            raise ValueError("incomplete_capture_denominator")
        protocol, pin, review, root, model_root = owned.context
        for slot, plan in zip(slots, owned.plans, strict=True):
            if gate._verify(protocol, pin, slot, review, root, model_root).payload != plan.payload:
                raise ValueError("admission_gate_changed")
        directory = session._directory(owned.directory)
        if directory != owned.parent_identity:
            raise ValueError("owned_directory_changed")
        journal_path = owned.directory / "journal.jsonl"
        session._reserved(journal_path, owned.journal_fd, directory)
        raw, identity = _read(journal_path, directory, MAX_JOURNAL, owned.journal_identity)
        if raw != owned.journal:
            raise ValueError("owned_journal_changed")
        events = [_header(owned.plans)]
        rows = []
        for index, (receipt, plan) in enumerate(zip(owned.receipts, owned.plans, strict=True)):
            if receipt.name != f"slot-{index + 1}.json":
                raise ValueError("invalid_owned_receipt_name")
            raw, _ = _read(owned.directory / receipt.name, directory, MAX_RECEIPT, receipt.identity)
            if raw != receipt.raw or _canonical(_parse(raw)) != receipt.returned:
                raise ValueError("owned_receipt_changed")
            rows.append(_validate_receipt(raw, plan))
            events.extend((_start(receipt.slot, receipt.name), _complete(receipt)))
        events.append(
            {"type": "capture_complete", "dispositions": {slot: "captured" for slot in slots}}
        )
        if _journal(events) != owned.journal:
            raise ValueError("owned_journal_chain_mismatch")
        evidence = owned.plans[0].value()["evidence"]
        return {
            "status": "observations_admitted_before_blinding",
            "admitted": True,
            "admission_before_blinding": True,
            "study_unlocked": False,
            "scoring_start": False,
            "protocol_sha256": pin,
            "review_commit": review,
            "source_commit": evidence["source_commit"],
            "study_id": evidence["study_id"],
            "journal_sha256": _sha(owned.journal),
            "observations": rows,
            "limitations": [
                "immediate-controller-owned-capture-only",
                "not-a-rehydratable-execution-capability",
                "offline-reuse-requires-trusted-custody-handoff",
                "scoring-and-unblinding-not-authorised",
                "not-hostile-python-or-owner-isolation",
                "not-clinical-or-operational-validation",
            ],
        }
    except (KeyError, TypeError, UnicodeError):
        raise ValueError("invalid_owned_capture") from None
