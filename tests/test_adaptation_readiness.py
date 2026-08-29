from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools.adaptation_readiness import (
    assess_readiness,
    build_rejection_card,
    canonical_hash,
    validate_dataset_manifest,
    validate_experiment_proposal,
    validate_registry,
)

ROOT = Path(__file__).parents[1]


def registry() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/registry.json").read_text())


def dataset() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/dataset-manifest.json").read_text())


def dependencies() -> dict:
    return {name: "archived_passing" for name in ("benchmark", "multimodal", "retrieval", "runtime_lab", "privacy", "jurisdiction")}


def readiness() -> dict:
    return assess_readiness(registry(), dataset(), dependencies())


def proposal(level: str = "prompt") -> dict:
    return {
        "experiment_id":"syn-proposal-1","level":level,"data_class":"generated_synthetic",
        "base_revision":"not_acquired","framework_revision":"not_acquired","seed":0,
        "compute_budget":"none","network":"none","telemetry":"none","remote_code":False,
        "execute":False,"readiness_sha256":readiness()["receipt_sha256"],
        "rollback":["discard proposal"],"stop_conditions":["readiness remains false"],
    }


def test_registry_and_dataset_contracts_pass() -> None:
    assert validate_registry(registry()) == []
    assert validate_dataset_manifest(dataset()) == []
    assert registry()["comparators"] == []


@pytest.mark.parametrize("value", [None, [], "bad"])
def test_registry_rejects_non_objects(value: object) -> None:
    assert validate_registry(value) == ["registry must be an object"]


def test_registry_fails_closed_on_policy_framework_and_comparator_drift() -> None:
    value = registry()
    value["extra"] = True
    value["schema_version"] = "2"
    value["policy"]["training"] = True
    value["frameworks"].append(dict(value["frameworks"][0]))
    value["frameworks"][0].update(status="supported", revision="main", licence="Apache-2.0", network="used", telemetry="used", remote_code=True)
    value["comparators"] = [{"id":"invented"}]
    value["readiness_thresholds"] = {}
    errors = validate_registry(value)
    assert "registry fields are invalid" in errors
    assert "policy.training must be False" in errors
    assert "frameworks[4].id is invalid or duplicated" in errors
    assert "comparators must remain empty without admitted exact revisions" in errors


def test_registry_rejects_malformed_collections() -> None:
    value = registry()
    value.update(policy=[], frameworks=[None, {}], comparators="bad", readiness_thresholds=[])
    errors = validate_registry(value)
    assert "policy fields are invalid" in errors
    assert "frameworks[0] fields are invalid" in errors
    assert "frameworks[1].id is invalid or duplicated" not in errors


@pytest.mark.parametrize("value", [None, [], "bad"])
def test_dataset_rejects_non_objects(value: object) -> None:
    assert validate_dataset_manifest(value) == ["dataset manifest must be an object"]


def test_dataset_rejects_rights_private_overlap_hash_and_split_drift() -> None:
    value = dataset()
    value["extra"] = True
    value.update(schema_version="2", data_class="public", origin="third_party", rights="unknown", consent="unknown", private_data=True, redistribution=True)
    value["splits"][1]["item_ids"] = value["splits"][0]["item_ids"]
    value["splits"][2]["sha256"] = "0" * 64
    errors = validate_dataset_manifest(value)
    assert "dataset manifest fields are invalid" in errors
    assert "dataset must be repository-authored generated synthetic" in errors
    assert "dataset rights or consent state is invalid" in errors
    assert "dataset splits overlap" in errors
    assert "dataset manifest hash mismatched" in errors


def test_dataset_rejects_malformed_splits_and_empty_governance() -> None:
    value = dataset()
    value.update(purpose="", deletion="", splits=[None, {}])
    errors = validate_dataset_manifest(value)
    assert "dataset purpose must be a non-empty string" in errors
    assert "dataset splits are incomplete" in errors


def test_readiness_is_hash_bound_negative_and_schema_valid() -> None:
    result = readiness()
    assert result["decision"] == "not_ready_reject_weight_adaptation"
    assert result["ready"] is False
    assert result["training_executed"] is False
    unsigned = {key:value for key,value in result.items() if key != "receipt_sha256"}
    assert result["receipt_sha256"] == canonical_hash(unsigned)
    schema = json.loads((ROOT / "conductor/schemas/adaptation-readiness.schema.json").read_text())
    assert list(Draft202012Validator(schema).iter_errors(result)) == []
    checked = json.loads((ROOT / "evaluation/adaptation/readiness-20260829.json").read_text())
    assert result == checked


def test_readiness_records_invalid_inputs_without_raising() -> None:
    result = assess_readiness({}, {}, None)
    assert result["ready"] is False
    assert "adaptation registry is invalid" in result["reasons"]
    assert "dataset manifest is invalid" in result["reasons"]
    assert "dependency state must be an object" in result["reasons"]


def test_safe_non_weight_proposal_is_dry_run_only() -> None:
    assert validate_experiment_proposal(proposal(), readiness()) == []


def test_proposal_rejects_weight_update_execution_private_remote_and_forgery() -> None:
    value = proposal("weight_update")
    value.update(data_class="governed_private", base_revision="model", framework_revision="main", compute_budget="paid", network="internet", telemetry="wandb", remote_code=True, execute=True, readiness_sha256="0"*64, rollback=[], stop_conditions=[])
    errors = validate_experiment_proposal(value, readiness())
    assert "weight-affecting experiment is blocked" in errors
    assert "experiment execution is not authorised" in errors
    assert "proposal is not bound to the negative readiness receipt" in errors


def test_proposal_rejects_non_object_unknown_level_and_fields() -> None:
    assert validate_experiment_proposal([],{}) == ["experiment proposal must be an object"]
    value = proposal()
    value.update(level="unknown", extra=True)
    assert validate_experiment_proposal(value, readiness())


def test_rejection_card_proves_no_artefact_or_release() -> None:
    card = build_rejection_card(readiness(), dataset())
    assert card["artefact_status"] == "no_adapted_artefact_created"
    assert card["training_executed"] is False
    assert card["release_performed"] is False
    assert card["receipt_sha256"] == canonical_hash({key:value for key,value in card.items() if key != "receipt_sha256"})
    assert card == json.loads((ROOT / "evaluation/adaptation/rejection-card-20260829.json").read_text())


def test_rejection_card_rejects_forged_positive_or_invalid_dataset() -> None:
    positive = readiness()
    positive["ready"] = True
    with pytest.raises(ValueError, match="negative readiness"):
        build_rejection_card(positive, dataset())
    bad = dataset()
    bad["private_data"] = True
    with pytest.raises(ValueError, match="valid generated-synthetic"):
        build_rejection_card(readiness(), bad)
