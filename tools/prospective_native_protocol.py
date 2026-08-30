"""Read-once native protocol candidates; no execution, freeze or study admission."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from tools import prospective_protocol as legacy
from tools import prospective_runner_contract as runner

PROTOCOL_VERSION = "2.0.0"
SCHEMA = deepcopy(legacy.SCHEMA)
SCHEMA["properties"].update(
    protocol_version=legacy.fixed(PROTOCOL_VERSION),
    normalization=legacy.fixed("llama-native-json-v1"),
    runner_contract_version=legacy.fixed(runner.VERSION),
)
SCHEMA["required"].append("runner_contract_version")


def validate_protocol(path: Path, expected_sha256: str) -> dict:
    """Construct two candidate requests using only pinned bytes read by shared checks."""
    result, value, artifacts = legacy._validate_candidate(path, expected_sha256, SCHEMA)
    template = artifacts[value["prompt_template"]["path"]]
    requests = {}
    for case in value["cases"]:
        slot = f"{case['id']}__{value['condition']['id']}__r1"
        requests[slot] = runner.build_request(template, artifacts[case["input"]["path"]])
    return {
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
