"""Synthetic-only contract evaluation for local Whisper-compatible adapters.

This module does not import, download, or execute a speech model. It normalises
already-produced in-memory result shapes so adapter authors can test the local
contract without audio, network access, remote code, or model redistribution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
FIXTURE_PATH = ROOT / "evaluation/multimodal/speech/synthetic-interface-fixtures.json"
SUPPORTED_BACKENDS = {"faster-whisper", "whisper.cpp"}
QUALITY_DIMENSIONS = (
    "accents",
    "terminology",
    "overlap",
    "noise",
    "timestamps",
    "speaker_uncertainty",
    "hallucination",
)


@dataclass(frozen=True)
class Segment:
    start_ms: int
    end_ms: int
    text: str
    speaker: None = None


def _segment(value: Any) -> Segment:
    """Normalise an object or mapping returned by a faster-whisper iterator."""
    if isinstance(value, dict):
        start, end, text = value.get("start"), value.get("end"), value.get("text")
    else:
        start, end, text = value.start, value.end, value.text
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise ValueError("faster-whisper segment requires numeric start and end offsets")
    return Segment(
        start_ms=round(float(start) * 1000),
        end_ms=round(float(end) * 1000),
        text=str(text).strip(),
    )


def normalise_faster_whisper(result: Any) -> list[Segment]:
    """Normalise ``WhisperModel.transcribe`` output without importing the package."""
    segments = result[0] if isinstance(result, tuple) else result
    return [_segment(value) for value in segments]


def normalise_whisper_cpp(result: dict[str, Any]) -> list[Segment]:
    """Normalise whisper.cpp JSON output using millisecond or centisecond offsets."""
    values = result.get("transcription", result.get("segments"))
    if not isinstance(values, list):
        raise ValueError("whisper.cpp result must contain a transcription or segments list")
    normalised: list[Segment] = []
    for value in values:
        if not isinstance(value, dict):
            raise ValueError("whisper.cpp segments must be objects")
        offsets = value.get("offsets", {})
        if "from" in offsets and "to" in offsets:
            start_ms, end_ms = int(offsets["from"]), int(offsets["to"])
        elif "t0" in value and "t1" in value:
            start_ms, end_ms = int(value["t0"]) * 10, int(value["t1"]) * 10
        else:
            raise ValueError("whisper.cpp segment is missing timestamp offsets")
        normalised.append(Segment(start_ms, end_ms, str(value.get("text", "")).strip()))
    return normalised


def normalise(backend: str, result: Any) -> list[Segment]:
    if backend == "faster-whisper":
        return normalise_faster_whisper(result)
    if backend == "whisper.cpp" and isinstance(result, dict):
        return normalise_whisper_cpp(result)
    raise ValueError(f"unsupported backend or result shape: {backend!r}")


def _words(text: str) -> list[str]:
    return text.casefold().split()


def _edit_distance(left: Iterable[str], right: Iterable[str]) -> int:
    right_values = tuple(right)
    previous = list(range(len(right_values) + 1))
    for row, left_value in enumerate(left, 1):
        current = [row]
        for column, right_value in enumerate(right_values, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (left_value != right_value),
                )
            )
        previous = current
    return previous[-1]


def evaluate_case(case: dict[str, Any], segments: list[Segment]) -> dict[str, Any]:
    expected = case["expected"]
    actual_text = " ".join(segment.text for segment in segments).strip()
    expected_words, actual_words = _words(expected["text"]), _words(actual_text)
    timestamp_errors = [
        abs(segment.start_ms - target["start_ms"]) + abs(segment.end_ms - target["end_ms"])
        for segment, target in zip(segments, expected["segments"], strict=False)
    ]
    is_silence = not expected_words
    return {
        "case_id": case["id"],
        "synthetic": True,
        "word_error_rate": (
            None
            if is_silence
            else _edit_distance(expected_words, actual_words) / len(expected_words)
        ),
        "timestamp_mean_absolute_error_ms": (
            sum(timestamp_errors) / (2 * len(timestamp_errors)) if timestamp_errors else None
        ),
        "hallucination_detected": bool(is_silence and actual_words),
        "segment_count": len(segments),
    }


def interface_receipt(backend: str, outputs: dict[str, Any]) -> dict[str, Any]:
    if backend not in SUPPORTED_BACKENDS:
        raise ValueError(f"unsupported backend: {backend!r}")
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    cases = fixture["cases"]
    results = [evaluate_case(case, normalise(backend, outputs[case["id"]])) for case in cases]
    dimensions = {
        dimension: {
            "status": "measured" if dimension in {"timestamps", "hallucination"} else "unsupported",
            "reason": (
                "synthetic interface fixture measured"
                if dimension in {"timestamps", "hallucination"}
                else "requires an exact model revision and generated audio corpus; neither was executed"
            ),
        }
        for dimension in QUALITY_DIMENSIONS
    }
    dimensions["speaker_uncertainty"] = {
        "status": "unsupported",
        "reason": "diarisation is separately licence and compute gated; no diarisation backend was admitted",
    }
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "profile_id": "speech-local",
        "backend_interface": backend,
        "data_class": "generated_synthetic_descriptors_only",
        "execution": "model_free_interface_contract",
        "network": "disabled_no_network_api_used",
        "telemetry": "none",
        "remote_code": "prohibited",
        "private_audio": False,
        "external_inference": False,
        "redistribution": False,
        "diarisation": "unsupported_pending_exact_licence_and_compute_clearance",
        "results": results,
        "quality_dimensions": dimensions,
        "limitations": [
            "no audio or speech model was executed",
            "interface compatibility is not transcription quality or device support",
            "accents, terminology, overlap and noise remain unmeasured",
            "speaker labels are always absent and diarisation remains unsupported",
        ],
        "supported": False,
    }
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = hashlib.sha256(payload).hexdigest()
    return receipt


def verify(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    digest = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if receipt.get("receipt_sha256") != digest:
        errors.append("receipt hash mismatch")
    if receipt.get("supported") is not False or receipt.get("diarisation") != (
        "unsupported_pending_exact_licence_and_compute_clearance"
    ):
        errors.append("support boundary mismatch")
    if receipt.get("private_audio") is not False or receipt.get("remote_code") != "prohibited":
        errors.append("privacy boundary mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("backend", choices=sorted(SUPPORTED_BACKENDS))
    parser.add_argument("result_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    outputs = json.loads(args.result_json.read_text(encoding="utf-8"))
    rendered = json.dumps(interface_receipt(args.backend, outputs), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
