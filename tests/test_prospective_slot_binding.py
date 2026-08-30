"""Synthetic binding candidates never launch a model or admit study evidence."""

import copy
import json

import pytest

from tests.test_prospective_native_protocol import fixture as native_fixture
from tests.test_prospective_protocol import pin
from tools import prospective_slot_binding as subject


@pytest.fixture
def synthetic(tmp_path, monkeypatch):
    path, value = native_fixture(tmp_path)
    condition = value["condition"]
    receipt = {
        key: condition[key]
        for key in (
            "model_id",
            "model_revision",
            "model_sha256",
            "profile_sha256",
            "registry_sha256",
        )
    }
    receipt.update(
        purpose="local-artefact-eligibility-only",
        local_artifact_eligible=True,
        admitted=False,
        study_unlocked=False,
        profile_id="synthetic-profile",
        model_path="/private/synthetic/model",
        model_license_path="/private/synthetic/LICENSE",
        runtime_overlay={
            "executable_sha256": condition["runtime_sha256"],
            "profile_sha256": condition["profile_sha256"],
            "profile_id": "synthetic-profile",
            "executable": "/private/synthetic/runtime",
        },
    )
    seal(receipt)
    calls = []

    def admit(root):
        calls.append(root)
        return receipt

    monkeypatch.setattr(subject.model, "admit_model", admit)
    return path, value, receipt, calls, tmp_path / "synthetic-cache"


def seal(receipt):
    receipt.pop("admission_sha256", None)
    receipt["admission_sha256"] = subject.model.digest(receipt)


def test_binding_entrypoint_exists():
    assert callable(subject.bind_slot)


@pytest.mark.parametrize("index", [0, 1])
def test_selects_exact_slot_with_private_path_free_projection(synthetic, index):
    path, value, receipt, calls, root = synthetic
    slot = value["expected_slots"][index]
    result = subject.bind_slot(path, pin(path), slot, root)
    assert calls == [root]
    assert result["slot_id"] == slot
    assert result["condition_declared"] == value["condition"]
    assert result["eligibility"]["admission_sha256"] == receipt["admission_sha256"]
    assert (
        result["request"] == subject.protocol.validate_protocol(path, pin(path))["requests"][slot]
    )
    assert result["execution_observed"] is result["admitted"] is result["study_unlocked"] is False
    assert result["adapter_verified"] is False
    assert "/private/" not in json.dumps(result)
    receipt["profile_id"] = "changed"
    value["condition"]["adapter_sha256"] = "changed"
    assert result["eligibility"]["profile_id"] == "synthetic-profile"
    assert result["condition_declared"]["adapter_sha256"] == "e" * 64


@pytest.mark.parametrize(
    "slot",
    [
        None,
        [],
        3,
        "",
        "case-other__condition-local-text__r1",
        "case-a__condition-local-text__r2",
        "a" * 151,
    ],
)
def test_invalid_slots_never_reach_model_eligibility(synthetic, slot):
    path, _, _, calls, root = synthetic
    with pytest.raises(ValueError, match="slot_not_in_protocol"):
        subject.bind_slot(path, pin(path), slot, root)
    assert calls == []


@pytest.mark.parametrize(
    "field",
    [
        "model_id",
        "model_revision",
        "model_sha256",
        "runtime_sha256",
        "profile_sha256",
        "registry_sha256",
    ],
)
def test_each_declared_identity_must_match(synthetic, field):
    path, value, receipt, _, root = synthetic
    if field == "runtime_sha256":
        receipt["runtime_overlay"]["executable_sha256"] = "0" * 64
    else:
        receipt[field] = "0" * 64
        if field == "profile_sha256":
            receipt["runtime_overlay"][field] = receipt[field]
    seal(receipt)
    with pytest.raises(ValueError, match="condition_eligibility_mismatch"):
        subject.bind_slot(path, pin(path), value["expected_slots"][0], root)


