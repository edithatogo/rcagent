"""Read-only exact-commit consistency; not review, admission or permission to execute."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Literal, TypedDict

from tools import json_shapes
from tools.evaluation_preflight import MAX_BYTES, read_artifact_bytes
from tools.prospective_inventory import ArtifactReference, is_artifact_reference, read_json
from tools.prospective_protocol import validate_protocol

COMPONENTS = (
    "tools/prospective_freeze.py",
    "tools/prospective_protocol.py",
    "tools/json_shapes.py",
    "tools/prospective_inventory.py",
    "tools/evaluation_preflight.py",
    "tools/local_execution_probe.py",
    "tools/local_model_comparator.py",
    "tools/darwin_runtime_profile.py",
)


class CommittedFile(TypedDict):
    """Exact historical closure shape; identity-file byte counts are separate."""

    path: str
    sha256: str


class FreezeResult(TypedDict):
    status: Literal["freeze_verified"]
    commit: str
    protocol_sha256: str
    study_id: str
    files: list[CommittedFile]
    admitted: Literal[False]
    study_unlocked: Literal[False]
    limitations: list[str]


def git_bytes(root: Path, *args: str) -> bytes:
    env = {key: value for key, value in os.environ.items() if key in {"PATH", "SYSTEMROOT"}}
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_LITERAL_PATHSPECS": "1",
        }
    )
    try:
        # Bound retained bytes, not temporary disk use; Git is a trusted local tool.
        with tempfile.TemporaryFile() as output:
            result = subprocess.run(  # nosec B603, B607 # trusted local Git with fixed operations and argv, no shell
                ["git", "--no-replace-objects", "-C", str(root), *args],
                stdout=output,
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
                env=env,
                stdin=subprocess.DEVNULL,
            )
            output.seek(0)
            data = output.read(MAX_BYTES + 1)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("git_unavailable") from exc
    if result.returncode or len(data) > MAX_BYTES:
        raise ValueError("git_lookup_failed")
    return data


def resolve_repository(protocol_path: Path, commit: str, root: Path) -> tuple[Path, Path, str]:
    """Resolve the original repository and exact-commit identity checks."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("invalid_freeze_commit")
    root = root.absolute()
    protocol_path = protocol_path.absolute()
    if root != root.resolve() or not root.is_dir():
        raise ValueError("invalid_repository_root")
    try:
        relative_protocol = protocol_path.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError("protocol_outside_repository") from exc
    if Path(git_bytes(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() != root:
        raise ValueError("repository_root_mismatch")
    if git_bytes(root, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip() != commit:
        raise ValueError("freeze_commit_mismatch")
    return root, protocol_path, relative_protocol


def committed_files(
    root: Path, commit: str, paths: list[str], expected: dict[str, str]
) -> list[CommittedFile]:
    """Compare the enumerated working files and optional pins with exact committed bytes."""
    if len({path.casefold() for path in paths}) != len(paths):
        raise ValueError("duplicate_freeze_path")
    files: list[CommittedFile] = []
    for relative in paths:
        if not re.fullmatch(r"[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*", relative) or any(
            part in {".", ".."} for part in relative.split("/")
        ):
            raise ValueError("invalid_freeze_path")
        working = read_artifact_bytes(root / relative)
        digest = hashlib.sha256(working).hexdigest()
        if relative in expected and digest != expected[relative]:
            raise ValueError("artifact_changed_during_verification")
        entry = git_bytes(root, "ls-tree", "-z", commit, "--", relative)
        match = re.fullmatch(rb"(100644|100755) blob ([0-9a-f]{40})\t([^\x00]+)\x00", entry)
        if not match or match[3] != relative.encode():
            raise ValueError("untracked_or_nonregular_freeze_file")
        blob = match[2].decode()
        size = int(git_bytes(root, "cat-file", "-s", blob).strip())
        if size != len(working) or size > MAX_BYTES:
            raise ValueError("freeze_bytes_mismatch")
        committed = git_bytes(root, "cat-file", "blob", blob)
        if committed != working:
            raise ValueError("freeze_bytes_mismatch")
        files.append({"path": relative, "sha256": digest})
    return files


def _references(value: object) -> list[ArtifactReference]:
    """Check only the references needed after the independent protocol reread."""
    if not json_shapes.is_object(value):
        raise ValueError("invalid_validated_object_type")
    cases = value["cases"]
    if not json_shapes.is_array(cases):
        raise ValueError("invalid_validated_object_type")
    refs: list[ArtifactReference] = []
    for case in cases:
        if not json_shapes.is_object(case):
            raise ValueError("invalid_validated_object_type")
        ref = case["input"]
        if not is_artifact_reference(ref):
            raise ValueError("invalid_validated_object_type")
        refs.append(ref)
    for key in ("rubric", "scoring_instructions", "prompt_template"):
        ref = value[key]
        if not is_artifact_reference(ref):
            raise ValueError("invalid_validated_object_type")
        refs.append(ref)
    return refs


def verify_freeze(
    protocol_path: Path, expected_sha256: str, commit: str, root: Path
) -> FreezeResult:
    """Bind working files to an explicit commit; hashes do not prove their approval."""
    root, protocol_path, relative_protocol = resolve_repository(protocol_path, commit, root)
    candidate = validate_protocol(protocol_path, expected_sha256)
    value, second_pin = read_json(protocol_path)
    if second_pin != expected_sha256:
        raise ValueError("protocol_changed_during_verification")
    refs = _references(value)
    paths = [relative_protocol]
    paths.extend((protocol_path.parent / ref["path"]).relative_to(root).as_posix() for ref in refs)
    paths.extend(COMPONENTS)
    expected = {relative_protocol: expected_sha256}
    expected.update(
        ((protocol_path.parent / ref["path"]).relative_to(root).as_posix(), ref["sha256"])
        for ref in refs
    )
    files = committed_files(root, commit, paths, expected)
    return {
        "status": "freeze_verified",
        "commit": commit,
        "protocol_sha256": candidate["protocol_sha256"],
        "study_id": candidate["study_id"],
        "files": files,
        "admitted": False,
        "study_unlocked": False,
        "limitations": [
            "exact-commit-byte-consistency-only",
            "ancestry-and-timestamps-not-verified",
            "loaded-python-code-not-attested",
            "review-and-approval-not-verified",
            "privacy-not-verified",
            "runtime-admission-not-verified",
            "runner-not-bound",
            "execution-not-authorised-by-this-check",
            "no-primary-observations",
        ],
    }
