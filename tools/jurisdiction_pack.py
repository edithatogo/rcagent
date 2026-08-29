"""Fail-closed validation and drift classification for jurisdiction packs."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from tools.evidence_core import TRANSITIONS

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "conductor/jurisdictions/registry.json"
SCHEMA_PATH = ROOT / "conductor/schemas/jurisdiction-pack.schema.json"
MATERIAL_CHANGE_CLASSES = {"guidance", "normative", "breaking"}


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_registry(registry: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in validator.iter_errors(registry)
    ]
    packs = registry.get("packs", [])
    sources = registry.get("sources", [])
    rules = registry.get("rules", [])
    artefacts = registry.get("artefacts", [])

    errors.extend(_unique_id_errors(packs, "pack_id", "packs"))
    errors.extend(_unique_id_errors(sources, "source_id", "sources"))
    errors.extend(_unique_id_errors(rules, "rule_id", "rules"))
    errors.extend(_unique_id_errors(artefacts, "artefact_id", "artefacts"))

    source_by_id = {
        source["source_id"]: source
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("source_id"), str)
    }
    pack_by_id = {
        pack["pack_id"]: pack
        for pack in packs
        if isinstance(pack, dict) and isinstance(pack.get("pack_id"), str)
    }
    for pack in packs:
        if not isinstance(pack, dict):
            continue
        parent = pack.get("inherits")
        if parent is not None and parent not in pack_by_id:
            errors.append(f"packs: unknown inherited pack {parent!r}")
        if pack.get("jurisdiction") != "national" and parent != "national":
            errors.append(f"packs: state pack {pack.get('pack_id')!r} must inherit 'national'")

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        for source_id in rule.get("source_ids", []):
            source = source_by_id.get(source_id)
            if source is None:
                errors.append(f"rules: unknown source_id {source_id!r}")
                continue
            if source.get("status") in {"draft", "consultation", "superseded", "unavailable"}:
                errors.append(
                    f"rules: {rule.get('rule_id')!r} cannot depend on {source.get('status')} source {source_id!r}"
                )
        cited_sources = [source_by_id[source_id] for source_id in rule.get("source_ids", []) if source_id in source_by_id]
        strong_authorities = {"legislation", "regulation", "mandatory_policy", "accreditation_standard"}
        if rule.get("requirement_level") == "must" and not any(
            source.get("authority_level") in strong_authorities for source in cited_sources
        ):
            errors.append(
                f"rules: {rule.get('rule_id')!r} uses 'must' without a binding, mandatory or accreditation source"
            )
        under_review = any(source.get("status") == "under_review" for source in cited_sources)
        if under_review and not rule.get("uncertainty"):
            errors.append(f"rules: {rule.get('rule_id')!r} must disclose under-review source uncertainty")
        if under_review and rule.get("activation_status") != "pending_owner_decision":
            errors.append(
                f"rules: {rule.get('rule_id')!r} must remain pending while an under-review source lacks owner approval"
            )
        if under_review and not rule.get("decision_id"):
            errors.append(f"rules: {rule.get('rule_id')!r} must reference its owner decision")
        if rule.get("activation_status") == "pending_owner_decision" and not rule.get("decision_id"):
            errors.append(f"rules: {rule.get('rule_id')!r} pending activation must reference an owner decision")
        workflow = rule.get("workflow", {})
        if isinstance(workflow, dict):
            to_state = workflow.get("to_state")
            for from_state in workflow.get("from_states", []):
                if to_state not in TRANSITIONS.get(from_state, set()):
                    errors.append(
                        f"rules: {rule.get('rule_id')!r} has invalid canonical transition "
                        f"{from_state!r} -> {to_state!r}"
                    )
        if rule.get("jurisdiction") == "national":
            state_sources = [
                source_id
                for source_id in rule.get("source_ids", [])
                if source_by_id.get(source_id, {}).get("tier") == "state"
            ]
            if state_sources:
                errors.append(
                    f"rules: national rule {rule.get('rule_id')!r} references state sources {state_sources!r}"
                )

    pending_jurisdictions = {
        rule.get("jurisdiction")
        for rule in rules
        if isinstance(rule, dict) and rule.get("activation_status") == "pending_owner_decision"
    }
    for pack in packs:
        if (
            isinstance(pack, dict)
            and pack.get("jurisdiction") in pending_jurisdictions
            and pack.get("status") != "blocked"
        ):
            errors.append(
                f"packs: {pack.get('pack_id')!r} must be blocked while its rules await an owner decision"
            )

    for artefact in artefacts:
        if not isinstance(artefact, dict):
            continue
        for source_id in artefact.get("source_ids", []):
            if source_id not in source_by_id:
                errors.append(f"artefacts: unknown source_id {source_id!r}")

    required_statuses = {"current", "under_review", "consultation", "superseded", "local", "advisory"}
    represented = {source.get("status") for source in sources if isinstance(source, dict)}
    for status in sorted(required_statuses - represented):
        errors.append(f"sources: status {status!r} is not visibly represented")

    required_safeguards = {
        "open_disclosure",
        "consumer_family",
        "staff_support",
        "procedural_fairness",
        "conflict_of_interest",
        "cultural_safety",
        "systems_analysis",
        "effectiveness",
        "no_privilege_inference",
    }
    represented_safeguards = {
        safeguard
        for rule in rules
        if isinstance(rule, dict)
        for safeguard in rule.get("safeguards", [])
    }
    for safeguard in sorted(required_safeguards - represented_safeguards):
        errors.append(f"rules: safeguard {safeguard!r} is not represented")
    return sorted(errors)


def _unique_id_errors(items: Any, key: str, label: str) -> list[str]:
    if not isinstance(items, list):
        return []
    identifiers = [
        identifier
        for item in items
        if isinstance(item, dict) and isinstance((identifier := item.get(key)), str)
    ]
    return [
        f"{label}: duplicate {key} {identifier!r}"
        for identifier in sorted({value for value in identifiers if identifiers.count(value) > 1})
    ]


def compare_snapshots(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return a reviewable, receipt-invalidating drift context without changing behaviour."""
    baseline_sources = {source["source_id"]: source for source in baseline.get("sources", [])}
    candidate_sources = {source["source_id"]: source for source in candidate.get("sources", [])}
    changes: list[dict[str, Any]] = []
    for source_id in sorted(baseline_sources.keys() | candidate_sources.keys()):
        before = baseline_sources.get(source_id)
        after = candidate_sources.get(source_id)
        if before is None:
            changes.append(_change(source_id, "guidance", ["source_added"]))
            continue
        if after is None:
            changes.append(_change(source_id, "breaking", ["source_removed"]))
            continue
        fields = sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))
        material_fields = [field for field in fields if field not in {"retrieved_at"}]
        if not material_fields:
            if fields:
                changes.append(_change(source_id, "cosmetic", fields))
            continue
        if any(field in material_fields for field in ("status", "authority_level", "rights_status")):
            change_class = "breaking"
        elif any(field in material_fields for field in ("version", "document_id", "replaces", "url")):
            change_class = "normative"
        else:
            change_class = "guidance"
        changes.append(_change(source_id, change_class, material_fields))

    material = [change for change in changes if change["change_class"] in MATERIAL_CHANGE_CLASSES]
    affected_sources = {change["source_id"] for change in material}
    affected_rules = sorted(
        rule["rule_id"]
        for rule in baseline.get("rules", [])
        if affected_sources.intersection(rule.get("source_ids", []))
    )
    return {
        "status": "review_required" if material else "no_material_change",
        "changes": changes,
        "affected_rule_ids": affected_rules,
        "receipt_status": "invalidated_pending_human_review" if material else "current",
        "behaviour_updated": False,
    }


