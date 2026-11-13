"""Read-once native protocol candidates; no execution, freeze or study admission."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Literal, TypeGuard

from tools import json_shapes
from tools import prospective_protocol as legacy
from tools import prospective_runner_contract as runner

PROTOCOL_VERSION = "2.0.0"
SCHEMA = deepcopy(legacy.SCHEMA)
_properties = json_shapes.require_object(SCHEMA["properties"], context="native schema properties")
_properties.update(
    protocol_version=legacy.fixed(PROTOCOL_VERSION),
    normalization=legacy.fixed("llama-native-json-v1"),
    runner_contract_version=legacy.fixed(runner.VERSION),
)
_required = SCHEMA["required"]
if not json_shapes.is_array(_required):
    raise ValueError("invalid_native_schema_required")
_required.append("runner_contract_version")


class NativeProtocolDocument(legacy.ProtocolDocument):
    runner_contract_version: str


class NativeProtocolCandidate(legacy.ProtocolCandidateFields):
    status: Literal["native_protocol_candidate_valid"]
    protocol_version: Literal["2.0.0"]
    normalization: Literal["llama-native-json-v1"]
    runner_contract_version: str
    requests: dict[str, runner.RequestPackage]
    execution_observed: Literal[False]


def _is_native_document(value: legacy.ProtocolDocument) -> TypeGuard[NativeProtocolDocument]:
    fields: Mapping[str, object] = value
    return isinstance(fields.get("runner_contract_version"), str)


def _validated_candidate(
    path: Path, expected_sha256: str
) -> tuple[NativeProtocolDocument, NativeProtocolCandidate]:
    """Construct two candidate requests using only pinned bytes read by shared checks."""
    result, value, artifacts = legacy._validate_candidate(path, expected_sha256, SCHEMA)
    if not _is_native_document(value):
        raise ValueError("invalid_validated_object_type")
    template = artifacts[value["prompt_template"]["path"]]
    requests: dict[str, runner.RequestPackage] = {}
    for case in value["cases"]:
        slot = f"{case['id']}__{value['condition']['id']}__r1"
        requests[slot] = runner.build_request(template, artifacts[case["input"]["path"]])
    candidate: NativeProtocolCandidate = {
        **result,
        "status": "native_protocol_candidate_valid",
        "protocol_version": PROTOCOL_VERSION,
        "normalization": "llama-native-json-v1",
        "runner_contract_version": runner.VERSION,
        "requests": requests,
        "execution_observed": False,
        "limitations": [
            "candidate-consistency-only",
            "protocol-declared-denominator-only",
            "privacy-and-data-class-unverified",
            "atomic-filesystem-snapshot-unverified",
            "git-freeze-not-verified",
            "runtime-and-model-identity-unverified",
            "request-response-binding-unverified",
            "no-primary-observations",
            "not-study-admission",
        ],
    }
    return value, candidate


def validate_protocol(path: Path, expected_sha256: str) -> NativeProtocolCandidate:
    """Return the unchanged public candidate without rereading its references."""
    return _validated_candidate(path, expected_sha256)[1]
