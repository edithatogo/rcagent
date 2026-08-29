from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from tools import multimodal_fabric
from tools.multimodal_fabric import execution_disclosure, load_registry, validate_registry


def test_registry_is_valid_and_framework_neutral() -> None:
    registry = load_registry()
    assert validate_registry(registry) == []
    assert {item["modality"] for item in registry["profiles"]} == {
        "document",
        "encoder",
        "speech",
        "image",
        "signal",
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


def test_read_rejects_non_object_and_invalid_registry_blocks_disclosure(tmp_path: Path) -> None:
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="expected an object"):
        multimodal_fabric._read(path)
    registry = load_registry()
    registry["profiles"][0]["privacy"]["remote_code"] = "allowed"
    with pytest.raises(ValueError, match="invalid registry"):
        execution_disclosure(registry, "documents-ocr", "document-layout")


def test_multimodal_cli_validate_success_failure_and_probe(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["multimodal-fabric", "validate"])
    assert multimodal_fabric.main() == 0
    assert "validation passed" in capsys.readouterr().out
    invalid = load_registry()
    invalid["profiles"][0]["privacy"]["network"] = "enabled"
    monkeypatch.setattr(multimodal_fabric, "load_registry", lambda: invalid)
    monkeypatch.setattr(sys, "argv", ["multimodal-fabric", "validate"])
    assert multimodal_fabric.main() == 1
    assert "ERROR:" in capsys.readouterr().out
    valid = load_registry()
    monkeypatch.setattr(multimodal_fabric, "load_registry", lambda: valid)
    fixture = valid["fixtures"][0]
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "multimodal-fabric",
            "probe",
            "--profile",
            fixture["profile_id"],
            "--fixture",
            fixture["id"],
        ],
    )
    assert multimodal_fabric.main() == 0
    assert json.loads(capsys.readouterr().out)["fixture_id"] == fixture["id"]
