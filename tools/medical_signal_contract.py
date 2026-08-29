"""Model-free medical-image and ECG contract evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import tracemalloc
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
FIXTURE_PATH = ROOT / "evaluation/multimodal/fixtures/medical-signal-cases.json"


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
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


def _resample_linear(values: list[float], output_samples: int) -> list[float]:
    if output_samples < 1 or not values:
        raise ValueError("signal and output length must be non-empty")
    if output_samples == 1:
        return [values[0]]
    scale = (len(values) - 1) / (output_samples - 1)
    result = []
    for index in range(output_samples):
        position = index * scale
        left = int(position)
        right = min(left + 1, len(values) - 1)
        fraction = position - left
        result.append(values[left] * (1 - fraction) + values[right] * fraction)
    return result


def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    source = case["input"]
    if case["profile_id"] == "medical-imaging-research":
        pixels = source["pixels"]
        resized = _resize_nearest(pixels, source["target_shape"])
        metadata = source["metadata"]
        hostile = bytes.fromhex(source["hostile_payload_hex"])
        direct_identifiers = bool({"PatientName", "PatientID"} & metadata.keys())
        observed = {
            "series_integrity": len(set(source["series_uids"])) == 1,
            "quarantine": source["burned_in_annotation"] == "YES",
            "output_shape": [len(resized), len(resized[0])],
            "direct_identifiers_absent": not direct_identifiers,
            "hostile_file_rejected": len(hostile) < 132 or hostile[128:132] != b"DICM",
            "interpretation_allowed": False,
            "inference_status": "unsupported_not_acquired",
        }
        passed = (
            observed == case["expected"]
            and observed["direct_identifiers_absent"]
            and observed["hostile_file_rejected"]
        )
    else:
        input_samples = source["sampling_hz"] * source["duration_s"]
        output_samples = source["target_sampling_hz"] * source["duration_s"]
        signal = _generated_signal(input_samples, source["noise_amplitude"])
        resampled = _resample_linear(signal, output_samples)
        clean = _generated_signal(input_samples, 0.0)
        measured_noise = (
            sum((a - b) ** 2 for a, b in zip(signal, clean, strict=True)) / input_samples
        ) ** 0.5
        observed = {
            "input_samples": len(signal),
            "output_samples": len(resampled),
            "missing_leads": len(source["leads"]) < source["standard_lead_count"],
            "noisy": measured_noise > 0.1,
            "context_exceeded": source["duration_s"] > source["context_limit_s"],
            "device_units_consistent": len(set(source["device_units"])) == 1,
            "interpretation_allowed": False,
        }
        passed = observed == case["expected"]
    return {
        "case_id": case["id"],
        "profile_id": case["profile_id"],
        "observed": observed,
        "passed": passed,
    }


def run() -> dict[str, Any]:
    fixture = _read(FIXTURE_PATH)
    if fixture.get("data_class") != "generated_synthetic_only":
        raise ValueError("only generated synthetic fixtures are admitted")
    started = time.perf_counter()
    tracemalloc.start()
    results = [evaluate(case) for case in fixture.get("cases", [])]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "scope": "model_free_medical_signal_contract",
        "fixture_sha256": hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest(),
        "data_class": fixture["data_class"],
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
    receipt["receipt_sha256"] = hashlib.sha256(unsigned).hexdigest()
    return receipt


def verify(receipt: dict[str, Any]) -> list[str]:
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
    if summary.get("cases") != len(results) or summary.get("passed") != sum(
        item.get("passed") is True for item in results if isinstance(item, dict)
    ):
        errors.append("summary mismatch")
    if any(item.get("observed", {}).get("interpretation_allowed") for item in results):
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
