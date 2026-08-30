"""At most one attempt per slot within one evidence-root/study/protocol/review run.

Alternative owner-selected roots are outside that guarantee. No retry or resume
is inferred from partial files. Immediate private admission is not an offline
JSON provenance claim, global deduplication or permission to score/unblind.
"""

from __future__ import annotations

import os
from pathlib import Path

from tools import prospective_execution_gate as gate
from tools import prospective_native_protocol as native
from tools import prospective_observation_admission as admission
from tools import prospective_primary_session as primary
from tools import prospective_server_session as session


def _plans(protocol_path: Path, pin: str, review: str, root: Path, model_root: Path):
    if ".." in protocol_path.parts or type(review) is not str:
        raise ValueError("invalid_controller_context")
    root, protocol_path, _ = gate.freeze._repository(protocol_path, review, root)
    value, _ = native._validated_candidate(protocol_path, pin)
    slots = value["expected_slots"]
    plans = tuple(
        gate._verify(protocol_path, pin, slot, review, root, model_root) for slot in slots
    )
    if len(plans) != 2:
        raise ValueError("invalid_controller_denominator")
    common = []
    for plan in plans:
        current = plan.value()
        evidence = dict(current["evidence"])
        evidence.pop("slot_id")
        common.append(
            admission._canonical({"admission": current["admission"], "evidence": evidence})
        )
    if common[0] != common[1]:
        raise ValueError("controller_gate_disagreement")
    return protocol_path, root, plans


def _append(stream, path, parent, events: list[dict], event: dict) -> None:
    if session._directory(path.parent) != parent:
        raise ValueError("owned_directory_changed")
    existing, _ = admission._read(path, parent, admission.MAX_JOURNAL)
    if existing != admission._journal(events):
        raise ValueError("journal_changed")
    # The journal is tiny and bounded; rebuilding avoids a mutable chain-head token.
    previous = (
        admission._sha(admission._journal(events).splitlines(keepends=True)[-1])
        if events
        else "0" * 64
    )
    raw = admission._line(event, len(events), previous)
    if len(admission._journal(events)) + len(raw) > admission.MAX_JOURNAL:
        raise ValueError("journal_byte_limit")
    session._reserved(path, stream.fileno(), parent)
    if stream.write(raw) != len(raw):
        raise OSError("short_journal_write")
    stream.flush()
    os.fsync(stream.fileno())
    session._reserved(path, stream.fileno(), parent)
    persisted, _ = admission._read(path, parent, admission.MAX_JOURNAL)
    if persisted != existing + raw:
        raise ValueError("journal_readback_mismatch")
    events.append(event)


def _write_result(path: Path, parent, result: dict) -> None:
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        session._reserved(path, descriptor, parent)
        raw = admission._canonical(result) + b"\n"
        if stream.write(raw) != len(raw):
            raise OSError("short_admission_write")
        stream.flush()
        os.fsync(descriptor)
        session._reserved(path, descriptor, parent)


def _sync_directory(path: Path, expected) -> None:
    if session._directory(path) != expected:
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
    if session._directory(path) != expected:
        raise ValueError("owned_directory_changed")


