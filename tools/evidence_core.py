"""Validation and lifecycle contracts for canonical safety-work records."""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).parents[1] / "conductor/schemas/safety-work.schema.json"
CURRENT_SCHEMA_VERSION = "1.1"
TRANSITIONS = {
    "intake": {"triage", "withdrawn"},
    "triage": {"review", "withdrawn"},
    "review": {"investigation", "consultation", "approval", "withdrawn"},
    "investigation": {"consultation", "approval", "withdrawn"},
    "consultation": {"investigation", "approval", "withdrawn"},
    "approval": {"action", "investigation", "withdrawn"},
    "action": {"effectiveness_review", "withdrawn"},
    "effectiveness_review": {"action", "closed", "withdrawn"},
    "closed": {"reopened", "appeal"},
    "reopened": {"review", "investigation", "withdrawn"},
    "appeal": {"review", "closed", "withdrawn"},
    "withdrawn": {"reopened"},
}
NON_STATE_EVENTS = {"correction_recorded", "evidence_withdrawn", "appeal_note_recorded"}


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_record(record: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = [f"{'.'.join(map(str, error.absolute_path))}: {error.message}" for error in validator.iter_errors(record)]
    identifiers: list[str] = []
    collections = (
        ("roles", "role_id"),
        ("sources", "source_id"),
        ("artefacts", "artefact_id"),
        ("evidence", "evidence_id"),
        ("statements", "statement_id"),
        ("factors", "factor_id"),
        ("events", "event_id"),
        ("actions", "action_id"),
        ("reviews", "review_id"),
        ("outcomes", "outcome_id"),
        ("referrals", "referral_id"),
    )
    for collection, key in collections:
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
        source_id = provenance.get("source_id") if isinstance(provenance, dict) else None
        source_ids = {item.get("source_id") for item in record.get("sources", []) if isinstance(item, dict)}
        if record.get("schema_version") == CURRENT_SCHEMA_VERSION and source_id not in source_ids:
            errors.append(f"statements: unknown source_id {source_id!r}")
    for relationship in record.get("relationships", []):
        if not isinstance(relationship, dict):
            continue
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
        event_type = event.get("event_type")
        valid_non_state_event = from_state == to_state and event_type in NON_STATE_EVENTS
        if isinstance(from_state, str) and isinstance(to_state, str) and not (can_transition(from_state, to_state) or valid_non_state_event):
            errors.append(f"events: invalid transition {from_state!r} -> {to_state!r}")
        for evidence_id in event.get("evidence_ids", []):
            if evidence_id not in ids:
                errors.append(f"events: unknown evidence_id {evidence_id!r}")
    for action in record.get("actions", []):
        if not isinstance(action, dict):
            continue
        for key in ("recommendation_id", "owner_role_id"):
            if action.get(key) not in ids:
                errors.append(f"actions: unknown {key} {action.get(key)!r}")
    for collection, fields in (
        ("artefacts", ("source_id",)),
        ("evidence", ("source_id", "artefact_id")),
        ("factors", ("statement_id",)),
        ("reviews", ("reviewer_role_ids", "statement_ids")),
        ("outcomes", ("evidence_ids", "statement_id")),
    ):
        for item in record.get(collection, []):
            if not isinstance(item, dict):
                continue
            for key in fields:
                references = item.get(key)
                if references is None:
                    continue
                if not isinstance(references, list):
                    references = [references]
                for reference in references:
                    if reference not in ids:
                        errors.append(f"{collection}: unknown {key} {reference!r}")
    for statement in record.get("statements", []):
        if not isinstance(statement, dict):
            continue
        for superseded_id in statement.get("supersedes", []):
            if superseded_id not in ids:
                errors.append(f"statements: unknown supersedes {superseded_id!r}")
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


def canonical_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for fingerprints and receipts."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def fingerprint(value: Any) -> str:
    return f"sha256:{sha256(canonical_bytes(value)).hexdigest()}"


def redact_evidence(item: dict[str, Any], *, reason: str, actor_role_id: str, at: str) -> dict[str, Any]:
    """Create a non-destructive redacted view while retaining source integrity."""
    redacted = deepcopy(item)
    redacted["original_fingerprint"] = item.get("fingerprint") or fingerprint(item)
    redacted.pop("content", None)
    redacted["redacted"] = True
    redacted["custody_state"] = "redacted"
    redacted["redaction"] = {"reason": reason, "actor_role_id": actor_role_id, "at": at}
    return redacted


def append_audit_receipt(receipts: list[dict[str, Any]], event: dict[str, Any]) -> dict[str, Any]:
    """Append a hash-linked receipt without mutating earlier receipts."""
    previous = receipts[-1]["receipt_hash"] if receipts else None
    payload = {"sequence": len(receipts) + 1, "previous_hash": previous, "event": deepcopy(event)}
    receipt = {**payload, "receipt_hash": fingerprint(payload)}
    receipts.append(receipt)
    return receipt


def verify_audit_receipts(receipts: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    previous: str | None = None
    for index, receipt in enumerate(receipts):
        payload = {"sequence": index + 1, "previous_hash": previous, "event": receipt.get("event")}
        expected = fingerprint(payload)
        if receipt.get("sequence") != index + 1:
            errors.append(f"receipts[{index}]: invalid sequence")
        if receipt.get("previous_hash") != previous:
            errors.append(f"receipts[{index}]: invalid previous_hash")
        if receipt.get("receipt_hash") != expected:
            errors.append(f"receipts[{index}]: invalid receipt_hash")
        previous = receipt.get("receipt_hash")
    return errors


def migrate_record(record: dict[str, Any], target_version: str = CURRENT_SCHEMA_VERSION) -> dict[str, Any]:
    """Perform the only supported, additive and reversible 1.0 to 1.1 migration."""
    source_version = record.get("schema_version")
    if source_version == target_version:
        return deepcopy(record)
    if (source_version, target_version) != ("1.0", "1.1"):
        raise ValueError(f"unsupported migration {source_version!r} -> {target_version!r}")
    migrated = deepcopy(record)
    migrated["schema_version"] = "1.1"
    for collection in ("sources", "artefacts", "evidence", "factors", "reviews", "outcomes", "referrals"):
        migrated.setdefault(collection, [])
    migrated.setdefault("system_of_record", {"kind": "unverified", "external_case_id": record["case_id"], "reconciled_at": None})
    known_sources = {item.get("source_id") for item in migrated["sources"] if isinstance(item, dict)}
    for statement in migrated.get("statements", []):
        provenance = statement.get("provenance", {}) if isinstance(statement, dict) else {}
        source_id = provenance.get("source_id") if isinstance(provenance, dict) else None
        if isinstance(source_id, str) and source_id not in known_sources:
            migrated["sources"].append(
                {
                    "source_id": source_id,
                    "source_type": "other",
                    "title": "Migrated unresolved source reference",
                    "fingerprint": fingerprint({"legacy_source_id": source_id}),
                    "acquired_at": provenance.get("recorded_at"),
                    "authority": "unverified migration",
                    "screening_state": "unverified",
                }
            )
            known_sources.add(source_id)
    return migrated


def export_record(record: dict[str, Any], *, profile: str) -> dict[str, Any]:
    """Create bounded machine-readable views without changing the canonical record."""
    if profile not in {"governed", "public"}:
        raise ValueError(f"unsupported export profile {profile!r}")
    exported = canonical_round_trip(record)
    if profile == "public":
        exported["privacy_mode"] = "public_remote"
        exported.pop("confidentiality", None)
        for item in exported.get("evidence", []):
            item.pop("content", None)
            item["redacted"] = True
    exported["export_profile"] = profile
    exported["export_fingerprint"] = fingerprint(exported)
    return exported
