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


def run_probe(model_root: Path, runtime_path: Path | None = None) -> dict:
    receipt = {
        "schema_version": "1.0",
        "purpose": "capability-probe-only",
        "study_unlocked": False,
        "admitted": False,
        "execution_observed": False,
    }
    try:
        manifest, model, model_path = _admission(model_root, runtime_path)
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
                env={"PATH": os.defpath, "LANG": "C"},
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
        out, err = stdout.read(MAX_OUTPUT + 1), stderr.read(MAX_OUTPUT + 1)
    oversized = any(size > MAX_OUTPUT for size in sizes)
    try:
        unchanged = (
            _sha256(executable) == manifest["runtime"]["executable_sha256"]
            and _sha256(model_path) == model["files"][0]["sha256"]
            and _sha256(MANIFEST_PATH) == REGISTRY_PIN
            and _sha256(Path(__file__)) == adapter_pin
        )
    except OSError:
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
            "environment_keys": ["LANG", "PATH"],
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
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--runtime-path", type=Path)
    args = parser.parse_args(argv)
    result = run_probe(args.model_root, args.runtime_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "process_completed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
