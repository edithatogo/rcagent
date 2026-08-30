"""Synthetic native declarations never freeze or admit a study."""

import base64
import copy
import json

import pytest

from tests.test_prospective_protocol import fixture as legacy_fixture
from tests.test_prospective_protocol import pin
from tools import prospective_native_protocol as subject
from tools import prospective_protocol as legacy


def fixture(root):
    path, value = legacy_fixture(root)
    value.update(
        protocol_version="2.0.0",
        normalization="llama-native-json-v1",
        runner_contract_version=subject.runner.VERSION,
    )
    prompt = root / value["prompt_template"]["path"]
    prompt.write_bytes(b"\xef\xbb\xbfSynthetic\r\n{{INPUT}}\n")
    value["prompt_template"]["sha256"] = pin(prompt)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path, value


def rewrite(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")
    return subject.validate_protocol(path, pin(path))


def test_native_version_is_distinct():
    assert subject.PROTOCOL_VERSION == "2.0.0"


def test_private_validated_view_preserves_public_api(tmp_path):
    path, value = fixture(tmp_path)
    parsed, candidate = subject._validated_candidate(path, pin(path))
    assert parsed == value
    assert candidate == subject.validate_protocol(path, pin(path))
    assert set(candidate) == {
        "status",
        "protocol_sha256",
        "study_id",
        "expected_slots",
        "study_unlocked",
        "admitted",
        "limitations",
        "protocol_version",
        "normalization",
        "runner_contract_version",
        "requests",
        "execution_observed",
    }


def test_native_rejects_unchanged_legacy_declaration(tmp_path):
    path, _ = legacy_fixture(tmp_path)
    with pytest.raises(ValueError):
        subject.validate_protocol(path, pin(path))


def test_native_candidate_builds_two_exact_slot_requests(tmp_path):
    path, value = fixture(tmp_path)
    result = subject.validate_protocol(path, pin(path))
    assert result["status"] == "native_protocol_candidate_valid"
    assert result["execution_observed"] is result["admitted"] is result["study_unlocked"] is False
    assert set(result["requests"]) == set(value["expected_slots"])
    assert result["expected_slots"] == 2
    assert result["protocol_sha256"] == pin(path)
    assert result["runner_contract_version"] == subject.runner.VERSION
    template = (tmp_path / value["prompt_template"]["path"]).read_bytes()
    for case in value["cases"]:
        slot = f"{case['id']}__{value['condition']['id']}__r1"
        raw_input = (tmp_path / case["input"]["path"]).read_bytes()
        package = result["requests"][slot]
        assert package == subject.runner.build_request(template, raw_input)
        assert base64.b64decode(package["prompt"]["base64"]) == template.replace(
            b"{{INPUT}}", raw_input
        )
    assert "atomic-filesystem-snapshot-unverified" in result["limitations"]
    assert "request-response-binding-unverified" in result["limitations"]


def test_protocol_and_references_read_once_then_exact_retained_bytes_used(tmp_path, monkeypatch):
    path, value = fixture(tmp_path)
    original_read, original_artifact = legacy.read_json, legacy.artifact
    reads, retained = [], {}

    def read_once(file):
        assert file not in reads
        reads.append(file)
        result = original_read(file)
        file.write_bytes(b"changed after pinned read")
        return result

    def artifact_once(root, ref):
        assert ref["path"] not in retained
        raw = original_artifact(root, ref)
        retained[ref["path"]] = raw
        (root / ref["path"]).write_bytes(b"changed after pinned read")
        return raw

    expected_pin = pin(path)
    monkeypatch.setattr(legacy, "read_json", read_once)
    monkeypatch.setattr(legacy, "artifact", artifact_once)
    result = subject.validate_protocol(path, expected_pin)
    assert reads == [path.absolute()]
    assert len(retained) == 5
    assert result["protocol_sha256"] == expected_pin != pin(path)
    for case in value["cases"]:
        slot = f"{case['id']}__{value['condition']['id']}__r1"
        assert result["requests"][slot] == subject.runner.build_request(
            retained[value["prompt_template"]["path"]], retained[case["input"]["path"]]
        )
    assert "atomic-filesystem-snapshot-unverified" in result["limitations"]


@pytest.mark.parametrize("mode", ["identity-utf8-v1", "strict-runtime-wrapper-v1"])
def test_native_rejects_both_legacy_modes(tmp_path, mode):
    path, value = fixture(tmp_path)
    value["normalization"] = mode
    with pytest.raises(ValueError):
        rewrite(path, value)


@pytest.mark.parametrize(
    "mutation",
    [
        "legacy-version",
        "missing-runner",
        "wrong-runner",
        "duplicate-slot",
        "wrong-slot",
        "duplicate-case",
        "duplicate-path",
        "stale-ref",
        "marker-absent",
        "marker-double",
        "generation",
        "generation-bool",
        "extra-field",
        "path-escape",
        "invalid-utf8",
    ],
)
def test_native_adversarial_declarations(tmp_path, mutation):
    path, value = fixture(tmp_path)
    if mutation == "legacy-version":
        value["protocol_version"] = "1.0.0"
    elif mutation == "missing-runner":
        del value["runner_contract_version"]
    elif mutation == "wrong-runner":
        value["runner_contract_version"] = "unknown"
    elif mutation == "duplicate-slot":
        value["expected_slots"][1] = value["expected_slots"][0]
    elif mutation == "wrong-slot":
        value["expected_slots"][1] = "case-other__condition-local-text__r1"
    elif mutation == "duplicate-case":
        value["cases"][1]["id"] = value["cases"][0]["id"]
    elif mutation == "duplicate-path":
        value["rubric"] = copy.deepcopy(value["cases"][0]["input"])
    elif mutation == "stale-ref":
        (tmp_path / value["cases"][0]["input"]["path"]).write_bytes(b"changed")
    elif mutation.startswith("marker-"):
        prompt = tmp_path / value["prompt_template"]["path"]
        prompt.write_bytes(b"absent" if mutation == "marker-absent" else b"{{INPUT}}{{INPUT}}")
        value["prompt_template"]["sha256"] = pin(prompt)
    elif mutation == "generation":
        value["generation"]["seed"] = 43
    elif mutation == "generation-bool":
        value["generation"]["temperature"] = False
    elif mutation == "extra-field":
        value["admitted"] = True
    elif mutation == "path-escape":
        value["cases"][0]["input"]["path"] = "../outside.txt"
    else:
        invalid = tmp_path / value["cases"][0]["input"]["path"]
        invalid.write_bytes(b"\xff")
        value["cases"][0]["input"]["sha256"] = pin(invalid)
    with pytest.raises(ValueError):
        rewrite(path, value)


def test_wrong_pin_rejected_before_any_reference_read(tmp_path, monkeypatch):
    path, _ = fixture(tmp_path)

    def forbidden(*args):
        raise AssertionError("references must not be read")

    monkeypatch.setattr(legacy, "artifact", forbidden)
    with pytest.raises(ValueError, match="protocol_pin_mismatch"):
        subject.validate_protocol(path, "0" * 64)


def test_schemas_do_not_share_mutable_declaration_state():
    assert subject.SCHEMA is not legacy.SCHEMA
    assert (
        subject.SCHEMA["properties"]["generation"] is not legacy.SCHEMA["properties"]["generation"]
    )
    assert legacy.SCHEMA["properties"]["protocol_version"] == {"const": "1.0.0"}
    assert legacy.SCHEMA["properties"]["normalization"] == {
        "enum": ["identity-utf8-v1", "strict-runtime-wrapper-v1"]
    }
    assert "runner_contract_version" not in legacy.SCHEMA["required"]
