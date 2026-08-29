"""Fail-closed, model-free contracts for domain adaptation readiness.

The module validates generated-synthetic governance artefacts and records a
negative readiness decision. It does not download, train, infer, publish, or
promote a model or dataset.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

SCHEMA_VERSION = "1.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
LEVELS = {"deterministic", "retrieval", "prompt", "structured_output", "tool", "adapter", "weight_update"}
STATUS = {"unavailable", "contract_only", "rejected"}


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def validate_registry(registry: object) -> list[str]:
    if not isinstance(registry, dict):
        return ["registry must be an object"]
    errors: list[str] = []
    required = {"schema_version", "policy", "frameworks", "comparators", "readiness_thresholds"}
    if set(registry) != required:
        errors.append("registry fields are invalid")
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be 1.0")
    policy = registry.get("policy")
    expected_policy = {
        "generated_synthetic_only": True, "private_data": False, "downloads": False,
        "remote_inference": False, "training": False, "weight_creation": False,
        "redistribution": False, "clinical_claims": False, "promotion": False,
    }
    if not isinstance(policy, dict) or set(policy) != set(expected_policy):
        errors.append("policy fields are invalid")
    else:
        for field, expected in expected_policy.items():
            if policy.get(field) is not expected:
                errors.append(f"policy.{field} must be {expected!r}")
    frameworks = registry.get("frameworks")
    if not isinstance(frameworks, list) or not frameworks:
        errors.append("frameworks must be a non-empty array")
    else:
        seen: set[str] = set()
        for index, framework in enumerate(frameworks):
            required_framework = {"id", "status", "revision", "licence", "network", "telemetry", "remote_code", "replacement_path"}
            if not isinstance(framework, dict) or set(framework) != required_framework:
                errors.append(f"frameworks[{index}] fields are invalid")
                continue
            identifier = framework.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in seen:
                errors.append(f"frameworks[{index}].id is invalid or duplicated")
            else:
                seen.add(identifier)
            if framework.get("status") not in STATUS:
                errors.append(f"frameworks[{index}].status is invalid")
            if framework.get("revision") != "not_acquired":
                errors.append(f"frameworks[{index}].revision must remain not_acquired")
            if framework.get("licence") != "not_evaluated_for_execution":
                errors.append(f"frameworks[{index}].licence must remain unevaluated")
            if framework.get("network") != "not_used" or framework.get("telemetry") != "not_used" or framework.get("remote_code") is not False:
                errors.append(f"frameworks[{index}] execution boundary is invalid")
    comparators = registry.get("comparators")
    if comparators != []:
        errors.append("comparators must remain empty without admitted exact revisions")
    thresholds = registry.get("readiness_thresholds")
    expected_thresholds = {
        "material_baseline_gap_required": True,
        "rights_complete_required": True,
        "privacy_complete_required": True,
        "supported_runtime_required": True,
        "admitted_comparator_required": True,
        "accountable_release_approval_required": True,
    }
    if not isinstance(thresholds, dict) or thresholds != expected_thresholds:
        errors.append("readiness thresholds are invalid")
    return sorted(errors)


def validate_dataset_manifest(manifest: object) -> list[str]:
    if not isinstance(manifest, dict):
        return ["dataset manifest must be an object"]
    required = {
        "schema_version", "dataset_id", "data_class", "origin", "rights", "consent",
        "purpose", "deidentification", "deletion", "splits", "contamination_control",
        "private_data", "redistribution", "manifest_sha256",
    }
    errors: list[str] = []
    if set(manifest) != required:
        errors.append("dataset manifest fields are invalid")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("dataset schema_version must be 1.0")
    if manifest.get("data_class") != "generated_synthetic" or manifest.get("origin") != "repository_authored_synthetic":
        errors.append("dataset must be repository-authored generated synthetic")
    if manifest.get("rights") != "Apache-2.0" or manifest.get("consent") != "not_applicable_generated_synthetic":
        errors.append("dataset rights or consent state is invalid")
    if manifest.get("private_data") is not False or manifest.get("redistribution") is not False:
        errors.append("dataset must contain no private data and remain non-redistributed")
    for field in ("purpose", "deidentification", "deletion", "contamination_control"):
        if not isinstance(manifest.get(field), str) or not manifest[field]:
            errors.append(f"dataset {field} must be a non-empty string")
    splits = manifest.get("splits")
    expected_names = {"train", "validation", "held_out", "challenge", "contamination_control"}
    seen_items: set[str] = set()
    if not isinstance(splits, list) or {item.get("name") for item in splits if isinstance(item, dict)} != expected_names:
        errors.append("dataset splits are incomplete")
    else:
        for index, split in enumerate(splits):
            if not isinstance(split, dict) or set(split) != {"name", "item_ids", "sha256"}:
                errors.append(f"splits[{index}] fields are invalid")
                continue
            item_ids = split.get("item_ids")
            if not isinstance(item_ids, list) or not item_ids or not all(isinstance(item, str) and re.fullmatch(r"syn-[a-z0-9-]+", item) for item in item_ids):
                errors.append(f"splits[{index}].item_ids are invalid")
                continue
            if seen_items.intersection(item_ids):
                errors.append("dataset splits overlap")
            seen_items.update(item_ids)
            if split.get("sha256") != canonical_hash(item_ids):
                errors.append(f"splits[{index}].sha256 mismatched")
    supplied = manifest.get("manifest_sha256")
    unsigned = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if not _is_sha(supplied) or supplied != canonical_hash(unsigned):
        errors.append("dataset manifest hash mismatched")
    return sorted(errors)


def assess_readiness(registry: object, dataset: object, dependencies: object) -> dict[str, Any]:
    reasons: list[str] = []
    if validate_registry(registry):
        reasons.append("adaptation registry is invalid")
    if validate_dataset_manifest(dataset):
        reasons.append("dataset manifest is invalid")
    if not isinstance(dependencies, dict):
        dependencies = {}
        reasons.append("dependency state must be an object")
    required_dependencies = {"benchmark", "multimodal", "retrieval", "runtime_lab", "privacy", "jurisdiction"}
    if set(dependencies) != required_dependencies or any(value != "archived_passing" for value in dependencies.values()):
        reasons.append("dependency evidence is incomplete")
    if isinstance(registry, dict) and not registry.get("comparators"):
        reasons.append("no exact admitted comparator exists")
    reasons.extend([
        "no measured material baseline gap exists",
        "no supported runtime and model pair exists",
        "no accountable approval exists for model acquisition, training, private data, or release",
    ])
    result = {
        "schema_version": SCHEMA_VERSION,
        "decision": "not_ready_reject_weight_adaptation",
        "ready": False,
        "allowed_levels": ["deterministic", "retrieval", "prompt", "structured_output", "tool"],
        "blocked_levels": ["adapter", "weight_update"],
        "reasons": sorted(set(reasons)),
        "model_downloaded": False, "training_executed": False, "weights_created": False,
        "private_data_used": False, "external_inference": False, "release_performed": False,
    }
    result["receipt_sha256"] = canonical_hash(result)
    return result


def validate_experiment_proposal(proposal: object, readiness: object) -> list[str]:
    if not isinstance(proposal, dict):
        return ["experiment proposal must be an object"]
    required = {
        "experiment_id", "level", "data_class", "base_revision", "framework_revision",
        "seed", "compute_budget", "network", "telemetry", "remote_code", "execute",
        "readiness_sha256", "rollback", "stop_conditions",
    }
    errors: list[str] = []
    if set(proposal) != required:
        errors.append("experiment proposal fields are invalid")
    if proposal.get("level") not in LEVELS:
        errors.append("experiment level is invalid")
    if proposal.get("data_class") != "generated_synthetic":
        errors.append("experiment data class is not admitted")
    if proposal.get("network") != "none" or proposal.get("telemetry") != "none" or proposal.get("remote_code") is not False:
        errors.append("experiment execution boundary is invalid")
    if proposal.get("execute") is not False:
        errors.append("experiment execution is not authorised")
    if proposal.get("compute_budget") != "none" or proposal.get("base_revision") != "not_acquired" or proposal.get("framework_revision") != "not_acquired":
        errors.append("experiment acquisition or compute state is invalid")
    if not isinstance(readiness, dict) or proposal.get("readiness_sha256") != readiness.get("receipt_sha256") or readiness.get("ready") is not False:
        errors.append("proposal is not bound to the negative readiness receipt")
    if proposal.get("level") in {"adapter", "weight_update"}:
        errors.append("weight-affecting experiment is blocked")
    for field in ("rollback", "stop_conditions"):
        if not isinstance(proposal.get(field), list) or not proposal[field] or not all(isinstance(item, str) and item for item in proposal[field]):
            errors.append(f"experiment {field} must be a non-empty string array")
    return sorted(errors)


def build_rejection_card(readiness: dict[str, Any], dataset: dict[str, Any]) -> dict[str, Any]:
    if readiness.get("ready") is not False or readiness.get("decision") != "not_ready_reject_weight_adaptation":
        raise ValueError("rejection card requires a negative readiness receipt")
    if validate_dataset_manifest(dataset):
        raise ValueError("rejection card requires a valid generated-synthetic manifest")
    card = {
        "schema_version": SCHEMA_VERSION,
        "artefact_status": "no_adapted_artefact_created",
        "decision": "rejected",
        "readiness_sha256": readiness["receipt_sha256"],
        "dataset_manifest_sha256": dataset["manifest_sha256"],
        "licence": "Apache-2.0 repository code only; no model or weight licence attached",
        "intended_use": "research readiness governance only",
        "out_of_scope": ["clinical use", "private data", "medical-device claims", "distribution"],
        "rollback": "remove registry references; no weights, runs, endpoints or private data exist",
        "maintenance": "reassess only after exact admitted comparator, runtime, data and authority receipts",
        "model_downloaded": False, "training_executed": False, "weights_created": False,
        "release_performed": False,
    }
    card["receipt_sha256"] = canonical_hash(card)
    return card
