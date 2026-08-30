"""Pure synthetic runner contracts never invoke a runtime or admit observations."""

import base64
import copy
import hashlib
import json
from typing import Any, cast

import pytest

from tools import prospective_runner_contract as subject

SLOT = "case-synthetic__condition-local__r1"


def response():
    return {
        "index": 0,
        "content": "  Synthetic é\r\n",
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
        "prompt": "<not-a-byte-exact-request-echo>",
        "has_new_line": True,
        "truncated": False,
        "stop_type": "eos",
        "stopping_word": "",
        "tokens_cached": 0,
        "timings": {},
    }


def normalize(package, raw=None, **kwargs):
    return subject.normalize_candidate(
        package,
        json.dumps(response()).encode() if raw is None else raw,
        slot_id=kwargs.get("slot_id", SLOT),
        expected_slot_id=kwargs.get("expected_slot_id", SLOT),
        expected_model=kwargs.get("expected_model", "synthetic-model"),
    )


def test_build_request_preserves_exact_bytes():
    result = subject.build_request(b"prefix {{INPUT}} suffix", b"synthetic")
    assert result["admitted"] is result["study_unlocked"] is False


def test_empty_prompt_rejected_but_empty_input_with_literal_template_allowed():
    with pytest.raises(ValueError, match="empty_prompt"):
        subject.build_request(subject.MARKER, b"")
    assert subject.build_request(b"prefix{{INPUT}}", b"")["input"]["bytes"] == 0


@pytest.mark.parametrize("model", [None, "", "A", "a" * 101, "\ud800", "bad/label"])
def test_expected_model_is_bounded_label(model):
    with pytest.raises(ValueError, match="invalid_expected_model"):
        normalize(subject.build_request(subject.MARKER, b"s"), expected_model=model)


@pytest.mark.parametrize("flag", ["execution_observed", "admitted", "study_unlocked"])
@pytest.mark.parametrize("value", [True, 0], ids=["claim-true", "integer-false"])
def test_all_request_execution_and_admission_flags_fail_closed(flag, value):
    package = subject.build_request(subject.MARKER, b"s")
    package[flag] = value
    with pytest.raises(ValueError, match="invalid_request_package"):
        normalize(package)


@pytest.mark.parametrize(
    "damage",
    ["artifact-type", "custom-scalar", "key-type", "list-size", "huge-prompt", "cyclic-field"],
)
def test_untrusted_shapes_are_rejected_without_serializing_them(damage, monkeypatch):
    package = subject.build_request(subject.MARKER, b"s")
    if damage == "artifact-type":
        package["input"] = []
    elif damage == "custom-scalar":

        class CustomInt(int):
            def __eq__(self, other):
                raise AssertionError("custom comparisons must not run")

        package["generation"]["seed"] = CustomInt(42)
    elif damage == "key-type":
        package[1] = package.pop("version")
    elif damage == "list-size":
        package["limitations"].append("extra")
    elif damage == "huge-prompt":
        package["prompt"]["base64"] = "A" * (2 * subject.native.MAX_BYTES)
    else:
        package["prompt"] = package
    original = subject._json

    def generated_only(value):
        assert type(value) is dict and set(value) == {
            "prompt",
            "n_predict",
            "seed",
            "temperature",
            "stream",
            "ignore_eos",
            "stop",
        }
        return original(value)

    monkeypatch.setattr(subject, "_json", generated_only)
    with pytest.raises(ValueError, match="invalid_request_package"):
        normalize(package)


@pytest.mark.parametrize("text", ["", " \r\n", "é e\u0301 🌿", "\ufefftext", "{{INPUT}}", "\x00"])
def test_exact_bytes_deterministic_and_single_insertion(text):
    template = b"\xef\xbb\xbf prefix\r\n{{INPUT}}\n suffix "
    raw_input = text.encode()
    package = subject.build_request(template, raw_input)
    assert package == subject.build_request(template, raw_input)
    prompt = template.replace(subject.MARKER, raw_input, 1)
    for name, raw in (("template", template), ("input", raw_input), ("prompt", prompt)):
        assert base64.b64decode(package[name]["base64"]) == raw
        assert package[name]["sha256"] == hashlib.sha256(raw).hexdigest()
        assert package[name]["bytes"] == len(raw)
    request = base64.b64decode(package["request"]["base64"])
    value = json.loads(request)
    assert value == {
        "prompt": prompt.decode(),
        "seed": 42,
        "temperature": 0,
        "n_predict": 512,
        "stream": False,
        "ignore_eos": False,
        "stop": [],
    }
    assert (
        request
        == json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )
    assert package["generation"] == subject.GENERATION
    package["generation"]["seed"] = 0
    assert subject.GENERATION["seed"] == 42


@pytest.mark.parametrize("template", [b"", b"absent", b"{{INPUT}}{{INPUT}}"])
def test_marker_rejected(template):
    with pytest.raises(ValueError, match="invalid_template_marker"):
        subject.build_request(template, b"synthetic")


@pytest.mark.parametrize(
    "bad", ["text", bytearray(b"text"), b"\xff", None], ids=["str", "bytearray", "utf8", "none"]
)
@pytest.mark.parametrize("position", ["template", "input"])
def test_nonbytes_and_invalid_utf8_rejected(bad, position):
    args = (bad, b"input") if position == "template" else (subject.MARKER, bad)
    with pytest.raises(ValueError):
        subject.build_request(*cast(Any, args))


