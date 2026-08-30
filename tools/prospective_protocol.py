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

from tools.evaluation_preflight import _digest
from tools.prospective_inventory import REF, artifact, identifier, obj, read_json, validate


def fixed(value: object) -> dict:
    return {"const": value}


DIGEST = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
GENERATION = {
    "seed": 42,
    "temperature": 0,
    "max_tokens": 512,
    "context_tokens": 2048,
    "timeout_seconds": 120,
}
CLAIMS = "research-only-public-two-case-one-condition-no-comparative-or-operational-claims"
SCHEMA = obj(
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
                **{
                    name: DIGEST
                    for name in (
                        "model_sha256",
                        "runtime_sha256",
                        "profile_sha256",
                        "adapter_sha256",
                        "registry_sha256",
                    )
                },
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
)


def validate_protocol(path: Path, expected_sha256: str) -> dict:
    """Validate candidate declarations and referenced text, not primary evidence."""
    path = path.absolute()
    value, pin = read_json(path)
    if not _digest(expected_sha256) or pin != expected_sha256:
        raise ValueError("protocol_pin_mismatch")
    validate(value, SCHEMA)
    assert isinstance(value, dict)
    integers = [value["repeats"], value["technical_retries"], *value["generation"].values()]
    if any(type(item) is not int for item in integers):
        raise ValueError("invalid_integer_type")
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
    for ref in refs:
        if ref["path"].casefold() in paths:
            raise ValueError("duplicate_artifact_path")
        paths.add(ref["path"].casefold())
        try:
            artifact(path.parent, ref).decode("utf-8")
        except UnicodeError as exc:
            raise ValueError("invalid_artifact_utf8") from exc
    return {
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
