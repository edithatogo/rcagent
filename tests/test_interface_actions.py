from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools.interface_actions import (
    build_audit_event,
    canonical_hash,
    dry_run_adapter,
    evaluate_synthetic_journeys,
    method_guidance,
    render_view,
    sanitize_export,
    transition_action,
    validate_approval,
    validate_communication_draft,
    validate_participation,
    validate_recommendation,
    validate_registry,
    validate_specialist_referral,
    verify_audit_chain,
)

ROOT = Path(__file__).parents[1]
HASH = "a" * 64


def registry() -> dict:
    return json.loads((ROOT / "evaluation/interfaces/registry.json").read_text())


def recommendation() -> dict:
    return {
        "recommendation_id": "rec-1", "evidence_ids": ["e-1"], "hazard": "handoff gap",
        "intended_mechanism": "reduce ambiguity", "strength": "system_control",
        "unintended_consequences": ["review burden"], "owner_role_id": "role-1",
        "dependencies": ["training"], "resources": ["time"], "due_date": "[Date]",
        "assurance_evidence": ["implementation receipt"], "process_measure": "completion rate",
        "outcome_measure": "handoff defects", "balancing_measure": "staff burden",
        "effectiveness_review_date": "[Date]", "residual_risk": "unknown",
        "status": "proposed", "effectiveness_state": "not_due",
        "effectiveness_evidence": "not_yet_assessed", "effectiveness_authority": "not_applicable",
    }


def view_context() -> dict:
    return {"citations": [], "model_involvement": {"used": False}, "limitations": ["synthetic"], "approval_receipt_ids": [], "outstanding_review_ids": ["r1"]}


def action_approval(action: dict) -> dict:
    return {
        "artefact_sha256": canonical_hash(action), "scope": "action", "authority_class": "human_organisational",
        "decision": "approved", "actor_class": "accountable_human", "conflict_declared": True,
        "actor_role_id": "reviewer", "author_role_id": "author",
        "issued_at": "2026-08-28T00:00:00Z", "expires_at": "2027-08-29T00:00:00Z",
    }


def canonical_record() -> dict:
    payload = {
        "schema_version": "1.1", "version": 1, "case_id": "syn-case-1", "state": "investigation",
        "jurisdiction": "synthetic", "privacy_mode": "fully_local", "authority": "synthetic-none",
        "statements": [], "events": [],
        "reviews": [{"review_id": "syn-review-1", "review_type": "other", "reviewer_role_ids": ["syn-role-1"], "status": "planned"}],
    }
    return {**payload, "source_sha256": canonical_hash(payload)}


def test_registry_passes_and_covers_original_templates() -> None:
    value = registry()
    assert validate_registry(value) == []
    schema = json.loads((ROOT / "conductor/schemas/interface-workspace.schema.json").read_text())
    assert list(Draft202012Validator(schema).iter_errors(value)) == []
    assert all(item["rights"] == "original_apache_2_0" for item in value["templates"])
    assert all(item["mutation"] is False for item in value["interfaces"])


def test_unsafe_legacy_templates_are_quarantined_from_supported_registry() -> None:
    audit = json.loads((ROOT / "evaluation/interfaces/legacy-template-audit.json").read_text())
    assert audit["status"] == "quarantined_legacy_not_supported"
    assert audit["admission"] is False
    supported_ids = {item["id"] for item in registry()["templates"]}
    assert not any("legacy" in identifier for identifier in supported_ids)
    lines = (ROOT / audit["manifest"]).read_text().splitlines()
    entries = {path: digest for digest, path in (line.split("  ", 1) for line in lines)}
    actual = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in (ROOT / audit["scope"]).rglob("*") if path.is_file()}
    assert entries == actual
    assert len(entries) == audit["manifest_entries"]


def test_registered_canonical_paths_resolve_against_safety_schema() -> None:
    safety = json.loads((ROOT / "conductor/schemas/safety-work.schema.json").read_text())
    roots = set(safety["properties"])
    statement_kinds = set(safety["$defs"]["statement"]["properties"]["kind"]["enum"])
    for template in registry()["templates"]:
        for field in template["fields"]:
            path = field["canonical_path"].removeprefix("$.")
            root = path.split("[")[0]
            assert root in roots
            if ".kind=" in path:
                assert path.split(".kind=", 1)[1] in statement_kinds


