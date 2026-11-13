"""Check a frozen-protocol candidate's consistency, never freeze or admit it.

Digests identify intended runtime/model/profile/study-runner bytes; matching hex
does not validate those artefacts or an implemented normalisation parser. This
read-only contract does not prove Git freeze, execution, or absence of private data.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard

from tools import json_shapes
from tools.evaluation_preflight import _digest
from tools.prospective_inventory import REF, artifact, identifier, obj, read_json, validate


class ArtifactReference(TypedDict):
    path: str
    sha256: str


class ProtocolCase(TypedDict):
    id: str
    input: ArtifactReference


class ScoringDeclaration(TypedDict):
    reviewer_class: str
    roles: list[str]
    adjudication: str
    raw_agreement_minimum: float
    ordinal_agreement_minimum: float
    hard_gates: list[str]
    non_operational: bool


class ProtocolDocument(TypedDict):
    """Common document fields after schema and immediate shape validation."""

    schema_version: str
    kind: str
    protocol_version: str
    study_id: str
    data_class: str
    case_exposure: str
    held_out: bool
    claims_boundary: str
    repeats: int
    cases: list[ProtocolCase]
    condition: dict[str, str]
    expected_slots: list[str]
    rubric: ArtifactReference
    scoring_instructions: ArtifactReference
    prompt_template: ArtifactReference
    generation: dict[str, int]
    technical_retries: int
    blinding: str
    normalization: str
    scoring: ScoringDeclaration


class ProtocolCandidateFields(TypedDict):
    protocol_sha256: str
    study_id: str
    expected_slots: Literal[2]
    study_unlocked: Literal[False]
    admitted: Literal[False]
    limitations: list[str]


class ProtocolCandidate(ProtocolCandidateFields):
    status: Literal["protocol_candidate_valid"]


def _is_strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _is_text_object(value: object) -> TypeGuard[dict[str, str]]:
    return json_shapes.is_object(value) and all(isinstance(item, str) for item in value.values())


def _is_integer_object(value: object) -> TypeGuard[dict[str, int]]:
    return json_shapes.is_object(value) and all(type(item) is int for item in value.values())


def _is_reference(value: object) -> TypeGuard[ArtifactReference]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("path"), str)
        and isinstance(value.get("sha256"), str)
    )


def _is_case(value: object) -> TypeGuard[ProtocolCase]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("id"), str)
        and _is_reference(value.get("input"))
    )


def _is_cases(value: object) -> TypeGuard[list[ProtocolCase]]:
    return json_shapes.is_array(value) and all(_is_case(item) for item in value)


def _is_scoring(value: object) -> TypeGuard[ScoringDeclaration]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("reviewer_class"), str)
        and _is_strings(value.get("roles"))
        and isinstance(value.get("adjudication"), str)
        and isinstance(value.get("raw_agreement_minimum"), (int, float))
        and isinstance(value.get("ordinal_agreement_minimum"), (int, float))
        and _is_strings(value.get("hard_gates"))
        and isinstance(value.get("non_operational"), bool)
    )


def _is_document(value: object) -> TypeGuard[ProtocolDocument]:
    return (
        json_shapes.is_object(value)
        and all(
            isinstance(value.get(key), str)
            for key in (
                "schema_version",
                "kind",
                "protocol_version",
                "study_id",
                "data_class",
                "case_exposure",
                "claims_boundary",
                "blinding",
                "normalization",
            )
        )
        and isinstance(value.get("held_out"), bool)
        and type(value.get("repeats")) is int
        and type(value.get("technical_retries")) is int
        and _is_cases(value.get("cases"))
        and _is_text_object(value.get("condition"))
        and _is_strings(value.get("expected_slots"))
        and all(
            _is_reference(value.get(key))
            for key in ("rubric", "scoring_instructions", "prompt_template")
        )
        and _is_integer_object(value.get("generation"))
        and _is_scoring(value.get("scoring"))
    )


def fixed(value: object) -> json_shapes.JsonObject:
    return {"const": value}


DIGEST: json_shapes.JsonObject = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
GENERATION: dict[str, int] = {
    "seed": 42,
    "temperature": 0,
    "max_tokens": 512,
    "context_tokens": 2048,
    "timeout_seconds": 120,
}
CLAIMS = "research-only-public-two-case-one-condition-no-comparative-or-operational-claims"
SCHEMA = json_shapes.require_object(
    obj(
        {
            "schema_version": fixed("1.0"),
            "kind": fixed("prospective-study-protocol"),
            "protocol_version": fixed("1.0.0"),
            "study_id": identifier("prospective"),
            "data_class": fixed("synthetic"),
            "case_exposure": fixed("public"),
            "held_out": {"type": "boolean", "const": False},
            "claims_boundary": fixed(CLAIMS),
            "repeats": fixed(1),
            "cases": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": obj({"id": identifier("case"), "input": REF}),
            },
            "condition": obj(
                {
                    "id": identifier("condition"),
                    "model_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9._-]{0,99}$"},
                    "model_revision": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
                    **dict.fromkeys(
                        (
                            "model_sha256",
                            "runtime_sha256",
                            "profile_sha256",
                            "adapter_sha256",
                            "registry_sha256",
                        ),
                        DIGEST,
                    ),
                }
            ),
            "expected_slots": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "uniqueItems": True,
                "items": {"type": "string", "maxLength": 150},
            },
            "rubric": REF,
            "scoring_instructions": REF,
            "prompt_template": REF,
            "generation": obj({key: fixed(value) for key, value in GENERATION.items()}),
            "technical_retries": fixed(1),
            "blinding": fixed("metadata-blinding-v1"),
            "normalization": {"enum": ["identity-utf8-v1", "strict-runtime-wrapper-v1"]},
            "scoring": obj(
                {
                    "reviewer_class": fixed("agent"),
                    "roles": fixed(["scorer-1", "scorer-2", "scorer-3"]),
                    "adjudication": fixed("after-three-sealed-submissions"),
                    "raw_agreement_minimum": fixed(0.80),
                    "ordinal_agreement_minimum": fixed(0.67),
                    "hard_gates": fixed(
                        ["privacy", "cultural-safety", "clinical-safety", "authority-boundaries"]
                    ),
                    "non_operational": {"type": "boolean", "const": True},
                }
            ),
        }
    ),
    context="protocol schema",
)


def _validate_candidate(
    path: Path, expected_sha256: str, schema: json_shapes.JsonObject
) -> tuple[ProtocolCandidate, ProtocolDocument, dict[str, bytes]]:
    """Share existing checks and retain the exact reference bytes already validated."""
    path = path.absolute()
    value, pin = read_json(path)
    if not _digest(expected_sha256) or pin != expected_sha256:
        raise ValueError("protocol_pin_mismatch")
    validate(value, schema)
    if not json_shapes.is_object(value):
        raise ValueError("invalid_validated_object_type")
    generation = json_shapes.require_object(value["generation"], context="protocol generation")
    integers = [value["repeats"], value["technical_retries"], *generation.values()]
    if any(type(item) is not int for item in integers):
        raise ValueError("invalid_integer_type")
    if not _is_document(value):
        raise ValueError("invalid_validated_object_type")
    condition = value["condition"]
    identities = [("prospective", value["study_id"]), ("condition", condition["id"])]
    identities.extend(("case", case["id"]) for case in value["cases"])
    if any(not re.fullmatch(prefix + r"-[a-z0-9-]+", name) for prefix, name in identities):
        raise ValueError("invalid_identity")
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,99}", condition["model_id"]) or not re.fullmatch(
        r"[0-9a-f]{40}", condition["model_revision"]
    ):
        raise ValueError("invalid_model_identity")
    if any(not _digest(item) for key, item in condition.items() if key.endswith("_sha256")):
        raise ValueError("invalid_condition_digest")
    case_ids = {case["id"] for case in value["cases"]}
    if len(case_ids) != 2:
        raise ValueError("duplicate_case_identity")
    expected = {f"{case}__{condition['id']}__r1" for case in case_ids}
    if set(value["expected_slots"]) != expected:
        raise ValueError("denominator_mismatch")
    refs = [case["input"] for case in value["cases"]]
    refs.extend(value[key] for key in ("rubric", "scoring_instructions", "prompt_template"))
    paths: set[str] = set()
    artifacts: dict[str, bytes] = {}
    for ref in refs:
        if ref["path"].casefold() in paths:
            raise ValueError("duplicate_artifact_path")
        paths.add(ref["path"].casefold())
        try:
            data = artifact(path.parent, dict(ref))
            data.decode("utf-8")
            artifacts[ref["path"]] = data
        except UnicodeError as exc:
            raise ValueError("invalid_artifact_utf8") from exc
    result: ProtocolCandidate = {
        "status": "protocol_candidate_valid",
        "protocol_sha256": pin,
        "study_id": value["study_id"],
        "expected_slots": 2,
        "study_unlocked": False,
        "admitted": False,
        "limitations": [
            "consistency-only",
            "git-freeze-not-verified",
            "runtime-and-adapter-not-verified",
            "normalization-not-verified",
            "privacy-not-verified",
            "no-primary-observations",
        ],
    }
    return result, value, artifacts


def validate_protocol(path: Path, expected_sha256: str) -> ProtocolCandidate:
    """Validate candidate declarations and referenced text, not primary evidence."""
    return _validate_candidate(path, expected_sha256, SCHEMA)[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        result = validate_protocol(args.protocol, args.expected_sha256)
    except (ValueError, OSError):
        print(
            json.dumps(
                {"status": "protocol_candidate_invalid", "study_unlocked": False, "admitted": False}
            )
        )
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
