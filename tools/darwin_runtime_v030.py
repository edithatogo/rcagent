"""Bounded local diagnostics for a distinct pinned llama.cpp 0.3.0 profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from tools import darwin_runtime_profile as core

PROFILE_ID = "darwin-llama-0.3.0-20260830"
EXECUTABLE = "/opt/homebrew/Cellar/llama.cpp/0.3.0/bin/llama-cli"
LIBRARY_DIRS = (
    "/opt/homebrew/Cellar/llama.cpp/0.3.0/lib",
    "/opt/homebrew/Cellar/ggml/0.22.0/lib",
    "/opt/homebrew/Cellar/libomp/23.1.0/lib",
    "/opt/homebrew/Cellar/openssl@3/3.6.3/lib",
)
VERSION_LINE = b"version: 0.3.0"
VERSION_MARKERS = (VERSION_LINE, b"commit c1d0e7a00)")
PINNED_FILES = {
    EXECUTABLE: "dd6208ade8be12c77c3342ff09b2b0963515c5b9083753f46fecbed364754618",
    f"{LIBRARY_DIRS[0]}/libllama-cli-impl.dylib": "1b6641e0bce599631fd056df5fbc5b7d550f411931d22fe0658c801382a110ea",
    f"{LIBRARY_DIRS[0]}/libllama-server-impl.dylib": "bd54b5a505851433eb12fe795f0d364e98c06c9eaf35630ef5733ac1a010b82c",
    f"{LIBRARY_DIRS[0]}/libllama-common.0.3.0.dylib": "61d19029a40835db05b8878a6ae93be5cc2f799c6c3de2d0345026ab99106c89",
    f"{LIBRARY_DIRS[0]}/libllama.0.3.0.dylib": "0f3a89c24da0e55a31a15064ac1565aab572d5ce0b2a1cd4b333676684061bda",
    f"{LIBRARY_DIRS[0]}/libmtmd.0.3.0.dylib": "5facb11477b7ae79586c7b2b7869f0d8924140d3714090ca5fdc6eb1d60c6c47",
    f"{LIBRARY_DIRS[1]}/libggml-base.0.22.0.dylib": "9d96b2f3e580901342d5981ceb8c3899ef562c3fec119e7f631a35ebf6997914",
    f"{LIBRARY_DIRS[1]}/libggml.0.22.0.dylib": "04e26574ebad49c5284f86bde3fd3935512988ab3d0b14fca1a83de8064fadfb",
    "/opt/homebrew/Cellar/ggml/0.22.0/libexec/libggml-blas.so": "cb0f72c3d4f66475143dde5974bec5e662e00ea0d8db65f12cb942ffe0112a3a",
    "/opt/homebrew/Cellar/ggml/0.22.0/libexec/libggml-cpu-apple_m4.so": "8c34933269a116f6bcdd25174f6f456f926c6a73f88b02906251b4893e85a47f",
    "/opt/homebrew/Cellar/ggml/0.22.0/libexec/libggml-cpu-apple_m2_m3.so": "682271fef76e7f6808cda2db200bb5f75197ce82290b02d58daa2478f4ef6d08",
    "/opt/homebrew/Cellar/ggml/0.22.0/libexec/libggml-cpu-apple_m1.so": "5582ec4e959ebfc3296ee8291ed1613a0e3b70017d5e7a629bd9d4fd32b5c26d",
    "/opt/homebrew/Cellar/ggml/0.22.0/libexec/libggml-metal.so": "c6c848b8174821090bd22864e72861cd469ac3c0c03c2d6a0f872f252239a7d7",
    f"{LIBRARY_DIRS[2]}/libomp.dylib": "0d18bd3a84eae020733be930e1e6fa47925597cfdc4afd9210644836bc4a1b54",
    f"{LIBRARY_DIRS[3]}/libssl.3.dylib": "4c3c554adc8ace6ec2245b4962b181451d245edfab92c3a09fc7b3be094e7438",
    f"{LIBRARY_DIRS[3]}/libcrypto.3.dylib": "34bc039f5c725691e757ef42d26f1709830b18046c3ad6d93985153c83d0bbbc",
}
REQUIRED_IMAGES = {path for path in PINNED_FILES if "/libexec/" not in path}
LOAD_ALIASES = {
    f"{LIBRARY_DIRS[0]}/libmtmd.0.dylib": f"{LIBRARY_DIRS[0]}/libmtmd.0.3.0.dylib",
    f"{LIBRARY_DIRS[0]}/libllama-common.0.dylib": f"{LIBRARY_DIRS[0]}/libllama-common.0.3.0.dylib",
    f"{LIBRARY_DIRS[0]}/libllama.0.dylib": f"{LIBRARY_DIRS[0]}/libllama.0.3.0.dylib",
    f"{LIBRARY_DIRS[1]}/libggml.0.dylib": f"{LIBRARY_DIRS[1]}/libggml.0.22.0.dylib",
    f"{LIBRARY_DIRS[1]}/libggml-base.0.dylib": f"{LIBRARY_DIRS[1]}/libggml-base.0.22.0.dylib",
}
# Component-level evidence stays local. Formula/SBOM declarations are not legal
# validation and do not override conflicting installed headers/licence text.
EVIDENCE_FILES = {
    "/opt/homebrew/Cellar/llama.cpp/0.3.0/LICENSE": "94f29bbed6a22c35b992c5c6ebf0e7c92f13b836b90f36f461c9cf2f0f1d010d",
    "/opt/homebrew/Cellar/ggml/0.22.0/LICENSE": "94f29bbed6a22c35b992c5c6ebf0e7c92f13b836b90f36f461c9cf2f0f1d010d",
    "/opt/homebrew/Cellar/libomp/23.1.0/LICENSE.TXT": "8d85c1057d742e597985c7d4e6320b015a9139385cff4cbae06ffc0ebe89afee",
    "/opt/homebrew/Cellar/libomp/23.1.0/include/omp.h": "4066c7a384a8c9a8a241287db0e2625216746da831c61083124d11ae203ab66f",
    "/opt/homebrew/Cellar/libomp/23.1.0/.brew/libomp.rb": "7d7be5b093acc3a6c08c399a1ef319b3bb79a277cb3f17dc51150e8c805dc548",
    "/opt/homebrew/Cellar/libomp/23.1.0/sbom.spdx.json": "2af26eb3906aa1b859af06fbc98558376634d0a60e5cdc6f5311cc3c00ad7981",
    "/opt/homebrew/Cellar/llama.cpp/0.3.0/sbom.spdx.json": "b8f3b43db2e57f1110876d6c5e951e18d842e315fdacb7eacaef03779260efb6",
    "/opt/homebrew/Cellar/ggml/0.22.0/sbom.spdx.json": "1e8bf3c51b84908cf72b728c2e0f5f042c665b8c5f5a301dd040f7d0a8e45869",
    "/opt/homebrew/Cellar/openssl@3/3.6.3/LICENSE.txt": "7d5450cb2d142651b8afa315b5f238efc805dad827d91ba367d8516bc9d49e7a",
    "/opt/homebrew/Cellar/llama.cpp/0.3.0/INSTALL_RECEIPT.json": "0e23309d328be8b3e857a9908c954009d2c2cb62adf587058982a7a9081e4dee",
    "/opt/homebrew/Cellar/ggml/0.22.0/INSTALL_RECEIPT.json": "4fdd361f7f6f74b2c418978b0b252a51150b7dc7da783d3e392f36d99fc0feb5",
    "/opt/homebrew/Cellar/libomp/23.1.0/INSTALL_RECEIPT.json": "a594117840bf0322ace223fcbddfcb3c3e4370be534ff7188398a9eee67d2f49",
    "/opt/homebrew/Cellar/openssl@3/3.6.3/INSTALL_RECEIPT.json": "61f92ad09c433d5445308a263987163f5463c2d40e26c84fc61469f264b72ca8",
}


def profile_digest() -> str:
    value = {
        "profile_id": PROFILE_ID,
        "runtime": core.profile_digest(sys.modules[__name__]),
        "evidence": EVIDENCE_FILES,
        "version": VERSION_LINE.hex(),
        "markers": [marker.hex() for marker in VERSION_MARKERS],
    }
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify_files() -> None:
    core.verify_files(sys.modules[__name__])
    for name, digest in EVIDENCE_FILES.items():
        path = Path(name)
        try:
            if path.resolve(strict=True) != path or not path.is_file():
                raise ValueError("profile_evidence_path_mismatch")
            if core._sha256(path) != digest:
                raise ValueError("profile_evidence_digest_mismatch")
        except OSError as exc:
            raise ValueError("profile_evidence_unavailable") from exc


def profile_environment() -> dict[str, str]:
    return core.profile_environment(sys.modules[__name__])


def verify_loaded_images(stderr: bytes) -> list[str]:
    return core.verify_loaded_images(stderr, sys.modules[__name__])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--diagnostic", choices=("version", "help"), default="version")
    args = parser.parse_args(argv)
    if args.receipt.exists() or args.receipt.is_symlink():
        print(json.dumps({"status": "receipt_exists", "study_unlocked": False}))
        return 1
    result = core.capture_version(sys.modules[__name__], diagnostic=args.diagnostic)
    data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        with args.receipt.open("xb") as stream:
            stream.write(data)
    except OSError:
        print(json.dumps({"status": "receipt_write_failed", "study_unlocked": False}))
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
    return 0 if result["status"] == "runtime_profile_observed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
