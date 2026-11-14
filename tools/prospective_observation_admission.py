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
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Never, TypeAlias, TypedDict

from tools import prospective_execution_gate as gate
from tools import prospective_runner_contract as runner
from tools import prospective_server_session as session
from tools.evaluation_preflight import unique_object_pairs
from tools.json_shapes import JsonObject, is_array, is_object

MAX_RECEIPT = 32 * 1024 * 1024
MAX_JOURNAL = 256 * 1024
MAX_STREAM = 1024 * 1024
_ORIGIN = object()
_LIVE: weakref.WeakSet[OwnedCapture] = weakref.WeakSet()

IssuerContext: TypeAlias = tuple[Path, str, str, Path, Path]
Plans: TypeAlias = tuple[gate.ExecutionPlan, ...]


class JournalHeader(TypedDict):
    type: Literal["run_started"]
    version: Literal["controller-journal-v1"]
    study_id: str
    protocol_sha256: str
    source_commit: str
    review_commit: str
    slots: list[str]
    receipt_names: list[str]
    retry_policy: Literal["no-automatic-retry-or-resume"]


class SlotStarted(TypedDict):
    type: Literal["slot_started"]
    slot_id: str
    receipt_name: str


class SlotCaptured(TypedDict):
    type: Literal["slot_captured"]
    slot_id: str
    receipt_name: str
    receipt_sha256: str
    receipt_bytes: int


class ObservationSummary(TypedDict):
    slot_id: str
    receipt_sha256: str
    response_sha256: str
    content_sha256: str


class AdmissionResult(TypedDict):
    status: Literal["observations_admitted_before_blinding"]
    admitted: Literal[True]
    admission_before_blinding: Literal[True]
    study_unlocked: Literal[False]
    scoring_start: Literal[False]
    protocol_sha256: str
    review_commit: str
    source_commit: str
    study_id: str
    journal_sha256: str
    observations: list[ObservationSummary]
    limitations: list[str]


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return gate.canonical_bytes(value)


def parse_owned_receipt(raw: bytes) -> JsonObject:
    try:
        result: object = json.loads(raw, object_pairs_hook=unique_object_pairs)
        if not is_object(result) or type(result) is not dict:
            raise ValueError("invalid_owned_receipt")
        canonical_bytes(result)
        return result
    except (ValueError, UnicodeError, RecursionError):
        raise ValueError("invalid_owned_receipt") from None


def _capture_object(value: object) -> JsonObject:
    """Narrow persisted fields at their first use; preserve TypeError handling."""
    if not is_object(value):
        raise TypeError("invalid_capture_object")
    return value


