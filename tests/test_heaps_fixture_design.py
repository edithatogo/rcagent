"""Independent H3 fixture integrity; no HEAPS runtime or clinical qualification.

Expected dispositions are literal, pre-authored data. These tests check their
finite coverage and input arrangements, not whether an H4/H5 consumer implements
the expected behaviour. No production hashing, rendering or admission helper is
imported.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from copy import deepcopy
from pathlib import Path
from typing import Protocol, TypeAlias, cast

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/heaps"
ObjectMap: TypeAlias = dict[str, object]
PathPart: TypeAlias = str | int


class SchemaValidator(Protocol):
    """Describe the supported validation API without asserting payload validity."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


SCHEMAS = {
    "case": "conductor/schemas/safety-work.schema.json",
    "profile": "evaluation/heaps/heaps-profile.schema.json",
    "manifest": "evaluation/heaps/packet-manifest.schema.json",
    "decision": "evaluation/heaps/review-decision.schema.json",
    "status": "evaluation/heaps/status-receipt.schema.json",
}
VARIANT_COUNTS = {
    "HP01": 1,
    "HP02": 1,
    "HP03": 2,
    "HP04": 2,
    "HP05": 1,
    "HP06": 2,
    "HP07": 1,
    "HP08": 1,
    "HP09": 3,
    "HP10": 1,
    "HP11": 1,
    "HP12": 2,
    "HP13": 2,
    "HP14": 1,
    "HP15": 1,
    "HP16": 1,
    "HP17": 1,
    "HP18": 1,
    "HP19": 1,
    "HP20": 2,
    "HP21": 3,
    "HP22": 2,
    "HP23": 1,
    "HP24": 2,
    "HP25": 2,
}


def _mapping(value: object) -> ObjectMap:
    assert isinstance(value, dict), "fixture value must be an object"
    broad = cast("dict[object, object]", value)
    assert all(isinstance(key, str) for key in broad), "fixture keys must be text"
    return cast("ObjectMap", value)


def _sequence(value: object) -> list[object]:
    assert isinstance(value, list), "fixture value must be an array"
    return cast("list[object]", value)


def _text(value: object) -> str:
    assert isinstance(value, str), "fixture value must be text"
    return value


def _read(path: Path) -> ObjectMap:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    return _mapping(value)


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def _pretty(value: object, *, sorted_keys: bool = False, indent: int = 2) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=sorted_keys,
            indent=indent,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _reverse_keys(value: object) -> object:
    if isinstance(value, dict):
        broad = cast("dict[object, object]", value)
        return {key: _reverse_keys(item) for key, item in reversed(_mapping(broad).items())}
    if isinstance(value, list):
        return [_reverse_keys(item) for item in cast("list[object]", value)]
    return value


def _path(value: object) -> list[PathPart]:
    result: list[PathPart] = []
    for item in _sequence(value):
        assert isinstance(item, (str, int))
        assert not isinstance(item, bool)
        result.append(item)
    assert result, "literal mutation paths must be nonempty"
    return result


def _child(value: object, part: PathPart) -> object:
    if isinstance(part, int):
        return _sequence(value)[part]
    return _mapping(value)[part]


def _apply(document: ObjectMap, mutation: ObjectMap) -> None:
    parts = _path(mutation["path"])
    parent: object = document
    for part in parts[:-1]:
        parent = _child(parent, part)
    last = parts[-1]
    operation = mutation["operation"]
    assert operation in {"replace", "add"}
    if isinstance(last, int):
        assert operation == "replace"
        _sequence(parent)[last] = deepcopy(mutation["value"])
    else:
        target = _mapping(parent)
        assert (last in target) == (operation == "replace")
        target[last] = deepcopy(mutation["value"])


def _documents(variant: ObjectMap) -> dict[str, ObjectMap]:
    result = {
        key: _read(FIXTURES / _text(path)) for key, path in _mapping(variant["documents"]).items()
    }
    for value in _sequence(variant["mutations"]):
        mutation = _mapping(value)
        _apply(result[_text(mutation["document"])], mutation)
    return result


def _case_ingress(variant: ObjectMap, case: ObjectMap) -> bytes:
    presentation = variant["case_presentation"]
    if presentation == "round_trip":
        return _pretty(case, indent=4)
    if presentation == "object_key_reorder":
        return _pretty(_reverse_keys(case))
    assert presentation in {"stored", "identical_replay"}
    return _pretty(case)


