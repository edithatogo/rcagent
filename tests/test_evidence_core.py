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


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda value: value["roles"].append(deepcopy(value["roles"][0])), "identifiers: duplicate 'role-reviewer'"),
        (lambda value: value["events"][0].update(actor_role_id="missing-role"), "events: unknown actor_role_id 'missing-role'"),
        (lambda value: value["events"][0].update(from_state="intake", to_state="closed"), "events: invalid transition 'intake' -> 'closed'"),
        (lambda value: value.update(state="closed"), "state: does not match the final event to_state"),
    ],
)
def test_semantic_integrity_checks(mutator: Any, expected: str) -> None:
    value = record()
    mutator(value)
    assert expected in validate_record(value)


def test_fingerprint_redaction_and_public_export_preserve_audit_meaning() -> None:
    value = record()
    item = value["evidence"][0]
    redacted = redact_evidence(item, reason="synthetic privacy rule", actor_role_id="role-reviewer", at="2026-08-29T02:00:00Z")
    assert "content" not in redacted
    assert redacted["original_fingerprint"] == item["fingerprint"]
    assert fingerprint({"a": 1, "b": 2}) == fingerprint({"b": 2, "a": 1})

    exported = export_record(value, profile="public")
    assert "content" not in exported["evidence"][0]
    assert exported["statements"][0]["kind"] == "observed_fact"
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
    for key in ("system_of_record", "sources", "artefacts", "evidence", "factors", "reviews", "outcomes", "referrals"):
        legacy.pop(key)
    legacy["events"][0].pop("evidence_ids")
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
