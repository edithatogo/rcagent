from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools import json_shapes, medical_signal_contract
from tools.medical_signal_contract import (
    FIXTURE_PATH,
    evaluate,
    main,
    resample_linear,
    run,
    verify,
)

MALFORMED_IMAGE_INPUTS: list[tuple[str, object]] = [
    ("target_shape", [0, 4]),
    ("pixels", [[0, 1], []]),
    ("series_uids", [[]]),
]


def fixture_cases() -> list[json_shapes.JsonObject]:
    parsed: object = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    fixture = json_shapes.require_object(parsed, context="stored medical signal fixture")
    cases = fixture["cases"]
    assert json_shapes.is_array(cases)
    return [json_shapes.require_object(case, context="stored case") for case in cases]


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
    tampered: json_shapes.JsonObject = deepcopy(dict(receipt))
    results = tampered["results"]
    assert json_shapes.is_array(results)
    result = json_shapes.require_object(results[0], context="tampered result")
    observed = json_shapes.require_object(result["observed"], context="tampered observation")
    observed["interpretation_allowed"] = True
    assert "clinical interpretation must remain disabled" in verify(tampered)


@pytest.mark.parametrize(("field", "value"), MALFORMED_IMAGE_INPUTS)
def test_malformed_image_inputs_are_rejected(field: str, value: object) -> None:
    case = fixture_cases()[0]
    source = json_shapes.require_object(case["input"], context="synthetic image input")
    source[field] = value
    with pytest.raises(ValueError, match="invalid medical image input shape"):
        evaluate(case)


def test_unknown_profile_and_boolean_sampling_rate_are_rejected() -> None:
    case = fixture_cases()[1]
    case["profile_id"] = "unregistered"
    with pytest.raises(ValueError, match="unsupported medical signal profile"):
        evaluate(case)
    case["profile_id"] = "ecg-research"
    source = json_shapes.require_object(case["input"], context="synthetic signal input")
    source["sampling_hz"] = True
    with pytest.raises(ValueError, match="invalid medical signal input shape"):
        evaluate(case)


@pytest.mark.parametrize("field", ["summary", "results", "observed", "interpretation_allowed"])
def test_rehashed_malformed_receipt_fields_are_rejected(field: str) -> None:
    receipt: json_shapes.JsonObject = dict(run())
    if field in {"summary", "results"}:
        receipt[field] = None
    else:
        results = receipt["results"]
        assert json_shapes.is_array(results)
        result = json_shapes.require_object(results[0], context="synthetic result")
        if field == "observed":
            result[field] = None
        else:
            observed = json_shapes.require_object(
                result["observed"], context="synthetic observation"
            )
            observed[field] = None
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    errors = verify(receipt)
    assert errors
    assert "receipt hash mismatch" not in errors


def test_checked_receipt_matches_current_fixture_and_verifies() -> None:
    receipt_path = FIXTURE_PATH.parent.parent / "medical-signal-contract-v1.json"
    receipt: object = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert verify(receipt) == []


def test_invalid_inputs_and_cli_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        resample_linear([], 0)
    assert resample_linear([2.0], 1) == [2.0]
    invalid = tmp_path / "invalid.json"
    invalid.write_text("[]", encoding="utf-8")
    with monkeypatch.context() as patch:
        patch.setattr(medical_signal_contract, "FIXTURE_PATH", invalid)
        with pytest.raises(ValueError, match="expected an object"):
            run()
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["medical", "--output", str(output)])
    assert main() == 0
    receipt: object = json.loads(output.read_text(encoding="utf-8"))
    assert verify(receipt) == []
    monkeypatch.setattr("sys.argv", ["medical"])
    assert main() == 0
    assert "receipt_sha256" in capsys.readouterr().out
