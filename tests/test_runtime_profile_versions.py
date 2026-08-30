"""Explicit synthetic profiles share verification without mutating legacy pins."""

import hashlib
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from tools import darwin_runtime_profile as shared


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Any:
    cfg: Any = ModuleType("synthetic_profile")
    source = tmp_path / "profile.py"
    source.write_bytes(b"# synthetic profile\n")
    cfg.__file__ = str(source)
    executable = tmp_path / "synthetic-cli"
    executable.write_bytes(b"synthetic executable")
    cfg.EXECUTABLE = str(executable.resolve())
    cfg.PINNED_FILES = {cfg.EXECUTABLE: hashlib.sha256(executable.read_bytes()).hexdigest()}
    cfg.REQUIRED_IMAGES = {cfg.EXECUTABLE}
    cfg.LIBRARY_DIRS = (str(tmp_path.resolve()),)
    cfg.LOAD_ALIASES = {}
    cfg.VERSION_LINE = b"version: synthetic-only"
    cfg.verify_files = lambda: shared.verify_files(cfg)
    cfg.profile_digest = lambda: shared.profile_digest(cfg)
    cfg.profile_environment = lambda: shared.profile_environment(cfg)
    cfg.verify_loaded_images = lambda err: shared.verify_loaded_images(err, cfg)
    monkeypatch.setattr(shared.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(shared.platform, "machine", lambda: "arm64")

    def forbidden(*args, **kwargs):
        raise AssertionError("real process forbidden")

    monkeypatch.setattr(shared.subprocess, "run", forbidden)
    return cfg


def process(cfg, monkeypatch, out=None, mutate=None):
    calls = []

    def run(args, **kwargs):
        calls.append((args, kwargs))
        kwargs["stdout"].write(cfg.VERSION_LINE if out is None else out)
        # Synthetic loader verification supplied explicitly; native Windows paths
        # must never masquerade as Darwin loader records in portable fixtures.
        kwargs["stderr"].write(b"synthetic loader evidence")
        if mutate:
            mutate()
        return subprocess.CompletedProcess(args, 0)

    cfg.verify_loaded_images = lambda err: [cfg.EXECUTABLE]
    monkeypatch.setattr(shared.subprocess, "run", run)
    return calls


def test_explicit_profile_does_not_mutate_legacy(tmp_path, monkeypatch):
    old = shared.profile_digest()
    cfg = fixture(tmp_path, monkeypatch)
    shared.verify_files(cfg)
    assert shared.profile_digest(cfg) != old
    assert shared.profile_digest() == old
    assert shared.profile_environment(cfg)["DYLD_LIBRARY_PATH"] == str(tmp_path.resolve())


@pytest.mark.parametrize("diagnostic,out", [("version", None), ("help", b"synthetic help")])
def test_explicit_capture_binds_both_sources(tmp_path, monkeypatch, diagnostic, out):
    cfg = fixture(tmp_path, monkeypatch)
    calls = process(cfg, monkeypatch, out)
    result = shared.capture_version(cfg, diagnostic=diagnostic)
    assert result["status"] == "runtime_profile_observed"
    assert calls[0][0] == [cfg.EXECUTABLE, "--" + diagnostic]
    assert result["profile_module_sha256"] == shared._sha256(Path(cfg.__file__))
    assert result["shared_helper_sha256"] == shared._sha256(Path(shared.__file__))
    assert result["diagnostic"] == diagnostic
    assert result["admitted"] is result["study_unlocked"] is False
    assert not any("OpenSSL" in item for item in result["limitations"])
    assert set(calls[0][1]["env"]) == {"PATH", "LANG", "DYLD_LIBRARY_PATH", "DYLD_PRINT_LIBRARIES"}


@pytest.mark.parametrize("source", ["profile", "helper"])
def test_source_drift_fails(tmp_path, monkeypatch, source):
    cfg = fixture(tmp_path, monkeypatch)
    real = shared._sha256
    target = cfg.__file__ if source == "profile" else shared.__file__
    calls = []

    def drift(path):
        if str(path) == target:
            calls.append(path)
            return "a" * 64 if len(calls) == 1 else "b" * 64
        return real(path)

    monkeypatch.setattr(shared, "_sha256", drift)
    process(cfg, monkeypatch)
    result = shared.capture_version(cfg)
    assert result["status"] == "profile_failed"
    assert result["pins_unchanged_after"] is False


@pytest.mark.parametrize(
    "diagnostic,out",
    [("help", b""), ("version", b"wrong version"), ("help", b"x" * (1024 * 1024 + 1))],
    ids=["emptyhelp", "wrongversion", "oversize"],
)
def test_bad_diagnostic_output(tmp_path, monkeypatch, diagnostic, out):
    cfg = fixture(tmp_path, monkeypatch)
    process(cfg, monkeypatch, out)
    result = shared.capture_version(cfg, diagnostic=diagnostic)
    assert result["status"] == "profile_failed"
    assert result["admitted"] is False


def test_unknown_diagnostic_never_executes(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="unsupported_diagnostic"):
        shared.capture_version(cfg, diagnostic="shell")


def test_cross_profile_loader_rejected(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    cfg.PINNED_FILES = {"/synthetic/new/cli": "a" * 64}
    cfg.REQUIRED_IMAGES = set(cfg.PINNED_FILES)
    trace = b"dyld[1]: <12345678-1234-1234-1234-123456789ABC> /synthetic/old/cli\n"
    with pytest.raises(ValueError, match="unexpected_loaded_image"):
        shared.verify_loaded_images(trace, cfg)
    assert shared.verify_loaded_images(trace.replace(b"/old/", b"/new/"), cfg) == [
        "/synthetic/new/cli"
    ]


def test_explicit_file_damage_not_legacy(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    Path(cfg.EXECUTABLE).write_bytes(b"changed")
    with pytest.raises(ValueError, match="profile_hash_mismatch"):
        shared.verify_files(cfg)


def test_version_requires_all_markers(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    cfg.VERSION_MARKERS = (cfg.VERSION_LINE, b"commit synthetic)")
    process(cfg, monkeypatch)
    assert shared.capture_version(cfg)["reason"] == "version_mismatch"
    process(cfg, monkeypatch, cfg.VERSION_LINE + b" commit synthetic)")
    assert shared.capture_version(cfg)["status"] == "runtime_profile_observed"


def test_unavailable_profile_source_fails_before_execution(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    cfg.__file__ = None
    result = shared.capture_version(cfg, diagnostic="help")
    assert result["status"] == "profile_failed"
    assert result["purpose"] == "runtime-profile-diagnostic-only"
    assert result["execution_observed"] is False


def test_profile_configuration_drift(tmp_path, monkeypatch):
    cfg = fixture(tmp_path, monkeypatch)
    process(cfg, monkeypatch, mutate=lambda: setattr(cfg, "LIBRARY_DIRS", ("/changed",)))
    result = shared.capture_version(cfg)
    assert result["reason"] == "profile_changed"
    assert result["pins_unchanged_after"] is False
