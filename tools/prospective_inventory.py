"""Read-only planning inventory; no execution provenance or admission is asserted."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Literal, Protocol, TypedDict, TypeGuard, cast

from jsonschema import Draft202012Validator

from tools import json_shapes
from tools.evaluation_preflight import _bytes, _digest, _unique


class _SchemaValidator(Protocol):
    def is_valid(self, _instance: object, /) -> bool: ...


class ArtifactReference(TypedDict):
    path: str
    sha256: str


class PlanningCase(TypedDict):
    id: str
    input: ArtifactReference


class PlanningCondition(TypedDict):
    id: str
    execution_status: str


class PlanningDocument(TypedDict):
    schema_version: str
    kind: str
    study_id: str
    version: str
    state: str
    data_class: str
    repeats: int
    cases: list[PlanningCase]
    conditions: list[PlanningCondition]
    rubric: ArtifactReference
    expected_slots: list[str]


class NormalizationDeclaration(TypedDict):
    source_sha256: str
    target_sha256: str
    method: str


class SubmissionDocument(TypedDict):
    schema_version: str
    purpose: str
    study_id: str
    manifest_sha256: str
    slot_id: str
    input_sha256: str
    raw: ArtifactReference
    normalized: ArtifactReference
    normalization: NormalizationDeclaration


class InventorySlot(TypedDict):
    slot_id: str
    disposition: Literal["pending", "quarantined"]
    reason: str


class InventoryCounts(TypedDict):
    expected: int
    pending: int
    quarantined: int
    unexpected: int
    admitted: Literal[0]


class InventoryResult(TypedDict):
    schema_version: Literal["1.0"]
    status: Literal["planning_inventory"]
    study_id: str
    manifest_sha256: str
    scope: Literal["manifest-adjacent-submissions-only"]
    study_unlocked: Literal[False]
    slots: list[InventorySlot]
    counts: InventoryCounts
    blockers: list[str]


def is_artifact_reference(value: object) -> TypeGuard[ArtifactReference]:
    """Check reference field types without claiming path or digest admission."""
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("path"), str)
        and isinstance(value.get("sha256"), str)
    )


def _is_strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _is_case(value: object) -> TypeGuard[PlanningCase]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("id"), str)
        and is_artifact_reference(value.get("input"))
    )


def _is_cases(value: object) -> TypeGuard[list[PlanningCase]]:
    return json_shapes.is_array(value) and all(_is_case(item) for item in value)


def _is_condition(value: object) -> TypeGuard[PlanningCondition]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("id"), str)
        and isinstance(value.get("execution_status"), str)
    )


def _is_conditions(value: object) -> TypeGuard[list[PlanningCondition]]:
    return json_shapes.is_array(value) and all(_is_condition(item) for item in value)


def _is_plan(value: object) -> TypeGuard[PlanningDocument]:
    return (
        json_shapes.is_object(value)
        and all(
            isinstance(value.get(key), str)
            for key in ("schema_version", "kind", "study_id", "version", "state", "data_class")
        )
        and type(value.get("repeats")) is int
        and _is_cases(value.get("cases"))
        and _is_conditions(value.get("conditions"))
        and is_artifact_reference(value.get("rubric"))
        and _is_strings(value.get("expected_slots"))
    )


def _is_normalization(value: object) -> TypeGuard[NormalizationDeclaration]:
    return json_shapes.is_object(value) and all(
        isinstance(value.get(key), str) for key in ("source_sha256", "target_sha256", "method")
    )


def _is_submission(value: object) -> TypeGuard[SubmissionDocument]:
    return (
        json_shapes.is_object(value)
        and all(
            isinstance(value.get(key), str)
            for key in (
                "schema_version",
                "purpose",
                "study_id",
                "manifest_sha256",
                "slot_id",
                "input_sha256",
            )
        )
        and is_artifact_reference(value.get("raw"))
        and is_artifact_reference(value.get("normalized"))
        and _is_normalization(value.get("normalization"))
    )


def obj(properties: json_shapes.JsonObject) -> json_shapes.JsonObject:
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def identifier(prefix: str) -> json_shapes.JsonObject:
    return {"type": "string", "pattern": f"^{prefix}-[a-z0-9-]+$", "maxLength": 64}


REF: json_shapes.JsonObject = obj(
    {
        "path": {"type": "string", "maxLength": 200},
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    }
)
SCHEMA: json_shapes.JsonObject = obj(
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
SUBMISSION: json_shapes.JsonObject = obj(
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


def read_json(path: Path) -> tuple[object, str]:
    data = _bytes(path.absolute())
    try:
        return json.loads(data, object_pairs_hook=_unique), hashlib.sha256(data).hexdigest()
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("invalid_json") from exc


def validate(value: object, schema: json_shapes.JsonObject) -> None:
    # Adapt jsonschema's object-validation method, whose deprecated overload has
    # incomplete annotations, without claiming any validity for the input value.
    validator = cast(_SchemaValidator, Draft202012Validator(schema))
    if not validator.is_valid(value):
        raise ValueError("invalid_schema")


def artifact(root: Path, ref: object) -> bytes:
    # Restricted relative paths; no parent components. Not a filesystem sandbox.
    if not json_shapes.is_object(ref):
        raise ValueError("invalid_artifact_path")
    path = ref.get("path")
    if not isinstance(path, str) or not re.fullmatch(
        r"[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*(?:\.[a-zA-Z0-9_-]+)?", path
    ):
        raise ValueError("invalid_artifact_path")
    data = _bytes(root / path)
    pin = ref.get("sha256")
    if not isinstance(pin, str) or hashlib.sha256(data).hexdigest() != pin:
        raise ValueError("artifact_hash_mismatch")
    return data


def submission_reason(
    path: Path, plan: PlanningDocument, pin: str, slot: str, input_pin: str
) -> str:
    value, _ = read_json(path)
    if json_shapes.is_object(value) and value.get("purpose") == "contract-fixture":
        return "fixture_not_observation"
    validate(value, SUBMISSION)
    if not _is_submission(value):
        raise ValueError("invalid_validated_object_type")
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


def inventory(manifest: Path, expected_sha256: object) -> InventoryResult:
    manifest = manifest.absolute()
    plan, pin = read_json(manifest)
    if not _digest(expected_sha256) or pin != expected_sha256:
        raise ValueError("manifest_pin_mismatch")
    validate(plan, SCHEMA)
    if not json_shapes.is_object(plan):
        raise ValueError("invalid_validated_object_type")
    if type(plan["repeats"]) is not int:
        raise ValueError("invalid_repeat_type")
    if not _is_plan(plan):
        raise ValueError("invalid_validated_object_type")
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
    entries: dict[str, Path] = {}
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
    rows: list[InventorySlot] = []
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
