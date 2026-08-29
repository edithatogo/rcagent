"""Client-neutral, synthetic-only interface and closed-loop action contracts."""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_VERSION = "1.0"
AUDIENCES = {"investigator", "reviewer", "consumer_family", "staff", "governance", "executive", "auditor"}
METHODS = {"RCA", "SEIPS", "AcciMap", "FRAM", "STPA", "bow_tie", "barrier_analysis", "FMEA"}
SPECIALIST_PATHWAYS = {
    "lookback", "cluster_review", "individual_worker", "cultural_review", "clinical_risk",
    "enterprise_risk", "quality_improvement", "medicolegal", "related_policy",
}
EXTERNAL_OPERATIONS = {"send", "lodge", "approve", "close_external", "notify", "publish"}
SAFE_ADAPTER_OPERATIONS = {"read", "import", "export", "reconcile"}
SECRET_FIELDS = {"token", "api_key", "client_secret", "password", "credential", "tenant_id", "site_id"}
CANONICAL_PATHS = {
    "$.evidence", "$.statements[*].uncertainty", "$.statements[*].kind=recommendation",
    "$.actions", "$.outcomes", "$.statements[*].kind=reported_account", "$.reviews",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SENSITIVE_VALUE_RE = re.compile(
    r"(?i)(?:\bMRN[- :]*\d+|\bemployee[- _]?id\b|(?:token|password|secret|api[_ -]?key)\s*[=:]|\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\+?61|0)\d{8,9}\b)"
)


def canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_registry(registry: object) -> list[str]:
    if not isinstance(registry, dict):
        return ["registry must be an object"]
    errors: list[str] = []
    required_top = {"schema_version", "policy", "journeys", "workflows", "templates", "interfaces", "participation"}
    if set(registry) != required_top:
        errors.append("registry fields are invalid")
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be 1.0")
    policy = registry.get("policy")
    required_policy = {
        "synthetic_only": True,
        "external_actions": False,
        "enterprise_mutation": False,
        "automated_approval": False,
        "effectiveness_inferred_from_completion": False,
        "organisation_branding": False,
    }
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
    else:
        if set(policy) != set(required_policy):
            errors.append("policy fields are invalid")
        for field, expected in required_policy.items():
            if policy.get(field) is not expected:
                errors.append(f"policy.{field} must be {expected!r}")
    journeys = registry.get("journeys")
    if not isinstance(journeys, list) or not journeys:
        errors.append("journeys must be a non-empty array")
    else:
        roles = [item.get("role") for item in journeys if isinstance(item, dict) and isinstance(item.get("role"), str)]
        covered = set(roles)
        if covered != AUDIENCES or len(roles) != len(covered):
            errors.append("journeys do not cover every required role")
        for index, journey in enumerate(journeys):
            if not isinstance(journey, dict) or set(journey) != {"role", "checkpoints", "failure_recovery", "accessibility"}:
                errors.append(f"journeys[{index}] fields are invalid")
                continue
            for field in ("checkpoints", "failure_recovery", "accessibility"):
                if not isinstance(journey.get(field), list) or not journey[field]:
                    errors.append(f"journeys[{index}].{field} must be non-empty")
    workflows = registry.get("workflows")
    if not isinstance(workflows, list) or not workflows:
        errors.append("workflows must be a non-empty array")
    else:
        workflow_ids: set[str] = set()
        for index, workflow in enumerate(workflows):
            prefix = f"workflows[{index}]"
            required = {"id", "purpose", "steps", "methods", "human_checkpoints", "system_of_record"}
            if not isinstance(workflow, dict) or set(workflow) != required:
                errors.append(f"{prefix} fields are invalid")
                continue
            identifier = workflow.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in workflow_ids:
                errors.append(f"{prefix}.id is invalid or duplicated")
            else:
                workflow_ids.add(identifier)
            methods = workflow.get("methods")
            if not isinstance(methods, list) or not methods or not all(isinstance(method, str) for method in methods) or not set(methods) <= METHODS:
                errors.append(f"{prefix}.methods are invalid")
            if workflow.get("system_of_record") != "external_approved_platform":
                errors.append(f"{prefix}.system_of_record must remain external")
            for field in ("steps", "human_checkpoints"):
                if not isinstance(workflow.get(field), list) or not workflow[field]:
                    errors.append(f"{prefix}.{field} must be non-empty")
    templates = registry.get("templates")
    if not isinstance(templates, list) or not templates:
        errors.append("templates must be a non-empty array")
    else:
        template_ids: set[str] = set()
        for index, template in enumerate(templates):
            prefix = f"templates[{index}]"
            required = {"id", "title", "rights", "fields", "audiences", "disclaimers"}
            if not isinstance(template, dict) or set(template) != required:
                errors.append(f"{prefix} fields are invalid")
                continue
            identifier = template.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in template_ids:
                errors.append(f"{prefix}.id is invalid or duplicated")
            else:
                template_ids.add(identifier)
            if template.get("rights") not in {"original_apache_2_0", "linked_only"}:
                errors.append(f"{prefix}.rights is invalid")
            audiences = template.get("audiences")
            if not isinstance(audiences, list) or not audiences or not all(isinstance(audience, str) for audience in audiences) or not set(audiences) <= AUDIENCES:
                errors.append(f"{prefix}.audiences are invalid")
            fields = template.get("fields")
            if not isinstance(fields, list) or not fields:
                errors.append(f"{prefix}.fields must be non-empty")
            else:
                for field_index, field in enumerate(fields):
                    if not isinstance(field, dict) or set(field) != {"name", "canonical_path", "provenance_required"}:
                        errors.append(f"{prefix}.fields[{field_index}] is invalid")
                    elif field.get("canonical_path") not in CANONICAL_PATHS:
                        errors.append(f"{prefix}.fields[{field_index}].canonical_path is invalid")
            disclaimers = template.get("disclaimers")
            required_disclaimers = {"clinical", "policy", "legal", "organisational", "external_action"}
            if not isinstance(disclaimers, list) or not all(isinstance(item, str) for item in disclaimers) or not required_disclaimers <= set(disclaimers):
                errors.append(f"{prefix}.disclaimers are incomplete")
    interfaces = registry.get("interfaces")
    if not isinstance(interfaces, list) or not interfaces:
        errors.append("interfaces must be a non-empty array")
    else:
        interface_ids: set[str] = set()
        for index, interface in enumerate(interfaces):
            required = {"id", "kind", "status", "operations", "mutation", "external_send", "replacement_path"}
            if not isinstance(interface, dict) or set(interface) != required:
                errors.append(f"interfaces[{index}] fields are invalid")
                continue
            operations = interface.get("operations")
            if not isinstance(operations, list) or not all(isinstance(operation, str) for operation in operations) or not set(operations) <= SAFE_ADAPTER_OPERATIONS:
                errors.append(f"interfaces[{index}].operations are unsafe")
            if interface.get("mutation") is not False or interface.get("external_send") is not False:
                errors.append(f"interfaces[{index}] must be dry-run only")
            if interface.get("status") not in {"contract_only", "unavailable"}:
                errors.append(f"interfaces[{index}].status is invalid")
            identifier = interface.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in interface_ids:
                errors.append(f"interfaces[{index}].id is invalid or duplicated")
            else:
                interface_ids.add(identifier)
    participation = registry.get("participation")
    required_participation = {
        "open_disclosure", "consumer_family", "staff_support", "procedural_fairness",
        "accessibility", "language_interpreter", "aboriginal_cultural_safety",
    }
    if not isinstance(participation, dict) or set(participation) != required_participation:
        errors.append("participation fields are incomplete")
    elif any(value != "prompt_and_human_checkpoint" for value in participation.values()):
        errors.append("participation must remain prompt_and_human_checkpoint")
    return sorted(errors)


def method_guidance(
    *, purpose: str, evidence_state: str, capability: list[str],
    open_questions: list[str] | None = None, evidence_signals: list[str] | None = None,
    method_budget: int = 2,
) -> dict[str, Any]:
    signal_map = {
        "human_factors": "SEIPS", "barrier_failure": "barrier_analysis",
        "cross_system": "AcciMap", "functional_variability": "FRAM",
        "control_failure": "STPA", "failure_mode": "FMEA",
    }
    permitted = {
        "retrospective_incident": {"SEIPS", "barrier_analysis", "AcciMap", "FRAM"},
        "proactive_risk": {"SEIPS", "STPA", "FMEA", "bow_tie"},
        "complex_cross_system": {"AcciMap", "FRAM", "STPA"},
    }.get(purpose, set())
    selected = [signal_map[signal] for signal in (evidence_signals or []) if signal in signal_map]
    selected = [method for method in selected if method in permitted and method in capability]
    if not open_questions or not evidence_signals or method_budget < 1:
        selected = []
    selected = selected[:method_budget]
    question = open_questions[0] if open_questions else "none declared"
    reasons = {method: f"responsive to declared evidence signals for {purpose}; question: {question}" for method in selected}
    return {
        "selected": selected,
        "reasons": reasons,
        "rejected": sorted(set(capability) - set(selected)),
        "stop_rule": "stop when declared questions are answered or evidence cannot discriminate further",
        "forced_method": False,
        "abstain": not selected,
        "limitations": ["Method selection is guidance, not a finding or organisational approval."],
    }


def dry_run_adapter(request: object, registry: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if validate_registry(registry):
        reasons.append("registry is invalid")
    if not isinstance(request, dict):
        request = {}
        reasons.append("request must be an object")
    allowed_request = {"operation", "data_class", "dry_run", "approved_endpoint", "source_revision"}
    unknown_fields = set(request) - allowed_request
    if unknown_fields:
        reasons.append("request contains unsupported or credential-like fields")
    if any(any(secret in field.casefold() for secret in SECRET_FIELDS) for field in request):
        reasons.append("credential-like fields are forbidden")
    operation = request.get("operation")
    if operation in EXTERNAL_OPERATIONS or operation not in SAFE_ADAPTER_OPERATIONS:
        reasons.append("operation is not permitted")
    if request.get("data_class") not in {"synthetic", "public"}:
        reasons.append("data class is not admitted")
    if request.get("dry_run") is not True:
        reasons.append("dry_run must be true")
    if request.get("approved_endpoint") is not None:
        reasons.append("endpoint use is unavailable")
    source_revision = request.get("source_revision")
    if not isinstance(source_revision, str) or not SHA256_RE.fullmatch(source_revision):
        reasons.append("source_revision must be an immutable sha256")
    safe_request: object = {}
    try:
        safe_request = sanitize_export(request)
    except ValueError:
        reasons.append("request contains unsafe content")
    receipt = {
        "status": "rejected" if reasons else "dry_run_validated",
        "reasons": sorted(reasons),
        "operation": operation if isinstance(operation, str) else None,
        "data_class": request.get("data_class"),
        "request_sha256": canonical_hash(safe_request),
        "registry_sha256": canonical_hash(registry),
        "source_revision": source_revision,
        "executed": False,
        "external_action": False,
        "enterprise_mutation": False,
        "message_sent": False,
        "system_of_record_updated": False,
    }
    receipt["receipt_sha256"] = canonical_hash(receipt)
    return receipt


def validate_communication_draft(draft: object) -> list[str]:
    if not isinstance(draft, dict):
        return ["communication must be an object"]
    allowed = {"purpose", "status", "recipient", "delivery_channel", "questions", "disagreement", "human_owner_role"}
    errors: list[str] = []
    if set(draft) != allowed:
        errors.append("communication fields are invalid")
    if draft.get("status") != "preparation_only":
        errors.append("communication must remain preparation_only")
    if draft.get("recipient") not in {"[Consumer B]", "[Family Representative]", "[Staff Member]", "unresolved"}:
        errors.append("recipient must be synthetic or unresolved")
    if draft.get("delivery_channel") != "none":
        errors.append("delivery channel must be none")
    if not isinstance(draft.get("human_owner_role"), str) or not draft.get("human_owner_role"):
        errors.append("human owner role is required")
    for field in ("questions", "disagreement"):
        if not isinstance(draft.get(field), list):
            errors.append(f"{field} must be an array")
    try:
        sanitize_export(draft)
    except ValueError:
        errors.append("communication contains unsafe or sensitive content")
    return sorted(errors)


def _unsafe_scalar(value: str) -> bool:
    normalised = unicodedata.normalize("NFKC", value).replace("\u200b", "")
    stripped = normalised.lstrip()
    return bool(
        stripped.startswith(("=", "+", "-", "@", "\t", "\r"))
        or re.search(r"(?i)<\s*script|javascript:|https?://|file:|data:|!\[[^]]*\]\(|\\\\|/(?:Users|home|var|tmp)/|[A-Z]:\\", normalised)
        or SENSITIVE_VALUE_RE.search(normalised)
    )


def sanitize_export(value: object) -> object:
    """Recursively preserve safe synthetic values and quarantine active content."""
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str) or _unsafe_scalar(key) or any(secret in key.casefold() for secret in SECRET_FIELDS):
                raise ValueError("unsafe export key")
            result[key] = sanitize_export(item)
        return result
    if isinstance(value, list):
        return [sanitize_export(item) for item in value]
    if isinstance(value, str):
        if _unsafe_scalar(value):
            raise ValueError("unsafe active export content")
        return value
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite export number")
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise ValueError("unsupported export value")


def _parse_utc(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        return None
    return parsed


def validate_approval(approval: object, *, artefact_sha256: str, evaluated_at: str) -> list[str]:
    if not isinstance(approval, dict):
        return ["approval must be an object"]
    required = {
        "artefact_sha256", "scope", "authority_class", "decision", "actor_class",
        "actor_role_id", "author_role_id", "conflict_declared", "issued_at", "expires_at",
    }
    errors = []
    if set(approval) != required:
        errors.append("approval fields are invalid")
    errors.extend(f"missing {field}" for field in sorted(required) if approval.get(field) in (None, ""))
    if not isinstance(artefact_sha256, str) or not SHA256_RE.fullmatch(artefact_sha256):
        errors.append("expected artefact hash is invalid")
    if not isinstance(approval.get("artefact_sha256"), str) or not SHA256_RE.fullmatch(approval["artefact_sha256"]):
        errors.append("approval artefact hash is invalid")
    if approval.get("artefact_sha256") != artefact_sha256:
        errors.append("approval is not bound to the exact artefact")
    if approval.get("actor_class") != "accountable_human":
        errors.append("actor class cannot provide accountable approval")
    if approval.get("authority_class") not in {"human_organisational", "human_clinical", "human_policy", "human_legal"}:
        errors.append("authority class is invalid")
    if approval.get("decision") not in {"approved", "rejected", "returned"}:
        errors.append("decision is invalid")
    if approval.get("scope") not in {"finding", "action", "effectiveness", "closure", "communication"}:
        errors.append("scope is invalid")
    if approval.get("actor_role_id") == approval.get("author_role_id"):
        errors.append("self approval is forbidden")
    issued = _parse_utc(approval.get("issued_at"))
    expires = _parse_utc(approval.get("expires_at"))
    evaluated = _parse_utc(evaluated_at)
    if issued is None or expires is None or evaluated is None:
        errors.append("approval timestamps must be UTC ISO timestamps")
    elif not issued <= evaluated < expires:
        errors.append("approval is not current at evaluation time")
    if approval.get("scope") == "effectiveness" and approval.get("authority_class") not in {"human_clinical", "human_organisational"}:
        errors.append("authority class is incompatible with effectiveness scope")
    if approval.get("conflict_declared") is not True:
        errors.append("conflict declaration is required")
    return sorted(errors)


def build_audit_event(*, event: object, previous_sha256: str | None) -> dict[str, Any]:
    """Create a deterministic append-only event envelope without claiming persistence."""
    if not isinstance(event, dict) or not event:
        raise ValueError("event must be a non-empty object")
    if previous_sha256 is not None and not SHA256_RE.fullmatch(previous_sha256):
        raise ValueError("previous_sha256 must be null or sha256")
    safe_event = sanitize_export(event)
    envelope: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "event": safe_event,
        "previous_sha256": previous_sha256,
        "append_only_contract": True,
        "persisted": False,
    }
    envelope["event_sha256"] = canonical_hash(envelope)
    return envelope


def verify_audit_chain(events: object) -> list[str]:
    if not isinstance(events, list) or not events:
        return ["audit chain must be a non-empty array"]
    errors: list[str] = []
    previous: str | None = None
    required = {"schema_version", "event", "previous_sha256", "append_only_contract", "persisted", "event_sha256"}
    for index, envelope in enumerate(events):
        if not isinstance(envelope, dict) or set(envelope) != required:
            errors.append(f"audit event {index} fields are invalid")
            continue
        claimed = envelope.get("event_sha256")
        body = {key: value for key, value in envelope.items() if key != "event_sha256"}
        if claimed != canonical_hash(body):
            errors.append(f"audit event {index} hash is invalid")
        if envelope.get("previous_sha256") != previous:
            errors.append(f"audit event {index} continuity is invalid")
        if envelope.get("append_only_contract") is not True or envelope.get("persisted") is not False:
            errors.append(f"audit event {index} flags are invalid")
        previous = claimed if isinstance(claimed, str) else None
    return sorted(errors)


def validate_participation(record: object) -> list[str]:
    if not isinstance(record, dict):
        return ["participation record must be an object"]
    required = {
        "account_id", "account_sha256", "attribution", "access", "uncertainty", "disagreement",
        "correction_history", "contact_preference", "consent_state", "interpreter_need",
        "accessibility_need", "cultural_need", "cultural_authority_status", "export_allowed",
    }
    errors = []
    if set(record) != required:
        errors.append("participation fields are invalid")
    errors.extend(f"missing {field}" for field in sorted(required) if field not in record)
    if not isinstance(record.get("account_sha256"), str) or not SHA256_RE.fullmatch(record["account_sha256"]):
        errors.append("account_sha256 is invalid")
    if record.get("attribution") != "generated_synthetic":
        errors.append("attribution must be generated_synthetic")
    if not isinstance(record.get("account_id"), str) or not re.fullmatch(r"syn-[a-z0-9-]+", record["account_id"]):
        errors.append("account_id must be an opaque synthetic identifier")
    if record.get("consent_state") not in {"provided_synthetic", "withdrawn", "not_provided"}:
        errors.append("consent state is invalid")
    if record.get("contact_preference") not in {"none", "human_contact_requested_synthetic"}:
        errors.append("contact preference is invalid")
    if record.get("access") != "local_restricted":
        errors.append("access must be local_restricted")
    if record.get("consent_state") in {"withdrawn", "not_provided"} and record.get("export_allowed") is not False:
        errors.append("withdrawn or absent consent forbids contact export")
    if record.get("cultural_authority_status") not in {"not_requested", "pending_human_referral", "declined", "external_only"}:
        errors.append("cultural authority cannot be inferred or completed here")
    if record.get("cultural_need") not in {"not_expressed", "expressed_synthetic", "declined_to_record"}:
        errors.append("cultural need must not be inferred")
    expected_account_hash = canonical_hash({key: value for key, value in record.items() if key != "account_sha256"})
    if record.get("account_sha256") != expected_account_hash:
        errors.append("account hash is not bound to account and corrections")
    try:
        sanitize_export(record)
    except ValueError:
        errors.append("participation contains unsafe or sensitive content")
    return sorted(errors)


def validate_recommendation(
    recommendation: object, *, effectiveness_review: object | None = None,
    effectiveness_approval: object | None = None, effectiveness_records: object | None = None,
    evaluated_at: str = "2026-08-29T00:00:00Z",
) -> list[str]:
    if not isinstance(recommendation, dict):
        return ["recommendation must be an object"]
    required = {
        "recommendation_id", "evidence_ids", "hazard", "intended_mechanism", "strength",
        "unintended_consequences", "owner_role_id", "dependencies", "resources", "due_date",
        "assurance_evidence", "process_measure", "outcome_measure", "balancing_measure",
        "effectiveness_review_date", "residual_risk", "status", "effectiveness_state",
        "effectiveness_evidence", "effectiveness_authority",
    }
    errors = [f"missing {field}" for field in sorted(required) if recommendation.get(field) in (None, "", [])]
    if recommendation.get("status") not in {"proposed", "approved", "in_progress", "implemented"}:
        errors.append("status is invalid")
    if recommendation.get("effectiveness_state") not in {"not_due", "pending_evidence", "effective", "partly_effective", "ineffective", "harm_detected"}:
        errors.append("effectiveness_state is invalid")
    if recommendation.get("effectiveness_state") in {"effective", "partly_effective", "ineffective", "harm_detected"}:
        effectiveness = recommendation.get("effectiveness_evidence")
        required_effectiveness = {"outcome_evidence_id", "balancing_evidence_id", "review_record_sha256", "approval_sha256"}
        if not isinstance(effectiveness, dict) or set(effectiveness) != required_effectiveness or not all(
            isinstance(effectiveness.get(field), str) and effectiveness[field] and effectiveness[field] != "not_yet_assessed"
            for field in required_effectiveness
        ):
            errors.append("effectiveness state requires outcome and balancing evidence")
        elif not all(SHA256_RE.fullmatch(effectiveness[field]) for field in ("review_record_sha256", "approval_sha256")):
            errors.append("effectiveness evidence hashes are invalid")
        elif effectiveness["outcome_evidence_id"] == effectiveness["balancing_evidence_id"]:
            errors.append("outcome and balancing evidence must be distinct")
        if not isinstance(effectiveness_review, dict) or set(effectiveness_review) != {
            "recommendation_sha256", "outcome_evidence_id", "outcome_evidence_sha256",
            "balancing_evidence_id", "balancing_evidence_sha256", "reviewed_at", "decision",
        }:
            errors.append("exact effectiveness review record is required")
        elif isinstance(effectiveness, dict):
            if canonical_hash(effectiveness_review) != effectiveness.get("review_record_sha256"):
                errors.append("effectiveness review hash does not match")
            if effectiveness_review.get("recommendation_sha256") != canonical_hash({k: v for k, v in recommendation.items() if k not in {"effectiveness_state", "effectiveness_evidence", "effectiveness_authority"}}):
                errors.append("effectiveness review is not bound to recommendation")
            if effectiveness_review.get("outcome_evidence_id") != effectiveness.get("outcome_evidence_id") or effectiveness_review.get("balancing_evidence_id") != effectiveness.get("balancing_evidence_id"):
                errors.append("effectiveness review evidence IDs do not match")
            admitted: dict[str, dict[str, object]] = {}
            if isinstance(effectiveness_records, list):
                for record in effectiveness_records:
                    if isinstance(record, dict) and isinstance(record.get("evidence_id"), str):
                        admitted[record["evidence_id"]] = record
            outcome_record = admitted.get(effectiveness["outcome_evidence_id"])
            balancing_record = admitted.get(effectiveness["balancing_evidence_id"])
            if (
                not outcome_record or outcome_record.get("kind") != "outcome"
                or not balancing_record or balancing_record.get("kind") != "balancing"
                or effectiveness_review.get("outcome_evidence_sha256") != canonical_hash(outcome_record)
                or effectiveness_review.get("balancing_evidence_sha256") != canonical_hash(balancing_record)
            ):
                errors.append("effectiveness evidence records are missing, mistyped or unbound")
            if effectiveness_review.get("decision") != recommendation.get("effectiveness_state"):
                errors.append("effectiveness review decision does not match state")
            if _parse_utc(effectiveness_review.get("reviewed_at")) is None:
                errors.append("effectiveness review timestamp is invalid")
            reviewed = _parse_utc(effectiveness_review.get("reviewed_at"))
            evaluated = _parse_utc(evaluated_at)
            due = _parse_utc(recommendation.get("effectiveness_review_date"))
            approval_issued = _parse_utc(effectiveness_approval.get("issued_at")) if isinstance(effectiveness_approval, dict) else None
            if reviewed is not None and evaluated is not None and reviewed > evaluated:
                errors.append("effectiveness review cannot be future dated")
            if reviewed is not None and due is not None and reviewed < due:
                errors.append("effectiveness review occurred before its due date")
            if due is None:
                errors.append("effectiveness review date is invalid")
            if reviewed is not None and approval_issued is not None and approval_issued < reviewed:
                errors.append("effectiveness approval predates review")
            approval_errors = validate_approval(
                effectiveness_approval, artefact_sha256=canonical_hash(effectiveness_review), evaluated_at=evaluated_at,
            )
            if (
                approval_errors
                or not isinstance(effectiveness_approval, dict)
                or effectiveness_approval.get("scope") != "effectiveness"
                or effectiveness_approval.get("decision") != "approved"
                or effectiveness.get("approval_sha256") != canonical_hash(effectiveness_approval)
            ):
                errors.append("valid exact effectiveness approval is required")
        if recommendation.get("effectiveness_authority") not in {
            "human_clinical", "human_organisational", "human_policy",
        }:
            errors.append("effectiveness state requires accountable human authority")
    return sorted(errors)


def transition_action(
    action: dict[str, Any], *, status: str, evidence: list[str] | None = None,
    approval: object | None = None, evaluated_at: str = "2026-08-29T00:00:00Z",
) -> dict[str, Any]:
    allowed = {
        "proposed": {"approved", "withdrawn"}, "approved": {"in_progress", "withdrawn"},
        "in_progress": {"implemented", "withdrawn"}, "implemented": set(), "withdrawn": set(),
    }
    current = action.get("status")
    if current not in allowed or status not in allowed[current]:
        raise ValueError("action status transition is invalid")
    if validate_recommendation(action):
        raise ValueError("action contract is invalid")
    result = deepcopy(action)
    if status == "approved":
        approval_errors = validate_approval(approval, artefact_sha256=canonical_hash(action), evaluated_at=evaluated_at)
        if approval_errors or not isinstance(approval, dict) or approval.get("scope") != "action" or approval.get("decision") != "approved":
            raise ValueError("valid exact action approval is required")
        result["action_approval_sha256"] = canonical_hash(approval)
    if status == "implemented" and not evidence:
        raise ValueError("implementation evidence is required")
    if evidence is not None:
        if not all(isinstance(item, str) and re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,127}", item) for item in evidence):
            raise ValueError("implementation evidence identifiers are invalid")
        try:
            sanitize_export(evidence)
        except ValueError as exc:
            raise ValueError("implementation evidence identifiers are unsafe") from exc
    result["status"] = status
    if status == "implemented" and result.get("effectiveness_state") == "not_due":
        result["effectiveness_state"] = "pending_evidence"
    if evidence is not None:
        result["assurance_evidence"] = list(evidence)
    result["effectiveness_inferred"] = False
    result["receipt_sha256"] = canonical_hash(result)
    return result


def validate_specialist_referral(referral: object) -> list[str]:
    if not isinstance(referral, dict):
        return ["referral must be an object"]
    errors: list[str] = []
    if referral.get("pathway") not in SPECIALIST_PATHWAYS:
        errors.append("pathway is invalid")
    if referral.get("merged_with_incident_finding") is not False:
        errors.append("specialist pathway must remain separate")
    if referral.get("status") not in {"proposed", "requested", "declined_local", "reported_unverified"}:
        errors.append("referral status is invalid")
    if referral.get("external_authority_verified") is not False:
        errors.append("repository cannot verify external authority")
    return sorted(errors)


def render_view(record: object, *, audience: str, data_class: str, view_context: object) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    if audience not in AUDIENCES:
        raise ValueError("audience is invalid")
    if data_class != "generated_synthetic":
        raise ValueError("only generated_synthetic records are admitted")
    required_source = {"schema_version", "version", "case_id", "state", "privacy_mode", "source_sha256"}
    if not required_source <= set(record):
        raise ValueError("canonical source identity is incomplete")
    if not isinstance(record.get("source_sha256"), str) or not SHA256_RE.fullmatch(record["source_sha256"]):
        raise ValueError("canonical source hash is invalid")
    source_payload = {key: value for key, value in record.items() if key != "source_sha256"}
    schema = json.loads((Path(__file__).parents[1] / "conductor/schemas/safety-work.schema.json").read_text())
    if list(Draft202012Validator(schema).iter_errors(source_payload)):
        raise ValueError("canonical source record is invalid")
    if record["source_sha256"] != canonical_hash(source_payload):
        raise ValueError("canonical source hash does not match record")
    context_fields = {"citations", "model_involvement", "limitations", "approval_receipt_ids", "outstanding_review_ids"}
    if not isinstance(view_context, dict) or set(view_context) != context_fields:
        raise ValueError("view context is invalid")
    policies = {
        "investigator": {"case_id", "state", "evidence", "statements", "actions", "reviews", "outcomes", "referrals", "privacy_mode"},
        "reviewer": {"case_id", "state", "evidence", "statements", "actions", "reviews", "outcomes", "referrals", "privacy_mode"},
        "auditor": {"case_id", "state", "evidence", "statements", "actions", "reviews", "outcomes", "referrals", "relationships", "privacy_mode"},
        "consumer_family": {"case_id", "state", "statements", "outcomes", "privacy_mode"},
        "staff": {"case_id", "state", "statements", "reviews", "privacy_mode"},
        "governance": {"case_id", "state", "statements", "actions", "reviews", "outcomes", "referrals", "privacy_mode"},
        "executive": {"case_id", "state", "statements", "actions", "outcomes", "privacy_mode"},
    }
    output = sanitize_export({key: deepcopy(value) for key, value in record.items() if key in policies[audience]})
    assert isinstance(output, dict)
    output["source_schema_version"] = record["schema_version"]
    output["source_version"] = record["version"]
    output["source_sha256"] = record["source_sha256"]
    safe_context = sanitize_export(view_context)
    assert isinstance(safe_context, dict)
    output.update(safe_context)
    allowed_statement_kinds = {
        "consumer_family": {"reported_account", "finding"},
        "staff": {"reported_account"},
    }.get(audience)
    if allowed_statement_kinds is not None and isinstance(output.get("statements"), list):
        output["statements"] = [item for item in output["statements"] if isinstance(item, dict) and item.get("kind") in allowed_statement_kinds]
    output["audience"] = audience
    output["external_action"] = False
    output["disclaimers"] = [
        "Not clinical, policy, legal or organisational approval.",
        "Generated view does not lodge, disclose, approve or close an external record.",
        "Action completion does not establish effectiveness.",
    ]
    output["receipt_sha256"] = canonical_hash(output)
    return output


def evaluate_synthetic_journeys(registry: dict[str, Any], scenarios: object) -> dict[str, Any]:
    errors = validate_registry(registry)
    cases: list[dict[str, object]] = []
    if not isinstance(scenarios, list):
        errors.append("scenarios must be an array")
        scenarios = []
    for scenario in scenarios:
        passed = False
        assertion = "invalid"
        if isinstance(scenario, dict):
            identifier = scenario.get("id")
            kind = scenario.get("kind")
            payload = scenario.get("payload")
            if kind == "registry_checkpoint":
                role = payload.get("role") if isinstance(payload, dict) else None
                passed = any(item.get("role") == role and item.get("failure_recovery") for item in registry.get("journeys", []))
                assertion = "role has explicit recovery"
            elif kind == "unsafe_export":
                try:
                    sanitize_export(payload)
                except ValueError:
                    passed = True
                assertion = "unsafe content rejected"
            elif kind == "specialist_separation":
                passed = "specialist pathway must remain separate" in validate_specialist_referral(payload)
                assertion = "merged pathway rejected"
            elif kind == "communication_boundary":
                passed = bool(validate_communication_draft(payload))
                assertion = "operational communication rejected"
            elif kind == "method_abstention" and isinstance(payload, dict):
                passed = method_guidance(**payload)["abstain"] is True
                assertion = "unsupported method request abstains"
            cases.append({"id": identifier, "assertion": assertion, "passed": passed})
    result = {
        "schema_version": SCHEMA_VERSION,
        "scope": "generated_synthetic_non_operational",
        "cases": [{**item, "passed": bool(item["passed"]) and not errors} for item in cases],
        "metrics": {
            "unsafe_certainty": None,
            "missed_required_disclosures": None,
            "external_actions": 0,
            "review_burden": "descriptive_not_operational_threshold",
        },
        "limitations": [
            "Agent-authored synthetic journey checks are not human usability research.",
            "No clinical deployment, policy applicability or cultural-safety validation.",
        ],
    }
    result["receipt_sha256"] = canonical_hash(result)
    return result
