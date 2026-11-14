"""At most one attempt per slot within one evidence-root/study/protocol/review run.

Alternative owner-selected roots are outside that guarantee. No retry or resume
is inferred from partial files. Immediate private admission is not an offline
JSON provenance claim, global deduplication or permission to score/unblind.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path
from typing import Literal, NotRequired, Protocol, TypeAlias, TypedDict

from tools import json_shapes
from tools import prospective_execution_gate as gate
from tools import prospective_native_protocol as native
from tools import prospective_observation_admission as admission
from tools import prospective_primary_session as primary
from tools import prospective_server_session as session
from tools.prospective_observation_admission import CaptureReceipt

Disposition: TypeAlias = Literal[
    "not-attempted", "attempted-outcome-unknown", "failed-receipt-retained", "captured"
]
FailureStage: TypeAlias = Literal[
    "persistence", "capture", "readback", "capture_validation", "admission"
]


class JournalStream(Protocol):
    def fileno(self) -> int: ...

    def write(self, raw: bytes, /) -> int: ...

    def flush(self) -> None: ...


class ControllerResult(TypedDict):
    """Durable controller outcome, without permission to unblind or score."""

    status: Literal["controller_failed", "controller_admitted_before_blinding"]
    error: Literal["none", "capture_or_admission_failed"]
    admitted: bool
    admission_before_blinding: bool
    study_unlocked: Literal[False]
    scoring_start: Literal[False]
    run_id: str
    dispositions: dict[str, Disposition]
    limitations: list[str]
    journal_sha256: NotRequired[str]
    admission_sha256: NotRequired[str]
    failure_stage: NotRequired[FailureStage]
    outcome_persistence_error: NotRequired[Literal["failure_outcome_persistence_failed"]]
    journal_persistence_error: NotRequired[Literal["journal_persistence_failed"]]


def _strings(value: object) -> list[str]:
    if not json_shapes.is_array(value):
        raise ValueError("invalid_controller_context")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError("invalid_controller_context")
        result.append(item)
    return result


def _plan_value(plan: session.PrimaryPlan) -> json_shapes.JsonObject:
    return json_shapes.require_object(plan.value(), context="controller plan")


def prepare_execution_plans(
    protocol_path: Path, pin: str, review: str, root: Path, model_root: Path
):
    if ".." in protocol_path.parts or type(review) is not str:
        raise ValueError("invalid_controller_context")
    root, protocol_path, _ = gate.freeze.resolve_repository(protocol_path, review, root)
    value = json_shapes.require_object(
        native.validated_candidate(protocol_path, pin)[0], context="controller protocol"
    )
    slots = _strings(value["expected_slots"])
    plans = tuple(
        gate.verify_execution_plan(protocol_path, pin, slot, review, root, model_root)
        for slot in slots
    )
    if len(plans) != 2:
        raise ValueError("invalid_controller_denominator")
    common: list[bytes] = []
    for plan in plans:
        current = _plan_value(plan)
        evidence = dict(
            json_shapes.require_object(current["evidence"], context="controller evidence")
        )
        evidence.pop("slot_id")
        common.append(
            admission.canonical_bytes({"admission": current["admission"], "evidence": evidence})
        )
    if common[0] != common[1]:
        raise ValueError("controller_gate_disagreement")
    return protocol_path, root, (plans[0], plans[1])


def append_journal(
    stream: JournalStream,
    path: Path,
    parent: tuple[int, int],
    events: list[json_shapes.JsonObject],
    event: json_shapes.JsonObject,
) -> None:
    if session.private_directory_identity(path.parent) != parent:
        raise ValueError("owned_directory_changed")
    existing, _ = admission.read_owned_receipt(path, parent, admission.MAX_JOURNAL)
    if existing != admission.encode_journal(events):
        raise ValueError("journal_changed")
    # The journal is tiny and bounded; rebuilding avoids a mutable chain-head token.
    previous = (
        admission.sha256_bytes(admission.encode_journal(events).splitlines(keepends=True)[-1])
        if events
        else "0" * 64
    )
    raw = admission.encode_journal_line(event, len(events), previous)
    if len(admission.encode_journal(events)) + len(raw) > admission.MAX_JOURNAL:
        raise ValueError("journal_byte_limit")
    session.verify_reserved_receipt(path, stream.fileno(), parent)
    if stream.write(raw) != len(raw):
        raise OSError("short_journal_write")
    stream.flush()
    os.fsync(stream.fileno())
    session.verify_reserved_receipt(path, stream.fileno(), parent)
    persisted, _ = admission.read_owned_receipt(path, parent, admission.MAX_JOURNAL)
    if persisted != existing + raw:
        raise ValueError("journal_readback_mismatch")
    events.append(event)


def write_result_exclusively(
    path: Path, parent: tuple[int, int], result: Mapping[str, object]
) -> None:
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        session.verify_reserved_receipt(path, descriptor, parent)
        raw = admission.canonical_bytes(result) + b"\n"
        if stream.write(raw) != len(raw):
            raise OSError("short_admission_write")
        stream.flush()
        os.fsync(descriptor)
        session.verify_reserved_receipt(path, descriptor, parent)


def sync_private_directory(path: Path, expected: tuple[int, int]) -> None:
    if session.private_directory_identity(path) != expected:
        raise ValueError("owned_directory_changed")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
        | getattr(os, "O_DIRECTORY", 0),
    )
    try:
        info = os.fstat(descriptor)
        if (info.st_dev, info.st_ino) != expected:
            raise ValueError("owned_directory_changed")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    if session.private_directory_identity(path) != expected:
        raise ValueError("owned_directory_changed")


def run_study(
    protocol_path: Path,
    pin: str,
    review_commit: str,
    root: Path,
    model_root: Path,
    evidence_root: Path,
) -> ControllerResult:
    """Own two once-only captures and consume immediate admission internally."""
    protocol_path, root, plans = prepare_execution_plans(
        protocol_path, pin, review_commit, root, model_root
    )
    if ".." in evidence_root.parts:
        raise ValueError("unsafe_evidence_root")
    evidence_root = evidence_root.absolute()
    parent_identity = session.private_directory_identity(evidence_root)
    header = json_shapes.require_object(
        admission.journal_header(plans), context="controller header"
    )
    slots = _strings(header["slots"])
    run_id = admission.sha256_bytes(
        admission.canonical_bytes(
            {key: header[key] for key in ("study_id", "protocol_sha256", "review_commit")}
        )
    )
    directory = evidence_root / ("run-" + run_id)
    # Revalidate exact plans before reserving persistent attempt ownership.
    for plan in plans:
        evidence = json_shapes.require_object(
            _plan_value(plan)["evidence"], context="controller evidence"
        )
        slot = evidence["slot_id"]
        if not isinstance(slot, str):
            raise ValueError("invalid_controller_context")
        if (
            gate.verify_execution_plan(
                protocol_path, pin, slot, review_commit, root, model_root
            ).payload
            != plan.payload
        ):
            raise ValueError("controller_gate_changed")
    if session.private_directory_identity(evidence_root) != parent_identity:
        raise ValueError("evidence_root_changed")
    directory.mkdir(mode=0o700)
    if session.private_directory_identity(evidence_root) != parent_identity:
        raise ValueError("evidence_root_changed")
    owned_parent = session.private_directory_identity(directory)
    journal_path = directory / "journal.jsonl"
    descriptor = os.open(journal_path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
    events: list[json_shapes.JsonObject] = []
    receipts: list[CaptureReceipt] = []
    dispositions: dict[str, Disposition] = dict.fromkeys(slots, "not-attempted")
    result: ControllerResult = {
        "status": "controller_failed",
        "error": "none",
        "admitted": False,
        "admission_before_blinding": False,
        "study_unlocked": False,
        "scoring_start": False,
        "run_id": run_id,
        "dispositions": dispositions,
        "limitations": [
            "at-most-once-per-evidence-root-study-protocol-review",
            "alternative-owner-roots-outside-deduplication-guarantee",
            "no-automatic-retry-or-resume",
            "start-does-not-prove-execution",
            "offline-reuse-requires-trusted-custody-handoff",
        ],
    }
    with os.fdopen(descriptor, "w+b") as stream:
        stage: FailureStage = "persistence"
        try:
            append_journal(stream, journal_path, owned_parent, events, header)
            # Persist the newly reserved directory entry before any child attempt.
            sync_private_directory(directory, owned_parent)
            sync_private_directory(evidence_root, parent_identity)
            for index, plan in enumerate(plans):
                slot, name = slots[index], f"slot-{index + 1}.json"
                receipt_path = directory / name
                if receipt_path.exists() or receipt_path.is_symlink():
                    raise ValueError("existing_slot_receipt")
                append_journal(
                    stream,
                    journal_path,
                    owned_parent,
                    events,
                    json_shapes.require_object(
                        admission.slot_started_record(slot, name), context="controller start event"
                    ),
                )
                if session.private_directory_identity(directory) != owned_parent:
                    raise ValueError("owned_directory_changed")
                dispositions[slot] = "attempted-outcome-unknown"
                stage = "capture"
                returned = primary.run_primary(
                    protocol_path, pin, slot, review_commit, root, model_root, receipt_path
                )
                stage = "readback"
                raw, identity = admission.read_owned_receipt(
                    receipt_path, owned_parent, admission.MAX_RECEIPT, synchronize=True
                )
                sync_private_directory(directory, owned_parent)
                returned_bytes = admission.canonical_bytes(returned)
                if admission.canonical_bytes(admission.parse_owned_receipt(raw)) != returned_bytes:
                    raise ValueError("primary_return_receipt_mismatch")
                row = CaptureReceipt(slot, name, identity, raw, returned_bytes)
                if (
                    returned.get("status") != "primary_session_captured"
                    or returned.get("error") != "none"
                ):
                    dispositions[slot] = "failed-receipt-retained"
                    failed = json_shapes.require_object(
                        admission.slot_captured_record(row), context="controller failed event"
                    )
                    failed["type"] = "slot_failed"
                    append_journal(stream, journal_path, owned_parent, events, failed)
                    raise ValueError("primary_capture_failed")
                stage = "capture_validation"
                admission.validate_captured_receipt(raw, plan)
                receipts.append(row)
                dispositions[slot] = "captured"
                append_journal(
                    stream,
                    journal_path,
                    owned_parent,
                    events,
                    json_shapes.require_object(
                        admission.slot_captured_record(row), context="controller complete event"
                    ),
                )
            sync_private_directory(directory, owned_parent)
            append_journal(
                stream,
                journal_path,
                owned_parent,
                events,
                {"type": "capture_complete", "dispositions": dict(dispositions)},
            )
            journal, journal_identity = admission.read_owned_receipt(
                journal_path, owned_parent, admission.MAX_JOURNAL
            )
            if journal != admission.encode_journal(events):
                raise ValueError("journal_readback_mismatch")
            owned = admission.issue_controller_capture(
                (protocol_path, pin, review_commit, root, model_root),
                plans,
                directory,
                owned_parent,
                descriptor,
                journal_identity,
                journal,
                tuple(receipts),
            )
            stage = "admission"
            admitted = json_shapes.require_object(
                admission.consume_controller_capture(owned), context="controller admission"
            )
            stage = "persistence"
            write_result_exclusively(directory / "admission.json", owned_parent, admitted)
            sync_private_directory(directory, owned_parent)
            persisted, _ = admission.read_owned_receipt(
                directory / "admission.json", owned_parent, admission.MAX_JOURNAL
            )
            if admission.canonical_bytes(
                admission.parse_owned_receipt(persisted)
            ) != admission.canonical_bytes(admitted):
                raise ValueError("admission_readback_mismatch")
            return {
                **result,
                "status": "controller_admitted_before_blinding",
                "admitted": True,
                "admission_before_blinding": True,
                "journal_sha256": admission.sha256_bytes(journal),
                "admission_sha256": admission.sha256_bytes(persisted),
            }
        except (
            ValueError,
            OSError,
            KeyError,
            TypeError,
            RuntimeError,
            ImportError,
            KeyboardInterrupt,
            SystemExit,
        ):
            result["error"] = "capture_or_admission_failed"
            result["failure_stage"] = stage
            if events and events[-1]["type"] == "capture_complete":
                try:
                    result["journal_sha256"] = admission.sha256_bytes(
                        admission.encode_journal(events)
                    )
                    write_result_exclusively(directory / "failure.json", owned_parent, result)
                    sync_private_directory(directory, owned_parent)
                except (ValueError, OSError):
                    result["outcome_persistence_error"] = "failure_outcome_persistence_failed"
            # A terminal sealed journal is never reopened or altered after admission starts.
            if not events or events[-1]["type"] != "capture_complete":
                try:
                    append_journal(
                        stream,
                        journal_path,
                        owned_parent,
                        events,
                        {
                            "type": "capture_failed",
                            "dispositions": dict(dispositions),
                            "failure_stage": stage,
                        },
                    )
                except (ValueError, OSError):
                    result["journal_persistence_error"] = "journal_persistence_failed"
            return result
