"""Fail-closed, model-free contracts for domain adaptation readiness.

The module validates generated-synthetic governance artefacts and records a
negative readiness decision. It does not download, train, infer, publish, or
promote a model or dataset.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

SCHEMA_VERSION = "1.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
LEVELS = {"deterministic", "retrieval", "prompt", "structured_output", "tool", "adapter", "weight_update"}
STATUS = {"unavailable", "contract_only", "rejected"}
SENSITIVE_RE = re.compile(r"(?i)(?:token|password|secret|api[_-]?key)\s*[=:]|https?://|file:|(?:^|/)\.\.(?:/|$)|/Users/|[A-Z]:\\")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_dependency_manifest(manifest: object, root: Path) -> list[str]:
    if not isinstance(manifest, dict):
        return ["dependency manifest must be an object"]
    required = {"schema_version", "dependencies", "claims", "manifest_sha256"}
    errors: list[str] = []
    if set(manifest) != required:
        errors.append("dependency manifest fields are invalid")
    dependencies = manifest.get("dependencies")
    required_ids = {"benchmark-evaluation-harness_20260731", "multimodal-capability-fabric_20260731", "retrieval-knowledge-system_20260731", "local-runtime-model-lab_20260731", "privacy-security-assurance_20260731", "nsw-health-jurisdiction-pack_20260731"}
    seen: set[str] = set()
    if not isinstance(dependencies, list):
        errors.append("dependencies must be an array")
        dependencies = []
    for index, item in enumerate(dependencies):
        if not isinstance(item, dict) or set(item) != {"track_id", "receipt_path", "sha256", "state"}:
            errors.append(f"dependencies[{index}] fields are invalid")
            continue
        track_id, path_value = item.get("track_id"), item.get("receipt_path")
        if not isinstance(track_id, str) or track_id in seen:
            errors.append(f"dependencies[{index}].track_id is invalid or duplicated")
            continue
        else:
            seen.add(track_id)
        if item.get("state") != "archived_passing" or not isinstance(path_value, str):
            errors.append(f"dependencies[{index}] state or path is invalid")
            continue
        posix, windows = PurePosixPath(path_value), PureWindowsPath(path_value)
        if posix.is_absolute() or windows.is_absolute() or ".." in posix.parts:
            errors.append(f"dependencies[{index}] path escapes repository")
            continue
        path = root / posix
        expected_prefix = PurePosixPath("conductor/archive") / track_id
        if not posix.is_relative_to(expected_prefix) or not path.is_file() or path.is_symlink():
            errors.append(f"dependencies[{index}] receipt path is invalid")
        elif not _is_sha(item.get("sha256")) or _sha256(path) != item["sha256"]:
            errors.append(f"dependencies[{index}] receipt hash mismatched")
    if seen != required_ids:
        errors.append("dependency track coverage is incomplete")
    claims = manifest.get("claims")
    if not isinstance(claims, list) or len(claims) != 2:
        errors.append("dependency claims are incomplete")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict) or set(claim) != {"id", "path", "sha256", "expected"}:
                errors.append(f"claims[{index}] fields are invalid")
                continue
            path_value = claim.get("path")
            if not isinstance(path_value, str) or PurePosixPath(path_value).is_absolute() or PureWindowsPath(path_value).is_absolute() or ".." in PurePosixPath(path_value).parts:
                errors.append(f"claims[{index}] path is invalid")
                continue
            path = root / PurePosixPath(path_value)
            if not path.is_file() or path.is_symlink() or not _is_sha(claim.get("sha256")) or _sha256(path) != claim["sha256"]:
                errors.append(f"claims[{index}] hash or path mismatched")
                continue
            value = json.loads(path.read_text())
            if claim.get("id") == "runtime_models_empty" and (claim.get("expected") is not True or value.get("models") != []):
                errors.append("runtime empty-model claim failed")
            if claim.get("id") == "benchmark_comparators_nonpromotion" and (
                claim.get("expected") is not True
                or value.get("scope") != "internal_nonpromotion_synthetic_comparator"
                or "no model promotion" not in value.get("limitations", [])
            ):
                errors.append("benchmark non-promotion claim failed")
        claim_ids = {claim.get("id") for claim in claims if isinstance(claim, dict)}
        if claim_ids != {"runtime_models_empty", "benchmark_comparators_nonpromotion"}:
            errors.append("dependency claim coverage is invalid")
    supplied = manifest.get("manifest_sha256")
    unsigned = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if not _is_sha(supplied) or supplied != canonical_hash(unsigned):
        errors.append("dependency manifest hash mismatched")
    return sorted(errors)


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
        "private_data", "redistribution", "data_materialised", "units", "manifest_sha256",
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
    if manifest.get("data_materialised") is not False or manifest.get("units") != []:
        errors.append("dataset contract plan must contain no materialised units")
    for field in ("purpose", "deidentification", "deletion", "contamination_control"):
        if not isinstance(manifest.get(field), str) or not manifest[field]:
            errors.append(f"dataset {field} must be a non-empty string")
    splits = manifest.get("splits")
    expected_names = {"train", "validation", "held_out", "challenge", "contamination_control"}
    if not isinstance(splits, list) or {item.get("name") for item in splits if isinstance(item, dict)} != expected_names:
        errors.append("dataset splits are incomplete")
    else:
        for index, split in enumerate(splits):
            if not isinstance(split, dict) or set(split) != {"name", "item_ids", "sha256"}:
                errors.append(f"splits[{index}] fields are invalid")
                continue
            item_ids = split.get("item_ids")
            if item_ids != []:
                errors.append(f"splits[{index}].item_ids must remain empty until data are materialised")
                continue
            if split.get("sha256") != canonical_hash(item_ids):
                errors.append(f"splits[{index}].sha256 mismatched")
    supplied = manifest.get("manifest_sha256")
    unsigned = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if not _is_sha(supplied) or supplied != canonical_hash(unsigned):
        errors.append("dataset manifest hash mismatched")
    return sorted(errors)


def assess_readiness(registry: object, dataset: object, dependencies: object, root: Path) -> dict[str, Any]:
    reasons: list[str] = []
    if validate_registry(registry):
        reasons.append("adaptation registry is invalid")
    if validate_dataset_manifest(dataset):
        reasons.append("dataset manifest is invalid")
    if validate_dependency_manifest(dependencies, root):
        reasons.append("dependency evidence is incomplete")
    if isinstance(registry, dict) and not registry.get("comparators"):
        reasons.append("no eligible supported Track10 comparator or common baseline exists")
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
        "registry_sha256": canonical_hash(registry),
        "dataset_contract_sha256": canonical_hash(dataset),
        "dependency_manifest_sha256": dependencies.get("manifest_sha256") if isinstance(dependencies, dict) else None,
        "model_downloaded": False, "training_executed": False, "weights_created": False,
        "private_data_used": False, "external_inference": False, "release_performed": False,
    }
    result["receipt_sha256"] = canonical_hash(result)
    return result


def validate_readiness_receipt(receipt: object, *, registry: object, dataset: object, dependencies: object) -> list[str]:
    if not isinstance(receipt, dict):
        return ["readiness receipt must be an object"]
    required = {
        "schema_version", "decision", "ready", "allowed_levels", "blocked_levels", "reasons",
        "registry_sha256", "dataset_contract_sha256", "dependency_manifest_sha256",
        "model_downloaded", "training_executed", "weights_created", "private_data_used",
        "external_inference", "release_performed", "receipt_sha256",
    }
    errors: list[str] = []
    if set(receipt) != required:
        errors.append("readiness receipt fields are invalid")
    if receipt.get("schema_version") != SCHEMA_VERSION or receipt.get("decision") != "not_ready_reject_weight_adaptation" or receipt.get("ready") is not False:
        errors.append("readiness decision invariants are invalid")
    for field in ("model_downloaded", "training_executed", "weights_created", "private_data_used", "external_inference", "release_performed"):
        if receipt.get(field) is not False:
            errors.append(f"readiness {field} must be false")
    expected_bindings = {
        "registry_sha256": canonical_hash(registry), "dataset_contract_sha256": canonical_hash(dataset),
        "dependency_manifest_sha256": dependencies.get("manifest_sha256") if isinstance(dependencies, dict) else None,
    }
    for field, expected in expected_bindings.items():
        if receipt.get(field) != expected:
            errors.append(f"readiness {field} binding mismatched")
    supplied = receipt.get("receipt_sha256")
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if not _is_sha(supplied) or supplied != canonical_hash(unsigned):
        errors.append("readiness receipt hash mismatched")
    return sorted(errors)


def validate_experiment_proposal(proposal: object, readiness: object, *, registry: object, dataset: object, dependencies: object) -> list[str]:
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
    if validate_readiness_receipt(readiness, registry=registry, dataset=dataset, dependencies=dependencies) or not isinstance(readiness, dict) or proposal.get("readiness_sha256") != readiness.get("receipt_sha256"):
        errors.append("proposal is not bound to the negative readiness receipt")
    if proposal.get("level") in {"adapter", "weight_update"}:
        errors.append("weight-affecting experiment is blocked")
    for field in ("rollback", "stop_conditions"):
        if not isinstance(proposal.get(field), list) or not proposal[field] or not all(isinstance(item, str) and item for item in proposal[field]):
            errors.append(f"experiment {field} must be a non-empty string array")
        elif any(SENSITIVE_RE.search(item) for item in proposal[field]):
            errors.append(f"experiment {field} contains unsafe content")
    if not isinstance(proposal.get("experiment_id"), str) or not re.fullmatch(r"syn-[a-z0-9-]{3,64}", proposal["experiment_id"]):
        errors.append("experiment_id must be an opaque synthetic identifier")
    seed = proposal.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= 2**32 - 1:
        errors.append("experiment seed is invalid")
    return sorted(errors)


def build_rejection_card(readiness: dict[str, Any], dataset: dict[str, Any], *, registry: object, dependencies: object, evidence_matrix: dict[str, Any]) -> dict[str, Any]:
    if validate_dataset_manifest(dataset):
        raise ValueError("rejection card requires a valid generated-synthetic manifest")
    if validate_readiness_receipt(readiness, registry=registry, dataset=dataset, dependencies=dependencies):
        raise ValueError("rejection card requires a negative readiness receipt")
    if validate_evidence_matrix(evidence_matrix, readiness):
        raise ValueError("rejection card requires a valid negative evidence matrix")
    card = {
        "schema_version": SCHEMA_VERSION,
        "artefact_status": "no_adapted_artefact_created",
        "decision": "rejected",
        "readiness_sha256": readiness["receipt_sha256"],
        "dataset_manifest_sha256": dataset["manifest_sha256"],
        "registry_sha256": canonical_hash(registry),
        "dependency_manifest_sha256": dependencies.get("manifest_sha256") if isinstance(dependencies, dict) else None,
        "evidence_matrix_sha256": evidence_matrix.get("receipt_sha256"),
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


def validate_evidence_matrix(matrix: object, readiness: object) -> list[str]:
    if not isinstance(matrix, dict):
        return ["evidence matrix must be an object"]
    required = {"schema_version", "comparison_status", "material_gap", "adaptation_hypothesis", "readiness_sha256", "approaches", "metrics", "limitations", "receipt_sha256"}
    errors: list[str] = []
    if set(matrix) != required:
        errors.append("evidence matrix fields are invalid")
    if matrix.get("comparison_status") != "not_executed_no_eligible_common_baseline" or matrix.get("material_gap") != "not_established" or matrix.get("adaptation_hypothesis") != "not_justified":
        errors.append("evidence matrix negative state is invalid")
    if not isinstance(readiness, dict) or matrix.get("readiness_sha256") != readiness.get("receipt_sha256"):
        errors.append("evidence matrix readiness binding mismatched")
    approaches = matrix.get("approaches")
    expected = {"deterministic", "retrieval", "prompt", "structured_output", "tool", "adapter", "weight_update", "domain_model"}
    if (
        not isinstance(approaches, list)
        or any(not isinstance(item, dict) or set(item) != {"approach", "state"} for item in approaches)
        or {item.get("approach") for item in approaches if isinstance(item, dict)} != expected
        or len(approaches) != len(expected)
    ):
        errors.append("evidence matrix approaches are incomplete")
    metrics = matrix.get("metrics")
    expected_metrics = {"quality", "calibration", "safety", "privacy", "fairness", "robustness", "device_cost", "maintenance_burden"}
    if not isinstance(metrics, dict) or set(metrics) != expected_metrics or any(value is not None for value in metrics.values()):
        errors.append("unexecuted evidence matrix metrics must be null")
    limitations = matrix.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(isinstance(item, str) and item for item in limitations):
        errors.append("evidence matrix limitations are invalid")
    supplied = matrix.get("receipt_sha256")
    unsigned = {key: value for key, value in matrix.items() if key != "receipt_sha256"}
    if not _is_sha(supplied) or supplied != canonical_hash(unsigned):
        errors.append("evidence matrix hash mismatched")
    return sorted(errors)
