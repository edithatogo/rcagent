from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest

from tools import build_distribution as distribution_module
from tools.build_distribution import build_distribution

ROOT = Path(__file__).parents[1]


def test_distribution_is_deterministic_and_self_describing(tmp_path: Path) -> None:
    first = build_distribution(ROOT, tmp_path / "first", version="0.0.0-test")
    second = build_distribution(ROOT, tmp_path / "second", version="0.0.0-test")

    assert first.archive.read_bytes() == second.archive.read_bytes()
    assert (
        first.manifest["archive"]["sha256"]
        == hashlib.sha256(first.archive.read_bytes()).hexdigest()
    )
    assert first.manifest["licence"] == "Apache-2.0"
    assert first.manifest["public_release"] is False
    assert first.manifest["telemetry"] == "none"
    assert first.manifest["network_required"] is False
    assert first.manifest["data_classification"] == "public-only-no-clinical-or-employee-data"
    assert first.manifest["third_party_content"] == "prohibited-unless-release-cleared"
    assert first.manifest["source_revision"] == "uncommitted-test-build"
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
        assert "rca-investigation/PRIVACY.md" in names
        assert "rca-investigation/SUPPORT.md" in names
        assert "rca-investigation/CHANGELOG.md" in names
        assert "rca-investigation/distribution-manifest.json" in names
        assert "rca-investigation/sbom.cdx.json" in names
        assert not any(name.startswith("rca-investigation/.git") for name in names)
        manifest = json.loads(archive.read("rca-investigation/distribution-manifest.json"))
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
    (repository / "PRIVACY.md").write_text("Privacy\n", encoding="utf-8")
    (repository / "SUPPORT.md").write_text("Support\n", encoding="utf-8")
    (repository / "CHANGELOG.md").write_text("Changelog\n", encoding="utf-8")

    with pytest.raises(ValueError, match="outside the portable source"):
        build_distribution(repository, skill / "dist", version="1.0.0")


def test_distribution_rejects_missing_inputs_and_symlinks(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    with pytest.raises(FileNotFoundError, match="missing"):
        build_distribution(repository, tmp_path / "missing-dist", version="1.0.0")
    skill = repository / "skills/rca-investigation"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
    (repository / "LICENSE").write_text("Apache License\n", encoding="utf-8")
    (repository / "DISCLAIMER.md").write_text("Disclaimer\n", encoding="utf-8")
    for name in ("PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION"):
        (repository / name).write_text(name + "\n", encoding="utf-8")
    target = tmp_path / "target.txt"
    target.write_text("outside", encoding="utf-8")
    (skill / "linked.txt").symlink_to(target)
    with pytest.raises(ValueError, match="refuses symlink"):
        build_distribution(repository, tmp_path / "symlink-dist", version="1.0.0")


def test_distribution_binds_exact_release_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(distribution_module, "verify_release_source", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(distribution_module, "verify_release_payloads", lambda *_args, **_kwargs: None)
    result = build_distribution(ROOT, tmp_path / "valid", version="0.1.0", source_revision="a" * 40)
    assert result.manifest["source_revision"] == "a" * 40
    assert result.manifest["source"] == "https://github.com/edithatogo/rcagent"
    with pytest.raises(ValueError, match="full Git commit"):
        build_distribution(ROOT, tmp_path / "invalid", version="0.1.0", source_revision="main")


def test_distribution_cli_success_and_parser_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = tmp_path / "dist"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build-distribution",
            "--repository",
            str(ROOT),
            "--destination",
            str(destination),
            "--version",
            "1.2.3",
        ],
    )
    assert distribution_module.main() == 0
    assert capsys.readouterr().out.strip().endswith("rca-investigation-1.2.3.zip")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build-distribution",
            "--repository",
            str(ROOT),
            "--destination",
            str(tmp_path / "bad"),
            "--version",
            "../bad",
        ],
    )
    with pytest.raises(SystemExit) as exc:
        distribution_module.main()
    assert exc.value.code == 2
    assert "safe release identifier" in capsys.readouterr().err
