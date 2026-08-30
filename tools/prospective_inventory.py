"""Read-only planning inventory; no execution provenance or admission is asserted."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.evaluation_preflight import _bytes, _digest, _unique


def obj(properties: dict) -> dict:
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def identifier(prefix: str) -> dict:
    return {"type": "string", "pattern": f"^{prefix}-[a-z0-9-]+$", "maxLength": 64}


REF = obj(
    {
        "path": {"type": "string", "maxLength": 200},
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    }
)
SCHEMA = obj(
    {
        "schema_version": {"const": "1.0"},
        "kind": {"const": "prospective-study-plan"},
        "study_id": identifier("prospective"),
        "version": {"const": "0.1.0"},
        "state": {"const": "planning"},
        "data_class": {"const": "synthetic"},
        "repeats": {"type": "integer", "minimum": 1, "maximum": 10},
        "cases": {
            "type": "array",
            "minItems": 1,
            "maxItems": 50,
            "items": obj({"id": identifier("case"), "input": REF}),
        },
        "conditions": {
            "type": "array",
            "minItems": 1,
            "maxItems": 10,
            "items": obj(
                {"id": identifier("condition"), "execution_status": {"const": "unassigned"}}
            ),
        },
        "rubric": REF,
        "expected_slots": {
            "type": "array",
            "minItems": 1,
            "maxItems": 500,
            "uniqueItems": True,
            "items": {"type": "string", "maxLength": 150},
        },
    }
)
SUBMISSION = obj(
    {
        "schema_version": {"const": "1.0"},
        "purpose": {"const": "primary-observation"},
        "study_id": identifier("prospective"),
        "manifest_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "slot_id": {"type": "string", "maxLength": 150},
        "input_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "raw": REF,
        "normalized": REF,
        "normalization": obj(
            {
                "source_sha256": {"type": "string"},
                "target_sha256": {"type": "string"},
                "method": {"const": "identity-utf8-v1"},
            }
        ),
    }
)


def read_json(path: Path) -> tuple[Any, str]:
    data = _bytes(path.absolute())
    try:
        return json.loads(data, object_pairs_hook=_unique), hashlib.sha256(data).hexdigest()
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("invalid_json") from exc


def validate(value: Any, schema: dict) -> None:
    if not Draft202012Validator(schema).is_valid(value):
        raise ValueError("invalid_schema")


def artifact(root: Path, ref: dict) -> bytes:
    # Restricted relative paths; no parent components. Not a filesystem sandbox.
    path = ref["path"]
    if not re.fullmatch(r"[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*(?:\.[a-zA-Z0-9_-]+)?", path):
        raise ValueError("invalid_artifact_path")
    data = _bytes(root / path)
    if hashlib.sha256(data).hexdigest() != ref["sha256"]:
        raise ValueError("artifact_hash_mismatch")
    return data


def submission_reason(path: Path, plan: dict, pin: str, slot: str, input_pin: str) -> str:
    value, _ = read_json(path)
    if isinstance(value, dict) and value.get("purpose") == "contract-fixture":
        return "fixture_not_observation"
    validate(value, SUBMISSION)
    assert isinstance(value, dict)
    if (value["study_id"], value["manifest_sha256"], value["slot_id"], value["input_sha256"]) != (
        plan["study_id"],
        pin,
        slot,
        input_pin,
    ):
        return "identity_mismatch"
    raw, normalized = (
        artifact(path.parent, value["raw"]),
        artifact(path.parent, value["normalized"]),
    )
    try:
        raw.decode("utf-8")
        normalized.decode("utf-8")
    except UnicodeError:
        return "invalid_utf8"
    if (
        raw != normalized
        or value["normalization"]["source_sha256"] != value["raw"]["sha256"]
        or value["normalization"]["target_sha256"] != value["normalized"]["sha256"]
    ):
        return "normalization_mismatch"
    return "execution_provenance_unverified"


def inventory(manifest: Path, expected_sha256: str) -> dict:
    manifest = manifest.absolute()
    plan, pin = read_json(manifest)
    if not _digest(expected_sha256) or pin != expected_sha256:
        raise ValueError("manifest_pin_mismatch")
    validate(plan, SCHEMA)
    assert isinstance(plan, dict)
    if type(plan["repeats"]) is not int:
        raise ValueError("invalid_repeat_type")
    for prefix, values in (
        ("prospective", [plan["study_id"]]),
        ("case", [item["id"] for item in plan["cases"]]),
        ("condition", [item["id"] for item in plan["conditions"]]),
    ):
        if any(not re.fullmatch(prefix + r"-[a-z0-9-]+", value) for value in values):
            raise ValueError("invalid_identity")
    cases = {case["id"]: case for case in plan["cases"]}
    conditions = {condition["id"] for condition in plan["conditions"]}
    if len(cases) != len(plan["cases"]) or len(conditions) != len(plan["conditions"]):
        raise ValueError("duplicate_identity")
    expected = {
        f"{case}__{condition}__r{repeat}": case
        for case in cases
        for condition in conditions
        for repeat in range(1, plan["repeats"] + 1)
    }
    if set(expected) != set(plan["expected_slots"]):
        raise ValueError("denominator_mismatch")
    for case in cases.values():
        artifact(manifest.parent, case["input"])
    artifact(manifest.parent, plan["rubric"])
    submissions = manifest.parent / "submissions"
    if submissions.is_symlink() or not submissions.is_dir():
        raise ValueError("submissions_root_unavailable")
    entries = {}
    # Inspect one level only. Unknown entries are counted but never opened/named in output.
    for entry in submissions.iterdir():
        if (
            entry.name == ".gitkeep"
            and not entry.is_symlink()
            and entry.is_file()
            and entry.stat().st_size == 0
        ):
            continue
        if len(entries) >= 1000:
            raise ValueError("too_many_submissions")
        entries[entry.name] = entry
    rows = []
    for slot, case in sorted(expected.items()):
        entry = entries.get(slot)
        reason = "submission_missing"
        if entry is not None:
            try:
                reason = submission_reason(
                    entry / "receipt.json", plan, pin, slot, cases[case]["input"]["sha256"]
                )
            except ValueError as exc:
                reason = str(exc)
        rows.append(
            {
                "slot_id": slot,
                "disposition": "pending" if entry is None else "quarantined",
                "reason": reason,
            }
        )
    return {
        "schema_version": "1.0",
        "status": "planning_inventory",
        "study_id": plan["study_id"],
        "manifest_sha256": pin,
        "scope": "manifest-adjacent-submissions-only",
        "study_unlocked": False,
        "slots": rows,
        "counts": {
            "expected": len(rows),
            "pending": sum(r["disposition"] == "pending" for r in rows),
            "quarantined": sum(r["disposition"] == "quarantined" for r in rows),
            "unexpected": len(set(entries) - set(expected)),
            "admitted": 0,
        },
        "blockers": [
            "protocol_not_frozen",
            "execution_adapter_unassigned",
            "semantic_admission_not_implemented",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        result = inventory(args.manifest, args.expected_sha256)
    except (ValueError, OSError):
        print(json.dumps({"status": "inventory_failed", "study_unlocked": False}))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0  # inventory command success, never a study transition


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
