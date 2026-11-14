"""Capture one fixed local capability probe; never admit a study observation."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import platform
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, NotRequired, TypeAlias, TypedDict, TypeGuard

from tools import darwin_runtime_profile as profile
from tools import json_shapes
from tools.local_model_comparator import MANIFEST_PATH, _sha256, validate_admission

REGISTRY_PIN = "6921d6ff0df9e41c28c59ca077c5c2ae0b84835822cb0d5d7e12eeca1d4485a5"
MODEL_ID = "qwen2.5-0.5b-instruct-q4_k_m"
PROMPT = "This is a synthetic software capability probe. Reply with the word READY."
TIMEOUT = 60
MAX_OUTPUT = 65536


class ProbeRuntime(TypedDict):
    executable: str
    executable_sha256: str
    version: str


class ProbeModelFile(TypedDict):
    path: str
    sha256: str


class ProbeModel(TypedDict):
    id: str
    revision: str
    cache_subdirectory: str
    files: list[ProbeModelFile]


class ProbeManifest(TypedDict):
    runtime: ProbeRuntime
    models: list[ProbeModel]


class DeviceInfo(TypedDict):
    system: str
    release: str
    machine: str
    python: str


class DependencyProfile(TypedDict):
    status: Literal["observed", "failed"]
    profile_sha256: str
    adapter_sha256: str
    loaded_non_system_images: list[str]
    environment: dict[str, str]
    raw_stderr_base64: str | None
    limitations: list[str]


class ProbeBase(TypedDict):
    schema_version: Literal["1.0"]
    purpose: Literal["capability-probe-only"]
    study_unlocked: Literal[False]
    admitted: Literal[False]
    execution_observed: bool


class AdmissionFailure(ProbeBase):
    status: Literal["admission_failed"]


class CapturedProbe(ProbeBase):
    status: Literal["process_completed", "probe_failed"]
    exit_state: int | Literal["timeout", "launch_failed"]
    started_at: str
    finished_at: str
    elapsed_ns: int
    pins_unchanged_after: bool
    registry_sha256: str
    adapter_sha256: str
    runtime_sha256: str
    runtime_version: str
    model_id: str
    quantisation: Literal["Q4_K_M"]
    device: DeviceInfo
    model_revision: str
    model_sha256: str
    prompt: str
    prompt_sha256: str
    arguments_without_local_paths: list[str]
    timeout_seconds: int
    environment_keys: list[str]
    stdout_bytes: int
    stderr_bytes: int
    output_complete: bool
    stdout_base64: str | None
    stdout_sha256: str | None
    stderr_sha256: str | None
    network: str
    limitations: list[str]
    dependency_profile: NotRequired[DependencyProfile]


ProbeResult: TypeAlias = AdmissionFailure | CapturedProbe


def _is_runtime(value: object) -> TypeGuard[ProbeRuntime]:
    return json_shapes.is_object(value) and all(
        isinstance(value.get(key), str) for key in ("executable", "executable_sha256", "version")
    )


def _is_model_file(value: object) -> TypeGuard[ProbeModelFile]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("path"), str)
        and isinstance(value.get("sha256"), str)
    )


def _is_model(value: object) -> TypeGuard[ProbeModel]:
    if not json_shapes.is_object(value) or not all(
        isinstance(value.get(key), str) for key in ("id", "revision", "cache_subdirectory")
    ):
        return False
    files = value.get("files")
    return json_shapes.is_array(files) and bool(files) and all(_is_model_file(f) for f in files)


def _is_manifest(value: object) -> TypeGuard[ProbeManifest]:
    if not json_shapes.is_object(value) or not _is_runtime(value.get("runtime")):
        return False
    models = value.get("models")
    return json_shapes.is_array(models) and all(_is_model(model) for model in models)


def _admission(
    model_root: Path, runtime_path: Path | None
) -> tuple[ProbeManifest, ProbeModel, Path]:
    data = MANIFEST_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != REGISTRY_PIN:
        raise ValueError("registry_pin_mismatch")
    parsed: object = copy.deepcopy(json.loads(data))
    manifest = json_shapes.require_object(parsed, context="probe manifest")
    if runtime_path is not None:
        # A relocated executable is allowed only when its admitted hash still matches.
        runtime = json_shapes.require_object(manifest["runtime"], context="probe runtime")
        runtime["executable"] = str(runtime_path.resolve(strict=True))
    if validate_admission(manifest, model_root):
        raise ValueError("admission_failed")
    if not _is_manifest(manifest):
        raise ValueError("invalid_admitted_manifest")
    model = next((item for item in manifest["models"] if item["id"] == MODEL_ID), None)
    if model is None:
        raise ValueError("selected_model_missing")
    model_path = model_root / model["cache_subdirectory"] / model["files"][0]["path"]
    return manifest, model, model_path


def run_probe(
    model_root: Path, runtime_path: Path | None = None, *, dependency_profile: bool = False
) -> ProbeResult:
    receipt: ProbeBase = {
        "schema_version": "1.0",
        "purpose": "capability-probe-only",
        "study_unlocked": False,
        "admitted": False,
        "execution_observed": False,
    }
    profile_pin = profile_adapter_pin = ""
    environment = {"PATH": os.defpath, "LANG": "C"}
    output_limit = MAX_OUTPUT
    try:
        manifest, model, model_path = _admission(model_root, runtime_path)
        if dependency_profile:
            if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
                raise ValueError("unsupported_profile_platform")
            if Path(manifest["runtime"]["executable"]).resolve() != Path(profile.EXECUTABLE):
                raise ValueError("profile_executable_mismatch")
            profile.verify_files()
            profile_pin = profile.profile_digest()
            profile_adapter_pin = _sha256(Path(profile.__file__))
            environment = profile.profile_environment()
            output_limit = profile.MAX_OUTPUT
    except (ValueError, OSError):
        return {**receipt, "status": "admission_failed"}
    executable = Path(manifest["runtime"]["executable"])
    adapter_pin = _sha256(Path(__file__))
    args = [
        str(executable),
        "-m",
        str(model_path),
        "-p",
        PROMPT,
        "-n",
        "16",
        "--seed",
        "42",
        "--temp",
        "0",
        "--no-display-prompt",
        "--log-disable",
        "--single-turn",
    ]
    start_utc = datetime.now(UTC).isoformat()
    start_ns = time.monotonic_ns()
    exit_state: int | Literal["timeout", "launch_failed"]
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            completed = subprocess.run(  # nosec B603 # admitted executable/model and fixed synthetic argv; no shell
                args,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                env=environment,
                timeout=TIMEOUT,
                check=False,
            )
            exit_state = completed.returncode
            receipt["execution_observed"] = True
        except subprocess.TimeoutExpired:
            exit_state = "timeout"
            receipt["execution_observed"] = True
        except OSError:
            exit_state = "launch_failed"
        elapsed_ns = time.monotonic_ns() - start_ns
        end_utc = datetime.now(UTC).isoformat()
        sizes = [stream.seek(0, os.SEEK_END) for stream in (stdout, stderr)]
        stdout.seek(0)
        stderr.seek(0)
        out, err = stdout.read(output_limit + 1), stderr.read(output_limit + 1)
    oversized = any(size > output_limit for size in sizes)
    loaded: list[str] = []
    try:
        unchanged = (
            _sha256(executable) == manifest["runtime"]["executable_sha256"]
            and _sha256(model_path) == model["files"][0]["sha256"]
            and _sha256(MANIFEST_PATH) == REGISTRY_PIN
            and _sha256(Path(__file__)) == adapter_pin
        )
        if dependency_profile:
            profile.verify_files()
            unchanged = (
                unchanged
                and profile.profile_digest() == profile_pin
                and _sha256(Path(profile.__file__)) == profile_adapter_pin
            )
            if not oversized:
                loaded = profile.verify_loaded_images(err)
    except (OSError, ValueError):
        unchanged = False
    status: Literal["process_completed", "probe_failed"] = (
        "process_completed"
        if exit_state == 0 and out and not oversized and unchanged
        else "probe_failed"
    )
    # Oversized streams are not represented as complete evidence by a prefix hash.
    captured: CapturedProbe = {
        **receipt,
        "status": status,
        "exit_state": exit_state,
        "started_at": start_utc,
        "finished_at": end_utc,
        "elapsed_ns": elapsed_ns,
        "pins_unchanged_after": unchanged,
        "registry_sha256": REGISTRY_PIN,
        "adapter_sha256": adapter_pin,
        "runtime_sha256": manifest["runtime"]["executable_sha256"],
        "runtime_version": manifest["runtime"]["version"],
        "model_id": model["id"],
        "quantisation": "Q4_K_M",
        "device": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "model_revision": model["revision"],
        "model_sha256": model["files"][0]["sha256"],
        "prompt": PROMPT,
        "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
        "arguments_without_local_paths": [
            "<pinned-runtime>",
            "-m",
            "<pinned-model>",
            *args[3:],
        ],
        "timeout_seconds": TIMEOUT,
        "environment_keys": sorted(environment),
        "stdout_bytes": sizes[0],
        "stderr_bytes": sizes[1],
        "output_complete": not oversized,
        "stdout_base64": None if oversized else base64.b64encode(out).decode("ascii"),
        "stdout_sha256": None if oversized else hashlib.sha256(out).hexdigest(),
        "stderr_sha256": None if oversized else hashlib.sha256(err).hexdigest(),
        "network": "local-file arguments; egress not independently monitored or sandboxed",
        "limitations": [
            "not a study observation",
            "no semantic correctness or model suitability claim",
            "shared libraries and OS not hash-attested",
            "not tamper-proof provenance",
            "stderr bytes not published",
            "temporary output storage is not a disk quota",
        ],
    }
    if dependency_profile:
        captured["dependency_profile"] = {
            "status": "observed" if status == "process_completed" else "failed",
            "profile_sha256": profile_pin,
            "adapter_sha256": profile_adapter_pin,
            "loaded_non_system_images": loaded,
            "environment": environment,
            "raw_stderr_base64": None if oversized else base64.b64encode(err).decode("ascii"),
            "limitations": [
                "trusted process loader reports, not tamper-proof attestation",
                "OS/driver bytes and unreported dynamic loads are outside this profile",
                "no atomic protection against concurrent filesystem replacement",
            ],
        }
        captured["limitations"] = [
            item
            for item in captured["limitations"]
            if item
            not in {"shared libraries and OS not hash-attested", "stderr bytes not published"}
        ] + [
            "observed non-system libraries checked; OS and drivers not hash-attested",
            "raw loader diagnostics retained locally; inspect before any publication",
        ]
    return captured


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--runtime-path", type=Path)
    parser.add_argument("--dependency-profile", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    if args.receipt and (args.receipt.exists() or args.receipt.is_symlink()):
        print(json.dumps({"status": "receipt_exists", "study_unlocked": False}))
        return 1
    result = run_probe(
        args.model_root, args.runtime_path, dependency_profile=args.dependency_profile
    )
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        try:
            with args.receipt.open("xb") as stream:
                stream.write(data.encode("utf-8"))
        except OSError:
            print(json.dumps({"status": "receipt_write_failed", "study_unlocked": False}))
            return 1
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "receipt_sha256": hashlib.sha256(data.encode()).hexdigest(),
                    "study_unlocked": False,
                }
            )
        )
    else:
        print(data, end="")
    return 0 if result["status"] == "process_completed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
