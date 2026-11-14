"""Explicit runtime overlay for existing local model rights checks, not study admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools import darwin_runtime_v030 as profile
from tools import json_shapes
from tools.local_model_comparator import MANIFEST_PATH, _admitted_file, _sha256, validate_admission

REGISTRY_PIN = "6921d6ff0df9e41c28c59ca077c5c2ae0b84835822cb0d5d7e12eeca1d4485a5"
MODEL_ID = "qwen2.5-0.5b-instruct-q4_k_m"


class CLIRuntimeOverlay(TypedDict):
    name: str
    version: str
    executable: str
    executable_sha256: str
    license: str
    distribution: str
    runtime_dependencies: list[str]


class _CLIAdmissionFields(TypedDict):
    purpose: Literal["local-artefact-eligibility-only"]
    local_artifact_eligible: Literal[True]
    admitted: Literal[False]
    study_unlocked: Literal[False]
    registry_sha256: str
    effective_manifest_sha256: str
    original_runtime: json_shapes.JsonObject
    runtime_overlay: CLIRuntimeOverlay
    model_id: str
    model_revision: str
    model_sha256: str
    model_license_sha256: str
    model_path: str
    model_license_path: str


class CLIModelAdmission(_CLIAdmissionFields):
    admission_sha256: str


class _ManifestFile(TypedDict):
    path: str
    sha256: str


class _ManifestModel(TypedDict):
    id: str
    cache_subdirectory: str
    revision: str
    license_sha256: str
    files: list[_ManifestFile]


def _is_manifest_file(value: object) -> TypeGuard[_ManifestFile]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("path"), str)
        and isinstance(value.get("sha256"), str)
    )


def _is_manifest_model(value: object) -> TypeGuard[_ManifestModel]:
    if not json_shapes.is_object(value) or not all(
        isinstance(value.get(key), str)
        for key in ("id", "cache_subdirectory", "revision", "license_sha256")
    ):
        return False
    files = value.get("files")
    return json_shapes.is_array(files) and bool(files) and all(_is_manifest_file(f) for f in files)


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def admit_model(model_root: Path) -> CLIModelAdmission:
    """Verify all original model classes; bind a separate, explicit runtime identity.

    This is local artefact eligibility, never a study-condition admission or a
    guarantee against concurrent file replacement. Nothing is written to disk.
    """
    try:
        root = model_root.absolute()
        if root.resolve(strict=True) != root or not root.is_dir():
            raise ValueError("model_root_not_canonical")
        raw = MANIFEST_PATH.read_bytes()
        if hashlib.sha256(raw).hexdigest() != REGISTRY_PIN:
            raise ValueError("registry_pin_mismatch")
        parsed: object = json.loads(raw)
        manifest = json_shapes.require_object(parsed, context="model manifest")
        original_runtime = manifest["runtime"]
        profile.verify_files()
        overlay: CLIRuntimeOverlay = {
            "name": "llama.cpp llama-cli",
            "version": "0.3.0 build 10621 commit c1d0e7a00",
            "executable": profile.EXECUTABLE,
            "executable_sha256": profile.PINNED_FILES[profile.EXECUTABLE],
            "license": "MIT",
            "distribution": f"Homebrew installed bytes; explicit {profile.PROFILE_ID} profile",
            "runtime_dependencies": [
                "ggml 0.22.0",
                "libomp 23.1.0",
                "openssl@3 3.6.3 bottle rebuild 2",
            ],
        }
        manifest["runtime"] = overlay
        if validate_admission(manifest, root):
            raise ValueError("model_or_runtime_admission_failed")
        profile.verify_files()
        if _sha256(MANIFEST_PATH) != REGISTRY_PIN:
            raise ValueError("registry_changed_during_admission")
        rows = manifest["models"]
        if not json_shapes.is_array(rows):
            raise ValueError("invalid_validated_model_shape")
        models: list[_ManifestModel] = []
        for item in rows:
            if not _is_manifest_model(item):
                raise ValueError("invalid_validated_model_shape")
            models.append(item)
        selected = next((item for item in models if item["id"] == MODEL_ID), None)
        if selected is None:
            raise ValueError("selected_model_missing")
        directory = root / selected["cache_subdirectory"]
        model_path = _admitted_file(directory, selected["files"][0]["path"])
        licence_path = _admitted_file(directory, "LICENSE")
        if model_path is None or licence_path is None:
            raise ValueError("selected_model_files_unavailable")
        if (
            _sha256(model_path) != selected["files"][0]["sha256"]
            or _sha256(licence_path) != selected["license_sha256"]
        ):
            raise ValueError("selected_model_files_changed")
        result: _CLIAdmissionFields = {
            "purpose": "local-artefact-eligibility-only",
            "local_artifact_eligible": True,
            "admitted": False,
            "study_unlocked": False,
            "registry_sha256": REGISTRY_PIN,
            "effective_manifest_sha256": digest(manifest),
            "original_runtime": json_shapes.require_object(
                original_runtime, context="original runtime metadata"
            ),
            "runtime_overlay": overlay,
            "model_id": MODEL_ID,
            "model_revision": selected["revision"],
            "model_sha256": selected["files"][0]["sha256"],
            "model_license_sha256": selected["license_sha256"],
            "model_path": str(model_path),
            "model_license_path": str(licence_path),
        }
        return {**result, "admission_sha256": digest(result)}
    except OSError as exc:
        raise ValueError("model_admission_file_unavailable") from exc