@pytest.mark.parametrize(
    "damage",
    [
        "purpose",
        "eligible",
        "admitted",
        "study",
        "missing",
        "overlay",
        "profile-id",
        "profile-drift",
        "profile-pin",
        "digest",
        "identity-type",
        "receipt-type",
    ],
)
def test_malformed_or_inconsistent_eligibility_rejected(synthetic, monkeypatch, damage):
    path, value, receipt, _, root = synthetic
    if damage == "purpose":
        receipt["purpose"] = "other"
    elif damage == "eligible":
        receipt["local_artifact_eligible"] = 1
    elif damage == "admitted":
        receipt["admitted"] = True
    elif damage == "study":
        receipt["study_unlocked"] = 0
    elif damage == "missing":
        del receipt["model_revision"]
    elif damage == "overlay":
        receipt["runtime_overlay"] = []
    elif damage == "profile-id":
        receipt["profile_id"] = ""
    elif damage == "profile-drift":
        receipt["runtime_overlay"]["profile_id"] = "other"
    elif damage == "profile-pin":
        receipt["runtime_overlay"]["profile_sha256"] = "0" * 64
    elif damage == "identity-type":
        receipt["model_id"] = None
    elif damage == "receipt-type":
        monkeypatch.setattr(subject.model, "admit_model", lambda root: [])
    seal(receipt)
    if damage == "digest":
        receipt["admission_sha256"] = "0" * 64
    with pytest.raises(ValueError):
        subject.bind_slot(path, pin(path), value["expected_slots"][0], root)


def test_protocol_ref_failure_precedes_eligibility(synthetic):
    path, value, _, calls, root = synthetic
    (path.parent / value["cases"][0]["input"]["path"]).write_bytes(b"altered")
    with pytest.raises(ValueError):
        subject.bind_slot(path, pin(path), value["expected_slots"][0], root)
    assert calls == []


def test_model_failure_is_not_replaced_with_candidate(synthetic, monkeypatch):
    path, value, _, _, root = synthetic

    def reject(root):
        raise ValueError("synthetic_eligibility_failure")

    monkeypatch.setattr(subject.model, "admit_model", reject)
    with pytest.raises(ValueError, match="synthetic_eligibility_failure"):
        subject.bind_slot(path, pin(path), value["expected_slots"][0], root)


def test_protocol_changed_during_eligibility_cannot_replace_bound_snapshot(synthetic, monkeypatch):
    path, value, receipt, _, root = synthetic
    slot = value["expected_slots"][0]
    expected_request = subject.protocol.validate_protocol(path, pin(path))["requests"][slot]
    receipt["private_extra"] = "SYNTHETIC_PRIVATE_SENTINEL"
    seal(receipt)

    def change_after_protocol(root):
        path.write_bytes(b"changed while eligibility checked")
        return receipt

    monkeypatch.setattr(subject.model, "admit_model", change_after_protocol)
    expected_pin = pin(path)
    result = subject.bind_slot(path, expected_pin, slot, root)
    assert result["request"] == expected_request
    assert result["protocol_sha256"] == expected_pin != pin(path)
    assert "SYNTHETIC_PRIVATE_SENTINEL" not in json.dumps(result)
    assert result["adapter_verified"] is False


def test_no_reread_or_alias_after_protocol_validation(synthetic, monkeypatch):
    path, value, _, _, root = synthetic
    original = subject.protocol._validated_candidate
    snapshots = []

    def changed_after_validation(*args):
        parsed, candidate = original(*args)
        snapshots.extend((parsed, candidate))
        path.write_bytes(b"changed protocol after validated snapshot")
        for case in parsed["cases"]:
            (path.parent / case["input"]["path"]).write_bytes(b"changed input")
        return parsed, candidate

    monkeypatch.setattr(subject.protocol, "_validated_candidate", changed_after_validation)
    protocol_pin = pin(path)
    slot = value["expected_slots"][0]
    result = subject.bind_slot(path, protocol_pin, slot, root)
    expected = copy.deepcopy(result)
    snapshots[0]["condition"]["adapter_sha256"] = "changed"
    snapshots[1]["requests"][slot]["generation"]["seed"] = 0
    assert result == expected
    assert result["protocol_sha256"] == protocol_pin != pin(path)
    assert "atomic-filesystem-snapshot-unverified" in result["limitations"]
