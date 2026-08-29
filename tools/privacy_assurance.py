"""Fail-closed privacy, security, and assurance contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from tools.evidence_core import fingerprint

MODES = {"public_remote", "governed_hybrid", "fully_local", "air_gapped"}
CLASSIFICATIONS = {"public", "internal", "confidential", "sensitive"}
REMOTE_MODES = {"public_remote", "governed_hybrid"}
DESTINATIONS = {"local", "model", "remote_log", "telemetry", "public_index"}
CONNECTION_STATES = {"off", "on", "unknown"}
ASSURANCE_DOMAINS = {"security", "privacy", "cultural_safety", "clinical_safety"}
ASSURANCE_CONTROL_STATUSES = {"inherited", "implemented", "supplemented"}
SAFE_ARTIFACT_TYPES = {"application/json", "text/csv", "text/markdown", "text/plain"}
UNSAFE_ARTIFACT_SUFFIXES = {".app", ".bat", ".cmd", ".com", ".dll", ".exe", ".jar", ".js", ".msi", ".ps1", ".scr", ".vbs"}
SENSITIVE_PATTERNS = {
    "nsw_mrn": re.compile(r"\b(?:MRN|URN)\s*[:#-]?\s*\d{6,10}\b", re.IGNORECASE),
    "qld_ur": re.compile(r"\b(?:UR|URN)\s*[:#-]?\s*\d{6,10}\b", re.IGNORECASE),
    "qld_coronial": re.compile(r"\b(?:COR|CI)\s*[-/]?\s*\d{2,4}[-/]\d{3,8}\b", re.IGNORECASE),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone": re.compile(r"(?<!\d)(?:\+?61\s?|0)[2-478](?:[ -]?\d){8}(?!\d)"),
}
INJECTION_PATTERNS = (
    re.compile(r"ignore (?:all |the )?(?:previous|prior) instructions", re.IGNORECASE),
    re.compile(r"reveal (?:the )?(?:system prompt|credentials|secrets)", re.IGNORECASE),
    re.compile(r"disable (?:privacy|security|logging|audit)", re.IGNORECASE),
)


@dataclass(frozen=True)
class RouteRequest:
    classification: str | None
    mode: str | None
    destination: str
    network: str
    telemetry: str
    model_provenance_known: bool
    deidentified: bool = False


@dataclass(frozen=True)
class RouteDecision:
    allowed: bool
    reason: str
    required_review: str | None = None


def route(request: RouteRequest) -> RouteDecision:
    if request.classification not in CLASSIFICATIONS:
        return RouteDecision(False, "classification unknown", "privacy review")
    if request.mode not in MODES:
        return RouteDecision(False, "execution mode unknown", "security review")
    if request.destination not in DESTINATIONS:
        return RouteDecision(False, "destination unknown", "security review")
    if request.network not in CONNECTION_STATES or request.network == "unknown":
        return RouteDecision(False, "egress status unknown", "security review")
    if request.telemetry not in CONNECTION_STATES or request.telemetry == "unknown":
        return RouteDecision(False, "telemetry status unknown", "privacy review")
    if request.destination == "model" and not request.model_provenance_known:
        return RouteDecision(False, "model provenance unknown", "model governance review")
    if request.mode in {"fully_local", "air_gapped"} and request.network != "off":
        return RouteDecision(False, "local-only mode requires network off", "security review")
    if request.mode in {"fully_local", "air_gapped"} and request.telemetry != "off":
        return RouteDecision(False, "local-only mode requires telemetry off", "privacy review")
    if request.mode in {"fully_local", "air_gapped"} and request.destination != "local":
        return RouteDecision(False, "local-only mode forbids remote destination", "privacy review")
    if request.classification != "public" and request.mode == "public_remote":
        return RouteDecision(False, "non-public content cannot use public remote mode", "privacy review")
    if request.classification == "sensitive" and request.mode == "governed_hybrid" and not request.deidentified:
        return RouteDecision(False, "sensitive hybrid content requires approved de-identification", "privacy review")
    return RouteDecision(True, "declared route satisfies the core policy")


def scan_sensitive_text(text: str) -> list[str]:
    return sorted(name for name, pattern in SENSITIVE_PATTERNS.items() if pattern.search(text))


def scan_adversarial_text(text: str) -> list[str]:
    findings = ["prompt_injection" for pattern in INJECTION_PATTERNS if pattern.search(text)]
    if "<script" in text.lower() or "javascript:" in text.lower():
        findings.append("active_content")
    if "../" in text or "..\\" in text:
        findings.append("path_traversal")
    return sorted(set(findings))


def compartment_key(mode: str, classification: str, resource: str) -> str:
    if mode not in MODES or classification not in CLASSIFICATIONS:
        raise ValueError("unknown mode or classification")
    zone = "public" if classification == "public" else "private"
    return f"{mode}:{zone}:{resource}"


def validate_execution_disclosure(disclosure: dict[str, Any]) -> list[str]:
    required = {
        "task",
        "tool",
        "revision",
        "mode",
        "classification",
        "network",
        "telemetry",
        "storage",
        "limitations",
        "human_review",
    }
    errors = [f"missing disclosure field: {key}" for key in sorted(required - disclosure.keys())]
    if disclosure.get("mode") not in MODES:
        errors.append("invalid disclosure mode")
    if disclosure.get("classification") not in CLASSIFICATIONS:
        errors.append("invalid disclosure classification")
    for key in ("task", "tool", "revision", "storage"):
        if key in disclosure and (not isinstance(disclosure[key], str) or not disclosure[key].strip()):
            errors.append(f"disclosure field must be a non-empty string: {key}")
    if disclosure.get("network") not in CONNECTION_STATES or disclosure.get("network") == "unknown":
        errors.append("network status must be known")
    if disclosure.get("telemetry") not in CONNECTION_STATES or disclosure.get("telemetry") == "unknown":
        errors.append("telemetry status must be known")
    if disclosure.get("mode") in {"fully_local", "air_gapped"} and disclosure.get("network") != "off":
        errors.append("local-only disclosure requires network off")
    if disclosure.get("mode") in {"fully_local", "air_gapped"} and disclosure.get("telemetry") != "off":
        errors.append("local-only disclosure requires telemetry off")
    if disclosure.get("mode") == "public_remote" and disclosure.get("classification") != "public":
        errors.append("public remote disclosure requires public classification")
    limitations = disclosure.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(isinstance(item, str) and item.strip() for item in limitations):
        errors.append("limitations must contain at least one explicit limitation")
    if disclosure.get("human_review") in {None, "", False}:
        errors.append("human review must be explicit")
    return sorted(set(errors))


def validate_model_result(result: dict[str, Any]) -> list[str]:
    """Require every model-assisted result to carry its complete disclosure."""
    errors: list[str] = []
    if not isinstance(result.get("output_id"), str) or not result.get("output_id", "").strip():
        errors.append("model result output_id must be explicit")
    if result.get("status") not in {"produced", "abstained", "quarantined"}:
        errors.append("model result status invalid")
    disclosure = result.get("disclosure")
    if not isinstance(disclosure, dict):
        errors.append("model result disclosure missing")
    else:
        errors.extend(f"model result {error}" for error in validate_execution_disclosure(disclosure))
    return sorted(errors)


def quarantine_output(*, output_id: str, reasons: list[str], actor: str, at: str) -> dict[str, Any]:
    if not reasons:
        raise ValueError("quarantine requires at least one reason")
    receipt = {"output_id": output_id, "status": "quarantined", "reasons": sorted(set(reasons)), "actor": actor, "at": at}
    return {**receipt, "receipt_hash": fingerprint(receipt)}


def sanitise_diagnostic(text: str) -> str:
    """Remove sensitive sentinels, credentials, and local paths from diagnostic text."""
    sanitised = text
    for pattern in SENSITIVE_PATTERNS.values():
        sanitised = pattern.sub("[REDACTED]", sanitised)
    sanitised = re.sub(
        r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*\S+",
        "credential=[REDACTED]",
        sanitised,
        flags=re.IGNORECASE,
    )
    sanitised = re.sub(r"(?<!\w)/(?:Users|home|Volumes|private|var)/\S+", "[LOCAL_PATH]", sanitised)
    return sanitised


def deletion_receipt(
    *, resource_id: str, compartment: str, actor: str, at: str, verification: dict[str, str]
) -> dict[str, Any]:
    """Create a content-free receipt after a caller has verified deletion."""
    if not resource_id or not compartment or not actor or not at:
        raise ValueError("deletion receipt fields must be explicit")
    if not compartment.count(":") == 2:
        raise ValueError("deletion compartment must be a canonical compartment key")
    method = verification.get("method", "").strip()
    evidence_hash = verification.get("evidence_hash", "").strip()
    verified_by = verification.get("verified_by", "").strip()
    if not method or not re.fullmatch(r"sha256:[0-9a-f]{64}", evidence_hash) or not verified_by:
        raise ValueError("deletion verification evidence must be explicit and hashed")
    receipt = {
        "resource_hash": fingerprint({"resource_id": resource_id}),
        "compartment": compartment,
        "status": "deletion_verified",
        "actor": actor,
        "at": at,
        "verification": {"method": method, "evidence_hash": evidence_hash, "verified_by": verified_by},
    }
    return {**receipt, "receipt_hash": fingerprint(receipt)}


def assess_input_artifact(*, name: str, media_type: str, text: str) -> list[str]:
    """Identify artifact properties that require isolation before parsing."""
    findings = scan_adversarial_text(name)
    suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if suffix in UNSAFE_ARTIFACT_SUFFIXES:
        findings.append("executable_artifact")
    if media_type not in SAFE_ARTIFACT_TYPES:
        findings.append("unsupported_media_type")
    if scan_adversarial_text(text):
        findings.append("untrusted_active_or_instructional_content")
    return sorted(set(findings))


def validate_retrieval_item(item: dict[str, Any], *, expected_compartment: str) -> list[str]:
    """Reject cross-compartment or unprovenanced retrieval before use."""
    errors: list[str] = []
    if item.get("compartment") != expected_compartment:
        errors.append("retrieval compartment mismatch")
    if item.get("provenance_status") != "current":
        errors.append("retrieval provenance is not current")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(item.get("source_hash", ""))):
        errors.append("retrieval source hash invalid")
    content = item.get("content")
    if not isinstance(content, str):
        errors.append("retrieval content missing")
    elif scan_adversarial_text(content):
        errors.append("retrieval content is adversarial")
    return sorted(errors)


def validate_plugin_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a bounded plugin admission declaration without activating it."""
    errors: list[str] = []
    for key in ("plugin_id", "revision", "licence", "sandbox"):
        if not isinstance(manifest.get(key), str) or not manifest.get(key, "").strip():
            errors.append(f"plugin field missing: {key}")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(manifest.get("checksum", ""))):
        errors.append("plugin checksum invalid")
    if manifest.get("remote_code") is not False:
        errors.append("plugin remote code must be disabled")
    if manifest.get("telemetry") != "off":
        errors.append("plugin telemetry must default off")
    if manifest.get("network") not in {"off", "disclosed"}:
        errors.append("plugin network state must be off or disclosed")
    if manifest.get("network") == "disclosed" and not manifest.get("external_processing"):
        errors.append("plugin external processing disclosure missing")
    return sorted(errors)


