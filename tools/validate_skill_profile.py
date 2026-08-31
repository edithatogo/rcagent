"""Validate the complete repository Agent Skill conformance profile."""

from __future__ import annotations

import argparse
import json
import re
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
REQUIRED_MATRIX_IDS = {
    *(f"AS-SPEC-{number:03d}" for number in range(1, 9)),
    *(f"AS-GUIDE-{number:03d}" for number in range(1, 4)),
    "RCA-PORT-001",
    "RCA-SAFE-001",
    "RCA-DRIFT-001",
    "RCA-ADAPTER-001",
}
EXTENSION_STATES = {"supported", "experimental", "unsupported", "inapplicable", "decision_pending"}
REQUIRED_EXTENSIONS = {"compatibility", "metadata", "allowed-tools", "license"}


def _valid_evidence(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    try:
        resolved = (root / path).resolve()
        return resolved.is_relative_to(root) and resolved.is_file() and resolved.stat().st_size > 0
    except (OSError, ValueError):
        return False


def _validate_extensions(root: Path, document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict) or not isinstance(document.get("extensions"), list):
        return ["RCA-PROFILE-005: extensions document must contain an extensions array"]
    if document.get("schema_version") != "1.0" or document.get("states") != [
        "supported",
        "experimental",
        "unsupported",
        "inapplicable",
        "decision_pending",
    ]:
        errors.append("RCA-PROFILE-005: invalid extensions schema or declared states")
    fields: set[str] = set()
    for index, item in enumerate(document["extensions"]):
        location = f"extensions[{index}]"
        if not isinstance(item, dict) or any(
            not isinstance(item.get(key), str) or not item[key].strip()
            for key in ("field", "scope", "state", "fallback", "evidence")
        ):
            errors.append(f"RCA-PROFILE-005: {location}: required non-empty strings missing")
            continue
        if item["field"] in fields or item["state"] not in EXTENSION_STATES:
            errors.append(f"RCA-PROFILE-005: {location}: duplicate field or invalid state")
        fields.add(item["field"])
        evidence = Path(item["evidence"])
        if (
            evidence.is_absolute()
            or ".." in evidence.parts
            or not _valid_evidence(root, str(TRACK / evidence))
        ):
            errors.append(f"RCA-PROFILE-005: {location}: invalid extension evidence")
    if REQUIRED_EXTENSIONS - fields:
        errors.append("RCA-PROFILE-005: required extension coverage is missing")
    return errors


def validate_profile(root: Path, *, require_complete: bool = False) -> list[str]:
    root = root.resolve()
    errors = [
        diagnostic.render() for diagnostic in validate_skill(root / "skills/rca-investigation")
    ]

    paths = {
        "matrix": root / TRACK / "evidence/compliance-matrix.json",
        "extensions": root / TRACK / "extensions.json",
        "baseline": root / TRACK / "upstream-baseline.json",
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

    baseline = documents.get("baseline")
    revision = matrix.get("baseline_revision")
    if (
        matrix.get("schema_version") != "1.0"
        or not isinstance(revision, str)
        or re.fullmatch(r"[0-9a-f]{40}", revision) is None
        or not isinstance(baseline, dict)
        or revision != baseline.get("upstream_revision")
    ):
        errors.append("RCA-PROFILE-002: matrix revision must match the pinned upstream baseline")
    sources = baseline.get("sources") if isinstance(baseline, dict) else None
    if (
        not isinstance(sources, list)
        or not sources
        or any(not isinstance(source, str) or not source.strip() for source in sources)
    ):
        errors.append("RCA-PROFILE-002: upstream baseline requires non-empty source URLs")
        sources = []

    identifiers: set[str] = set()
    for index, item in enumerate(matrix["items"]):
        location = f"compliance-matrix.json:items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"RCA-PROFILE-002: {location}: item must be an object")
            continue
        missing = REQUIRED_MATRIX_FIELDS - set(item)
        if missing:
            errors.append(f"RCA-PROFILE-002: {location}: missing fields {sorted(missing)}")
            continue
        invalid_fields = [
            field
            for field in sorted(REQUIRED_MATRIX_FIELDS - {"evidence"})
            if not isinstance(item[field], str) or not item[field].strip()
        ]
        if invalid_fields:
            errors.append(
                f"RCA-PROFILE-002: {location}: non-empty strings required for {invalid_fields}"
            )
            continue
        identifier = item["id"]
        if identifier in identifiers:
            errors.append(f"RCA-PROFILE-002: {location}: invalid or duplicate id")
        identifiers.add(identifier)
        source = item["source"].split("#", 1)[0]
        if source not in sources and not _valid_evidence(root, source):
            errors.append(f"RCA-PROFILE-002: {location}: source is outside the recorded baseline")
        if item["result"] not in RESULTS:
            errors.append(f"RCA-PROFILE-002: {location}: invalid result")
        evidence = item["evidence"]
        if (item["result"] == "pass" or evidence is not None) and not _valid_evidence(
            root, evidence
        ):
            errors.append(
                f"RCA-PROFILE-003: {location}: evidence must be a non-empty repository file"
            )
        if item["applicability"] in {"decision_pending", "adapter_only"} and (
            not isinstance(item.get("omission_rationale"), str)
            or not item["omission_rationale"].strip()
        ):
            errors.append(f"RCA-PROFILE-002: {location}: omission rationale is required")
        if require_complete and item["result"] != "pass":
            errors.append(f"RCA-PROFILE-004: {identifier}: result is {item['result']}, not pass")

    missing_ids = REQUIRED_MATRIX_IDS - identifiers
    if missing_ids:
        errors.append(
            f"RCA-PROFILE-002: compliance matrix missing required ids {sorted(missing_ids)}"
        )
    if "extensions" in documents:
        errors.extend(_validate_extensions(root, documents["extensions"]))

    if "triggers" in documents:
        trigger_data = documents["triggers"]
        if not isinstance(trigger_data, dict) or not isinstance(trigger_data.get("cases"), list):
            errors.append("RCA-EVAL-001: trigger document must contain a cases array")
            trigger_data = {"cases": []}
        partitions = {
            case.get("partition")
            for case in trigger_data.get("cases", [])
            if isinstance(case, dict) and isinstance(case.get("partition"), str)
        }
        if not {"train", "held_out"}.issubset(partitions):
            errors.append("RCA-EVAL-001: trigger cases require train and held_out partitions")

    if "outputs" in documents:
        output_data = documents["outputs"]
        aggregation = output_data.get("aggregation") if isinstance(output_data, dict) else None
        if not isinstance(aggregation, dict) or aggregation.get("unavailable_is_pass") is not False:
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
