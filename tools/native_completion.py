"""Read-only consistency for pinned native completion JSON, never live admission.

Contract: llama.cpp c1d0e7a004015f23bc0233470b747b596f29b264 native /completion,
non-streaming, one prompt, no stopping words. This is NOT the chat/completions
contract or CLI stdout. Content means decoded server text, not raw token bytes.
The caller must retain the original body and independently prove its provenance.
"""

from __future__ import annotations

import hashlib
import json

from tools.prospective_protocol import GENERATION

MAX_BYTES = 1024 * 1024
FIELDS = frozenset(
    {
        "index",
        "content",
        "tokens",
        "id_slot",
        "stop",
        "model",
        "tokens_predicted",
        "tokens_evaluated",
        "generation_settings",
        "prompt",
        "has_new_line",
        "truncated",
        "stop_type",
        "stopping_word",
        "tokens_cached",
        "timings",
    }
)


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _constant(value: str) -> object:
    raise ValueError("nonfinite_json_number")


def _integer(value: object, minimum: int, maximum: int) -> bool:
    return type(value) is int and minimum <= value <= maximum


def decode_completion(raw: bytes, *, expected_model: str) -> dict:
    """Check selected response declarations; labels/settings are not attestation.

    The response prompt is detokenised input, NOT a byte-for-byte request echo.
    Model is only an expected label. Neither establishes model or request binding.
    Other sampling settings are preserved in raw JSON but not qualified here.
    """
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_BYTES:
        raise ValueError("invalid_raw_body")
    if not isinstance(expected_model, str) or not expected_model:
        raise ValueError("invalid_expected_model")
    try:
        expected_model.encode("utf-8")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
        # Also reject lone surrogates and numeric overflow in ignored metadata.
        json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ValueError("invalid_completion_json") from exc
    if not isinstance(value, dict) or set(value) != FIELDS:
        raise ValueError("unsupported_completion_fields")
    if (
        value["stop"] is not True
        or value["truncated"] is not False
        or value["stop_type"] != "eos"
        or value["stopping_word"] != ""
    ):
        raise ValueError("incomplete_generation")
    if (
        not isinstance(value["content"], str)
        or not value["content"]
        or not isinstance(value["prompt"], str)
        or not value["prompt"]
        or value["model"] != expected_model
        or type(value["has_new_line"]) is not bool
        or not isinstance(value["timings"], dict)
    ):
        raise ValueError("invalid_completion_metadata")
    counts = (
        ("index", 0, 0),
        ("id_slot", 0, 2**31 - 1),
        ("tokens_predicted", 1, GENERATION["max_tokens"]),
        ("tokens_evaluated", 1, GENERATION["context_tokens"]),
        ("tokens_cached", 0, GENERATION["context_tokens"]),
    )
    if any(not _integer(value[key], low, high) for key, low, high in counts):
        raise ValueError("invalid_completion_counts")
    if not isinstance(value["tokens"], list) or any(
        not _integer(token, 0, 2**31 - 1) for token in value["tokens"]
    ):
        raise ValueError("invalid_completion_tokens")
    settings = value["generation_settings"]
    if not isinstance(settings, dict):
        raise ValueError("invalid_generation_settings")
    expected = {
        "seed": GENERATION["seed"],
        "n_predict": GENERATION["max_tokens"],
        "max_tokens": GENERATION["max_tokens"],
    }
    if (
        any(not _integer(settings.get(key), number, number) for key, number in expected.items())
        or type(settings.get("temperature")) not in (int, float)
        or settings["temperature"] != GENERATION["temperature"]
        or settings.get("stream") is not False
        or settings.get("ignore_eos") is not False
        or settings.get("stop") != []
    ):
        raise ValueError("generation_settings_mismatch")
    content = value["content"].encode("utf-8")
    return {
        "status": "native_completion_consistent",
        "normalization": "llama-native-json-v1",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "content": value["content"],
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "content_bytes": len(content),
        "detokenized_prompt_sha256": hashlib.sha256(value["prompt"].encode("utf-8")).hexdigest(),
        "tokens_predicted": value["tokens_predicted"],
        "tokens_evaluated": value["tokens_evaluated"],
        "admitted": False,
        "study_unlocked": False,
        "limitations": [
            "response-declarations-only",
            "request-binding-not-verified",
            "transport-and-runtime-not-verified",
            "model-label-not-model-identity",
            "other-sampling-settings-not-qualified",
            "context-and-timeout-not-verified",
            "raw-token-bytes-not-preserved-by-json",
            "privacy-not-verified",
            "protocol-freeze-and-review-not-verified",
            "not-primary-study-evidence",
        ],
    }
