"""H3 structural boundaries; these checks do not execute an H4 consumer."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol, cast

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
SCHEMAS = ROOT / "evaluation/heaps"
FIXTURES = ROOT / "tests/fixtures/heaps/packet"
SPECIMENS: tuple[tuple[str, str], ...] = (
    ("heaps-profile", "base-profile"),
    ("packet-manifest", "base-manifest"),
    ("review-decision", "simulated-approved-decision"),
    ("status-receipt", "design-status"),
)


class SchemaValidator(Protocol):
    """Narrow the supported API, not the fixture's validity or payload type."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


def load_object(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    return require_object(value, context=str(path))


def specimen(name: str) -> JsonObject:
    return load_object(FIXTURES / f"{name}.json")


def member(value: JsonObject, key: str) -> JsonObject:
    return require_object(value.get(key), context=key)


def first_row(value: JsonObject, key: str) -> JsonObject:
    rows = value.get(key)
    if not is_array(rows) or not rows:
        raise ValueError(f"fixture requires a nonempty {key} array")
    return require_object(rows[0], context=key)


def errors(schema_name: str, value: JsonObject) -> list[ValidationError]:
    schema = load_object(SCHEMAS / f"{schema_name}.schema.json")
    # The upstream stub's deprecated overload is partially untyped. This
    # supported method accepts arbitrary objects and returns validation errors.
    validator = cast(SchemaValidator, Draft202012Validator(schema))
    return list(validator.iter_errors(value))


def has_error(observed: list[ValidationError], keyword: str, path: tuple[str | int, ...]) -> bool:
    return any(
        error.validator == keyword and tuple(error.absolute_path) == path for error in observed
    )


@pytest.mark.parametrize(("schema_name", "fixture_name"), SPECIMENS)
def test_standalone_schema_and_independent_positive_specimen(
    schema_name: str, fixture_name: str
) -> None:
    schema = load_object(SCHEMAS / f"{schema_name}.schema.json")
    Draft202012Validator.check_schema(schema)
    assert errors(schema_name, specimen(fixture_name)) == []


@pytest.mark.parametrize(("schema_name", "fixture_name"), SPECIMENS)
def test_closed_root_rejects_an_unrecognised_completion_claim(
    schema_name: str, fixture_name: str
) -> None:
    value = specimen(fixture_name)
    value["clinical_complete"] = True
    assert has_error(errors(schema_name, value), "additionalProperties", ())


@pytest.mark.parametrize(("schema_name", "fixture_name"), SPECIMENS)
@pytest.mark.parametrize(
    ("field", "forbidden"),
    [("data_class", "real_clinical"), ("privacy_mode", "public_remote")],
)
def test_all_companions_keep_the_synthetic_local_boundary(
    schema_name: str, fixture_name: str, field: str, forbidden: str
) -> None:
    value = specimen(fixture_name)
    value[field] = forbidden
    assert has_error(errors(schema_name, value), "const", (field,))


@pytest.mark.parametrize("field", ["fingerprint", "manifest_binding", "approval", "status_receipt"])
def test_profile_body_rejects_self_or_future_bindings(field: str) -> None:
    value = specimen("base-profile")
    value[field] = "invented-binding"
    assert has_error(errors("heaps-profile", value), "additionalProperties", ())


def test_case_binding_rejects_wrong_hash_domain_and_shadow_fields() -> None:
    value = specimen("base-profile")
    binding = member(value, "case_binding")
    binding["hash_domain"] = "sha256-raw-bytes-v1"
    binding["heaps_state"] = "complete"
    observed = errors("heaps-profile", value)
    assert has_error(observed, "const", ("case_binding", "hash_domain"))
    assert has_error(observed, "additionalProperties", ("case_binding",))


@pytest.mark.parametrize("invalid_id", ["Case-UPPER", "id:colon", "ab", "../case"])
def test_case_binding_uses_the_canonical_identifier_grammar(invalid_id: str) -> None:
    value = specimen("base-profile")
    member(value, "case_binding")["case_id"] = invalid_id
    assert has_error(errors("heaps-profile", value), "pattern", ("case_binding", "case_id"))


def test_chronology_rejects_a_workflow_event_reference() -> None:
    value = specimen("base-profile")
    member(first_row(value, "chronology"), "statement_ref")["kind"] = "event"
    assert has_error(
        errors("heaps-profile", value), "enum", ("chronology", 0, "statement_ref", "kind")
    )


def test_account_position_requires_reported_account_kind() -> None:
    value = specimen("base-profile")
    first_row(first_row(value, "participation"), "account_refs")["kind"] = "finding"
    assert has_error(
        errors("heaps-profile", value), "enum", ("participation", 0, "account_refs", 0, "kind")
    )


def test_incident_involvement_is_required_separately_from_responsibilities() -> None:
    value = specimen("base-profile")
    first_row(value, "roles").pop("incident_involvement")
    assert has_error(errors("heaps-profile", value), "required", ("roles", 0))


@pytest.mark.parametrize("state", ["unknown", "pending", "not_requested", "declined"])
def test_participation_states_preserve_distinct_missingness(state: str) -> None:
    value = specimen("base-profile")
    participant = first_row(value, "participation")
    participant.update(
        state=state,
        account_refs=[],
        response_refs=[],
        disagreement_refs=[],
        confirmation="not_requested",
        state_note="Explicit synthetic state; no agreement is inferred.",
        state_basis_refs=[],
    )
    assert errors("heaps-profile", value) == []
    participant.pop("state_note")
    assert has_error(errors("heaps-profile", value), "required", ("participation", 0))


def test_available_snapshot_requires_a_digest_and_explicit_version_field() -> None:
    value = specimen("base-profile")
    snapshot = first_row(value, "source_snapshots")
    snapshot["raw_sha256"] = None
    snapshot.pop("version")
    observed = errors("heaps-profile", value)
    assert has_error(observed, "type", ("source_snapshots", 0, "raw_sha256"))
    assert has_error(observed, "required", ("source_snapshots", 0))


@pytest.mark.parametrize("field", ["calendar_snapshot_id", "time_zone", "counting_convention"])
def test_specified_deadline_rejects_a_missing_declared_basis(field: str) -> None:
    value = specimen("base-profile")
    first_row(value, "deadlines")[field] = None
    assert has_error(errors("heaps-profile", value), "type", ("deadlines", 0, field))


def test_taxonomy_can_be_multiple_or_explicitly_unmapped() -> None:
    value = specimen("base-profile")
    assignment = first_row(value, "factor_assignments")
    assert assignment["state"] == "unmapped"
    assert errors("heaps-profile", value) == []
    assignment["categories"] = ["synthetic-a", "synthetic-b"]
    assert has_error(
        errors("heaps-profile", value), "maxItems", ("factor_assignments", 0, "categories")
    )
    assignment.update(
        state="mapped",
        taxonomy_id="synthetic-taxonomy",
        taxonomy_version="1",
        taxonomy_authority="original_synthetic",
    )
    assert errors("heaps-profile", value) == []


def test_no_official_template_conformity_state_exists() -> None:
    value = specimen("base-profile")
    member(value, "template_mapping")["state"] = "official_conformant"
    assert has_error(errors("heaps-profile", value), "enum", ("template_mapping", "state"))


def test_manifest_requires_supporting_inventory_and_rejects_path_traversal() -> None:
    value = specimen("base-manifest")
    components = member(value, "components")
    components.pop("supporting_artifacts")
    member(components, "case")["path"] = "../private/case.json"
    observed = errors("packet-manifest", value)
    assert has_error(observed, "required", ("components",))
    assert has_error(observed, "pattern", ("components", "case", "path"))


def test_raw_manifest_digest_cannot_be_a_prefixed_core_fingerprint() -> None:
    value = specimen("base-manifest")
    member(member(value, "components"), "case")["sha256"] = "sha256:" + "0" * 64
    assert has_error(errors("packet-manifest", value), "pattern", ("components", "case", "sha256"))


@pytest.mark.parametrize(
    ("field", "forbidden"),
    [
        ("scope", "communication"),
        ("authority_status", "verified"),
        ("substantive_approval", "approved"),
    ],
)
def test_draft_decision_cannot_claim_shared_scope_or_substantive_authority(
    field: str, forbidden: str
) -> None:
    value = specimen("simulated-approved-decision")
    value[field] = forbidden
    assert has_error(errors("review-decision", value), "const", (field,))


def test_draft_approval_requires_declared_reviewer_conflict_and_times() -> None:
    value = specimen("simulated-approved-decision")
    value.update(reviewer_role_ref=None, conflict_state="unresolved", expires_at=None)
    observed = errors("review-decision", value)
    assert has_error(observed, "type", ("reviewer_role_ref",))
    assert has_error(observed, "const", ("conflict_state",))
    assert has_error(observed, "type", ("expires_at",))


def test_timestamp_pattern_rejects_lexical_garbage_but_not_impossible_dates() -> None:
    value = specimen("simulated-approved-decision")
    value["issued_at"] = "not-a-time"
    assert errors("review-decision", value)
    value["issued_at"] = "2030-02-30T12:00:00Z"
    assert errors("review-decision", value) == []
    # H4's strict parser must reject this value; H3 makes no format-checker claim.


@pytest.mark.parametrize("state", ["empty", "all_abstain"])
def test_empty_and_all_abstain_statuses_cannot_be_reviewed_drafts(state: str) -> None:
    value = specimen("design-status")
    value["preparation"] = state
    value["counts"] = {
        "input_items": 0 if state == "empty" else 7,
        "usable_items": 0,
        "abstained_items": 0 if state == "empty" else 7,
    }
    assert errors("status-receipt", value) == []
    value["review"] = "synthetic_draft_reviewed"
    assert has_error(errors("status-receipt", value), "const", ("preparation",))


def test_source_check_requires_a_separate_scope_and_stale_review_is_explicit() -> None:
    value = specimen("design-status")
    value["source_check"] = "passed"
    assert has_error(errors("status-receipt", value), "enum", ("source_check_scope",))
    value["source_check_scope"] = "record_reference_integrity"
    value["review"] = "stale"
    assert errors("status-receipt", value) == []
    # This is structural acceptance of a declaration, not evidence of a check.


@pytest.mark.parametrize(
    ("field", "forbidden"),
    [
        ("submission", "submitted"),
        ("clinical_review", "complete"),
        ("actual_authority", "verified"),
    ],
)
def test_status_cannot_promote_synthetic_work_to_submission_or_clinical_completion(
    field: str, forbidden: str
) -> None:
    value = specimen("design-status")
    value[field] = forbidden
    assert has_error(errors("status-receipt", value), "const", (field,))


def test_schema_does_not_claim_reference_digest_or_reviewer_resolution() -> None:
    profile = specimen("base-profile")
    member(profile, "case_binding")["fingerprint"] = "sha256:" + "0" * 64
    member(first_row(profile, "chronology"), "statement_ref")["id"] = "syn-missing-statement"
    assert errors("heaps-profile", profile) == []
    decision = specimen("simulated-approved-decision")
    decision["reviewer_role_ref"] = dict(member(decision, "author_role_ref"))
    assert errors("review-decision", decision) == []
    # The future consumer must reject these semantic faults, not trust a schema pass.