@pytest.mark.parametrize("value", [None, [], "bad"])
def test_registry_rejects_non_object(value: object) -> None:
    assert validate_registry(value) == ["registry must be an object"]


def test_registry_rejects_policy_journey_workflow_and_template_drift() -> None:
    value = registry()
    value["policy"]["external_actions"] = True
    value["journeys"] = []
    value["workflows"][0]["system_of_record"] = "local_shadow_registry"
    value["templates"][0]["disclaimers"] = []
    value["interfaces"][0]["operations"] = ["send"]
    value["interfaces"][0]["mutation"] = True
    value["participation"]["aboriginal_cultural_safety"] = "automated"
    errors = validate_registry(value)
    assert "policy.external_actions must be False" in errors
    assert "journeys must be a non-empty array" in errors
    assert "workflows[0].system_of_record must remain external" in errors
    assert "templates[0].disclaimers are incomplete" in errors
    assert "interfaces[0].operations are unsafe" in errors
    assert "interfaces[0] must be dry-run only" in errors
    assert "participation must remain prompt_and_human_checkpoint" in errors


def test_registry_fails_closed_on_malformed_array_members() -> None:
    value = registry()
    value["journeys"][0]["role"] = {}
    value["templates"][0]["audiences"] = [{}]
    value["interfaces"][0]["operations"] = [{}]
    errors = validate_registry(value)
    assert errors


def test_registry_rejects_each_structural_boundary() -> None:
    mutations = [
        lambda v: v.update(schema_version="2", extra=True),
        lambda v: v.update(policy=[]),
        lambda v: v["policy"].update(extra=True),
        lambda v: v.update(journeys=["bad"]),
        lambda v: v["journeys"][0].update(checkpoints=[]),
        lambda v: v.update(workflows=[]),
        lambda v: v.update(workflows=[{}]),
        lambda v: v["workflows"][1].update(id=v["workflows"][0]["id"], methods=[], steps=[]),
        lambda v: v.update(templates=[]),
        lambda v: v.update(templates=[{}]),
        lambda v: v["templates"][1].update(id=v["templates"][0]["id"], rights="unknown", fields=[], audiences=[]),
        lambda v: v["templates"][0]["fields"][0].update(canonical_path="$.unknown"),
        lambda v: v["templates"][0].update(fields=["bad"], disclaimers=[{}]),
        lambda v: v.update(interfaces=[]),
        lambda v: v.update(interfaces=[{}]),
        lambda v: v["interfaces"][1].update(id=v["interfaces"][0]["id"], status="live"),
        lambda v: v.update(participation=[]),
    ]
    for mutate in mutations:
        value = registry()
        mutate(value)
        assert validate_registry(value)


def test_method_guidance_never_forces_a_method() -> None:
    result = method_guidance(
        purpose="retrospective_incident", evidence_state="conflicting", capability=["SEIPS"],
        open_questions=["How did work conditions interact?"], evidence_signals=["human_factors"],
    )
    assert result["selected"] == ["SEIPS"]
    assert result["forced_method"] is False
    assert result["abstain"] is False
    unavailable = method_guidance(purpose="unknown", evidence_state="sparse", capability=[])
    assert unavailable["abstain"] is True


@pytest.mark.parametrize("operation", ["send", "lodge", "approve", "publish", "delete"])
def test_adapter_rejects_external_or_mutating_operations(operation: str) -> None:
    result = dry_run_adapter(
        {"operation": operation, "data_class": "synthetic", "dry_run": True, "approved_endpoint": None},
        registry(),
    )
    assert result["status"] == "rejected"
    assert result["external_action"] is False
    assert result["system_of_record_updated"] is False


def test_adapter_accepts_only_synthetic_dry_run_and_rejects_private_endpoint() -> None:
    request = {"operation": "export", "data_class": "synthetic", "dry_run": True, "approved_endpoint": None, "source_revision": HASH}
    assert dry_run_adapter(request, registry())["status"] == "dry_run_validated"
    request.update(data_class="governed_private", dry_run=False, approved_endpoint="https://internal")
    reasons = dry_run_adapter(request, registry())["reasons"]
    assert "data class is not admitted" in reasons
    assert "dry_run must be true" in reasons
    assert "endpoint use is unavailable" in reasons


