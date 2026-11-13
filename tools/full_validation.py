"""Run the complete deterministic local repository gate with one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
CHECKS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "ruff", "check", "tools", "tests"),
    (sys.executable, "-m", "ruff", "format", "--check", "tools", "tests"),
    (sys.executable, "-m", "ty", "check", "tools", "tests"),
    (sys.executable, "-m", "basedpyright", "--baselinemode=discard"),
    (sys.executable, "-m", "tools.quality_gate", "baseline"),
    (sys.executable, "-m", "tools.quality_gate", "security"),
    (sys.executable, "-m", "vulture"),
    (sys.executable, "-m", "tools.check_gremlins", "."),
    (sys.executable, "-m", "tools.validate_repository"),
    (sys.executable, "-m", "tools.benchmark_harness", "validate"),
    (sys.executable, "-m", "tools.benchmark_harness", "run", "--suite", "regression"),
    (
        sys.executable,
        "-m",
        "pytest",
        "--cov",
        "--cov-report=xml",
        "--cov-report=term-missing",
    ),
)


def main(argv: list[str] | None = None) -> int:
    """Run checks in hosted Quality-workflow order and fail on the first error."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--defer-coverage-floor",
        action="store_true",
        help="Collect coverage for the required combined matrix gate; keep test failures fatal.",
    )
    args = parser.parse_args([] if argv is None else argv)
    for command in CHECKS:
        if command[2] == "pytest" and args.defer_coverage_floor:
            command = (*command, "--cov-fail-under=0")
        print(f"+ {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)  # nosec B603 # fixed local Python module commands; shell is not used
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":  # pragma: no branch - exercised by the documented command
    raise SystemExit(main(sys.argv[1:]))  # pragma: no cover - subprocess entry point
