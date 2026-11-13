"""Synthetic gate evidence is not an actual panel review or execution permit."""

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import TypedDict, Unpack

import pytest

from tests.prospective_fixture_types import GateFixture, ObjectMap, mapping, sequence, text_value
from tests.test_prospective_freeze import git as real_git
from tests.test_prospective_native_protocol import fixture as native_fixture
from tests.test_prospective_protocol import pin
from tools import prospective_execution_gate as gate
from tools import prospective_freeze

S, R = "a" * 40, "b" * 40
REAL_GIT = prospective_freeze._git
REAL_FILES = prospective_freeze._committed_files


class VerifyOptions(TypedDict, total=False):
    path: Path
    pin: str
    slot: object
    review: object


@pytest.fixture
def synthetic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> GateFixture:
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
    files: list[ObjectMap] = [{"path": name, "sha256": pin(root / name)} for name in paths]
    environment: ObjectMap = {"synthetic": True}
    reviewers: list[ObjectMap] = []
    record: ObjectMap = {
        "version": "primary-review-v1",
        "source_commit": S,
        "protocol_sha256": pin(path),
        "adapter_sha256": pin(root / gate.ADAPTER),
        "closure_sha256": gate.identity.digest(files),
        "environment_sha256": gate.identity.digest(environment),
        "unresolved_findings": [],
        "reviewers": reviewers,
    }
    blobs: dict[str, bytes] = {}
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
        reviewers.append(
            {
                "role": role,
                "reviewer_id": "synthetic-" + role,
                "outcome": "pass",
                "evidence_path": evidence_path,
                "evidence_sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    calls: list[tuple[str, ...]] = []

    def git(_root_arg: Path, *args: str) -> bytes:
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

    def committed_files(*args: object) -> list[ObjectMap]:
        return copy.deepcopy(files)

    def project_closure(*args: object) -> None:
        return None

    monkeypatch.setattr(gate.freeze, "_git", git)
    monkeypatch.setattr(gate.freeze, "_committed_files", committed_files)
    monkeypatch.setattr(gate.identity, "project_closure", project_closure)
    monkeypatch.setattr(gate.identity, "environment_identity", lambda: copy.deepcopy(environment))
    _, candidate = gate.native._validated_candidate(path, pin(path))
    condition = value["condition"]
    admission: gate.model.ModelAdmission = {
        "purpose": "local-artefact-eligibility-only",
        "local_artifact_eligible": True,
        "admitted": False,
        "study_unlocked": False,
        "registry_sha256": condition["registry_sha256"],
        "effective_manifest_sha256": "f" * 64,
        "original_runtime": {"name": "synthetic-historical-cli", "version": "unchanged"},
        "runtime_overlay": {
            "name": "synthetic-server",
            "version": "synthetic",
            "executable": "/synthetic/server",
            "executable_sha256": condition["runtime_sha256"],
            "license": "MIT",
            "profile_id": "synthetic-profile",
            "profile_sha256": condition["profile_sha256"],
            "distribution": "synthetic",
            "runtime_dependencies": [],
        },
        "profile_id": "synthetic-profile",
        "profile_sha256": condition["profile_sha256"],
        "model_id": condition["model_id"],
        "model_revision": condition["model_revision"],
        "model_sha256": condition["model_sha256"],
        "model_license_sha256": "a" * 64,
        "model_path": str(root / "synthetic-cache/model.gguf"),
        "model_license_path": str(root / "synthetic-cache/LICENSE"),
        "limitations": ["synthetic-fixture-not-actual-eligibility"],
        "admission_sha256": "d" * 64,
    }

    def bind_slot(protocol: Path, pin: str, slot: str, model_root: Path) -> ObjectMap:
        return {
            "request": copy.deepcopy(candidate["requests"][slot]),
            "eligibility": {"admission_sha256": admission["admission_sha256"]},
        }

    def admit_model(root: Path) -> gate.model.ModelAdmission:
        return copy.deepcopy(admission)

    monkeypatch.setattr(gate.binding, "bind_slot", bind_slot)
    monkeypatch.setattr(gate.model, "admit_model", admit_model)
    return root, path, mapping(value), record, blobs, files, environment, mapping(admission)


def verify(data: GateFixture, **kwargs: Unpack[VerifyOptions]):
    root, path, value, *_ = data
    return gate._verify(
        kwargs.get("path", path),
        kwargs.get("pin", pin(path)),
        kwargs.get("slot", text_value(sequence(value["expected_slots"])[0])),
        kwargs.get("review", R),
        root,
        root / "synthetic-cache",
    )


def test_fixed_review_path() -> None:
    assert gate.REVIEW_PATH == "conductor/reviews/primary-execution.json"


def test_actual_repository_static_sources_are_complete_and_correctly_imported() -> None:
    root = Path(gate.__file__).resolve().parents[1]
    hashes = {source: pin(root / source) for source in gate.SOURCES}
    gate.identity.project_closure(root, gate.SOURCES, hashes)


@pytest.mark.parametrize("damage", ["same-commit", "duplicate-reviewer", "invalid-digest"])
def test_resealed_review_still_cannot_bypass_semantic_guards(
    synthetic: GateFixture, damage: str
) -> None:
    record, blobs = synthetic[3:5]
    if damage == "same-commit":
        record["source_commit"] = R
    elif damage == "duplicate-reviewer":
        mapping(sequence(record["reviewers"])[1])["reviewer_id"] = mapping(
            sequence(record["reviewers"])[0]
        )["reviewer_id"]
    else:
        record["closure_sha256"] = "bad"
    for item in sequence(record["reviewers"]):
        reviewer = mapping(item)
        envelope = mapping(json.loads(blobs[text_value(reviewer["evidence_path"])]))
        envelope["source_commit"] = record["source_commit"]
        envelope["reviewer_id"] = reviewer["reviewer_id"]
        raw = json.dumps(envelope).encode()
        blobs[text_value(reviewer["evidence_path"])] = raw
        reviewer["evidence_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(ValueError):
        verify(synthetic)


def test_review_blob_rejects_traversal_and_empty_content(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(ValueError, match="invalid_review_path"):
        gate._blob(synthetic[0], R, "conductor/../private.json")
    git = gate.freeze._git

    def empty_blob(root: Path, *args: str) -> bytes:
        return b"" if args[0] == "cat-file" else git(root, *args)

    monkeypatch.setattr(gate.freeze, "_git", empty_blob)
    with pytest.raises(ValueError, match="empty_review_evidence"):
        gate._blob(synthetic[0], R, gate.REVIEW_PATH)


def test_reviewed_fixture_plan_is_immutable_not_admission(synthetic: GateFixture) -> None:
    plan = verify(synthetic)
    result = plan.value()
    assert result["evidence"]["execution_permitted"] is True
    assert result["evidence"]["admitted"] is result["evidence"]["study_unlocked"] is False
    mapping(result["admission"]).clear()
    assert plan.value()["admission"]
    with pytest.raises(AttributeError):
        plan.__setattr__("payload", b"altered")


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        (("request", "request", "bytes"), True),
        (("request", "generation", "seed"), "7"),
        (("request", "limits", "context_tokens_validated"), 0),
        (("request", "execution_observed"), True),
        (("admission", "model_id"), 3),
        (("admission", "original_runtime"), []),
        (("admission", "runtime_overlay", "runtime_dependencies"), ["synthetic", 3]),
        (("admission", "admitted"), 0),
        (("evidence", "execution_permitted"), 1),
        (("evidence", "limitations"), [None]),
    ],
)
def test_plan_reconstruction_rejects_invalid_nested_shapes(
    synthetic: GateFixture, field: tuple[str, ...], replacement: object
) -> None:
    plan = verify(synthetic)
    value = mapping(plan.value())
    target = value
    for key in field[:-1]:
        target = mapping(target[key])
    target[field[-1]] = replacement
    altered = replace(plan, payload=json.dumps(value).encode())
    with pytest.raises(ValueError, match="invalid_execution_plan"):
        altered.value()


def test_checked_plan_rejects_incomplete_payload(synthetic: GateFixture) -> None:
    altered = replace(verify(synthetic), payload=b"{}")
    with pytest.raises(ValueError, match="invalid_execution_plan"):
        altered.value()


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
def test_review_failures_never_reach_eligibility(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
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
        sequence(record["reviewers"]).pop()
    elif damage == "duplicate-id":
        mapping(sequence(record["reviewers"])[1])["reviewer_id"] = mapping(
            sequence(record["reviewers"])[0]
        )["reviewer_id"]
    elif damage == "outcome":
        mapping(sequence(record["reviewers"])[0])["outcome"] = "fail"
    elif damage == "path":
        mapping(sequence(record["reviewers"])[0])["evidence_path"] = "../private"
    elif damage == "evidence-hash":
        mapping(sequence(record["reviewers"])[0])["evidence_sha256"] = "0" * 64
    else:
        reviewer = mapping(sequence(record["reviewers"])[0])
        envelope = mapping(json.loads(blobs[text_value(reviewer["evidence_path"])]))
        envelope["source_commit" if damage == "evidence-scope" else "evidence_locator"] = ""
        raw = json.dumps(envelope).encode()
        blobs[text_value(reviewer["evidence_path"])] = raw
        reviewer["evidence_sha256"] = hashlib.sha256(raw).hexdigest()

    def forbidden(*args: object) -> None:
        raise AssertionError("Model eligibility must not be reached")

    monkeypatch.setattr(gate.model, "admit_model", forbidden)
    with pytest.raises(ValueError):
        verify(synthetic)


@pytest.mark.parametrize(
    "damage",
    ["slot", "path", "commit-type", "source-parity", "environment", "admission", "request"],
)
def test_gate_identity_and_confinement_failures(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    kwargs: VerifyOptions = {}
    if damage == "slot":
        kwargs["slot"] = "unknown"
    elif damage == "path":
        kwargs["path"] = synthetic[0] / ".." / "outside.json"
    elif damage == "commit-type":
        kwargs["review"] = None
    elif damage == "source-parity":

        def different_files(root: Path, commit: str, *args: object) -> list[ObjectMap]:
            return synthetic[5] if commit == S else []

        monkeypatch.setattr(gate.freeze, "_committed_files", different_files)
    elif damage == "environment":
        synthetic[6]["changed"] = True
    elif damage == "admission":

        def changed_admission(root: Path) -> ObjectMap:
            return {"admission_sha256": "x"}

        monkeypatch.setattr(gate.model, "admit_model", changed_admission)
    else:

        def changed_request(*args: object) -> ObjectMap:
            return {"request": {}, "eligibility": {"admission_sha256": "d" * 64}}

        monkeypatch.setattr(gate.binding, "bind_slot", changed_request)
    with pytest.raises(ValueError):
        verify(synthetic, **kwargs)


@pytest.mark.parametrize(
    "entry", [b"", b"120000 blob " + b"a" * 40 + b"\t" + gate.REVIEW_PATH.encode() + b"\0"]
)
def test_review_record_must_be_regular_blob(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch, entry: bytes
) -> None:
    def invalid_entry(*args: object) -> bytes:
        return entry

    monkeypatch.setattr(gate.freeze, "_git", invalid_entry)
    with pytest.raises(ValueError, match="review_not_regular_blob"):
        gate._blob(synthetic[0], R, gate.REVIEW_PATH)


def test_review_envelopes_bind_environment_not_only_outer_record(synthetic: GateFixture) -> None:
    synthetic[6]["changed"] = True
    synthetic[3]["environment_sha256"] = gate.identity.digest(synthetic[6])
    with pytest.raises(ValueError, match="review_evidence_scope_mismatch"):
        verify(synthetic)


def test_unsupported_platform_rejected_before_repository(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gate.platform, "system", lambda: "Linux")

    def forbidden(*args: object) -> None:
        pytest.fail("No repository lookup")

    monkeypatch.setattr(gate.freeze, "_repository", forbidden)
    with pytest.raises(ValueError, match="unsupported_primary_platform"):
        verify(synthetic)


def test_wrong_loaded_checkout_rejected_before_eligibility(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    def origin_failure(*args: object) -> None:
        raise ValueError("project_import_origin_mismatch")

    def forbidden(root: Path) -> None:
        pytest.fail("No eligibility after origin mismatch")

    monkeypatch.setattr(gate.identity, "project_closure", origin_failure)
    monkeypatch.setattr(gate.model, "admit_model", forbidden)
    with pytest.raises(ValueError, match="project_import_origin_mismatch"):
        verify(synthetic)


def commit_review(synthetic: GateFixture, damage: str = "none") -> tuple[str, str]:
    root, _path, _value, record, blobs, *_ = synthetic
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
    for item in sequence(record["reviewers"]):
        reviewer = mapping(item)
        evidence_path = text_value(reviewer["evidence_path"])
        envelope = mapping(json.loads(blobs[evidence_path]))
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
def test_real_git_source_review_and_evidence_integration(
    synthetic: GateFixture, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
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
