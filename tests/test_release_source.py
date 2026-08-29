from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tools.release_source import verify_release_payloads, verify_release_source


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()


def _repository(tmp_path: Path) -> tuple[Path, str]:
    repository = tmp_path / "repository"
    (repository / "input/nested").mkdir(parents=True)
    (repository / "input/nested/file.txt").write_bytes(b"exact\n")
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
    (repository / "input/nested/file.txt").write_bytes(b"drift\n")
    with pytest.raises(ValueError, match="uncommitted drift"):
        verify_release_source(repository, revision, [repository / "input"])


def test_release_source_rejects_symlinked_input(tmp_path: Path) -> None:
    repository, revision = _repository(tmp_path)
    (repository / "input/link").symlink_to(repository / "input/nested/file.txt")
    with pytest.raises(ValueError, match="symlink"):
        verify_release_source(repository, revision, [repository / "input"])


def test_captured_release_payload_must_equal_commit_even_after_worktree_reversion(
    tmp_path: Path,
) -> None:
    repository, revision = _repository(tmp_path)
    captured = {"input/nested/file.txt": b"raced\n"}
    verify_release_source(repository, revision, [repository / "input"])
    with pytest.raises(ValueError, match="captured release payload differs"):
        verify_release_payloads(repository, revision, captured)


def test_release_source_rejects_wrong_head_missing_and_outside_inputs(tmp_path: Path) -> None:
    repository, revision = _repository(tmp_path)
    (repository / "second.txt").write_bytes(b"second\n")
    _git(repository, "add", ".")
    _git(repository, "commit", "-qm", "second")
    with pytest.raises(ValueError, match="checked-out HEAD"):
        verify_release_source(repository, revision, [repository / "input"])
    head = _git(repository, "rev-parse", "HEAD")
    with pytest.raises(ValueError, match="outside"):
        verify_release_source(repository, head, [tmp_path / "outside"])
    with pytest.raises(ValueError, match="missing or special"):
        verify_release_source(repository, head, [repository / "missing"])
    with pytest.raises(ValueError, match="absent from source revision"):
        verify_release_payloads(repository, head, {"missing.txt": b"missing"})
