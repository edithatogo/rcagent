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
    if request.classification in {"confidential", "sensitive"} and request.mode == "public_remote":
        return RouteDecision(False, "private content cannot use public remote mode", "privacy review")
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
    if disclosure.get("human_review") in {None, "", False}:
        errors.append("human review must be explicit")
    return errors


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


def deletion_receipt(*, resource_id: str, compartment: str, actor: str, at: str) -> dict[str, Any]:
    """Create a content-free receipt after a caller has verified deletion."""
    if not resource_id or not compartment or not actor or not at:
        raise ValueError("deletion receipt fields must be explicit")
    receipt = {
        "resource_hash": fingerprint({"resource_id": resource_id}),
        "compartment": compartment,
        "status": "deletion_verified",
        "actor": actor,
        "at": at,
    }
    return {**receipt, "receipt_hash": fingerprint(receipt)}


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
    for key in ("mode", "risks", "controls", "tests", "evidence", "owners", "review_due", "residual_risks"):
        if key not in case:
            errors.append(f"assurance case missing: {key}")
    if case.get("mode") not in MODES:
        errors.append("assurance case mode invalid")
    for risk in case.get("risks", []):
        if risk.get("control_id") not in {control.get("control_id") for control in case.get("controls", [])}:
            errors.append(f"risk has no valid control: {risk.get('risk_id')}")
    if case.get("dependency_status") != "current":
        errors.append("assurance invalidated by dependency drift")
    try:
        review_due = datetime.fromisoformat(str(case.get("review_due", "")).replace("Z", "+00:00"))
        if review_due < now:
            errors.append("assurance review is stale")
    except ValueError:
        errors.append("assurance review date invalid")
    if case.get("residual_risks") and case.get("residual_risk_acceptance") != "owner_required":
        errors.append("residual risk acceptance must remain owner-required")
    return sorted(errors)
