"""Synthetic-only pinned Darwin loader checks; never launch a real runtime."""

import base64
import hashlib
import json
import subprocess
from types import SimpleNamespace

import pytest

from tools import darwin_runtime_profile as profile

VERSION_OUTPUT = b"version: 0.2.0 (build 10566, commit bb4caa754)\n"


@pytest.fixture
def pinned(tmp_path, monkeypatch):
    paths = []
    for name in ("llama-cli", "libllama.dylib", "libggml-cpu.dylib"):
        path = tmp_path / name
        path.write_bytes(name.encode())
        paths.append(str(path.resolve()))
    monkeypatch.setattr(
        profile,
        "PINNED_FILES",
        dict(
            zip(
                paths,
                [
                    hashlib.sha256(name.encode()).hexdigest()
                    for name in ("llama-cli", "libllama.dylib", "libggml-cpu.dylib")
                ],
                strict=True,
            )
        ),
    )
    monkeypatch.setattr(profile, "REQUIRED_IMAGES", set(paths[:2]))
    monkeypatch.setattr(profile, "LIBRARY_DIRS", (str(tmp_path.resolve()),))
    monkeypatch.setattr(profile, "EXECUTABLE", paths[0])
    monkeypatch.setattr(profile, "LOAD_ALIASES", {})
    monkeypatch.setattr(profile.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(profile.platform, "machine", lambda: "arm64")

    def forbidden(*args, **kwargs):
        raise AssertionError("real execution forbidden")

    monkeypatch.setattr(profile.subprocess, "run", forbidden)
    return paths


def trace(paths):
    return "".join(
        f"dyld[123]: <12345678-1234-1234-1234-123456789ABC> {path}\n" for path in paths
    ).encode()


def process(monkeypatch, paths, out=VERSION_OUTPUT, err=None, code=0, failure=None, mutate=None):
    calls = []

    def execute(args, **kwargs):
        calls.append((args, kwargs))
        kwargs["stdout"].write(out)
        kwargs["stderr"].write(trace(paths) if err is None else err)
        if mutate:
            mutate()
        if failure:
            raise failure
        return SimpleNamespace(returncode=code)

    monkeypatch.setattr(profile.subprocess, "run", execute)
    return calls


def test_environment_is_fresh_and_minimal(pinned, monkeypatch):
    monkeypatch.setenv("SECRET_API_TOKEN", "private")
    monkeypatch.setenv("DYLD_INSERT_LIBRARIES", "/private/injection")
    expected = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "DYLD_LIBRARY_PATH": ":".join(profile.LIBRARY_DIRS),
        "DYLD_PRINT_LIBRARIES": "1",
    }
    first = profile.profile_environment()
    assert first == expected
    first["LANG"] = "changed"
    assert profile.profile_environment() == expected


def test_profile_digest_stable_and_covers_configuration(pinned, monkeypatch):
    original = profile.profile_digest()
    assert len(original) == 64
    monkeypatch.setattr(profile, "PINNED_FILES", dict(reversed(list(profile.PINNED_FILES.items()))))
    assert profile.profile_digest() == original
    for attribute, changed in (
        ("EXECUTABLE", "/different"),
        ("LIBRARY_DIRS", ("/different",)),
        ("REQUIRED_IMAGES", set(pinned)),
        ("PINNED_FILES", {pinned[0]: "0" * 64}),
    ):
        with monkeypatch.context() as patch:
            patch.setattr(profile, attribute, changed)
            assert profile.profile_digest() != original


def test_verify_files_accepts_exact_bytes(pinned):
    assert profile.verify_files() is None


def test_backend_discovery_directory_rejects_extra_or_missing(pinned, tmp_path, monkeypatch):
    backend_dir = tmp_path.resolve() / "libexec"
    backend_dir.mkdir()
    backend = backend_dir / "cpu.so"
    backend.write_bytes(b"backend")
    monkeypatch.setattr(
        profile,
        "PINNED_FILES",
        {**profile.PINNED_FILES, str(backend): hashlib.sha256(b"backend").hexdigest()},
    )
    profile.verify_files()
    extra = backend_dir / "unknown.so"
    extra.write_bytes(b"extra")
    with pytest.raises(ValueError, match="profile_backend_inventory_mismatch"):
        profile.verify_files()
    extra.unlink()
    backend.unlink()
    backend_dir.rmdir()
    with pytest.raises(ValueError, match="profile_backend_directory_unavailable"):
        profile.verify_files()


def test_verify_files_checks_loader_alias_resolution(pinned, monkeypatch):
    from pathlib import Path

    alias = Path(pinned[1]).with_name("libllama.0.dylib")
    alias.symlink_to(pinned[1])
    original = profile.profile_digest()
    monkeypatch.setattr(profile, "LOAD_ALIASES", {str(alias): pinned[1]})
    assert profile.profile_digest() != original
    assert profile.verify_files() is None
    alias.unlink()
    alias.symlink_to(pinned[2])
    with pytest.raises(ValueError):
        profile.verify_files()