def test_adapter_receipt_is_bound_to_request_and_registry() -> None:
    request = {"operation": "read", "data_class": "public", "dry_run": True, "approved_endpoint": None, "source_revision": HASH}
    first = dry_run_adapter(request, registry())
    changed = {**request, "operation": "export"}
    second = dry_run_adapter(changed, registry())
    assert first["status"] == "dry_run_validated"
    assert first["receipt_sha256"] != second["receipt_sha256"]
    assert first["executed"] is False


def test_adapter_rejects_credentials_and_unknown_fields() -> None:
    request = {
        "operation": "read", "data_class": "public", "dry_run": True,
        "approved_endpoint": None, "source_revision": HASH, "api_key": "not-a-real-key",
    }
    result = dry_run_adapter(request, registry())
    assert result["status"] == "rejected"
    assert "credential-like fields are forbidden" in result["reasons"]
    assert result["message_sent"] is False


def test_adapter_fails_closed_for_non_object_invalid_registry_and_active_request() -> None:
    bad_registry = registry()
    bad_registry["policy"]["external_actions"] = True
    result = dry_run_adapter([], bad_registry)
    assert "registry is invalid" in result["reasons"]
    result = dry_run_adapter({"operation": "read", "data_class": "public", "dry_run": True, "approved_endpoint": None, "source_revision": HASH, "note": "https://example.test"}, registry())
    assert "request contains unsafe content" in result["reasons"]


def test_communication_is_preparation_only_and_synthetic() -> None:
    draft = {
        "purpose": "questions", "status": "preparation_only", "recipient": "[Consumer B]",
        "delivery_channel": "none", "questions": ["What matters?"], "disagreement": [],
        "human_owner_role": "open_disclosure_lead",
    }
    assert validate_communication_draft(draft) == []
    draft.update(status="sent", delivery_channel="email", recipient="person@example.test")
    errors = validate_communication_draft(draft)
    assert "communication must remain preparation_only" in errors
    assert "delivery channel must be none" in errors
    assert "recipient must be synthetic or unresolved" in errors
    assert validate_communication_draft([]) == ["communication must be an object"]
    assert validate_communication_draft({})


@pytest.mark.parametrize(
    "unsafe",
    ["=WEBSERVICE('x')", "+cmd", "@SUM(A1)", "<script>alert(1)</script>", "https://example.test", "/Users/name/private"],
)
def test_export_quarantines_active_content_and_paths(unsafe: str) -> None:
    with pytest.raises(ValueError, match="unsafe active export content"):
        sanitize_export({"nested": [unsafe]})
    assert sanitize_export({"case": "[Case ID]", "count": 1}) == {"case": "[Case ID]", "count": 1}


def test_export_rejects_unsafe_keys_nonfinite_and_objects() -> None:
    for value in [{"api_key": "x"}, {"safe": float("nan")}, {"safe": object()}]:
        with pytest.raises(ValueError):
            sanitize_export(value)


def test_approval_is_hash_bound_and_agents_cannot_approve() -> None:
    approval = {
        "artefact_sha256": "b" * 64, "scope": "closure", "authority_class": "human_organisational",
        "decision": "approve", "actor_class": "agent_panel", "conflict_declared": True,
        "actor_role_id": "reviewer", "author_role_id": "author",
        "issued_at": "2026-08-29T00:00:00Z", "expires_at": "2027-08-29T00:00:00Z",
    }
    errors = validate_approval(approval, artefact_sha256=HASH, evaluated_at="2026-08-29T00:00:00Z")
    assert "approval is not bound to the exact artefact" in errors
    assert "actor class cannot provide accountable approval" in errors
    assert "decision is invalid" in errors


