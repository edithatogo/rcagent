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
    "measured_research",
    "supported",
    "unavailable",
    "experimental",
}
RUNTIME_CLASSES = {"optional_adapter", "experimental"}
DATA_CLASSES = {"synthetic", "public", "governed_private"}
HASH_LENGTH = 64


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
        "accelerator_class": accelerator,
        "identifiers_redacted": True,
        "network_observation": "not_probed",
        "telemetry_observation": "not_probed",
    }
    profile["receipt_sha256"] = _digest(profile)
    return profile


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
    for index, runtime in enumerate(runtimes):
        prefix = f"runtimes[{index}]"
        if not isinstance(runtime, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(required_runtime - runtime.keys())
        errors.extend(f"{prefix}.{field} is required" for field in missing)
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
    for index, model in enumerate(models):
        prefix = f"models[{index}]"
        if not isinstance(model, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(f"{prefix}.{field} is required" for field in sorted(required_model - model.keys()))
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
        if not isinstance(provenance, str) or len(provenance) != HASH_LENGTH:
            errors.append(f"{prefix}.provenance_sha256 must be sha256")
        if model.get("remote_code") is not False:
            errors.append(f"{prefix}.remote_code must be false")
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
        if not isinstance(expected_hash, str) or len(expected_hash) != HASH_LENGTH:
            errors.append(f"{prefix}.sha256 must be sha256")
        elif _sha256(resolved) != expected_hash:
            errors.append(f"{prefix}.sha256 mismatched")
        if resolved.stat().st_size != entry.get("bytes"):
            errors.append(f"{prefix}.bytes mismatched")
    return sorted(errors)


def route_request(
    request: object,
    registry: dict[str, Any],
    discovery: dict[str, Any],
) -> dict[str, Any]:
    reasons: list[str] = []
    if not isinstance(request, dict):
        reasons.append("request must be an object")
        request = {}
    required = {"task", "modality", "data_class", "runtime_id", "model_id", "context_tokens"}
    reasons.extend(f"request.{key} is required" for key in sorted(required - request.keys()))
    if request.get("data_class") not in DATA_CLASSES:
        reasons.append("request.data_class is invalid")
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
        if request.get("context_tokens", 0) > model.get("context_limit", 0):
            reasons.append("requested context exceeds measured limit")
        if request.get("task") not in model.get("task_fit", []):
            reasons.append("task is unsupported")
    result = {
        "status": "no_capability" if reasons else "eligible_local_route",
        "reasons": sorted(set(reasons)),
        "external_fallback": False,
        "model_executed": False,
    }
    result["receipt_sha256"] = _digest(result)
    return result


def recommendation_matrix(registry: dict[str, Any], discovery: dict[str, Any], *, date: str) -> dict[str, Any]:
    rows = []
    observed = {item["runtime_id"]: item for item in discovery.get("observations", [])}
    for runtime in registry.get("runtimes", []):
        state = observed.get(runtime["id"], {}).get("observed_state", "unavailable")
        rows.append(
            {
                "runtime_id": runtime["id"],
                "classification": "unsupported" if state != "supported" else "conditional",
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
