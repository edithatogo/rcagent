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
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal, TypedDict, TypeGuard

from tools.json_shapes import is_array, is_object

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


class DeviceProfileBody(TypedDict):
    schema_version: str
    os_family: str
    architecture: str
    logical_cpu_count: int | None
    memory_gib_floor: int | None
    memory_probe_state: Literal["provided_coarse", "unobserved"]
    storage_gib_floor: None
    storage_probe_state: Literal["unobserved"]
    accelerator_class: Literal["apple_silicon", "unobserved"]
    driver_state: Literal["unobserved"]
    instruction_set_state: Literal["architecture_only_unmeasured"]
    power_proxy_state: Literal["unobserved"]
    identifiers_redacted: Literal[True]
    network_observation: Literal["not_probed"]
    telemetry_observation: Literal["not_probed"]


class DeviceProfile(DeviceProfileBody):
    receipt_sha256: str


class RuntimeIdentity(TypedDict):
    id: str
    executable_names: list[str]


class RegistryInventory(TypedDict):
    runtimes: list[RuntimeIdentity]


class ObservationIdentity(TypedDict):
    runtime_id: str
    observed_state: str


class DiscoveryInventory(TypedDict):
    observations: list[ObservationIdentity]


class Observation(TypedDict):
    runtime_id: str
    observed_state: Literal["installed_unmeasured", "unavailable"]
    executable_observed: bool
    executable_path: None
    version: Literal["unmeasured", "unavailable"]
    support_state: Literal["unsupported_without_execution_receipt"]


class DiscoveryBody(TypedDict):
    schema_version: str
    scope: Literal["read_only_runtime_discovery_no_execution"]
    observations: list[Observation]
    network: Literal["not_used"]
    telemetry: Literal["not_used"]
    model_executed: Literal[False]


class DiscoveryReceipt(DiscoveryBody):
    receipt_sha256: str


class RouteBody(TypedDict):
    status: Literal["no_capability", "eligible_local_route"]
    reasons: list[str]
    external_fallback: Literal[False]
    model_executed: Literal[False]


class RouteReceipt(RouteBody):
    receipt_sha256: str


class RecommendationRow(TypedDict):
    runtime_id: str
    classification: Literal["unsupported"]
    evidence_state: str
    measured_device: Literal[False]
    public_comparative_claim: Literal[False]
    rationale: str


class AgentAgreement(TypedDict):
    status: Literal["unanimous_accept"]
    reviewed_revision: str
    roles: list[str]
    human_agreement: Literal[False]


class MatrixBody(TypedDict):
    schema_version: str
    date: str
    scope: Literal["internal_non_operational_recommendation"]
    rows: list[RecommendationRow]
    agent_agreement: AgentAgreement
    human_agreement: Literal[False]
    limitations: list[str]


class RecommendationMatrix(MatrixBody):
    receipt_sha256: str


def _is_registry_inventory(value: object) -> TypeGuard[RegistryInventory]:
    if not is_object(value):
        return False
    runtimes = value.get("runtimes")
    if not is_array(runtimes):
        return False
    for runtime in runtimes:
        if not is_object(runtime) or not isinstance(runtime.get("id"), str):
            return False
        names = runtime.get("executable_names")
        if not is_array(names) or not all(isinstance(name, str) for name in names):
            return False
    return True


def _is_discovery_inventory(value: object) -> TypeGuard[DiscoveryInventory]:
    if not is_object(value):
        return False
    observations = value.get("observations")
    return is_array(observations) and all(
        is_object(item)
        and isinstance(item.get("runtime_id"), str)
        and isinstance(item.get("observed_state"), str)
        for item in observations
    )


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


