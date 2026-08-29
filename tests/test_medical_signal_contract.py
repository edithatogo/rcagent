from __future__ import annotations

import json
from copy import deepcopy

import pytest

from tools.medical_signal_contract import (
    FIXTURE_PATH,
    _read,
    _resample_linear,
    evaluate,
    main,
    run,
    verify,
)


def test_model_free_medical_and_signal_contract_passes() -> None:
    receipt = run()
    assert receipt["summary"] == {"cases": 3, "passed": 3}
    assert verify(receipt) == []
    assert all(
        result["observed"]["interpretation_allowed"] is False for result in receipt["results"]
    )


def test_image_identifiers_fail_closed() -> None:
    case = {
        "id": "image",
        "profile_id": "medical-imaging-research",
        "input": {
            "series_uids": ["one", "one"],
            "metadata": {"PatientName": "synthetic"},
            "burned_in_annotation": "YES",
            "pixels": [[0, 1], [2, 3]],
            "target_shape": [4, 4],
            "hostile_payload_hex": "00",
        },
        "expected": {
            "series_integrity": True,
            "quarantine": True,
            "output_shape": [4, 4],
            "direct_identifiers_absent": False,
            "hostile_file_rejected": True,
            "interpretation_allowed": False,
            "inference_status": "unsupported_not_acquired",
        },
    }
    assert evaluate(case)["passed"] is False


def test_receipt_tampering_is_rejected() -> None:
    receipt = run()
    changed = deepcopy(receipt)
    changed["summary"]["passed"] = 99
    assert "summary mismatch" in verify(changed)
    changed = deepcopy(receipt)
    changed["results"][0]["observed"]["interpretation_allowed"] = True
    assert "clinical interpretation must remain disabled" in verify(changed)


def test_checked_receipt_matches_current_fixture_and_verifies() -> None:
    receipt_path = FIXTURE_PATH.parent.parent / "medical-signal-contract-v1.json"
    assert verify(json.loads(receipt_path.read_text(encoding="utf-8"))) == []


def test_invalid_inputs_and_cli_paths(monkeypatch, tmp_path, capsys) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        _resample_linear([], 0)
    assert _resample_linear([2.0], 1) == [2.0]
    invalid = tmp_path / "invalid.json"
    invalid.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="expected an object"):
        _read(invalid)
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["medical", "--output", str(output)])
    assert main() == 0
    assert verify(json.loads(output.read_text(encoding="utf-8"))) == []
    monkeypatch.setattr("sys.argv", ["medical"])
    assert main() == 0
    assert "receipt_sha256" in capsys.readouterr().out