def test_approval_rejects_impossible_or_expired_timestamps() -> None:
    value = action_approval(recommendation())
    value["issued_at"] = "2026-99-99T00:00:00Z"
    assert "approval timestamps must be UTC ISO timestamps" in validate_approval(value, artefact_sha256=value["artefact_sha256"], evaluated_at="2026-08-29T00:00:00Z")
    value = action_approval(recommendation())
    assert "approval is not current at evaluation time" in validate_approval(value, artefact_sha256=value["artefact_sha256"], evaluated_at="2028-08-29T00:00:00Z")


def test_approval_rejects_all_authority_shape_failures() -> None:
    assert validate_approval([], artefact_sha256=HASH, evaluated_at="2026-08-29T00:00:00Z") == ["approval must be an object"]
    value = action_approval(recommendation())
    value.update(artefact_sha256="bad", scope="unknown", authority_class="human_policy", actor_role_id="same", author_role_id="same", conflict_declared=False)
    value["extra"] = True
    errors = validate_approval(value, artefact_sha256="bad", evaluated_at="bad")
    assert len(errors) >= 6


def test_audit_event_is_hash_chained_but_does_not_claim_persistence() -> None:
    first = build_audit_event(event={"kind": "draft_saved", "case": "[Case ID]"}, previous_sha256=None)
    second = build_audit_event(event={"kind": "review_returned"}, previous_sha256=first["event_sha256"])
    assert second["previous_sha256"] == first["event_sha256"]
    assert second["append_only_contract"] is True
    assert second["persisted"] is False
    assert verify_audit_chain([first, second]) == []
    second["previous_sha256"] = "b" * 64
    assert any("continuity" in error or "hash" in error for error in verify_audit_chain([first, second]))
    assert verify_audit_chain([]) == ["audit chain must be a non-empty array"]
    assert verify_audit_chain([{}])
    with pytest.raises(ValueError):
        build_audit_event(event={}, previous_sha256=None)
    with pytest.raises(ValueError):
        build_audit_event(event={"kind": "x"}, previous_sha256="bad")


def test_participation_preserves_withdrawal_and_cultural_authority_boundary() -> None:
    record = {
        "account_id": "syn-account-1", "account_sha256": "", "attribution": "generated_synthetic",
        "access": "local_restricted", "uncertainty": [], "disagreement": [], "correction_history": [],
        "contact_preference": "none", "consent_state": "withdrawn", "interpreter_need": "unknown",
        "accessibility_need": "unknown", "cultural_need": "expressed_synthetic",
        "cultural_authority_status": "complete", "export_allowed": True,
    }
    record["account_sha256"] = canonical_hash({key: value for key, value in record.items() if key != "account_sha256"})
    errors = validate_participation(record)
    assert "withdrawn or absent consent forbids contact export" in errors
    assert "cultural authority cannot be inferred or completed here" in errors


def test_participation_rejects_sensitive_nested_content_and_hash_drift() -> None:
    record = {
        "account_id": "syn-account-1", "account_sha256": HASH, "attribution": "generated_synthetic",
        "access": "local_restricted", "uncertainty": ["HF_TOKEN=secret"], "disagreement": [],
        "correction_history": [], "contact_preference": "none", "consent_state": "not_provided",
        "interpreter_need": "unknown", "accessibility_need": "unknown", "cultural_need": "not_expressed",
        "cultural_authority_status": "not_requested", "export_allowed": False,
    }
    errors = validate_participation(record)
    assert "participation contains unsafe or sensitive content" in errors
    assert "account hash is not bound to account and corrections" in errors
    assert validate_participation([]) == ["participation record must be an object"]
    assert validate_participation({})


def test_participation_hash_covers_disagreement_and_consent() -> None:
    record = {
        "account_id": "syn-account-1", "account_sha256": "", "attribution": "generated_synthetic",
        "access": "local_restricted", "uncertainty": [], "disagreement": [], "correction_history": [],
        "contact_preference": "none", "consent_state": "not_provided", "interpreter_need": "unknown",
        "accessibility_need": "unknown", "cultural_need": "not_expressed", "cultural_authority_status": "not_requested", "export_allowed": False,
    }
    record["account_sha256"] = canonical_hash({key: value for key, value in record.items() if key != "account_sha256"})
    assert validate_participation(record) == []
    record["disagreement"] = ["changed"]
    assert "account hash is not bound to account and corrections" in validate_participation(record)


