"""Run the complete deterministic local repository gate with one command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
CHECKS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "ruff", "check", "tools", "tests"),
    (sys.executable, "-m", "ty", "check", "tools", "tests"),
    (sys.executable, "-m", "basedpyright"),
    (sys.executable, "-m", "tools.check_gremlins", "."),
    (sys.executable, "-m", "tools.validate_repository"),
    (sys.executable, "-m", "tools.benchmark_harness", "validate"),
    (sys.executable, "-m", "tools.benchmark_harness", "run", "--suite", "regression"),
    (
        sys.executable,
        "-m",
        "pytest",
        "--cov=tools",
        "--cov-report=xml",
        "--cov-report=term-missing",
    ),
)


def main() -> int:
    """Run checks in hosted Quality-workflow order and fail on the first error."""
    for command in CHECKS:
        print(f"+ {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":  # pragma: no branch - exercised by the documented command
    raise SystemExit(main())  # pragma: no cover - subprocess entry point
