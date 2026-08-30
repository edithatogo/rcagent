"""Read-only slot/declaration eligibility consistency; never launch or admit."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from tools import prospective_native_protocol as protocol
from tools import prospective_server_model as model
from tools.evaluation_preflight import _digest


def bind_slot(
    protocol_path: Path, expected_protocol_sha256: str, slot_id: str, model_root: Path
) -> dict:
    """Select a declared slot before checking fresh local artefact eligibility."""
    value, candidate = protocol._validated_candidate(protocol_path, expected_protocol_sha256)
    if type(slot_id) is not str or len(slot_id) > 150 or slot_id not in candidate["requests"]:
        raise ValueError("slot_not_in_protocol")
    receipt = model.admit_model(model_root)
    try:
        if (
            type(receipt) is not dict
            or receipt["purpose"] != "local-artefact-eligibility-only"
            or receipt["local_artifact_eligible"] is not True
            or receipt["admitted"] is not False
            or receipt["study_unlocked"] is not False
        ):
            raise ValueError("invalid_eligibility_receipt")
        overlay = receipt["runtime_overlay"]
        if (
            type(overlay) is not dict
            or type(receipt["profile_id"]) is not str
            or not receipt["profile_id"]
            or len(receipt["profile_id"]) > 150
            or overlay["profile_id"] != receipt["profile_id"]
            or overlay["profile_sha256"] != receipt["profile_sha256"]
        ):
            raise ValueError("invalid_eligibility_receipt")
        pin = receipt["admission_sha256"]
        unsigned = {key: item for key, item in receipt.items() if key != "admission_sha256"}
        if not _digest(pin) or model.digest(unsigned) != pin:
            raise ValueError("invalid_eligibility_receipt")
        observed = {
            key: receipt[key]
            for key in (
                "model_id",
                "model_revision",
                "model_sha256",
                "profile_sha256",
                "registry_sha256",
            )
        }
        observed["runtime_sha256"] = overlay["executable_sha256"]
        condition = value["condition"]
        if any(type(item) is not str or item != condition[key] for key, item in observed.items()):
            raise ValueError("condition_eligibility_mismatch")
    except (KeyError, TypeError, OverflowError, RecursionError):
        raise ValueError("invalid_eligibility_receipt") from None
    return {
        "status": "slot_binding_candidate",
        "protocol_sha256": candidate["protocol_sha256"],
        "study_id": candidate["study_id"],
        "slot_id": slot_id,
        "condition_declared": deepcopy(condition),
        "request": deepcopy(candidate["requests"][slot_id]),
        "eligibility": {**observed, "profile_id": receipt["profile_id"], "admission_sha256": pin},
        "adapter_verified": False,
        "execution_observed": False,
        "admitted": False,
        "study_unlocked": False,
        "limitations": [
            "point-in-time-filesystem-eligibility-consistency-only",
            "atomic-filesystem-snapshot-unverified",
            "loaded-identity-unverified",
            "freeze-unverified",
            "privacy-and-data-class-unverified",
            "adapter-unverified",
            "request-response-binding-unverified",
            "not-study-admission",
        ],
    }