def test_recommendation_contract_and_completion_do_not_infer_effectiveness() -> None:
    value = recommendation()
    assert validate_recommendation(value) == []
    approved = transition_action(value, status="approved", approval=action_approval(value))
    started = transition_action(approved, status="in_progress")
    result = transition_action(started, status="implemented", evidence=["e-implementation"])
    assert result["status"] == "implemented"
    assert result["effectiveness_state"] == "pending_evidence"
    assert result["effectiveness_inferred"] is False
    with pytest.raises(ValueError, match="transition is invalid"):
        transition_action(result, status="approved")


def test_recommendation_rejects_missing_and_invalid_states() -> None:
    value = recommendation()
    value["owner_role_id"] = ""
    value["status"] = "done"
    value["effectiveness_state"] = "proven"
    errors = validate_recommendation(value)
    assert "missing owner_role_id" in errors
    assert "status is invalid" in errors
    assert "effectiveness_state is invalid" in errors
    assert validate_recommendation([]) == ["recommendation must be an object"]


def test_effectiveness_requires_distinct_evidence_and_human_authority() -> None:
    value = recommendation()
    value.update(status="implemented", effectiveness_state="effective", effectiveness_evidence="", effectiveness_authority="agent_panel")
    errors = validate_recommendation(value)
    assert "effectiveness state requires outcome and balancing evidence" in errors
    assert "effectiveness state requires accountable human authority" in errors


def test_effectiveness_requires_exact_review_and_current_scoped_approval() -> None:
    value = recommendation()
    value["effectiveness_review_date"] = "2026-08-27T00:00:00Z"
    base_hash = canonical_hash({k: v for k, v in value.items() if k not in {"effectiveness_state", "effectiveness_evidence", "effectiveness_authority"}})
    records = [{"evidence_id": "ev-outcome", "kind": "outcome", "value": "improved"}, {"evidence_id": "ev-balancing", "kind": "balancing", "value": "no harm observed"}]
    review = {"recommendation_sha256": base_hash, "outcome_evidence_id": "ev-outcome", "outcome_evidence_sha256": canonical_hash(records[0]), "balancing_evidence_id": "ev-balancing", "balancing_evidence_sha256": canonical_hash(records[1]), "reviewed_at": "2026-08-28T00:00:00Z", "decision": "effective"}
    approval = {
        "artefact_sha256": canonical_hash(review), "scope": "effectiveness", "authority_class": "human_organisational",
        "decision": "approved", "actor_class": "accountable_human", "actor_role_id": "effectiveness-reviewer",
        "author_role_id": "action-owner", "conflict_declared": True,
        "issued_at": "2026-08-28T00:00:00Z", "expires_at": "2027-08-29T00:00:00Z",
    }
    value.update(effectiveness_state="effective", effectiveness_authority="human_organisational", effectiveness_evidence={"outcome_evidence_id": "ev-outcome", "balancing_evidence_id": "ev-balancing", "review_record_sha256": canonical_hash(review), "approval_sha256": canonical_hash(approval)})
    assert validate_recommendation(value, effectiveness_review=review, effectiveness_approval=approval, effectiveness_records=records) == []
    approval["scope"] = "action"
    assert "valid exact effectiveness approval is required" in validate_recommendation(value, effectiveness_review=review, effectiveness_approval=approval, effectiveness_records=records)
    review["reviewed_at"] = "2099-01-01T00:00:00Z"
    assert "effectiveness review cannot be future dated" in validate_recommendation(value, effectiveness_review=review, effectiveness_approval=approval, effectiveness_records=records)
    records[1]["kind"] = "outcome"
    assert "effectiveness evidence records are missing, mistyped or unbound" in validate_recommendation(value, effectiveness_review=review, effectiveness_approval=approval, effectiveness_records=records)


def test_closed_status_and_invalid_implementation_evidence_are_rejected() -> None:
    value = recommendation()
    value["status"] = "closed"
    assert "status is invalid" in validate_recommendation(value)
    value["status"] = "in_progress"
    with pytest.raises(ValueError, match="identifiers are invalid"):
        transition_action(value, status="implemented", evidence=[""])
    with pytest.raises(ValueError, match="action contract is invalid"):
        transition_action({"status": "proposed"}, status="approved")
    with pytest.raises(ValueError, match="action approval"):
        transition_action(recommendation(), status="approved")


