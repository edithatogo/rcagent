"""Validation and lifecycle contracts for canonical safety-work records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).parents[1] / "conductor/schemas/safety-work.schema.json"
TRANSITIONS = {
    "intake": {"triage", "withdrawn"},
    "triage": {"review", "withdrawn"},
    "review": {"investigation", "consultation", "approval", "withdrawn"},
    "investigation": {"consultation", "approval", "withdrawn"},
    "consultation": {"investigation", "approval", "withdrawn"},
    "approval": {"action", "investigation", "withdrawn"},
    "action": {"effectiveness_review", "withdrawn"},
    "effectiveness_review": {"action", "closed", "withdrawn"},
    "closed": {"reopened"},
    "reopened": {"review", "investigation", "withdrawn"},
    "withdrawn": {"reopened"},
}


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_record(record: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = [f"{'.'.join(map(str, error.absolute_path))}: {error.message}" for error in validator.iter_errors(record)]
    identifiers: list[str] = []
    for collection, key in (("roles", "role_id"), ("statements", "statement_id"), ("events", "event_id"), ("actions", "action_id")):
        identifiers.extend(
            item[key]
            for item in record.get(collection, [])
            if isinstance(item, dict) and isinstance(item.get(key), str)
        )
    ids = set(identifiers)
    for identifier in ids:
        if identifiers.count(identifier) > 1:
            errors.append(f"identifiers: duplicate {identifier!r}")

    role_ids = {
        item["role_id"]
        for item in record.get("roles", [])
        if isinstance(item, dict) and isinstance(item.get("role_id"), str)
    }
    for statement in record.get("statements", []):
        provenance = statement.get("provenance", {}) if isinstance(statement, dict) else {}
        author_id = provenance.get("author_role_id") if isinstance(provenance, dict) else None
        if author_id not in role_ids:
            errors.append(f"statements: unknown author_role_id {author_id!r}")
    for relationship in record.get("relationships", []):
        for key in ("from_id", "to_id"):
            if relationship.get(key) not in ids:
                errors.append(f"relationships: unknown {key} {relationship.get(key)!r}")
    for event in record.get("events", []):
        if not isinstance(event, dict):
            continue
        actor_id = event.get("actor_role_id")
        if actor_id not in role_ids:
            errors.append(f"events: unknown actor_role_id {actor_id!r}")
        from_state, to_state = event.get("from_state"), event.get("to_state")
        if isinstance(from_state, str) and isinstance(to_state, str) and not can_transition(from_state, to_state):
            errors.append(f"events: invalid transition {from_state!r} -> {to_state!r}")
    events = record.get("events", [])
    if events and isinstance(events[-1], dict) and record.get("state") != events[-1].get("to_state"):
        errors.append("state: does not match the final event to_state")
    return sorted(errors)


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in TRANSITIONS.get(from_state, set())


def canonical_round_trip(record: dict[str, Any]) -> dict[str, Any]:
    if errors := validate_record(record):
        raise ValueError("invalid safety-work record: " + "; ".join(errors))
    return json.loads(json.dumps(record, sort_keys=True, separators=(",", ":")))
