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
    validate_dependency_manifest,
    validate_evidence_matrix,
    validate_experiment_proposal,
    validate_readiness_receipt,
    validate_registry,
)

ROOT = Path(__file__).parents[1]


def registry() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/registry.json").read_text())


def dataset() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/dataset-manifest.json").read_text())


def dependencies() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/dependencies.json").read_text())


def evidence_matrix() -> dict:
    return json.loads((ROOT / "evaluation/adaptation/evidence-availability-matrix.json").read_text())


def readiness() -> dict:
    return assess_readiness(registry(), dataset(), dependencies(), ROOT)


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
    assert validate_dependency_manifest(dependencies(), ROOT) == []
    assert dataset()["data_materialised"] is False
    assert dataset()["units"] == []


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
    value["splits"][1]["item_ids"] = ["syn-should-not-exist"]
    value["splits"][2]["sha256"] = "0" * 64
    errors = validate_dataset_manifest(value)
    assert "dataset manifest fields are invalid" in errors
    assert "dataset must be repository-authored generated synthetic" in errors
    assert "dataset rights or consent state is invalid" in errors
    assert "splits[1].item_ids must remain empty until data are materialised" in errors
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
    result = assess_readiness({}, {}, None, ROOT)
    assert result["ready"] is False
    assert "adaptation registry is invalid" in result["reasons"]
    assert "dataset manifest is invalid" in result["reasons"]
    assert "dependency evidence is incomplete" in result["reasons"]


def test_safe_non_weight_proposal_is_dry_run_only() -> None:
    assert validate_experiment_proposal(proposal(), readiness(), registry=registry(), dataset=dataset(), dependencies=dependencies()) == []


def test_proposal_rejects_weight_update_execution_private_remote_and_forgery() -> None:
    value = proposal("weight_update")
    value.update(data_class="governed_private", base_revision="model", framework_revision="main", compute_budget="paid", network="internet", telemetry="wandb", remote_code=True, execute=True, readiness_sha256="0"*64, rollback=[], stop_conditions=[])
    errors = validate_experiment_proposal(value, readiness(), registry=registry(), dataset=dataset(), dependencies=dependencies())
    assert "weight-affecting experiment is blocked" in errors
    assert "experiment execution is not authorised" in errors
    assert "proposal is not bound to the negative readiness receipt" in errors


def test_proposal_rejects_non_object_unknown_level_and_fields() -> None:
    assert validate_experiment_proposal([], {}, registry=registry(), dataset=dataset(), dependencies=dependencies()) == ["experiment proposal must be an object"]
    value = proposal()
    value.update(level="unknown", extra=True)
    assert validate_experiment_proposal(value, readiness(), registry=registry(), dataset=dataset(), dependencies=dependencies())


def test_rejection_card_proves_no_artefact_or_release() -> None:
    card = build_rejection_card(readiness(), dataset(), registry=registry(), dependencies=dependencies(), evidence_matrix=evidence_matrix())
    assert card["artefact_status"] == "no_adapted_artefact_created"
    assert card["training_executed"] is False
    assert card["release_performed"] is False
    assert card["receipt_sha256"] == canonical_hash({key:value for key,value in card.items() if key != "receipt_sha256"})
    assert card == json.loads((ROOT / "evaluation/adaptation/rejection-card-20260829.json").read_text())


def test_rejection_card_rejects_forged_positive_or_invalid_dataset() -> None:
    positive = readiness()
    positive["ready"] = True
    with pytest.raises(ValueError, match="negative readiness"):
        build_rejection_card(positive, dataset(), registry=registry(), dependencies=dependencies(), evidence_matrix=evidence_matrix())
    bad = dataset()
    bad["private_data"] = True
    with pytest.raises(ValueError, match="valid generated-synthetic"):
        build_rejection_card(readiness(), bad, registry=registry(), dependencies=dependencies(), evidence_matrix=evidence_matrix())


def test_dependency_manifest_rejects_hash_path_and_claim_forgery() -> None:
    value = dependencies()
    value["dependencies"][0]["receipt_path"] = "../outside"
    value["dependencies"][1]["sha256"] = "0" * 64
    value["claims"][0]["id"] = "forged"
    errors = validate_dependency_manifest(value, ROOT)
    assert "dependencies[0] path escapes repository" in errors
    assert "dependencies[1] receipt hash mismatched" in errors
    assert "dependency claim coverage is invalid" in errors


