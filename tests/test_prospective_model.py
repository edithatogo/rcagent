"""Synthetic admission-overlay fixtures; never read real models."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import TypeAlias

import pytest

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools import prospective_model as model

AdmittedFixture: TypeAlias = tuple[Path, Path, ObjectMap]


@pytest.fixture
def admitted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AdmittedFixture:
    root = tmp_path / "models"
    root.mkdir()
    runtime = tmp_path / "runtime"
    runtime.write_bytes(b"runtime")
    manifest = mapping(json.loads(model.MANIFEST_PATH.read_bytes()))
    for raw_item in sequence(manifest["models"]):
        item = mapping(raw_item)
        directory = root / text_value(item["cache_subdirectory"])
        directory.mkdir()
        (directory / "LICENSE").write_bytes(b"synthetic licence")
        item["license_sha256"] = hashlib.sha256(b"synthetic licence").hexdigest()
        for raw_file in sequence(item["files"]):
            file = mapping(raw_file)
            name = text_value(file["path"])
            data = name.encode()
            (directory / name).write_bytes(data)
            file.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    source = tmp_path / "registry.json"
    source.write_text(json.dumps(manifest))
    monkeypatch.setattr(model, "MANIFEST_PATH", source)
    monkeypatch.setattr(model, "REGISTRY_PIN", hashlib.sha256(source.read_bytes()).hexdigest())
    monkeypatch.setattr(model.profile, "EXECUTABLE", str(runtime))
    monkeypatch.setattr(
        model.profile, "PINNED_FILES", {str(runtime): hashlib.sha256(b"runtime").hexdigest()}
    )
    monkeypatch.setattr(model.profile, "verify_files", lambda: None)
    return root, source, manifest


def test_overlay_preserves_registry_and_all_model_checks(admitted: AdmittedFixture) -> None:
    root, source, original = admitted
    before = source.read_bytes()
    result = model.admit_model(root)
    assert source.read_bytes() == before
    assert json.loads(before) == original
    assert result["runtime_overlay"]["version"] != mapping(original["runtime"])["version"]
    assert (
        result["runtime_overlay"]["distribution"]
        == f"Homebrew installed bytes; explicit {model.profile.PROFILE_ID} profile"
    )
    assert result["registry_sha256"] == hashlib.sha256(before).hexdigest()
    assert result["model_id"] == model.MODEL_ID
    assert result["original_runtime"] == original["runtime"]
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["local_artifact_eligible"] is True
    assert result == model.admit_model(root)
    unsigned: dict[str, object]
    unsigned = {key: value for key, value in result.items() if key != "admission_sha256"}
    assert result["admission_sha256"] == model.digest(unsigned)


@pytest.mark.parametrize(
    "damage", ["registry", "licence", "other_model", "runtime", "profile", "root"]
)
def test_admission_rejects_drift(
    admitted: AdmittedFixture, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    root, source, manifest = admitted
    if damage == "registry":
        source.write_bytes(b"{}")
    elif damage == "licence":
        first = mapping(sequence(manifest["models"])[0])
        (root / text_value(first["cache_subdirectory"]) / "LICENSE").write_bytes(b"changed")
    elif damage == "other_model":
        item = mapping(sequence(manifest["models"])[-1])
        file = mapping(sequence(item["files"])[0])
        (root / text_value(item["cache_subdirectory"]) / text_value(file["path"])).unlink()
    elif damage == "runtime":
        Path(model.profile.EXECUTABLE).write_bytes(b"changed")
    elif damage == "profile":
        monkeypatch.setattr(
            model.profile, "verify_files", lambda: (_ for _ in ()).throw(ValueError("changed"))
        )
    else:
        alias = root.parent / "alias"
        alias.symlink_to(root, target_is_directory=True)
        root = alias
    with pytest.raises(ValueError):
        model.admit_model(root)


def test_registry_drift_during_validation(
    admitted: AdmittedFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, source, _ = admitted

    def validate(*args: object) -> list[str]:
        source.write_bytes(b"changed")
        return []

    monkeypatch.setattr(model, "validate_admission", validate)
    with pytest.raises(ValueError):
        model.admit_model(root)


def test_missing_selected_model(admitted: AdmittedFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, _ = admitted
    monkeypatch.setattr(model, "MODEL_ID", "absent")
    with pytest.raises(ValueError):
        model.admit_model(root)


@pytest.mark.parametrize("which", ["model", "licence"])
@pytest.mark.parametrize("damage", ["missing", "changed"])
def test_selected_file_disappears_after_validation(
    admitted: AdmittedFixture, monkeypatch: pytest.MonkeyPatch, which: str, damage: str
) -> None:
    root, _, manifest = admitted
    selected = mapping(sequence(manifest["models"])[0])

    def validate(*args: object) -> list[str]:
        file = mapping(sequence(selected["files"])[0])
        name = text_value(file["path"]) if which == "model" else "LICENSE"
        path = root / text_value(selected["cache_subdirectory"]) / name
        if damage == "missing":
            path.unlink()
        else:
            path.write_bytes(b"changed")
        return []

    monkeypatch.setattr(model, "validate_admission", validate)
    with pytest.raises(ValueError):
        model.admit_model(root)


def test_overlay_identity_is_complete_and_separate(admitted: AdmittedFixture) -> None:
    root, _, manifest = admitted
    copy = deepcopy(manifest)
    result = model.admit_model(root)
    copy["runtime"] = result["runtime_overlay"]
    assert result["effective_manifest_sha256"] == model.digest(copy)
    assert "23.1.0" in " ".join(result["runtime_overlay"]["runtime_dependencies"])


@pytest.mark.parametrize("kind", ["missing", "file"])
def test_unavailable_root_is_rejected(tmp_path: Path, kind: str) -> None:
    root = tmp_path / "root"
    if kind == "file":
        root.write_bytes(b"not a directory")
    with pytest.raises(ValueError):
        model.admit_model(root)