def _rows(value: object) -> list[ObjectMap]:
    return [_mapping(item) for item in _sequence(value)]


ORACLE = _read(FIXTURES / "oracle.json")
VARIANTS = _rows(ORACLE["variants"])
BY_ID = {_text(row["id"]): row for row in VARIANTS}


def test_heaps_literal_coverage_is_25_cases_and_38_variants() -> None:
    acceptance = _read(ROOT / _text(ORACLE["acceptance_catalogue"]))
    cases = {_text(row["id"]) for row in _rows(acceptance["cases"])}
    assert cases == set(VARIANT_COUNTS)
    assert len(VARIANTS) == len(BY_ID) == 38
    assert Counter(_text(row["acceptance_id"]) for row in VARIANTS) == VARIANT_COUNTS
    assert Counter(row["control_kind"] for row in VARIANTS) == {
        "positive_control": 4,
        "boundary": 34,
    }
    assert Counter(_mapping(row["expected"])["preparation_disposition"] for row in VARIANTS) == {
        "prepare_draft": 22,
        "reject_input": 14,
        "abstain": 2,
    }
    assert Counter(_mapping(row["expected"])["review_disposition"] for row in VARIANTS) == {
        "not_established": 31,
        "stale": 5,
        "withheld": 2,
    }
    denominator = _mapping(ORACLE["denominator"])
    assert denominator == {
        "acceptance_cases": 25,
        "variants": 38,
        "positive_controls": 4,
        "adversarial_or_boundary_variants": 34,
        "expected_prepare_draft": 22,
        "expected_reject_input": 14,
        "expected_abstain": 2,
        "expected_review_not_established": 31,
        "expected_review_stale": 5,
        "expected_review_withheld": 2,
        "per_acceptance_case": VARIANT_COUNTS,
    }
    rules = {
        _text(rule) for row in VARIANTS for rule in _sequence(_mapping(row["expected"])["rule_ids"])
    }
    assert len(rules) == 34
    assert rules == set(_sequence(_mapping(ORACLE["vocabulary"])["rule_ids"]))


@pytest.mark.parametrize("variant", VARIANTS, ids=[_text(row["id"]) for row in VARIANTS])
def test_heaps_literal_input_shapes_and_identities(variant: ObjectMap) -> None:
    documents = _documents(variant)
    expected = _mapping(variant["expected"])
    validity = _mapping(expected["schema_validity"])
    keywords = _mapping(expected["schema_error_keywords"])
    assert set(documents) == set(validity) == set(keywords)
    for kind, document in documents.items():
        schema = _read(ROOT / SCHEMAS[kind])
        # The installed upstream stub also exposes a partially untyped deprecated
        # overload. Narrow only the supported API; document values stay object.
        validator = cast(SchemaValidator, Draft202012Validator(schema))
        errors = list(validator.iter_errors(document))
        assert (not errors) is validity[kind], (variant["id"], kind)
        assert sorted(str(error.validator) for error in errors) == keywords[kind]
    case = documents["case"]
    profile = documents["profile"]
    identity = _mapping(expected["input_identity"])
    assert identity == {
        "case_canonical_fingerprint": "sha256:" + _sha(_canonical(case)),
        "case_ingress_raw_sha256": _sha(_case_ingress(variant, case)),
        "normalized_case_sha256": _sha(_pretty(case, sorted_keys=True)),
        "profile_ingress_raw_sha256": _sha(_pretty(profile)),
        "normalized_profile_sha256": _sha(_pretty(profile, sorted_keys=True)),
    }


def test_heaps_source_bytes_are_original_synthetic_and_locked() -> None:
    manifest = _read(FIXTURES / "source-manifest.json")
    sources = _rows(manifest["sources"])
    assert len(sources) == 7
    assert len({_text(row["path"]) for row in sources}) == 7
    for source in sources:
        raw = (FIXTURES / _text(source["path"])).read_bytes()
        assert source["sha256"] == _sha(raw)
        assert source["bytes"] == len(raw)
        assert source["data_class"] == "generated_synthetic"
        assert raw.decode("utf-8").startswith("GENERATED SYNTHETIC")
    core = _read(FIXTURES / "canonical/base-case.json")
    originals = {_text(row["source_id"]): row for row in sources if row["derivation"] == "original"}
    assert len(originals) == 5
    assert len(_rows(core["sources"])) == 4
    for source in _rows(core["sources"]):
        original = originals[_text(source["source_id"])]
        assert source["fingerprint"] == "sha256:" + _text(original["sha256"])
    for evidence in _rows(core["evidence"]):
        original = originals[_text(evidence["source_id"])]
        assert (
            _text(evidence["content"]).encode("utf-8")
            == (FIXTURES / _text(original["path"])).read_bytes()
        )
        assert evidence["fingerprint"] == "sha256:" + _text(original["sha256"])
    assert "révision µ" in _text(_rows(core["evidence"])[0]["content"])
    escaped = json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    assert _sha(escaped) != _sha(_canonical(core))