def read_owned_receipt(
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
        session.verify_reserved_receipt(path, descriptor, parent)
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
        session.verify_reserved_receipt(path, descriptor, parent)
        after = os.fstat(descriptor)
        if not stat.S_ISREG(after.st_mode) or after.st_nlink != 1 or after.st_uid != getuid():
            raise ValueError("unsafe_owned_receipt")
        return raw, identity


@dataclass(frozen=True)
class CaptureReceipt:
    slot: str
    name: str
    identity: tuple[int, int]
    raw: bytes
    returned: bytes


@dataclass(frozen=True, eq=False, slots=True, weakref_slot=True)
class OwnedCapture:
    origin: object
    context: IssuerContext
    plans: Plans
    directory: Path
    parent_identity: tuple[int, int]
    journal_fd: int
    journal_identity: tuple[int, int]
    journal: bytes
    receipts: tuple[CaptureReceipt, ...]

    def __post_init__(self) -> None:
        if self.origin is not _ORIGIN:
            raise ValueError("invalid_capture_capability")

    def __reduce__(self) -> Never:
        raise TypeError("capture_capability_not_serializable")

    def __copy__(self) -> Never:
        raise TypeError("capture_capability_not_copyable")

    def __deepcopy__(self, memo: object) -> Never:
        del memo  # Required copy protocol argument; copying is deliberately prohibited.
        raise TypeError("capture_capability_not_copyable")


def issue_controller_capture(
    context: IssuerContext,
    plans: Plans,
    directory: Path,
    parent_identity: tuple[int, int],
    journal_fd: int,
    journal_identity: tuple[int, int],
    journal: bytes,
    receipts: tuple[CaptureReceipt, ...],
) -> OwnedCapture:
    """Issue only inside the trusted controller; persisted JSON cannot call this path.

    This package interface is not a hostile-Python security boundary. The live
    witness set remains private and consumption removes authority before checks.
    """
    result = OwnedCapture(
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


def revoke_capture(owned: object) -> None:
    """Discard a live capture capability without creating or restoring one."""
    if type(owned) is OwnedCapture:
        _LIVE.discard(owned)


def capture_is_live(owned: object) -> bool:
    """Inspect nominal liveness without exposing the mutable witness registry."""
    return type(owned) is OwnedCapture and owned in _LIVE


def journal_header(plans: Plans) -> JournalHeader:
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


def slot_started_record(slot: str, name: str) -> SlotStarted:
    return {"type": "slot_started", "slot_id": slot, "receipt_name": name}


def slot_captured_record(receipt: CaptureReceipt) -> SlotCaptured:
    return {
        "type": "slot_captured",
        "slot_id": receipt.slot,
        "receipt_name": receipt.name,
        "receipt_sha256": sha256_bytes(receipt.raw),
        "receipt_bytes": len(receipt.raw),
    }


def encode_journal_line(event: Mapping[str, object], index: int, previous: str) -> bytes:
    return canonical_bytes({"sequence": index, "previous_sha256": previous, "event": event}) + b"\n"


def encode_journal(events: Sequence[Mapping[str, object]]) -> bytes:
    previous = "0" * 64
    lines: list[bytes] = []
    for index, event in enumerate(events):
        line = encode_journal_line(event, index, previous)
        lines.append(line)
        previous = sha256_bytes(line)
    return b"".join(lines)


def verified_bounded_body(value: Mapping[str, object], prefix: str, maximum: int) -> bytes:
    encoded = value[prefix]
    if type(encoded) is not str or len(encoded) > 4 * ((maximum + 2) // 3):
        raise ValueError("invalid_capture_bytes")
    raw = base64.b64decode(encoded, validate=True)
    if len(raw) > maximum or base64.b64encode(raw).decode() != encoded:
        raise ValueError("invalid_capture_bytes")
    return raw


def validate_captured_receipt(raw: bytes, plan: gate.ExecutionPlan) -> ObservationSummary:
    value = parse_owned_receipt(raw)
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
    expected = plan.value()
    if canonical_bytes(value["primary_gate"]) != canonical_bytes(
        expected["evidence"]
    ) or canonical_bytes(value["admission"]) != canonical_bytes(expected["admission"]):
        raise ValueError("capture_gate_mismatch")
    request = verified_bounded_body(value, "request_base64", runner.native.MAX_BYTES)
    if sha256_bytes(request) != expected["request"]["request"]["sha256"] or value[
        "request_sha256"
    ] != sha256_bytes(request):
        raise ValueError("capture_request_mismatch")
    completion = value["completion"]
    health = value.get("health")
    if (
        not is_array(health)
        or type(health) is not list
        or not 1 <= len(health) <= session.HEALTH_ATTEMPTS
    ):
        raise ValueError("capture_health_incomplete")
    final_health = _capture_object(health[-1])
    health_body = verified_bounded_body(final_health, "body_base64", session.HEALTH_BYTES)
    if (
        final_health.get("status") != "http_response_captured"
        or final_health.get("error") != "none"
        or type(final_health.get("http_status")) is not int
        or final_health["http_status"] != 200
        or final_health.get("body_complete") is not True
        or type(final_health.get("body_bytes")) is not int
        or final_health["body_bytes"] != len(health_body)
        or final_health.get("body_sha256") != sha256_bytes(health_body)
        or parse_owned_receipt(health_body) != {"status": "ok"}
    ):
        raise ValueError("capture_health_incomplete")
    completion = _capture_object(completion)
    if (
        completion["status"] != "http_response_captured"
        or completion.get("transport") != "unix-domain-socket"
        or completion["error"] != "none"
        or completion["body_complete"] is not True
        or type(completion["http_status"]) is not int
        or completion["http_status"] != 200
        or completion["method"] != "POST"
        or completion["route"] != "/completion"
        or completion["request_body_sha256"] != sha256_bytes(request)
    ):
        raise ValueError("capture_http_incomplete")
    body = verified_bounded_body(completion, "body_base64", runner.native.MAX_BYTES)
    if (
        type(completion["body_bytes"]) is not int
        or completion["body_bytes"] != len(body)
        or completion["body_sha256"] != sha256_bytes(body)
    ):
        raise ValueError("capture_body_mismatch")
    normalized = runner.normalize_candidate(
        expected["request"],
        body,
        slot_id=expected["evidence"]["slot_id"],
        expected_slot_id=expected["evidence"]["slot_id"],
        expected_model=expected["admission"]["model_id"],
    )
    if canonical_bytes(value["candidate"]) != canonical_bytes(normalized) or canonical_bytes(
        value["decoded"]
    ) != canonical_bytes(normalized["decoded"]):
        raise ValueError("capture_normalization_mismatch")
    child = _capture_object(value["process"])
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
    streams: dict[str, bytes] = {}
    for name in ("stdout", "stderr"):
        data = verified_bounded_body(child, f"raw_{name}_base64", MAX_STREAM)
        if (
            child[f"{name}_complete"] is not True
            or child[f"{name}_truncated"] is not False
            or any(
                type(child[key]) is not int or child[key] != len(data)
                for key in (f"{name}_bytes_observed", f"{name}_bytes_retained")
            )
            or child[f"{name}_sha256"] != sha256_bytes(data)
            or child[f"{name}_retained_sha256"] != sha256_bytes(data)
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
    socket_path = value["socket_path"]
    if not isinstance(socket_path, str):
        raise TypeError("invalid_capture_socket_path")
    if value["arguments"] != session.fixed_server_arguments(
        expected["admission"], Path(socket_path)
    ):
        raise ValueError("capture_arguments_mismatch")
    environment = session.profile.profile_environment()
    if value["environment_sha256"] != hashlib.sha256(
        json.dumps(environment, sort_keys=True).encode()
    ).hexdigest() or value["environment_keys"] != sorted(environment):
        raise ValueError("capture_environment_mismatch")
    return {
        "slot_id": normalized["slot_id"],
        "receipt_sha256": sha256_bytes(raw),
        "response_sha256": sha256_bytes(body),
        "content_sha256": normalized["decoded"]["content_sha256"],
    }


def consume_controller_capture(owned: object) -> AdmissionResult:
    if type(owned) is not OwnedCapture or owned not in _LIVE:
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
            if (
                gate.verify_execution_plan(protocol, pin, slot, review, root, model_root).payload
                != plan.payload
            ):
                raise ValueError("admission_gate_changed")
        directory = session.private_directory_identity(owned.directory)
        if directory != owned.parent_identity:
            raise ValueError("owned_directory_changed")
        journal_path = owned.directory / "journal.jsonl"
        session.verify_reserved_receipt(journal_path, owned.journal_fd, directory)
        raw, _identity = read_owned_receipt(
            journal_path, directory, MAX_JOURNAL, owned.journal_identity
        )
        if raw != owned.journal:
            raise ValueError("owned_journal_changed")
        events: list[Mapping[str, object]] = [journal_header(owned.plans)]
        rows: list[ObservationSummary] = []
        for index, (receipt, plan) in enumerate(zip(owned.receipts, owned.plans, strict=True)):
            if receipt.name != f"slot-{index + 1}.json":
                raise ValueError("invalid_owned_receipt_name")
            raw, _ = read_owned_receipt(
                owned.directory / receipt.name, directory, MAX_RECEIPT, receipt.identity
            )
            if raw != receipt.raw or canonical_bytes(parse_owned_receipt(raw)) != receipt.returned:
                raise ValueError("owned_receipt_changed")
            rows.append(validate_captured_receipt(raw, plan))
            events.extend(
                (slot_started_record(receipt.slot, receipt.name), slot_captured_record(receipt))
            )
        events.append(
            {"type": "capture_complete", "dispositions": dict.fromkeys(slots, "captured")}
        )
        if encode_journal(events) != owned.journal:
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
            "journal_sha256": sha256_bytes(owned.journal),
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
