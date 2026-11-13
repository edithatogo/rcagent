from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from tools.evidence_core import (
    append_audit_receipt,
    can_transition,
    canonical_round_trip,
    export_record,
    fingerprint,
    load_schema,
    migrate_record,
    redact_evidence,
    validate_record,
    verify_audit_receipts,
)

FIXTURE = Path(__file__).parent / "fixtures/safety-work/valid-case.json"
INVALID_FIXTURES = Path(__file__).parent / "fixtures/safety-work/invalid-cases.json"


def record() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_schema_and_round_trip() -> None:
    assert load_schema()["$defs"]["statement"]["properties"]["kind"]
    value = record()
    assert validate_record(value) == []
    assert canonical_round_trip(value) == value


def test_invalid_statement_kind_and_reference_fail() -> None:
    value = record()
    value["statements"][0]["kind"] = "truth"
    value["relationships"][0]["to_id"] = "missing-id"
    errors = validate_record(value)
    assert any("is not one of" in error for error in errors)
    assert "relationships: unknown to_id 'missing-id'" in errors
    with pytest.raises(ValueError, match="invalid safety-work record"):
        canonical_round_trip(value)


def test_lifecycle_is_explicit_and_fail_closed() -> None:
    assert can_transition("review", "investigation")
    assert can_transition("closed", "reopened")
    assert not can_transition("intake", "closed")
    assert not can_transition("unknown", "review")


def test_workflow_history_must_be_continuous() -> None:
    value = record()
    value["events"].append(
        {
            "event_id": "event-action-01",
            "event_type": "action_started",
            "occurred_at": "2026-08-29T02:00:00Z",
            "actor_role_id": "role-reviewer",
            "from_state": "approval",
            "to_state": "action",
            "authority": "fixture",
        }
    )
    value["state"] = "action"
    assert (
        "events[1]: discontinuous history; expected from_state 'investigation', got 'approval'"
        in validate_record(value)
    )


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        ("duplicate_role", "identifiers: duplicate 'role-reviewer'"),
        ("unknown_actor", "events: unknown actor_role_id 'missing-role'"),
        ("invalid_transition", "events: invalid transition 'intake' -> 'closed'"),
        ("different_final_state", "state: does not match the final event to_state"),
    ],
)
def test_semantic_integrity_checks(change: str, expected: str) -> None:
    value = record()
    if change == "duplicate_role":
        value["roles"].append(deepcopy(value["roles"][0]))
    elif change == "unknown_actor":
        value["events"][0].update(actor_role_id="missing-role")
    elif change == "invalid_transition":
        value["events"][0].update(from_state="intake", to_state="closed")
    else:
        assert change == "different_final_state"
        value["state"] = "closed"
    assert expected in validate_record(value)


def test_fingerprint_redaction_and_public_export_preserve_audit_meaning() -> None:
    value = record()
    item = value["evidence"][0]
    redacted = redact_evidence(
        item,
        reason="synthetic privacy rule",
        actor_role_id="role-reviewer",
        at="2026-08-29T02:00:00Z",
    )
    assert "content" not in redacted
    assert redacted["original_fingerprint"] == item["fingerprint"]
    assert redacted["custody_state"] == "redacted"
    assert fingerprint({"a": 1, "b": 2}) == fingerprint({"b": 2, "a": 1})

    with pytest.raises(ValueError, match="already public"):
        export_record(value, profile="public")
    value["privacy_mode"] = "public_remote"
    exported = export_record(value, profile="public")
    assert exported["schema_version"] == "public-summary-1.0"
    assert exported["statement_kinds"]["observed_fact"] == 1
    assert "evidence" not in exported
    assert "statements" not in exported
    assert exported["export_fingerprint"].startswith("sha256:")
    with pytest.raises(ValueError, match="unsupported export profile"):
        export_record(value, profile="secret")


def test_hash_linked_receipts_detect_tampering() -> None:
    receipts: list[dict[str, Any]] = []
    append_audit_receipt(receipts, {"event": "created", "case_id": "case-synthetic-01"})
    append_audit_receipt(receipts, {"event": "reviewed", "case_id": "case-synthetic-01"})
    assert verify_audit_receipts(receipts) == []
    receipts[0]["event"]["event"] = "tampered"
    assert any("invalid receipt_hash" in error for error in verify_audit_receipts(receipts))


def test_additive_migration_is_explicit_and_valid() -> None:
    legacy = record()
    legacy["schema_version"] = "1.0"
    for key in (
        "system_of_record",
        "sources",
        "artefacts",
        "evidence",
        "factors",
        "reviews",
        "outcomes",
        "referrals",
    ):
        legacy.pop(key)
    legacy["events"][0].pop("evidence_ids")
    assert validate_record(legacy) == []
    migrated = migrate_record(legacy)
    assert migrated["schema_version"] == "1.1"
    assert migrated["sources"][0]["screening_state"] == "unverified"
    assert validate_record(migrated) == []
    assert migrate_record(migrated) == migrated
    with pytest.raises(ValueError, match="unsupported migration"):
        migrate_record(migrated, "2.0")


