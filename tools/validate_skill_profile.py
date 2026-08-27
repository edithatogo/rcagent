"""Validate the complete repository Agent Skill conformance profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.validate_skill import validate_skill

TRACK = Path("conductor/tracks/agent-skills-living-conformance_20260731")
REQUIRED_MATRIX_FIELDS = {
    "id",
    "source",
    "requirement",
    "applicability",
    "implementation",
    "validation",
    "result",
    "evidence",
}
RESULTS = {"pass", "partial", "pending", "blocked", "fail"}


def validate_profile(root: Path, *, require_complete: bool = False) -> list[str]:
    root = root.resolve()
    errors = [
        diagnostic.render()
        for diagnostic in validate_skill(root / "skills/rca-investigation")
    ]

    paths = {
        "matrix": root / TRACK / "evidence/compliance-matrix.json",
        "extensions": root / TRACK / "extensions.json",
        "triggers": root / "evaluations/skills/rca-investigation/trigger-cases.json",
        "outputs": root / "evaluations/skills/rca-investigation/output-cases.json",
    }
    documents: dict[str, Any] = {}
    for label, path in paths.items():
        try:
            documents[label] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"RCA-PROFILE-001: {path.relative_to(root)}: {exc}")
    if "matrix" not in documents:
        return errors

    matrix = documents["matrix"]
    if not isinstance(matrix, dict) or not isinstance(matrix.get("items"), list):
        errors.append("RCA-PROFILE-002: compliance matrix must contain an items array")
        return errors

    identifiers: set[str] = set()
    for index, item in enumerate(matrix["items"]):
        location = f"compliance-matrix.json:items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"RCA-PROFILE-002: {location}: item must be an object")
            continue
        missing = REQUIRED_MATRIX_FIELDS - set(item)
        if missing:
            errors.append(
                f"RCA-PROFILE-002: {location}: missing fields {sorted(missing)}"
            )
            continue
        identifier = item["id"]
        if not isinstance(identifier, str) or identifier in identifiers:
            errors.append(f"RCA-PROFILE-002: {location}: invalid or duplicate id")
        identifiers.add(identifier)
        if item["result"] not in RESULTS:
            errors.append(f"RCA-PROFILE-002: {location}: invalid result")
        evidence = item["evidence"]
        if evidence is not None and (
            not isinstance(evidence, str) or not (root / evidence).is_file()
        ):
            errors.append(f"RCA-PROFILE-003: {location}: evidence path is missing")
        if (
            item["applicability"] in {"decision_pending", "adapter_only"}
            and not item.get("omission_rationale")
        ):
            errors.append(f"RCA-PROFILE-002: {location}: omission rationale is required")
        if require_complete and item["result"] != "pass":
            errors.append(
                f"RCA-PROFILE-004: {identifier}: result is {item['result']}, not pass"
            )

    if "triggers" in documents:
        trigger_data = documents["triggers"]
        partitions = {
            case.get("partition")
            for case in trigger_data.get("cases", [])
            if isinstance(case, dict)
        }
        if not {"train", "held_out"}.issubset(partitions):
            errors.append("RCA-EVAL-001: trigger cases require train and held_out partitions")

    if "outputs" in documents:
        output_data = documents["outputs"]
        aggregation = output_data.get("aggregation", {})
        if aggregation.get("unavailable_is_pass") is not False:
            errors.append("RCA-EVAL-002: unavailable output evaluation must not pass")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    errors = validate_profile(args.root, require_complete=args.require_complete)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Agent Skill conformance profile validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
