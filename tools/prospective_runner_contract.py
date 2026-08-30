"""Pure native request/normalization candidates, never execution or admission.

No protocol is consumed here. Labels and reconstructed bytes are consistency
checks, not denominator membership, provenance, model identity or response binding.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re

from tools import native_completion as native
from tools.prospective_protocol import GENERATION

MARKER = b"{{INPUT}}"
VERSION = "native-runner-candidate-v1"
SLOT = re.compile(r"(case-[a-z0-9-]+)__(condition-[a-z0-9-]+)__r1")
LIMITATIONS = (
    "protocol-compatibility-unverified",
    "denominator-membership-unverified",
    "slot-and-input-provenance-unverified",
    "request-response-binding-unverified",
    "model-identity-unverified",
    "privacy-and-data-class-unverified",
    "execution-unverified",
    "byte-limits-not-context-token-validation",
    "not-study-admission",
)


def _json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def _artifact(raw: bytes) -> dict:
    return {
        "base64": base64.b64encode(raw).decode("ascii"),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def _text(raw: bytes) -> str:
    if type(raw) is not bytes or len(raw) > native.MAX_BYTES:
        raise ValueError("invalid_text_bytes")
    try:
        return raw.decode("utf-8")
    except UnicodeError:
        raise ValueError("invalid_utf8") from None


def build_request(template: bytes, input_bytes: bytes) -> dict:
    """Insert exactly once and retain exact UTF-8 bytes; do not apply chat wrapping."""
    _text(template)
    _text(input_bytes)
    if template.count(MARKER) != 1:
        raise ValueError("invalid_template_marker")
    prompt = template.replace(MARKER, input_bytes, 1)
    text = _text(prompt)
    if not text:
        raise ValueError("empty_prompt")
    raw = _json(
        {
            "prompt": text,
            "n_predict": GENERATION["max_tokens"],
            "seed": GENERATION["seed"],
            "temperature": GENERATION["temperature"],
            "stream": False,
            "ignore_eos": False,
            "stop": [],
        }
    )
    if len(raw) > native.MAX_BYTES:
        raise ValueError("request_byte_limit")
    return {
        "version": VERSION,
        "template": _artifact(template),
        "input": _artifact(input_bytes),
        "prompt": _artifact(prompt),
        "request": _artifact(raw),
        "generation": dict(GENERATION),
        "limits": {"max_bytes_per_artifact": native.MAX_BYTES, "context_tokens_validated": False},
        "limitations": list(LIMITATIONS),
        "execution_observed": False,
        "admitted": False,
        "study_unlocked": False,
    }


def _same(value: object, expected: object) -> bool:
    """Visit only the bounded rebuilt shape, without serializing untrusted fields."""
    if type(value) is not type(expected):
        return False
    if isinstance(expected, dict):
        assert isinstance(value, dict)
        return (
            len(value) == len(expected)
            and all(type(key) is str for key in value)
            and value.keys() == expected.keys()
            and all(_same(value[key], item) for key, item in expected.items())
        )
    if isinstance(expected, list):
        assert isinstance(value, list)
        return len(value) == len(expected) and all(
            _same(actual, item) for actual, item in zip(value, expected, strict=True)
        )
    return value == expected


def _reconstruct(request: dict) -> dict:
    try:
        if type(request) is not dict:
            raise ValueError("invalid_request_package")
        # Bound encoded inputs before decoding; canonical equality rejects alternate encodings.
        raw = []
        for name in ("template", "input"):
            if type(request[name]) is not dict:
                raise ValueError("invalid_request_package")
            encoded = request[name]["base64"]
            if type(encoded) is not str or len(encoded) > 4 * ((native.MAX_BYTES + 2) // 3):
                raise ValueError("invalid_request_package")
            raw.append(base64.b64decode(encoded, validate=True))
        rebuilt = build_request(raw[0], raw[1])
        if not _same(request, rebuilt):
            raise ValueError("invalid_request_package")
        return rebuilt
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid_request_package") from None


def normalize_candidate(
    request: dict, raw_body: bytes, *, slot_id: str, expected_slot_id: str, expected_model: str
) -> dict:
    """Retain a slot-labelled candidate, not a verified primary observation."""
    for slot in (slot_id, expected_slot_id):
        if type(slot) is not str or len(slot) > 150:
            raise ValueError("invalid_slot_id")
        match = SLOT.fullmatch(slot)
        if match is None or any(len(label) > 64 for label in match.groups()):
            raise ValueError("invalid_slot_id")
    if slot_id != expected_slot_id:
        raise ValueError("slot_mismatch")
    if (
        type(expected_model) is not str
        or len(expected_model) > 100
        or re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,99}", expected_model) is None
    ):
        raise ValueError("invalid_expected_model")
    rebuilt = _reconstruct(request)
    decoded = native.decode_completion(raw_body, expected_model=expected_model)
    return {
        "version": VERSION,
        "status": "normalized_candidate",
        "slot_id": slot_id,
        "expected_model": expected_model,
        "request": rebuilt,
        "response": _artifact(raw_body),
        "decoded": decoded,
        "limitations": list(LIMITATIONS),
        "execution_observed": False,
        "admitted": False,
        "study_unlocked": False,
    }