def test_specialist_pathways_remain_separate_and_external() -> None:
    referral = {
        "pathway": "cultural_review", "merged_with_incident_finding": False,
        "status": "requested", "external_authority_verified": False,
    }
    assert validate_specialist_referral(referral) == []
    referral.update(merged_with_incident_finding=True, external_authority_verified=True)
    errors = validate_specialist_referral(referral)
    assert "specialist pathway must remain separate" in errors
    assert "repository cannot verify external authority" in errors
    assert validate_specialist_referral([]) == ["referral must be an object"]
    assert len(validate_specialist_referral({})) == 4


def test_audience_views_expose_limits_and_never_send() -> None:
    record = canonical_record()
    view = render_view(record, audience="consumer_family", data_class="generated_synthetic", view_context=view_context())
    assert "private_note" not in view
    assert "reviews" not in view
    assert view["external_action"] is False
    assert len(view["disclaimers"]) == 3


def test_view_minimises_by_audience_and_rejects_nested_active_content() -> None:
    record = canonical_record()
    consumer = render_view(record, audience="consumer_family", data_class="generated_synthetic", view_context=view_context())
    assert "evidence" not in consumer and "reviews" not in consumer
    record["statements"] = [{"statement_id": "syn-statement-1", "kind": "reported_account", "text": "=WEBSERVICE('x')", "provenance": {"source_id": "syn-source-1", "author_role_id": "syn-role-1", "recorded_at": "2026-08-29T00:00:00Z", "review_state": "unreviewed"}}]
    payload = {key: value for key, value in record.items() if key != "source_sha256"}
    record["source_sha256"] = canonical_hash(payload)
    with pytest.raises(ValueError, match="unsafe active export content"):
        render_view(record, audience="consumer_family", data_class="generated_synthetic", view_context=view_context())


def test_view_rejects_malformed_record_and_audience() -> None:
    with pytest.raises(ValueError, match="record must be an object"):
        render_view([], audience="auditor", data_class="generated_synthetic", view_context=view_context())
    with pytest.raises(ValueError, match="audience is invalid"):
        render_view({}, audience="public", data_class="generated_synthetic", view_context=view_context())
    value = canonical_record()
    with pytest.raises(ValueError, match="only generated_synthetic"):
        render_view(value, audience="auditor", data_class="private", view_context=view_context())
    with pytest.raises(ValueError, match="view context"):
        render_view(value, audience="auditor", data_class="generated_synthetic", view_context={})
    malformed = canonical_record()
    malformed["source_sha256"] = "bad"
    with pytest.raises(ValueError, match="hash is invalid"):
        render_view(malformed, audience="auditor", data_class="generated_synthetic", view_context=view_context())
    drifted = canonical_record()
    drifted["state"] = "closed"
    with pytest.raises(ValueError, match="hash does not match"):
        render_view(drifted, audience="auditor", data_class="generated_synthetic", view_context=view_context())


def test_synthetic_journey_evaluation_is_non_operational() -> None:
    scenarios = json.loads((ROOT / "evaluation/interfaces/scenarios.json").read_text())
    result = evaluate_synthetic_journeys(registry(), scenarios)
    assert len(result["cases"]) == 7
    assert all(item["passed"] for item in result["cases"])
    assert result["metrics"]["external_actions"] == 0
    assert "not human usability research" in result["limitations"][0]
    checked = json.loads((ROOT / "conductor/tracks/interfaces-templates-action-loop_20260731/evidence/synthetic-evaluation-20260829.json").read_text())
    assert result == checked


def test_synthetic_journey_evaluation_negative_controls() -> None:
    assert evaluate_synthetic_journeys(registry(), None)["cases"] == []
    scenarios = [{"id": "bad", "kind": "unknown", "payload": {}}, "malformed"]
    result = evaluate_synthetic_journeys(registry(), scenarios)
    assert result["cases"] == [{"id": "bad", "assertion": "invalid", "passed": False}]
