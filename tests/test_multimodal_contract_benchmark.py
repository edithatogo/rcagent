from __future__ import annotations

import hashlib
import json
from copy import deepcopy

from tools.multimodal_contract_benchmark import RECEIPT, main, run, verify


def test_all_ci_contract_profiles_pass_conservative_benchmark() -> None:
    result = run()
    assert result["summary"] == {"profiles": 5, "passed": 5}
    assert verify(result) == []


def test_checked_receipt_is_valid_and_tampering_fails() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert verify(receipt) == []
    changed = deepcopy(receipt)
    changed["results"][0]["passed"] = False
    assert verify(changed)


def test_rehashed_over_threshold_receipt_still_fails_semantically() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    receipt["results"][0]["elapsed_ms"] = 2000.001
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert any("benchmark result failed" in error for error in verify(receipt))


def test_profile_coverage_and_cli_serialization(monkeypatch, tmp_path, capsys) -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert verify(receipt) == []
    # CLI serialization is independent of live host resource measurements;
    # test_all_ci_contract_profiles_pass_conservative_benchmark measures those.
    monkeypatch.setattr("tools.multimodal_contract_benchmark.run", lambda: deepcopy(receipt))
    changed = deepcopy(receipt)
    changed["results"].pop()
    assert "profile coverage mismatch" in verify(changed)
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["benchmark", "--output", str(output)])
    assert main() == 0
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
    monkeypatch.setattr("sys.argv", ["benchmark"])
    assert main() == 0
    assert json.loads(capsys.readouterr().out) == receipt


def test_cli_returns_failure_and_preserves_failed_receipt(monkeypatch, tmp_path) -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    receipt["results"][0]["elapsed_ms"] = 2000.001
    receipt["results"][0]["passed"] = False
    receipt["summary"]["passed"] -= 1
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    monkeypatch.setattr("tools.multimodal_contract_benchmark.run", lambda: deepcopy(receipt))
    output = tmp_path / "failed.json"
    monkeypatch.setattr("sys.argv", ["benchmark", "--output", str(output)])
    assert main() == 1
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
