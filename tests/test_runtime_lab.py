from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools import runtime_lab

ROOT = Path(__file__).parents[1]


def registry() -> dict:
    return json.loads((ROOT / "evaluation/runtime-lab/registry.json").read_text())


def test_registry_is_valid_and_has_no_admitted_models() -> None:
    value = registry()
    assert runtime_lab.validate_runtime_registry(value) == []
    assert value["models"] == []
    assert all(item["status"] == "unverified_hypothesis" for item in value["hypotheses"])
    schema = json.loads((ROOT / "conductor/schemas/runtime-lab.schema.json").read_text())
    assert list(Draft202012Validator(schema).iter_errors(value)) == []


def test_registry_rejects_unknown_policy_duplicate_and_mutable_model() -> None:
    value = registry()
    value["unknown"] = True
    value["policy"]["downloads"] = True
    value["runtimes"].append(dict(value["runtimes"][0]))
    value["models"] = [{"id": "m", "revision": "main", "provenance_sha256": "bad"}]
    errors = runtime_lab.validate_runtime_registry(value)
    assert "registry: unknown field unknown" in errors
    assert "registry.policy.downloads must be false" in errors
    assert "runtimes[5].id is duplicated" in errors
    assert "models[0].revision must be immutable and exact" in errors
    assert "models[0].remote_code must be false" in errors


@pytest.mark.parametrize("value", [None, [], "bad"])
def test_registry_rejects_non_object(value: object) -> None:
    assert runtime_lab.validate_runtime_registry(value) == ["registry must be an object"]


def test_registry_reports_malformed_collections_and_runtime_fields() -> None:
    value = registry()
    value.update(schema_version="bad", policy=None, runtimes=[None, {}], models="bad", hypotheses="bad")
    errors = runtime_lab.validate_runtime_registry(value)
    assert "registry.schema_version must be 1.0" in errors
    assert "registry.policy must be an object" in errors
    assert "runtimes[0] must be an object" in errors
    assert "runtimes[1].id must be a non-empty string" in errors
    assert "runtimes[1].dependency_class is invalid" in errors
    assert "runtimes[1].support_state is invalid" in errors
    assert "runtimes[1].remote_code must be false" in errors
    assert "runtimes[1].network must be none or unknown" in errors
    assert "runtimes[1].telemetry must be disabled or unknown" in errors
    assert "runtimes[1].failure_modes must be a non-empty array" in errors
    assert "registry.models must be an array" in errors
    assert "registry.hypotheses must be an array" in errors


def test_registry_reports_malformed_models_and_hypotheses() -> None:
    value = registry()
    valid = {
        "id": "duplicate", "repository": "owner/repo", "revision": "abcdef012345",
        "licence": "Apache-2.0", "provenance_sha256": "a" * 64, "task_fit": ["none"],
        "input_limits": {"modalities": ["text"]}, "context_limit": 1, "quantisation": "none",
        "device_evidence": "none", "failure_modes": ["unknown"],
        "admission_status": "unsupported", "remote_code": False,
    }
    value["models"] = [None, {}, valid, dict(valid)]
    value["hypotheses"] = [None, {"status": "verified"}]
    errors = runtime_lab.validate_runtime_registry(value)
    assert "models[0] must be an object" in errors
    assert "models[1].id must be a non-empty string" in errors
    assert "models[1].provenance_sha256 must be sha256" in errors
    assert "models[3].id is duplicated" in errors
    assert "hypotheses[0] must remain unverified_hypothesis" in errors


def test_discovery_rejects_invalid_registry() -> None:
    with pytest.raises(ValueError, match="invalid runtime registry"):
        runtime_lab.discover_runtimes({})


def test_device_profile_is_coarse_and_excludes_identifiers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", "/Users/[Clinician A]")
    monkeypatch.setenv("HF_TOKEN", "secret-sentinel")
    profile = runtime_lab.privacy_safe_device_profile(memory_bytes=35 * 1024**3)
    encoded = json.dumps(profile)
    assert profile["memory_gib_floor"] == 32
    assert profile["identifiers_redacted"] is True
    for forbidden in ("Clinician", "secret-sentinel", "hostname", "username", "serial"):
        assert forbidden not in encoded
    assert len(profile["receipt_sha256"]) == 64
    assert runtime_lab.validate_device_profile(profile) == []
    assert profile["storage_probe_state"] == "unobserved"
    assert profile["driver_state"] == "unobserved"


