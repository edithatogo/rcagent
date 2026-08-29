from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from tools.speech_adapter_eval import (
    interface_receipt,
    main,
    normalise_faster_whisper,
    normalise_whisper_cpp,
    verify,
)


def _faster_outputs():
    return {
        "timestamp-plain": (
            [
                SimpleNamespace(start=0.0, end=1.0, text=" synthetic alpha"),
                SimpleNamespace(start=1.1, end=2.2, text=" synthetic beta"),
            ],
            SimpleNamespace(language="en"),
        ),
        "silence-hallucination": ([], SimpleNamespace(language="en")),
    }


def _cpp_outputs():
    return {
        "timestamp-plain": {
            "transcription": [
                {"offsets": {"from": 0, "to": 1000}, "text": "synthetic alpha"},
                {"offsets": {"from": 1100, "to": 2200}, "text": "synthetic beta"},
            ]
        },
        "silence-hallucination": {"transcription": []},
    }


@pytest.mark.parametrize(
    ("backend", "outputs"),
    [("faster-whisper", _faster_outputs()), ("whisper.cpp", _cpp_outputs())],
)
def test_synthetic_interfaces_measure_only_timestamps_and_hallucination(backend, outputs) -> None:
    receipt = interface_receipt(backend, outputs)
    assert receipt["supported"] is False
    assert receipt["private_audio"] is False
    assert receipt["diarisation"].startswith("unsupported")
    assert receipt["quality_dimensions"]["timestamps"]["status"] == "measured"
    assert receipt["quality_dimensions"]["hallucination"]["status"] == "measured"
    for dimension in ("accents", "terminology", "overlap", "noise", "speaker_uncertainty"):
        assert receipt["quality_dimensions"][dimension]["status"] == "unsupported"
    assert receipt["results"][0]["word_error_rate"] == 0
    assert receipt["results"][0]["timestamp_mean_absolute_error_ms"] == 0
    assert receipt["results"][1]["hallucination_detected"] is False
    assert len(receipt["receipt_sha256"]) == 64
    assert verify(receipt) == []


def test_hallucination_is_detected_for_nonempty_silence_output() -> None:
    outputs = _cpp_outputs()
    outputs["silence-hallucination"] = {
        "transcription": [{"offsets": {"from": 0, "to": 500}, "text": "invented"}]
    }
    receipt = interface_receipt("whisper.cpp", outputs)
    assert receipt["results"][1]["hallucination_detected"] is True


def test_whisper_cpp_centisecond_offsets_and_invalid_shape() -> None:
    segments = normalise_whisper_cpp({"segments": [{"t0": 2, "t1": 7, "text": "x"}]})
    assert (segments[0].start_ms, segments[0].end_ms) == (20, 70)
    with pytest.raises(ValueError, match="timestamp offsets"):
        normalise_whisper_cpp({"segments": [{"text": "x"}]})


def test_faster_whisper_mapping_shape_and_unknown_backend() -> None:
    segment = normalise_faster_whisper([{"start": 0.1, "end": 0.2, "text": " x "}])[0]
    assert (segment.start_ms, segment.end_ms, segment.text, segment.speaker) == (
        100,
        200,
        "x",
        None,
    )
    with pytest.raises(ValueError, match="unsupported backend"):
        interface_receipt("other", {})


def test_tampered_speech_receipt_is_rejected() -> None:
    receipt = interface_receipt("whisper.cpp", _cpp_outputs())
    receipt["supported"] = True
    assert "receipt hash mismatch" in verify(receipt)
    assert "support boundary mismatch" in verify(receipt)


def test_invalid_numeric_segment_and_privacy_tamper_fail() -> None:
    with pytest.raises(ValueError, match="numeric start and end"):
        normalise_faster_whisper([{"start": "bad", "end": 1, "text": "x"}])
    receipt = interface_receipt("whisper.cpp", _cpp_outputs())
    receipt["private_audio"] = True
    assert "privacy boundary mismatch" in verify(receipt)


def test_cli_writes_and_prints_receipts(monkeypatch, tmp_path, capsys) -> None:
    source = tmp_path / "outputs.json"
    source.write_text(json.dumps(_cpp_outputs()), encoding="utf-8")
    output = tmp_path / "receipt.json"
    monkeypatch.setattr("sys.argv", ["speech", "whisper.cpp", str(source), "--output", str(output)])
    assert main() == 0
    assert verify(json.loads(output.read_text(encoding="utf-8"))) == []
    monkeypatch.setattr("sys.argv", ["speech", "whisper.cpp", str(source)])
    assert main() == 0
    assert '"supported": false' in capsys.readouterr().out
