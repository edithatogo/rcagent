from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tools.release_source import verify_release_source


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()


def _repository(tmp_path: Path) -> tuple[Path, str]:
    repository = tmp_path / "repository"
    (repository / "input/nested").mkdir(parents=True)
    (repository / "input/nested/file.txt").write_text("exact\n", encoding="utf-8")
    _git(repository, "init", "-q")
    _git(repository, "config", "user.name", "Test")
    _git(repository, "config", "user.email", "test@example.invalid")
    _git(repository, "add", ".")
    _git(repository, "commit", "-qm", "fixture")
    return repository, _git(repository, "rev-parse", "HEAD")


def test_release_source_requires_real_exact_clean_head(tmp_path: Path) -> None:
    repository, revision = _repository(tmp_path)
    verify_release_source(repository, revision, [repository / "input"])
    with pytest.raises(ValueError, match="repository commit"):
        verify_release_source(repository, "1" * 40, [repository / "input"])
    (repository / "input/nested/file.txt").write_text("drift\n", encoding="utf-8")
    with pytest.raises(ValueError, match="uncommitted drift"):
        verify_release_source(repository, revision, [repository / "input"])


def test_release_source_rejects_symlinked_input(tmp_path: Path) -> None:
    repository, revision = _repository(tmp_path)
    (repository / "input/link").symlink_to(repository / "input/nested/file.txt")
    with pytest.raises(ValueError, match="symlink"):
        verify_release_source(repository, revision, [repository / "input"])