@pytest.mark.parametrize("kind", ["template", "input", "prompt", "request"])
def test_byte_limits_cover_every_stage(kind, monkeypatch):
    monkeypatch.setattr(subject.native, "MAX_BYTES", 200)
    template, raw_input = subject.MARKER, b"s"
    if kind == "template":
        template = subject.MARKER + b"t" * 200
    elif kind == "input":
        raw_input = b"s" * 201
    elif kind == "prompt":
        template, raw_input = b"t" * 190 + subject.MARKER, b"s" * 20
    else:
        raw_input = b"\x00" * 50  # JSON escaping exceeds the raw prompt budget.
    with pytest.raises(ValueError):
        subject.build_request(template, raw_input)


def test_normalization_preserves_raw_and_content_without_aliasing():
    package = subject.build_request(subject.MARKER, b"synthetic")
    raw = json.dumps(response()).encode()
    result = normalize(package, raw)
    assert result["slot_id"] == SLOT
    assert result["expected_model"] == "synthetic-model"
    assert result["status"] == "normalized_candidate"
    assert result["execution_observed"] is result["admitted"] is result["study_unlocked"] is False
    assert base64.b64decode(result["response"]["base64"]) == raw
    assert result["response"]["sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["decoded"]["content"] == response()["content"]
    assert result["request"] == package and result["request"] is not package
    package["generation"]["seed"] = 0
    package["limitations"].clear()
    assert result["request"]["generation"]["seed"] == 42
    assert result["request"]["limitations"]
    assert "request-response-binding-unverified" in result["limitations"]
    assert "denominator-membership-unverified" in result["limitations"]
    assert "privacy-and-data-class-unverified" in result["limitations"]


@pytest.mark.parametrize("field", ["base64", "sha256", "bytes"])
@pytest.mark.parametrize("artifact", ["template", "input", "prompt", "request"])
def test_every_retained_artifact_is_reconstructed(artifact, field):
    package = subject.build_request(subject.MARKER, b"synthetic")
    package[artifact][field] = 0 if field == "bytes" else "tampered"
    with pytest.raises(ValueError, match="invalid_request_package"):
        normalize(package)


@pytest.mark.parametrize(
    "kind",
    [
        "bool-int",
        "float-int",
        "extra",
        "missing",
        "tuple",
        "nonstring-key",
        "nonfinite",
        "surrogate",
        "object",
        "deep",
        "notdict",
        "encoded-too-long",
        "encoded-notstr",
        "noncanonical-base64",
    ],
)
def test_strict_complete_package_types_and_fields(kind):
    package = subject.build_request(subject.MARKER, b"s")
    if kind == "bool-int":
        package["input"]["bytes"] = True
    elif kind == "float-int":
        package["generation"]["temperature"] = 0.0
    elif kind == "extra":
        package["extra"] = None
    elif kind == "missing":
        del package["version"]
    elif kind == "tuple":
        package["limitations"] = tuple(package["limitations"])
    elif kind == "nonstring-key":
        package[1] = "extra"
    elif kind == "nonfinite":
        package["extra"] = float("nan")
    elif kind == "surrogate":
        package["version"] = "\ud800"
    elif kind == "object":
        package["extra"] = object()
    elif kind == "deep":
        nested = []
        package["extra"] = nested
        for _ in range(40):
            child = []
            nested.append(child)
            nested = child
    elif kind == "notdict":
        package = []
    elif kind == "encoded-too-long":
        package["input"]["base64"] = "A" * (4 * subject.native.MAX_BYTES)
    elif kind == "encoded-notstr":
        package["input"]["base64"] = 4
    else:
        package["input"]["base64"] = "cx=="  # Same decoded s, nonzero unused bits.
    with pytest.raises(ValueError, match="invalid_request_package"):
        normalize(package)


@pytest.mark.parametrize(
    "slot",
    [
        None,
        "",
        "case-A__condition-local__r1",
        "case-a__condition-local__r2",
        SLOT + "\n",
        "case-" + "a" * 60 + "__condition-local__r1",
        "x" * 151,
    ],
)
def test_invalid_slot_labels(slot):
    package = subject.build_request(subject.MARKER, b"s")
    with pytest.raises(ValueError, match="invalid_slot_id"):
        normalize(package, slot_id=slot, expected_slot_id=slot)


def test_expected_slot_is_checked_and_mismatch_rejected():
    package = subject.build_request(subject.MARKER, b"s")
    for expected, error in (
        ("invalid", "invalid_slot_id"),
        ("case-other__condition-local__r1", "slot_mismatch"),
    ):
        with pytest.raises(ValueError, match=error):
            normalize(package, expected_slot_id=expected)


@pytest.mark.parametrize("damage", ["eos", "truncated", "settings", "model", "extra"])
def test_native_decoder_rejections_remain_failures(damage):
    value = copy.deepcopy(response())
    if damage == "eos":
        value["stop_type"] = "limit"
    elif damage == "truncated":
        value["truncated"] = True
    elif damage == "settings":
        value["generation_settings"]["seed"] = 0
    elif damage == "model":
        value["model"] = "other"
    else:
        value["extra"] = 1
    with pytest.raises(ValueError):
        normalize(subject.build_request(subject.MARKER, b"s"), json.dumps(value).encode())


@pytest.mark.parametrize(
    "raw", [b"{}", b"\xff", b'{"a":1,"a":2}', b""], ids=["schema", "utf8", "duplicate", "empty"]
)
def test_malformed_response_rejected(raw):
    with pytest.raises(ValueError):
        normalize(subject.build_request(subject.MARKER, b"s"), raw)