def run_study(
    protocol_path: Path,
    pin: str,
    review_commit: str,
    root: Path,
    model_root: Path,
    evidence_root: Path,
) -> dict:
    """Own two once-only captures and consume immediate admission internally."""
    protocol_path, root, plans = _plans(protocol_path, pin, review_commit, root, model_root)
    if ".." in evidence_root.parts:
        raise ValueError("unsafe_evidence_root")
    evidence_root = evidence_root.absolute()
    parent_identity = session._directory(evidence_root)
    header = admission._header(plans)
    run_id = admission._sha(
        admission._canonical(
            {key: header[key] for key in ("study_id", "protocol_sha256", "review_commit")}
        )
    )
    directory = evidence_root / ("run-" + run_id)
    # Revalidate exact plans before reserving persistent attempt ownership.
    for plan in plans:
        slot = plan.value()["evidence"]["slot_id"]
        if (
            gate._verify(protocol_path, pin, slot, review_commit, root, model_root).payload
            != plan.payload
        ):
            raise ValueError("controller_gate_changed")
    if session._directory(evidence_root) != parent_identity:
        raise ValueError("evidence_root_changed")
    directory.mkdir(mode=0o700)
    if session._directory(evidence_root) != parent_identity:
        raise ValueError("evidence_root_changed")
    owned_parent = session._directory(directory)
    journal_path = directory / "journal.jsonl"
    descriptor = os.open(journal_path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
    events, receipts = [], []
    slots = header["slots"]
    dispositions = {slot: "not-attempted" for slot in slots}
    result = {
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
        stage = "persistence"
        try:
            _append(stream, journal_path, owned_parent, events, header)
            # Persist the newly reserved directory entry before any child attempt.
            _sync_directory(directory, owned_parent)
            _sync_directory(evidence_root, parent_identity)
            for index, plan in enumerate(plans):
                slot, name = slots[index], f"slot-{index + 1}.json"
                receipt_path = directory / name
                if receipt_path.exists() or receipt_path.is_symlink():
                    raise ValueError("existing_slot_receipt")
                _append(stream, journal_path, owned_parent, events, admission._start(slot, name))
                if session._directory(directory) != owned_parent:
                    raise ValueError("owned_directory_changed")
                dispositions[slot] = "attempted-outcome-unknown"
                stage = "capture"
                returned = primary.run_primary(
                    protocol_path, pin, slot, review_commit, root, model_root, receipt_path
                )
                stage = "readback"
                raw, identity = admission._read(
                    receipt_path, owned_parent, admission.MAX_RECEIPT, synchronize=True
                )
                returned_bytes = admission._canonical(returned)
                if admission._canonical(admission._parse(raw)) != returned_bytes:
                    raise ValueError("primary_return_receipt_mismatch")
                row = admission._Receipt(slot, name, identity, raw, returned_bytes)
                if (
                    returned.get("status") != "primary_session_captured"
                    or returned.get("error") != "none"
                ):
                    dispositions[slot] = "failed-receipt-retained"
                    failed = admission._complete(row)
                    failed["type"] = "slot_failed"
                    _append(stream, journal_path, owned_parent, events, failed)
                    raise ValueError("primary_capture_failed")
                stage = "capture_validation"
                admission._validate_receipt(raw, plan)
                receipts.append(row)
                dispositions[slot] = "captured"
                _append(stream, journal_path, owned_parent, events, admission._complete(row))
            _sync_directory(directory, owned_parent)
            _append(
                stream,
                journal_path,
                owned_parent,
                events,
                {"type": "capture_complete", "dispositions": dict(dispositions)},
            )
            journal, journal_identity = admission._read(
                journal_path, owned_parent, admission.MAX_JOURNAL
            )
            if journal != admission._journal(events):
                raise ValueError("journal_readback_mismatch")
            owned = admission._issue(
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
            admitted = admission._consume(owned)
            stage = "persistence"
            _write_result(directory / "admission.json", owned_parent, admitted)
            _sync_directory(directory, owned_parent)
            persisted, _ = admission._read(
                directory / "admission.json", owned_parent, admission.MAX_JOURNAL
            )
            if admission._canonical(admission._parse(persisted)) != admission._canonical(admitted):
                raise ValueError("admission_readback_mismatch")
            return {
                **result,
                "status": "controller_admitted_before_blinding",
                "admitted": True,
                "admission_before_blinding": True,
                "journal_sha256": admission._sha(journal),
                "admission_sha256": admission._sha(persisted),
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
                    result["journal_sha256"] = admission._sha(admission._journal(events))
                    _write_result(directory / "failure.json", owned_parent, result)
                    _sync_directory(directory, owned_parent)
                except (ValueError, OSError):
                    result["outcome_persistence_error"] = "failure_outcome_persistence_failed"
            # A terminal sealed journal is never reopened or altered after admission starts.
            if not events or events[-1]["type"] != "capture_complete":
                try:
                    _append(
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
