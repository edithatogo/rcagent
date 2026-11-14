"""Validation and lifecycle contracts for canonical safety-work records."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Literal, Protocol, TypedDict, cast, overload

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

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


class _RecordValidator(Protocol):
    """The supported non-deprecated part of jsonschema's validator interface."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


class _AuditFields(TypedDict):
    sequence: int
    previous_hash: str | None
    event: JsonObject


class AuditReceipt(_AuditFields):
    receipt_hash: str


class _PublicSummaryFields(TypedDict):
    schema_version: Literal["public-summary-1.0"]
    source_schema_version: str
    privacy_mode: Literal["public_remote"]
    state: str
    record_counts: dict[str, int]
    statement_kinds: dict[str, int]
    content_policy: Literal["metadata-only-no-record-text-or-identifiers"]
    distribution_authority: Literal["not-established-by-export"]
    export_profile: Literal["public"]


class PublicSummary(_PublicSummaryFields):
    export_fingerprint: str


def _text(value: object, *, context: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{context} must be text")
    return value


def load_schema() -> JsonObject:
    value: object = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema = require_object(value, context="safety-work schema")
    Draft202012Validator.check_schema(schema)
    return schema


COLLECTION_IDS = {
    "roles": "role_id",
    "sources": "source_id",
    "artefacts": "artefact_id",
    "evidence": "evidence_id",
    "statements": "statement_id",
    "factors": "factor_id",
    "events": "event_id",
    "actions": "action_id",
    "reviews": "review_id",
    "outcomes": "outcome_id",
    "referrals": "referral_id",
}
REFERENCE_TARGETS = {
    "artefacts": {"source_id": "sources"},
    "evidence": {"source_id": "sources", "artefact_id": "artefacts"},
    "factors": {"statement_id": "statements"},
    "events": {"actor_role_id": "roles", "evidence_ids": "evidence"},
    "actions": {
        "recommendation_id": "recommendations",
        "owner_role_id": "roles",
        "implementation_evidence_ids": "evidence",
    },
    "reviews": {"reviewer_role_ids": "roles", "statement_ids": "statements"},
    "outcomes": {"evidence_ids": "evidence", "statement_id": "statements"},
    "statements": {"supersedes": "statements"},
}


def _objects(value: object) -> list[JsonObject]:
    return object_rows(value)


def _reference_errors(
    item: Mapping[str, object], targets: dict[str, str], indexes: dict[str, set[str]], context: str
) -> list[str]:
    errors: list[str] = []
    for field, target in targets.items():
        if field not in item:
            continue  # Required fields are checked by JSON Schema.
        raw_value = item[field]
        values = raw_value if is_array(raw_value) else [raw_value]
        for value in values:
            if not isinstance(value, str) or value not in indexes[target]:
                errors.append(f"{context}: unknown {field} {value!r}")
    return errors


def _relationship_errors(
    relationship: Mapping[str, object], indexes: dict[str, set[str]], identifiers: set[str]
) -> list[str]:
    errors: list[str] = []
    source, target, relation = (
        relationship.get("from_id"),
        relationship.get("to_id"),
        relationship.get("relation"),
    )
    for field, value in (("from_id", source), ("to_id", target)):
        if not isinstance(value, str) or value not in identifiers:
            errors.append(f"relationships: unknown {field} {value!r}")
    if errors:
        return errors
    knowledge = (
        indexes["sources"]
        | indexes["artefacts"]
        | indexes["evidence"]
        | indexes["statements"]
        | indexes["factors"]
    )
    claims = indexes["statements"] | indexes["factors"]
    allowed = {
        "supports": (knowledge, claims),
        "contradicts": (knowledge, claims),
        "derived_from": (
            indexes["artefacts"] | indexes["evidence"] | claims | indexes["outcomes"],
            knowledge,
        ),
        "implements": (indexes["actions"], indexes["recommendations"]),
        "evaluates": (indexes["reviews"] | indexes["outcomes"], claims | indexes["actions"]),
        "relevant_to": (identifiers, identifiers),
    }
    if relation == "supersedes":
        same_kind = any(
            source in indexes[kind] and target in indexes[kind]
            for kind in COLLECTION_IDS
            if kind not in {"roles", "events"}
        )
        valid = same_kind and source != target
    elif isinstance(relation, str) and relation in allowed:
        from_ids, to_ids = allowed[relation]
        valid = source in from_ids and target in to_ids
    else:
        return []  # An unknown relation is already rejected by JSON Schema.
    if not valid:
        errors.append(
            f"relationships: invalid endpoint types for {relation!r}: {source!r} -> {target!r}"
        )
    return errors


def validate_record(record: Mapping[str, object]) -> list[str]:
    # Upstream's deprecated overload has an untyped instance parameter; bind
    # only the documented interface used here, without disabling diagnostics.
    validator = cast(
        "_RecordValidator", Draft202012Validator(load_schema(), format_checker=FormatChecker())
    )
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in validator.iter_errors(record)
    ]
    objects = {name: _objects(record.get(name)) for name in COLLECTION_IDS}
    indexes = {
        name: {
            identifier for item in objects[name] if isinstance((identifier := item.get(key)), str)
        }
        for name, key in COLLECTION_IDS.items()
    }
    all_identifiers = [
        identifier
        for name, key in COLLECTION_IDS.items()
        for item in objects[name]
        if isinstance((identifier := item.get(key)), str)
    ]
    identifiers = set(all_identifiers)
    for identifier in identifiers:
        if all_identifiers.count(identifier) > 1:
            errors.append(f"identifiers: duplicate {identifier!r}")
    indexes["recommendations"] = {
        identifier
        for item in objects["statements"]
        if item.get("kind") == "recommendation"
        and isinstance((identifier := item.get("statement_id")), str)
    }
    for name, targets in REFERENCE_TARGETS.items():
        for item in objects[name]:
            errors.extend(_reference_errors(item, targets, indexes, name))
    for statement in objects["statements"]:
        raw_provenance = statement.get("provenance")
        if is_object(raw_provenance):
            provenance = raw_provenance
            targets = {"author_role_id": "roles", "reviewer_role_id": "roles"}
            source_id = provenance.get("source_id")
            # Schema 1.0 may carry unresolved external source IDs for migration.
            # A registered ID of another kind is never an external source.
            if record.get("schema_version") == CURRENT_SCHEMA_VERSION or (
                isinstance(source_id, str) and source_id in identifiers
            ):
                targets["source_id"] = "sources"
            errors.extend(_reference_errors(provenance, targets, indexes, "statements"))
        supersedes = statement.get("supersedes", [])
        if is_array(supersedes) and statement.get("statement_id") in supersedes:
            errors.append("statements: a statement cannot supersede itself")
    for relationship in _objects(record.get("relationships")):
        errors.extend(_relationship_errors(relationship, indexes, identifiers))
    previous_to_state: str | None = None
    for event_index, event in enumerate(objects["events"]):
        from_state, to_state = event.get("from_state"), event.get("to_state")
        event_type = event.get("event_type")
        valid_non_state_event = (
            from_state == to_state
            and isinstance(event_type, str)
            and event_type in NON_STATE_EVENTS
        )
        if (
            isinstance(from_state, str)
            and isinstance(to_state, str)
            and not (can_transition(from_state, to_state) or valid_non_state_event)
        ):
            errors.append(f"events: invalid transition {from_state!r} -> {to_state!r}")
        if previous_to_state is not None and from_state != previous_to_state:
            errors.append(
                f"events[{event_index}]: discontinuous history; expected from_state {previous_to_state!r}, got {from_state!r}"
            )
        if isinstance(to_state, str):
            previous_to_state = to_state
    if objects["events"] and record.get("state") != objects["events"][-1].get("to_state"):
        errors.append("state: does not match the final event to_state")
    return sorted(errors)


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in TRANSITIONS.get(from_state, set())


