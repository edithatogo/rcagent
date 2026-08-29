"""Validate the bounded, synthetic-only Docling evaluation receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
EVALUATION = ROOT / "evaluation/multimodal/docling-synthetic-evaluation.json"
REQUIRED_CLASSES = {
    "born-digital",
    "scanned",
    "rotated",
    "low-quality",
    "multilingual",
    "handwritten",
    "hostile",
}


def load_evaluation(path: Path = EVALUATION) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("evaluation must be an object")
    return value


def validate_evaluation(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unsigned = {key: item for key, item in value.items() if key != "receipt_sha256"}
    digest = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if value.get("receipt_sha256") != digest:
        errors.append("receipt hash mismatch")
    boundary = value.get("execution_boundary", {})
    for key, expected in (
        ("network", "disabled during evaluation"),
        ("remote_code", "prohibited"),
        ("external_inference", "prohibited"),
        ("private_data", "prohibited"),
    ):
        if boundary.get(key) != expected:
            errors.append(f"execution_boundary.{key} must be {expected!r}")
    cases = value.get("cases", [])
    if not isinstance(cases, list):
        return errors + ["cases must be an array"]
    classes = {case.get("class") for case in cases if isinstance(case, dict)}
    if classes != REQUIRED_CLASSES:
        errors.append("cases must cover every required challenge class exactly")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(set(ids)):
        errors.append("case identifiers must be unique")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case must be an object")
            continue
        if case.get("state") not in {"measured_contract", "unsupported"}:
            errors.append(f"{case.get('id')}: invalid state")
        for field in ("source", "output", "transformations", "provenance_limit", "evidence"):
            if field not in case:
                errors.append(f"{case.get('id')}: missing {field}")
        output = case.get("output", {})
        if not isinstance(output, dict) or "region" not in output or "confidence" not in output:
            errors.append(f"{case.get('id')}: region and confidence state are required")
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "report"))
    args = parser.parse_args()
    value = load_evaluation()
    errors = validate_evaluation(value)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    if args.command == "validate":
        print("Docling synthetic evaluation validation passed.")
    else:
        print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
