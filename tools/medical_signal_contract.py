"""Model-free medical-image and ECG contract evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
import tracemalloc
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools import json_shapes

ROOT = Path(__file__).parents[1]
FIXTURE_PATH = ROOT / "evaluation/multimodal/fixtures/medical-signal-cases.json"


class ImageInput(TypedDict):
    pixels: list[list[float]]
    target_shape: list[int]
    metadata: json_shapes.JsonObject
    hostile_payload_hex: str
    series_uids: list[str]
    burned_in_annotation: str


class SignalInput(TypedDict):
    sampling_hz: int
    target_sampling_hz: int
    duration_s: int
    noise_amplitude: float
    leads: list[str]
    standard_lead_count: int
    context_limit_s: int
    device_units: list[str]


class ImageObservation(TypedDict):
    series_integrity: bool
    quarantine: bool
    output_shape: list[int]
    direct_identifiers_absent: bool
    hostile_file_rejected: bool
    interpretation_allowed: Literal[False]
    inference_status: Literal["unsupported_not_acquired"]


class SignalObservation(TypedDict):
    input_samples: int
    output_samples: int
    missing_leads: bool
    noisy: bool
    context_exceeded: bool
    device_units_consistent: bool
    interpretation_allowed: Literal[False]


class CaseResult(TypedDict):
    case_id: str
    profile_id: Literal["medical-imaging-research", "ecg-research"]
    observed: ImageObservation | SignalObservation
    passed: bool


class Summary(TypedDict):
    cases: int
    passed: int


class DeviceMeasurements(TypedDict):
    elapsed_ms: float
    allocation_peak_bytes: int


class ReceiptBody(TypedDict):
    schema_version: Literal["1.0"]
    scope: Literal["model_free_medical_signal_contract"]
    fixture_sha256: str
    data_class: Literal["generated_synthetic_only"]
    network: Literal["disabled"]
    telemetry: Literal["none"]
    remote_code: Literal["prohibited"]
    clinical_interpretation: Literal["disabled"]
    results: list[CaseResult]
    summary: Summary
    device: DeviceMeasurements
    limitations: list[str]


class MedicalSignalReceipt(ReceiptBody):
    receipt_sha256: str


def _is_strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _is_finite_number(value: object) -> TypeGuard[float]:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _is_image_input(value: object) -> TypeGuard[ImageInput]:
    if not json_shapes.is_object(value):
        return False
    pixels, target = value.get("pixels"), value.get("target_shape")
    if not json_shapes.is_array(pixels) or not pixels:
        return False
    widths: set[int] = set()
    for row in pixels:
        if (
            not json_shapes.is_array(row)
            or not row
            or not all(_is_finite_number(item) for item in row)
        ):
            return False
        widths.add(len(row))
    return (
        len(widths) == 1
        and json_shapes.is_array(target)
        and len(target) == 2
        and all(type(item) is int and item > 0 for item in target)
        and json_shapes.is_object(value.get("metadata"))
        and isinstance(value.get("hostile_payload_hex"), str)
        and _is_strings(value.get("series_uids"))
        and isinstance(value.get("burned_in_annotation"), str)
    )


def _is_signal_input(value: object) -> TypeGuard[SignalInput]:
    if not json_shapes.is_object(value):
        return False
    for key in ("sampling_hz", "target_sampling_hz", "duration_s"):
        item = value.get(key)
        if type(item) is not int or item < 1:
            return False
    return (
        _is_finite_number(value.get("noise_amplitude"))
        and _is_strings(value.get("leads"))
        and _is_strings(value.get("device_units"))
        and type(value.get("standard_lead_count")) is int
        and type(value.get("context_limit_s")) is int
    )


def _read(path: Path) -> json_shapes.JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not json_shapes.is_object(value):
        raise ValueError(f"{path}: expected an object")
    return value


def _resize_nearest(pixels: list[list[float]], target: list[int]) -> list[list[float]]:
    height, width = target
    source_height, source_width = len(pixels), len(pixels[0])
    return [
        [
            pixels[min(source_height - 1, row * source_height // height)][
                min(source_width - 1, column * source_width // width)
            ]
            for column in range(width)
        ]
        for row in range(height)
    ]


def _generated_signal(samples: int, noise: float) -> list[float]:
    return [((index % 20) / 20.0) + (noise if index % 2 else -noise) for index in range(samples)]


def resample_linear(values: list[float], output_samples: int) -> list[float]:
    if output_samples < 1 or not values:
        raise ValueError("signal and output length must be non-empty")
    if output_samples == 1:
        return [values[0]]
    scale = (len(values) - 1) / (output_samples - 1)
    result: list[float] = []
    for index in range(output_samples):
        position = index * scale
        left = int(position)
        right = min(left + 1, len(values) - 1)
        fraction = position - left
        result.append(values[left] * (1 - fraction) + values[right] * fraction)
    return result


def evaluate(case: object) -> CaseResult:
    case = json_shapes.require_object(case, context="medical signal case")
    case_id, profile_id = case.get("id"), case.get("profile_id")
    if not isinstance(case_id, str):
        raise ValueError("medical signal case requires a string id")
    if not isinstance(profile_id, str):
        raise ValueError("unsupported medical signal profile")
    source = case["input"]
    if profile_id == "medical-imaging-research":
        if not _is_image_input(source):
            raise ValueError("invalid medical image input shape")
        pixels = source["pixels"]
        resized = _resize_nearest(pixels, source["target_shape"])
        metadata = source["metadata"]
        hostile = bytes.fromhex(source["hostile_payload_hex"])
        direct_identifiers = bool({"PatientName", "PatientID"} & metadata.keys())
        image_observed: ImageObservation = {
            "series_integrity": len(set(source["series_uids"])) == 1,
            "quarantine": source["burned_in_annotation"] == "YES",
            "output_shape": [len(resized), len(resized[0])],
            "direct_identifiers_absent": not direct_identifiers,
            "hostile_file_rejected": len(hostile) < 132 or hostile[128:132] != b"DICM",
            "interpretation_allowed": False,
            "inference_status": "unsupported_not_acquired",
        }
        passed = (
            image_observed == case["expected"]
            and image_observed["direct_identifiers_absent"]
            and image_observed["hostile_file_rejected"]
        )
        observed = image_observed
    elif profile_id == "ecg-research":
        if not _is_signal_input(source):
            raise ValueError("invalid medical signal input shape")
        input_samples = source["sampling_hz"] * source["duration_s"]
        output_samples = source["target_sampling_hz"] * source["duration_s"]
        signal = _generated_signal(input_samples, source["noise_amplitude"])
        resampled = resample_linear(signal, output_samples)
        clean = _generated_signal(input_samples, 0.0)
        measured_noise = (
            sum((a - b) ** 2 for a, b in zip(signal, clean, strict=True)) / input_samples
        ) ** 0.5
        signal_observed: SignalObservation = {
            "input_samples": len(signal),
            "output_samples": len(resampled),
            "missing_leads": len(source["leads"]) < source["standard_lead_count"],
            "noisy": measured_noise > 0.1,
            "context_exceeded": source["duration_s"] > source["context_limit_s"],
            "device_units_consistent": len(set(source["device_units"])) == 1,
            "interpretation_allowed": False,
        }
        passed = signal_observed == case["expected"]
        observed = signal_observed
    else:
        raise ValueError("unsupported medical signal profile")
    return {
        "case_id": case_id,
        "profile_id": profile_id,
        "observed": observed,
        "passed": passed,
    }


def run() -> MedicalSignalReceipt:
    fixture = _read(FIXTURE_PATH)
    if fixture.get("data_class") != "generated_synthetic_only":
        raise ValueError("only generated synthetic fixtures are admitted")
    cases = fixture.get("cases", [])
    if not json_shapes.is_array(cases):
        raise ValueError("medical signal cases must be an array")
    started = time.perf_counter()
    tracemalloc.start()
    results = [evaluate(case) for case in cases]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    receipt: ReceiptBody = {
        "schema_version": "1.0",
        "scope": "model_free_medical_signal_contract",
        "fixture_sha256": hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest(),
        "data_class": "generated_synthetic_only",
        "network": "disabled",
        "telemetry": "none",
        "remote_code": "prohibited",
        "clinical_interpretation": "disabled",
        "results": results,
        "summary": {"cases": len(results), "passed": sum(item["passed"] for item in results)},
        "device": {
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
            "allocation_peak_bytes": peak,
        },
        "limitations": [
            "model-free synthetic contract only",
            "MONAI inference and clinical interpretation were not acquired or executed",
            "two synthetic ECG leads do not establish diagnostic or device validity",
        ],
    }
    unsigned = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    return {**receipt, "receipt_sha256": hashlib.sha256(unsigned).hexdigest()}


def verify(receipt: object) -> list[str]:
    if not json_shapes.is_object(receipt):
        return ["receipt must be an object"]
    errors: list[str] = []
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    digest = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if receipt.get("receipt_sha256") != digest:
        errors.append("receipt hash mismatch")
    if receipt.get("fixture_sha256") != hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest():
        errors.append("fixture hash mismatch")
    summary = receipt.get("summary", {})
    results = receipt.get("results", [])
    if not json_shapes.is_object(summary):
        return [*errors, "summary must be an object"]
    if not json_shapes.is_array(results):
        return [*errors, "results must be an array"]
    if summary.get("cases") != len(results) or summary.get("passed") != sum(
        item.get("passed") is True for item in json_shapes.object_rows(results)
    ):
        errors.append("summary mismatch")
    interpretation_enabled = False
    for item in results:
        if not json_shapes.is_object(item):
            errors.append("result must be an object")
            continue
        observed = item.get("observed", {})
        if not json_shapes.is_object(observed):
            errors.append("result observed must be an object")
        elif observed.get("interpretation_allowed") is not False:
            interpretation_enabled = True
    if interpretation_enabled:
        errors.append("clinical interpretation must remain disabled")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = run()
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