@pytest.mark.parametrize("filename", ["base-manifest.json", "revised-report-manifest.json"])
def test_heaps_detached_input_manifests_bind_exact_artifact_bytes(filename: str) -> None:
    manifest = _read(FIXTURES / "packet" / filename)
    groups = _mapping(manifest["components"])
    artifacts = [_mapping(groups[key]) for key in ["case", "profile", "mapping", "template"]]
    for key in ["sources", "reports", "supporting_artifacts"]:
        rows = _rows(groups[key])
        assert [_text(row["path"]) for row in rows] == sorted(_text(row["path"]) for row in rows)
        artifacts.extend(rows)
    assert len(artifacts) == len({_text(row["path"]) for row in artifacts})
    for artifact in artifacts:
        raw = (FIXTURES / _text(artifact["path"])).read_bytes()
        assert artifact["sha256"] == _sha(raw)
        assert artifact["bytes"] == len(raw)
    assert not {"decision", "approval", "status", "manifest"}.intersection(groups)


def test_heaps_simulated_decision_only_matches_original_input_manifest() -> None:
    decision = _read(FIXTURES / "packet/simulated-approved-decision.json")
    binding = _mapping(decision["manifest_binding"])
    original = (FIXTURES / "packet/base-manifest.json").read_bytes()
    revised = (FIXTURES / "packet/revised-report-manifest.json").read_bytes()
    assert binding["raw_sha256"] == _sha(original)
    assert binding["raw_sha256"] != _sha(revised)
    assert decision["authority_status"] == "unverified"
    assert decision["substantive_approval"] == "not_established"
    assert decision["scope"] == "heaps-synthetic-draft-packet"
    for identifier in ["HP12-template-revision", "HP12-source-revision"]:
        variant = BY_ID[identifier]
        overrides = _mapping(variant["raw_artifact_overrides"])
        assert len(overrides) == 1
        for previous, replacement in overrides.items():
            assert (FIXTURES / previous).read_bytes() != (
                FIXTURES / _text(replacement)
            ).read_bytes()
        assert _mapping(variant["expected"])["review_disposition"] == "stale"


def test_heaps_key_order_is_not_array_order_or_raw_byte_identity() -> None:
    baseline = _documents(BY_ID["HP01-valid"])["case"]
    for identifier in ["HP21-identical-replay", "HP21-round-trip", "HP21-object-key-reorder"]:
        variant = BY_ID[identifier]
        case = _documents(variant)["case"]
        assert case == baseline
        assert _canonical(case) == _canonical(baseline)
        assert _pretty(case, sorted_keys=True) == _pretty(baseline, sorted_keys=True)
        if identifier != "HP21-identical-replay":
            assert _case_ingress(variant, case) != _pretty(baseline)
    for identifier in ["HP25-array-permutation", "HP25-canonical-content-change"]:
        documents = _documents(BY_ID[identifier])
        assert _canonical(documents["case"]) != _canonical(baseline)
        assert _mapping(documents["profile"]["case_binding"])["fingerprint"] == (
            "sha256:" + _sha(_canonical(baseline))
        )
        assert (
            _mapping(_mapping(BY_ID[identifier]["expected"])["required_states"])[
                "semantic_equivalence"
            ]
            == "not_asserted"
        )


def test_heaps_duplicate_derivative_retains_one_incident_source_family() -> None:
    profile = _documents(BY_ID["HP18-duplicate-source-family"])["profile"]
    incident = [
        row
        for row in _rows(profile["source_snapshots"])
        if "incident_evidence" in _sequence(row["purposes"])
    ]
    assert len(incident) == 4
    assert len({_text(row["source_family_id"]) for row in incident}) == 3
    derived = _rows(profile["source_families"])[-1]
    assert derived["family_id"] == "syn-family-record"
    assert derived["derived_from"] == [{"kind": "source", "id": "syn-src-record"}]
    assert derived["independence"] == "not_established"