def recovery_action(failure: str, *, mode: str) -> RouteDecision:
    """Return a bounded fail-closed action for operational failure states."""
    if mode not in MODES:
        return RouteDecision(False, "execution mode unknown", "security review")
    actions = {
        "model_unavailable": "abstain and request human review",
        "index_corrupt": "isolate index and rebuild from verified sources",
        "network_loss": "continue local-only without remote fallback" if mode != "public_remote" else "abstain until route is restored",
        "power_loss": "halt and verify receipts before resume",
    }
    reason = actions.get(failure, "halt and escalate unknown recovery state")
    return RouteDecision(False, reason, "human recovery review")


def evaluate_assurance(case: dict[str, Any], *, now: datetime | None = None) -> list[str]:
    now = now or datetime.now(UTC)
    errors: list[str] = []
    for key in (
        "schema_version",
        "mode",
        "risks",
        "controls",
        "tests",
        "evidence",
        "owners",
        "review_due",
        "residual_risks",
        "limitations",
        "domains",
    ):
        if key not in case:
            errors.append(f"assurance case missing: {key}")
    if case.get("schema_version") != "1.1":
        errors.append("assurance case schema version invalid")
    if case.get("mode") not in MODES:
        errors.append("assurance case mode invalid")
    for key in ("risks", "controls", "tests", "evidence", "owners", "limitations"):
        if key in case and (not isinstance(case[key], list) or not case[key]):
            errors.append(f"assurance case requires non-empty: {key}")
    controls = case.get("controls", []) if isinstance(case.get("controls", []), list) else []
    risks = case.get("risks", []) if isinstance(case.get("risks", []), list) else []
    control_ids = [control.get("control_id") for control in controls if isinstance(control, dict)]
    risk_ids = [risk.get("risk_id") for risk in risks if isinstance(risk, dict)]
    if len(control_ids) != len(set(control_ids)):
        errors.append("assurance control identifiers must be unique")
    if len(risk_ids) != len(set(risk_ids)):
        errors.append("assurance risk identifiers must be unique")
    valid_controls = {
        control.get("control_id")
        for control in controls
        if isinstance(control, dict) and control.get("status") in ASSURANCE_CONTROL_STATUSES
    }
    for risk in risks:
        if isinstance(risk, dict) and risk.get("control_id") not in valid_controls:
            errors.append(f"risk has no valid control: {risk.get('risk_id')}")
    domains = case.get("domains")
    if not isinstance(domains, dict) or set(domains) != ASSURANCE_DOMAINS:
        errors.append("assurance domains must cover security, privacy, cultural safety, and clinical safety")
    else:
        for domain, result in domains.items():
            if not isinstance(result, dict) or result.get("status") not in {"tested_bounded", "owner_required"}:
                errors.append(f"assurance domain status invalid: {domain}")
            if not isinstance(result, dict) or not isinstance(result.get("evidence"), list) or not result["evidence"]:
                errors.append(f"assurance domain evidence missing: {domain}")
    if case.get("dependency_status") != "current":
        errors.append("assurance invalidated by dependency drift")
    try:
        review_due = datetime.fromisoformat(str(case.get("review_due", "")).replace("Z", "+00:00"))
        if review_due.tzinfo is None:
            errors.append("assurance review date must include timezone")
        elif review_due < now:
            errors.append("assurance review is stale")
    except (TypeError, ValueError):
        errors.append("assurance review date invalid")
    if case.get("residual_risks") and case.get("residual_risk_acceptance") != "owner_required":
        errors.append("residual risk acceptance must remain owner-required")
    return sorted(errors)
