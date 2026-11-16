"""Independent H4 consumer regressions against the frozen H3 arrangements.

Expected outcomes and byte identities come from the prior fixture design, never
from assembler helpers. These checks exercise engineering behaviour; they do not
establish official-template fidelity or clinical/organisational acceptance.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import string
import subprocess
import sys
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Protocol, cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools import heaps

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/heaps"
EVALUATED_AT = "2030-01-07T02:00:00Z"
DETACHED_OUTPUTS = {
    "manifest.json",
    "status.json",
    "decision.json",
    "verification.json",
    "verification-input-manifest.json",
    "verification-input-status.json",
}


class SchemaValidator(Protocol):
    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


def _read(path: Path) -> ObjectMap:
    value: object = json.loads(path.read_bytes())
    return mapping(value)


def _json(value: object, *, sorted_keys: bool = False, indent: int = 2) -> bytes:
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


def _parsed(raw: bytes) -> ObjectMap:
    value: object = json.loads(raw)
    return mapping(value)


def _rows(value: object) -> list[ObjectMap]:
    return [mapping(item) for item in sequence(value)]


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _fingerprint(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    return "sha256:" + _sha(raw)


def _reverse_keys(value: object) -> object:
    if isinstance(value, dict):
        broad = cast("dict[object, object]", value)
        return {key: _reverse_keys(item) for key, item in reversed(mapping(broad).items())}
    if isinstance(value, list):
        return [_reverse_keys(item) for item in cast("list[object]", value)]
    return value


def _apply(document: ObjectMap, mutation: ObjectMap) -> None:
    path = sequence(mutation["path"])
    assert path
    parent: object = document
    for part in path[:-1]:
        if isinstance(part, str):
            parent = mapping(parent)[part]
        else:
            assert isinstance(part, int)
            assert not isinstance(part, bool)
            parent = sequence(parent)[part]
    final = path[-1]
    if isinstance(final, str):
        mapping(parent)[final] = deepcopy(mutation["value"])
    else:
        assert isinstance(final, int)
        assert not isinstance(final, bool)
        sequence(parent)[final] = deepcopy(mutation["value"])


@dataclass(frozen=True)
class Inputs:
    case: bytes
    profile: bytes
    artifacts: dict[str, bytes]
    manifest: bytes | None = None
    decision: bytes | None = None
    status: bytes | None = None

    def run(self, *, evaluated_at: str = EVALUATED_AT) -> heaps.PacketResult:
        return heaps.assemble_packet(
            self.case,
            self.profile,
            self.artifacts,
            evaluated_at=evaluated_at,
            template_path="packet/template-v1.md",
            manifest_bytes=self.manifest,
            decision_bytes=self.decision,
            status_bytes=self.status,
        )


ORACLE = _read(FIXTURES / "oracle.json")
VARIANTS = _rows(ORACLE["variants"])
BY_ID = {text_value(row["id"]): row for row in VARIANTS}


def _inputs(variant_id: str = "HP01-valid") -> Inputs:
    variant = BY_ID[variant_id]
    documents = {
        name: _read(FIXTURES / text_value(path))
        for name, path in mapping(variant["documents"]).items()
    }
    for mutation in _rows(variant["mutations"]):
        _apply(documents[text_value(mutation["document"])], mutation)
    case = documents["case"]
    if variant["case_presentation"] == "round_trip":
        case_raw = _json(case, indent=4)
    elif variant["case_presentation"] == "object_key_reorder":
        case_raw = _json(_reverse_keys(case))
    else:
        case_raw = _json(case)
    profile_raw = _json(documents["profile"])
    artifacts = {
        path.relative_to(FIXTURES).as_posix(): path.read_bytes()
        for folder in ["sources", "packet", "canonical"]
        for path in (FIXTURES / folder).rglob("*")
        if path.is_file()
    }
    paths = mapping(variant["documents"])
    artifacts[text_value(paths["case"])] = case_raw
    artifacts[text_value(paths["profile"])] = profile_raw
    for path, replacement in mapping(variant["raw_artifact_overrides"]).items():
        artifacts[path] = (FIXTURES / text_value(replacement)).read_bytes()
    roles = mapping(variant["document_roles"])

    def consumed(name: str) -> bytes | None:
        if name not in documents or roles[name] != "consumer_input":
            return None
        return _json(documents[name])

    return Inputs(
        case_raw,
        profile_raw,
        artifacts,
        consumed("manifest"),
        consumed("decision"),
        consumed("status"),
    )


def _rebound(inputs: Inputs, case: ObjectMap, profile: ObjectMap | None = None) -> Inputs:
    profile = _parsed(inputs.profile) if profile is None else profile
    binding = mapping(profile["case_binding"])
    binding["case_id"] = case["case_id"]
    binding["version"] = case["version"]
    binding["fingerprint"] = _fingerprint(case)
    return replace(inputs, case=_json(case), profile=_json(profile))


def _status(result: heaps.PacketResult) -> ObjectMap:
    assert result.status is not None
    return mapping(result.status)


def _report(result: heaps.PacketResult) -> str:
    return _visible_markdown(result.files["report.md"])


def _visible_markdown(raw: bytes) -> str:
    # A Markdown escape is presentation, not omitted source text. Keep the raw
    # byte checks separate; compare visible punctuation for fidelity assertions.
    return re.sub(r"\\([" + re.escape(string.punctuation) + r"])", r"\1", raw.decode("utf-8"))


def _inventory(manifest: ObjectMap) -> list[ObjectMap]:
    groups = mapping(manifest["components"])
    result = [mapping(groups[name]) for name in ["case", "profile", "mapping", "template"]]
    for name in ["sources", "supporting_artifacts", "reports"]:
        rows = _rows(groups[name])
        paths = [text_value(row["path"]) for row in rows]
        assert paths == sorted(paths)
        result.extend(rows)
    return result


@pytest.mark.parametrize("variant_id", list(BY_ID))
def test_frozen_h3_dispositions_on_actual_consumer(variant_id: str) -> None:
    inputs = _inputs(variant_id)
    expected = mapping(BY_ID[variant_id]["expected"])
    identities = mapping(expected["input_identity"])
    assert _sha(inputs.case) == identities["case_ingress_raw_sha256"]
    assert _sha(inputs.profile) == identities["profile_ingress_raw_sha256"]
    result = inputs.run()
    assert result.preparation_disposition == expected["preparation_disposition"], result.errors
    assert result.review_disposition == expected["review_disposition"], result.errors
    if result.preparation_disposition == "reject_input":
        assert result.errors
        assert "report.md" not in result.files
        for identifier in sequence(expected["retained_ids"]):
            assert text_value(identifier) in "\n".join(result.errors)
        return
    status = _status(result)
    assert status["clinical_review"] == "not_established"
    assert status["actual_authority"] == "unverified"
    assert status["submission"] == "not_submitted"
    assert status["source_check_scope"] == "record_reference_integrity"
    assert result.files["case.json"] == _json(_parsed(inputs.case), sorted_keys=True)
    assert result.files["profile.json"] == _json(_parsed(inputs.profile), sorted_keys=True)
    if result.preparation_disposition == "prepare_draft":
        assert status["preparation"] == "prepared"
        assert status["structural_check"] == "passed"
    for identifier in sequence(expected["retained_ids"]):
        assert text_value(identifier) in "\n".join(
            raw.decode("utf-8") for name, raw in result.files.items() if name.endswith(".md")
        )


def test_packet_manifest_and_status_match_exact_output_bytes() -> None:
    inputs = _inputs()
    result = inputs.run()
    assert not result.errors
    manifest = _parsed(result.files["manifest.json"])
    entries = _inventory(manifest)
    paths = [text_value(row["path"]) for row in entries]
    ids = [text_value(row["artifact_id"]) for row in entries]
    assert len(paths) == len(set(paths))
    assert len(ids) == len(set(ids))
    assert "manifest.json" not in paths
    assert "status.json" not in paths
    assert set(paths) == set(result.files) - DETACHED_OUTPUTS
    for entry in entries:
        raw = result.files[text_value(entry["path"])]
        assert entry["bytes"] == len(raw)
        assert entry["sha256"] == _sha(raw)
    raw_entries = [result.files[path] for path in paths]
    assert inputs.case in raw_entries
    assert inputs.profile in raw_entries
    for name, schema_file in [
        ("manifest.json", "packet-manifest.schema.json"),
        ("status.json", "status-receipt.schema.json"),
    ]:
        schema = _read(ROOT / "evaluation/heaps" / schema_file)
        validator = cast(SchemaValidator, Draft202012Validator(schema))
        assert not list(validator.iter_errors(_parsed(result.files[name])))
    status = _status(result)
    assert mapping(status["manifest_binding"])["raw_sha256"] == _sha(result.files["manifest.json"])
    assert mapping(status["profile_binding"])["raw_sha256"] == _sha(result.files["profile.json"])
    for name in [
        "case.json",
        "profile.json",
        "mapping.json",
        "manifest.json",
        "status.json",
        "verification.json",
    ]:
        raw = result.files[name]
        assert raw == _json(_parsed(raw), sorted_keys=True)
    for name in ["report.md", "chronology.md", "actions.md"]:
        raw = result.files[name]
        assert raw.endswith(b"\n")
        assert not raw.endswith(b"\n\n")
        assert b"\r" not in raw
        assert not raw.startswith(b"\xef\xbb\xbf")


@pytest.mark.parametrize(
    "variant_id", ["HP01-valid", "HP07-report-after-approval", "HP16-no-submission-receipt"]
)
def test_detached_verification_receipt_binds_exact_input_manifest_and_current_observation(
    variant_id: str,
) -> None:
    inputs = _inputs(variant_id)
    result = inputs.run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    receipt = _parsed(result.files["verification.json"])
    assert receipt["schema_version"] == "heaps-verification-1.0"
    assert receipt["scope"] == "synthetic_packet_verification"
    assert receipt["data_class"] == "generated_synthetic"
    assert receipt["privacy_mode"] == "fully_local"
    assert receipt["actual_authority"] == "unverified"
    assert receipt["clinical_review"] == "not_established"
    assert receipt["submission"] == "not_submitted"
    assert receipt["generated_manifest_sha256"] == _sha(result.files["manifest.json"])
    assert receipt["status_sha256"] == _sha(result.files["status.json"])
    assert receipt["input_status_sha256"] is None
    assert "verification-input-status.json" not in result.files
    assert receipt["evaluated_at"] == EVALUATED_AT
    if inputs.manifest is None:
        assert receipt["input_manifest_sha256"] is None
        assert "verification-input-manifest.json" not in result.files
    else:
        assert receipt["input_manifest_sha256"] == _sha(inputs.manifest)
        assert result.files["verification-input-manifest.json"] == inputs.manifest
    paths = {text_value(row["path"]) for row in _inventory(_parsed(result.files["manifest.json"]))}
    assert not paths.intersection(DETACHED_OUTPUTS)
    assert paths == set(result.files) - DETACHED_OUTPUTS


def test_supplied_status_raw_identity_is_detached_from_recomputed_observation() -> None:
    inputs = _inputs()
    original = inputs.run()
    supplied = original.files["status.json"]
    reordered = _json(_reverse_keys(_parsed(supplied)), indent=4)
    assert supplied != reordered
    assert _parsed(supplied) == _parsed(reordered)
    results = [replace(inputs, status=raw).run() for raw in [supplied, reordered]]
    for raw, result in zip([supplied, reordered], results, strict=True):
        assert result.preparation_disposition == "prepare_draft", result.errors
        assert result.files["manifest.json"] == original.files["manifest.json"]
        assert result.files["status.json"] == original.files["status.json"]
        assert result.files["verification-input-status.json"] == raw
        receipt = _parsed(result.files["verification.json"])
        assert receipt["input_status_sha256"] == _sha(raw)
        assert receipt["status_sha256"] == _sha(original.files["status.json"])
    assert results[0].files["verification.json"] != results[1].files["verification.json"]


def test_supplied_status_narrative_is_admitted_before_raw_retention() -> None:
    inputs = _inputs()
    status = _parsed(inputs.run().files["status.json"])
    status["limitations"] = ["<script>synthetic active-content probe</script>"]
    result = replace(inputs, status=_json(status)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert not result.files


def test_replay_and_ingress_identity_are_separate_from_normalized_values() -> None:
    first = _inputs().run()
    assert first.files == _inputs("HP21-identical-replay").run().files
    for variant_id in ["HP21-round-trip", "HP21-object-key-reorder"]:
        other = _inputs(variant_id).run()
        assert other.preparation_disposition == first.preparation_disposition
        assert other.files["case.json"] == first.files["case.json"]
        assert other.files["profile.json"] == first.files["profile.json"]
        assert other.files["manifest.json"] != first.files["manifest.json"]


def test_mutating_returned_status_cannot_change_later_deterministic_results() -> None:
    inputs = _inputs()
    artifacts_before = dict(inputs.artifacts)
    first = inputs.run()
    original_files = dict(first.files)
    sequence(_status(first)["limitations"]).append("Synthetic caller mutation must remain local.")
    mapping(_status(first)["counts"])["usable_items"] = 0
    second = inputs.run()
    assert second.files == original_files
    assert inputs.artifacts == artifacts_before


def test_profile_object_key_order_changes_only_raw_ingress_identity() -> None:
    inputs = _inputs()
    first = inputs.run()
    reordered = replace(inputs, profile=_json(_reverse_keys(_parsed(inputs.profile)))).run()
    assert reordered.preparation_disposition == "prepare_draft", reordered.errors
    for path in [
        "case.json",
        "profile.json",
        "mapping.json",
        "report.md",
        "chronology.md",
        "actions.md",
    ]:
        assert reordered.files[path] == first.files[path], path
    assert reordered.files["manifest.json"] != first.files["manifest.json"]


def test_report_retains_conflict_uncertainty_participation_and_original_kind() -> None:
    inputs = _inputs("HP08-conflicting-accounts")
    result = inputs.run()
    report = _report(result)
    case = _parsed(inputs.case)
    for statement in _rows(case["statements"]):
        assert text_value(statement["statement_id"]) in report
        assert text_value(statement["text"]) in report
        assert text_value(statement["uncertainty"]) in report
    profile = _parsed(inputs.profile)
    for context in _rows(profile["finding_context"]):
        for key in ["supporting_refs", "contrary_refs", "alternative_refs"]:
            for reference in _rows(context[key]):
                assert text_value(reference["id"]) in report
        assert text_value(context["uncertainty"]) in report
    for row in _rows(profile["participation"]):
        assert text_value(row["state_note"]) in report
    assert "reported_account" in report
    assert "hypothesis" in report
    assert not report.startswith("# CONFIDENTIAL")
    assert _status(result)["review"] == "not_requested"


@pytest.mark.parametrize("variant_id", ["HP20-empty", "HP20-all-abstain"])
def test_empty_and_all_abstain_counts_are_derived_from_case(variant_id: str) -> None:
    inputs = _inputs(variant_id)
    assert inputs.status is None
    result = inputs.run()
    states = mapping(mapping(BY_ID[variant_id]["expected"])["required_states"])
    status = _status(result)
    assert status["preparation"] == states["preparation"]
    assert status["counts"] == states["counts"]
    assert status["review"] != "synthetic_draft_reviewed"


def test_action_status_does_not_promote_effectiveness() -> None:
    result = _inputs("HP15-implemented-without-outcomes").run()
    actions = _visible_markdown(result.files["actions.md"])
    assert "syn-action-mockup" in actions
    assert "implemented" in actions
    assert "pending_evidence" in actions
    assert "syn-outcome-mockup" in actions
    assert "pending" in actions
    assert (
        "No operational action, outcome evidence or clinical effectiveness is asserted." in actions
    )


def test_chronology_preserves_three_clocks_and_does_not_fill_missing_times() -> None:
    inputs = _inputs()
    chronology = _visible_markdown(inputs.run().files["chronology.md"])
    for row in _rows(_parsed(inputs.profile)["chronology"]):
        assert text_value(mapping(row["statement_ref"])["id"]) in chronology
        assert text_value(row["ordering_note"]) in chronology
        for field in ["event_time", "document_time", "available_time"]:
            value = mapping(row[field])
            assert text_value(value["uncertainty"]) in chronology
    assert "2030-01-06T23:30:00Z" in chronology
    assert "unknown" in chronology


def test_unsupported_recommendation_remains_explicitly_incomplete() -> None:
    inputs = _inputs("HP05-unsupported-recommendation")
    result = inputs.run()
    actions = _visible_markdown(result.files["actions.md"])
    assert "syn-stmt-recommendation" in actions
    assert "incomplete" in _report(result).lower()
    assert "accepted recommendations: 0" in _report(result).lower()
    assert _status(result)["review"] == "not_requested"
    assert _rows(_parsed(result.files["profile.json"])["action_context"])[0]["finding_refs"] == []
    assert _rows(_parsed(result.files["profile.json"])["action_context"])[0]["condition_refs"] == []


@pytest.mark.parametrize(
    "variant_id",
    ["HP09-participation-missing", "HP09-participation-declined", "HP09-participation-unavailable"],
)
def test_participation_gaps_remain_visible_without_agreement(variant_id: str) -> None:
    inputs = _inputs(variant_id)
    result = inputs.run()
    consumer = _rows(_parsed(inputs.profile)["participation"])[1]
    report = _report(result)
    assert text_value(consumer["state"]) in report
    assert text_value(consumer["state_note"]) in report
    assert "syn-role-consumer" in report
    assert "syn-stmt-consumer" in report
    assert text_value(sequence(consumer["needs"])[0]) in report
    assert _status(result)["review"] == "not_requested"


def test_unavailable_template_does_not_block_or_invent_official_conformity() -> None:
    inputs = _inputs("HP11-unavailable-local-template")
    result = inputs.run()
    assert result.preparation_disposition == "prepare_draft"
    assert _status(result)["template_mapping"] == "unavailable"
    gaps = sequence(mapping(_parsed(inputs.profile)["template_mapping"])["gaps"])
    for gap in gaps:
        assert text_value(gap) in _report(result)
    assert result.files["template.md"]


@pytest.mark.parametrize("variant_id", ["HP13-missing-trigger", "HP13-missing-calendar"])
def test_unresolved_deadlines_are_rendered_without_fabricated_due_time(variant_id: str) -> None:
    inputs = _inputs(variant_id)
    result = inputs.run()
    deadline = _rows(_parsed(result.files["profile.json"])["deadlines"])[0]
    assert deadline["state"] == "unresolved"
    assert mapping(deadline["due"])["value"] is None
    view = _visible_markdown(result.files["chronology.md"]) + _report(result)
    assert "syn-deadline-training" in view
    assert text_value(mapping(deadline["due"])["uncertainty"]) in view
    assert "2030-01-08T00:00:00Z" not in view


def test_method_handover_retains_existing_clocks_and_unresolved_routes() -> None:
    result = _inputs("HP14-method-change").run()
    profile = _parsed(result.files["profile.json"])
    clocks = mapping(profile["clocks"])
    assert mapping(clocks["awareness"])["value"] == "2030-01-07T00:00:00Z"
    assert mapping(clocks["sac1_reporting"])["value"] is None
    assert mapping(clocks["review_submission"])["value"] is None
    due = mapping(_rows(profile["deadlines"])[0]["due"])
    assert due["value"] == "2030-01-08T00:00:00Z"
    view = _visible_markdown(result.files["chronology.md"]) + _report(result)
    assert "2030-01-07T00:00:00Z" in view
    assert "2030-01-08T00:00:00Z" in view
    assert "synthetic-preliminary-review" in view
    assert "syn-stmt-method-handover" in view


def test_derivative_source_family_is_retained_and_not_an_independent_observation() -> None:
    result = _inputs("HP18-duplicate-source-family").run()
    profile = _parsed(result.files["profile.json"])
    incident = [
        row
        for row in _rows(profile["source_snapshots"])
        if "incident_evidence" in sequence(row["purposes"])
    ]
    assert len(incident) == 4
    assert len({text_value(row["source_family_id"]) for row in incident}) == 3
    lineage = [
        row
        for row in _rows(profile["source_families"])
        if mapping(row["source_ref"])["id"] == "syn-src-record-summary"
    ]
    assert len(lineage) == 1
    assert lineage[0]["family_id"] == "syn-family-record"
    assert lineage[0]["derived_from"] == [{"kind": "source", "id": "syn-src-record"}]
    assert lineage[0]["independence"] == "not_established"
    report = _report(result)
    for identifier in ["syn-src-record-summary", "syn-src-record", "syn-family-record"]:
        assert identifier in report
    assert "not_established" in report


def test_optional_unqualified_component_is_not_used_to_establish_a_graph() -> None:
    result = _inputs("HP22-accimap-unqualified").run()
    assert result.preparation_disposition == "prepare_draft"
    report = _report(result).lower()
    assert "accimap" in report
    assert "unqualified" in report
    assert _status(result)["source_check_scope"] == "record_reference_integrity"
    assert not any(path.endswith((".mmd", ".svg")) for path in result.files)


def test_concurrent_route_questions_remain_open_in_the_report() -> None:
    inputs = _inputs("HP23-concurrent-routes")
    result = inputs.run()
    report = _report(result)
    for row in _rows(_parsed(inputs.profile)["open_route_questions"]):
        assert text_value(row["route"]) in report
        assert text_value(row["question"]) in report
        assert row["state"] == "open"
    assert _status(result)["submission"] == "not_submitted"


def _taxonomy_inputs() -> Inputs:
    inputs = _inputs()
    case = _parsed(inputs.case)
    profile = _parsed(inputs.profile)
    raw = b"GENERATED SYNTHETIC TAXONOMY version 1\nCategory syn-category-prompt: fictional prompt labels only.\n"
    sequence(case["sources"]).append(
        {
            "source_id": "syn-src-taxonomy",
            "source_type": "other",
            "title": "Original synthetic taxonomy",
            "fingerprint": "sha256:" + _sha(raw),
            "acquired_at": "2030-01-07T01:00:00Z",
            "authority": "Synthetic test only; no clinical or organisational authority.",
            "citation": "sources/taxonomy.txt",
            "screening_state": "included",
            "late": False,
        }
    )
    sequence(profile["source_snapshots"]).append(
        {
            "snapshot_id": "syn-snapshot-taxonomy",
            "source_id": "syn-src-taxonomy",
            "source_family_id": "syn-family-taxonomy",
            "state": "available",
            "raw_sha256": _sha(raw),
            "rights_status": "original_synthetic",
            "authority_status": "unverified",
            "version": "1",
            "locator": "synthetic:sources/taxonomy.txt",
            "source_kind": "generated_synthetic",
            "purposes": ["taxonomy"],
            "applicability": "applies_synthetic",
        }
    )
    sequence(profile["source_families"]).append(
        {
            "source_ref": {"kind": "source", "id": "syn-src-taxonomy"},
            "family_id": "syn-family-taxonomy",
            "derived_from": [],
            "independence": "not_established",
        }
    )
    _rows(profile["factor_assignments"])[0].update(
        {
            "state": "mapped",
            "taxonomy_id": "syn-snapshot-taxonomy",
            "taxonomy_version": "1",
            "taxonomy_authority": "original_synthetic",
            "categories": ["syn-category-prompt"],
            "rationale": "Declared synthetic label only; category fit and clinical meaning remain unverified.",
        }
    )
    return _rebound(
        replace(inputs, artifacts={**inputs.artifacts, "sources/taxonomy.txt": raw}), case, profile
    )


@pytest.mark.parametrize("taxonomy_id", ["syn-snapshot-taxonomy", "syn-src-taxonomy"])
def test_mapped_taxonomy_requires_captured_versioned_source_without_claiming_fit(
    taxonomy_id: str,
) -> None:
    inputs = _taxonomy_inputs()
    profile = _parsed(inputs.profile)
    _rows(profile["factor_assignments"])[0]["taxonomy_id"] = taxonomy_id
    result = replace(inputs, profile=_json(profile)).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert result.files["sources/taxonomy.txt"] == inputs.artifacts["sources/taxonomy.txt"]
    assert "syn-category-prompt" in _report(result)
    assert "category fit and clinical meaning remain unverified" in _report(result)
    assert _status(result)["clinical_review"] == "not_established"


@pytest.mark.parametrize(
    "defect", ["missing_id", "wrong_version", "unavailable", "wrong_purpose", "changed_bytes"]
)
def test_taxonomy_mapping_cannot_invent_missing_source_or_version(defect: str) -> None:
    inputs = _taxonomy_inputs()
    profile = _parsed(inputs.profile)
    assignment = _rows(profile["factor_assignments"])[0]
    snapshot = _rows(profile["source_snapshots"])[-1]
    artifacts = dict(inputs.artifacts)
    if defect == "missing_id":
        assignment["taxonomy_id"] = "syn-missing-taxonomy"
    elif defect == "wrong_version":
        assignment["taxonomy_version"] = "2"
    elif defect == "unavailable":
        snapshot["state"] = "unavailable"
        snapshot["raw_sha256"] = None
    elif defect == "wrong_purpose":
        snapshot["purposes"] = ["context"]
    else:
        artifacts["sources/taxonomy.txt"] += b"Changed synthetic bytes.\n"
    result = replace(inputs, profile=_json(profile), artifacts=artifacts).run()
    assert result.preparation_disposition == "reject_input"
    errors = "\n".join(result.errors)
    assert ("raw_byte_identity" if defect == "changed_bytes" else "taxonomy") in errors


@pytest.mark.parametrize("exclusion", ["withdrawn_flag", "withdrawn_state", "rejected_state"])
def test_partial_abstention_counts_and_reason_survive_preparation(exclusion: str) -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    statement = deepcopy(_rows(case["statements"])[0])
    statement["statement_id"] = "syn-stmt-excluded"
    statement["uncertainty"] = "Synthetic retained history; excluded from usable draft items."
    if exclusion == "withdrawn_flag":
        statement["withdrawn"] = True
    else:
        mapping(statement["provenance"])["review_state"] = (
            "withdrawn" if exclusion == "withdrawn_state" else "rejected"
        )
    sequence(case["statements"]).append(statement)
    result = _rebound(inputs, case).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert _status(result)["counts"] == {"input_items": 8, "usable_items": 7, "abstained_items": 1}
    report = _report(result)
    assert "syn-stmt-excluded" in report
    assert text_value(statement["uncertainty"]) in report
    assert "withdrawn" in report if exclusion != "rejected_state" else "rejected" in report


@pytest.mark.parametrize(
    "raw",
    [
        b'{"a": 1, "a": 1}',
        b"\xef\xbb\xbf{}",
        b'{"a": "\xff"}',
        b'{"a": NaN}',
        b'{"a": Infinity}',
        b'{"a": -Infinity}',
        b'{"a": 1e400}',
        b'{"a": "\\ud800"}',
        b'{"a": "\\udfff"}',
        b"[]",
        b"null",
        b"{",
    ],
)
@pytest.mark.parametrize("document", ["case", "profile"])
def test_strict_ingress_never_repairs_invalid_json(raw: bytes, document: str) -> None:
    inputs = _inputs()
    invalid = replace(inputs, case=raw) if document == "case" else replace(inputs, profile=raw)
    result = invalid.run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert "report.md" not in result.files


@pytest.mark.parametrize("document", ["case", "profile"])
def test_equal_duplicate_keys_in_otherwise_valid_input_are_rejected(document: str) -> None:
    inputs = _inputs()
    raw = inputs.case if document == "case" else inputs.profile
    name, value = (
        ("schema_version", "1.1") if document == "case" else ("schema_version", "heaps-profile-1.0")
    )
    pair = f'  "{name}": "{value}",'.encode()
    assert pair in raw
    duplicate = raw.replace(pair, pair + b"\n" + pair, 1)
    # A permissive last-key-wins parser sees the original valid document.
    assert _parsed(duplicate) == _parsed(raw)
    invalid = (
        replace(inputs, case=duplicate)
        if document == "case"
        else replace(inputs, profile=duplicate)
    )
    result = invalid.run()
    assert result.preparation_disposition == "reject_input"
    assert "duplicate" in "\n".join(result.errors).lower()


@pytest.mark.parametrize("document", ["case", "profile"])
def test_bom_on_otherwise_valid_input_is_rejected(document: str) -> None:
    inputs = _inputs()
    raw = inputs.case if document == "case" else inputs.profile
    invalid = (
        replace(inputs, case=b"\xef\xbb\xbf" + raw)
        if document == "case"
        else replace(inputs, profile=b"\xef\xbb\xbf" + raw)
    )
    result = invalid.run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


def test_unpaired_surrogate_inside_schema_valid_profile_string_rejects_cleanly() -> None:
    inputs = _inputs()
    raw = inputs.profile.replace(b"Prepare a generated", b"\\ud800Prepare a generated", 1)
    result = replace(inputs, profile=raw).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None, 0, -1])
@pytest.mark.parametrize("document", ["case", "profile", "binding"])
def test_versions_require_exact_positive_integers(document: str, value: object) -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    profile = _parsed(inputs.profile)
    if document == "case":
        case["version"] = value
    elif document == "profile":
        profile["profile_version"] = value
    else:
        mapping(profile["case_binding"])["version"] = value
    result = replace(inputs, case=_json(case), profile=_json(profile)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


def test_integral_float_canonical_version_is_rejected_even_with_matching_digest() -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    case["version"] = 1.0
    profile = _parsed(inputs.profile)
    mapping(profile["case_binding"])["fingerprint"] = _fingerprint(case)
    # Keep profile.version and binding.version actual ints, so no stale hash or
    # malformed profile can mask admission of the non-integral representation.
    result = replace(inputs, case=_json(case), profile=_json(profile)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize(
    "invalid_time",
    [
        "2030-02-30T02:00:00Z",
        "2030-01-07T24:00:00Z",
        "2030-01-07T02:00:60Z",
        "2030-01-07T02:00:00",
        "2030-01-07",
        "2030-01-07T02:00:00+99:00",
    ],
)
def test_explicit_evaluation_time_is_strict(invalid_time: str) -> None:
    result = _inputs().run(evaluated_at=invalid_time)
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize("field", ["event_time", "document_time", "available_time"])
def test_impossible_profile_chronology_time_rejects(field: str) -> None:
    inputs = _inputs()
    profile = _parsed(inputs.profile)
    row = _rows(profile["chronology"])[0]
    row[field] = {
        "state": "known",
        "value": "2030-02-30T00:00:00Z",
        "precision": "second",
        "basis_refs": [{"kind": "source", "id": "syn-src-record"}],
        "uncertainty": "Deliberately invalid synthetic test time.",
    }
    result = replace(inputs, profile=_json(profile)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


def test_impossible_canonical_date_cannot_hide_behind_schema_format_gap() -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    _rows(case["sources"])[0]["acquired_at"] = "2030-02-30T00:00:00+10:00"
    result = _rebound(inputs, case).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize("field", ["reviewed_at", "deadline"])
def test_other_canonical_timestamps_are_strict_after_rebinding(field: str) -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    if field == "reviewed_at":
        mapping(_rows(case["statements"])[0]["provenance"])[field] = "2030-02-30T01:00:00Z"
    else:
        _rows(case["events"])[0][field] = "2030-02-30T01:00:00Z"
    result = _rebound(inputs, case).run()
    assert result.preparation_disposition == "reject_input"
    assert "time" in "\n".join(result.errors).lower()


@pytest.mark.parametrize("defect", ["duplicate_source", "unknown_source", "illegal_transition"])
def test_canonical_semantic_admission_precedes_rendering(defect: str) -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    if defect == "duplicate_source":
        sequence(case["sources"]).append(deepcopy(_rows(case["sources"])[0]))
    elif defect == "unknown_source":
        _rows(case["evidence"])[0]["source_id"] = "syn-unknown-source"
    else:
        _rows(case["events"])[0]["from_state"] = "closed"
    result = _rebound(inputs, case).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert "report.md" not in result.files


def _decision_for(result: heaps.PacketResult) -> ObjectMap:
    decision = _read(FIXTURES / "packet/simulated-approved-decision.json")
    manifest = _parsed(result.files["manifest.json"])
    binding = mapping(decision["manifest_binding"])
    binding["manifest_id"] = manifest["manifest_id"]
    binding["raw_sha256"] = _sha(result.files["manifest.json"])
    return decision


def test_matching_detached_synthetic_decision_does_not_change_packet_manifest() -> None:
    inputs = _inputs()
    original = inputs.run()
    decision = _json(_decision_for(original))
    reviewed = replace(inputs, decision=decision).run()
    assert reviewed.preparation_disposition == "prepare_draft", reviewed.errors
    assert reviewed.files["manifest.json"] == original.files["manifest.json"]
    assert reviewed.files["report.md"] == original.files["report.md"]
    assert reviewed.files["decision.json"] == decision
    status = _status(reviewed)
    assert status["review"] == "synthetic_draft_reviewed"
    assert status["clinical_review"] == "not_established"
    assert status["actual_authority"] == "unverified"
    assert status["submission"] == "not_submitted"
    assert mapping(status["decision_binding"])["raw_sha256"] == _sha(decision)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reviewer_role_ref", {"kind": "role", "id": "syn-role-facilitator"}),
        ("reviewer_role_ref", {"kind": "role", "id": "syn-role-not-present"}),
        ("author_role_ref", {"kind": "role", "id": "syn-role-not-present"}),
        ("reviewer_role_ref", None),
        ("conflict_state", "unresolved"),
        ("scope", "communication"),
        ("issued_at", "2030-02-30T00:00:00Z"),
        ("expires_at", "2030-02-30T00:00:00Z"),
        ("evaluated_at", "2030-02-30T00:00:00Z"),
        ("issued_at", "2030-01-07T02:00:01Z"),
        ("expires_at", EVALUATED_AT),
        ("expires_at", "2030-01-07T01:59:59Z"),
        ("evaluated_at", "2030-01-07T02:00:01Z"),
        ("evaluated_at", "2030-01-07T00:59:59Z"),
    ],
)
def test_invalid_synthetic_approval_is_not_admitted(field: str, value: object) -> None:
    inputs = _inputs()
    decision = _decision_for(inputs.run())
    decision[field] = value
    result = replace(inputs, decision=_json(decision)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert result.status is None or _status(result)["review"] != "synthetic_draft_reviewed"


def test_prior_valid_decision_evaluation_does_not_replace_current_observation_clock() -> None:
    inputs = _inputs()
    decision = _decision_for(inputs.run())
    decision["evaluated_at"] = "2030-01-07T01:59:59Z"
    raw = _json(decision)
    result = replace(inputs, decision=raw).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert _status(result)["review"] == "synthetic_draft_reviewed"
    assert _status(result)["evaluated_at"] == EVALUATED_AT
    assert result.files["decision.json"] == raw
    expired = replace(inputs, decision=raw).run(evaluated_at="2030-01-08T01:00:00Z")
    assert expired.preparation_disposition == "reject_input"
    assert expired.status is None or _status(expired)["review"] != "synthetic_draft_reviewed"


@pytest.mark.parametrize("decision_state", ["pending", "returned", "rejected"])
def test_nonapproved_decisions_remain_separate_from_preparation(decision_state: str) -> None:
    inputs = _inputs()
    decision = _decision_for(inputs.run())
    decision["decision"] = decision_state
    result = replace(inputs, decision=_json(decision)).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert _status(result)["review"] == decision_state
    assert _status(result)["clinical_review"] == "not_established"


def test_material_case_revision_stales_prior_decision_without_rewriting_it() -> None:
    inputs = _inputs()
    first = inputs.run()
    original_decision = _json(_decision_for(first))
    case = _parsed(inputs.case)
    case["version"] = 2
    _rows(case["statements"])[0]["uncertainty"] = "Revised synthetic uncertainty; still unresolved."
    revised = _rebound(inputs, case)
    result = replace(revised, decision=original_decision).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert result.review_disposition == "stale"
    assert _status(result)["review"] == "stale"
    assert result.files["decision.json"] == original_decision
    assert result.files["manifest.json"] != first.files["manifest.json"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("counts", {"input_items": 7, "usable_items": 0, "abstained_items": 7}),
        ("counts", {"input_items": 7, "usable_items": 8, "abstained_items": 0}),
        ("source_check_scope", "accepted_d0_byte_spans"),
        ("review", "synthetic_draft_reviewed"),
        ("template_mapping", "mapped_unverified"),
        ("preparation", "all_abstain"),
        ("submission", "submitted"),
        ("clinical_review", "completed"),
    ],
)
def test_positive_status_claims_cannot_override_executed_observations(
    field: str, value: object
) -> None:
    inputs = _inputs()
    status = _parsed(inputs.run().files["status.json"])
    status[field] = value
    result = replace(inputs, status=_json(status)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize(
    "defect",
    [
        "duplicate_id",
        "duplicate_path",
        "unsorted",
        "omitted_source",
        "bad_bytes",
        "bad_digest",
        "wrong_profile",
    ],
)
def test_manifest_cross_object_invariants_are_executed(defect: str) -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    manifest = _parsed(inputs.manifest)
    components = mapping(manifest["components"])
    sources = sequence(components["sources"])
    if defect == "duplicate_id":
        mapping(components["mapping"])["artifact_id"] = mapping(components["case"])["artifact_id"]
    elif defect == "duplicate_path":
        mapping(components["mapping"])["path"] = mapping(components["case"])["path"]
    elif defect == "unsorted":
        sources.reverse()
    elif defect == "omitted_source":
        sources.pop()
    elif defect == "bad_bytes":
        mapping(sources[0])["bytes"] = 1
    elif defect == "bad_digest":
        mapping(sources[0])["sha256"] = "0" * 64
    else:
        manifest["profile_id"] = "syn-other-profile"
    result = replace(inputs, manifest=_json(manifest)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert "report.md" not in result.files


def test_generated_manifest_can_be_admitted_as_a_later_input() -> None:
    inputs = _inputs()
    first = inputs.run()
    artifacts = {**inputs.artifacts, **first.files}
    result = replace(inputs, artifacts=artifacts, manifest=first.files["manifest.json"]).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert result.files["case.json"] == first.files["case.json"]
    assert result.files["profile.json"] == first.files["profile.json"]
    assert result.files["manifest.json"] == first.files["manifest.json"]
    assert result.files["verification.json"] != first.files["verification.json"]


@pytest.mark.parametrize(
    "path", ["report.md", "mapping.json", "ingress/old-report.md", "history/old-report.md"]
)
def test_every_consumed_historical_artifact_is_bound_regardless_of_filename(path: str) -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    historical_manifest = _parsed(inputs.manifest)
    if path.endswith(".json"):
        payload_a = _json({"data_class": "generated_synthetic", "report": "Unresolved account A."})
        payload_b = _json({"data_class": "generated_synthetic", "report": "Unresolved account B."})
    else:
        payload_a = b"# Original synthetic historical report\n\nUnresolved account A.\n"
        payload_b = b"# Revised synthetic historical report\n\nUnresolved account B.\n"
    descriptor: ObjectMap = {
        "artifact_id": "syn-historical-report",
        "path": path,
        "sha256": _sha(payload_a),
        "bytes": len(payload_a),
    }
    mapping(historical_manifest["components"])["reports"] = [descriptor]
    artifacts_a = {**inputs.artifacts, path: payload_a}
    manifest_a = _json(historical_manifest)
    first = replace(inputs, artifacts=artifacts_a, manifest=manifest_a).run()
    assert first.preparation_disposition == "prepare_draft", first.errors
    inventory_a = _inventory(_parsed(first.files["manifest.json"]))
    assert any(row["sha256"] == _sha(payload_a) for row in inventory_a)
    decision_a = _json(_decision_for(first))
    descriptor["sha256"] = _sha(payload_b)
    descriptor["bytes"] = len(payload_b)
    artifacts_b = {**inputs.artifacts, path: payload_b}
    second = replace(
        inputs, artifacts=artifacts_b, manifest=_json(historical_manifest), decision=decision_a
    ).run()
    assert second.preparation_disposition == "prepare_draft", second.errors
    inventory_b = _inventory(_parsed(second.files["manifest.json"]))
    assert any(row["sha256"] == _sha(payload_b) for row in inventory_b)
    assert second.files["manifest.json"] != first.files["manifest.json"]
    assert second.review_disposition == "stale"
    assert _status(second)["review"] == "stale"
    assert second.files["decision.json"] == decision_a


@pytest.mark.parametrize("group", ["case", "profile"])
def test_historical_case_and_profile_raw_bytes_are_not_discarded_by_value_equality(
    group: str,
) -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    historical = _parsed(inputs.manifest)
    first = inputs.run()
    assert first.preparation_disposition == "prepare_draft"
    original_decision = _json(_decision_for(first))
    descriptor = mapping(mapping(historical["components"])[group])
    path = text_value(descriptor["path"])
    original = inputs.artifacts[path]
    changed = _json(_parsed(original), indent=4)
    assert original != changed
    assert _parsed(original) == _parsed(changed)
    descriptor["sha256"] = _sha(changed)
    descriptor["bytes"] = len(changed)
    result = replace(
        inputs,
        artifacts={**inputs.artifacts, path: changed},
        manifest=_json(historical),
        decision=original_decision,
    ).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    assert result.review_disposition == "stale"
    assert result.files["manifest.json"] != first.files["manifest.json"]
    entries = _inventory(_parsed(result.files["manifest.json"]))
    assert any(row["sha256"] == _sha(changed) for row in entries)


def test_manifest_cannot_smuggle_an_unbound_additional_source() -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    manifest = _parsed(inputs.manifest)
    source = b"GENERATED SYNTHETIC extra source without a canonical source/profile binding.\n"
    sequence(mapping(manifest["components"])["sources"]).append(
        {
            "artifact_id": "syn-unbound-source",
            "path": "sources/z-extra.txt",
            "sha256": _sha(source),
            "bytes": len(source),
        }
    )
    result = replace(
        inputs,
        artifacts={**inputs.artifacts, "sources/z-extra.txt": source},
        manifest=_json(manifest),
    ).run()
    assert result.preparation_disposition == "reject_input"
    assert "source inventory" in "\n".join(result.errors)


@pytest.mark.parametrize(
    "path",
    [
        "verification.json",
        "verification-input-manifest.json",
        "verification-input-status.json",
        "status.json",
        "decision.json",
        "manifest.json",
    ],
)
def test_detached_output_names_cannot_be_admitted_as_construction_artifacts(path: str) -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    manifest = _parsed(inputs.manifest)
    raw = _json({"synthetic_note": "A reserved detached filename is not a construction artifact."})
    mapping(manifest["components"])["supporting_artifacts"] = [
        {
            "artifact_id": "syn-reserved-artifact",
            "path": path,
            "sha256": _sha(raw),
            "bytes": len(raw),
        }
    ]
    result = replace(
        inputs, artifacts={**inputs.artifacts, path: raw}, manifest=_json(manifest)
    ).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize("prefix", [b"", b"\xef\xbb\xbf"])
def test_receipt_payload_cannot_be_disguised_as_a_text_construction_artifact(prefix: bytes) -> None:
    inputs = _inputs("HP16-no-submission-receipt")
    assert inputs.manifest is not None
    manifest = _parsed(inputs.manifest)
    raw = prefix + (FIXTURES / "packet/design-status.json").read_bytes()
    path = "history/disguised-receipt.txt"
    mapping(manifest["components"])["supporting_artifacts"] = [
        {
            "artifact_id": "syn-disguised-status",
            "path": path,
            "sha256": _sha(raw),
            "bytes": len(raw),
        }
    ]
    result = replace(
        inputs, artifacts={**inputs.artifacts, path: raw}, manifest=_json(manifest)
    ).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "../escape.txt",
        "/absolute.txt",
        "sources/../escape.txt",
        "a\\b.txt",
        "CON",
        "nul.txt",
        "sources/file.",
        "sources/file ",
    ],
)
def test_unsafe_artifact_paths_cannot_enter_packet(unsafe_path: str) -> None:
    inputs = _inputs()
    artifacts = dict(inputs.artifacts)
    artifacts[unsafe_path] = b"synthetic unused unsafe path"
    result = replace(inputs, artifacts=artifacts).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


def test_casefold_colliding_paths_are_rejected_across_platforms() -> None:
    inputs = _inputs()
    artifacts = dict(inputs.artifacts)
    artifacts["sources/RECORD.txt"] = artifacts["sources/record.txt"]
    result = replace(inputs, artifacts=artifacts).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize("field", ["calendar_snapshot_id", "source_snapshot_id"])
def test_specified_deadline_requires_resolvable_source_and_calendar(field: str) -> None:
    inputs = _inputs()
    profile = _parsed(inputs.profile)
    _rows(profile["deadlines"])[0][field] = "syn-missing-snapshot"
    result = replace(inputs, profile=_json(profile)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@pytest.mark.parametrize(
    ("field", "value"),
    [("version", None), ("purposes", ["incident_evidence"]), ("state", "unavailable")],
)
def test_specified_deadline_needs_admitted_versioned_calendar(field: str, value: object) -> None:
    inputs = _inputs()
    profile = _parsed(inputs.profile)
    _rows(profile["source_snapshots"])[3][field] = value
    result = replace(inputs, profile=_json(profile)).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@given(st.integers(min_value=0, max_value=389), st.integers(min_value=1, max_value=255))
@settings(max_examples=30, deadline=None)
def test_generated_single_byte_source_tampering_rejects(index: int, xor_mask: int) -> None:
    inputs = _inputs()
    artifacts = dict(inputs.artifacts)
    source = bytearray(artifacts["sources/record.txt"])
    source[index] ^= xor_mask
    artifacts["sources/record.txt"] = bytes(source)
    result = replace(inputs, artifacts=artifacts).run()
    assert result.preparation_disposition == "reject_input"
    assert result.errors


@given(st.permutations(tuple(range(4))))
@settings(max_examples=24, deadline=None)
def test_changed_canonical_array_order_stales_profile(order: list[int]) -> None:
    inputs = _inputs()
    case = _parsed(inputs.case)
    sources = sequence(case["sources"])
    case["sources"] = [sources[index] for index in order]
    result = replace(inputs, case=_json(case)).run()
    expected = "prepare_draft" if order == [0, 1, 2, 3] else "reject_input"
    assert result.preparation_disposition == expected


def _write_cli_inputs(inputs: Inputs, directory: Path) -> None:
    directory.mkdir()
    (directory / "case.json").write_bytes(inputs.case)
    (directory / "profile.json").write_bytes(inputs.profile)
    assets = directory / "artifacts"
    for relative, raw in inputs.artifacts.items():
        path = assets / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    for option, raw in [
        ("manifest", inputs.manifest),
        ("decision", inputs.decision),
        ("status", inputs.status),
    ]:
        if raw is not None:
            (directory / f"{option}.json").write_bytes(raw)


def _cli_arguments(directory: Path, output: Path) -> list[str]:
    arguments = [
        "--case",
        str(directory / "case.json"),
        "--profile",
        str(directory / "profile.json"),
        "--artifacts",
        str(directory / "artifacts"),
        "--template",
        "packet/template-v1.md",
        "--evaluated-at",
        EVALUATED_AT,
        "--output",
        str(output),
    ]
    for option in ["manifest", "decision", "status"]:
        path = directory / f"{option}.json"
        if path.exists():
            arguments.extend([f"--{option}", str(path)])
    return arguments


def _run_cli(directory: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tools.heaps", *_cli_arguments(directory, output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )


def _cli(inputs: Inputs, directory: Path, output: Path) -> subprocess.CompletedProcess[str]:
    _write_cli_inputs(inputs, directory)
    return _run_cli(directory, output)


def test_real_cli_two_clean_runs_match_all_output_bytes(tmp_path: Path) -> None:
    inputs = _inputs()
    outputs = [tmp_path / "first-output", tmp_path / "second-output"]
    for index, output in enumerate(outputs):
        result = _cli(inputs, tmp_path / f"input-{index}", output)
        assert result.returncode == 0, result.stderr + result.stdout
        observed = _parsed(result.stdout.encode())
        assert observed["preparation_disposition"] == "prepare_draft"
    snapshots = [
        {
            path.relative_to(output).as_posix(): path.read_bytes()
            for path in output.rglob("*")
            if path.is_file()
        }
        for output in outputs
    ]
    assert snapshots[0] == snapshots[1] == inputs.run().files


@pytest.mark.parametrize(
    ("variant_id", "exit_code"),
    [("HP04-wrong-kind", 2), ("HP20-empty", 3), ("HP20-all-abstain", 3)],
)
def test_real_cli_negative_and_abstention_exit_codes(
    tmp_path: Path, variant_id: str, exit_code: int
) -> None:
    output = tmp_path / "output"
    result = _cli(_inputs(variant_id), tmp_path / "input", output)
    assert result.returncode == exit_code, result.stderr + result.stdout
    observed = _parsed(result.stdout.encode())
    expected = mapping(BY_ID[variant_id]["expected"])
    assert observed["preparation_disposition"] == expected["preparation_disposition"]
    if exit_code == 2:
        assert not (output / "report.md").exists()


def test_real_cli_never_overwrites_existing_output(tmp_path: Path) -> None:
    output = tmp_path / "existing"
    output.mkdir()
    sentinel = output / "retain.txt"
    sentinel.write_bytes(b"existing generated synthetic work")
    result = _cli(_inputs(), tmp_path / "input", output)
    assert result.returncode == 2
    assert sentinel.read_bytes() == b"existing generated synthetic work"
    assert sorted(path.name for path in output.iterdir()) == ["retain.txt"]


def _symlink(link: Path, target: Path, *, directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=directory)
    except OSError:
        if os.name == "nt":
            pytest.skip("Windows execution environment does not permit symlink creation")
        raise


@pytest.mark.parametrize("target", ["case", "source"])
def test_real_cli_rejects_symlink_inputs(tmp_path: Path, target: str) -> None:
    directory = tmp_path / "input"
    _write_cli_inputs(_inputs(), directory)
    original = (
        directory / "case.json" if target == "case" else directory / "artifacts/sources/record.txt"
    )
    retained = directory / "retained-input"
    original.rename(retained)
    _symlink(original, retained)
    output = tmp_path / "output"
    result = _run_cli(directory, output)
    assert result.returncode == 2
    assert not (output / "report.md").exists()


def test_real_cli_rejects_output_through_symlink_parent(tmp_path: Path) -> None:
    directory = tmp_path / "input"
    _write_cli_inputs(_inputs(), directory)
    actual = tmp_path / "actual"
    actual.mkdir()
    link = tmp_path / "linked"
    _symlink(link, actual, directory=True)
    result = _run_cli(directory, link / "output")
    assert result.returncode == 2
    assert not list(actual.iterdir())


@pytest.mark.skipif(os.name == "nt", reason="Named pipes use a separate Windows API")
def test_real_cli_rejects_nonregular_source_without_waiting_for_a_writer(tmp_path: Path) -> None:
    directory = tmp_path / "input"
    _write_cli_inputs(_inputs(), directory)
    source = directory / "artifacts/sources/record.txt"
    source.unlink()
    os.mkfifo(source)
    result = _run_cli(directory, tmp_path / "output")
    assert result.returncode == 2


def test_cli_publish_failure_leaves_no_partial_packet_or_deleted_inputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = _inputs("HP07-report-after-approval")
    directory = tmp_path / "input"
    output = tmp_path / "output"
    _write_cli_inputs(inputs, directory)

    def fail_publication(_self: Path, _target: object) -> Path:
        raise OSError("Synthetic publication failure")

    monkeypatch.setattr(Path, "replace", fail_publication)
    monkeypatch.setattr(Path, "rename", fail_publication)
    assert heaps.main(_cli_arguments(directory, output)) == 2
    observed = _parsed(capsys.readouterr().out.encode())
    assert observed["preparation_disposition"] == "reject_input"
    assert observed["output_files"] == []
    assert not output.exists()
    assert sorted(path.name for path in tmp_path.iterdir()) == ["input"]
    assert (directory / "case.json").read_bytes() == inputs.case
    assert (directory / "profile.json").read_bytes() == inputs.profile


@pytest.mark.parametrize(
    "defect", ["missing_source", "oversized_source", "artifact_root_file", "missing_parent"]
)
def test_cli_filesystem_boundaries_return_structured_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    defect: str,
) -> None:
    directory = tmp_path / "input"
    output = tmp_path / "output"
    _write_cli_inputs(_inputs(), directory)
    arguments = _cli_arguments(directory, output)
    source = directory / "artifacts/sources/record.txt"
    if defect == "missing_source":
        source.unlink()
    elif defect == "oversized_source":
        source.write_bytes(b"x" * (4 * 1024 * 1024 + 1))
    elif defect == "artifact_root_file":
        arguments[arguments.index("--artifacts") + 1] = str(directory / "case.json")
    else:
        arguments[arguments.index("--output") + 1] = str(tmp_path / "absent" / "output")
    assert heaps.main(arguments) == 2
    observed = _parsed(capsys.readouterr().out.encode())
    assert observed["preparation_disposition"] == "reject_input"
    assert observed["errors"]
    assert observed["output_files"] == []
    assert not output.exists()