def test_device_profile_validator_fails_closed() -> None:
    assert runtime_lab.validate_device_profile([]) == ["device profile must be an object"]
    profile = runtime_lab.privacy_safe_device_profile()
    profile["identifiers_redacted"] = False
    profile["extra"] = "identifier"
    errors = runtime_lab.validate_device_profile(profile)
    assert "device profile fields are invalid" in errors
    assert "device identifiers must be redacted" in errors
    assert "device profile receipt hash mismatched" in errors
    profile = runtime_lab.privacy_safe_device_profile()
    profile["os_family"] = "secret-sentinel"
    unsigned = {key: value for key, value in profile.items() if key != "receipt_sha256"}
    profile["receipt_sha256"] = runtime_lab._digest(unsigned)
    assert "device os_family is not a coarse allowed value" in runtime_lab.validate_device_profile(profile)


def test_discovery_never_exposes_paths_or_executes_models(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runtime_lab.shutil, "which", lambda name: f"/private/{name}" if name == "llama-cli" else None)
    receipt = runtime_lab.discover_runtimes(registry())
    observed = {item["runtime_id"]: item for item in receipt["observations"]}
    assert observed["llama-cpp"]["observed_state"] == "installed_unmeasured"
    assert observed["llama-cpp"]["executable_path"] is None
    assert receipt["model_executed"] is False
    assert receipt["network"] == "not_used"
    assert runtime_lab.validate_discovery_receipt(receipt, registry()) == []


def test_discovery_validator_rejects_rehashed_private_fields() -> None:
    receipt = runtime_lab.discover_runtimes(registry())
    receipt["observations"][0]["executable_path"] = "/Users/[Clinician A]/private"
    receipt["observations"][0]["secret"] = "HF_TOKEN=value"
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = runtime_lab._digest(unsigned)
    errors = runtime_lab.validate_discovery_receipt(receipt, registry())
    assert "discovery.observations[0] fields are invalid" in errors
    assert "discovery.observations[0] executable path must be redacted" in errors


def _bundle(tmp_path: Path) -> tuple[dict, Path]:
    root = tmp_path / "bundle"
    root.mkdir()
    payload = root / "runtime.bin"
    payload.write_bytes(b"runtime")
    return {
        "schema_version": "1.0",
        "network": "offline",
        "redistribution": False,
        "files": [{"path": payload.name, "bytes": 7, "sha256": runtime_lab._sha256(payload)}],
    }, root