def test_heaps_empty_and_all_abstain_are_distinct_finite_arrangements() -> None:
    for identifier, count in [("HP20-empty", 0), ("HP20-all-abstain", 7)]:
        variant = BY_ID[identifier]
        documents = _documents(variant)
        status = documents["status"]
        counts = _mapping(status["counts"])
        assert len(_sequence(documents["case"]["statements"])) == count
        assert counts == {"input_items": count, "usable_items": 0, "abstained_items": count}
        assert status["review"] == "not_requested"
        assert status["submission"] == "not_submitted"
        assert _mapping(variant["document_roles"])["status"] == (
            "illustrative_expected_status_not_input"
        )
        assert _mapping(status["profile_binding"])["raw_sha256"] == _sha(
            _pretty(documents["profile"])
        )
        expected = _mapping(variant["expected"])
        assert expected["preparation_disposition"] == "abstain"
        assert expected["review_disposition"] == "withheld"
        for statement in _rows(documents["case"]["statements"]):
            assert statement["withdrawn"] is True
            assert _mapping(statement["provenance"])["review_state"] == "withdrawn"
    assert _mapping(ORACLE["count_contract"])["unit"] == "canonical_statement"


def test_heaps_missing_clock_inputs_and_method_change_are_explicit() -> None:
    baseline = _documents(BY_ID["HP01-valid"])["profile"]
    changed = _documents(BY_ID["HP14-method-change"])["profile"]
    assert changed["selection"] != baseline["selection"]
    assert _mapping(changed["selection"])["decision_ref"] == {
        "kind": "decision",
        "id": "syn-stmt-method-handover",
    }
    handover_case = _documents(BY_ID["HP14-method-change"])["case"]
    handover = _rows(handover_case["statements"])[-1]
    assert handover["kind"] == "decision"
    assert "synthetic-preliminary-review is replaced by HEAPS" in _text(handover["text"])
    assert changed["clocks"] == baseline["clocks"]
    assert changed["deadlines"] == baseline["deadlines"]
    for identifier in ["HP13-missing-trigger", "HP13-missing-calendar"]:
        profile = _documents(BY_ID[identifier])["profile"]
        deadline = _rows(profile["deadlines"])[0]
        assert deadline["state"] == "unresolved"
        assert _mapping(deadline["due"])["value"] is None
    assert (
        _rows(_documents(BY_ID["HP13-missing-calendar"])["profile"]["deadlines"])[0][
            "calendar_snapshot_id"
        ]
        is None
    )
    source = _rows(baseline["source_snapshots"])[-1]
    assert source["purposes"] == ["obligation", "calendar"]
    assert source["source_kind"] == "generated_synthetic"
    assert source["state"] == "available"
    assert source["authority_status"] == "unverified"


def test_heaps_design_expectations_do_not_claim_runtime_or_authority() -> None:
    assert ORACLE["status"] == "frozen_independent_design"
    boundary = _mapping(ORACLE["execution_boundary"])
    assert boundary["h4"] == boundary["h5"] == "not_run"
    assert boundary["actual_human_or_organisational_acceptance"] == "not_established"
    for variant in VARIANTS:
        assert variant["execution"] == {"h4": "not_run", "h5": "not_run"}
        expected = _mapping(variant["expected"])
        assert {
            "clinical_review_completed",
            "statutory_rca_protection",
            "official_template_conformity",
            "external_submission",
            "independent_human_validation",
        }.issubset(set(_sequence(expected["prohibited_claims"])))
    profile = _read(FIXTURES / "packet/base-profile.json")
    assert not {"manifest", "approval", "decision_binding", "own_hash"}.intersection(profile)
    assert _mapping(profile["applicability"])["protection_status"] == "not_established"
    status = _read(FIXTURES / "packet/design-status.json")
    assert status["preparation"] == "not_started"
    assert status["structural_check"] == status["source_check"] == "not_checked"


def test_heaps_fixture_lock_covers_every_data_file() -> None:
    lock = _read(FIXTURES / "fixture-lock.json")
    rows = _rows(lock["artifacts"])
    actual_paths = {
        path.relative_to(FIXTURES).as_posix()
        for path in FIXTURES.rglob("*")
        if path.is_file() and path.name != "fixture-lock.json"
    }
    assert len(rows) == 22
    assert {_text(row["path"]) for row in rows} == actual_paths
    for row in rows:
        raw = (FIXTURES / _text(row["path"])).read_bytes()
        assert row["sha256"] == _sha(raw)
        assert row["bytes"] == len(raw)
