"""Synthetic-only contract evaluation for local Whisper-compatible adapters.

This module does not import, download, or execute a speech model. It normalises
already-produced in-memory result shapes so adapter authors can test the local
contract without audio, network access, remote code, or model redistribution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools import json_shapes

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


class ExpectedSegment(TypedDict):
    start_ms: int
    end_ms: int


class ExpectedOutput(TypedDict):
    text: str
    segments: list[ExpectedSegment]


class EvaluationCase(TypedDict):
    id: str
    expected: ExpectedOutput


class CaseResult(TypedDict):
    case_id: str
    synthetic: Literal[True]
    word_error_rate: float | None
    timestamp_mean_absolute_error_ms: float | None
    hallucination_detected: bool
    segment_count: int


class QualityDimension(TypedDict):
    status: Literal["measured", "unsupported"]
    reason: str


class ReceiptBody(TypedDict):
    schema_version: Literal["1.0"]
    profile_id: Literal["speech-local"]
    backend_interface: str
    data_class: Literal["generated_synthetic_descriptors_only"]
    execution: Literal["model_free_interface_contract"]
    network: Literal["disabled_no_network_api_used"]
    telemetry: Literal["none"]
    remote_code: Literal["prohibited"]
    private_audio: Literal[False]
    external_inference: Literal[False]
    redistribution: Literal[False]
    diarisation: Literal["unsupported_pending_exact_licence_and_compute_clearance"]
    results: list[CaseResult]
    quality_dimensions: dict[str, QualityDimension]
    limitations: list[str]
    supported: Literal[False]


class SpeechReceipt(ReceiptBody):
    receipt_sha256: str


def _seconds_to_ms(value: object) -> int:
    message = "faster-whisper segment requires numeric start and end offsets"
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(message)
    try:
        milliseconds = float(value) * 1000
        if not math.isfinite(milliseconds):
            raise ValueError(message)
        return round(milliseconds)
    except OverflowError as exc:
        raise ValueError(message) from exc


def _segment(value: object) -> Segment:
    """Normalise an object or mapping returned by a faster-whisper iterator."""
    if json_shapes.is_object(value):
        start, end, text = value.get("start"), value.get("end"), value.get("text")
    else:
        start: object = getattr(value, "start", None)
        end: object = getattr(value, "end", None)
        text: object = getattr(value, "text", None)
    start_ms, end_ms = _seconds_to_ms(start), _seconds_to_ms(end)
    if not isinstance(text, str):
        raise ValueError("faster-whisper segment text must be a string")
    return Segment(
        start_ms=start_ms,
        end_ms=end_ms,
        text=text.strip(),
    )


def _is_tuple(value: object) -> TypeGuard[tuple[object, ...]]:
    return isinstance(value, tuple)


def _is_iterable(value: object) -> TypeGuard[Iterable[object]]:
    return isinstance(value, Iterable)


def normalise_faster_whisper(result: object) -> list[Segment]:
    """Normalise ``WhisperModel.transcribe`` output without importing the package."""
    if _is_tuple(result):
        if not result:
            raise ValueError("faster-whisper result must contain a segments iterable")
        segments = result[0]
    else:
        segments = result
    if (
        not _is_iterable(segments)
        or isinstance(segments, (str, bytes))
        or json_shapes.is_object(segments)
    ):
        raise ValueError("faster-whisper result must contain a segments iterable")
    return [_segment(value) for value in segments]


def _cpp_offset(value: object) -> int:
    message = "whisper.cpp offsets must be finite numbers or integer strings"
    if not isinstance(value, (int, float, str)) or isinstance(value, bool):
        raise ValueError(message)
    try:
        return int(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError(message) from exc


def normalise_whisper_cpp(result: object) -> list[Segment]:
    """Normalise whisper.cpp JSON output using millisecond or centisecond offsets."""
    if not json_shapes.is_object(result):
        raise ValueError("whisper.cpp result must contain a transcription or segments list")
    values = result.get("transcription", result.get("segments"))
    if not json_shapes.is_array(values):
        raise ValueError("whisper.cpp result must contain a transcription or segments list")
    normalised: list[Segment] = []
    for value in values:
        if not json_shapes.is_object(value):
            raise ValueError("whisper.cpp segments must be objects")
        offsets = value.get("offsets", {})
        if not json_shapes.is_object(offsets):
            raise ValueError("whisper.cpp timestamp offsets must be an object")
        if "from" in offsets and "to" in offsets:
            start_ms, end_ms = _cpp_offset(offsets["from"]), _cpp_offset(offsets["to"])
        elif "t0" in value and "t1" in value:
            start_ms, end_ms = _cpp_offset(value["t0"]) * 10, _cpp_offset(value["t1"]) * 10
        else:
            raise ValueError("whisper.cpp segment is missing timestamp offsets")
        text = value.get("text")
        if not isinstance(text, str):
            raise ValueError("whisper.cpp segment text must be a string")
        normalised.append(Segment(start_ms, end_ms, text.strip()))
    return normalised


def normalise(backend: str, result: object) -> list[Segment]:
    if backend == "faster-whisper":
        return normalise_faster_whisper(result)
    if backend == "whisper.cpp" and json_shapes.is_object(result):
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


def _is_case(value: object) -> TypeGuard[EvaluationCase]:
    if not json_shapes.is_object(value) or not isinstance(value.get("id"), str):
        return False
    expected = value.get("expected")
    if not json_shapes.is_object(expected) or not isinstance(expected.get("text"), str):
        return False
    segments = expected.get("segments")
    return json_shapes.is_array(segments) and all(
        json_shapes.is_object(segment)
        and all(type(segment.get(key)) is int for key in ("start_ms", "end_ms"))
        for segment in segments
    )


def evaluate_case(case: object, segments: list[Segment]) -> CaseResult:
    if not _is_case(case):
        raise ValueError("speech fixture case requires text and integer timestamp expectations")
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


def interface_receipt(backend: str, outputs: object) -> SpeechReceipt:
    if backend not in SUPPORTED_BACKENDS:
        raise ValueError(f"unsupported backend: {backend!r}")
    outputs = json_shapes.require_object(outputs, context="speech outputs")
    parsed: object = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    fixture = json_shapes.require_object(parsed, context="speech fixture")
    cases = fixture["cases"]
    if not json_shapes.is_array(cases):
        raise ValueError("speech fixture cases must be an array")
    results: list[CaseResult] = []
    for case in cases:
        if not _is_case(case):
            raise ValueError("speech fixture case requires text and integer timestamp expectations")
        results.append(evaluate_case(case, normalise(backend, outputs[case["id"]])))
    dimensions: dict[str, QualityDimension] = {
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
    receipt: ReceiptBody = {
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
    return {**receipt, "receipt_sha256": hashlib.sha256(payload).hexdigest()}


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
    outputs: object = json.loads(args.result_json.read_text(encoding="utf-8"))
    rendered = json.dumps(interface_receipt(args.backend, outputs), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
