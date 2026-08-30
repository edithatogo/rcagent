"""Synthetic rejection paths across capture and the one-shot admission boundary."""

import dataclasses
import json

import pytest

from tests.test_prospective_execution_gate import synthetic as synthetic
from tests.test_prospective_study_controller import capture_fixture as capture_fixture
from tools import prospective_observation_admission as admission
from tools import prospective_study_controller as controller


def reissue_for_test(owned, **changes):
    """Explicit fixture injection, never an offline/public capability constructor."""
    fields = {
        field.name: getattr(owned, field.name)
        for field in dataclasses.fields(owned)
        if field.name != "origin"
    }
    fields.update(changes)
    return admission._issue(**fields)


def test_untrusted_origin_cannot_construct_capture_witness(tmp_path):
    plan = admission.gate._Plan(b"{}")
    receipt = admission._Receipt("synthetic-slot", "slot.json", (1, 3), b"{}", b"{}")
    with pytest.raises(ValueError, match="invalid_capture_capability"):
        admission._OwnedRun(
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
    "field,value,reason",
    [
        ("request_sha256", "0" * 64, "capture_request_mismatch"),
        ("source_sha256", {"synthetic": "0" * 64}, "capture_source_mismatch"),
        ("profile_sha256", "0" * 64, "capture_source_mismatch"),
        ("arguments", ["synthetic-wrong-executable"], "capture_arguments_mismatch"),
    ],
)
def test_request_source_and_arguments_bound_before_next_capture(
    capture_fixture, monkeypatch, field, value, reason
):
    args, calls, capture = capture_fixture
    original_validate = admission._validate_receipt
    observed = []

    def changed(*parameters):
        result = capture(*parameters)
        result[field] = value
        parameters[-1].write_bytes(admission._canonical(result) + b"\n")
        return result

    def validate(raw, plan):
        with pytest.raises(ValueError, match=reason) as rejected:
            original_validate(raw, plan)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(controller.primary, "run_primary", changed)
    monkeypatch.setattr(admission, "_validate_receipt", validate)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1
    assert observed == [reason]


@pytest.mark.parametrize(
    "damage,reason",
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
    capture_fixture, monkeypatch, damage, reason
):
    args, calls, _ = capture_fixture
    original_consume = admission._consume
    observed = []

    def corrupted(owned):
        changes = {}
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
            events = [json.loads(line)["event"] for line in owned.journal.splitlines()]
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
        mutated = reissue_for_test(owned, **changes)
        admission._LIVE.discard(owned)
        with pytest.raises(ValueError, match=reason) as rejected:
            original_consume(mutated)
        with pytest.raises(ValueError, match="invalid_or_consumed_capture_capability"):
            original_consume(mutated)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(admission, "_consume", corrupted)
    result = controller.run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is result["scoring_start"] is False
    assert result["failure_stage"] == "admission"
    assert observed == [reason]
    with pytest.raises(FileExistsError):
        controller.run_study(*args)
    assert len(calls) == 2


def test_gate_drift_during_immediate_admission_rejects_capture(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    original_consume = admission._consume
    original_verify = admission.gate._verify
    observed = []

    def changed_verify(*parameters):
        plan = original_verify(*parameters)
        return admission.gate._Plan(plan.payload + b" ")

    def consume(owned):
        with monkeypatch.context() as patch:
            patch.setattr(admission.gate, "_verify", changed_verify)
            with pytest.raises(ValueError, match="admission_gate_changed") as rejected:
                original_consume(owned)
        observed.append(str(rejected.value))
        raise rejected.value

    monkeypatch.setattr(admission, "_consume", consume)
    result = controller.run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is False
    assert observed == ["admission_gate_changed"]
