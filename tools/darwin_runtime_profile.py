"""Observe one pinned Darwin userland profile; never admit study evidence."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import platform
import re
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from tools.local_model_comparator import _sha256

EXECUTABLE = "/opt/homebrew/Cellar/llama.cpp/0.2.0/bin/llama-cli"
LIBRARY_DIRS = (
    "/opt/homebrew/Cellar/llama.cpp/0.2.0/lib",
    "/opt/homebrew/Cellar/ggml/0.21.0/lib",
    "/opt/homebrew/Cellar/libomp/22.1.8/lib",
    "/opt/homebrew/Cellar/openssl@3/3.6.3/lib",
)
PINNED_FILES = {
    EXECUTABLE: "456af2d481095b6a953b6ad21e9caa0411e5508955eb841f37574235da10a44e",
    f"{LIBRARY_DIRS[0]}/libllama-cli-impl.dylib": "da414fe802b897ddb37cf62d41a6f07f7eca67245c5a674f3b24675425ff6100",
    f"{LIBRARY_DIRS[0]}/libllama-server-impl.dylib": "0935f907c3dd5053d4426164b21409da8702da2ba873e8fbe69ee8d8f8672c09",
    f"{LIBRARY_DIRS[0]}/libmtmd.0.2.0.dylib": "7af25a040710843eba663f2c1a58f395e391e963d3c09380ca225b5cdf9cdbf8",
    f"{LIBRARY_DIRS[0]}/libllama-common.0.2.0.dylib": "8d9bf475e2d324b3c7407d243b3a2baa843afb9d4ec41e7ce7986db73ddb68e7",
    f"{LIBRARY_DIRS[0]}/libllama.0.2.0.dylib": "31104cdae6319f58f947abbfd0e1afb55671ba64a5b6fbf30f71eeb673e72242",
    f"{LIBRARY_DIRS[1]}/libggml.0.21.0.dylib": "c3d660fbd37d5bae33e68371d27aab78b9875ccb5676532d3f1cfe1cea6f8734",
    f"{LIBRARY_DIRS[1]}/libggml-base.0.21.0.dylib": "5d193ff57adff4912c686903b38a2802a716639d2240cebd4275faeee4d94574",
    f"{LIBRARY_DIRS[2]}/libomp.dylib": "b6d9b621ca10f9e097de32b77b1bd50ca0b6e606168a0d7368e82fd279dbfb4f",
    f"{LIBRARY_DIRS[3]}/libssl.3.dylib": "4c3c554adc8ace6ec2245b4962b181451d245edfab92c3a09fc7b3be094e7438",
    f"{LIBRARY_DIRS[3]}/libcrypto.3.dylib": "34bc039f5c725691e757ef42d26f1709830b18046c3ad6d93985153c83d0bbbc",
    "/opt/homebrew/Cellar/ggml/0.21.0/libexec/libggml-cpu-apple_m1.so": "11808ed60ba4982a0128469b226c9bbeafdc0f7812fcaea1e35a7c0a479d0b72",
    "/opt/homebrew/Cellar/ggml/0.21.0/libexec/libggml-cpu-apple_m2_m3.so": "66780f49ea1eca2b924d5c6caba37b0884779bec1a5688e7af2137ba42ffd993",
    "/opt/homebrew/Cellar/ggml/0.21.0/libexec/libggml-cpu-apple_m4.so": "0d1acc4b4d3ac89e0c2d21cc488f6f5ac66f94f7ebd862727b93b14922fb4100",
    "/opt/homebrew/Cellar/ggml/0.21.0/libexec/libggml-blas.so": "d71754ba60be01507dab9a3ffef6713a6906fe523c01487d0984c1038ec87eca",
    "/opt/homebrew/Cellar/ggml/0.21.0/libexec/libggml-metal.so": "6bd57fb72e52d48898e4bc399c7873eaffdcfef0d247423ff52824230f7f67d2",
}
REQUIRED_IMAGES = {path for path in PINNED_FILES if "/libexec/" not in path}
LOAD_ALIASES = {
    f"{LIBRARY_DIRS[0]}/libmtmd.0.dylib": f"{LIBRARY_DIRS[0]}/libmtmd.0.2.0.dylib",
    f"{LIBRARY_DIRS[0]}/libllama-common.0.dylib": f"{LIBRARY_DIRS[0]}/libllama-common.0.2.0.dylib",
    f"{LIBRARY_DIRS[0]}/libllama.0.dylib": f"{LIBRARY_DIRS[0]}/libllama.0.2.0.dylib",
    f"{LIBRARY_DIRS[1]}/libggml.0.dylib": f"{LIBRARY_DIRS[1]}/libggml.0.21.0.dylib",
    f"{LIBRARY_DIRS[1]}/libggml-base.0.dylib": f"{LIBRARY_DIRS[1]}/libggml-base.0.21.0.dylib",
}
VERSION_LINE = b"version: 0.2.0 (build 10566, commit bb4caa754)"
MAX_OUTPUT = 1024 * 1024
TIMEOUT = 60
IMAGE_LINE = re.compile(
    r"dyld\[([0-9]+)\]: <[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}> (/.+)"
)
DELAYED_LINE = re.compile(
    r"dyld\[([0-9]+)\]: move (?:delayed to loaded|loaded to delayed): ([A-Za-z0-9_.+-]+)"
)


def profile_digest() -> str:
    value = {
        "files": PINNED_FILES,
        "required": sorted(REQUIRED_IMAGES),
        "directories": LIBRARY_DIRS,
        "executable": EXECUTABLE,
        "aliases": LOAD_ALIASES,
    }
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify_files() -> None:
    """Check exact resolved local bytes, not arbitrary caller-selected artefacts."""
    # ggml discovers backends in libexec: extra files must fail before discovery.
    for directory in {Path(name).parent for name in PINNED_FILES if "/libexec/" in name}:
        try:
            if {str(entry) for entry in directory.iterdir()} != {
                name for name in PINNED_FILES if Path(name).parent == directory
            }:
                raise ValueError("profile_backend_inventory_mismatch")
        except OSError as exc:
            raise ValueError("profile_backend_directory_unavailable") from exc
    for alias, target in LOAD_ALIASES.items():
        try:
            if target not in PINNED_FILES or Path(alias).resolve(strict=True) != Path(target):
                raise ValueError("profile_alias_mismatch")
        except OSError as exc:
            raise ValueError("profile_alias_unavailable") from exc
    for name, digest in PINNED_FILES.items():
        path = Path(name)
        try:
            if path.resolve(strict=True) != path or not path.is_file():
                raise ValueError("profile_path_mismatch")
            if _sha256(path) != digest:
                raise ValueError("profile_hash_mismatch")
        except OSError as exc:
            raise ValueError("profile_file_unavailable") from exc


def profile_environment() -> dict[str, str]:
    return {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "DYLD_LIBRARY_PATH": ":".join(LIBRARY_DIRS),
        "DYLD_PRINT_LIBRARIES": "1",
    }


def verify_loaded_images(stderr: bytes) -> list[str]:
    """Validate reported userland images; OS shared-cache bytes are not attested."""
    try:
        lines = stderr.decode("utf-8", errors="strict").splitlines()
    except UnicodeError as exc:
        raise ValueError("invalid_loader_encoding") from exc
    images: set[str] = set()
    pids: set[str] = set()
    reported_names: set[str] = set()
    delayed_names: set[str] = set()
    for line in lines:
        if not line.startswith("dyld"):
            continue  # Runtime diagnostics are retained but are not loader evidence.
        match = IMAGE_LINE.fullmatch(line)
        if match is None:
            delayed = DELAYED_LINE.fullmatch(line)
            if delayed is None:
                raise ValueError("malformed_loader_line")
            pids.add(delayed[1])
            delayed_names.add(delayed[2])
            continue
        pids.add(match[1])
        name = match[2]
        path = PurePosixPath(name)
        if str(path) != name or ".." in path.parts or any(ord(c) < 32 for c in name):
            raise ValueError("invalid_loader_path")
        reported_names.add(path.name)
        if name.startswith(("/usr/lib/", "/System/Library/")):
            continue
        if name not in PINNED_FILES:
            raise ValueError("unexpected_loaded_image")
        images.add(name)
    if (
        len(pids) != 1
        or not REQUIRED_IMAGES.issubset(images)
        or not delayed_names.issubset(reported_names)
    ):
        raise ValueError("incomplete_loader_evidence")
    return sorted(images)


def capture_version() -> dict:
    receipt = {
        "schema_version": "1.0",
        "purpose": "runtime-profile-observation-only",
        "admitted": False,
        "study_unlocked": False,
        "execution_observed": False,
    }
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        return {**receipt, "status": "unsupported_platform"}
    try:
        verify_files()
        pin = profile_digest()
        adapter_pin = _sha256(Path(__file__))
    except (ValueError, OSError):
        return {**receipt, "status": "profile_failed", "reason": "profile_preflight_failed"}
    start = datetime.now(UTC).isoformat()
    clock = time.monotonic_ns()
    exit_state: int | str
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            result = subprocess.run(
                [EXECUTABLE, "--version"],
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                env=profile_environment(),
                timeout=TIMEOUT,
                check=False,
            )
            exit_state = result.returncode
            receipt["execution_observed"] = True
        except subprocess.TimeoutExpired:
            exit_state = "timeout"
            receipt["execution_observed"] = True
        except OSError:
            exit_state = "launch_failed"
        sizes = [stream.seek(0, os.SEEK_END) for stream in (stdout, stderr)]
        stdout.seek(0)
        stderr.seek(0)
        out, err = stdout.read(MAX_OUTPUT + 1), stderr.read(MAX_OUTPUT + 1)
    complete = all(size <= MAX_OUTPUT for size in sizes)
    images: list[str] = []
    reason = "none"
    unchanged = False
    try:
        verify_files()
        unchanged = pin == profile_digest() and adapter_pin == _sha256(Path(__file__))
        if not unchanged:
            raise ValueError("profile_changed")
        if exit_state != 0:
            raise ValueError("process_failed")
        if not complete:
            raise ValueError("output_limit_exceeded")
        if VERSION_LINE not in out + err:
            raise ValueError("version_mismatch")
        images = verify_loaded_images(err)
    except (ValueError, OSError) as exc:
        reason = str(exc) if isinstance(exc, ValueError) else "profile_file_unavailable"
    receipt.update(
        {
            "status": "runtime_profile_observed" if reason == "none" else "profile_failed",
            "reason": reason,
            "exit_state": exit_state,
            "started_at": start,
            "finished_at": datetime.now(UTC).isoformat(),
            "elapsed_ns": time.monotonic_ns() - clock,
            "profile_sha256": pin,
            "adapter_sha256": adapter_pin,
            "pins_unchanged_after": unchanged,
            "loaded_non_system_images": images,
            "environment": profile_environment(),
            "arguments": [EXECUTABLE, "--version"],
            "device": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
            },
            "stdout_bytes": sizes[0],
            "stderr_bytes": sizes[1],
            "output_complete": complete,
            "raw_stdout_base64": base64.b64encode(out).decode() if complete else None,
            "raw_stderr_base64": base64.b64encode(err).decode() if complete else None,
            "stdout_sha256": hashlib.sha256(out).hexdigest() if complete else None,
            "stderr_sha256": hashlib.sha256(err).hexdigest() if complete else None,
            "limitations": [
                "not a study observation or model-inference compatibility test",
                "OS shared cache and driver bytes are not hash-attested",
                "loader reports are trusted process diagnostics, not tamper-proof attestation",
                "no protection against concurrent replacement or unreported dynamic loads",
                "network egress not independently monitored or sandboxed",
                "temporary output storage is not a disk quota",
                "OpenSSL package 3.6.3 revision 0 bottle rebuild 1; historical label differs",
            ],
        }
    )
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.receipt.exists() or args.receipt.is_symlink():
        print(json.dumps({"status": "receipt_exists", "study_unlocked": False}))
        return 1
    result = capture_version()
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
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
    return 0 if result["status"] == "runtime_profile_observed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