def canonical_round_trip(record: Mapping[str, object]) -> JsonObject:
    if errors := validate_record(record):
        raise ValueError("invalid safety-work record: " + "; ".join(errors))
    value: object = json.loads(json.dumps(record, sort_keys=True, separators=(",", ":")))
    return require_object(value, context="safety-work record")


def canonical_bytes(value: object) -> bytes:
    """Return deterministic UTF-8 JSON bytes for fingerprints and receipts."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def fingerprint(value: object) -> str:
    return f"sha256:{sha256(canonical_bytes(value)).hexdigest()}"


def redact_evidence(
    item: Mapping[str, object], *, reason: str, actor_role_id: str, at: str
) -> JsonObject:
    """Create a non-destructive redacted view while retaining source integrity."""
    redacted = deepcopy(dict(item))
    redacted["original_fingerprint"] = item.get("fingerprint") or fingerprint(item)
    redacted.pop("content", None)
    redacted["redacted"] = True
    redacted["custody_state"] = "redacted"
    redacted["redaction"] = {"reason": reason, "actor_role_id": actor_role_id, "at": at}
    return redacted


def append_audit_receipt(receipts: list[AuditReceipt], event: Mapping[str, object]) -> AuditReceipt:
    """Append a hash-linked receipt without mutating earlier receipts."""
    previous = receipts[-1]["receipt_hash"] if receipts else None
    payload: _AuditFields = {
        "sequence": len(receipts) + 1,
        "previous_hash": previous,
        "event": deepcopy(dict(event)),
    }
    receipt: AuditReceipt = {**payload, "receipt_hash": fingerprint(payload)}
    receipts.append(receipt)
    return receipt


def verify_audit_receipts(receipts: Sequence[object]) -> list[str]:
    errors: list[str] = []
    previous: object = None
    for index, receipt in enumerate(receipts):
        if not is_object(receipt):
            errors.append(f"receipts[{index}]: receipt must be an object")
            previous = None
            continue
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


def migrate_record(
    record: Mapping[str, object], target_version: str = CURRENT_SCHEMA_VERSION
) -> JsonObject:
    """Perform the only supported, additive and reversible 1.0 to 1.1 migration."""
    source_version = record.get("schema_version")
    if source_version == target_version:
        return deepcopy(dict(record))
    if (source_version, target_version) != ("1.0", "1.1"):
        raise ValueError(f"unsupported migration {source_version!r} -> {target_version!r}")
    migrated = deepcopy(dict(record))
    migrated["schema_version"] = "1.1"
    for collection in (
        "sources",
        "artefacts",
        "evidence",
        "factors",
        "reviews",
        "outcomes",
        "referrals",
    ):
        migrated.setdefault(collection, [])
    migrated.setdefault(
        "system_of_record",
        {"kind": "unverified", "external_case_id": record["case_id"], "reconciled_at": None},
    )
    known_sources = {
        source_id
        for item in _objects(migrated["sources"])
        if isinstance((source_id := item.get("source_id")), str)
    }
    for statement in _objects(migrated.get("statements")):
        provenance = statement.get("provenance")
        if not is_object(provenance):
            continue
        source_id = provenance.get("source_id")
        if isinstance(source_id, str) and source_id not in known_sources:
            sources = migrated["sources"]
            if not is_array(sources):
                raise ValueError("migration sources must be an array")
            sources.append(
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


@overload
def export_record(record: Mapping[str, object], *, profile: Literal["public"]) -> PublicSummary: ...


@overload
def export_record(record: Mapping[str, object], *, profile: Literal["governed"]) -> JsonObject: ...


@overload
def export_record(record: Mapping[str, object], *, profile: str) -> JsonObject | PublicSummary: ...


def export_record(record: Mapping[str, object], *, profile: str) -> JsonObject | PublicSummary:
    """Export a governed record or a metadata-only summary of an already public record.

    Public summaries exclude identifiers, source hashes, dates and all free text.
    This helper neither de-identifies private records nor authorises distribution.
    Its public-summary schema is deliberately distinct from a case record.
    """
    if profile not in {"governed", "public"}:
        raise ValueError(f"unsupported export profile {profile!r}")
    validated = canonical_round_trip(record)
    if profile == "public":
        if validated["privacy_mode"] != "public_remote":
            raise ValueError(
                "public export requires an already public record; private-mode conversion is prohibited"
            )
        kinds: dict[str, int] = {}
        for statement in _objects(validated["statements"]):
            kind = _text(statement["kind"], context="statement kind")
            kinds[kind] = kinds.get(kind, 0) + 1
        summary: _PublicSummaryFields = {
            "schema_version": "public-summary-1.0",
            "source_schema_version": _text(
                validated["schema_version"], context="record schema version"
            ),
            "privacy_mode": "public_remote",
            "state": _text(validated["state"], context="record state"),
            "record_counts": {
                name: len(_objects(validated.get(name, []))) for name in COLLECTION_IDS
            },
            "statement_kinds": kinds,
            "content_policy": "metadata-only-no-record-text-or-identifiers",
            "distribution_authority": "not-established-by-export",
            "export_profile": "public",
        }
        return {**summary, "export_fingerprint": fingerprint(summary)}
    exported = validated
    exported["export_profile"] = profile
    exported["export_fingerprint"] = fingerprint(exported)
    return exported