def due_sources(registry: dict[str, Any], *, as_of: str) -> list[str]:
    """List sources due for retrieval using UTC timestamps and declared cadences."""
    from datetime import datetime, timedelta

    now = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    due: list[str] = []
    for source in registry.get("sources", []):
        retrieved = datetime.fromisoformat(source["retrieved_at"].replace("Z", "+00:00"))
        if now >= retrieved + timedelta(days=source["review_cadence_days"]):
            due.append(source["source_id"])
    return sorted(due)


def unavailable_upstream(source_id: str, diagnostic: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "status": "unavailable_not_passed",
        "diagnostic": diagnostic,
        "behaviour_updated": False,
        "receipt_status": "current_snapshot_retained_pending_retrieval",
    }


def _change(source_id: str, change_class: str, fields: list[str]) -> dict[str, Any]:
    return {"source_id": source_id, "change_class": change_class, "changed_fields": fields}


def candidate_with_change(registry: dict[str, Any], source_id: str, **updates: Any) -> dict[str, Any]:
    """Test helper: return a detached candidate snapshot."""
    candidate = deepcopy(registry)
    for source in candidate["sources"]:
        if source["source_id"] == source_id:
            source.update(updates)
            return candidate
    raise KeyError(source_id)


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path", nargs="?", type=Path, default=REGISTRY_PATH)
    drift_parser = subparsers.add_parser("drift")
    drift_parser.add_argument("baseline", type=Path)
    drift_parser.add_argument("candidate", type=Path)
    due_parser = subparsers.add_parser("due")
    due_parser.add_argument("--as-of", required=True)
    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_registry(load_registry(args.path))
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Jurisdiction registry validation passed.")
        return 0
    if args.command == "due":
        print(json.dumps({"due_source_ids": due_sources(load_registry(), as_of=args.as_of)}, indent=2))
        return 0
    baseline = load_registry(args.baseline)
    candidate = load_registry(args.candidate)
    errors = [f"baseline: {error}" for error in validate_registry(baseline)]
    errors.extend(f"candidate: {error}" for error in validate_registry(candidate))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    result = compare_snapshots(baseline, candidate)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["status"] == "review_required" else 0


if __name__ == "__main__":
    raise SystemExit(main())
