"""Synthetic fixtures only; no model invocation or primary study evidence."""

import hashlib
import json
from typing import Any, cast

import pytest

from tools import native_completion as subject


def response():
    return {
        "index": 0,
        "content": "  Synthetic response\r\n\n",
        "tokens": [],
        "id_slot": 0,
        "stop": True,
        "model": "synthetic-model",
        "tokens_predicted": 8,
        "tokens_evaluated": 12,
        "generation_settings": {
            "seed": 42,
            "temperature": 0.0,
            "n_predict": 512,
            "max_tokens": 512,
            "stream": False,
            "ignore_eos": False,
            "stop": [],
        },
        "prompt": "<synthetic-detokenized-prompt>",
        "has_new_line": True,
        "truncated": False,
        "stop_type": "eos",
        "stopping_word": "",
        "tokens_cached": 0,
        "timings": {},
    }


def decode(value):
    return subject.decode_completion(json.dumps(value).encode(), expected_model="synthetic-model")


@pytest.mark.parametrize("content", ["READY", "READY\n", "\n", " a\r\n\n", "é e\u0301 🌿", "\x00"])
def test_preserves_content_exactly(content):
    value = response()
    value["content"] = content
    raw = json.dumps(value).encode()
    result = subject.decode_completion(raw, expected_model="synthetic-model")
    assert result["content"] == content
    assert result["content_sha256"] == hashlib.sha256(content.encode()).hexdigest()
    assert result["raw_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["content_bytes"] == len(content.encode())
    assert result["admitted"] is False
    assert result["study_unlocked"] is False
    assert result["status"] == "native_completion_consistent"
    assert "request-binding-not-verified" in result["limitations"]


def test_detokenized_prompt_is_not_request_echo():
    value = response()
    value["prompt"] = "<BOS> synthetic prompt"
    result = decode(value)
    assert (
        result["detokenized_prompt_sha256"] == hashlib.sha256(value["prompt"].encode()).hexdigest()
    )


@pytest.mark.parametrize(
    "raw",
    [
        b"",
        b"READY\n\nExiting...\n",
        b"{} {}",
        b"[]",
        b"null",
        b"42",
        b"\xff",
        b'{"content":"a","content":"b"}',
        b'{"a":{"x":1,"x":2}}',
        b'{"x": NaN}',
        b'{"x": Infinity}',
        b'{"x": 1e999}',
        b'{"x":"\\ud800"}',
        b"[" * 2000 + b"]" * 2000,
    ],
)
def test_rejects_bad_json(raw):
    with pytest.raises(ValueError):
        subject.decode_completion(raw, expected_model="synthetic-model")


def test_rejects_oversized_and_nonbytes():
    for raw in (b" " * (subject.MAX_BYTES + 1), "{}", bytearray(b"{}")):
        with pytest.raises(ValueError):
            subject.decode_completion(cast(Any, raw), expected_model="synthetic-model")


@pytest.mark.parametrize("model", [None, "", 1, "\ud800"])
def test_rejects_bad_expected_model(model):
    with pytest.raises(ValueError):
        subject.decode_completion(json.dumps(response()).encode(), expected_model=model)


@pytest.mark.parametrize("field", list(response()))
def test_requires_every_native_field(field):
    value = response()
    del value[field]
    with pytest.raises(ValueError):
        decode(value)


@pytest.mark.parametrize(
    "field,value",
    [
        ("error", {}),
        ("choices", []),
        ("unexpected", True),
        ("content", ""),
        ("content", None),
        ("prompt", []),
        ("prompt", ""),
        ("model", "another-model"),
        ("index", 1),
        ("index", False),
        ("stop", False),
        ("stop", 1),
        ("truncated", True),
        ("truncated", 0),
        ("stop_type", "limit"),
        ("stop_type", "none"),
        ("stop_type", "word"),
        ("stopping_word", "STOP"),
        ("has_new_line", 1),
        ("tokens_predicted", 0),
        ("tokens_predicted", 513),
        ("tokens_predicted", True),
        ("tokens_evaluated", 0),
        ("tokens_evaluated", 2049),
        ("tokens_cached", -1),
        ("tokens_cached", 2049),
        ("id_slot", -1),
        ("tokens", [False]),
        ("tokens", [-1]),
        ("tokens", ""),
        ("timings", []),
        ("generation_settings", []),
    ],
)
def test_rejects_invalid_native_fields(field, value):
    fixture = response()
    fixture[field] = value
    with pytest.raises(ValueError):
        decode(fixture)


@pytest.mark.parametrize(
    "field,value",
    [
        ("seed", 43),
        ("seed", 42.0),
        ("temperature", False),
        ("temperature", 1),
        ("n_predict", -1),
        ("max_tokens", 512.0),
        ("stream", True),
        ("stream", 0),
        ("ignore_eos", True),
        ("ignore_eos", 0),
        ("stop", ["STOP"]),
        ("stop", None),
    ],
)
def test_rejects_settings_mismatch(field, value):
    fixture = response()
    fixture["generation_settings"][field] = value
    with pytest.raises(ValueError):
        decode(fixture)


@pytest.mark.parametrize("field", list(response()["generation_settings"]))
def test_requires_selected_settings(field):
    fixture = response()
    del fixture["generation_settings"][field]
    with pytest.raises(ValueError):
        decode(fixture)


def test_native_tokens_and_other_settings_are_retained_in_raw_only():
    fixture = response()
    fixture["tokens"] = [1, 2]
    fixture["generation_settings"]["top_k"] = 40
    assert decode(fixture)["status"] == "native_completion_consistent"


def test_wrapper_rendering_is_not_invertible():
    # Independent synthetic counterexample to the inspected renderer's final-LF rule.
    def render(content):
        return content + ("" if content.endswith("\n") else "\n")

    assert render("READY") == render("READY\n")
    for rendered in (render("READY"), "Error: synthetic failure\n\nExiting...\n"):
        with pytest.raises(ValueError):
            subject.decode_completion(rendered.encode(), expected_model="synthetic-model")
