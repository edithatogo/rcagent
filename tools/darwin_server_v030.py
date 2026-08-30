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

PROFILE_ID = "darwin-llama-server-0.3.0-20260830"
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
    "darwin_runtime_profile.py": "c910b867fa1bb71c397fd466fe0f57931cfe1894f2b49a5752befb4d3b854998",
    "darwin_runtime_v030.py": "d84755db8d098393887e0fca0e67ef4d5d76bdfcacdda2a229d3138fe2605f37",
    "local_model_comparator.py": "429ae531533c5a90f618c3eb2f4d8f04c745c06ebf993159603710cefd25b090",
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
