"""Generated synthetic checks of model-free signal and admission contracts."""

from __future__ import annotations

import hashlib
import json
import os

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tools import json_shapes
from tools.medical_signal_contract import evaluate, resample_linear, run, verify

_EXAMPLES = int(os.environ.get("SIGNAL_FUZZ_EXAMPLES", "100"))
if not 1 <= _EXAMPLES <= 1000:
    raise ValueError("SIGNAL_FUZZ_EXAMPLES must be between 1 and 1000")
_BOUNDED = settings(max_examples=_EXAMPLES, deadline=1000)


def _signal_case() -> json_shapes.JsonObject:
    return {
        "id": "synthetic-signal",
        "profile_id": "ecg-research",
        "input": {
            "sampling_hz": 4,
            "target_sampling_hz": 8,
            "duration_s": 2,
            "noise_amplitude": 0.0,
            "leads": ["synthetic-lead"],
            "standard_lead_count": 2,
            "context_limit_s": 10,
            "device_units": ["synthetic-units"],
        },
        "expected": {},
    }


@_BOUNDED
@given(
    start=st.integers(-10000, 10000),
    step=st.integers(-100, 100),
    input_size=st.integers(1, 64),
    output_size=st.integers(1, 128),
)
def test_resampling_an_affine_signal_matches_an_independent_coordinate_oracle(
    start: int, step: int, input_size: int, output_size: int
) -> None:
    """Linear signals preserve their endpoints and coordinates after resampling."""
    signal = [float(start + step * index) for index in range(input_size)]
    actual = resample_linear(signal, output_size)
    expected = [
        start + step * (input_size - 1) * index / max(1, output_size - 1)
        for index in range(output_size)
    ]
    assert actual == pytest.approx(expected, rel=1e-12, abs=1e-9)
    assert len(actual) == output_size
    assert actual[0] == signal[0]
    if output_size > 1:
        assert actual[-1] == pytest.approx(signal[-1], rel=1e-12, abs=1e-9)


@_BOUNDED
@given(rate=st.integers(1, 64), target=st.integers(1, 64), duration=st.integers(1, 8))
def test_generated_signal_counts_never_enable_interpretation(
    rate: int, target: int, duration: int
) -> None:
    """Expected-output data cannot turn a synthetic calculation into clinical authority."""
    case = _signal_case()
    source = json_shapes.require_object(case["input"], context="synthetic input")
    source.update(sampling_hz=rate, target_sampling_hz=target, duration_s=duration)
    case["expected"] = {"interpretation_allowed": True}
    result = evaluate(case)
    observed = json_shapes.require_object(result["observed"], context="synthetic observation")
    assert observed["input_samples"] == rate * duration
    assert observed["output_samples"] == target * duration
    assert observed["interpretation_allowed"] is False
    assert result["passed"] is False


@_BOUNDED
@given(
    field=st.sampled_from(["sampling_hz", "target_sampling_hz", "duration_s"]),
    value=st.one_of(st.integers(-(10**12), 0), st.booleans(), st.none(), st.text(max_size=64)),
)
def test_invalid_sampling_dimensions_fail_before_signal_allocation(
    field: str, value: object
) -> None:
    """Boolean, nonpositive and incorrectly typed dimensions cannot allocate a signal."""
    case = _signal_case()
    source = json_shapes.require_object(case["input"], context="synthetic input")
    source[field] = value
    with pytest.raises(ValueError, match=r"^invalid medical signal input shape$"):
        evaluate(case)


@_BOUNDED
@given(height=st.integers(1, 16), width=st.integers(1, 16), identifier=st.text(max_size=64))
def test_identifier_metadata_cannot_acquire_a_passing_image_receipt(
    height: int, width: int, identifier: str
) -> None:
    """Even an empty or unusual identifier value keeps the input unqualified."""
    case: json_shapes.JsonObject = {
        "id": "synthetic-image",
        "profile_id": "medical-imaging-research",
        "input": {
            "pixels": [[0.0, 1.0], [2.0, 3.0]],
            "target_shape": [height, width],
            "metadata": {"PatientID": identifier},
            "hostile_payload_hex": "00",
            "series_uids": ["synthetic-series"],
            "burned_in_annotation": "NO",
        },
        "expected": {},
    }
    first = evaluate(case)
    case["expected"] = first["observed"]
    second = evaluate(case)
    observed = json_shapes.require_object(second["observed"], context="synthetic observation")
    assert observed["output_shape"] == [height, width]
    assert observed["direct_identifiers_absent"] is False
    assert observed["interpretation_allowed"] is False
    assert second["passed"] is False


@_BOUNDED
@given(replacement=st.one_of(st.just(True), st.none(), st.integers(), st.text(max_size=64)))
def test_rehashing_does_not_admit_an_interpretation_permission(replacement: object) -> None:
    """A valid digest alone cannot authorise interpretation in a modified receipt."""
    receipt: json_shapes.JsonObject = dict(run())
    results = receipt["results"]
    assert json_shapes.is_array(results)
    result = json_shapes.require_object(results[0], context="synthetic result")
    observed = json_shapes.require_object(result["observed"], context="synthetic observation")
    observed["interpretation_allowed"] = replacement
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    errors = verify(receipt)
    assert "receipt hash mismatch" not in errors
    assert "clinical interpretation must remain disabled" in errors
