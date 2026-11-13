from __future__ import annotations

import sys
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from tools import full_validation
from tools.full_validation import CHECKS


def test_full_validation_is_local_deterministic_and_matches_quality_gate() -> None:
    modules = [command[2] for command in CHECKS]
    assert all(command[:2] == (sys.executable, "-m") for command in CHECKS)
    assert modules == [
        "ruff",
        "ruff",
        "ty",
        "basedpyright",
        "tools.quality_gate",
        "tools.quality_gate",
        "vulture",
        "tools.check_gremlins",
        "tools.validate_repository",
        "tools.benchmark_harness",
        "tools.benchmark_harness",
        "pytest",
    ]
    command_text = " ".join(part for command in CHECKS for part in command).lower()
    assert all(
        token not in command_text for token in ("curl", "wget", "download", "ollama", "huggingface")
    )
    assert CHECKS[-1][3:] == (
        "--cov",
        "--cov-report=xml",
        "--cov-report=term-missing",
    )


def test_full_validation_runs_every_check_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: list[tuple[tuple[str, ...], object, bool]] = []

    def fake_run(command: tuple[str, ...], *, cwd: Path, check: bool) -> CompletedProcess[str]:
        observed.append((command, cwd, check))
        return CompletedProcess(command, 0)

    monkeypatch.setattr(full_validation.subprocess, "run", fake_run)
    assert full_validation.main() == 0
    assert [item[0] for item in observed] == list(CHECKS)
    assert all(item[1] == full_validation.ROOT and item[2] is False for item in observed)


def test_full_validation_stops_at_first_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    return_codes = iter((0, 9))
    observed: list[tuple[str, ...]] = []

    def fake_run(command: tuple[str, ...], *, cwd: Path, check: bool) -> CompletedProcess[str]:
        del cwd, check
        observed.append(command)
        return CompletedProcess(command, next(return_codes))

    monkeypatch.setattr(full_validation.subprocess, "run", fake_run)
    assert full_validation.main() == 9
    assert observed == list(CHECKS[:2])


@pytest.mark.parametrize("test_exit", [0, 1, 2])
def test_deferred_coverage_keeps_checks_and_test_failure_exit(
    monkeypatch: pytest.MonkeyPatch, test_exit: int
) -> None:
    observed: list[tuple[str, ...]] = []

    def fake_run(command: tuple[str, ...], *, cwd: Path, check: bool) -> CompletedProcess[str]:
        assert cwd == full_validation.ROOT
        assert check is False
        observed.append(command)
        return CompletedProcess(command, test_exit if command[2] == "pytest" else 0)

    monkeypatch.setattr(full_validation.subprocess, "run", fake_run)
    assert full_validation.main(["--defer-coverage-floor"]) == test_exit
    assert observed[:-1] == list(CHECKS[:-1])
    assert observed[-1] == (*CHECKS[-1], "--cov-fail-under=0")
