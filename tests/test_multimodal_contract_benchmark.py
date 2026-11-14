from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools import json_shapes
from tools.multimodal_contract_benchmark import RECEIPT, main, run, verify


def stored_receipt() -> json_shapes.JsonObject:
    value: object = json.loads(RECEIPT.read_text(encoding="utf-8"))
    return json_shapes.require_object(value, context="stored benchmark receipt")


def result_rows(receipt: json_shapes.JsonObject) -> list[json_shapes.JsonObject]:
    values = receipt["results"]
    assert json_shapes.is_array(values)
    return [json_shapes.require_object(value, context="benchmark result") for value in values]


def test_all_ci_contract_profiles_pass_conservative_benchmark() -> None:
    result = run()
    assert result["summary"] == {"profiles": 5, "passed": 5}
    assert verify(result) == []


def test_checked_receipt_is_valid_and_tampering_fails() -> None:
    receipt = stored_receipt()
    assert verify(receipt) == []
    changed = deepcopy(receipt)
    result_rows(changed)[0]["passed"] = False
    assert verify(changed)


def test_rehashed_over_threshold_receipt_still_fails_semantically() -> None:
    receipt = stored_receipt()
    result_rows(receipt)[0]["elapsed_ms"] = 2000.001
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert any("benchmark result failed" in error for error in verify(receipt))


@pytest.mark.parametrize("results", [None, {}, [None], [{"profile_id": []}]])
def test_rehashed_malformed_results_return_errors(results: object) -> None:
    receipt = stored_receipt()
    receipt["results"] = results
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    errors = verify(receipt)
    assert errors
    assert "receipt hash mismatch" not in errors


def test_extra_malformed_profile_is_not_hidden_by_complete_coverage() -> None:
    receipt = stored_receipt()
    results = result_rows(receipt)
    extra = deepcopy(results[0])
    extra["profile_id"] = []
    receipt["results"] = [*results, extra]
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert "profile coverage mismatch" in verify(receipt)


def test_profile_coverage_and_cli_serialization(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    receipt = stored_receipt()
    assert verify(receipt) == []
    # CLI serialization is independent of live host resource measurements;
    # test_all_ci_contract_profiles_pass_conservative_benchmark measures those.
    monkeypatch.setattr("tools.multimodal_contract_benchmark.run", lambda: deepcopy(receipt))
    changed = deepcopy(receipt)
    changed["results"] = result_rows(changed)[:-1]
    assert "profile coverage mismatch" in verify(changed)
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["benchmark", "--output", str(output)])
    assert main() == 0
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
    monkeypatch.setattr("sys.argv", ["benchmark"])
    assert main() == 0
    assert json.loads(capsys.readouterr().out) == receipt


def test_cli_returns_failure_and_preserves_failed_receipt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    receipt = stored_receipt()
    result_rows(receipt)[0]["elapsed_ms"] = 2000.001
    result_rows(receipt)[0]["passed"] = False
    summary = json_shapes.require_object(receipt["summary"], context="benchmark summary")
    passed = summary["passed"]
    assert isinstance(passed, int)
    summary["passed"] = passed - 1
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    monkeypatch.setattr("tools.multimodal_contract_benchmark.run", lambda: deepcopy(receipt))
    output = tmp_path / "failed.json"
    monkeypatch.setattr("sys.argv", ["benchmark", "--output", str(output)])
    assert main() == 1
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
