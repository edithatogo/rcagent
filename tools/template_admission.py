"""Verify revision-bound draft-template admission against captured package bytes.

This gate checks a reviewed inventory, not legal protection, case applicability,
or a cryptographic assertion about who reviewed the content. Release source
verification separately binds the inventory and payload to a Git revision.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from hashlib import sha256
from pathlib import PurePosixPath
from typing import cast

MANIFEST_PATH = "assets/template-admission.json"
CONTRACT_PATH = "assets/template-use-contract.md"
_REQUIRED_SUPPORT = {
    CONTRACT_PATH,
    "assets/styles/docx-style-guide.md",
    "assets/styles/pptx-style-guide.md",
    "references/just-culture-guide.md",
}
_PREFIXES = ("assets/templates/", "assets/styles/")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"template admission: duplicate JSON key {key!r}")
        result[key] = value
    return result


def _object(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"template admission: {context} must be an object")
    return cast(dict[str, object], value)


def _in_scope(path: str) -> bool:
    return path in _REQUIRED_SUPPORT or path.startswith(_PREFIXES)


def validate_template_admission(files: Mapping[str, bytes]) -> str:
    """Reject missing, altered, unlisted or non-admitted rendering assets.

    ``files`` uses skill-relative paths and the exact captured payloads that
    will be written to the archive. No second filesystem read can substitute
    unreviewed bytes between this check and packaging. Return the manifest hash.
    """
    payload = files.get(MANIFEST_PATH)
    if payload is None:
        raise ValueError("template admission: manifest is missing")
    try:
        decoded = cast(
            object, json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object)
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("template admission: manifest must be UTF-8 JSON") from error
    manifest = _object(decoded, "manifest")
    if manifest.get("schema_version") != "1.0":
        raise ValueError("template admission: unsupported schema version")
    if manifest.get("admission") != "portable_draft_only":
        raise ValueError("template admission: revision is not admitted for draft packaging")
    if manifest.get("scope") != "templates-and-support":
        raise ValueError("template admission: unsupported asset scope")
    if not isinstance(manifest.get("revision"), str) or not manifest["revision"]:
        raise ValueError("template admission: revision identifier is missing")
    raw_entries = manifest.get("files")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ValueError("template admission: files must be a non-empty array")
    entries = cast(list[object], raw_entries)
    admitted: set[str] = set()
    for raw_entry in entries:
        entry = _object(raw_entry, "file entry")
        path, digest = entry.get("path"), entry.get("sha256")
        if (
            not isinstance(path, str)
            or "\\" in path
            or PurePosixPath(path).is_absolute()
            or PurePosixPath(path).as_posix() != path
            or ".." in PurePosixPath(path).parts
            or not _in_scope(path)
        ):
            raise ValueError("template admission: file path is outside the canonical asset scope")
        if path in admitted:
            raise ValueError(f"template admission: duplicate file {path!r}")
        if entry.get("status") != "admitted_portable_draft":
            raise ValueError(f"template admission: file is not admitted {path!r}")
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            raise ValueError(f"template admission: invalid SHA-256 for {path!r}")
        if path not in files:
            raise ValueError(f"template admission: admitted file is missing {path!r}")
        if sha256(files[path]).hexdigest() != digest:
            raise ValueError(f"template admission: content hash mismatch for {path!r}")
        admitted.add(path)
    captured = {path for path in files if _in_scope(path)}
    if captured != admitted:
        raise ValueError(
            f"template admission: unlisted rendering assets {sorted(captured - admitted)!r}"
        )
    if not admitted >= _REQUIRED_SUPPORT or not any(
        path.startswith(_PREFIXES[0]) for path in admitted
    ):
        raise ValueError("template admission: required support or templates are missing")
    return sha256(payload).hexdigest()
