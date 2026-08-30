"""Synthetic-only server profile checks without process or network execution."""

import hashlib
import json
import sys
from pathlib import Path

import pytest

from tools import darwin_runtime_v030 as cli
from tools import darwin_server_v030 as server


@pytest.fixture
def files(tmp_path, monkeypatch):
    source = tmp_path / "source.py"
    source.write_bytes(b"source")
    evidence = tmp_path / "LICENSE"
    evidence.write_bytes(b"synthetic licence")
    monkeypatch.setattr(server, "SOURCE_ROOT", tmp_path.resolve())
    monkeypatch.setattr(
        server, "SOURCE_FILES", {source.name: hashlib.sha256(b"source").hexdigest()}
    )
    monkeypatch.setattr(
        server,
        "EVIDENCE_FILES",
        {str(evidence.resolve()): hashlib.sha256(b"synthetic licence").hexdigest()},
    )
    calls = []
    monkeypatch.setattr(server.core, "verify_files", lambda config: calls.append(config))
    return source, evidence, calls


def test_server_is_distinct_without_mutating_cli():
    assert server.EXECUTABLE.endswith("/0.3.0/bin/llama-server")
    assert (
        server.PINNED_FILES[server.EXECUTABLE]
        == "07c17ec087076d582147208beadba5cbe534ae6e5015658e6f4c96d9457232f6"
    )
    assert cli.EXECUTABLE not in server.PINNED_FILES
    assert not any("cli-impl" in name for name in server.PINNED_FILES)
    assert any("cli-impl" in name for name in cli.PINNED_FILES)
    expected_required = {name for name in server.PINNED_FILES if "/libexec/" not in name}
    assert expected_required == server.REQUIRED_IMAGES
    assert server.PINNED_FILES is not cli.PINNED_FILES
    assert server.EVIDENCE_FILES == cli.EVIDENCE_FILES
    assert server.EVIDENCE_FILES is not cli.EVIDENCE_FILES
    assert len(server.EVIDENCE_FILES) == 13
    assert set(server.SOURCE_FILES) == {
        "darwin_runtime_profile.py",
        "darwin_runtime_v030.py",
        "local_model_comparator.py",
    }


def test_profile_digest_covers_pins_sources_evidence_and_version(monkeypatch):
    original = server.profile_digest()
    assert len(original) == 64
    assert original != cli.profile_digest()
    for name, value in (
        ("SOURCE_FILES", {"new.py": "a" * 64}),
        ("EVIDENCE_FILES", {}),
        ("VERSION_MARKERS", (b"changed",)),
        ("VERSION_LINE", b"changed"),
        ("PROFILE_ID", "changed"),
        ("PINNED_FILES", {}),
        ("LOAD_ALIASES", {}),
    ):
        with monkeypatch.context() as patch:
            patch.setattr(server, name, value)
            assert server.profile_digest() != original


def test_verify_sources_and_rights_before_runtime(files):
    _, _, calls = files
    assert server.verify_files() is None
    assert calls == [sys.modules[server.__name__]]


@pytest.mark.parametrize("target", ["source", "evidence"])
@pytest.mark.parametrize("damage", ["missing", "changed", "symlink", "directory"])
def test_missing_or_changed_sources_and_rights_fail_closed(files, target, damage):
    source, evidence, calls = files
    path = source if target == "source" else evidence
    original = path.read_bytes()
    path.unlink()
    if damage == "changed":
        path.write_bytes(b"changed")
    elif damage == "symlink":
        other = path.with_name("same-bytes")
        other.write_bytes(original)
        path.symlink_to(other)
    elif damage == "directory":
        path.mkdir()
    with pytest.raises(ValueError):
        server.verify_files()
    assert calls == []


def test_runtime_failure_propagates(files, monkeypatch):
    def fail(config):
        raise ValueError("profile_backend_inventory_mismatch")

    monkeypatch.setattr(server.core, "verify_files", fail)
    with pytest.raises(ValueError, match="profile_backend_inventory_mismatch"):
        server.verify_files()


def test_environment_does_not_inherit_secrets(monkeypatch):
    monkeypatch.setenv("SECRET_TOKEN", "private")
    assert server.profile_environment() == {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "DYLD_LIBRARY_PATH": ":".join(server.LIBRARY_DIRS),
        "DYLD_PRINT_LIBRARIES": "1",
    }


