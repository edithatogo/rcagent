"""Run the complete Agent Skill conformance profile and emit a durable receipt."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from tools.check_skill_drift import check_drift
from tools.json_shapes import is_object, require_object
from tools.validate_skill_profile import TRACK, validate_profile


class ValidatorProvenance(TypedDict):
    verified: bool
    source: NotRequired[str]
    revision: NotRequired[str | None]


class RuntimeDetails(TypedDict):
    python: str
    platform: str


class OfficialValidatorResult(TypedDict):
    command: list[str]
    provenance: ValidatorProvenance
    exit_code: int
    passed: bool


class ProjectProfileResult(TypedDict):
    passed: bool
    diagnostics: list[str]
    complete: bool
    completion_diagnostics: list[str]


class ConformanceReceipt(TypedDict):
    schema_version: Literal["1.0"]
    checked_at: str
    runtime: RuntimeDetails
    official_validator: OfficialValidatorResult
    project_profile: ProjectProfileResult
    upstream_drift: dict[str, object]
    local_validation_passed: bool
    current_conformance: bool


def validator_provenance(root: Path) -> ValidatorProvenance:
    """Check the installed official distribution's recorded VCS provenance.

    This is installation provenance, not an attestation against local tampering.
    The validator is invoked through this interpreter, never an unrelated PATH.
    """
    source = "https://github.com/agentskills/agentskills.git"
    result: ValidatorProvenance = {"verified": False, "source": source}
    try:
        baseline = require_object(
            json.loads((root / TRACK / "upstream-baseline.json").read_text()),
            context="upstream baseline",
        )
        expected = baseline["upstream_revision"]
        distribution = importlib.metadata.distribution("skills-ref")
        direct: object = json.loads(distribution.read_text("direct_url.json") or "null")
        if not is_object(direct):
            return result
        vcs = direct.get("vcs_info")
        if not is_object(vcs):
            return result
        revision = vcs.get("commit_id")
        result["revision"] = revision if isinstance(revision, str) else None
        result["verified"] = (
            isinstance(expected, str)
            and len(expected) == 40
            and all(character in "0123456789abcdef" for character in expected)
            and direct.get("url") == source
            and direct.get("subdirectory") == "skills-ref"
            and vcs.get("vcs") == "git"
            and revision == expected
        )
    except (OSError, ValueError, KeyError, TypeError, importlib.metadata.PackageNotFoundError):
        pass
    return result


def run_conformance(
    root: Path,
    *,
    validator: str | None = None,
    offline: bool = False,
    require_complete: bool = True,
) -> tuple[int, ConformanceReceipt]:
    root = root.resolve()
    skill = root / "skills/rca-investigation"
    provenance: ValidatorProvenance = (
        validator_provenance(root) if validator is None else {"verified": False}
    )
    command = (
        [sys.executable, "-I", "-m", "skills_ref.cli", "validate", str(skill)]
        if validator is None
        else [validator, "validate", str(skill)]
    )
    try:
        completed = subprocess.run(  # nosec B603 # pinned interpreter/module or explicit diagnostic executable; no shell
            command,
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        validator_code = completed.returncode
    except (OSError, subprocess.TimeoutExpired):
        validator_code = 127
    profile_errors = validate_profile(root, require_complete=require_complete)
    complete_errors = (
        profile_errors if require_complete else validate_profile(root, require_complete=True)
    )
    drift_code, drift = check_drift(root / TRACK / "upstream-baseline.json", offline=offline)
    local_pass = validator_code == 0 and not profile_errors
    current_pass = (
        not offline
        and local_pass
        and not complete_errors
        and provenance["verified"] is True
        and drift_code == 0
        and drift.get("current_conformance") is True
    )
    receipt: ConformanceReceipt = {
        "schema_version": "1.0",
        "checked_at": datetime.now(UTC).isoformat(),
        "runtime": {"python": platform.python_version(), "platform": platform.system()},
        "official_validator": {
            "command": (
                ["python", "-I", "-m", "skills_ref.cli", "validate", "skills/rca-investigation"]
                if validator is None
                else [validator, "validate", "skills/rca-investigation"]
            ),
            "provenance": provenance,
            "exit_code": validator_code,
            "passed": validator_code == 0,
        },
        "project_profile": {
            "passed": not profile_errors,
            "diagnostics": profile_errors,
            "complete": not complete_errors,
            "completion_diagnostics": complete_errors,
        },
        "upstream_drift": drift,
        "local_validation_passed": local_pass,
        "current_conformance": current_pass,
    }
    return (0 if current_pass or (offline and local_pass and drift_code == 0) else 1), receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--validator", help="Custom diagnostic validator; cannot certify current conformance"
    )
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--require-complete", action="store_true", default=True)
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
