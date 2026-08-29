"""Assemble a deterministic public-release candidate without publishing it."""

from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from tools.build_client_plugins import build_client_plugin
from tools.build_distribution import build_distribution


@dataclass(frozen=True)
class ReleaseCandidate:
    destination: Path
    files: tuple[Path, ...]
    manifest: dict[str, object]


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_release_candidate(
    repository: Path, destination: Path, *, version: str, source_revision: str
) -> ReleaseCandidate:
    """Build core and skills-only client assets with one checksum manifest."""
    repository, destination = repository.resolve(), destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError("release candidate destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rcagent-release-") as temporary:
        work = Path(temporary)
        core = build_distribution(repository, work / "core", version=version)
        codex = build_client_plugin(
            repository, work / "codex", client="codex", version=version, source_revision=source_revision
        )
        claude = build_client_plugin(
            repository, work / "claude", client="claude-code", version=version, source_revision=source_revision
        )
        sources = [core.archive, core.manifest_path, core.sbom_path, codex.archive, claude.archive]
        outputs: list[Path] = []
        for source in sources:
            target = destination / source.name
            target.write_bytes(source.read_bytes())
            outputs.append(target)
    records = [
        {"path": path.name, "sha256": _hash(path), "size": path.stat().st_size}
        for path in sorted(outputs)
    ]
    manifest: dict[str, object] = {
        "schema_version": "1.0",
        "name": "rca-investigation",
        "version": version,
        "source_repository": "https://github.com/edithatogo/rcagent",
        "source_revision": source_revision,
        "licence": "Apache-2.0",
        "release_state": "candidate_not_published",
        "rights_state": "repository_authored_public_only_candidate",
        "private_data": False,
        "third_party_controlled_bytes": False,
        "clients": ["agent-skills", "codex", "claude-code"],
        "files": records,
    }
    manifest_path = destination / "release-candidate.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    checksum_path = destination / "MANIFEST.sha256"
    checksum_path.write_text(
        "".join(f"{_hash(path)}  {path.name}\n" for path in sorted([*outputs, manifest_path]))
    )
    return ReleaseCandidate(destination, tuple([*outputs, manifest_path, checksum_path]), manifest)
