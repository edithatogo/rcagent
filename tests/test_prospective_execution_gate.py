"""Synthetic gate evidence is not an actual panel review or execution permit."""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, cast

import pytest

from tests.test_prospective_freeze import git as real_git
from tests.test_prospective_native_protocol import fixture as native_fixture
from tests.test_prospective_protocol import pin
from tools import prospective_execution_gate as gate
from tools import prospective_freeze

S, R = "a" * 40, "b" * 40
REAL_GIT = prospective_freeze._git
REAL_FILES = prospective_freeze._committed_files


@pytest.fixture
def synthetic(tmp_path, monkeypatch):
    monkeypatch.setattr(gate.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(gate.platform, "machine", lambda: "arm64")
    root = tmp_path.resolve()
    path, value = native_fixture(root)
    for relative in (*gate.SOURCES, gate.REGISTRY):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"# synthetic bytes, not executed\n")
    value["condition"]["adapter_sha256"] = pin(root / gate.ADAPTER)
    value["condition"]["registry_sha256"] = pin(root / gate.REGISTRY)
    path.write_text(json.dumps(value), encoding="utf-8")
    refs = [case["input"] for case in value["cases"]]
    refs.extend(value[key] for key in ("rubric", "scoring_instructions", "prompt_template"))
    paths = [path.name, *(ref["path"] for ref in refs), *gate.SOURCES, gate.REGISTRY]
    files = [{"path": name, "sha256": pin(root / name)} for name in paths]
    environment = {"synthetic": True}
    record = {
        "version": "primary-review-v1",
        "source_commit": S,
        "protocol_sha256": pin(path),
        "adapter_sha256": pin(root / gate.ADAPTER),
        "closure_sha256": gate.identity.digest(files),
        "environment_sha256": gate.identity.digest(environment),
        "unresolved_findings": [],
        "reviewers": [],
    }
    blobs = {}
    for role in ("acceptance", "evidence-integrity", "safety-privacy"):
        evidence_path = f"conductor/reviews/evidence/{role}.json"
        envelope = {
            key: record[key]
            for key in ("source_commit", "protocol_sha256", "closure_sha256", "environment_sha256")
        }
        envelope.update(
            role=role,
            reviewer_id="synthetic-" + role,
            outcome="pass",
            evidence_locator="synthetic-fixture-not-actual-panel",
            unresolved_findings=[],
        )
        raw = json.dumps(envelope).encode()
        blobs[evidence_path] = raw
        record["reviewers"].append(
            {
                "role": role,
                "reviewer_id": "synthetic-" + role,
                "outcome": "pass",
                "evidence_path": evidence_path,
                "evidence_sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    calls = []

    def git(root_arg, *args):
        calls.append(args)
        if args == ("rev-parse", "--show-toplevel"):
            return str(root).encode()
        if args[:2] == ("rev-parse", "--verify"):
            return R.encode()
        if args[0] == "merge-base":
            if args[2:] != (S, R):
                raise ValueError("git_lookup_failed")
            return b""
        if args[0] == "ls-tree":
            return b"100644 blob " + b"c" * 40 + b"\t" + args[-1].encode() + b"\0"
        if args[:2] == ("cat-file", "blob"):
            selected = calls[-2][-1]
            return json.dumps(record).encode() if selected == gate.REVIEW_PATH else blobs[selected]
        raise AssertionError(args)

    monkeypatch.setattr(gate.freeze, "_git", git)
    monkeypatch.setattr(gate.freeze, "_committed_files", lambda *args: copy.deepcopy(files))
    monkeypatch.setattr(gate.identity, "project_closure", lambda *args: None)
    monkeypatch.setattr(gate.identity, "environment_identity", lambda: copy.deepcopy(environment))
    _, candidate = gate.native._validated_candidate(path, pin(path))
    admission = {"admission_sha256": "d" * 64, "model_id": value["condition"]["model_id"]}
    monkeypatch.setattr(
        gate.binding,
        "bind_slot",
        lambda protocol, pin, slot, model_root: {
            "request": copy.deepcopy(candidate["requests"][slot]),
            "eligibility": {"admission_sha256": admission["admission_sha256"]},
        },
    )
    monkeypatch.setattr(gate.model, "admit_model", lambda root: copy.deepcopy(admission))
    return root, path, value, record, blobs, files, environment, admission


def verify(data, **kwargs):
    root, path, value, *_ = data
    return gate._verify(
        kwargs.get("path", path),
        kwargs.get("pin", pin(path)),
        kwargs.get("slot", value["expected_slots"][0]),
        kwargs.get("review", R),
        root,
        root / "synthetic-cache",
    )


def test_fixed_review_path():
    assert gate.REVIEW_PATH == "conductor/reviews/primary-execution.json"


def test_actual_repository_static_sources_are_complete_and_correctly_imported():
    root = Path(gate.__file__).resolve().parents[1]
    hashes = {source: pin(root / source) for source in gate.SOURCES}
    gate.identity.project_closure(root, gate.SOURCES, hashes)


@pytest.mark.parametrize("damage", ["same-commit", "duplicate-reviewer", "invalid-digest"])
def test_resealed_review_still_cannot_bypass_semantic_guards(synthetic, damage):
    record, blobs = synthetic[3:5]
    if damage == "same-commit":
        record["source_commit"] = R
    elif damage == "duplicate-reviewer":
        record["reviewers"][1]["reviewer_id"] = record["reviewers"][0]["reviewer_id"]
    else:
        record["closure_sha256"] = "bad"
    for reviewer in record["reviewers"]:
        envelope = json.loads(blobs[reviewer["evidence_path"]])
        envelope["source_commit"] = record["source_commit"]
        envelope["reviewer_id"] = reviewer["reviewer_id"]
        raw = json.dumps(envelope).encode()
        blobs[reviewer["evidence_path"]] = raw
        reviewer["evidence_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError):
        verify(synthetic)


def test_review_blob_rejects_traversal_and_empty_content(synthetic, monkeypatch):
    with pytest.raises(ValueError, match="invalid_review_path"):
        gate._blob(synthetic[0], R, "conductor/../private.json")
    git = gate.freeze._git
    monkeypatch.setattr(
        gate.freeze, "_git", lambda root, *args: b"" if args[0] == "cat-file" else git(root, *args)
    )
    with pytest.raises(ValueError, match="empty_review_evidence"):
        gate._blob(synthetic[0], R, gate.REVIEW_PATH)


def test_reviewed_fixture_plan_is_immutable_not_admission(synthetic):
    plan = verify(synthetic)
    result = plan.value()
    assert result["evidence"]["execution_permitted"] is True
    assert result["evidence"]["admitted"] is result["evidence"]["study_unlocked"] is False
    result["admission"].clear()
    assert plan.value()["admission"]
    with pytest.raises(AttributeError):
        cast(Any, plan).payload = b"altered"


@pytest.mark.parametrize(
    "damage",
    [
        "extra",
        "version",
        "findings",
        "source",
        "same-commit",
        "protocol",
        "adapter",
        "closure",
        "environment",
        "missing-role",
        "duplicate-id",
        "outcome",
        "path",
        "evidence-hash",
        "evidence-scope",
        "locator",
    ],
)
def test_review_failures_never_reach_eligibility(synthetic, monkeypatch, damage):
    record, blobs = synthetic[3:5]
    if damage == "extra":
        record["extra"] = True
    elif damage == "version":
        record["version"] = "other"
    elif damage == "findings":
        record["unresolved_findings"] = ["hard finding"]
    elif damage == "source":
        record["source_commit"] = "invalid"
    elif damage == "same-commit":
        record["source_commit"] = R
    elif damage in {"protocol", "adapter", "closure", "environment"}:
        record[damage + "_sha256"] = "0" * 64
    elif damage == "missing-role":
        record["reviewers"].pop()
    elif damage == "duplicate-id":
        record["reviewers"][1]["reviewer_id"] = record["reviewers"][0]["reviewer_id"]
    elif damage == "outcome":
        record["reviewers"][0]["outcome"] = "fail"
    elif damage == "path":
        record["reviewers"][0]["evidence_path"] = "../private"
    elif damage == "evidence-hash":
        record["reviewers"][0]["evidence_sha256"] = "0" * 64
    else:
        reviewer = record["reviewers"][0]
        envelope = json.loads(blobs[reviewer["evidence_path"]])
        envelope["source_commit" if damage == "evidence-scope" else "evidence_locator"] = ""
        raw = json.dumps(envelope).encode()
        blobs[reviewer["evidence_path"]] = raw
        reviewer["evidence_sha256"] = hashlib.sha256(raw).hexdigest()

    def forbidden(*args):
        raise AssertionError("Model eligibility must not be reached")

    monkeypatch.setattr(gate.model, "admit_model", forbidden)
    with pytest.raises(ValueError):
        verify(synthetic)


@pytest.mark.parametrize(
    "damage",
    ["slot", "path", "commit-type", "source-parity", "environment", "admission", "request"],
)
def test_gate_identity_and_confinement_failures(synthetic, monkeypatch, damage):
    kwargs = {}
    if damage == "slot":
        kwargs["slot"] = "unknown"
    elif damage == "path":
        kwargs["path"] = synthetic[0] / ".." / "outside.json"
    elif damage == "commit-type":
        kwargs["review"] = None
    elif damage == "source-parity":
        monkeypatch.setattr(
            gate.freeze,
            "_committed_files",
            lambda root, commit, *args: synthetic[5] if commit == S else [],
        )
    elif damage == "environment":
        synthetic[6]["changed"] = True
    elif damage == "admission":
        monkeypatch.setattr(gate.model, "admit_model", lambda root: {"admission_sha256": "x"})
    else:
        monkeypatch.setattr(
            gate.binding,
            "bind_slot",
            lambda *args: {"request": {}, "eligibility": {"admission_sha256": "d" * 64}},
        )
    with pytest.raises(ValueError):
        verify(synthetic, **kwargs)


@pytest.mark.parametrize(
    "entry", [b"", b"120000 blob " + b"a" * 40 + b"\t" + gate.REVIEW_PATH.encode() + b"\0"]
)
def test_review_record_must_be_regular_blob(synthetic, monkeypatch, entry):
    monkeypatch.setattr(gate.freeze, "_git", lambda *args: entry)
    with pytest.raises(ValueError, match="review_not_regular_blob"):
        gate._blob(synthetic[0], R, gate.REVIEW_PATH)


def test_review_envelopes_bind_environment_not_only_outer_record(synthetic):
    synthetic[6]["changed"] = True
    synthetic[3]["environment_sha256"] = gate.identity.digest(synthetic[6])
    with pytest.raises(ValueError, match="review_evidence_scope_mismatch"):
        verify(synthetic)


def test_unsupported_platform_rejected_before_repository(synthetic, monkeypatch):
    monkeypatch.setattr(gate.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        gate.freeze, "_repository", lambda *args: pytest.fail("No repository lookup")
    )
    with pytest.raises(ValueError, match="unsupported_primary_platform"):
        verify(synthetic)


def test_wrong_loaded_checkout_rejected_before_eligibility(synthetic, monkeypatch):
    def origin_failure(*args):
        raise ValueError("project_import_origin_mismatch")

    monkeypatch.setattr(gate.identity, "project_closure", origin_failure)
    monkeypatch.setattr(
        gate.model, "admit_model", lambda root: pytest.fail("No eligibility after origin mismatch")
    )
    with pytest.raises(ValueError, match="project_import_origin_mismatch"):
        verify(synthetic)


def commit_review(synthetic, damage="none"):
    root, path, value, record, blobs, *_ = synthetic
    real_git(root, "init", "-q")
    for key, val in (
        ("user.name", "Synthetic Fixture"),
        ("user.email", "synthetic@example.invalid"),
        ("core.autocrlf", "false"),
        ("core.safecrlf", "false"),
    ):
        real_git(root, "config", key, val)
    real_git(root, "add", ".")
    real_git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic source only")
    source = real_git(root, "rev-parse", "HEAD")
    record["source_commit"] = source
    for reviewer in record["reviewers"]:
        evidence_path = reviewer["evidence_path"]
        envelope = json.loads(blobs[evidence_path])
        envelope["source_commit"] = source
        raw = json.dumps(envelope).encode()
        reviewer["evidence_sha256"] = hashlib.sha256(raw).hexdigest()
        target = root / evidence_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    reviewpath = root / gate.REVIEW_PATH
    reviewpath.write_text(json.dumps(record), encoding="utf-8")
    if damage == "source-parity":
        (root / gate.SOURCES[0]).write_bytes(b"# changed after review source\n")
    if damage == "nonancestor":
        real_git(root, "checkout", "--orphan", "synthetic-unrelated")
    real_git(root, "add", ".")
    real_git(
        root,
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "Synthetic review fixture, not actual review",
    )
    review = real_git(root, "rev-parse", "HEAD")
    return source, review


@pytest.mark.parametrize("damage", ["none", "source-parity", "nonancestor"])
def test_real_git_source_review_and_evidence_integration(synthetic, monkeypatch, damage):
    source, review = commit_review(synthetic, damage)
    monkeypatch.setattr(gate.freeze, "_git", REAL_GIT)
    monkeypatch.setattr(gate.freeze, "_committed_files", REAL_FILES)
    if damage != "none":
        with pytest.raises(ValueError):
            verify(synthetic, review=review)
    else:
        result = verify(synthetic, review=review).value()
        assert result["evidence"]["source_commit"] == source
        assert result["evidence"]["review_commit"] == review
        assert result["evidence"]["admitted"] is False
