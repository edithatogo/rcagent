"""Synthetic Git consistency checks are never a study freeze or admission."""

import json

import pytest

from tests.test_prospective_freeze import git
from tests.test_prospective_native_protocol import fixture as native_fixture
from tests.test_prospective_protocol import pin
from tools import prospective_native_prerequisites as subject


@pytest.fixture
def synthetic(tmp_path):
    root = tmp_path.resolve()
    path, value = native_fixture(root)
    git(root, "init", "-q")
    for key, val in (
        ("user.name", "Synthetic Fixture"),
        ("user.email", "synthetic@example.invalid"),
        ("core.autocrlf", "false"),
        ("core.safecrlf", "false"),
    ):
        git(root, "config", key, val)
    for source in subject.KNOWN_NATIVE_SOURCES:
        file = root / source
        file.parent.mkdir(exist_ok=True)
        file.write_bytes(b"# synthetic source, never imported\n")
    git(root, "add", ".")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic fixture")
    return root, path, value, git(root, "rev-parse", "HEAD")


def verify(fixture, **kwargs):
    root, path, value, commit = fixture
    return subject.verify_native_prerequisites(
        kwargs.get("path", path),
        kwargs.get("pin", pin(path)),
        kwargs.get("slot", value["expected_slots"][0]),
        kwargs.get("commit", commit),
        kwargs.get("root", root),
    )


def test_fixed_source_inventory_exists():
    assert "tools/prospective_native_prerequisites.py" in subject.KNOWN_NATIVE_SOURCES


def test_enumerated_consistency_never_permits_execution(synthetic):
    result = verify(synthetic)
    root, path, value, commit = synthetic
    assert result["status"] == "native_prerequisites_consistent"
    assert result["commit"] == commit and result["protocol_sha256"] == pin(path)
    assert result["slot_id"] == value["expected_slots"][0]
    assert all(
        result[key] is False
        for key in ("execution_permitted", "execution_observed", "admitted", "study_unlocked")
    )
    expected = {
        path.name,
        *subject.KNOWN_NATIVE_SOURCES,
        *(case["input"]["path"] for case in value["cases"]),
        *(value[key]["path"] for key in ("rubric", "scoring_instructions", "prompt_template")),
    }
    assert {item["path"] for item in result["files"]} == expected
    assert all(item["sha256"] == pin(root / item["path"]) for item in result["files"])
    assert "full-transitive-execution-closure" in result["pending"]
    assert "agent-review-evidence" in result["pending"]
    assert "not-study-freeze" in result["limitations"]


@pytest.mark.parametrize("slot", [None, [], "unknown", "x" * 151])
def test_slot_rejected_before_git(synthetic, monkeypatch, slot):
    def forbidden(*args):
        raise AssertionError("Git must not run for invalid slot")

    monkeypatch.setattr(subject.freeze, "_git", forbidden)
    with pytest.raises(ValueError, match="slot_not_in_protocol"):
        verify(synthetic, slot=slot)


@pytest.mark.parametrize("source", subject.KNOWN_NATIVE_SOURCES)
def test_each_fixed_source_drift_rejected(synthetic, source):
    root, _, _, _ = synthetic
    (root / source).write_bytes(b"changed")
    with pytest.raises(ValueError, match="freeze_bytes_mismatch"):
        verify(synthetic)


@pytest.mark.parametrize("kind", ["protocol", "input", "template", "rubric"])
def test_original_pins_retained_after_native_parse(synthetic, monkeypatch, kind):
    root, path, value, _ = synthetic
    original = subject.native._validated_candidate
    selected = {
        "protocol": path,
        "input": root / value["cases"][0]["input"]["path"],
        "template": root / value["prompt_template"]["path"],
        "rubric": root / value["rubric"]["path"],
    }[kind]
    calls = []

    def changed(*args):
        calls.append(args)
        result = original(*args)
        selected.write_bytes(b"changed after validation")
        return result

    monkeypatch.setattr(subject.native, "_validated_candidate", changed)
    with pytest.raises(ValueError, match="artifact_changed_during_verification"):
        verify(synthetic)
    assert len(calls) == 1


@pytest.mark.parametrize("damage", ["missing", "untracked", "symlink"])
def test_missing_untracked_and_symlink_sources_rejected(synthetic, damage):
    root, _, _, _ = synthetic
    file = root / subject.KNOWN_NATIVE_SOURCES[0]
    if damage == "missing":
        file.unlink()
    elif damage == "untracked":
        git(root, "rm", "--cached", str(file))
        git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic removal")
        synthetic = (*synthetic[:3], git(root, "rev-parse", "HEAD"))
    else:
        target = root / "synthetic-target.txt"
        target.write_bytes(file.read_bytes())
        file.unlink()
        try:
            file.symlink_to(target)
        except OSError:
            pytest.skip("Host does not permit fixture symlinks")
    with pytest.raises((ValueError, OSError)):
        verify(synthetic)


@pytest.mark.parametrize("commit", ["HEAD", "a" * 39, "a" * 40 + "\n", "0" * 40])
def test_invalid_or_absent_commit(synthetic, commit):
    with pytest.raises(ValueError):
        verify(synthetic, commit=commit)


def test_protocol_outside_repository_rejected(synthetic, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    path, _ = native_fixture(outside)
    root, _, _, commit = synthetic
    nested = root / "tools"
    with pytest.raises(ValueError, match="protocol_outside_repository"):
        subject.verify_native_prerequisites(
            path, pin(path), "case-a__condition-local-text__r1", commit, nested
        )


def test_original_ref_tamper_rejected_before_committed_checks(synthetic, monkeypatch):
    root, _, value, _ = synthetic
    (root / value["cases"][0]["input"]["path"]).write_bytes(b"changed")

    def forbidden(*args):
        raise AssertionError("Git must not run for invalid reference")

    monkeypatch.setattr(subject.freeze, "_committed_files", forbidden)
    with pytest.raises(ValueError, match="artifact_hash_mismatch"):
        verify(synthetic)


def test_well_formed_unknown_slot_rejected_before_file_checks(synthetic, monkeypatch):
    def forbidden(*args):
        raise AssertionError("No committed checks for undeclared slot")

    monkeypatch.setattr(subject.freeze, "_committed_files", forbidden)
    with pytest.raises(ValueError, match="slot_not_in_protocol"):
        verify(synthetic, slot="case-unknown__condition-local-text__r1")


@pytest.mark.parametrize("damage", ["traversal", "outside", "noncanonical-root", "commit-type"])
def test_boundary_rejected_before_protocol_parse(synthetic, monkeypatch, damage):
    root, path, _, _ = synthetic

    def forbidden(*args):
        raise AssertionError("Unconfined bytes must not be read")

    monkeypatch.setattr(subject.native, "_validated_candidate", forbidden)
    kwargs: dict = {"pin": pin(path)}
    if damage == "traversal":
        kwargs["path"] = root / "tools" / ".." / path.name
    elif damage == "outside":
        kwargs["root"] = root / "tools"
    elif damage == "noncanonical-root":
        kwargs["root"] = root / "tools" / ".."
    else:
        kwargs["commit"] = None
    with pytest.raises(ValueError):
        verify(synthetic, **kwargs)


def test_different_committed_protocol_rejected_even_if_current_valid(synthetic):
    _, path, value, _ = synthetic
    value["study_id"] = "prospective-another"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="freeze_bytes_mismatch"):
        verify(synthetic)
