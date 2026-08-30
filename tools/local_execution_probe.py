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

from tools import darwin_runtime_profile as profile
from tools.local_model_comparator import MANIFEST_PATH, _sha256, validate_admission

REGISTRY_PIN = "6921d6ff0df9e41c28c59ca077c5c2ae0b84835822cb0d5d7e12eeca1d4485a5"
MODEL_ID = "qwen2.5-0.5b-instruct-q4_k_m"
PROMPT = "This is a synthetic software capability probe. Reply with the word READY."
TIMEOUT = 60
MAX_OUTPUT = 65536


def _admission(model_root: Path, runtime_path: Path | None) -> tuple[dict, dict, Path]:
    data = MANIFEST_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != REGISTRY_PIN:
        raise ValueError("registry_pin_mismatch")
    manifest = copy.deepcopy(json.loads(data))
    if runtime_path is not None:
        # A relocated executable is allowed only when its admitted hash still matches.
        manifest["runtime"]["executable"] = str(runtime_path.resolve(strict=True))
    if validate_admission(manifest, model_root):
        raise ValueError("admission_failed")
    model = next(item for item in manifest["models"] if item["id"] == MODEL_ID)
    model_path = model_root / model["cache_subdirectory"] / model["files"][0]["path"]
    return manifest, model, model_path


def run_probe(
    model_root: Path, runtime_path: Path | None = None, *, dependency_profile: bool = False
) -> dict:
    receipt = {
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
    exit_state: int | str
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            completed = subprocess.run(
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
    status = (
        "process_completed"
        if exit_state == 0 and out and not oversized and unchanged
        else "probe_failed"
    )
    # Oversized streams are not represented as complete evidence by a prefix hash.
    receipt.update(
        {
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
    )
    if dependency_profile:
        receipt["dependency_profile"] = {
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
        receipt["limitations"] = [
            item
            for item in receipt["limitations"]
            if item
            not in {"shared libraries and OS not hash-attested", "stderr bytes not published"}
        ] + [
            "observed non-system libraries checked; OS and drivers not hash-attested",
            "raw loader diagnostics retained locally; inspect before any publication",
        ]
    return receipt


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
