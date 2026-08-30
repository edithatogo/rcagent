"""Fixture receipt integrity checks; live semantic admission is not implemented."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROLES = {
    "admission": {"protocol", "manifest", "raw", "normalized", "metadata", "attestation"},
    "scoring": {"protocol", "manifest", "admission", "blinding"},
    "analysis": {"protocol", "manifest", "admission", "blinding", "scores", "panel-review"},
}
MAX_BYTES = 4 * 1024 * 1024


def _unique(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _bytes(path: Path) -> bytes:
    try:
        if any(part.is_symlink() for part in (path, *path.parents)) or not path.is_file():
            raise ValueError("non_regular_or_symlink_artifact")
        with path.open("rb") as handle:
            value = handle.read(MAX_BYTES + 1)
    except OSError as exc:
        raise ValueError("unreadable_artifact") from exc
    if not value or len(value) > MAX_BYTES:
        raise ValueError("artifact_size_out_of_bounds")
    return value


def _digest(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def check_envelope(receipt: Path, expected_sha256: str, stage: str) -> dict:
    """Check fixture structure and byte identity; this never admits a study."""
    data = _bytes(receipt.absolute())
    if not _digest(expected_sha256) or hashlib.sha256(data).hexdigest() != expected_sha256:
        raise ValueError("receipt_pin_mismatch")
    try:
        value = json.loads(data, object_pairs_hook=_unique)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("invalid_json") from exc
    fields = {"schema_version", "purpose", "study_id", "revision", "stage", "files"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("invalid_envelope_fields")
    if value["schema_version"] != "1.0" or value["purpose"] != "contract-fixture":
        raise ValueError("unsupported_schema_or_purpose")
    if stage not in ROLES or value["stage"] != stage:
        raise ValueError("stage_mismatch")
    if not isinstance(value["study_id"], str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9-]{0,79}", value["study_id"]
    ):
        raise ValueError("invalid_study_id")
    if not isinstance(value["revision"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", value["revision"]
    ):
        raise ValueError("invalid_revision")
    entries = value["files"]
    if not isinstance(entries, list) or len(entries) != len(ROLES[stage]):
        raise ValueError("invalid_artifact_count")
    roles: set[str] = set()
    paths: set[str] = set()
    root = receipt.absolute().parent
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"role", "path", "sha256"}:
            raise ValueError("invalid_artifact_fields")
        role, relative = entry["role"], entry["path"]
        if not isinstance(role, str) or role not in ROLES[stage] or role in roles:
            raise ValueError("invalid_or_duplicate_role")
        if (
            not isinstance(relative, str)
            or not relative
            or "\\" in relative
            or ":" in relative
            or any(ord(char) < 32 for char in relative)
        ):
            raise ValueError("invalid_artifact_path")
        parts = relative.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError("invalid_artifact_path")
        if relative.casefold() in paths:
            raise ValueError("duplicate_artifact_path")
        content = _bytes(root.joinpath(*parts))
        if not _digest(entry["sha256"]) or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise ValueError("artifact_hash_mismatch")
        roles.add(role)
        paths.add(relative.casefold())
    return {"status": "fixture_pass", "stage": stage, "study_unlocked": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=sorted(ROLES))
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--expected-sha256", default="")
    parser.add_argument("--check-fixture", action="store_true")
    args = parser.parse_args(argv)
    if not args.check_fixture:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason": "semantic_admission_not_implemented",
                    "stage": args.stage,
                    "study_unlocked": False,
                },
                sort_keys=True,
            )
        )
        return 1
    try:
        if args.receipt is None:
            raise ValueError("receipt_required")
        result = check_envelope(args.receipt, args.expected_sha256, args.stage)
    except ValueError as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc), "study_unlocked": False}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover - thin entry point
    raise SystemExit(main())
