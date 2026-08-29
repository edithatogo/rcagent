"""Build a deterministic, review-only portable skill distribution."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.release_source import (
    require_release_version,
    verify_release_payloads,
    verify_release_source,
)

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
_SAFE_VERSION = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9._+-]{0,127})\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")


@dataclass(frozen=True)
class DistributionResult:
    archive: Path
    manifest_path: Path
    sbom_path: Path
    manifest: dict[str, Any]


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_zip_member(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, _ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    archive.writestr(info, payload)


def build_distribution(
    repository: Path,
    destination: Path,
    *,
    version: str,
    source_revision: str | None = None,
) -> DistributionResult:
    """Create a deterministic local package without publishing or network access."""
    repository = repository.resolve()
    destination = destination.resolve()
    if not _SAFE_VERSION.fullmatch(version) or version in {".", ".."}:
        raise ValueError("version must be a safe release identifier")
    if source_revision is not None and _REVISION.fullmatch(source_revision) is None:
        raise ValueError("source revision must be a full Git commit hash")
    skill_root = repository / "skills" / "rca-investigation"
    if skill_root.is_symlink() or not skill_root.resolve().is_relative_to(repository):
        raise ValueError("portable skill root must be a contained non-symlink directory")
    if destination == skill_root or skill_root in destination.parents:
        raise ValueError("destination must be outside the portable source")
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError("destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)

    documents = [
        repository / name
        for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION")
    ]
    if (
        not (skill_root / "SKILL.md").is_file()
        or not all(path.is_file() and not path.is_symlink() for path in documents)
    ):
        raise FileNotFoundError("portable skill, repository licence, or disclaimer is missing")

    files: list[tuple[str, bytes]] = []
    for path in sorted(skill_root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"distribution refuses symlink: {path.relative_to(repository)}")
        if not path.is_file() and not path.is_dir():
            raise ValueError(f"distribution refuses special file: {path.relative_to(repository)}")
        if path.is_file():
            files.append((path.relative_to(skill_root).as_posix(), path.read_bytes()))
    files.extend((path.name, path.read_bytes()) for path in documents)
    if source_revision is not None:
        require_release_version(repository, version)
        verify_release_source(repository, source_revision, [skill_root, *documents])
        captured = {
            (skill_root / name).relative_to(repository).as_posix(): payload
            for name, payload in files[: len(files) - len(documents)]
        }
        captured.update(
            {path.relative_to(repository).as_posix(): payload for path, (_, payload) in zip(documents, files[-len(documents):], strict=True)}
        )
        verify_release_payloads(repository, source_revision, captured)

    file_records = [
        {"path": name, "sha256": _sha256(payload), "size": len(payload)}
        for name, payload in files
    ]
    internal_manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "name": "rca-investigation",
        "version": version,
        "licence": "Apache-2.0",
        "source": "local-review-build" if source_revision is None else "https://github.com/edithatogo/rcagent",
        "source_revision": source_revision or "uncommitted-test-build",
        "build_state": "release_candidate_at_build_time",
        "distribution_intent": "public_release",
        "publication_observation": "not_observed_by_offline_builder",
        "network_required": False,
        "telemetry": "none",
        "data_classification": "public-only-no-clinical-or-employee-data",
        "third_party_content": "prohibited-unless-release-cleared",
        "approval_boundaries": ["clinical", "policy", "legal", "organisational"],
        "files": file_records,
    }
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {"component": {"type": "data", "name": "rca-investigation", "version": version}},
        "components": [
            {
                "type": "file",
                "name": record["path"],
                "hashes": [{"alg": "SHA-256", "content": record["sha256"]}],
            }
            for record in file_records
        ],
    }

    archive_path = destination / f"rca-investigation-{version}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, payload in files:
            _write_zip_member(archive, f"rca-investigation/{name}", payload)
        _write_zip_member(
            archive,
            "rca-investigation/distribution-manifest.json",
            _json_bytes(internal_manifest),
        )
        _write_zip_member(archive, "rca-investigation/sbom.cdx.json", _json_bytes(sbom))

    archive_payload = archive_path.read_bytes()
    external_manifest: dict[str, Any] = dict(internal_manifest)
    external_manifest["archive"] = {
        "path": archive_path.name,
        "sha256": _sha256(archive_payload),
        "size": len(archive_payload),
    }
    manifest_path = destination / "distribution-manifest.json"
    sbom_path = destination / "sbom.cdx.json"
    manifest_path.write_bytes(_json_bytes(external_manifest))
    sbom_path.write_bytes(_json_bytes(sbom))
    return DistributionResult(archive_path, manifest_path, sbom_path, external_manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        result = build_distribution(args.repository, args.destination, version=args.version)
    except (FileExistsError, FileNotFoundError, OSError, ValueError) as error:
        parser.error(str(error))
    print(result.archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