def test_verify_files_rejects_absent_loader_alias(pinned, monkeypatch):
    from pathlib import Path

    alias = Path(pinned[1]).with_name("absent.dylib")
    monkeypatch.setattr(profile, "LOAD_ALIASES", {str(alias): pinned[1]})
    with pytest.raises(ValueError):
        profile.verify_files()


@pytest.mark.parametrize("damage", ["missing", "changed", "symlink", "directory"])
def test_verify_files_rejects_damage(pinned, damage):
    from pathlib import Path

    path = Path(pinned[1])
    path.unlink()
    if damage == "changed":
        path.write_bytes(b"changed")
    elif damage == "symlink":
        replacement = path.with_name("same-bytes-other-location")
        replacement.write_bytes(b"libllama.dylib")
        path.symlink_to(replacement)
    elif damage == "directory":
        path.mkdir()
    with pytest.raises(ValueError):
        profile.verify_files()


def test_loader_accepts_system_and_optional_backend(pinned):
    stderr = trace(
        pinned
        + [
            pinned[0],
            "/usr/lib/libSystem.B.dylib",
            "/System/Library/Frameworks/Security.framework/Security",
        ]
    )
    assert profile.verify_loaded_images(stderr) == sorted(pinned)


def test_loader_allows_delayed_diagnostic(pinned):
    stderr = trace(pinned) + b"dyld[123]: move delayed to loaded: libggml-cpu.dylib\n"
    assert profile.verify_loaded_images(stderr) == sorted(pinned)


def test_loader_rejects_delayed_image_without_full_record(pinned):
    stderr = trace(pinned[:2]) + b"dyld[123]: move delayed to loaded: libggml-cpu.dylib\n"
    with pytest.raises(ValueError):
        profile.verify_loaded_images(stderr)


def test_loader_allows_runtime_logs_without_treating_them_as_images(pinned):
    stderr = b"runtime: initialising\n" + trace(pinned[:2])
    assert profile.verify_loaded_images(stderr) == sorted(pinned[:2])


def test_loader_accepts_reverse_transition_only_with_full_image(pinned):
    known = trace(pinned) + b"dyld[123]: move loaded to delayed: libggml-cpu.dylib\n"
    assert profile.verify_loaded_images(known) == sorted(pinned)
    with pytest.raises(ValueError, match="incomplete_loader_evidence"):
        profile.verify_loaded_images(
            trace(pinned[:2]) + b"dyld[123]: move loaded to delayed: libggml-cpu.dylib\n"
        )


@pytest.mark.parametrize(
    "extra",
    [
        b"dyld[123]: malformed\n",
        b"dyld[123]: <UUID> /private/evil.dylib\n",
        b"\xff",
        b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> /usr/lib/../private/evil.dylib\n",
    ],
)
def test_loader_rejects_malformed_or_unknown(pinned, extra):
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace(pinned) + extra)


@pytest.mark.parametrize("kind", ["none", "missing", "unknown-backend", "fake-system"])
def test_loader_requires_attested_images(pinned, kind):
    paths = {
        "none": [],
        "missing": pinned[1:],
        "unknown-backend": pinned + ["/private/libggml-metal.dylib"],
        "fake-system": pinned + ["/usr/library/evil.dylib"],
    }[kind]
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace(paths))


def test_loader_rejects_mixed_process_evidence(pinned):
    stderr = trace(pinned[:1]) + trace(pinned[1:]).replace(b"dyld[123]", b"dyld[456]")
    with pytest.raises(ValueError):
        profile.verify_loaded_images(stderr)


@pytest.mark.parametrize("suffix", ["/../evil", "//evil", "/./evil", "/evil\x00"])
def test_loader_rejects_noncanonical_system_paths(pinned, suffix):
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace(pinned + ["/usr/lib" + suffix]))


def test_capture_success_fixed_invocation(pinned, monkeypatch):
    calls = process(monkeypatch, pinned)
    receipt = profile.capture_version()
    args, kwargs = calls[0]
    assert args == [pinned[0], "--version"]
    assert kwargs["env"] == profile.profile_environment()
    assert kwargs["stdin"] == subprocess.DEVNULL
    assert kwargs["timeout"] == 60
    assert kwargs["check"] is False
    assert not kwargs.get("shell", False)
    assert receipt["status"] == "runtime_profile_observed"
    assert receipt["admitted"] is receipt["study_unlocked"] is False
    assert base64.b64decode(receipt["raw_stdout_base64"]) == VERSION_OUTPUT
    assert base64.b64decode(receipt["raw_stderr_base64"]) == trace(pinned)
    assert receipt["stdout_sha256"] == hashlib.sha256(VERSION_OUTPUT).hexdigest()
    assert receipt["stderr_sha256"] == hashlib.sha256(trace(pinned)).hexdigest()
    assert receipt["stdout_bytes"] == len(VERSION_OUTPUT)
    assert receipt["stderr_bytes"] == len(trace(pinned))


