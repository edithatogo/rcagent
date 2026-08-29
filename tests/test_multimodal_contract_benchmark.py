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


def test_profile_coverage_and_cli_output_fail_closed(monkeypatch, tmp_path) -> None:
    receipt = run()
    receipt["results"].pop()
    assert "profile coverage mismatch" in verify(receipt)
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["benchmark", "--output", str(output)])
    assert main() == 0
    assert verify(json.loads(output.read_text(encoding="utf-8"))) == []
    monkeypatch.setattr("sys.argv", ["benchmark"])
    assert main() == 0
