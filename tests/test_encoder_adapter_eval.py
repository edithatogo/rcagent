from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from tools import encoder_adapter_eval


def test_evaluation_is_offline_synthetic_and_fails_closed() -> None:
    result = encoder_adapter_eval.evaluate()
    assert result["data_class"] == "generated_synthetic_only"
    assert result["network"] == "disabled_no_network_api_used"
    assert result["remote_code"] == "prohibited"
    assert result["external_inference"] is False
    assert all(backend["model_executed"] is False for backend in result["backends"])
    assert all(
        status == "unsupported_no_cleared_model_asset"
        for backend in result["backends"]
        for status in backend["tasks"].values()
    )


def test_contract_oracle_measures_only_bounded_numeric_effects() -> None:
    result = encoder_adapter_eval.evaluate()
    truncation = next(item for item in result["measurements"] if item["id"] == "truncation")
    assert truncation["truncated"] is True
    assert truncation["left_tokens"] > 8
    assert all(item["int8_oracle_max_abs_error"] <= 1 / 127 for item in result["measurements"])
    assert result["effects"]["calibration"].startswith("unsupported")
    assert result["effects"]["drift"].startswith("unsupported")
    assert "not_backend_or_model" in result["effects"]["quantisation"]


def test_backend_observation_does_not_become_support(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        encoder_adapter_eval,
        "_distribution_version",
        lambda name: "synthetic-version" if name == "transformers" else None,
    )
    backends = {item["backend"]: item for item in encoder_adapter_eval.evaluate()["backends"]}
    assert backends["transformers"]["contract_status"] == "observed_unadmitted"
    assert backends["onnxruntime"]["contract_status"] == "unavailable"
    assert backends["transformers"]["model_executed"] is False


def test_invalid_fixture_is_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"pairs": [], "max_tokens": 0}), encoding="utf-8")
    with pytest.raises(ValueError, match="positive integer"):
        encoder_adapter_eval.evaluate(bad)


def test_cli_writes_receipt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    output = tmp_path / "receipt.json"
    monkeypatch.setattr(sys, "argv", ["encoder-adapter-eval", "--output", str(output)])
    assert encoder_adapter_eval.main() == 0
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert len(receipt["receipt_sha256"]) == 64


def test_checked_in_receipt_preserves_fail_closed_result() -> None:
    receipt_path = (
        encoder_adapter_eval.ROOT / "evaluation/multimodal/encoder-contract-receipt-20260829.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert encoder_adapter_eval.verify(receipt) == []
    assert receipt["execution_mode"] == "offline_contract_oracle_no_model"
    assert all(backend["model_executed"] is False for backend in receipt["backends"])
    assert all(backend["network"] == "disabled" for backend in receipt["backends"])
    assert receipt["effects"]["language"] == "described_not_quality_validated"


def test_tampered_receipt_is_rejected() -> None:
    receipt = encoder_adapter_eval.evaluate()
    receipt["backends"][0]["model_executed"] = True
    assert "receipt hash mismatch" in encoder_adapter_eval.verify(receipt)
    assert any("boundary invalid" in error for error in encoder_adapter_eval.verify(receipt))
