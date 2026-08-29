from __future__ import annotations

import sys
from types import SimpleNamespace

from tools import full_validation
from tools.full_validation import CHECKS


def test_full_validation_is_local_deterministic_and_matches_quality_gate() -> None:
    modules = [command[2] for command in CHECKS]
    assert all(command[:2] == (sys.executable, "-m") for command in CHECKS)
    assert modules == [
        "ruff",
        "ty",
        "basedpyright",
        "tools.check_gremlins",
        "tools.validate_repository",
        "tools.benchmark_harness",
        "tools.benchmark_harness",
        "pytest",
    ]
    command_text = " ".join(part for command in CHECKS for part in command).lower()
    assert all(token not in command_text for token in ("curl", "wget", "download", "ollama", "huggingface"))


def test_full_validation_runs_every_check_on_success(monkeypatch) -> None:
    observed: list[tuple[tuple[str, ...], object, bool]] = []

    def fake_run(command, *, cwd, check):
        observed.append((command, cwd, check))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(full_validation.subprocess, "run", fake_run)
    assert full_validation.main() == 0
    assert [item[0] for item in observed] == list(CHECKS)
    assert all(item[1] == full_validation.ROOT and item[2] is False for item in observed)


def test_full_validation_stops_at_first_failure(monkeypatch) -> None:
    return_codes = iter((0, 9))
    observed: list[tuple[str, ...]] = []

    def fake_run(command, *, cwd, check):
        del cwd, check
        observed.append(command)
        return SimpleNamespace(returncode=next(return_codes))

    monkeypatch.setattr(full_validation.subprocess, "run", fake_run)
    assert full_validation.main() == 9
    assert observed == list(CHECKS[:2])
