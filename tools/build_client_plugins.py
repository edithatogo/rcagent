"""Build deterministic, skills-only client plugin release candidates."""

from __future__ import annotations

import hashlib
import json
import re
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
_SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")
_CLIENTS = {"codex", "claude-code"}


@dataclass(frozen=True)
class ClientPluginResult:
    archive: Path
    manifest: dict[str, Any]
    sha256: str


def _json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _member(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, _TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    archive.writestr(info, payload)


def _manifest(client: str, version: str) -> tuple[str, dict[str, Any]]:
    common: dict[str, Any] = {
        "name": "rca-investigation",
        "version": version,
        "description": "Evidence-grounded healthcare safety investigation support for accountable human teams.",
        "author": {"name": "edithatogo", "url": "https://github.com/edithatogo"},
        "homepage": "https://github.com/edithatogo/rcagent",
        "repository": "https://github.com/edithatogo/rcagent",
        "license": "Apache-2.0",
        "keywords": ["agent-skills", "healthcare-safety", "systems-analysis"],
        "skills": "./skills/",
    }
    if client == "codex":
        common["interface"] = {
            "displayName": "RCA Investigation",
            "shortDescription": "Evidence-grounded healthcare safety investigation support.",
            "longDescription": "Supports accountable human teams with bounded chronology, systems analysis, reporting, and action review workflows.",
            "developerName": "edithatogo",
            "category": "Productivity",
            "capabilities": [],
            "defaultPrompt": "Help me scope a generated-synthetic safety investigation.",
        }
        return ".codex-plugin/plugin.json", common
    return ".claude-plugin/plugin.json", common


def build_client_plugin(
    repository: Path,
    destination: Path,
    *,
    client: str,
    version: str,
    source_revision: str,
) -> ClientPluginResult:
    """Create a no-network plugin archive containing an exact copy of the core."""
    repository, destination = repository.resolve(), destination.resolve()
    if client not in _CLIENTS:
        raise ValueError("unsupported client plugin")
    if _SEMVER.fullmatch(version) is None:
        raise ValueError("version must be strict semantic versioning")
    if _REVISION.fullmatch(source_revision) is None:
        raise ValueError("source revision must be a full Git commit hash")
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError("destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    skill = repository / "skills/rca-investigation"
    documents = [repository / name for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md")]
    if not (skill / "SKILL.md").is_file() or not all(path.is_file() for path in documents):
        raise FileNotFoundError("plugin release inputs are incomplete")
    paths = sorted(skill.rglob("*"))
    if any(path.is_symlink() for path in paths):
        raise ValueError("plugin release refuses symlinks")
    manifest_path, manifest = _manifest(client, version)
    provenance = {
        "schema_version": "1.0",
        "source_repository": "https://github.com/edithatogo/rcagent",
        "source_revision": source_revision,
        "version": version,
        "client": client,
        "network": "none",
        "telemetry": "none-in-package",
        "private_data": False,
    }
    archive_path = destination / f"rca-investigation-{client}-{version}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        _member(archive, manifest_path, _json(manifest))
        _member(archive, "PROVENANCE.json", _json(provenance))
        for path in paths:
            if path.is_file():
                relative = path.relative_to(skill).as_posix()
                _member(archive, f"skills/rca-investigation/{relative}", path.read_bytes())
        for path in documents:
            _member(archive, path.name, path.read_bytes())
    payload = archive_path.read_bytes()
    return ClientPluginResult(archive_path, manifest, _hash(payload))