def test_loader_uses_server_identity_not_cli(monkeypatch):
    paths = {"/synthetic/llama-server": "a" * 64, "/synthetic/libserver.dylib": "b" * 64}
    monkeypatch.setattr(server, "PINNED_FILES", paths)
    monkeypatch.setattr(server, "REQUIRED_IMAGES", set(paths))
    stderr = "".join(
        f"dyld[123]: <12345678-1234-1234-1234-123456789ABC> {path}\n" for path in paths
    ).encode()
    assert server.verify_loaded_images(stderr) == sorted(paths)
    with pytest.raises(ValueError):
        server.verify_loaded_images(
            stderr + b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> /synthetic/llama-cli\n"
        )


def test_source_pins_match_reviewed_repository_bytes():
    for name, digest in server.SOURCE_FILES.items():
        assert (
            hashlib.sha256((Path(server.__file__).parent / name).read_bytes()).hexdigest() == digest
        )


@pytest.mark.parametrize("diagnostic", ["version", "help"])
@pytest.mark.parametrize(
    "status", ["runtime_profile_observed", "profile_failed", "unsupported_platform"]
)
def test_diagnostic_cli_reserves_before_capture(tmp_path, monkeypatch, capsys, diagnostic, status):
    destination = tmp_path.resolve() / "receipt.json"
    calls = []

    def capture(config, diagnostic):
        assert destination.read_bytes() == b""
        calls.append((config, diagnostic))
        return {"status": status, "admitted": False, "study_unlocked": False}

    monkeypatch.setattr(server.core, "capture_version", capture)
    result = server.main(["--receipt", str(destination), "--diagnostic", diagnostic])
    assert result == (0 if status == "runtime_profile_observed" else 1)
    assert calls == [(sys.modules[server.__name__], diagnostic)]
    raw = destination.read_bytes()
    assert b"\r\n" not in raw
    receipt = json.loads(raw)
    assert receipt["admitted"] is receipt["study_unlocked"] is False
    summary = json.loads(capsys.readouterr().out)
    assert summary["receipt_sha256"] == hashlib.sha256(raw).hexdigest()
    assert summary["study_unlocked"] is False
    assert str(tmp_path) not in json.dumps(summary)


@pytest.mark.parametrize(
    "kind", ["existing", "missing-parent", "symlink-file", "symlink-parent", "parent-traversal"]
)
def test_diagnostic_cli_refuses_unsafe_destination_before_capture(
    tmp_path, monkeypatch, capsys, kind
):
    root = tmp_path.resolve()
    destination = root / "receipt.json"
    if kind == "existing":
        destination.write_bytes(b"preserve")
    elif kind == "missing-parent":
        destination = root / "missing" / "receipt.json"
    elif kind == "symlink-file":
        destination.symlink_to(root / "absent")
    elif kind == "symlink-parent":
        link = root / "link"
        link.symlink_to(root, target_is_directory=True)
        destination = link / "receipt.json"
    else:
        nested = root / "nested"
        nested.mkdir()
        destination = nested / ".." / "receipt.json"

    def forbidden(*args, **kwargs):
        raise AssertionError("capture must not run")

    monkeypatch.setattr(server.core, "capture_version", forbidden)
    assert server.main(["--receipt", str(destination)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "receipt_unavailable"
    if kind == "existing":
        assert destination.read_bytes() == b"preserve"


def test_diagnostic_cli_default_and_capture_error(tmp_path, monkeypatch, capsys):
    destination = tmp_path.resolve() / "receipt.json"

    def fail(config, diagnostic):
        assert diagnostic == "version"
        raise OSError("private-error-path")

    monkeypatch.setattr(server.core, "capture_version", fail)
    assert server.main(["--receipt", str(destination)]) == 1
    summary = capsys.readouterr().out
    assert "private-error-path" not in summary
    assert destination.read_bytes() == b""


def test_diagnostic_cli_rejects_other_modes(tmp_path):
    with pytest.raises(SystemExit):
        server.main(["--receipt", str(tmp_path / "receipt.json"), "--diagnostic", "serve"])


def test_diagnostic_cli_rejects_parent_resolution_change(tmp_path, monkeypatch):
    destination = tmp_path.resolve() / "receipt.json"
    monkeypatch.setattr(Path, "resolve", lambda path, strict=False: path / "changed")

    def forbidden(*args, **kwargs):
        raise AssertionError("capture must not run")

    monkeypatch.setattr(server.core, "capture_version", forbidden)
    assert server.main(["--receipt", str(destination)]) == 1
