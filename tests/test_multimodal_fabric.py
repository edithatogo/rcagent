from __future__ import annotations

from copy import deepcopy

import pytest

from tools.multimodal_fabric import execution_disclosure, load_registry, validate_registry


def test_registry_is_valid_and_framework_neutral() -> None:
    registry = load_registry()
    assert validate_registry(registry) == []
    assert {item["modality"] for item in registry["profiles"]} == {
        "document", "encoder", "speech", "image", "signal"
    }
    assert all(item["status"] != "supported" for item in registry["profiles"])


def test_every_probe_discloses_unsupported_nonclinical_execution() -> None:
    registry = load_registry()
    for fixture in registry["fixtures"]:
        result = execution_disclosure(registry, fixture["profile_id"], fixture["id"])
        assert result["network"] == "disabled"
        assert result["remote_code"] == "prohibited"
        assert result["interpretation_allowed"] is False
        assert result["supported"] is False
        assert result["output_provenance"] == fixture["expected_provenance"]


def test_research_profiles_and_unadmitted_network_fail_closed() -> None:
    registry = load_registry()
    image = next(item for item in registry["profiles"] if item["modality"] == "image")
    image["status"] = "supported"
    assert any("research-disabled" in error for error in validate_registry(registry))

    registry = load_registry()
    registry["profiles"][0]["privacy"]["network"] = "enabled"
    assert any("must disable network" in error for error in validate_registry(registry))


def test_remote_code_and_fixture_mismatch_are_rejected() -> None:
    registry = load_registry()
    registry["profiles"][0]["privacy"]["remote_code"] = "allowed"
    assert any("must prohibit remote code" in error for error in validate_registry(registry))

    with pytest.raises(ValueError, match="mismatched"):
        execution_disclosure(load_registry(), "documents-ocr", "speech-timestamp")


def test_duplicate_and_unknown_identifiers_are_rejected() -> None:
    registry = load_registry()
    registry["profiles"].append(deepcopy(registry["profiles"][0]))
    assert any("duplicate id" in error for error in validate_registry(registry))

    registry = load_registry()
    registry["fixtures"][0]["profile_id"] = "missing"
    assert any("unknown profile" in error for error in validate_registry(registry))