def test_offline_bundle_verifies_operator_owned_bytes(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    assert runtime_lab.validate_bundle_manifest(manifest, root) == []


@pytest.mark.parametrize("path", ["../escape", "/absolute", "sub/../../escape"])
def test_bundle_rejects_path_escape(tmp_path: Path, path: str) -> None:
    manifest, root = _bundle(tmp_path)
    manifest["files"][0]["path"] = path
    assert any("escapes bundle root" in error for error in runtime_lab.validate_bundle_manifest(manifest, root))


def test_bundle_rejects_symlink_hash_drift_and_case_collision(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    outside = tmp_path / "outside"
    outside.write_bytes(b"runtime")
    link = root / "link"
    link.symlink_to(outside)
    manifest["files"] = [
        {"path": "link", "bytes": 7, "sha256": runtime_lab._sha256(outside)},
        {"path": "LINK", "bytes": 7, "sha256": "0" * 64},
    ]
    errors = runtime_lab.validate_bundle_manifest(manifest, root)
    assert "files[0].path contains a symlink" in errors
    assert "files[1].path is duplicated or case-colliding" in errors


def test_bundle_rejects_malformed_and_mismatched_manifest(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    manifest["network"] = "online"
    manifest["files"][0]["bytes"] = 999
    manifest["files"][0]["sha256"] = "0" * 64
    errors = runtime_lab.validate_bundle_manifest(manifest, root)
    assert "bundle must be offline and non-redistributable" in errors
    assert "files[0].bytes mismatched" in errors
    assert "files[0].sha256 mismatched" in errors
    assert runtime_lab.validate_bundle_manifest([], root) == ["bundle manifest must be an object"]


def test_bundle_rejects_empty_non_object_missing_and_bad_hash(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    manifest["schema_version"] = "bad"
    manifest["files"] = []
    assert "bundle.files must be a non-empty array" in runtime_lab.validate_bundle_manifest(manifest, root)
    manifest["files"] = [None, {}, {"path": "missing", "bytes": 1, "sha256": "bad"}]
    errors = runtime_lab.validate_bundle_manifest(manifest, root)
    assert "files[0] must be an object" in errors
    assert "files[1].path must be a non-empty string" in errors
    assert "files[2].path is missing or outside bundle root" in errors


def test_bundle_rejects_nonregular_directory_and_malformed_hash(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    directory = root / "directory"
    directory.mkdir()
    manifest["files"] = [{"path": "directory", "bytes": 0, "sha256": "bad"}]
    assert "files[0].path must be a regular non-symlink file" in runtime_lab.validate_bundle_manifest(manifest, root)
    manifest["files"] = [{"path": "runtime.bin", "bytes": 7, "sha256": "bad"}]
    assert "files[0].sha256 must be sha256" in runtime_lab.validate_bundle_manifest(manifest, root)


def test_bundle_rejects_intermediate_symlink_and_undeclared_file(tmp_path: Path) -> None:
    manifest, root = _bundle(tmp_path)
    real = root / "real"
    real.mkdir()
    nested = real / "nested.bin"
    nested.write_bytes(b"nested")
    alias = root / "alias"
    alias.symlink_to(real, target_is_directory=True)
    manifest["files"] = [{
        "path": "alias/nested.bin", "bytes": 6, "sha256": runtime_lab._sha256(nested)
    }]
    errors = runtime_lab.validate_bundle_manifest(manifest, root)
    assert "files[0].path contains a symlink" in errors
    other = tmp_path / "other"
    other.mkdir()
    manifest, root = _bundle(other)
    (root / "extra.bin").write_bytes(b"extra")
    assert "bundle inventory does not exactly match regular files" in runtime_lab.validate_bundle_manifest(manifest, root)
    outside = tmp_path / "secret"
    outside.write_bytes(b"secret")
    (root / "extra-link").symlink_to(outside)
    errors = runtime_lab.validate_bundle_manifest(manifest, root)
    assert "bundle contains undeclared symlink: extra-link" in errors


def test_routing_fails_closed_without_measured_runtime_and_model() -> None:
    discovery = runtime_lab.discover_runtimes(registry())
    request = {
        "task": "summarisation",
        "modality": "text",
        "data_class": "synthetic",
        "runtime_id": "llama-cpp",
        "model_id": "missing",
        "context_tokens": 100,
        "allow_external": False,
        "allow_remote_code": False,
    }
    result = runtime_lab.route_request(request, registry(), discovery)
    assert result["status"] == "no_capability"
    assert result["external_fallback"] is False
    assert result["model_executed"] is False
    assert "model is not admitted" in result["reasons"]
    assert "runtime lacks a measured execution receipt" in result["reasons"]


def test_routing_rejects_private_external_remote_code_and_missing_fields() -> None:
    result = runtime_lab.route_request(
        {"data_class": "governed_private", "allow_external": True, "allow_remote_code": True},
        registry(),
        {"observations": []},
    )
    assert result["status"] == "no_capability"
    assert "external routing is forbidden" in result["reasons"]
    assert "remote code is forbidden" in result["reasons"]
    assert "request.task is required" in result["reasons"]
    assert "request.data_class is invalid" not in result["reasons"]


def test_routing_rejects_nonobject_and_unisolated_runtime() -> None:
    result = runtime_lab.route_request(None, registry(), {"observations": []})
    assert "request must be an object" in result["reasons"]
    value = registry()
    runtime = next(item for item in value["runtimes"] if item["id"] == "openvino")
    request = {
        "task": "unknown", "modality": "text", "data_class": "invalid",
        "runtime_id": runtime["id"], "model_id": "none", "context_tokens": 1,
        "allow_external": False, "allow_remote_code": False,
    }
    reasons = runtime_lab.route_request(request, value, {"observations": []})["reasons"]
    assert "request.data_class is invalid" in reasons
    assert "runtime isolation is not established" in reasons


@pytest.mark.parametrize(
    ("bad_registry", "bad_discovery"),
    [(None, {}), (registry(), None), (registry(), []), ({"runtimes": "bad", "models": []}, {})],
)
def test_routing_malformed_evidence_returns_no_capability(
    bad_registry: object, bad_discovery: object
) -> None:
    result = runtime_lab.route_request({}, bad_registry, bad_discovery)
    assert result["status"] == "no_capability"
    assert any(reason.startswith(("registry invalid:", "discovery invalid:")) for reason in result["reasons"])


def test_forged_measured_evidence_cannot_become_eligible() -> None:
    value = registry()
    value["models"] = [{
        "id": "model-1", "repository": "owner/repo", "revision": "abcdef0123456789",
        "licence": "Apache-2.0", "provenance_sha256": "a" * 64,
        "task_fit": ["summarisation"], "input_limits": {"modalities": ["text"]},
        "context_limit": 2048, "quantisation": "q4", "device_evidence": "receipt",
        "failure_modes": ["hallucination"], "admission_status": "measured_research",
        "remote_code": False,
    }]
    discovery = runtime_lab.discover_runtimes(value)
    observation = next(item for item in discovery["observations"] if item["runtime_id"] == "llama-cpp")
    observation["observed_state"] = "measured_research"
    unsigned = {key: val for key, val in discovery.items() if key != "receipt_sha256"}
    discovery["receipt_sha256"] = runtime_lab._digest(unsigned)
    request = {
        "task": "summarisation", "modality": "text", "data_class": "synthetic",
        "runtime_id": "llama-cpp", "model_id": "model-1", "context_tokens": 512,
        "allow_external": False, "allow_remote_code": False,
    }
    result = runtime_lab.route_request(request, value, discovery)
    assert result["status"] == "no_capability"
    assert any("cannot contain measured support evidence" in reason for reason in result["reasons"])
    request["context_tokens"] = 4096
    assert "requested context exceeds measured limit" in runtime_lab.route_request(request, value, discovery)["reasons"]
    value["models"][0]["admission_status"] = "pending"
    request["task"] = "other"
    reasons = runtime_lab.route_request(request, value, discovery)["reasons"]
    assert "model lacks measured admission" in reasons
    assert "task is unsupported" in reasons


@pytest.mark.parametrize("value", ["1", True, 0, -1])
def test_route_rejects_malformed_context_without_crashing(value: object) -> None:
    request = {
        "task": "summarisation", "modality": "text", "data_class": "synthetic",
        "runtime_id": "llama-cpp", "model_id": "none", "context_tokens": value,
        "allow_external": False, "allow_remote_code": False,
    }
    result = runtime_lab.route_request(request, registry(), runtime_lab.discover_runtimes(registry()))
    assert "request.context_tokens must be a positive integer" in result["reasons"]


def test_route_rejects_modality_and_governed_private() -> None:
    value = registry()
    value["models"] = [{
        "id": "m", "repository": "owner/repo", "revision": "abcdef012345",
        "licence": "Apache-2.0", "provenance_sha256": "a" * 64,
        "task_fit": ["summarisation"], "input_limits": {"modalities": ["text"]},
        "context_limit": 2048, "quantisation": "q4", "device_evidence": "receipt",
        "failure_modes": ["hallucination"], "admission_status": "measured_research",
        "remote_code": False,
    }]
    discovery = runtime_lab.discover_runtimes(value)
    request = {
        "task": "summarisation", "modality": "image", "data_class": "governed_private",
        "runtime_id": "llama-cpp", "model_id": "m", "context_tokens": 1,
        "allow_external": False, "allow_remote_code": False,
    }
    reasons = runtime_lab.route_request(request, value, discovery)["reasons"]
    assert "modality is unsupported" in reasons
    assert "governed-private routing requires separately verified local isolation" in reasons


def test_recommendations_remain_unsupported_without_promotion_evidence() -> None:
    discovery = runtime_lab.discover_runtimes(registry())
    matrix = runtime_lab.recommendation_matrix(registry(), discovery, date="2026-08-29")
    assert {row["classification"] for row in matrix["rows"]} == {"unsupported"}
    assert matrix["human_agreement"] is False
    assert all(row["public_comparative_claim"] is False for row in matrix["rows"])
    forged = json.loads(json.dumps(discovery))
    forged["observations"][0]["observed_state"] = "supported"
    unsigned = {key: value for key, value in forged.items() if key != "receipt_sha256"}
    forged["receipt_sha256"] = runtime_lab._digest(unsigned)
    with pytest.raises(ValueError, match="cannot contain measured support evidence"):
        runtime_lab.recommendation_matrix(registry(), forged, date="2026-08-29")


def test_durable_discovery_and_recommendation_receipts_reproduce(monkeypatch: pytest.MonkeyPatch) -> None:
    observed = json.loads(
        (ROOT / "evaluation/runtime-lab/runtime-discovery-20260829.json").read_text()
    )
    installed = {
        item["runtime_id"]
        for item in observed["observations"]
        if item["executable_observed"]
    }
    names_by_runtime = {
        item["id"]: set(item["executable_names"])
        for item in registry()["runtimes"]
    }
    installed_names = set().union(*(names_by_runtime[item] for item in installed))
    monkeypatch.setattr(
        runtime_lab.shutil,
        "which",
        lambda name: f"/redacted/{name}" if name in installed_names else None,
    )
    assert runtime_lab.discover_runtimes(registry()) == observed
    expected_matrix = json.loads(
        (ROOT / "evaluation/runtime-lab/recommendation-matrix-20260829.json").read_text()
    )
    assert runtime_lab.recommendation_matrix(
        registry(), observed, date="2026-08-29"
    ) == expected_matrix
