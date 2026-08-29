"""Fail-closed admission of public release inputs against a reviewed inventory."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SENSITIVE = re.compile(
    rb"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s<]{8,}"
    rb"|\b(?:MRN|employee[_ -]?id|patient[_ -]?id)\s*[:=]\s*[A-Za-z0-9-]{4,}"
)


def release_input_paths(repository: Path) -> list[Path]:
    skill = repository / "skills/rca-investigation"
    paths = [path for path in sorted(skill.rglob("*")) if path.is_file()]
    paths.extend(
        repository / name
        for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION")
    )
    return paths


def validate_release_inventory(repository: Path, inventory_path: Path) -> dict[str, object]:
    """Require every and only release input to have exact public-rights evidence."""
    repository = repository.resolve()
    value = json.loads(inventory_path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "1.0" or value.get("licence") != "Apache-2.0":
        raise ValueError("release rights inventory metadata is invalid")
    records = value.get("files")
    if not isinstance(records, list):
        raise ValueError("release rights inventory files are invalid")
    by_path: dict[str, dict[str, object]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise ValueError("release rights inventory record is invalid")
        name = str(record["path"])
        if name in by_path:
            raise ValueError(f"duplicate rights record: {name}")
        if record.get("rights_basis") != "repository_authored_or_apache_licensed":
            raise ValueError(f"release rights are not admitted: {name}")
        if record.get("author") != "rcagent repository contributors" or record.get(
            "source"
        ) != "https://github.com/edithatogo/rcagent":
            raise ValueError(f"release authorship or source is not admitted: {name}")
        if record.get("licence") != "Apache-2.0" or record.get("data_class") != "public_no_personal_data":
            raise ValueError(f"release data or licence is not admitted: {name}")
        if not isinstance(record.get("sha256"), str) or not _SHA256.fullmatch(str(record["sha256"])):
            raise ValueError(f"release hash is invalid: {name}")
        by_path[name] = record
    actual = release_input_paths(repository)
    actual_names = {path.relative_to(repository).as_posix() for path in actual}
    if set(by_path) != actual_names:
        raise ValueError("release rights inventory is stale or incomplete")
    for path in actual:
        name = path.relative_to(repository).as_posix()
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != by_path[name]["sha256"]:
            raise ValueError(f"release rights hash mismatch: {name}")
        if _SENSITIVE.search(payload):
            raise ValueError(f"release input contains credential or private-data sentinel: {name}")
    return value
