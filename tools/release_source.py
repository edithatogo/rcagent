"""Verify release inputs against an exact clean Git commit."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal, overload


@overload
def _git(repository: Path, *args: str, text: Literal[True] = True) -> str: ...


@overload
def _git(repository: Path, *args: str, text: Literal[False]) -> bytes: ...


def _git(repository: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args], cwd=repository, check=True, capture_output=True, text=text
    )
    return result.stdout


def verify_release_source(repository: Path, revision: str, paths: list[Path]) -> None:
    """Require HEAD, worktree bytes, and named commit bytes to agree exactly."""
    repository = repository.resolve()
    try:
        resolved = str(_git(repository, "rev-parse", "--verify", f"{revision}^{{commit}}")).strip()
        head = str(_git(repository, "rev-parse", "HEAD")).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError("source revision is not a repository commit") from error
    if resolved != revision or head != revision:
        raise ValueError("source revision must equal the checked-out HEAD commit")
    expanded: list[Path] = []
    for path in paths:
        if path.is_symlink():
            raise ValueError(f"release input is a symlink: {path}")
        try:
            path.relative_to(repository)
        except ValueError as error:
            raise ValueError(f"release input is outside the repository: {path}") from error
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_symlink():
                    raise ValueError(f"release input is a symlink: {child}")
                if child.is_file():
                    expanded.append(child)
                elif not child.is_dir():
                    raise ValueError(f"release input is a special file: {child}")
        elif path.is_file():
            expanded.append(path)
        else:
            raise ValueError(f"release input is missing or special: {path}")
    relative_paths = [path.relative_to(repository).as_posix() for path in expanded]
    status = str(_git(repository, "status", "--porcelain", "--", *relative_paths)).strip()
    if status:
        raise ValueError("release source paths contain uncommitted drift")
    for path, relative in zip(expanded, relative_paths, strict=True):
        try:
            committed = _git(repository, "show", f"{revision}:{relative}", text=False)
        except (OSError, subprocess.CalledProcessError) as error:
            raise ValueError(f"release input is absent from source revision: {relative}") from error
        if committed != path.read_bytes():
            raise ValueError(f"release input differs from source revision: {relative}")


def verify_release_payloads(
    repository: Path, revision: str, payloads: dict[str, bytes]
) -> None:
    """Bind already captured package bytes to the exact named commit."""
    for relative, payload in payloads.items():
        try:
            committed = _git(repository, "show", f"{revision}:{relative}", text=False)
        except (OSError, subprocess.CalledProcessError) as error:
            raise ValueError(f"release payload is absent from source revision: {relative}") from error
        if committed != payload:
            raise ValueError(f"captured release payload differs from source revision: {relative}")


def require_release_version(repository: Path, version: str) -> None:
    """Use VERSION and changelog as the single release-version authority."""
    declared = (repository / "VERSION").read_text().strip()
    changelog = (repository / "CHANGELOG.md").read_text()
    if version != declared or f"## {version} —" not in changelog:
        raise ValueError("release version does not match VERSION and CHANGELOG.md")
