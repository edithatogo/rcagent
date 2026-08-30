"""Server eligibility uses only synthetic model, rights and runtime bytes."""

import hashlib
import json
from copy import deepcopy

import pytest

from tools import prospective_server_model as model


def sha(data):
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def admitted(tmp_path, monkeypatch):
    root = tmp_path.resolve() / "models"
    root.mkdir()
    runtime = tmp_path.resolve() / "server"
    runtime.write_bytes(b"server")
    entries = []
    for size in ("small", "medium", "larger"):
        directory = root / size
        directory.mkdir()
        (directory / "LICENSE").write_bytes(b"synthetic licence")
        data = size.encode()
        (directory / "model.gguf").write_bytes(data)
        entries.append(
            {
                "id": model.MODEL_ID if size == "small" else size,
                "size_class": size,
                "revision": "a" * 40,
                "cache_subdirectory": size,
                "license": "Apache-2.0",
                "license_sha256": sha(b"synthetic licence"),
                "admission_status": "admitted_local_research_only",
                "files": [{"path": "model.gguf", "bytes": len(data), "sha256": sha(data)}],
            }
        )
    manifest = {
        "runtime": {"name": "historical-cli", "version": "unchanged"},
        "models": entries,
        "admission_policy": {
            "data_class": "synthetic_only",
            "network": "disabled",
            **dict.fromkeys(
                (
                    "external_inference",
                    "remote_code",
                    "telemetry",
                    "redistribution",
                    "publication",
                    "promotion_eligible",
                ),
                False,
            ),
        },
    }
    registry = tmp_path.resolve() / "registry.json"
    registry.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(model, "MANIFEST_PATH", registry)
    monkeypatch.setattr(model, "REGISTRY_PIN", sha(registry.read_bytes()))
    monkeypatch.setattr(model.profile, "EXECUTABLE", str(runtime))
    monkeypatch.setattr(model.profile, "PINNED_FILES", {str(runtime): sha(b"server")})
    monkeypatch.setattr(model.profile, "profile_digest", lambda: "b" * 64)
    checks = []

    def verify():
        checks.append(True)
        if runtime.read_bytes() != b"server":
            raise ValueError("runtime_changed")

    monkeypatch.setattr(model.profile, "verify_files", verify)
    return root, registry, manifest, runtime, checks


def test_server_overlay_preserves_registry_and_is_deterministic(admitted):
    root, registry, original, _, checks = admitted
    before = registry.read_bytes()
    result = model.admit_model(root)
    assert registry.read_bytes() == before
    assert result["original_runtime"] == original["runtime"]
    assert result["runtime_overlay"]["name"] == "llama.cpp llama-server"
    assert result["runtime_overlay"]["executable"] == model.profile.EXECUTABLE
    assert result["runtime_overlay"]["executable_sha256"] == sha(b"server")
    assert result["profile_sha256"] == "b" * 64
    assert result["registry_sha256"] == sha(before)
    assert result["model_id"] == model.MODEL_ID
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["local_artifact_eligible"] is True
    assert len(checks) >= 2
    effective = deepcopy(original)
    effective["runtime"] = result["runtime_overlay"]
    assert result["effective_manifest_sha256"] == model.digest(effective)
    unsigned = {key: value for key, value in result.items() if key != "admission_sha256"}
    assert result["admission_sha256"] == model.digest(unsigned)
    assert result == model.admit_model(root)


@pytest.mark.parametrize(
    "damage", ["registry", "runtime", "model", "licence", "other-model", "other-licence", "profile"]
)
def test_preexisting_drift_rejected(admitted, monkeypatch, damage):
    root, registry, _, runtime, _ = admitted
    if damage == "registry":
        registry.write_bytes(b"changed")
    elif damage == "runtime":
        runtime.write_bytes(b"changed")
    elif damage == "profile":
        monkeypatch.setattr(
            model.profile,
            "verify_files",
            lambda: (_ for _ in ()).throw(ValueError("profile_changed")),
        )
    else:
        group = "larger" if damage.startswith("other") else "small"
        name = "LICENSE" if "licence" in damage else "model.gguf"
        (root / group / name).write_bytes(b"changed")
    with pytest.raises(ValueError):
        model.admit_model(root)


