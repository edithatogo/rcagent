"""Independent black-box H5 qualification of the synthetic HEAPS API and CLI.

Expected dispositions come from frozen H3 fixtures, never producer helpers.
Engineering checks do not establish clinical or organisational approval.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from dataclasses import dataclass, replace
from pathlib import Path
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools.heaps import PacketResult, assemble_packet

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "heaps"
EVALUATED_AT = "2030-01-07T02:00:00Z"
ORACLE = mapping(json.loads((FIXTURES / "oracle.json").read_bytes()))
VARIANTS = {
    text_value(row["id"]): row for row in (mapping(item) for item in sequence(ORACLE["variants"]))
}


def _encode(value: object, *, indent: int = 2) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=indent) + "\n").encode()


def _read(path: str) -> ObjectMap:
    return mapping(json.loads((FIXTURES / path).read_bytes()))


def _decode(payload: bytes) -> ObjectMap:
    return mapping(json.loads(payload))


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _reverse(value: object) -> object:
    if isinstance(value, dict):
        fields = cast("dict[str, object]", value)
        return {key: _reverse(item) for key, item in reversed(list(fields.items()))}
    if isinstance(value, list):
        return [_reverse(item) for item in cast("list[object]", value)]
    return value


def _change(documents: dict[str, ObjectMap], mutation: ObjectMap) -> None:
    path = sequence(mutation["path"])
    assert path
    parent: object = documents[text_value(mutation["document"])]
    for part in path[:-1]:
        if isinstance(part, str):
            parent = mapping(parent)[part]
        else:
            assert isinstance(part, int)
            assert not isinstance(part, bool)
            parent = sequence(parent)[part]
    last = path[-1]
    if isinstance(last, str):
        mapping(parent)[last] = deepcopy(mutation["value"])
    else:
        assert isinstance(last, int)
        assert not isinstance(last, bool)
        sequence(parent)[last] = deepcopy(mutation["value"])


@dataclass(frozen=True)
class Scenario:
    case: bytes
    profile: bytes
    assets: dict[str, bytes]
    manifest: bytes | None = None
    decision: bytes | None = None
    status: bytes | None = None

    def run(self) -> PacketResult:
        return assemble_packet(
            self.case,
            self.profile,
            self.assets,
            evaluated_at=EVALUATED_AT,
            template_path="packet/template-v1.md",
            manifest_bytes=self.manifest,
            decision_bytes=self.decision,
            status_bytes=self.status,
        )


def _scenario(variant_id: str = "HP01-valid") -> Scenario:
    variant = VARIANTS[variant_id]
    documents = {
        name: _read(text_value(path)) for name, path in mapping(variant["documents"]).items()
    }
    for mutation in sequence(variant["mutations"]):
        _change(documents, mapping(mutation))
    case = documents["case"]
    presentation = variant["case_presentation"]
    if presentation == "object_key_reorder":
        case_bytes = _encode(_reverse(case))
    else:
        case_bytes = _encode(case, indent=4 if presentation == "round_trip" else 2)
    profile_bytes = _encode(documents["profile"])
    assets = {
        path.relative_to(FIXTURES).as_posix(): path.read_bytes()
        for folder in ("canonical", "packet", "sources")
        for path in (FIXTURES / folder).rglob("*")
        if path.is_file()
    }
    paths = mapping(variant["documents"])
    assets[text_value(paths["case"])] = case_bytes
    assets[text_value(paths["profile"])] = profile_bytes
    for path, replacement in mapping(variant["raw_artifact_overrides"]).items():
        assets[path] = (FIXTURES / text_value(replacement)).read_bytes()
    roles = mapping(variant["document_roles"])

    def detached(name: str) -> bytes | None:
        if name in documents and roles[name] == "consumer_input":
            return _encode(documents[name])
        return None

    return Scenario(
        case_bytes,
        profile_bytes,
        assets,
        detached("manifest"),
        detached("decision"),
        detached("status"),
    )


def _rebind(case: ObjectMap, profile: ObjectMap) -> bytes:
    canonical = json.dumps(
        case,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    binding = mapping(profile["case_binding"])
    binding["case_id"] = case["case_id"]
    binding["version"] = case["version"]
    binding["fingerprint"] = "sha256:" + _digest(canonical)
    return _encode(profile)


def _rejected(result: PacketResult) -> None:
    assert result.preparation_disposition == "reject_input"
    assert result.errors
    assert result.files == {}
    assert result.status is None


@pytest.mark.parametrize("variant_id", sorted(VARIANTS))
def test_independent_frozen_oracle_public_api(variant_id: str) -> None:
    expected = mapping(VARIANTS[variant_id]["expected"])
    actual = _scenario(variant_id).run()
    assert actual.preparation_disposition == expected["preparation_disposition"]
    assert actual.review_disposition == expected["review_disposition"]
    if actual.preparation_disposition == "reject_input":
        _rejected(actual)
    else:
        assert not actual.errors
        status = mapping(actual.status)
        assert status["clinical_review"] == "not_established"
        assert status["actual_authority"] == "unverified"
        assert status["submission"] == "not_submitted"
        assert status["source_check_scope"] == "record_reference_integrity"


def test_independent_sha256_of_every_manifest_entry() -> None:
    original = _scenario()
    result = original.run()
    assert result.preparation_disposition == "prepare_draft"
    manifest = _decode(result.files["manifest.json"])
    groups = mapping(manifest["components"])
    entries = [mapping(groups[name]) for name in ("case", "profile", "mapping", "template")]
    for name in ("sources", "supporting_artifacts", "reports"):
        extra = [mapping(item) for item in sequence(groups[name])]
        paths = [text_value(item["path"]) for item in extra]
        assert paths == sorted(paths)
        entries.extend(extra)
    paths_seen: set[str] = set()
    ids_seen: set[str] = set()
    for entry in entries:
        path = text_value(entry["path"])
        identity = text_value(entry["artifact_id"])
        assert path not in paths_seen
        assert identity not in ids_seen
        paths_seen.add(path)
        ids_seen.add(identity)
        raw = result.files[path]
        assert entry["bytes"] == len(raw)
        assert entry["sha256"] == _digest(raw)
    assert result.files["ingress/case.json"] == original.case
    assert result.files["ingress/profile.json"] == original.profile
    assert not paths_seen.intersection(
        {"manifest.json", "decision.json", "status.json", "verification.json"}
    )
    receipt = _decode(result.files["verification.json"])
    assert receipt["generated_manifest_sha256"] == _digest(result.files["manifest.json"])
    assert receipt["status_sha256"] == _digest(result.files["status.json"])


@pytest.mark.parametrize("document", ["case", "profile"])
def test_object_key_order_preserves_normalised_but_changes_ingress(
    document: str,
) -> None:
    base = _scenario()
    initial = base.run()
    raw = base.case if document == "case" else base.profile
    changed = _encode(_reverse(_decode(raw)))
    assert changed != raw
    scenario = replace(base, case=changed) if document == "case" else replace(base, profile=changed)
    after = scenario.run()
    assert after.preparation_disposition == "prepare_draft", after.errors
    assert after.files[f"{document}.json"] == initial.files[f"{document}.json"]
    assert after.files[f"ingress/{document}.json"] != initial.files[f"ingress/{document}.json"]
    assert after.files["manifest.json"] != initial.files["manifest.json"]
    assert after.files["report.md"] == initial.files["report.md"]


@given(st.permutations(tuple(range(4))))
@settings(max_examples=24, deadline=None)
def test_property_source_array_order_changes_case_binding(order: list[int]) -> None:
    base = _scenario()
    case = _decode(base.case)
    sources = sequence(case["sources"])
    case["sources"] = [sources[index] for index in order]
    result = replace(base, case=_encode(case)).run()
    if order == [0, 1, 2, 3]:
        assert result.preparation_disposition == "prepare_draft"
    else:
        _rejected(result)


@given(st.integers(min_value=0, max_value=128), st.integers(min_value=1, max_value=255))
@settings(max_examples=12, deadline=None)
def test_property_source_byte_mutation_rejected(offset: int, mask: int) -> None:
    base = _scenario()
    assets = dict(base.assets)
    raw = bytearray(assets["sources/record.txt"])
    raw[offset] ^= mask
    assets["sources/record.txt"] = bytes(raw)
    _rejected(replace(base, assets=assets).run())


def test_duplicate_source_identity_and_nonsynthetic_profile_rejected() -> None:
    base = _scenario()
    profile = _decode(base.profile)
    sources = sequence(profile["source_snapshots"])
    mapping(sources[1])["source_id"] = mapping(sources[0])["source_id"]
    _rejected(replace(base, profile=_encode(profile)).run())
    profile = _decode(base.profile)
    profile["data_class"] = "clinical"
    _rejected(replace(base, profile=_encode(profile)).run())


def test_material_revision_stales_decision_without_approval() -> None:
    base = _scenario()
    initial = base.run()
    decision = _read("packet/simulated-approved-decision.json")
    bound = mapping(decision["manifest_binding"])
    bound["manifest_id"] = _decode(initial.files["manifest.json"])["manifest_id"]
    bound["raw_sha256"] = _digest(initial.files["manifest.json"])
    approved = replace(base, decision=_encode(decision)).run()
    assert approved.preparation_disposition == "prepare_draft", approved.errors
    assert mapping(approved.status)["review"] == "synthetic_draft_reviewed"
    assert mapping(approved.status)["clinical_review"] == "not_established"
    case = _decode(base.case)
    case["version"] = 2
    mapping(sequence(case["statements"])[0])["uncertainty"] = "Independent synthetic revision."
    changed = replace(
        base,
        case=_encode(case),
        profile=_rebind(case, _decode(base.profile)),
        decision=_encode(decision),
    ).run()
    assert changed.preparation_disposition == "prepare_draft", changed.errors
    assert changed.review_disposition == "stale"
    assert changed.files["decision.json"] == _encode(decision)
    assert changed.files["manifest.json"] != initial.files["manifest.json"]
    assert mapping(changed.status)["clinical_review"] == "not_established"


@pytest.mark.parametrize(
    "variant_id",
    [
        "HP05-unsupported-recommendation",
        "HP09-participation-missing",
        "HP09-participation-declined",
        "HP11-unavailable-local-template",
        "HP13-missing-trigger",
        "HP13-missing-calendar",
        "HP15-implemented-without-outcomes",
        "HP18-duplicate-source-family",
    ],
)
def test_gaps_never_become_substantive_approval(variant_id: str) -> None:
    result = _scenario(variant_id).run()
    assert result.preparation_disposition == "prepare_draft", result.errors
    status = mapping(result.status)
    assert status["clinical_review"] == "not_established"
    assert status["actual_authority"] == "unverified"
    assert status["submission"] == "not_submitted"
    assert status["source_check_scope"] == "record_reference_integrity"
    for name in ("report.md", "chronology.md", "actions.md"):
        assert result.files[name].startswith(b"#")


def test_positive_external_submission_claim_rejected() -> None:
    base = _scenario()
    claim = _decode(base.run().files["status.json"])
    claim["submission"] = "submitted"
    _rejected(replace(base, status=_encode(claim)).run())


def _write_inputs(scenario: Scenario, root: Path) -> list[str]:
    root.mkdir(parents=True)
    case = root / "case.json"
    profile = root / "profile.json"
    case.write_bytes(scenario.case)
    profile.write_bytes(scenario.profile)
    assets = root / "assets"
    for relative, raw in scenario.assets.items():
        path = assets / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    args = [
        "--case",
        str(case),
        "--profile",
        str(profile),
        "--artifacts",
        str(assets),
        "--template",
        "packet/template-v1.md",
        "--evaluated-at",
        EVALUATED_AT,
    ]
    for name in ("manifest", "decision", "status"):
        raw = getattr(scenario, name)
        if raw is not None:
            path = root / f"{name}.json"
            path.write_bytes(raw)
            args.extend([f"--{name}", str(path)])
    return args


def _cli(args: list[str], output: Path) -> subprocess.CompletedProcess[str]:
    # B603/B607: fixed Python executable/module and explicit argv; no shell.
    return subprocess.run(
        [sys.executable, "-m", "tools.heaps", *args, "--output", str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=35,
    )


def test_independent_subprocess_replay_matches_public_api(tmp_path: Path) -> None:
    scenario = _scenario()
    expected = scenario.run()
    snapshots: list[dict[str, bytes]] = []
    for number in range(2):
        args = _write_inputs(scenario, tmp_path / f"inputs-{number}")
        output = tmp_path / f"packet-{number}"
        process = _cli(args, output)
        assert process.returncode == 0, process.stdout + process.stderr
        assert mapping(json.loads(process.stdout))["preparation_disposition"] == "prepare_draft"
        snapshot = {
            path.relative_to(output).as_posix(): path.read_bytes()
            for path in output.rglob("*")
            if path.is_file()
        }
        assert snapshot == expected.files
        snapshots.append(snapshot)
    assert snapshots[0] == snapshots[1]


@pytest.mark.parametrize(
    ("variant_id", "exit_code"),
    [
        ("HP04-wrong-kind", 2),
        ("HP20-empty", 3),
        ("HP20-all-abstain", 3),
    ],
)
def test_independent_subprocess_reject_and_abstain(
    variant_id: str, exit_code: int, tmp_path: Path
) -> None:
    scenario = _scenario(variant_id)
    args = _write_inputs(scenario, tmp_path / "inputs")
    output = tmp_path / "packet"
    process = _cli(args, output)
    assert process.returncode == exit_code, process.stdout + process.stderr
    console = mapping(json.loads(process.stdout))
    assert (
        console["preparation_disposition"]
        == mapping(VARIANTS[variant_id]["expected"])["preparation_disposition"]
    )
    if exit_code == 2:
        assert not output.exists()
    else:
        assert (output / "status.json").is_file()
        receipt = _decode((output / "status.json").read_bytes())
        assert receipt["review"] == "not_requested"
        assert receipt["preparation"] == (
            "empty" if variant_id == "HP20-empty" else "all_abstain"
        )
        assert console["review_disposition"] == "withheld"


DETACHED_CHANNELS = {
    "manifest.json",
    "decision.json",
    "status.json",
    "verification.json",
    "verification-input-manifest.json",
    "verification-input-status.json",
}


@pytest.mark.parametrize(
    "variant_id",
    [
        name
        for name, variant in sorted(VARIANTS.items())
        if mapping(variant["expected"])["preparation_disposition"] != "reject_input"
    ],
)
def test_manifest_inventory_complete_for_each_admitted_variant(variant_id: str) -> None:
    """Check the required set, not only hashes the producer elected to inventory."""
    scenario = _scenario(variant_id)
    result = scenario.run()
    assert result.preparation_disposition != "reject_input", result.errors
    manifest = _decode(result.files["manifest.json"])
    groups = mapping(manifest["components"])
    listed = {
        text_value(mapping(groups[name])["path"])
        for name in ("case", "profile", "mapping", "template")
    }
    for name in ("sources", "supporting_artifacts", "reports"):
        listed.update(text_value(mapping(row)["path"]) for row in sequence(groups[name]))
    assert listed == set(result.files) - DETACHED_CHANNELS
    assert {
        "case.json", "profile.json", "mapping.json", "template.md",
        "ingress/case.json", "ingress/profile.json",
        "report.md", "chronology.md", "actions.md",
    } <= listed

    case = _decode(scenario.case)
    profile = _decode(scenario.profile)
    sources = {
        text_value(mapping(row)["source_id"]): mapping(row)
        for row in sequence(case.get("sources", []))
    }
    expected_sources: set[str] = set()
    for snapshot in sequence(profile["source_snapshots"]):
        row = mapping(snapshot)
        if row["state"] != "available":
            continue
        source = sources[text_value(row["source_id"])]
        citation = source.get("citation")
        if isinstance(citation, str):
            expected_sources.add(citation)
        else:
            expected_sources.add(text_value(row["locator"]).removeprefix("synthetic:"))
    declared_sources = {
        text_value(mapping(row)["path"]) for row in sequence(groups["sources"])
    }
    assert declared_sources == expected_sources
    for path in expected_sources:
        assert result.files[path] == scenario.assets[path]

    for component in sequence(profile["optional_components"]):
        path = text_value(mapping(mapping(component)["artifact"])["path"])
        assert path in listed
        assert result.files[path] == scenario.assets[path]

    if scenario.manifest is not None:
        assert result.files["verification-input-manifest.json"] == scenario.manifest
        earlier = mapping(_decode(scenario.manifest)["components"])
        old_entries = [
            mapping(earlier[name]) for name in ("case", "profile", "mapping", "template")
        ]
        for name in ("sources", "supporting_artifacts", "reports"):
            old_entries.extend(mapping(row) for row in sequence(earlier[name]))
        for entry in old_entries:
            path = text_value(entry["path"])
            raw = scenario.assets[path]
            assert any(
                result.files.get(candidate) == raw
                for candidate in (path, "history/" + path)
            )


@pytest.mark.parametrize("variant_id", sorted(VARIANTS))
def test_frozen_case_specific_semantics_and_retained_ids(variant_id: str) -> None:
    """Retain case-level meaning as well as the frozen disposition."""
    scenario = _scenario(variant_id)
    expected = mapping(VARIANTS[variant_id]["expected"])
    required = mapping(expected["required_states"])
    result = scenario.run()
    retained = [text_value(value) for value in sequence(expected["retained_ids"])]
    if result.preparation_disposition == "reject_input":
        _rejected(result)
        raw_inputs = scenario.case + scenario.profile
        for identity in retained:
            assert identity.encode() in raw_inputs
        return

    status = mapping(result.status)
    case = _decode(result.files["case.json"])
    profile = _decode(result.files["profile.json"])
    report = result.files["report.md"].decode("utf-8")
    actions = result.files["actions.md"].decode("utf-8")
    combined = report + result.files["chronology.md"].decode("utf-8") + actions
    for identity in retained:
        assert identity in combined

    canonical_statements = [mapping(row) for row in sequence(case.get("statements", []))]
    usable = sum(
        row.get("withdrawn") is not True
        and mapping(row["provenance"])["review_state"] not in ("withdrawn", "rejected")
        for row in canonical_statements
    )
    assert status["counts"] == {
        "input_items": len(canonical_statements),
        "usable_items": usable,
        "abstained_items": len(canonical_statements) - usable,
    }
    assert "Accepted recommendations: 0" in report
    assert status["clinical_review"] == "not_established"
    assert status["actual_authority"] == "unverified"
    assert status["submission"] == "not_submitted"

    if variant_id == "HP05-unsupported-recommendation":
        assert required["recommendation_support"] == "incomplete"
        assert required["accepted_recommendations"] == 0
        assert "Recommendation support incomplete for: syn-stmt-recommendation" in report
    elif variant_id == "HP08-conflicting-accounts":
        assert required["account_conflict"] == "unresolved"
        assert required["alternatives"] == "retained"
        for identity in (
            "syn-stmt-staff", "syn-stmt-consumer",
            "syn-stmt-document-gap", "syn-stmt-recall",
        ):
            assert identity in report
        assert "Reported accounts" in report
        assert "Hypotheses and alternatives" in report
        assert "contrary evidence and alternatives" in report
    elif variant_id.startswith("HP09-"):
        expected_state = text_value(required["consumer_participation"])
        participation = [
            mapping(row) for row in sequence(profile["participation"])
            if mapping(mapping(row)["role_ref"])["id"] == "syn-role-consumer"
        ]
        assert len(participation) == 1
        assert participation[0]["state"] == expected_state
        assert f'"state": "{expected_state}"' in report
        assert required["consultation_completed"] is False
        assert required["agreement_established"] is False
        assert "do not establish consultation completion or agreement" in report
    elif variant_id == "HP10-no-statutory-authority":
        assert mapping(profile["applicability"])["protection_status"] == required["protection"]
        assert "No" in report and "clinical" in report
    elif variant_id == "HP11-unavailable-local-template":
        assert required["local_template_conformity"] == "not_established"
        assert required["draft_preparation"] == "available"
        assert "Current local HEAPS instrument conformity is not established" in report
        assert status["preparation"] == "prepared"
    elif variant_id.startswith("HP13-"):
        deadline = mapping(sequence(profile["deadlines"])[0])
        assert required["deadline"] == "unresolved"
        assert required["due_timestamp"] is None
        assert mapping(deadline["due"])["value"] is None
        assert "Unverified deadlines and unresolved bases" in report
    elif variant_id == "HP14-method-change":
        assert required["awareness"] in report
        assert required["due_timestamp"] in report
        assert required["prior_process"] in report
        assert required["selected_process"] in report
        assert required["clock_reset"] is False
        clocks = mapping(profile["clocks"])
        assert mapping(clocks["sac1_reporting"])["value"] is None
        assert mapping(clocks["review_submission"])["value"] is None
    elif variant_id == "HP15-implemented-without-outcomes":
        action = mapping(sequence(case["actions"])[0])
        outcome = mapping(sequence(case["outcomes"])[0])
        assert action["status"] == required["implementation"]
        assert action["effectiveness_state"] == required["effectiveness"]
        assert outcome["status"] == required["outcome_status"]
        assert "Recorded implementation is distinct from effectiveness" in actions
        for value in (required["implementation"], required["effectiveness"]):
            assert text_value(value) in actions
    elif variant_id == "HP16-no-submission-receipt":
        assert required["submission"] == "not_submitted"
        assert required["system_of_record_receipt"] is None
        assert required["case_closed"] is False
        assert status["submission"] == "not_submitted"
    elif variant_id == "HP18-duplicate-source-family":
        snapshots = [
            mapping(row) for row in sequence(profile["source_snapshots"])
            if "incident_evidence" in sequence(mapping(row)["purposes"])
        ]
        assert len(snapshots) == required["incident_source_count"]
        family_count = len({text_value(row["source_family_id"]) for row in snapshots})
        assert family_count == required["incident_source_family_count"]
        assert (
            f"Incident source count: {len(snapshots)}; "
            f"incident source-family count: {family_count}"
        ) in report
        assert "Independent corroboration is not established" in report
    elif variant_id == "HP19-missing-documentation":
        assert required["care_omission_finding"] == "not_established"
        assert "Missing documentation does not establish omitted care" in report
    elif variant_id.startswith("HP20-"):
        assert status["preparation"] == required["preparation"]
        assert status["counts"] == mapping(required["counts"])
        assert status["review"] == "not_requested"
        assert required["completed_review"] is False
    elif variant_id.startswith("HP21-"):
        original = _scenario("HP01-valid").run()
        assert result.files["case.json"] == original.files["case.json"]
        assert result.files["profile.json"] == original.files["profile.json"]
        assert result.files["report.md"] == original.files["report.md"]
        if variant_id in ("HP21-round-trip", "HP21-object-key-reorder"):
            assert result.files["ingress/case.json"] != original.files["ingress/case.json"]
            assert result.files["manifest.json"] != original.files["manifest.json"]
    elif variant_id.startswith("HP22-"):
        assert required["graph_qualification"] == "not_established"
        assert required["core_draft"] == "available"
        assert "No qualified graph or source-span view is emitted" in report
        assert "accimap.md" not in result.files
    elif variant_id == "HP23-concurrent-routes":
        assert required["route_resolution"] == "not_established"
        for route in sequence(required["open_routes"]):
            assert text_value(route) in report


@pytest.mark.parametrize(
    ("variant_id", "exit_code"),
    [
        ("HP07-report-after-approval", 0),
        ("HP12-template-revision", 2),
        ("HP12-source-revision", 2),
        ("HP16-no-submission-receipt", 0),
    ],
)
def test_cli_detached_manifest_decision_revision_matches_api(
    tmp_path: Path, variant_id: str, exit_code: int
) -> None:
    scenario = _scenario(variant_id)
    assert scenario.manifest is not None
    expected = scenario.run()
    args = _write_inputs(scenario, tmp_path / "inputs")
    output = tmp_path / "packet"
    process = _cli(args, output)
    assert process.returncode == exit_code, process.stdout + process.stderr
    console = mapping(json.loads(process.stdout))
    assert console["preparation_disposition"] == expected.preparation_disposition
    assert console["review_disposition"] == expected.review_disposition
    if exit_code == 2:
        assert not output.exists()
        _rejected(expected)
    else:
        files = {
            path.relative_to(output).as_posix(): path.read_bytes()
            for path in output.rglob("*")
            if path.is_file()
        }
        assert files == expected.files
        assert files["verification-input-manifest.json"] == scenario.manifest
        if scenario.decision is not None:
            assert files["decision.json"] == scenario.decision


def test_cli_rejects_forged_detached_submission_status(tmp_path: Path) -> None:
    baseline = _scenario()
    forged = _decode(baseline.run().files["status.json"])
    forged["submission"] = "submitted"
    scenario = replace(baseline, status=_encode(forged))
    _rejected(scenario.run())
    args = _write_inputs(scenario, tmp_path / "inputs")
    output = tmp_path / "packet"
    process = _cli(args, output)
    assert process.returncode == 2, process.stdout + process.stderr
    console = mapping(json.loads(process.stdout))
    assert console["preparation_disposition"] == "reject_input"
    assert console["review_disposition"] == "not_established"
    assert not output.exists()
