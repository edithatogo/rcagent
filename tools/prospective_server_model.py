"""Read-only local model eligibility for the separate pinned server profile.

Reuse existing model/rights checks without modifying the historical registry or
CLI helper. This receipt does not freeze source code, launch or admit a study.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import darwin_server_v030 as profile
from tools.local_model_comparator import MANIFEST_PATH, _admitted_file, _sha256, validate_admission
from tools.prospective_model import MODEL_ID, REGISTRY_PIN, digest


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


def admit_model(model_root: Path) -> dict:
    """Require original model classes and a stable explicit server identity."""
    try:
        root = _root(model_root)
        root_identity = (root.stat().st_dev, root.stat().st_ino)
        if _sha256(MANIFEST_PATH) != REGISTRY_PIN:
            raise ValueError("registry_pin_mismatch")
        raw = MANIFEST_PATH.read_bytes()
        manifest = json.loads(raw)
        # Recheck the bytes actually parsed, not only the preceding file read.
        if hashlib.sha256(raw).hexdigest() != REGISTRY_PIN:
            raise ValueError("registry_changed_during_admission")
        original_runtime = manifest["runtime"]
        profile_pin = profile.profile_digest()
        profile_id = profile.PROFILE_ID
        profile.verify_files()
        overlay = {
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
        selected = next((item for item in manifest["models"] if item["id"] == MODEL_ID), None)
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
        result = {
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
        return {**result, "admission_sha256": digest(result)}
    except OSError as exc:
        raise ValueError("server_model_admission_file_unavailable") from exc
