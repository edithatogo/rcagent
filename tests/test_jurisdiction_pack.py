from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from tools import jurisdiction_pack
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


def under_review_registry() -> dict[str, Any]:
    """Exercise under-review rules without inventing a real policy status."""
    value = registry()
    source = deepcopy(value["sources"][0])
    source.update(
        source_id="synthetic-under-review-source",
        issuer="Synthetic test authority",
        title="Synthetic policy under review",
        document_id="SYNTHETIC-REVIEW",
        url="https://example.invalid/synthetic-policy",
        status="under_review",
        checksum=None,
        checksum_basis="not_available",
    )
    value["sources"].append(source)
    rule = deepcopy(value["rules"][0])
    rule.update(
        rule_id="synthetic-under-review-rule",
        source_ids=[source["source_id"]],
        uncertainty="Synthetic source under review; applicability is uncertain.",
        decision_id="synthetic-recorded-decision",
        decision_status="approved",
    )
    value["rules"].append(rule)
    return value


def test_registry_and_pack_inheritance_are_valid() -> None:
    value = registry()
    assert validate_registry(value) == []
    packs = {pack["pack_id"]: pack for pack in value["packs"]}
    assert packs["nsw"]["inherits"] == "national"
    assert packs["nsw"]["status"] == "blocked"
    assert packs["qld"]["inherits"] == "national"
    assert packs["qld"]["status"] == "implemented"


def test_observed_source_statuses_do_not_require_a_manufactured_under_review_source() -> None:
    statuses = {source["status"] for source in registry()["sources"]}
    assert {
        "current",
        "unavailable",
        "consultation",
        "superseded",
        "local",
        "advisory",
    } <= statuses


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
    value = under_review_registry()
    rule = value["rules"][-1]
    rule.pop("uncertainty")
    assert any("must disclose under-review" in error for error in validate_registry(value))


def test_under_review_rules_activate_only_with_the_recorded_owner_decision() -> None:
    value = under_review_registry()
    assert validate_registry(value) == []
    value["rules"][-1].pop("decision_status")
    assert any("must remain pending" in error for error in validate_registry(value))


def test_pending_rule_requires_decision_and_blocks_its_pack() -> None:
    value = under_review_registry()
    rule = value["rules"][-1]
    rule.pop("decision_id")
    assert any("must reference" in error for error in validate_registry(value))

    value = under_review_registry()
    pending_rule = value["rules"][-1]
    pending_rule["activation_status"] = "pending_owner_decision"
    pending_rule["decision_status"] = "pending"
    assert any("must be blocked" in error for error in validate_registry(value))


def test_nsw_transition_withholds_rules_without_requiring_owner_approval() -> None:
    value = registry()
    pending = [rule for rule in value["rules"] if "nsw-pd2026-036" in rule["source_ids"]]
    assert {rule["rule_id"] for rule in pending} == {"nsw-notify-ims", "nsw-serious-review"}
    for rule in pending:
        assert rule["activation_status"] == "pending_source_verification"
        assert rule["workflow"]["deadline"] is None
        assert rule["uncertainty"].strip()
        assert "nsw-cec-incident-transition-2026" in rule["source_ids"]
        assert "decision_id" not in rule
        assert "decision_status" not in rule
    assert all("nsw-pd2020-047" not in rule["source_ids"] for rule in value["rules"])
    legacy = next(source for source in value["sources"] if source["source_id"] == "nsw-pd2020-047")
    assert legacy["status"] == "unavailable"
    assert legacy["retrieved_at"] == "2026-08-29T00:54:13Z"
    assert (
        legacy["checksum"]
        == "sha256:206514440bf425ccb5fc0dc1743ea546f8b81d89f5007e27db4f988795d5d560"
    )
    assert "20260829-001-active-under-review-pd2020-047" in legacy["limitations"]
    assert validate_registry(value) == []


@pytest.mark.parametrize("activation", ["active", "pending_owner_decision"])
def test_unavailable_source_cannot_be_enabled_by_owner_approval(activation: str) -> None:
    value = registry()
    rule = next(rule for rule in value["rules"] if rule["rule_id"] == "nsw-notify-ims")
    rule.update(
        activation_status=activation,
        decision_id="synthetic-owner-approval",
        decision_status="approved",
    )
    assert any("cannot depend on unavailable source" in error for error in validate_registry(value))


@pytest.mark.parametrize("uncertainty", [None, "", "   "])
def test_pending_source_verification_requires_visible_uncertainty(uncertainty: str | None) -> None:
    value = registry()
    rule = next(rule for rule in value["rules"] if rule["rule_id"] == "nsw-notify-ims")
    rule["uncertainty"] = uncertainty
    assert any(
        "must disclose pending source verification" in error for error in validate_registry(value)
    )


