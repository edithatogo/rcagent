from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import runtime_lab

ROOT = Path(__file__).parents[1]


def registry() -> dict:
    return json.loads((ROOT / "evaluation/runtime-lab/registry.json").read_text())


def test_registry_is_valid_and_has_no_admitted_models() -> None:
    value = registry()
    assert runtime_lab.validate_runtime_registry(value) == []
    assert value["models"] == []
    assert all(item["status"] == "unverified_hypothesis" for item in value["hypotheses"])


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


def test_discovery_never_exposes_paths_or_executes_models(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runtime_lab.shutil, "which", lambda name: f"/private/{name}" if name == "llama-cli" else None)
    receipt = runtime_lab.discover_runtimes(registry())
    observed = {item["runtime_id"]: item for item in receipt["observations"]}
    assert observed["llama-cpp"]["observed_state"] == "installed_unmeasured"
    assert observed["llama-cpp"]["executable_path"] is None
    assert receipt["model_executed"] is False
    assert receipt["network"] == "not_used"


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
    assert "files[0].path is missing or outside bundle root" in errors or "files[0].path must be a regular non-symlink file" in errors
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


def test_route_can_only_be_eligible_with_explicit_measured_evidence() -> None:
    value = registry()
    value["models"] = [{
        "id": "model-1", "repository": "owner/repo", "revision": "abcdef0123456789",
        "licence": "Apache-2.0", "provenance_sha256": "a" * 64,
        "task_fit": ["summarisation"], "input_limits": {"modality": "text"},
        "context_limit": 2048, "quantisation": "q4", "device_evidence": "receipt",
        "failure_modes": ["hallucination"], "admission_status": "measured_research",
        "remote_code": False,
    }]
    discovery = {"observations": [{"runtime_id": "llama-cpp", "observed_state": "measured_research"}]}
    request = {
        "task": "summarisation", "modality": "text", "data_class": "synthetic",
        "runtime_id": "llama-cpp", "model_id": "model-1", "context_tokens": 512,
        "allow_external": False, "allow_remote_code": False,
    }
    assert runtime_lab.route_request(request, value, discovery)["status"] == "eligible_local_route"
    request["context_tokens"] = 4096
    assert "requested context exceeds measured limit" in runtime_lab.route_request(request, value, discovery)["reasons"]


def test_recommendations_remain_unsupported_without_promotion_evidence() -> None:
    discovery = runtime_lab.discover_runtimes(registry())
    matrix = runtime_lab.recommendation_matrix(registry(), discovery, date="2026-08-29")
    assert {row["classification"] for row in matrix["rows"]} == {"unsupported"}
    assert matrix["human_agreement"] is False
    assert all(row["public_comparative_claim"] is False for row in matrix["rows"])


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
