from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from tools.build_distribution import build_distribution

ROOT = Path(__file__).parents[1]


def test_distribution_is_deterministic_and_self_describing(tmp_path: Path) -> None:
    first = build_distribution(ROOT, tmp_path / "first", version="0.0.0-test")
    second = build_distribution(ROOT, tmp_path / "second", version="0.0.0-test")

    assert first.archive.read_bytes() == second.archive.read_bytes()
    assert first.manifest["archive"]["sha256"] == hashlib.sha256(
        first.archive.read_bytes()
    ).hexdigest()
    assert first.manifest["licence"] == "Apache-2.0"
    assert first.manifest["public_release"] is False
    assert first.manifest["telemetry"] == "none"
    assert first.manifest["network_required"] is False
    assert first.manifest["data_classification"] == "public-only-no-clinical-or-employee-data"
    assert first.manifest["third_party_content"] == "prohibited-unless-release-cleared"
    assert first.manifest["approval_boundaries"] == [
        "clinical",
        "policy",
        "legal",
        "organisational",
    ]


def test_distribution_contains_only_portable_core_and_release_metadata(tmp_path: Path) -> None:
    result = build_distribution(ROOT, tmp_path, version="0.0.0-test")

    with zipfile.ZipFile(result.archive) as archive:
        names = set(archive.namelist())
        assert "rca-investigation/SKILL.md" in names
        assert "rca-investigation/LICENSE" in names
        assert "rca-investigation/DISCLAIMER.md" in names
        assert "rca-investigation/distribution-manifest.json" in names
        assert "rca-investigation/sbom.cdx.json" in names
        assert not any(name.startswith("rca-investigation/.git") for name in names)
        manifest = json.loads(
            archive.read("rca-investigation/distribution-manifest.json")
        )
        for entry in manifest["files"]:
            payload = archive.read(f"rca-investigation/{entry['path']}")
            assert hashlib.sha256(payload).hexdigest() == entry["sha256"]


def test_distribution_rejects_nonempty_destination(tmp_path: Path) -> None:
    destination = tmp_path / "dist"
    destination.mkdir()
    (destination / "unrelated.txt").write_text("preserve", encoding="utf-8")

    try:
        build_distribution(ROOT, destination, version="0.0.0-test")
    except FileExistsError as error:
        assert "destination must be empty" in str(error)
    else:
        raise AssertionError("non-empty destination was overwritten")


@pytest.mark.parametrize("version", ["../escape", "a/b", "a\\b", "", ".", ".."])
def test_distribution_rejects_unsafe_version(version: str, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="safe release identifier"):
        build_distribution(ROOT, tmp_path / "dist", version=version)


def test_distribution_refuses_destination_inside_portable_source(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    skill = repository / "skills/rca-investigation"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
    (repository / "LICENSE").write_text("Apache License\n", encoding="utf-8")
    (repository / "DISCLAIMER.md").write_text("Disclaimer\n", encoding="utf-8")

    with pytest.raises(ValueError, match="outside the portable source"):
        build_distribution(repository, skill / "dist", version="1.0.0")