def test_invalid_fixture_catalog_has_diagnostics_and_safe_recovery() -> None:
    catalog = json.loads(INVALID_FIXTURES.read_text(encoding="utf-8"))
    for case in catalog["cases"]:
        value = record()
        target: Any = value
        for segment in case["path"][:-1]:
            target = target[segment]
        key = case["path"][-1]
        if "copy_from" in case:
            source: Any = value
            for segment in case["copy_from"]:
                source = source[segment]
            if isinstance(key, int) and key == len(target):
                target.append(deepcopy(source))
            else:
                target[key] = deepcopy(source)
        else:
            target[key] = case["value"]
        assert case["expected"] in validate_record(value), case["id"]
        assert case["recovery"], case["id"]


def test_malformed_relationship_returns_diagnostics_not_exception() -> None:
    value = record()
    value["relationships"] = ["not-an-object"]
    assert any("is not of type 'object'" in error for error in validate_record(value))


def test_all_cross_reference_failures_are_reported() -> None:
    value = record()
    value["statements"][0]["provenance"]["author_role_id"] = "missing-role"
    value["events"][0]["evidence_ids"] = ["missing-evidence"]
    value["actions"] = [
        {
            "action_id": "action-01",
            "recommendation_id": "missing-recommendation",
            "owner_role_id": "missing-role",
            "status": "proposed",
            "effectiveness_state": "not_due",
        }
    ]
    value["artefacts"][0]["source_id"] = "missing-source"
    value["evidence"][0]["artefact_id"] = "missing-artefact"
    errors = validate_record(value)
    assert "statements: unknown author_role_id 'missing-role'" in errors
    assert "events: unknown evidence_ids 'missing-evidence'" in errors
    assert "actions: unknown recommendation_id 'missing-recommendation'" in errors
    assert "actions: unknown owner_role_id 'missing-role'" in errors
    assert "artefacts: unknown source_id 'missing-source'" in errors
    assert "evidence: unknown artefact_id 'missing-artefact'" in errors


def test_malformed_collections_remain_diagnostic_safe() -> None:
    value = record()
    value["events"] = ["bad-event"]
    value["actions"] = ["bad-action"]
    value["reviews"] = ["bad-review"]
    value["statements"] = ["bad-statement"]
    errors = validate_record(value)
    assert sum("is not of type 'object'" in error for error in errors) >= 4


def test_non_state_correction_and_optional_references_are_supported() -> None:
    value = record()
    value["events"][0].update(
        event_type="correction_recorded",
        from_state="investigation",
        to_state="investigation",
    )
    value["outcomes"][0].pop("statement_id")
    assert validate_record(value) == []


def test_redaction_without_existing_fingerprint_and_governed_export() -> None:
    item = {"evidence_id": "evidence-01", "content": "synthetic", "custody_state": "acquired"}
    redacted = redact_evidence(
        item, reason="fixture", actor_role_id="role-reviewer", at="2026-08-29T03:00:00Z"
    )
    assert redacted["original_fingerprint"] == fingerprint(item)
    governed = export_record(record(), profile="governed")
    assert governed["privacy_mode"] == "fully_local"
    assert governed["evidence"][0]["content"] == "Synthetic evidence only."


def test_audit_chain_reports_sequence_and_previous_hash_tampering() -> None:
    receipts: list[dict[str, Any]] = []
    append_audit_receipt(receipts, {"event": "created"})
    append_audit_receipt(receipts, {"event": "reviewed"})
    receipts[0]["sequence"] = 4
    receipts[1]["previous_hash"] = "sha256:" + "0" * 64
    errors = verify_audit_receipts(receipts)
    assert "receipts[0]: invalid sequence" in errors
    assert "receipts[1]: invalid previous_hash" in errors


def test_malformed_audit_receipt_returns_diagnostic() -> None:
    receipts: list[Any] = ["not-an-object"]
    assert verify_audit_receipts(receipts) == ["receipts[0]: receipt must be an object"]


@pytest.mark.parametrize(
    ("collection", "field", "replacement"),
    [
        ("artefacts", "source_id", "role-reviewer"),
        ("evidence", "source_id", "role-reviewer"),
        ("evidence", "artefact_id", "role-reviewer"),
        ("events", "evidence_ids", ["role-reviewer"]),
        ("events", "actor_role_id", "evidence-record-01"),
        ("factors", "statement_id", "role-reviewer"),
        ("reviews", "reviewer_role_ids", ["evidence-record-01"]),
        ("reviews", "statement_ids", ["role-reviewer"]),
        ("outcomes", "evidence_ids", ["role-reviewer"]),
        ("outcomes", "statement_id", "role-reviewer"),
        ("statements", "supersedes", ["role-reviewer"]),
    ],
)
def test_existing_wrong_kind_references_are_rejected(
    collection: str, field: str, replacement: str | list[str]
) -> None:
    value = record()
    value[collection][0][field] = replacement
    assert any(field in error for error in validate_record(value))