@pytest.mark.parametrize(
    "damage",
    [
        "registry",
        "runtime",
        "model",
        "licence",
        "other-model",
        "other-licence",
        "profile",
        "missing-model",
        "missing-licence",
    ],
)
def test_drift_during_validator_is_rejected(admitted, monkeypatch, damage):
    root, registry, _, runtime, _ = admitted
    original = model.validate_admission
    calls = []

    def validate(manifest, directory):
        result = original(manifest, directory)
        calls.append(True)
        if len(calls) == 1:
            if damage == "registry":
                registry.write_bytes(b"changed")
            elif damage == "runtime":
                runtime.write_bytes(b"changed")
            elif damage == "profile":
                monkeypatch.setattr(model.profile, "profile_digest", lambda: "c" * 64)
            else:
                group = "larger" if damage.startswith("other") else "small"
                path = root / group / ("LICENSE" if "licence" in damage else "model.gguf")
                if damage.startswith("missing"):
                    path.unlink()
                else:
                    path.write_bytes(b"changed")
        return result

    monkeypatch.setattr(model, "validate_admission", validate)
    with pytest.raises(ValueError):
        model.admit_model(root)


@pytest.mark.parametrize(
    "kind", ["missing", "regular-file", "symlink", "parent-symlink", "traversal"]
)
def test_unsafe_roots_fail_before_profile(admitted, monkeypatch, kind):
    root, _, _, _, _ = admitted
    if kind == "missing":
        root = root.parent / "absent"
    elif kind == "regular-file":
        root = root.parent / "file"
        root.write_bytes(b"not a directory")
    elif kind == "symlink":
        alias = root.parent / "alias"
        alias.symlink_to(root, target_is_directory=True)
        root = alias
    elif kind == "parent-symlink":
        alias = root.parent / "alias"
        alias.symlink_to(root.parent, target_is_directory=True)
        root = alias / "models"
    else:
        nested = root / "nested"
        nested.mkdir()
        root = nested / ".."

    def forbidden():
        raise AssertionError("profile must not be read")

    monkeypatch.setattr(model.profile, "verify_files", forbidden)
    with pytest.raises(ValueError):
        model.admit_model(root)


def test_selected_identity_missing(admitted, monkeypatch):
    monkeypatch.setattr(model, "MODEL_ID", "missing")
    with pytest.raises(ValueError):
        model.admit_model(admitted[0])


def test_profile_changes_during_its_first_verification(admitted, monkeypatch):
    def verify():
        monkeypatch.setattr(model.profile, "profile_digest", lambda: "c" * 64)

    monkeypatch.setattr(model.profile, "verify_files", verify)
    with pytest.raises(ValueError):
        model.admit_model(admitted[0])


def test_profile_id_change_is_rejected_even_if_digest_helper_is_stale(admitted, monkeypatch):
    def verify():
        monkeypatch.setattr(model.profile, "PROFILE_ID", "changed-server-profile")

    monkeypatch.setattr(model.profile, "verify_files", verify)
    with pytest.raises(ValueError, match="server_profile_changed"):
        model.admit_model(admitted[0])


@pytest.mark.parametrize("kind", ["symlink", "replacement"])
def test_root_replacement_during_final_profile_check_is_rejected(admitted, monkeypatch, kind):
    import shutil

    root = admitted[0]
    calls = []

    def verify():
        calls.append(True)
        if len(calls) == 2:
            saved = root.with_name("saved")
            root.rename(saved)
            if kind == "symlink":
                root.symlink_to(saved, target_is_directory=True)
            else:
                shutil.copytree(saved, root)

    monkeypatch.setattr(model.profile, "verify_files", verify)
    with pytest.raises(ValueError):
        model.admit_model(root)


def test_registry_bytes_change_between_pin_and_read_is_rejected(admitted, monkeypatch):
    from pathlib import Path

    registry = admitted[1]
    real_read = Path.read_bytes
    monkeypatch.setattr(
        Path, "read_bytes", lambda path: b"{}" if path == registry else real_read(path)
    )
    with pytest.raises(ValueError, match="registry_changed"):
        model.admit_model(admitted[0])


def test_selected_path_missing_after_validations_is_rejected(admitted, monkeypatch):
    monkeypatch.setattr(model, "_admitted_file", lambda *args: None)
    with pytest.raises(ValueError, match="selected_model_files_unavailable"):
        model.admit_model(admitted[0])


def test_selected_bytes_changed_after_final_validator_is_rejected(admitted, monkeypatch):
    real_validate = model.validate_admission
    calls = []

    def validate(manifest, root):
        result = real_validate(manifest, root)
        calls.append(True)
        if len(calls) == 2:
            (root / "small" / "model.gguf").write_bytes(b"changed")
        return result

    monkeypatch.setattr(model, "validate_admission", validate)
    with pytest.raises(ValueError, match="selected_model_files_changed"):
        model.admit_model(admitted[0])