def test_pending_source_verification_forbids_deadlines_and_blocks_its_pack() -> None:
    value = registry()
    rule = next(rule for rule in value["rules"] if rule["rule_id"] == "nsw-notify-ims")
    rule["workflow"]["deadline"] = "P1D from obsolete policy"
    next(pack for pack in value["packs"] if pack["pack_id"] == "nsw")["status"] = "implemented"
    errors = validate_registry(value)
    assert any("cannot set a deadline" in error for error in errors)
    assert any(
        "must be blocked while its rules await source verification" in error for error in errors
    )


def test_source_verification_can_precede_any_under_review_owner_decision() -> None:
    value = under_review_registry()
    rule = value["rules"][-1]
    rule["activation_status"] = "pending_source_verification"
    rule.pop("decision_id")
    rule.pop("decision_status")
    next(pack for pack in value["packs"] if pack["pack_id"] == "national")["status"] = "blocked"
    assert validate_registry(value) == []


def test_qld_deadlines_retain_directive_authority_despite_guideline_metadata_conflict() -> None:
    value = registry()
    rules = {rule["rule_id"]: rule for rule in value["rules"]}
    for rule_id in ("qld-sac1-report", "qld-sac1-analysis"):
        assert rules[rule_id]["activation_status"] == "active"
        assert rules[rule_id]["source_ids"] == ["qld-qh-hsd-032"]
        assert rules[rule_id]["workflow"]["deadline"]
    guideline = next(
        source for source in value["sources"] if source["source_id"] == "qld-qh-hsdgdl-032-2"
    )
    assert guideline["status"] == "current"
    assert "metadata conflict" in guideline["version"]


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
    candidate = candidate_with_change(
        baseline, "nsw-pd2023-034", retrieved_at="2026-08-30T00:00:00Z"
    )
    result = compare_snapshots(baseline, candidate)
    assert result["status"] == "no_material_change"
    assert result["changes"][0]["change_class"] == "cosmetic"


def test_removed_source_is_breaking_and_new_source_is_guidance() -> None:
    baseline = registry()
    removed = deepcopy(baseline)
    removed["sources"] = [
        source for source in removed["sources"] if source["source_id"] != "qld-qh-hsd-032"
    ]
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
    value = registry()
    for source in value["sources"]:
        source["retrieved_at"] = "2026-08-29T00:54:13Z"
    assert due_sources(value, as_of="2026-08-30T00:54:13Z") == []
    due = due_sources(value, as_of="2026-09-29T00:54:13Z")
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
    assert "PD2026_036" not in source
    assert "QH-HSD-032" not in source
    assert "ims+" not in source
    assert "RiskMan" not in source


def test_registry_rejects_duplicate_inheritance_artefact_and_missing_safeguards() -> None:
    value = registry()
    value["packs"].append(deepcopy(value["packs"][0]))
    value["packs"][1]["inherits"] = "missing-pack"
    value["packs"][1]["jurisdiction"] = "AU-NSW"
    value["artefacts"][0]["source_ids"] = ["missing-source"]
    value["rules"] = []
    errors = validate_registry(value)
    assert any("duplicate pack_id" in error for error in errors)
    assert any("unknown inherited pack" in error for error in errors)
    assert any("must inherit 'national'" in error for error in errors)
    assert any("artefacts: unknown source_id" in error for error in errors)
    assert any("safeguard" in error for error in errors)


def test_under_review_decision_status_and_candidate_lookup_fail_closed() -> None:
    value = under_review_registry()
    rule = value["rules"][-1]
    rule["decision_status"] = "rejected"
    assert any("pending or approved" in error for error in validate_registry(value))
    with pytest.raises(KeyError, match="missing-source"):
        candidate_with_change(value, "missing-source", status="current")


def test_jurisdiction_cli_validate_due_and_drift_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    baseline = registry()
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    candidate_path.write_text(json.dumps(baseline), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["jurisdiction-pack", "validate", str(baseline_path)])
    assert jurisdiction_pack.main() == 0
    assert "validation passed" in capsys.readouterr().out
    monkeypatch.setattr(
        sys, "argv", ["jurisdiction-pack", "due", "--as-of", "2026-09-29T00:54:13Z"]
    )
    assert jurisdiction_pack.main() == 0
    assert "due_source_ids" in capsys.readouterr().out
    monkeypatch.setattr(
        sys, "argv", ["jurisdiction-pack", "drift", str(baseline_path), str(candidate_path)]
    )
    assert jurisdiction_pack.main() == 0
    assert "no_material_change" in capsys.readouterr().out
    changed = candidate_with_change(baseline, "nsw-pd2023-034", status="superseded")
    candidate_path.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(
        sys, "argv", ["jurisdiction-pack", "drift", str(baseline_path), str(candidate_path)]
    )
    assert jurisdiction_pack.main() == 1
    assert "candidate:" in capsys.readouterr().out
    changed = candidate_with_change(baseline, "nsw-pd2023-034", version="replacement")
    candidate_path.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(
        sys, "argv", ["jurisdiction-pack", "drift", str(baseline_path), str(candidate_path)]
    )
    assert jurisdiction_pack.main() == 2
    assert "review_required" in capsys.readouterr().out
