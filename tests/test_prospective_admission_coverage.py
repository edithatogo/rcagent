"""Synthetic rejection paths across capture and the one-shot admission boundary."""

import dataclasses
import json
from pathlib import Path
from typing import Never, TypedDict

import pytest

from tests.prospective_fixture_types import (
    CaptureFixture,
    ObjectMap,
    PrimaryArgs,
    VerifyArgs,
    mapping,
    mapping_call,
)
from tests.test_prospective_execution_gate import synthetic as synthetic
from tests.test_prospective_study_controller import capture_fixture as capture_fixture
from tools import prospective_observation_admission as admission
from tools import prospective_study_controller as controller
from tools.prospective_execution_gate import _Plan
from tools.prospective_observation_admission import _OwnedRun, _Receipt


class WitnessOverrides(TypedDict, total=False):
    parent_identity: tuple[int, int]
    journal: bytes
    receipts: tuple[_Receipt, ...]


run_study = mapping_call(controller.run_study)


def reissue_for_test(owned: _OwnedRun, changes: WitnessOverrides) -> _OwnedRun:
    """Explicit fixture injection, never an offline/public capability constructor."""
    return admission._issue(
        context=owned.context,
        plans=owned.plans,
        directory=owned.directory,
        parent_identity=changes.get("parent_identity", owned.parent_identity),
        journal_fd=owned.journal_fd,
        journal_identity=owned.journal_identity,
        journal=changes.get("journal", owned.journal),
        receipts=changes.get("receipts", owned.receipts),
    )


def test_untrusted_origin_cannot_construct_capture_witness(tmp_path: Path) -> None:
    plan = _Plan(b"{}")
    receipt = _Receipt("synthetic-slot", "slot.json", (1, 3), b"{}", b"{}")
    with pytest.raises(ValueError, match="invalid_capture_capability"):
        _OwnedRun(
            object(),
            (tmp_path, "a" * 64, "b" * 40, tmp_path, tmp_path),
            (plan, plan),
            tmp_path,
            (1, 2),
            -1,
            (1, 3),
            b"",
            (receipt, receipt),
        )


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("request_sha256", "0" * 64, "capture_request_mismatch"),
        ("source_sha256", {"synthetic": "0" * 64}, "capture_source_mismatch"),
        ("profile_sha256", "0" * 64, "capture_source_mismatch"),
        ("arguments", ["synthetic-wrong-executable"], "capture_arguments_mismatch"),
    ],
)
def test_request_source_and_arguments_bound_before_next_capture(
    capture_fixture: CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
    reason: str,
) -> None:
    args, calls, capture = capture_fixture
    original_validate = admission._validate_receipt
    observed: list[str] = []

    def changed(*parameters: *PrimaryArgs) -> ObjectMap:
        result = capture(*parameters)
        result[field] = value
        parameters[-1].write_bytes(admission._canonical(result) + b"\n")
        return result

    def validate(raw: bytes, plan: _Plan) -> Never:
        with pytest.raises(ValueError, match=reason) as rejected:
            original_validate(raw, plan)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(controller.primary, "run_primary", changed)
    monkeypatch.setattr(admission, "_validate_receipt", validate)
    result = run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1
    assert observed == [reason]


@pytest.mark.parametrize(
    ("damage", "reason"),
    [
        ("duplicate-slot", "incomplete_capture_denominator"),
        ("parent-identity", "owned_directory_changed"),
        ("journal-snapshot", "owned_journal_changed"),
        ("receipt-name", "invalid_owned_receipt_name"),
        ("receipt-snapshot", "owned_receipt_changed"),
        ("returned-snapshot", "owned_receipt_changed"),
        ("journal-extra-event", "owned_journal_chain_mismatch"),
        ("missing-capture-field", "invalid_owned_capture"),
    ],
)
def test_postcapture_owned_evidence_rejection_consumes_witness(
    capture_fixture: CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    damage: str,
    reason: str,
) -> None:
    args, calls, _ = capture_fixture
    original_consume = admission._consume
    observed: list[str] = []

    def corrupted(owned: object) -> Never:
        assert isinstance(owned, _OwnedRun)
        changes: WitnessOverrides = {}
        receipts = owned.receipts
        first = receipts[0]
        if damage == "duplicate-slot":
            changes["receipts"] = (first, dataclasses.replace(receipts[1], slot=first.slot))
        elif damage == "parent-identity":
            changes["parent_identity"] = (-1, -1)
        elif damage == "journal-snapshot":
            changes["journal"] = owned.journal + b"changed"
        elif damage == "receipt-name":
            changes["receipts"] = (dataclasses.replace(first, name="wrong.json"), receipts[1])
        elif damage == "receipt-snapshot":
            changes["receipts"] = (dataclasses.replace(first, raw=b"changed"), receipts[1])
        elif damage == "returned-snapshot":
            changes["receipts"] = (dataclasses.replace(first, returned=b"{}"), receipts[1])
        elif damage == "journal-extra-event":
            events = [
                mapping(mapping(json.loads(line))["event"]) for line in owned.journal.splitlines()
            ]
            events.append({"type": "untrusted-extra-event"})
            journal = admission._journal(events)
            (owned.directory / "journal.jsonl").write_bytes(journal)
            changes["journal"] = journal
        else:
            value = admission._parse(first.raw)
            del value["primary_gate"]
            raw = admission._canonical(value) + b"\n"
            (owned.directory / first.name).write_bytes(raw)
            changes["receipts"] = (
                dataclasses.replace(first, raw=raw, returned=admission._canonical(value)),
                receipts[1],
            )
        mutated = reissue_for_test(owned, changes)
        admission._LIVE.discard(owned)
        with pytest.raises(ValueError, match=reason) as rejected:
            original_consume(mutated)
        with pytest.raises(ValueError, match="invalid_or_consumed_capture_capability"):
            original_consume(mutated)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(admission, "_consume", corrupted)
    result = run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is result["scoring_start"] is False
    assert "failure_stage" in result
    assert result["failure_stage"] == "admission"
    assert observed == [reason]
    with pytest.raises(FileExistsError):
        run_study(*args)
    assert len(calls) == 2


def test_gate_drift_during_immediate_admission_rejects_capture(
    capture_fixture: CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    args, calls, _ = capture_fixture
    original_consume = admission._consume
    original_verify = admission.gate._verify
    observed: list[str] = []

    def changed_verify(*parameters: *VerifyArgs) -> _Plan:
        plan = original_verify(*parameters)
        return _Plan(plan.payload + b" ")

    def consume(owned: object) -> Never:
        with monkeypatch.context() as patch:
            patch.setattr(admission.gate, "_verify", changed_verify)
            with pytest.raises(ValueError, match="admission_gate_changed") as rejected:
                original_consume(owned)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(admission, "_consume", consume)
    result = run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is False
    assert observed == ["admission_gate_changed"]
