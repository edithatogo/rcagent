"""Read-only local model eligibility for the separate pinned server profile.

Reuse existing model/rights checks without modifying the historical registry or
CLI helper. This receipt does not freeze source code, launch or admit a study.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools import darwin_server_v030 as profile
from tools import json_shapes
from tools.local_model_comparator import MANIFEST_PATH, _admitted_file, _sha256, validate_admission
from tools.prospective_model import MODEL_ID, REGISTRY_PIN, digest


class RuntimeOverlay(TypedDict):
    name: str
    version: str
    executable: str
    executable_sha256: str
    license: str
    profile_id: str
    profile_sha256: str
    distribution: str
    runtime_dependencies: list[str]


class _AdmissionFields(TypedDict):
    purpose: Literal["local-artefact-eligibility-only"]
    local_artifact_eligible: Literal[True]
    admitted: Literal[False]
    study_unlocked: Literal[False]
    registry_sha256: str
    effective_manifest_sha256: str
    original_runtime: json_shapes.JsonObject
    runtime_overlay: RuntimeOverlay
    profile_id: str
    profile_sha256: str
    model_id: str
    model_revision: str
    model_sha256: str
    model_license_sha256: str
    model_path: str
    model_license_path: str
    limitations: list[str]


class ModelAdmission(_AdmissionFields):
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


def _strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _is_overlay(value: object) -> TypeGuard[RuntimeOverlay]:
    return (
        json_shapes.is_object(value)
        and all(
            isinstance(value.get(key), str)
            for key in (
                "name",
                "version",
                "executable",
                "executable_sha256",
                "license",
                "profile_id",
                "profile_sha256",
                "distribution",
            )
        )
        and _strings(value.get("runtime_dependencies"))
    )


def is_model_admission(value: object) -> TypeGuard[ModelAdmission]:
    """Check the receipt's structural types, without re-attesting its artefacts."""
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("purpose"), str)
        and value.get("purpose") == "local-artefact-eligibility-only"
        and value.get("local_artifact_eligible") is True
        and value.get("admitted") is False
        and value.get("study_unlocked") is False
        and all(
            isinstance(value.get(key), str)
            for key in (
                "registry_sha256",
                "effective_manifest_sha256",
                "profile_id",
                "profile_sha256",
                "model_id",
                "model_revision",
                "model_sha256",
                "model_license_sha256",
                "model_path",
                "model_license_path",
                "admission_sha256",
            )
        )
        and json_shapes.is_object(value.get("original_runtime"))
        and _is_overlay(value.get("runtime_overlay"))
        and _strings(value.get("limitations"))
    )


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


def _root(model_root: Path) -> Path:
    if ".." in model_root.parts:
        raise ValueError("model_root_not_canonical")
    root = model_root.absolute()
    if (
        any(path.is_symlink() for path in (root, *root.parents))
        or root.resolve(strict=True) != root
        or not root.is_dir()
    ):
        raise ValueError("model_root_not_canonical")
    return root


def admit_model(model_root: Path) -> ModelAdmission:
    """Require original model classes and a stable explicit server identity."""
    try:
        root = _root(model_root)
        root_identity = (root.stat().st_dev, root.stat().st_ino)
        if _sha256(MANIFEST_PATH) != REGISTRY_PIN:
            raise ValueError("registry_pin_mismatch")
        raw = MANIFEST_PATH.read_bytes()
        parsed: object = json.loads(raw)
        # Recheck the bytes actually parsed, not only the preceding file read.
        if hashlib.sha256(raw).hexdigest() != REGISTRY_PIN:
            raise ValueError("registry_changed_during_admission")
        manifest = json_shapes.require_object(parsed, context="model manifest")
        original_runtime = json_shapes.require_object(
            manifest["runtime"], context="original runtime metadata"
        )
        profile_pin = profile.profile_digest()
        profile_id = profile.PROFILE_ID
        profile.verify_files()
        overlay: RuntimeOverlay = {
            "name": "llama.cpp llama-server",
            "version": "0.3.0 build 10621 commit c1d0e7a00",
            "executable": profile.EXECUTABLE,
            "executable_sha256": profile.PINNED_FILES[profile.EXECUTABLE],
            "license": "MIT",
            "profile_id": profile_id,
            "profile_sha256": profile_pin,
            "distribution": "Homebrew installed bytes; separate pinned server profile",
            "runtime_dependencies": [
                "ggml 0.22.0",
                "libomp 23.1.0",
                "openssl@3 3.6.3 bottle rebuild 2",
            ],
        }
        manifest["runtime"] = overlay
        if validate_admission(manifest, root):
            raise ValueError("model_or_runtime_admission_failed")
        # Repeat all original class checks, not only the selected small model.
        if validate_admission(manifest, root):
            raise ValueError("model_or_runtime_changed_during_admission")
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
        profile.verify_files()
        if profile.profile_digest() != profile_pin or profile_id != profile.PROFILE_ID:
            raise ValueError("server_profile_changed_during_admission")
        if _sha256(MANIFEST_PATH) != REGISTRY_PIN:
            raise ValueError("registry_changed_during_admission")
        if _root(model_root) != root or (root.stat().st_dev, root.stat().st_ino) != root_identity:
            raise ValueError("model_root_changed_during_admission")
        result: _AdmissionFields = {
            "purpose": "local-artefact-eligibility-only",
            "local_artifact_eligible": True,
            "admitted": False,
            "study_unlocked": False,
            "registry_sha256": REGISTRY_PIN,
            "effective_manifest_sha256": digest(manifest),
            "original_runtime": original_runtime,
            "runtime_overlay": overlay,
            "profile_id": profile_id,
            "profile_sha256": profile_pin,
            "model_id": MODEL_ID,
            "model_revision": selected["revision"],
            "model_sha256": selected["files"][0]["sha256"],
            "model_license_sha256": selected["license_sha256"],
            "model_path": str(model_path),
            "model_license_path": str(licence_path),
            "limitations": [
                "read-only-local-eligibility",
                "not-atomic-file-attestation",
                "os-and-egress-not-attested",
                "execution-not-observed",
                "source-code-not-frozen",
                "not-study-admission",
            ],
        }
        return {**result, "admission_sha256": digest(dict(result))}
    except OSError as exc:
        raise ValueError("server_model_admission_file_unavailable") from exc