def privacy_safe_device_profile(*, memory_bytes: int | None = None) -> DeviceProfile:
    """Return coarse capability fields without host, user, path, or serial data."""
    machine = platform.machine().lower() or "unknown"
    system = platform.system().lower() or "unknown"
    memory_gib = None if memory_bytes is None else max(0, memory_bytes // (1024**3))
    if memory_gib is not None:
        memory_gib = (memory_gib // 4) * 4
    accelerator = (
        "apple_silicon" if system == "darwin" and machine in {"arm64", "aarch64"} else "unobserved"
    )
    profile: DeviceProfileBody = {
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
    return {**profile, "receipt_sha256": _digest(profile)}


def validate_device_profile(profile: object) -> list[str]:
    if not is_object(profile):
        return ["device profile must be an object"]
    required = {
        "schema_version",
        "os_family",
        "architecture",
        "logical_cpu_count",
        "memory_gib_floor",
        "memory_probe_state",
        "storage_gib_floor",
        "storage_probe_state",
        "accelerator_class",
        "driver_state",
        "instruction_set_state",
        "power_proxy_state",
        "identifiers_redacted",
        "network_observation",
        "telemetry_observation",
        "receipt_sha256",
    }
    errors: list[str] = []
    if set(profile) != required:
        errors.append("device profile fields are invalid")
    if profile.get("schema_version") != SCHEMA_VERSION:
        errors.append("device profile schema version is invalid")
    if profile.get("identifiers_redacted") is not True:
        errors.append("device identifiers must be redacted")
    os_family = profile.get("os_family")
    if not isinstance(os_family, str) or os_family not in {"darwin", "linux", "windows", "unknown"}:
        errors.append("device os_family is not a coarse allowed value")
    architecture = profile.get("architecture")
    if not isinstance(architecture, str) or architecture not in {
        "arm64",
        "aarch64",
        "x86_64",
        "amd64",
        "unknown",
    }:
        errors.append("device architecture is not a coarse allowed value")
    cpu_count = profile.get("logical_cpu_count")
    if cpu_count is not None and (
        isinstance(cpu_count, bool) or not isinstance(cpu_count, int) or not 1 <= cpu_count <= 4096
    ):
        errors.append("device logical_cpu_count is invalid")
    for field in ("memory_gib_floor", "storage_gib_floor"):
        value = profile.get(field)
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            or value > 1048576
            or value % 4
        ):
            errors.append(f"device {field} must be a coarse four-GiB floor")
    categorical = {
        "memory_probe_state": {"provided_coarse", "unobserved"},
        "storage_probe_state": {"provided_coarse", "unobserved"},
        "accelerator_class": {"apple_silicon", "intel_igpu", "discrete_gpu", "unobserved"},
        "driver_state": {"unobserved"},
        "instruction_set_state": {"architecture_only_unmeasured", "unobserved"},
        "power_proxy_state": {"unobserved"},
        "network_observation": {"not_probed"},
        "telemetry_observation": {"not_probed"},
    }
    for field, choices in categorical.items():
        value = profile.get(field)
        if not isinstance(value, str) or value not in choices:
            errors.append(f"device {field} is invalid")
    supplied = profile.get("receipt_sha256")
    unsigned = {key: value for key, value in profile.items() if key != "receipt_sha256"}
    if not _is_sha256(supplied) or supplied != _digest(unsigned):
        errors.append("device profile receipt hash mismatched")
    return sorted(errors)


def validate_runtime_registry(registry: object) -> list[str]:
    if not is_object(registry):
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
    if not is_object(policy):
        errors.append("registry.policy must be an object")
    else:
        for key, expected in required_policy.items():
            if policy.get(key) is not expected:
                errors.append(f"registry.policy.{key} must be false")
    runtimes = registry.get("runtimes")
    if not is_array(runtimes):
        errors.append("registry.runtimes must be an array")
        runtimes = []
    seen: set[str] = set()
    required_runtime = {
        "id",
        "dependency_class",
        "support_state",
        "interface",
        "executable_names",
        "licence",
        "network",
        "telemetry",
        "remote_code",
        "applicability",
        "failure_modes",
        "replacement_path",
        "freshness_date",
    }
    allowed_runtime = required_runtime
    for index, runtime in enumerate(runtimes):
        prefix = f"runtimes[{index}]"
        if not is_object(runtime):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(required_runtime - runtime.keys())
        errors.extend(f"{prefix}.{field} is required" for field in missing)
        errors.extend(
            f"{prefix}.{field} is unknown" for field in sorted(runtime.keys() - allowed_runtime)
        )
        runtime_id = runtime.get("id")
        if not isinstance(runtime_id, str) or not runtime_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif runtime_id in seen:
            errors.append(f"{prefix}.id is duplicated")
        else:
            seen.add(runtime_id)
        dependency_class = runtime.get("dependency_class")
        if not isinstance(dependency_class, str) or dependency_class not in RUNTIME_CLASSES:
            errors.append(f"{prefix}.dependency_class is invalid")
        support_state = runtime.get("support_state")
        if not isinstance(support_state, str) or support_state not in SUPPORT_STATES:
            errors.append(f"{prefix}.support_state is invalid")
        if runtime.get("remote_code") is not False:
            errors.append(f"{prefix}.remote_code must be false")
        network = runtime.get("network")
        if not isinstance(network, str) or network not in {"none", "unknown"}:
            errors.append(f"{prefix}.network must be none or unknown")
        telemetry = runtime.get("telemetry")
        if not isinstance(telemetry, str) or telemetry not in {"disabled", "unknown"}:
            errors.append(f"{prefix}.telemetry must be disabled or unknown")
        failure_modes = runtime.get("failure_modes")
        if not is_array(failure_modes) or not failure_modes:
            errors.append(f"{prefix}.failure_modes must be a non-empty array")
        elif not all(isinstance(item, str) and item for item in failure_modes):
            errors.append(f"{prefix}.failure_modes entries must be non-empty strings")
        executable_names = runtime.get("executable_names")
        if not is_array(executable_names) or not all(
            isinstance(item, str) and item for item in executable_names
        ):
            errors.append(f"{prefix}.executable_names must be a string array")
    models = registry.get("models")
    if not is_array(models):
        errors.append("registry.models must be an array")
        models = []
    model_ids: set[str] = set()
    required_model = {
        "id",
        "repository",
        "revision",
        "licence",
        "provenance_sha256",
        "task_fit",
        "input_limits",
        "context_limit",
        "quantisation",
        "device_evidence",
        "failure_modes",
        "admission_status",
        "remote_code",
    }
    allowed_model = required_model
    for index, model in enumerate(models):
        prefix = f"models[{index}]"
        if not is_object(model):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(
            f"{prefix}.{field} is required" for field in sorted(required_model - model.keys())
        )
        errors.extend(
            f"{prefix}.{field} is unknown" for field in sorted(model.keys() - allowed_model)
        )
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
        admission_status = model.get("admission_status")
        if not isinstance(admission_status, str) or admission_status not in {
            "measured_research",
            "supported",
        }:
            errors.append(f"{prefix}.admission_status is invalid")
        for field in ("task_fit", "failure_modes"):
            values = model.get(field)
            if (
                not is_array(values)
                or not values
                or not all(isinstance(item, str) and item for item in values)
            ):
                errors.append(f"{prefix}.{field} must be a non-empty string array")
        limits = model.get("input_limits")
        modalities = limits.get("modalities") if is_object(limits) else None
        if (
            not is_object(limits)
            or set(limits) != {"modalities"}
            or not is_array(modalities)
            or not modalities
            or not all(isinstance(item, str) and item for item in modalities)
        ):
            errors.append(f"{prefix}.input_limits must contain a non-empty modalities string array")
        context_limit = model.get("context_limit")
        if (
            isinstance(context_limit, bool)
            or not isinstance(context_limit, int)
            or context_limit < 1
        ):
            errors.append(f"{prefix}.context_limit must be a positive integer")
    hypotheses = registry.get("hypotheses")
    if not is_array(hypotheses):
        errors.append("registry.hypotheses must be an array")
    else:
        for index, hypothesis in enumerate(hypotheses):
            if not is_object(hypothesis) or hypothesis.get("status") != "unverified_hypothesis":
                errors.append(f"hypotheses[{index}] must remain unverified_hypothesis")
    return sorted(errors)


def discover_runtimes(registry: object) -> DiscoveryReceipt:
    errors = validate_runtime_registry(registry)
    if errors:
        raise ValueError("invalid runtime registry: " + "; ".join(errors))
    if not _is_registry_inventory(registry):
        raise ValueError("invalid runtime registry: invalid runtime field shapes")
    observations: list[Observation] = []
    for runtime in registry["runtimes"]:
        executable_names: list[str] = runtime["executable_names"]
        found = next((shutil.which(name) for name in executable_names if shutil.which(name)), None)
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
    receipt: DiscoveryBody = {
        "schema_version": SCHEMA_VERSION,
        "scope": "read_only_runtime_discovery_no_execution",
        "observations": observations,
        "network": "not_used",
        "telemetry": "not_used",
        "model_executed": False,
    }
    return {**receipt, "receipt_sha256": _digest(receipt)}


def validate_discovery_receipt(discovery: object, registry: object) -> list[str]:
    if not is_object(discovery):
        return ["discovery must be an object"]
    errors: list[str] = []
    expected_fields = {
        "schema_version",
        "scope",
        "observations",
        "network",
        "telemetry",
        "model_executed",
        "receipt_sha256",
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
    if not is_array(observations):
        errors.append("discovery.observations must be an array")
        return sorted(errors)
    safe_registry = registry if is_object(registry) else {}
    runtimes = safe_registry.get("runtimes", [])
    if not is_array(runtimes):
        runtimes = []
    runtime_ids = [item.get("id") for item in runtimes if is_object(item)]
    observed_ids = [item.get("runtime_id") for item in observations if is_object(item)]
    if (
        len(runtime_ids) != len(runtimes)
        or len(observed_ids) != len(observations)
        or any(not isinstance(identifier, str) for identifier in [*runtime_ids, *observed_ids])
        or set(observed_ids) != set(runtime_ids)
        or len(set(observed_ids)) != len(observed_ids)
    ):
        errors.append("discovery observations must bind every registered runtime exactly once")
    for index, observation in enumerate(observations):
        if not is_object(observation):
            continue
        observed_state = observation.get("observed_state")
        if not isinstance(observed_state, str) or observed_state not in {
            "installed_unmeasured",
            "unavailable",
        }:
            errors.append(
                f"discovery.observations[{index}] cannot contain measured support evidence"
            )
        if observation.get("support_state") != "unsupported_without_execution_receipt":
            errors.append(f"discovery.observations[{index}] must remain unsupported")
        observation_fields = {
            "runtime_id",
            "observed_state",
            "executable_observed",
            "executable_path",
            "version",
            "support_state",
        }
        if set(observation) != observation_fields:
            errors.append(f"discovery.observations[{index}] fields are invalid")
        if observation.get("executable_path") is not None:
            errors.append(f"discovery.observations[{index}] executable path must be redacted")
        executable_observed = observation.get("executable_observed")
        if not isinstance(executable_observed, bool):
            errors.append(f"discovery.observations[{index}] executable_observed must be boolean")
        expected_version = "unmeasured" if executable_observed else "unavailable"
        expected_state = "installed_unmeasured" if executable_observed else "unavailable"
        if (
            observation.get("version") != expected_version
            or observation.get("observed_state") != expected_state
        ):
            errors.append(f"discovery.observations[{index}] state is inconsistent")
    return sorted(errors)


def validate_bundle_manifest(manifest: object, root: Path) -> list[str]:
    if not is_object(manifest):
        return ["bundle manifest must be an object"]
    errors: list[str] = []
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("bundle.schema_version must be 1.0")
    if manifest.get("network") != "offline" or manifest.get("redistribution") is not False:
        errors.append("bundle must be offline and non-redistributable")
    entries = manifest.get("files")
    if not is_array(entries) or not entries:
        return sorted([*errors, "bundle.files must be a non-empty array"])
    root = root.resolve()
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"files[{index}]"
        if not is_object(entry):
            errors.append(f"{prefix} must be an object")
            continue
        relative = entry.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append(f"{prefix}.path must be a non-empty string")
            continue
        candidate_relative = Path(relative)
        if (
            candidate_relative.is_absolute()
            or PurePosixPath(relative).is_absolute()
            or PureWindowsPath(relative).is_absolute()
            or ".." in candidate_relative.parts
            or ".." in PurePosixPath(relative).parts
            or ".." in PureWindowsPath(relative).parts
        ):
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
    declared = {str(entry.get("path")).casefold() for entry in entries if is_object(entry)}
    allowed_directories = {
        str(parent).casefold()
        for entry in entries
        if is_object(entry) and isinstance(entry_path := entry.get("path"), str)
        for parent in Path(entry_path).parents
        if str(parent) != "."
    }
    for path in root.rglob("*"):
        relative = str(path.relative_to(root)).casefold()
        if path.is_symlink():
            errors.append(f"bundle contains undeclared symlink: {relative}")
        elif path.is_dir() and relative not in allowed_directories:
            errors.append(f"bundle contains undeclared directory: {relative}")
        elif not path.is_file() and not path.is_dir():
            errors.append(f"bundle contains unsupported filesystem entry: {relative}")
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
    registry: object,
    discovery: object,
) -> RouteReceipt:
    reasons: list[str] = []
    registry_errors = validate_runtime_registry(registry)
    reasons.extend(f"registry invalid: {error}" for error in registry_errors)
    discovery_errors = validate_discovery_receipt(discovery, registry)
    reasons.extend(f"discovery invalid: {error}" for error in discovery_errors)
    if not is_object(request):
        reasons.append("request must be an object")
        request = {}
    required = {"task", "modality", "data_class", "runtime_id", "model_id", "context_tokens"}
    reasons.extend(f"request.{key} is required" for key in sorted(required - request.keys()))
    data_class = request.get("data_class")
    if not isinstance(data_class, str) or data_class not in DATA_CLASSES:
        reasons.append("request.data_class is invalid")
    context_tokens = request.get("context_tokens")
    if (
        isinstance(context_tokens, bool)
        or not isinstance(context_tokens, int)
        or context_tokens < 1
    ):
        reasons.append("request.context_tokens must be a positive integer")
    if request.get("allow_external") is not False:
        reasons.append("external routing is forbidden")
    if request.get("allow_remote_code") is not False:
        reasons.append("remote code is forbidden")
    safe_registry = registry if is_object(registry) else {}
    safe_discovery = discovery if is_object(discovery) else {}
    runtimes = safe_registry.get("runtimes", [])
    models = safe_registry.get("models", [])
    observations = safe_discovery.get("observations", [])
    runtimes = runtimes if is_array(runtimes) else []
    models = models if is_array(models) else []
    observations = observations if is_array(observations) else []
    runtime = next(
        (
            item
            for item in runtimes
            if is_object(item) and item.get("id") == request.get("runtime_id")
        ),
        None,
    )
    model = next(
        (item for item in models if is_object(item) and item.get("id") == request.get("model_id")),
        None,
    )
    observation = next(
        (
            item
            for item in observations
            if is_object(item) and item.get("runtime_id") == request.get("runtime_id")
        ),
        None,
    )
    if runtime is None:
        reasons.append("runtime is not registered")
    elif runtime.get("network") != "none" or runtime.get("telemetry") != "disabled":
        reasons.append("runtime isolation is not established")
    observed_state = observation.get("observed_state") if observation is not None else None
    if not isinstance(observed_state, str) or observed_state not in {
        "measured_research",
        "supported",
    }:
        reasons.append("runtime lacks a measured execution receipt")
    if model is None:
        reasons.append("model is not admitted")
    else:
        admission_status = model.get("admission_status")
        if not isinstance(admission_status, str) or admission_status not in {
            "measured_research",
            "supported",
        }:
            reasons.append("model lacks measured admission")
        model_limit = model.get("context_limit")
        if (
            isinstance(context_tokens, int)
            and not isinstance(context_tokens, bool)
            and isinstance(model_limit, int)
            and not isinstance(model_limit, bool)
            and context_tokens > model_limit
        ):
            reasons.append("requested context exceeds measured limit")
        task_fit = model.get("task_fit")
        if not is_array(task_fit) or request.get("task") not in task_fit:
            reasons.append("task is unsupported")
        input_limits = model.get("input_limits")
        modalities = input_limits.get("modalities") if is_object(input_limits) else None
        if not is_array(modalities) or request.get("modality") not in modalities:
            reasons.append("modality is unsupported")
    if request.get("data_class") == "governed_private":
        reasons.append("governed-private routing requires separately verified local isolation")
    result: RouteBody = {
        "status": "no_capability" if reasons else "eligible_local_route",
        "reasons": sorted(set(reasons)),
        "external_fallback": False,
        "model_executed": False,
    }
    return {**result, "receipt_sha256": _digest(result)}


def recommendation_matrix(
    registry: object, discovery: object, *, date: str
) -> RecommendationMatrix:
    validation_errors = [
        *validate_runtime_registry(registry),
        *validate_discovery_receipt(discovery, registry),
    ]
    if validation_errors:
        raise ValueError("invalid recommendation evidence: " + "; ".join(validation_errors))
    if not _is_registry_inventory(registry) or not _is_discovery_inventory(discovery):
        raise ValueError("invalid recommendation evidence: invalid runtime field shapes")
    rows: list[RecommendationRow] = []
    observed = {item["runtime_id"]: item["observed_state"] for item in discovery["observations"]}
    for runtime in registry["runtimes"]:
        state = observed.get(runtime["id"], "unavailable")
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
    matrix: MatrixBody = {
        "schema_version": SCHEMA_VERSION,
        "date": date,
        "scope": "internal_non_operational_recommendation",
        "rows": rows,
        "agent_agreement": {
            "status": "unanimous_accept",
            "reviewed_revision": "8000b2c",
            "roles": ["acceptance", "security_privacy", "lifecycle_archive"],
            "human_agreement": False,
        },
        "human_agreement": False,
        "limitations": [
            "No model was downloaded or executed by Track 08.",
            "No clinical, legal, policy, organisational, deployment or public-comparison approval.",
        ],
    }
    return {**matrix, "receipt_sha256": _digest(matrix)}