@pytest.mark.parametrize(
    "system,machine", [("Linux", "arm64"), ("Darwin", "x86_64"), ("Windows", "AMD64")]
)
def test_capture_unsupported_never_executes(pinned, monkeypatch, system, machine):
    monkeypatch.setattr(profile.platform, "system", lambda: system)
    monkeypatch.setattr(profile.platform, "machine", lambda: machine)
    receipt = profile.capture_version()
    assert receipt["status"] == "unsupported_platform"
    assert receipt["admitted"] is receipt["study_unlocked"] is False


@pytest.mark.parametrize(
    "damage",
    ["bad-version", "nonzero", "loader", "timeout", "launch", "file-drift", "profile-drift"],
)
def test_capture_fail_closed(pinned, monkeypatch, damage):
    from pathlib import Path

    options = {}
    if damage == "bad-version":
        options["out"] = b"version: 99999 (unknown)\n"
    elif damage == "nonzero":
        options["code"] = 2
    elif damage == "loader":
        options["err"] = trace(pinned + ["/private/unknown.dylib"])
    elif damage == "timeout":
        options["failure"] = subprocess.TimeoutExpired("private-launch", 60)
    elif damage == "launch":
        options["failure"] = OSError("private-launch")
    elif damage == "file-drift":
        options["mutate"] = lambda: Path(pinned[1]).write_bytes(b"changed")
    else:
        options["mutate"] = lambda: monkeypatch.setattr(profile, "LIBRARY_DIRS", ("/changed",))
    process(monkeypatch, pinned, **options)
    receipt = profile.capture_version()
    assert receipt["status"] == "profile_failed"
    assert receipt["admitted"] is receipt["study_unlocked"] is False
    assert "private-launch" not in json.dumps(receipt)


def test_capture_rejects_preexisting_file_damage(pinned):
    from pathlib import Path

    Path(pinned[1]).unlink()
    assert profile.capture_version()["status"] == "profile_failed"


def test_capture_rejects_adapter_digest_drift(pinned, monkeypatch):
    real_hash = profile._sha256
    adapter_calls = []

    def fake_hash(path):
        if str(path) == profile.__file__:
            adapter_calls.append(path)
            return "a" * 64 if len(adapter_calls) == 1 else "b" * 64
        return real_hash(path)

    monkeypatch.setattr(profile, "_sha256", fake_hash)
    process(monkeypatch, pinned)
    result = profile.capture_version()
    assert result["status"] == "profile_failed"
    assert result["pins_unchanged_after"] is False


def test_capture_exact_output_limit_is_retained(pinned, monkeypatch):
    out = VERSION_OUTPUT + b" " * (1048576 - len(VERSION_OUTPUT))
    process(monkeypatch, pinned, out=out)
    receipt = profile.capture_version()
    assert receipt["status"] == "runtime_profile_observed"
    assert base64.b64decode(receipt["raw_stdout_base64"]) == out
    assert receipt["stdout_sha256"] == hashlib.sha256(out).hexdigest()


@pytest.mark.parametrize("stream", ["out", "err"])
def test_capture_oversize_not_partially_attested(pinned, monkeypatch, stream):
    oversized = b"x" * (1048576 + 1)
    if stream == "out":
        process(monkeypatch, pinned, out=oversized)
    else:
        process(monkeypatch, pinned, err=oversized)
    receipt = profile.capture_version()
    assert receipt["status"] == "profile_failed"
    key = "stdout" if stream == "out" else "stderr"
    assert receipt[f"raw_{key}_base64"] is None
    assert receipt[f"{key}_sha256"] is None
    assert receipt[f"{key}_bytes"] == 1048577


def test_cli_exclusive_receipt_and_safe_summary(pinned, monkeypatch, tmp_path, capsys):
    process(monkeypatch, pinned)
    destination = tmp_path / "receipt.json"
    assert profile.main(["--receipt", str(destination)]) == 0
    original = destination.read_bytes()
    assert json.loads(original)["status"] == "runtime_profile_observed"
    assert str(tmp_path) not in capsys.readouterr().out
    assert profile.main(["--receipt", str(destination)]) != 0
    assert destination.read_bytes() == original


def test_cli_write_failure_is_safe(pinned, monkeypatch, tmp_path, capsys):
    process(monkeypatch, pinned)
    assert profile.main(["--receipt", str(tmp_path / "missing" / "receipt.json")]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "receipt_write_failed"
    assert str(tmp_path) not in json.dumps(result)


def test_cli_existing_symlink_does_not_execute(pinned, tmp_path):
    destination = tmp_path / "receipt.json"
    destination.symlink_to(tmp_path / "absent.json")
    assert profile.main(["--receipt", str(destination)]) == 1
    assert destination.is_symlink()


def test_cli_requires_receipt(pinned):
    with pytest.raises(SystemExit):
        profile.main([])