def test_action_requires_recommendation_and_typed_implementation_evidence() -> None:
    value = record()
    value["actions"] = [
        {
            "action_id": "action-01",
            "recommendation_id": "statement-observed-01",
            "owner_role_id": "evidence-record-01",
            "status": "proposed",
            "effectiveness_state": "not_due",
            "implementation_evidence_ids": ["role-reviewer"],
        }
    ]
    errors = validate_record(value)
    for field in ("recommendation_id", "owner_role_id", "implementation_evidence_ids"):
        assert any(field in error for error in errors)
    value["statements"][0]["kind"] = "recommendation"
    value["actions"][0]["owner_role_id"] = "role-reviewer"
    value["actions"][0]["implementation_evidence_ids"] = ["evidence-record-01"]
    assert validate_record(value) == []


@pytest.mark.parametrize(
    "relation", ["supports", "contradicts", "derived_from", "implements", "evaluates", "supersedes"]
)
def test_relationship_endpoint_types_are_enforced(relation: str) -> None:
    value = record()
    value["relationships"] = [
        {"from_id": "role-reviewer", "relation": relation, "to_id": "statement-observed-01"}
    ]
    assert any("endpoint types" in error for error in validate_record(value))


def test_typed_relationships_allow_implemented_recommendation_and_review() -> None:
    value = record()
    value["statements"][0]["kind"] = "recommendation"
    value["actions"] = [
        {
            "action_id": "action-01",
            "recommendation_id": "statement-observed-01",
            "owner_role_id": "role-reviewer",
            "status": "proposed",
            "effectiveness_state": "not_due",
        }
    ]
    value["relationships"] = [
        {"from_id": "action-01", "relation": "implements", "to_id": "statement-observed-01"},
        {"from_id": "review-huddle-01", "relation": "evaluates", "to_id": "action-01"},
        {
            "from_id": "statement-account-01",
            "relation": "derived_from",
            "to_id": "source-synthetic-02",
        },
        {
            "from_id": "statement-account-01",
            "relation": "supersedes",
            "to_id": "statement-observed-01",
        },
        {"from_id": "role-reviewer", "relation": "relevant_to", "to_id": "action-01"},
    ]
    assert validate_record(value) == []


def test_provenance_reviewer_must_be_a_role_and_supersession_cannot_be_reflexive() -> None:
    value = record()
    value["statements"][0]["provenance"]["reviewer_role_id"] = "source-synthetic-01"
    value["statements"][0]["supersedes"] = ["statement-observed-01"]
    assert "statements: unknown reviewer_role_id 'source-synthetic-01'" in validate_record(value)
    assert "statements: a statement cannot supersede itself" in validate_record(value)


@pytest.mark.parametrize(
    "collection", ["roles", "sources", "statements", "relationships", "events"]
)
def test_non_array_collections_return_errors(collection: str) -> None:
    value = record()
    value[collection] = None
    assert validate_record(value)


def test_unhashable_relationship_reference_remains_diagnostic() -> None:
    value = record()
    value["relationships"][0]["from_id"] = {"invalid": "object"}
    assert validate_record(value)


@pytest.mark.parametrize("mode", ["fully_local", "governed_hybrid", "air_gapped"])
def test_public_export_cannot_reclassify_private_modes(mode: str) -> None:
    value = record()
    value["privacy_mode"] = mode
    original = deepcopy(value)
    with pytest.raises(ValueError, match="private-mode conversion is prohibited"):
        export_record(value, profile="public")
    assert value == original


def test_public_export_omits_free_text_identifiers_dates_and_source_hashes() -> None:
    value = record()
    value["privacy_mode"] = "public_remote"
    value["statements"][0]["text"] = "SYNTHETIC-CONFIDENTIAL-CANARY"
    value["sources"][0]["title"] = "SYNTHETIC-SOURCE-CANARY"
    value["authority"] = "SYNTHETIC-AUTHORITY-CANARY"
    original = deepcopy(value)
    exported = export_record(value, profile="public")
    payload = json.dumps(exported)
    for forbidden in ("CANARY", "case-synthetic", "role-reviewer", "2026-08-29", "aaaaaaaa"):
        assert forbidden not in payload
    assert set(exported) == {
        "schema_version",
        "source_schema_version",
        "privacy_mode",
        "state",
        "record_counts",
        "statement_kinds",
        "content_policy",
        "distribution_authority",
        "export_profile",
        "export_fingerprint",
    }
    assert value == original


def test_legacy_provenance_cannot_disguise_an_existing_role_as_an_external_source() -> None:
    value = record()
    value["schema_version"] = "1.0"
    value["statements"][0]["provenance"]["source_id"] = "role-reviewer"
    assert "statements: unknown source_id 'role-reviewer'" in validate_record(value)
