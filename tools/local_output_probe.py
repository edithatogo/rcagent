"""Observe fixed synthetic output grammar; never admit or normalise a study."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import platform
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

from tools import darwin_runtime_profile, local_model_comparator, prospective_model
from tools import darwin_runtime_v030 as profile
from tools.local_model_comparator import _sha256
from tools.prospective_model import admit_model

PROMPT = "This is a synthetic software capability probe. Reply with the word READY."
TIMEOUT = 60
MAX_OUTPUT = 1024 * 1024


def source_pins() -> dict[str, str]:
    paths = [Path(__file__)]
    for module in (profile, darwin_runtime_profile, prospective_model, local_model_comparator):
        name = module.__file__
        if not isinstance(name, str):
            raise ValueError("source_file_unavailable")
        paths.append(Path(name))
    return {path.name: _sha256(path) for path in paths}


def run_probe(model_root: Path) -> dict:
    receipt: dict = {
        "schema_version": "1.0",
        "purpose": "output-mode-probe-only",
        "admitted": False,
        "study_unlocked": False,
        "execution_observed": False,
        "response_only_verified": False,
    }
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        return {**receipt, "status": "unsupported_platform"}
    try:
        admission = admit_model(model_root)
        sources = source_pins()
        profile_pin = profile.profile_digest()
        environment = profile.profile_environment()
    except (ValueError, OSError):
        return {**receipt, "status": "admission_failed"}
    args = [
        profile.EXECUTABLE,
        "-m",
        admission["model_path"],
        "-p",
        PROMPT,
        "-n",
        "16",
        "-c",
        "512",
        "--seed",
        "42",
        "--temp",
        "0",
        "--offline",
        "--single-turn",
        "--simple-io",
        "--no-display-prompt",
        "--no-show-timings",
        "--color",
        "off",
        "--log-colors",
        "off",
        "--log-disable",
        "--no-warmup",
        "--no-escape",
    ]
    start = datetime.now(UTC).isoformat()
    clock = time.monotonic_ns()
    exit_state: int | str
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            process = subprocess.run(
                args,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                env=environment,
                timeout=TIMEOUT,
                check=False,
            )
            exit_state = process.returncode
            receipt["execution_observed"] = True
        except subprocess.TimeoutExpired:
            exit_state = "timeout"
            receipt["execution_observed"] = True
        except OSError:
            exit_state = "launch_failed"
        elapsed = time.monotonic_ns() - clock
        finish = datetime.now(UTC).isoformat()
        sizes = [stream.seek(0, os.SEEK_END) for stream in (stdout, stderr)]
        stdout.seek(0)
        stderr.seek(0)
        out, err = stdout.read(MAX_OUTPUT + 1), stderr.read(MAX_OUTPUT + 1)
    complete = all(size <= MAX_OUTPUT for size in sizes)
    unchanged = False
    images: list[str] = []
    reason = "none"
    try:
        unchanged = (
            admit_model(model_root) == admission
            and source_pins() == sources
            and profile.profile_digest() == profile_pin
        )
        if not unchanged:
            raise ValueError("pins_changed")
        if exit_state != 0:
            raise ValueError("process_failed")
        if not complete:
            raise ValueError("output_limit_exceeded")
        if not out:
            raise ValueError("empty_output")
        images = profile.verify_loaded_images(err)
    except (ValueError, OSError) as exc:
        reason = (
            str(exc)
            if str(exc)
            in {
                "pins_changed",
                "process_failed",
                "output_limit_exceeded",
                "empty_output",
                "unexpected_loaded_image",
                "incomplete_loader_evidence",
                "malformed_loader_line",
                "invalid_loader_encoding",
                "invalid_loader_path",
            }
            else "post_execution_validation_failed"
        )
    receipt.update(
        {
            "status": "process_completed" if reason == "none" else "probe_failed",
            "reason": reason,
            "exit_state": exit_state,
            "started_at": start,
            "finished_at": finish,
            "elapsed_ns": elapsed,
            "model_admission": admission,
            "source_sha256": sources,
            "profile_sha256": profile_pin,
            "pins_unchanged_after": unchanged,
            "loaded_non_system_images": images,
            "prompt": PROMPT,
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "arguments": args,
            "arguments_without_local_paths": [
                "<pinned-runtime>",
                "-m",
                "<pinned-model>",
                *args[3:],
            ],
            "environment": environment,
            "timeout_seconds": TIMEOUT,
            "device": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": platform.python_version(),
            },
            "stdout_bytes": sizes[0],
            "stderr_bytes": sizes[1],
            "output_complete": complete,
            "raw_stdout_base64": base64.b64encode(out).decode() if complete else None,
            "raw_stderr_base64": base64.b64encode(err).decode() if complete else None,
            "stdout_sha256": hashlib.sha256(out).hexdigest() if complete else None,
            "stderr_sha256": hashlib.sha256(err).hexdigest() if complete else None,
            "limitations": [
                "not a study observation, admission or normalisation result",
                "suppression flags do not prove response-only output",
                "trusted process diagnostics, not tamper-proof provenance",
                "OS/driver bytes and unreported dynamic loads are not attested",
                "no atomic protection against concurrent replacement",
                "network egress is not independently monitored or sandboxed",
                "temporary output storage is not a disk quota",
                "raw local paths may appear; inspect before publication",
            ],
        }
    )
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args(argv)
    destination = args.receipt.absolute()
    try:
        if any(path.is_symlink() for path in (destination, *destination.parents)):
            raise ValueError("symlink_destination")
        # Exclusive reservation precedes all model checks and process launches.
        with destination.open("xb") as stream:
            result = run_probe(args.model_root)
            data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
            stream.write(data)
    except (ValueError, OSError):
        print(json.dumps({"status": "receipt_unavailable", "study_unlocked": False}))
        return 1
    print(
        json.dumps(
            {
                "status": result["status"],
                "receipt_sha256": hashlib.sha256(data).hexdigest(),
                "study_unlocked": False,
            }
        )
    )
    return 0 if result["status"] == "process_completed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
