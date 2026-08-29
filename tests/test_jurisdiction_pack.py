from __future__ import annotations

from copy import deepcopy
from typing import Any

from tools.jurisdiction_pack import (
    candidate_with_change,
    compare_snapshots,
    due_sources,
    load_registry,
    unavailable_upstream,
    validate_registry,
)


def registry() -> dict[str, Any]:
    return load_registry()


def test_registry_and_pack_inheritance_are_valid() -> None:
    value = registry()
    assert validate_registry(value) == []
    packs = {pack["pack_id"]: pack for pack in value["packs"]}
    assert packs["nsw"]["inherits"] == "national"
    assert packs["qld"]["inherits"] == "national"


def test_current_under_review_consultation_superseded_local_and_advisory_are_visible() -> None:
    statuses = {source["status"] for source in registry()["sources"]}
    assert {"current", "under_review", "consultation", "superseded", "local", "advisory"} <= statuses


def test_rules_cannot_use_non_current_or_unknown_sources() -> None:
    value = registry()
    value["rules"][0]["source_ids"] = ["acsqhc-clinical-governance-2017", "missing"]
    errors = validate_registry(value)
    assert any("cannot depend on superseded source" in error for error in errors)
    assert "rules: unknown source_id 'missing'" in errors


def test_mandatory_language_requires_strong_authority() -> None:
    value = registry()
    value["rules"][0]["source_ids"] = ["nsw-cec-incident-resources"]
    assert any("uses 'must' without" in error for error in validate_registry(value))


def test_under_review_rule_requires_uncertainty_disclosure() -> None:
    value = registry()
    rule = next(rule for rule in value["rules"] if rule["rule_id"] == "nsw-notify-ims")
    rule.pop("uncertainty")
    assert any("must disclose under-review" in error for error in validate_registry(value))


def test_national_rules_cannot_import_state_authority() -> None:
    value = registry()
    value["rules"][0]["source_ids"] = ["nsw-pd2023-034"]
    assert any("national rule" in error for error in validate_registry(value))


def test_workflow_transitions_use_the_canonical_contract() -> None:
    value = registry()
    value["rules"][0]["workflow"].update(from_states=["intake"], to_state="closed")
    assert any("invalid canonical transition" in error for error in validate_registry(value))


def test_material_drift_opens_review_and_invalidates_receipts_without_changing_behaviour() -> None:
    baseline = registry()
    candidate = candidate_with_change(
        baseline,
        "nsw-pd2023-034",
        version="replacement candidate",
        checksum="sha256:" + "0" * 64,
    )
    result = compare_snapshots(baseline, candidate)
    assert result["status"] == "review_required"
    assert result["receipt_status"] == "invalidated_pending_human_review"
    assert result["behaviour_updated"] is False
    assert "nsw-clinician-disclosure" in result["affected_rule_ids"]


def test_retrieval_timestamp_only_is_cosmetic() -> None:
    baseline = registry()
    candidate = candidate_with_change(baseline, "nsw-pd2023-034", retrieved_at="2026-08-30T00:00:00Z")
    result = compare_snapshots(baseline, candidate)
    assert result["status"] == "no_material_change"
    assert result["changes"][0]["change_class"] == "cosmetic"


def test_removed_source_is_breaking_and_new_source_is_guidance() -> None:
    baseline = registry()
    removed = deepcopy(baseline)
    removed["sources"] = [source for source in removed["sources"] if source["source_id"] != "qld-qh-hsd-032"]
    result = compare_snapshots(baseline, removed)
    assert any(change["change_class"] == "breaking" for change in result["changes"])

    added = deepcopy(baseline)
    new_source = deepcopy(added["sources"][0])
    new_source["source_id"] = "synthetic-new-source"
    added["sources"].append(new_source)
    result = compare_snapshots(baseline, added)
    assert any(change["change_class"] == "guidance" for change in result["changes"])


def test_unavailable_upstream_is_not_a_pass() -> None:
    result = unavailable_upstream("nsw-pd2020-047", "synthetic timeout")
    assert result["status"] == "unavailable_not_passed"
    assert result["behaviour_updated"] is False


def test_review_cadence_produces_a_deterministic_due_queue() -> None:
    assert due_sources(registry(), as_of="2026-08-30T00:54:13Z") == []
    due = due_sources(registry(), as_of="2026-09-29T00:54:13Z")
    assert "nsw-pd2020-047" in due
    assert "qld-qh-hsd-032" in due


def test_required_people_culture_and_system_safeguards_are_mapped() -> None:
    safeguards = {item for rule in registry()["rules"] for item in rule["safeguards"]}
    assert {
        "open_disclosure",
        "consumer_family",
        "staff_support",
        "procedural_fairness",
        "conflict_of_interest",
        "cultural_safety",
        "systems_analysis",
        "effectiveness",
        "no_privilege_inference",
    } <= safeguards


def test_generic_evidence_core_has_no_state_policy_identifiers() -> None:
    from tools import evidence_core

    source = evidence_core.SCHEMA_PATH.read_text(encoding="utf-8")
    assert "PD2020_047" not in source
    assert "QH-HSD-032" not in source
    assert "ims+" not in source
    assert "RiskMan" not in source
