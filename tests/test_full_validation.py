from __future__ import annotations

import sys

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
