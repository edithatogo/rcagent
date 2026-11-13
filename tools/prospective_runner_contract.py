"""Pure native request/normalization candidates, never execution or admission.

No protocol is consumed here. Labels and reconstructed bytes are consistency
checks, not denominator membership, provenance, model identity or response binding.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from typing import Literal, TypedDict, cast

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


class Artifact(TypedDict):
    base64: str
    sha256: str
    bytes: int


class RequestLimits(TypedDict):
    max_bytes_per_artifact: int
    context_tokens_validated: Literal[False]


class RequestPackage(TypedDict):
    """Constructed native request bytes and their unadmitted provenance labels."""

    version: str
    template: Artifact
    input: Artifact
    prompt: Artifact
    request: Artifact
    generation: dict[str, int]
    limits: RequestLimits
    limitations: list[str]
    execution_observed: Literal[False]
    admitted: Literal[False]
    study_unlocked: Literal[False]


class NormalizedCandidate(TypedDict):
    version: str
    status: Literal["normalized_candidate"]
    slot_id: str
    expected_model: str
    request: RequestPackage
    response: Artifact
    decoded: native.DecodedCompletion
    limitations: list[str]
    execution_observed: Literal[False]
    admitted: Literal[False]
    study_unlocked: Literal[False]


def _json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def _artifact(raw: bytes) -> Artifact:
    return {
        "base64": base64.b64encode(raw).decode("ascii"),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def _text(raw: object) -> str:
    if type(raw) is not bytes or len(raw) > native.MAX_BYTES:
        raise ValueError("invalid_text_bytes")
    try:
        return raw.decode("utf-8")
    except UnicodeError:
        raise ValueError("invalid_utf8") from None


def build_request(template: object, input_bytes: object) -> RequestPackage:
    """Insert exactly once and retain exact UTF-8 bytes; do not apply chat wrapping."""
    _text(template)
    _text(input_bytes)
    # _text has checked the exact bytes type, byte bound and UTF-8 for each input.
    template = cast("bytes", template)
    input_bytes = cast("bytes", input_bytes)
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
        if not isinstance(value, dict):
            raise ValueError("invalid_validated_object_type")
        # Establish only container types; inspect length before keys or values
        # so unexpected huge/deep fields cannot expand reconstruction work.
        actual_object = cast("dict[object, object]", value)
        expected_object = cast("dict[object, object]", expected)
        return (
            len(actual_object) == len(expected_object)
            and all(type(key) is str for key in actual_object)
            and actual_object.keys() == expected_object.keys()
            and all(_same(actual_object[key], item) for key, item in expected_object.items())
        )
    if isinstance(expected, list):
        if not isinstance(value, list):
            raise ValueError("invalid_validated_object_type")
        actual_items = cast("list[object]", value)
        expected_items = cast("list[object]", expected)
        return len(actual_items) == len(expected_items) and all(
            _same(actual, item) for actual, item in zip(actual_items, expected_items, strict=True)
        )
    return value == expected


def _reconstruct(request: object) -> RequestPackage:
    try:
        if type(request) is not dict:
            raise ValueError("invalid_request_package")
        package = cast("dict[object, object]", request)
        # Bound encoded inputs before decoding; canonical equality rejects alternate encodings.
        raw: list[bytes] = []
        for name in ("template", "input"):
            artifact = package[name]
            if type(artifact) is not dict:
                raise ValueError("invalid_request_package")
            fields = cast("dict[object, object]", artifact)
            encoded = fields["base64"]
            if type(encoded) is not str or len(encoded) > 4 * ((native.MAX_BYTES + 2) // 3):
                raise ValueError("invalid_request_package")
            raw.append(base64.b64decode(encoded, validate=True))
        rebuilt = build_request(raw[0], raw[1])
        if not _same(package, rebuilt):
            raise ValueError("invalid_request_package")
        return rebuilt
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OverflowError):
        raise ValueError("invalid_request_package") from None


def _slot(slot: object) -> str:
    if type(slot) is not str or len(slot) > 150:
        raise ValueError("invalid_slot_id")
    match = SLOT.fullmatch(slot)
    if match is None or any(len(label) > 64 for label in match.groups()):
        raise ValueError("invalid_slot_id")
    return slot


def normalize_candidate(
    request: object,
    raw_body: object,
    *,
    slot_id: object,
    expected_slot_id: object,
    expected_model: object,
) -> NormalizedCandidate:
    """Retain a slot-labelled candidate, not a verified primary observation."""
    slot_id = _slot(slot_id)
    expected_slot_id = _slot(expected_slot_id)
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
    # Successful decoding establishes the exact bytes type and response size bound.
    raw_body = cast("bytes", raw_body)
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
