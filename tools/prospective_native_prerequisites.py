"""Enumerated native committed-byte prerequisites, not a complete execution gate."""

from __future__ import annotations

from pathlib import Path

from tools import prospective_freeze as freeze
from tools import prospective_native_protocol as native

KNOWN_NATIVE_SOURCES = (
    "tools/__init__.py",
    "tools/prospective_native_prerequisites.py",
    "tools/prospective_freeze.py",
    "tools/prospective_native_protocol.py",
    "tools/prospective_protocol.py",
    "tools/prospective_runner_contract.py",
    "tools/native_completion.py",
    "tools/prospective_inventory.py",
    "tools/evaluation_preflight.py",
)


def verify_native_prerequisites(
    protocol_path: Path, expected_protocol_sha256: str, slot_id: str, commit: str, root: Path
) -> dict:
    """Check a fixed subset of committed bytes; never issue execution permission."""
    if (
        type(slot_id) is not str
        or len(slot_id) > 150
        or native.runner.SLOT.fullmatch(slot_id) is None
    ):
        raise ValueError("slot_not_in_protocol")
    if ".." in protocol_path.parts:
        raise ValueError("invalid_protocol_path")
    if type(commit) is not str:
        raise ValueError("invalid_freeze_commit")
    root, protocol_path, relative = freeze._repository(protocol_path, commit, root)
    value, candidate = native._validated_candidate(protocol_path, expected_protocol_sha256)
    if slot_id not in candidate["requests"]:
        raise ValueError("slot_not_in_protocol")
    refs = [case["input"] for case in value["cases"]]
    refs.extend(value[key] for key in ("rubric", "scoring_instructions", "prompt_template"))
    expected = {relative: expected_protocol_sha256}
    for ref in refs:
        path = (protocol_path.parent / ref["path"]).relative_to(root).as_posix()
        expected[path] = ref["sha256"]
    paths = [
        relative,
        *((protocol_path.parent / ref["path"]).relative_to(root).as_posix() for ref in refs),
        *KNOWN_NATIVE_SOURCES,
    ]
    files = freeze._committed_files(root, commit, paths, expected)
    return {
        "status": "native_prerequisites_consistent",
        "commit": commit,
        "protocol_sha256": candidate["protocol_sha256"],
        "study_id": candidate["study_id"],
        "slot_id": slot_id,
        "files": files,
        "execution_permitted": False,
        "execution_observed": False,
        "admitted": False,
        "study_unlocked": False,
        "pending": [
            "primary-adapter",
            "full-transitive-execution-closure",
            "agent-review-evidence",
            "fresh-model-eligibility",
            "loaded-code-attestation",
        ],
        "limitations": [
            "enumerated-committed-byte-consistency-only",
            "not-study-freeze",
            "not-atomic-filesystem-attestation",
            "privacy-unverified",
            "not-execution-permission",
            "no-primary-observations",
        ],
    }
