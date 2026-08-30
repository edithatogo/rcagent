"""Temporary Git histories prove byte consistency, never study execution."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from tools import prospective_freeze
from tools.prospective_freeze import COMPONENTS, verify_freeze
from tools.prospective_protocol import CLAIMS, GENERATION


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def pin(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root: Path) -> tuple[Path, str]:
    git(root, "init", "-q")
    git(root, "config", "user.email", "synthetic@example.invalid")
    git(root, "config", "user.name", "Synthetic Fixture")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "core.safecrlf", "false")
    refs = {}
    for name in ("case-a", "case-b", "rubric", "instructions", "prompt"):
        path = root / f"{name}.txt"
        path.write_text(f"Synthetic {name}", encoding="utf-8")
        refs[name] = {"path": path.name, "sha256": pin(path)}
    for component in COMPONENTS:
        path = root / component
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Synthetic component only\n", encoding="utf-8")
    value = {
        "schema_version": "1.0",
        "kind": "prospective-study-protocol",
        "protocol_version": "1.0.0",
        "study_id": "prospective-test-only",
        "data_class": "synthetic",
        "case_exposure": "public",
        "held_out": False,
        "claims_boundary": CLAIMS,
        "repeats": 1,
        "cases": [{"id": name, "input": refs[name]} for name in ("case-a", "case-b")],
        "condition": {
            "id": "condition-test",
            "model_id": "model-test",
            "model_revision": "a" * 40,
            **{
                f"{name}_sha256": "b" * 64
                for name in ("model", "runtime", "profile", "adapter", "registry")
            },
        },
        "expected_slots": [f"case-{c}__condition-test__r1" for c in ("a", "b")],
        "rubric": refs["rubric"],
        "scoring_instructions": refs["instructions"],
        "prompt_template": refs["prompt"],
        "generation": GENERATION,
        "technical_retries": 1,
        "blinding": "metadata-blinding-v1",
        "normalization": "identity-utf8-v1",
        "scoring": {
            "reviewer_class": "agent",
            "roles": ["scorer-1", "scorer-2", "scorer-3"],
            "adjudication": "after-three-sealed-submissions",
            "raw_agreement_minimum": 0.8,
            "ordinal_agreement_minimum": 0.67,
            "hard_gates": ["privacy", "cultural-safety", "clinical-safety", "authority-boundaries"],
            "non_operational": True,
        },
    }
    protocol = root / "protocol.json"
    protocol.write_text(json.dumps(value), encoding="utf-8")
    git(root, "add", ".")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic fixture")
    return protocol, git(root, "rev-parse", "HEAD")


def test_exact_commit_is_not_admission(tmp_path: Path) -> None:
    protocol, commit = fixture(tmp_path)
    result = verify_freeze(protocol, pin(protocol), commit, tmp_path)
    assert result["status"] == "freeze_verified"
    assert result["study_unlocked"] is result["admitted"] is False
    assert len(result["files"]) == len(COMPONENTS) + 6


@pytest.mark.parametrize("commit", ["HEAD", "a" * 39, "a" * 40 + "\n", "0" * 40])
def test_bad_commit(tmp_path: Path, commit: str) -> None:
    protocol, _ = fixture(tmp_path)
    with pytest.raises(ValueError):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


@pytest.mark.parametrize(
    "mutation",
    [
        "component-change",
        "component-missing",
        "ref-change",
        "untracked",
        "working-symlink",
        "tracked-symlink",
    ],
)
def test_mutations(tmp_path: Path, mutation: str) -> None:
    protocol, commit = fixture(tmp_path)
    target = tmp_path / COMPONENTS[0]
    if mutation == "component-change":
        target.write_text("changed", encoding="utf-8")
    elif mutation == "component-missing":
        target.unlink()
    elif mutation == "ref-change":
        (tmp_path / "rubric.txt").write_text("changed", encoding="utf-8")
    elif mutation == "untracked":
        git(tmp_path, "rm", "--cached", COMPONENTS[0])
        git(tmp_path, "-c", "commit.gpgsign=false", "commit", "-qm", "Remove tracked fixture")
        commit = git(tmp_path, "rev-parse", "HEAD")
    else:
        target.unlink()
        target.symlink_to(tmp_path / "rubric.txt")
        if mutation == "tracked-symlink":
            git(tmp_path, "add", COMPONENTS[0])
            git(tmp_path, "-c", "commit.gpgsign=false", "commit", "-qm", "Symlink fixture")
            commit = git(tmp_path, "rev-parse", "HEAD")
            target.unlink()
            target.write_text(str(tmp_path / "rubric.txt"), encoding="utf-8")
    with pytest.raises(ValueError):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


def test_wrong_root_and_outside_protocol(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    protocol, commit = fixture(root)
    for supplied_root in (tmp_path, root / "tools"):
        with pytest.raises(ValueError):
            verify_freeze(protocol, pin(protocol), commit, supplied_root)
    outside = tmp_path / "outside.json"
    outside.write_bytes(protocol.read_bytes())
    with pytest.raises(ValueError):
        verify_freeze(outside, pin(outside), commit, root)


def test_tree_object_not_commit(tmp_path: Path) -> None:
    protocol, _ = fixture(tmp_path)
    tree = git(tmp_path, "rev-parse", "HEAD^{tree}")
    with pytest.raises(ValueError):
        verify_freeze(protocol, pin(protocol), tree, tmp_path)


def test_git_environment_cannot_redirect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    protocol, commit = fixture(tmp_path)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY"):
        monkeypatch.setenv(name, "/nonexistent-synthetic-path")
    assert verify_freeze(protocol, pin(protocol), commit, tmp_path)["status"] == "freeze_verified"


def test_repinned_working_change_is_not_frozen(tmp_path: Path) -> None:
    protocol, commit = fixture(tmp_path)
    changed = tmp_path / "rubric.txt"
    changed.write_text("Synthetic replacement", encoding="utf-8")
    value = json.loads(protocol.read_text(encoding="utf-8"))
    value["rubric"]["sha256"] = pin(changed)
    protocol.write_text(json.dumps(value), encoding="utf-8")
    git(tmp_path, "add", ".")
    with pytest.raises(ValueError, match="freeze_bytes_mismatch"):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


def test_replacement_objects_ignored(tmp_path: Path) -> None:
    protocol, commit = fixture(tmp_path)
    original = git(tmp_path, "rev-parse", f"{commit}:{COMPONENTS[0]}")
    replacement_file = tmp_path / "replacement.txt"
    replacement_file.write_text("Synthetic replacement object", encoding="utf-8")
    replacement = git(tmp_path, "hash-object", "-w", str(replacement_file))
    git(tmp_path, "replace", original, replacement)
    assert verify_freeze(protocol, pin(protocol), commit, tmp_path)["status"] == "freeze_verified"


def test_protocol_changed_after_validation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    protocol, commit = fixture(tmp_path)
    original = prospective_freeze.validate_protocol
    expected = pin(protocol)

    def change_after_validation(path: Path, digest: str) -> dict:
        result = original(path, digest)
        path.write_bytes(path.read_bytes() + b"\n")
        return result

    monkeypatch.setattr(prospective_freeze, "validate_protocol", change_after_validation)
    with pytest.raises(ValueError, match="protocol_changed_during_verification"):
        verify_freeze(protocol, expected, commit, tmp_path)


def test_reference_rechecked_after_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    protocol, commit = fixture(tmp_path)
    original = prospective_freeze._bytes

    def changed_read(path: Path) -> bytes:
        if path.name == "rubric.txt":
            return b"Synthetic switched bytes"
        return original(path)

    monkeypatch.setattr(prospective_freeze, "_bytes", changed_read)
    with pytest.raises(ValueError, match="artifact_changed_during_verification"):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


def test_git_disables_lazy_fetch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original = subprocess.run

    def inspect(*args, **kwargs):
        assert kwargs["env"]["GIT_NO_LAZY_FETCH"] == "1"
        assert kwargs["env"]["GIT_NO_REPLACE_OBJECTS"] == "1"
        return original(*args, **kwargs)

    monkeypatch.setattr(prospective_freeze.subprocess, "run", inspect)
    assert prospective_freeze._git(tmp_path, "--version").startswith(b"git version")


@pytest.mark.parametrize("failure", [OSError("synthetic"), subprocess.TimeoutExpired("git", 10)])
def test_git_launch_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: Exception
) -> None:
    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(prospective_freeze.subprocess, "run", fail)
    with pytest.raises(ValueError, match="git_unavailable"):
        prospective_freeze._git(tmp_path, "--version")


def test_git_oversized_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def oversized(*args, **kwargs):
        kwargs["stdout"].write(b"x" * (prospective_freeze.MAX_BYTES + 1))
        return subprocess.CompletedProcess(args=[], returncode=0)

    monkeypatch.setattr(prospective_freeze.subprocess, "run", oversized)
    with pytest.raises(ValueError, match="git_lookup_failed"):
        prospective_freeze._git(tmp_path, "--version")


def test_missing_repository_root(tmp_path: Path) -> None:
    root = tmp_path / "missing"
    with pytest.raises(ValueError, match="invalid_repository_root"):
        verify_freeze(root / "protocol.json", "a" * 64, "b" * 40, root)


@pytest.mark.parametrize("mutation", ["root", "commit", "tree-path"])
def test_git_identity_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    protocol, commit = fixture(tmp_path)
    original = prospective_freeze._git

    def mismatched(root: Path, *args: str) -> bytes:
        if mutation == "root" and args == ("rev-parse", "--show-toplevel"):
            return str(tmp_path.parent).encode()
        if mutation == "commit" and args[:2] == ("rev-parse", "--verify"):
            return b"0" * 40
        value = original(root, *args)
        if mutation == "tree-path" and args[0] == "ls-tree":
            return value.replace(b"\tprotocol.json", b"\tother.json")
        return value

    monkeypatch.setattr(prospective_freeze, "_git", mismatched)
    reason = {
        "root": "repository_root_mismatch",
        "commit": "freeze_commit_mismatch",
        "tree-path": "untracked_or_nonregular_freeze_file",
    }[mutation]
    with pytest.raises(ValueError, match=reason):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


@pytest.mark.parametrize("component", ["protocol.json", "bad:path", "tools/../bad.py"])
def test_component_path_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, component: str
) -> None:
    protocol, commit = fixture(tmp_path)
    monkeypatch.setattr(prospective_freeze, "COMPONENTS", (component,))
    reason = "duplicate_freeze_path" if component == "protocol.json" else "invalid_freeze_path"
    with pytest.raises(ValueError, match=reason):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)


def test_same_size_component_change(tmp_path: Path) -> None:
    protocol, commit = fixture(tmp_path)
    component = tmp_path / COMPONENTS[0]
    original = component.read_bytes()
    component.write_bytes(original.replace(b"Synthetic", b"Different"))
    assert component.stat().st_size == len(original)
    with pytest.raises(ValueError, match="freeze_bytes_mismatch"):
        verify_freeze(protocol, pin(protocol), commit, tmp_path)
