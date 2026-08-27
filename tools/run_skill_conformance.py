"""Run the complete Agent Skill conformance profile and emit a durable receipt."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools.check_skill_drift import check_drift
from tools.validate_skill_profile import TRACK, validate_profile


def run_conformance(
    root: Path,
    *,
    validator: str = "skills-ref",
    offline: bool = False,
    require_complete: bool = False,
) -> tuple[int, dict[str, Any]]:
    root = root.resolve()
    skill = root / "skills/rca-investigation"
    try:
        completed = subprocess.run(
            [validator, "validate", str(skill)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        validator_code = completed.returncode
    except OSError:
        validator_code = 127
    profile_errors = validate_profile(root, require_complete=require_complete)
    drift_code, drift = check_drift(
        root / TRACK / "upstream-baseline.json", offline=offline
    )
    local_pass = validator_code == 0 and not profile_errors
    current_pass = local_pass and drift_code == 0 and bool(drift["current_conformance"])
    receipt: dict[str, object] = {
        "schema_version": "1.0",
        "checked_at": datetime.now(UTC).isoformat(),
        "runtime": {"python": platform.python_version(), "platform": platform.system()},
        "official_validator": {
            "command": [validator, "validate", "skills/rca-investigation"],
            "exit_code": validator_code,
            "passed": validator_code == 0,
        },
        "project_profile": {"passed": not profile_errors, "diagnostics": profile_errors},
        "upstream_drift": drift,
        "local_validation_passed": local_pass,
        "current_conformance": current_pass,
    }
    return (0 if current_pass or (offline and local_pass) else 1), receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--validator", default="skills-ref")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    code, receipt = run_conformance(
        args.root,
        validator=args.validator,
        offline=args.offline,
        require_complete=args.require_complete,
    )
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
