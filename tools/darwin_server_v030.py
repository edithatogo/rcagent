"""Pinned llama-server profile and non-study version/help diagnostics.

Reuse the reviewed runtime verifier and component evidence without mutating the
CLI profile. Source pins bind imported configuration and verifier code. Hashes
are byte identity, not legal clearance or tamper-proof execution attestation.
No serving transport or study admission is enabled by this entrypoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from tools import darwin_runtime_profile as core
from tools import darwin_runtime_v030 as cli

PROFILE_ID = "darwin-llama-server-0.3.0-typing-20261114"
EXECUTABLE = "/opt/homebrew/Cellar/llama.cpp/0.3.0/bin/llama-server"
LIBRARY_DIRS = tuple(cli.LIBRARY_DIRS)
VERSION_LINE = cli.VERSION_LINE
VERSION_MARKERS = tuple(cli.VERSION_MARKERS)
PINNED_FILES = {
    name: digest
    for name, digest in cli.PINNED_FILES.items()
    if name != cli.EXECUTABLE and not name.endswith("/libllama-cli-impl.dylib")
}
PINNED_FILES[EXECUTABLE] = "07c17ec087076d582147208beadba5cbe534ae6e5015658e6f4c96d9457232f6"
REQUIRED_IMAGES = {name for name in PINNED_FILES if "/libexec/" not in name}
LOAD_ALIASES = dict(cli.LOAD_ALIASES)
EVIDENCE_FILES = dict(cli.EVIDENCE_FILES)
SOURCE_ROOT = Path(__file__).resolve().parent
SOURCE_FILES = {
    "darwin_runtime_profile.py": "31f0627bd3386a164872f1c14640e14b26a5551b7f61c6c23795ce2427a5c3ee",
    "darwin_runtime_v030.py": "2f9d42e8522d376401188c89e6a4d55692cd145985506b88e31e26c31f26de8d",
    "local_model_comparator.py": "f27bf6dcf890887bf30112982ba78843828d58ce00b8a1b3481f23a1c2a49074",
    "json_shapes.py": "85d1b47e29a4dc26c6af02560692a7a323a1e31ec54158a709a1f3a7fb0946e5",
}


def profile_digest() -> str:
    value = {
        "profile_id": PROFILE_ID,
        "runtime": core.profile_digest(sys.modules[__name__]),
        "evidence": EVIDENCE_FILES,
        "sources": SOURCE_FILES,
        "version": VERSION_LINE.hex(),
        "markers": [marker.hex() for marker in VERSION_MARKERS],
    }
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify_files() -> None:
    """Require source/evidence bytes before delegating runtime-file checks."""
    records = {
        **{str(SOURCE_ROOT / name): digest for name, digest in SOURCE_FILES.items()},
        **EVIDENCE_FILES,
    }
    for name, digest in records.items():
        path = Path(name)
        try:
            if path.resolve(strict=True) != path or not path.is_file():
                raise ValueError("server_profile_evidence_path_mismatch")
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("server_profile_evidence_digest_mismatch")
        except OSError as exc:
            raise ValueError("server_profile_evidence_unavailable") from exc
    core.verify_files(sys.modules[__name__])


def profile_environment() -> dict[str, str]:
    return core.profile_environment(sys.modules[__name__])


def verify_loaded_images(stderr: bytes) -> list[str]:
    return core.verify_loaded_images(stderr, sys.modules[__name__])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--diagnostic", choices=("version", "help"), default="version")
    args = parser.parse_args(argv)
    destination = args.receipt.absolute()
    try:
        if ".." in args.receipt.parts:
            raise ValueError("noncanonical_destination")
        if any(path.is_symlink() for path in (destination, *destination.parents)):
            raise ValueError("symlink_destination")
        if destination.parent.resolve(strict=True) != destination.parent:
            raise ValueError("noncanonical_parent")
        # Reserve exclusive local evidence storage before any runtime launch.
        with destination.open("xb") as stream:
            result = core.capture_version(sys.modules[__name__], diagnostic=args.diagnostic)
            data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
            stream.write(data)
    except (ValueError, OSError):
        print(
            json.dumps(
                {"status": "receipt_unavailable", "study_unlocked": False, "admitted": False}
            )
        )
        return 1
    print(
        json.dumps(
            {
                "status": result["status"],
                "receipt_sha256": hashlib.sha256(data).hexdigest(),
                "study_unlocked": False,
                "admitted": False,
            }
        )
    )
    return 0 if result["status"] == "runtime_profile_observed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
