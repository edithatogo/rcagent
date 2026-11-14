"""Read-only slot/declaration eligibility consistency; never launch or admit."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Literal, TypedDict

from tools import json_shapes
from tools import prospective_native_protocol as protocol
from tools import prospective_runner_contract as runner
from tools import prospective_server_model as model
from tools.evaluation_preflight import is_sha256


class SlotEligibility(TypedDict):
    model_id: str
    model_revision: str
    model_sha256: str
    profile_sha256: str
    registry_sha256: str
    runtime_sha256: str
    profile_id: str
    admission_sha256: str


class SlotBinding(TypedDict):
    status: Literal["slot_binding_candidate"]
    protocol_sha256: str
    study_id: str
    slot_id: str
    condition_declared: dict[str, str]
    request: runner.RequestPackage
    eligibility: SlotEligibility
    adapter_verified: Literal[False]
    execution_observed: Literal[False]
    admitted: Literal[False]
    study_unlocked: Literal[False]
    limitations: list[str]


def bind_slot(
    protocol_path: Path, expected_protocol_sha256: str, slot_id: object, model_root: Path
) -> SlotBinding:
    """Select a declared slot before checking fresh local artefact eligibility."""
    value, candidate = protocol.validated_candidate(protocol_path, expected_protocol_sha256)
    if type(slot_id) is not str or len(slot_id) > 150 or slot_id not in candidate["requests"]:
        raise ValueError("slot_not_in_protocol")
    returned: object = model.admit_model(model_root)
    try:
        if not json_shapes.is_object(returned) or type(returned) is not dict:
            raise ValueError("invalid_eligibility_receipt")
        receipt = returned
        if (
            receipt["purpose"] != "local-artefact-eligibility-only"
            or receipt["local_artifact_eligible"] is not True
            or receipt["admitted"] is not False
            or receipt["study_unlocked"] is not False
        ):
            raise ValueError("invalid_eligibility_receipt")
        overlay = receipt["runtime_overlay"]
        profile_id = receipt["profile_id"]
        if (
            not json_shapes.is_object(overlay)
            or type(overlay) is not dict
            or type(profile_id) is not str
            or not profile_id
            or len(profile_id) > 150
            or overlay["profile_id"] != profile_id
            or overlay["profile_sha256"] != receipt["profile_sha256"]
        ):
            raise ValueError("invalid_eligibility_receipt")
        pin = receipt["admission_sha256"]
        unsigned = {key: item for key, item in receipt.items() if key != "admission_sha256"}
        if not isinstance(pin, str) or not is_sha256(pin) or model.digest(unsigned) != pin:
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
        checked: dict[str, str] = {}
        for key, item in observed.items():
            if type(item) is not str or item != condition[key]:
                raise ValueError("condition_eligibility_mismatch")
            checked[key] = item
    except (KeyError, TypeError, OverflowError, RecursionError):
        raise ValueError("invalid_eligibility_receipt") from None
    return {
        "status": "slot_binding_candidate",
        "protocol_sha256": candidate["protocol_sha256"],
        "study_id": candidate["study_id"],
        "slot_id": slot_id,
        "condition_declared": deepcopy(condition),
        "request": deepcopy(candidate["requests"][slot_id]),
        "eligibility": {
            "model_id": checked["model_id"],
            "model_revision": checked["model_revision"],
            "model_sha256": checked["model_sha256"],
            "profile_sha256": checked["profile_sha256"],
            "registry_sha256": checked["registry_sha256"],
            "runtime_sha256": checked["runtime_sha256"],
            "profile_id": profile_id,
            "admission_sha256": pin,
        },
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
