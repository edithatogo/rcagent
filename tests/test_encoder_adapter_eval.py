from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

from tools import encoder_adapter_eval, json_shapes

MALFORMED_FIXTURES: list[json_shapes.JsonObject] = [
    {"pairs": [], "max_tokens": True},
    {"pairs": [None], "max_tokens": 8},
    {
        "pairs": [{"id": "bad", "language": "en", "domain": "synthetic", "left": [], "right": "x"}],
        "max_tokens": 8,
    },
]


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
    def version(name: str) -> str | None:
        return "synthetic-version" if name == "transformers" else None

    monkeypatch.setattr(encoder_adapter_eval, "_distribution_version", version)
    backends = {item["backend"]: item for item in encoder_adapter_eval.evaluate()["backends"]}
    assert backends["transformers"]["contract_status"] == "observed_unadmitted"
    assert backends["onnxruntime"]["contract_status"] == "unavailable"
    assert backends["transformers"]["model_executed"] is False


def test_invalid_fixture_is_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"pairs": [], "max_tokens": 0}), encoding="utf-8")
    with pytest.raises(ValueError, match="positive integer"):
        encoder_adapter_eval.evaluate(bad)


@pytest.mark.parametrize("fixture", MALFORMED_FIXTURES)
def test_malformed_encoder_fixture_is_rejected(tmp_path: Path, fixture: object) -> None:
    path = tmp_path / "malformed.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    with pytest.raises(ValueError, match=r"positive integer|string id"):
        encoder_adapter_eval.evaluate(path)


def test_cli_writes_receipt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    output = tmp_path / "receipt.json"
    monkeypatch.setattr(sys, "argv", ["encoder-adapter-eval", "--output", str(output)])
    assert encoder_adapter_eval.main() == 0
    value: object = json.loads(output.read_text(encoding="utf-8"))
    receipt = json_shapes.require_object(value, context="CLI encoder receipt")
    digest = receipt["receipt_sha256"]
    assert isinstance(digest, str)
    assert len(digest) == 64


def test_checked_in_receipt_preserves_fail_closed_result() -> None:
    receipt_path = (
        encoder_adapter_eval.ROOT / "evaluation/multimodal/encoder-contract-receipt-20260829.json"
    )
    value: object = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt = json_shapes.require_object(value, context="stored encoder receipt")
    assert encoder_adapter_eval.verify(receipt) == []
    assert receipt["execution_mode"] == "offline_contract_oracle_no_model"
    raw_backends = receipt["backends"]
    assert json_shapes.is_array(raw_backends)
    backends = [json_shapes.require_object(item, context="stored backend") for item in raw_backends]
    assert all(backend["model_executed"] is False for backend in backends)
    assert all(backend["network"] == "disabled" for backend in backends)
    effects = json_shapes.require_object(receipt["effects"], context="stored effects")
    assert effects["language"] == "described_not_quality_validated"


def test_tampered_receipt_is_rejected() -> None:
    receipt: json_shapes.JsonObject = dict(encoder_adapter_eval.evaluate())
    backends = receipt["backends"]
    assert json_shapes.is_array(backends)
    backend = json_shapes.require_object(backends[0], context="tampered backend")
    backend["model_executed"] = True
    assert "receipt hash mismatch" in encoder_adapter_eval.verify(receipt)
    assert any("boundary invalid" in error for error in encoder_adapter_eval.verify(receipt))


@pytest.mark.parametrize("backends", [None, {}, [None]])
def test_rehashed_malformed_backends_return_errors(backends: object) -> None:
    receipt: json_shapes.JsonObject = dict(encoder_adapter_eval.evaluate())
    receipt["backends"] = backends
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    errors = encoder_adapter_eval.verify(receipt)
    assert errors
    assert "receipt hash mismatch" not in errors


def test_cli_prints_and_non_synthetic_receipt_fails(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["encoder-adapter-eval"])
    assert encoder_adapter_eval.main() == 0
    assert '"data_class": "generated_synthetic_only"' in capsys.readouterr().out
    receipt: json_shapes.JsonObject = dict(encoder_adapter_eval.evaluate())
    receipt["data_class"] = "private"
    assert "data class is not synthetic" in encoder_adapter_eval.verify(receipt)
