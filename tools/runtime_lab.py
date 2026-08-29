"""Deterministic, model-free contracts for the local runtime and model lab.

This module discovers capabilities and verifies operator-owned bundles.  It
does not download models, execute inference, or promote a runtime.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
SUPPORT_STATES = {
    "interface_contract",
    "installed_unmeasured",
    "unavailable",
    "experimental",
}
RUNTIME_CLASSES = {"optional_adapter", "experimental"}
DATA_CLASSES = {"synthetic", "public", "governed_private"}
HASH_LENGTH = 64


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == HASH_LENGTH
        and all(character in "0123456789abcdef" for character in value)
    )


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def privacy_safe_device_profile(*, memory_bytes: int | None = None) -> dict[str, Any]:
    """Return coarse capability fields without host, user, path, or serial data."""
    machine = platform.machine().lower() or "unknown"
    system = platform.system().lower() or "unknown"
    memory_gib = None if memory_bytes is None else max(0, memory_bytes // (1024**3))
    if memory_gib is not None:
        memory_gib = (memory_gib // 4) * 4
    accelerator = "apple_silicon" if system == "darwin" and machine in {"arm64", "aarch64"} else "unobserved"
    profile = {
        "schema_version": SCHEMA_VERSION,
        "os_family": system,
        "architecture": machine,
        "logical_cpu_count": os.cpu_count(),
        "memory_gib_floor": memory_gib,
        "memory_probe_state": "provided_coarse" if memory_bytes is not None else "unobserved",
        "storage_gib_floor": None,
        "storage_probe_state": "unobserved",
        "accelerator_class": accelerator,
        "driver_state": "unobserved",
        "instruction_set_state": "architecture_only_unmeasured",
        "power_proxy_state": "unobserved",
        "identifiers_redacted": True,
        "network_observation": "not_probed",
        "telemetry_observation": "not_probed",
    }
    profile["receipt_sha256"] = _digest(profile)
    return profile


def validate_device_profile(profile: object) -> list[str]:
    if not isinstance(profile, dict):
        return ["device profile must be an object"]
    required = {
        "schema_version", "os_family", "architecture", "logical_cpu_count",
        "memory_gib_floor", "memory_probe_state", "storage_gib_floor",
        "storage_probe_state", "accelerator_class", "driver_state",
        "instruction_set_state", "power_proxy_state", "identifiers_redacted",
        "network_observation", "telemetry_observation", "receipt_sha256",
    }
    errors: list[str] = []
    if set(profile) != required:
        errors.append("device profile fields are invalid")
    if profile.get("schema_version") != SCHEMA_VERSION:
        errors.append("device profile schema version is invalid")
    if profile.get("identifiers_redacted") is not True:
        errors.append("device identifiers must be redacted")
    supplied = profile.get("receipt_sha256")
    unsigned = {key: value for key, value in profile.items() if key != "receipt_sha256"}
    if not _is_sha256(supplied) or supplied != _digest(unsigned):
        errors.append("device profile receipt hash mismatched")
    return sorted(errors)


def validate_runtime_registry(registry: object) -> list[str]:
    if not isinstance(registry, dict):
        return ["registry must be an object"]
    allowed_top = {"schema_version", "runtimes", "models", "hypotheses", "policy"}
    errors = [f"registry: unknown field {key}" for key in registry if key not in allowed_top]
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append("registry.schema_version must be 1.0")
    policy = registry.get("policy")
    required_policy = {
        "downloads": False,
        "external_inference": False,
        "remote_code": False,
        "promotion": False,
        "redistribution": False,
    }
    if not isinstance(policy, dict):
        errors.append("registry.policy must be an object")
    else:
        for key, expected in required_policy.items():
            if policy.get(key) is not expected:
                errors.append(f"registry.policy.{key} must be false")
    runtimes = registry.get("runtimes")
    if not isinstance(runtimes, list):
        errors.append("registry.runtimes must be an array")
        runtimes = []
    seen: set[str] = set()
    required_runtime = {
        "id", "dependency_class", "support_state", "interface", "executable_names",
        "licence", "network", "telemetry", "remote_code", "applicability",
        "failure_modes", "replacement_path", "freshness_date",
    }
    allowed_runtime = required_runtime
    for index, runtime in enumerate(runtimes):
        prefix = f"runtimes[{index}]"
        if not isinstance(runtime, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(required_runtime - runtime.keys())
        errors.extend(f"{prefix}.{field} is required" for field in missing)
        errors.extend(f"{prefix}.{field} is unknown" for field in sorted(runtime.keys() - allowed_runtime))
        runtime_id = runtime.get("id")
        if not isinstance(runtime_id, str) or not runtime_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif runtime_id in seen:
            errors.append(f"{prefix}.id is duplicated")
        else:
            seen.add(runtime_id)
        if runtime.get("dependency_class") not in RUNTIME_CLASSES:
            errors.append(f"{prefix}.dependency_class is invalid")
        if runtime.get("support_state") not in SUPPORT_STATES:
            errors.append(f"{prefix}.support_state is invalid")
        if runtime.get("remote_code") is not False:
            errors.append(f"{prefix}.remote_code must be false")
        if runtime.get("network") not in {"none", "unknown"}:
            errors.append(f"{prefix}.network must be none or unknown")
        if runtime.get("telemetry") not in {"disabled", "unknown"}:
            errors.append(f"{prefix}.telemetry must be disabled or unknown")
        if not isinstance(runtime.get("failure_modes"), list) or not runtime.get("failure_modes"):
            errors.append(f"{prefix}.failure_modes must be a non-empty array")
        elif not all(isinstance(item, str) and item for item in runtime["failure_modes"]):
            errors.append(f"{prefix}.failure_modes entries must be non-empty strings")
        if not isinstance(runtime.get("executable_names"), list) or not all(
            isinstance(item, str) and item for item in runtime.get("executable_names", [])
        ):
            errors.append(f"{prefix}.executable_names must be a string array")
    models = registry.get("models")
    if not isinstance(models, list):
        errors.append("registry.models must be an array")
        models = []
    model_ids: set[str] = set()
    required_model = {
        "id", "repository", "revision", "licence", "provenance_sha256", "task_fit",
        "input_limits", "context_limit", "quantisation", "device_evidence",
        "failure_modes", "admission_status", "remote_code",
    }
    allowed_model = required_model
    for index, model in enumerate(models):
        prefix = f"models[{index}]"
        if not isinstance(model, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(f"{prefix}.{field} is required" for field in sorted(required_model - model.keys()))
        errors.extend(f"{prefix}.{field} is unknown" for field in sorted(model.keys() - allowed_model))
        model_id = model.get("id")
        if not isinstance(model_id, str) or not model_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif model_id in model_ids:
            errors.append(f"{prefix}.id is duplicated")
        else:
            model_ids.add(model_id)
        revision = model.get("revision")
        if not isinstance(revision, str) or len(revision) < 7 or revision in {"main", "latest"}:
            errors.append(f"{prefix}.revision must be immutable and exact")
        provenance = model.get("provenance_sha256")
        if not _is_sha256(provenance):
            errors.append(f"{prefix}.provenance_sha256 must be sha256")
        if model.get("remote_code") is not False:
            errors.append(f"{prefix}.remote_code must be false")
        for field in ("repository", "licence", "quantisation", "device_evidence"):
            if not isinstance(model.get(field), str) or not model.get(field):
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if model.get("admission_status") not in {"measured_research", "supported"}:
            errors.append(f"{prefix}.admission_status is invalid")
        for field in ("task_fit", "failure_modes"):
            if not isinstance(model.get(field), list) or not model.get(field) or not all(
                isinstance(item, str) and item for item in model.get(field, [])
            ):
                errors.append(f"{prefix}.{field} must be a non-empty string array")
        limits = model.get("input_limits")
        if not isinstance(limits, dict) or set(limits) != {"modalities"} or not isinstance(limits.get("modalities"), list) or not limits["modalities"] or not all(isinstance(item, str) and item for item in limits["modalities"]):
            errors.append(f"{prefix}.input_limits must contain a non-empty modalities string array")
        context_limit = model.get("context_limit")
        if isinstance(context_limit, bool) or not isinstance(context_limit, int) or context_limit < 1:
            errors.append(f"{prefix}.context_limit must be a positive integer")
    hypotheses = registry.get("hypotheses")
    if not isinstance(hypotheses, list):
        errors.append("registry.hypotheses must be an array")
    else:
        for index, hypothesis in enumerate(hypotheses):
            if not isinstance(hypothesis, dict) or hypothesis.get("status") != "unverified_hypothesis":
                errors.append(f"hypotheses[{index}] must remain unverified_hypothesis")
    return sorted(errors)


def discover_runtimes(registry: dict[str, Any]) -> dict[str, Any]:
    errors = validate_runtime_registry(registry)
    if errors:
        raise ValueError("invalid runtime registry: " + "; ".join(errors))
    observations = []
    for runtime in registry["runtimes"]:
        found = next((shutil.which(name) for name in runtime["executable_names"] if shutil.which(name)), None)
        observations.append(
            {
                "runtime_id": runtime["id"],
                "observed_state": "installed_unmeasured" if found else "unavailable",
                "executable_observed": found is not None,
                "executable_path": None,
                "version": "unmeasured" if found else "unavailable",
                "support_state": "unsupported_without_execution_receipt",
            }
        )
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "scope": "read_only_runtime_discovery_no_execution",
        "observations": observations,
        "network": "not_used",
        "telemetry": "not_used",
        "model_executed": False,
    }
    receipt["receipt_sha256"] = _digest(receipt)
    return receipt


def validate_discovery_receipt(discovery: object, registry: dict[str, Any]) -> list[str]:
    if not isinstance(discovery, dict):
        return ["discovery must be an object"]
    errors: list[str] = []
    expected_fields = {
        "schema_version", "scope", "observations", "network", "telemetry",
        "model_executed", "receipt_sha256",
    }
    if set(discovery) != expected_fields:
        errors.append("discovery fields are invalid")
    if discovery.get("schema_version") != SCHEMA_VERSION:
        errors.append("discovery.schema_version must be 1.0")
    supplied_hash = discovery.get("receipt_sha256")
    unsigned = {key: value for key, value in discovery.items() if key != "receipt_sha256"}
    if not _is_sha256(supplied_hash) or supplied_hash != _digest(unsigned):
        errors.append("discovery receipt hash mismatched")
    if discovery.get("scope") != "read_only_runtime_discovery_no_execution":
        errors.append("discovery scope is invalid")
    if discovery.get("network") != "not_used" or discovery.get("telemetry") != "not_used":
        errors.append("discovery must not use network or telemetry")
    if discovery.get("model_executed") is not False:
        errors.append("discovery cannot claim model execution")
    observations = discovery.get("observations")
    if not isinstance(observations, list):
        errors.append("discovery.observations must be an array")
        return sorted(errors)
    runtime_ids = {item.get("id") for item in registry.get("runtimes", []) if isinstance(item, dict)}
    observed_ids = [item.get("runtime_id") for item in observations if isinstance(item, dict)]
    if len(observed_ids) != len(observations) or set(observed_ids) != runtime_ids or len(set(observed_ids)) != len(observed_ids):
        errors.append("discovery observations must bind every registered runtime exactly once")
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            continue
        if observation.get("observed_state") not in {"installed_unmeasured", "unavailable"}:
            errors.append(f"discovery.observations[{index}] cannot contain measured support evidence")
        if observation.get("support_state") != "unsupported_without_execution_receipt":
            errors.append(f"discovery.observations[{index}] must remain unsupported")
    return sorted(errors)


def validate_bundle_manifest(manifest: object, root: Path) -> list[str]:
    if not isinstance(manifest, dict):
        return ["bundle manifest must be an object"]
    errors: list[str] = []
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("bundle.schema_version must be 1.0")
    if manifest.get("network") != "offline" or manifest.get("redistribution") is not False:
        errors.append("bundle must be offline and non-redistributable")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return sorted([*errors, "bundle.files must be a non-empty array"])
    root = root.resolve()
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"files[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        relative = entry.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append(f"{prefix}.path must be a non-empty string")
            continue
        candidate_relative = Path(relative)
        if candidate_relative.is_absolute() or ".." in candidate_relative.parts:
            errors.append(f"{prefix}.path escapes bundle root")
            continue
        if relative.casefold() in seen:
            errors.append(f"{prefix}.path is duplicated or case-colliding")
            continue
        seen.add(relative.casefold())
        candidate = root / candidate_relative
        cursor = root
        component_symlink = False
        for part in candidate_relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                component_symlink = True
                break
        if component_symlink:
            errors.append(f"{prefix}.path contains a symlink")
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (FileNotFoundError, ValueError):
            errors.append(f"{prefix}.path is missing or outside bundle root")
            continue
        if candidate.is_symlink() or not resolved.is_file():
            errors.append(f"{prefix}.path must be a regular non-symlink file")
            continue
        expected_hash = entry.get("sha256")
        if not _is_sha256(expected_hash):
            errors.append(f"{prefix}.sha256 must be sha256")
        elif _sha256(resolved) != expected_hash:
            errors.append(f"{prefix}.sha256 mismatched")
        if resolved.stat().st_size != entry.get("bytes"):
            errors.append(f"{prefix}.bytes mismatched")
    declared = {str(entry.get("path")).casefold() for entry in entries if isinstance(entry, dict)}
    actual = {
        str(path.relative_to(root)).casefold()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    if declared != actual:
        errors.append("bundle inventory does not exactly match regular files")
    return sorted(errors)


def route_request(
    request: object,
    registry: dict[str, Any],
    discovery: dict[str, Any],
) -> dict[str, Any]:
    reasons: list[str] = []
    registry_errors = validate_runtime_registry(registry)
    reasons.extend(f"registry invalid: {error}" for error in registry_errors)
    discovery_errors = validate_discovery_receipt(discovery, registry)
    reasons.extend(f"discovery invalid: {error}" for error in discovery_errors)
    if not isinstance(request, dict):
        reasons.append("request must be an object")
        request = {}
    required = {"task", "modality", "data_class", "runtime_id", "model_id", "context_tokens"}
    reasons.extend(f"request.{key} is required" for key in sorted(required - request.keys()))
    if request.get("data_class") not in DATA_CLASSES:
        reasons.append("request.data_class is invalid")
    context_tokens = request.get("context_tokens")
    if isinstance(context_tokens, bool) or not isinstance(context_tokens, int) or context_tokens < 1:
        reasons.append("request.context_tokens must be a positive integer")
    if request.get("allow_external") is not False:
        reasons.append("external routing is forbidden")
    if request.get("allow_remote_code") is not False:
        reasons.append("remote code is forbidden")
    runtime = next((item for item in registry.get("runtimes", []) if item.get("id") == request.get("runtime_id")), None)
    model = next((item for item in registry.get("models", []) if item.get("id") == request.get("model_id")), None)
    observation = next((item for item in discovery.get("observations", []) if item.get("runtime_id") == request.get("runtime_id")), None)
    if runtime is None:
        reasons.append("runtime is not registered")
    elif runtime.get("network") != "none" or runtime.get("telemetry") != "disabled":
        reasons.append("runtime isolation is not established")
    if observation is None or observation.get("observed_state") not in {"measured_research", "supported"}:
        reasons.append("runtime lacks a measured execution receipt")
    if model is None:
        reasons.append("model is not admitted")
    else:
        if model.get("admission_status") not in {"measured_research", "supported"}:
            reasons.append("model lacks measured admission")
        model_limit = model.get("context_limit")
        if isinstance(context_tokens, int) and not isinstance(context_tokens, bool) and isinstance(model_limit, int) and not isinstance(model_limit, bool) and context_tokens > model_limit:
            reasons.append("requested context exceeds measured limit")
        if request.get("task") not in model.get("task_fit", []):
            reasons.append("task is unsupported")
        modalities = model.get("input_limits", {}).get("modalities", []) if isinstance(model.get("input_limits"), dict) else []
        if request.get("modality") not in modalities:
            reasons.append("modality is unsupported")
    if request.get("data_class") == "governed_private":
        reasons.append("governed-private routing requires separately verified local isolation")
    result = {
        "status": "no_capability" if reasons else "eligible_local_route",
        "reasons": sorted(set(reasons)),
        "external_fallback": False,
        "model_executed": False,
    }
    result["receipt_sha256"] = _digest(result)
    return result


def recommendation_matrix(registry: dict[str, Any], discovery: dict[str, Any], *, date: str) -> dict[str, Any]:
    validation_errors = [
        *validate_runtime_registry(registry),
        *validate_discovery_receipt(discovery, registry),
    ]
    if validation_errors:
        raise ValueError("invalid recommendation evidence: " + "; ".join(validation_errors))
    rows = []
    observed = {item["runtime_id"]: item for item in discovery.get("observations", [])}
    for runtime in registry.get("runtimes", []):
        state = observed.get(runtime["id"], {}).get("observed_state", "unavailable")
        rows.append(
            {
                "runtime_id": runtime["id"],
                "classification": "unsupported",
                "evidence_state": state,
                "measured_device": False,
                "public_comparative_claim": False,
                "rationale": "No exact runtime, model, device and benchmark promotion receipt.",
            }
        )
    matrix = {
        "schema_version": SCHEMA_VERSION,
        "date": date,
        "scope": "internal_non_operational_recommendation",
        "rows": rows,
        "agent_agreement": "pending_panel",
        "human_agreement": False,
        "limitations": [
            "No model was downloaded or executed by Track 08.",
            "No clinical, legal, policy, organisational, deployment or public-comparison approval.",
        ],
    }
    matrix["receipt_sha256"] = _digest(matrix)
    return matrix
