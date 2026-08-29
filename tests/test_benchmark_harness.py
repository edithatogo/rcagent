from __future__ import annotations

import hashlib
import json
from copy import deepcopy

import pytest

from tools.benchmark_harness import (
    ROOT,
    load_registry,
    render_report,
    run_suite,
    score_case,
    validate_registry,
    verify_result,
)


def test_registry_is_valid_and_legacy_estate_is_preserved() -> None:
    registry = load_registry()
    assert validate_registry(registry) == []
    assert {item["condition"] for item in registry["legacy_map"]} == {f"H{number}" for number in range(9)}
    assert all(item["mapping_status"] != "mapped" for item in registry["legacy_map"])


def test_pending_nsw_case_is_not_promotion_eligible_or_runnable() -> None:
    registry = load_registry()
    case = next(item for item in registry["cases"] if item["id"] == "nsw-policy-drift")
    assert case["activation_status"] == "pending_owner_decision"
    assert case["promotion_eligible"] is False
    assert all(case["id"] not in suite["case_ids"] for suite in registry["suites"])

    changed = deepcopy(registry)
    changed["suites"][0]["case_ids"].append(case["id"])
    assert any("pending cases cannot run" in error for error in validate_registry(changed))


def test_fixture_checksum_and_pending_decision_fail_closed() -> None:
    registry = load_registry()
    registry["cases"][0]["sha256"] = "0" * 64
    assert any("checksum mismatch" in error for error in validate_registry(registry))

    registry = load_registry()
    next(item for item in registry["cases"] if item["id"] == "nsw-policy-drift").pop("decision_id")
    assert any("requires decision_id" in error for error in validate_registry(registry))


def test_fixture_paths_and_modality_claims_fail_closed() -> None:
    registry = load_registry()
    registry["cases"][0]["path"] = "evaluation/benchmark/fixtures/../registry.json"
    assert any("escapes the fixture directory" in error for error in validate_registry(registry))

    registry = load_registry()
    registry["cases"][0]["modalities"] = ["audio"]
    assert any("modality mismatch" in error for error in validate_registry(registry))


def test_deterministic_baseline_passes_structural_and_hard_gates() -> None:
    result = run_suite(load_registry(), "regression")
    assert result["summary"]["case_count"] == 6
    assert result["summary"]["passed"] == 6
    assert result["summary"]["promotion_status"] == "eligible_for_human_review"
    assert all(not any(item["gate_violations"].values()) for item in result["results"])
    assert all(item["citation_validity"] == 1 for item in result["results"])
    assert all(item["robustness_challenge_pass"] for item in result["results"])
    assert result["device_observations"]["storage_bytes"] > 0
    assert result["network"] == "disabled"
    assert result["execution_manifest"]["model"] == "none-deterministic-contract"
    assert result["execution_manifest"]["seed"] == 0


def test_every_hard_gate_blocks_a_case() -> None:
    fixture = load_registry()["cases"][0]["path"]
    case = json.loads((ROOT / fixture).read_text(encoding="utf-8"))["cases"][0]
    for category in case["candidate"]["gate_violations"]:
        changed = deepcopy(case)
        changed["candidate"]["gate_violations"][category] = ["synthetic violation"]
        assert score_case(changed)["passed"] is False


def test_result_integrity_is_verified_before_reporting() -> None:
    result = run_suite(load_registry(), "smoke")
    assert verify_result(result) == []
    result["summary"]["passed"] = 999
    assert verify_result(result) == [
        "result pass count is inconsistent",
        "result receipt hash mismatch",
    ]


def test_rehashed_result_cannot_claim_a_pass_over_a_failed_hard_gate() -> None:
    result = run_suite(load_registry(), "smoke")
    result["results"][0]["gate_violations"]["privacy"] = 1
    unsigned = {key: value for key, value in result.items() if key != "receipt_sha256"}
    result["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert verify_result(result) == [
        "result passes a failed hard gate for 'incomplete-evidence'"
    ]


def test_unknown_suite_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown suite"):
        run_suite(load_registry(), "missing")


def test_report_preserves_nonpublication_boundaries() -> None:
    report = render_report(run_suite(load_registry(), "smoke"))
    assert "not an approved model ranking" in report
    assert "no generative model comparator" in report