@pytest.mark.parametrize("value", [None, [], "bad"])
def test_dependency_manifest_rejects_non_objects(value: object) -> None:
    assert validate_dependency_manifest(value, ROOT) == ["dependency manifest must be an object"]


def test_dependency_manifest_rejects_malformed_collections_and_entries() -> None:
    value = dependencies()
    value.update(extra=True, dependencies="bad", claims="bad")
    errors = validate_dependency_manifest(value, ROOT)
    assert "dependency manifest fields are invalid" in errors
    assert "dependencies must be an array" in errors
    assert "dependency track coverage is incomplete" in errors
    assert "dependency claims are incomplete" in errors
    value = dependencies()
    value["dependencies"] = [None, {}, {**value["dependencies"][0], "state": "active"}]
    value["claims"] = [None, {}]
    errors = validate_dependency_manifest(value, ROOT)
    assert "dependencies[0] fields are invalid" in errors
    assert "dependencies[2] state or path is invalid" in errors
    assert "claims[0] fields are invalid" in errors


def test_dependency_manifest_rejects_bad_claim_paths_and_receipt_locations() -> None:
    value = dependencies()
    value["dependencies"][0]["receipt_path"] = "README.md"
    value["claims"][0]["path"] = "../outside.json"
    value["claims"][1]["sha256"] = "0" * 64
    errors = validate_dependency_manifest(value, ROOT)
    assert "dependencies[0] receipt path is invalid" in errors
    assert "claims[0] path is invalid" in errors
    assert "claims[1] hash or path mismatched" in errors


def test_readiness_receipt_rejects_tampering_and_wrong_input_binding() -> None:
    value = readiness()
    value["ready"] = True
    assert validate_readiness_receipt(value, registry=registry(), dataset=dataset(), dependencies=dependencies())
    other_registry = registry()
    other_registry["comparators"] = [{"id": "forged"}]
    assert "readiness registry_sha256 binding mismatched" in validate_readiness_receipt(
        readiness(), registry=other_registry, dataset=dataset(), dependencies=dependencies()
    )
    assert validate_readiness_receipt([], registry=registry(), dataset=dataset(), dependencies=dependencies()) == ["readiness receipt must be an object"]
    value = readiness()
    value.update(extra=True, model_downloaded=True)
    errors = validate_readiness_receipt(value, registry=registry(), dataset=dataset(), dependencies=dependencies())
    assert "readiness receipt fields are invalid" in errors
    assert "readiness model_downloaded must be false" in errors


def test_evidence_matrix_is_complete_null_and_hash_bound() -> None:
    assert validate_evidence_matrix(evidence_matrix(), readiness()) == []
    value = evidence_matrix()
    value["metrics"]["quality"] = 1
    value["approaches"].pop()
    assert validate_evidence_matrix(value, readiness())
    assert validate_evidence_matrix([], readiness()) == ["evidence matrix must be an object"]
    value = evidence_matrix()
    value.update(extra=True, comparison_status="executed", readiness_sha256="0" * 64, metrics=[], limitations=[])
    errors = validate_evidence_matrix(value, {})
    assert "evidence matrix fields are invalid" in errors
    assert "evidence matrix negative state is invalid" in errors
    assert "evidence matrix readiness binding mismatched" in errors
    assert "unexecuted evidence matrix metrics must be null" in errors
    assert "evidence matrix limitations are invalid" in errors


def test_rejection_card_rejects_invalid_evidence_matrix() -> None:
    bad_matrix = evidence_matrix()
    bad_matrix["metrics"]["quality"] = 1
    with pytest.raises(ValueError, match="valid negative evidence matrix"):
        build_rejection_card(readiness(), dataset(), registry=registry(), dependencies=dependencies(), evidence_matrix=bad_matrix)


def test_proposal_rejects_unsafe_content_bad_identifier_and_seed() -> None:
    value = proposal()
    value.update(experiment_id="human@example.com", seed=True)
    value["rollback"] = ["https://example.invalid?token=secret"]
    errors = validate_experiment_proposal(value, readiness(), registry=registry(), dataset=dataset(), dependencies=dependencies())
    assert "experiment_id must be an opaque synthetic identifier" in errors
    assert "experiment seed is invalid" in errors
    assert "experiment rollback contains unsafe content" in errors
