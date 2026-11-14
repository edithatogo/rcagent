"""Synthetic-only pinned Darwin loader checks; never launch a real runtime."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
from collections.abc import Callable, Iterator
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import SimpleNamespace
from typing import BinaryIO, TypedDict, Unpack
from unittest.mock import Mock

import pytest

from tools import darwin_runtime_profile as profile

VERSION_OUTPUT = b"version: 0.2.0 (build 10566, commit bb4caa754)\n"


class RunOptions(TypedDict):
    stdout: BinaryIO
    stderr: BinaryIO
    stdin: int
    env: dict[str, str]
    timeout: int
    check: bool


class ProcessOptions(TypedDict, total=False):
    out: bytes
    err: bytes
    code: int
    failure: Exception
    mutate: Callable[[], object]


@pytest.fixture
def pinned(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> list[str]:
    paths: list[str] = []
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

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("real execution forbidden")

    monkeypatch.setattr(profile.subprocess, "run", forbidden)
    # File checks use native temporary paths; loader records always use Darwin paths.
    real_loader = profile.verify_loaded_images

    def mapped_loader(stderr: bytes) -> list[str]:
        with monkeypatch.context() as patch:
            patch.setattr(
                profile,
                "PINNED_FILES",
                {wire_path(name): digest for name, digest in profile.PINNED_FILES.items()},
            )
            patch.setattr(
                profile, "REQUIRED_IMAGES", {wire_path(name) for name in profile.REQUIRED_IMAGES}
            )
            return real_loader(stderr)

    monkeypatch.setattr(profile, "verify_loaded_images", mapped_loader)
    return paths


def wire_path(path: str) -> str:
    return path if path.startswith("/") else "/synthetic/" + PureWindowsPath(path).name


def test_windows_fixture_path_maps_to_darwin_wire_format() -> None:
    assert wire_path(r"C:\fixture\libllama.dylib") == "/synthetic/libllama.dylib"


@pytest.fixture
def loader_pinned(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    paths = ["/synthetic/" + name for name in ("llama-cli", "libllama.dylib", "libggml-cpu.dylib")]
    monkeypatch.setattr(profile, "PINNED_FILES", dict.fromkeys(paths, "a" * 64))
    monkeypatch.setattr(profile, "REQUIRED_IMAGES", set(paths[:2]))
    return paths


def trace(paths: list[str]) -> bytes:
    return "".join(
        f"dyld[123]: <12345678-1234-1234-1234-123456789ABC> {wire_path(path)}\n" for path in paths
    ).encode()


def process(
    monkeypatch: pytest.MonkeyPatch,
    paths: list[str],
    out: bytes = VERSION_OUTPUT,
    err: bytes | None = None,
    code: int = 0,
    failure: Exception | None = None,
    mutate: Callable[[], object] | None = None,
) -> list[tuple[list[str], RunOptions]]:
    calls: list[tuple[list[str], RunOptions]] = []

    def execute(args: list[str], **kwargs: Unpack[RunOptions]) -> SimpleNamespace:
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


def test_environment_is_fresh_and_minimal(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
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


def test_profile_digest_stable_and_covers_configuration(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
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


def test_verify_files_accepts_exact_bytes(pinned: list[str]) -> None:
    assert profile.verify_files() is None


def test_backend_discovery_directory_rejects_extra_or_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Model Darwin directory enumeration independently of the host path syntax.
    entries = {"/synthetic/libexec/cpu.so"}
    available = True

    class DarwinPath(PurePosixPath):
        def iterdir(self) -> Iterator[DarwinPath]:
            if not available:
                raise FileNotFoundError
            return iter(DarwinPath(name) for name in entries)

        def resolve(self, strict: bool = False) -> DarwinPath:
            del strict
            return self

        def is_file(self) -> bool:
            return str(self) in entries

    monkeypatch.setattr(profile, "Path", DarwinPath)
    monkeypatch.setattr(profile, "LOAD_ALIASES", {})
    monkeypatch.setattr(profile, "PINNED_FILES", {"/synthetic/libexec/cpu.so": "a" * 64})
    monkeypatch.setattr(profile, "_sha256", Mock(return_value="a" * 64))
    profile.verify_files()
    entries.add("/synthetic/libexec/unknown.so")
    with pytest.raises(ValueError, match="profile_backend_inventory_mismatch"):
        profile.verify_files()
    available = False
    with pytest.raises(ValueError, match="profile_backend_directory_unavailable"):
        profile.verify_files()


def test_verify_files_checks_loader_alias_resolution(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
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


def test_verify_files_rejects_absent_loader_alias(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    from pathlib import Path

    alias = Path(pinned[1]).with_name("absent.dylib")
    monkeypatch.setattr(profile, "LOAD_ALIASES", {str(alias): pinned[1]})
    with pytest.raises(ValueError):
        profile.verify_files()


@pytest.mark.parametrize("damage", ["missing", "changed", "symlink", "directory"])
def test_verify_files_rejects_damage(pinned: list[str], damage: str) -> None:
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


def test_loader_accepts_system_and_optional_backend(loader_pinned: list[str]) -> None:
    pinned = loader_pinned
    stderr = trace(
        [
            *pinned,
            pinned[0],
            "/usr/lib/libSystem.B.dylib",
            "/System/Library/Frameworks/Security.framework/Security",
        ]
    )
    assert profile.verify_loaded_images(stderr) == sorted(pinned)


def test_loader_allows_delayed_diagnostic(loader_pinned: list[str]) -> None:
    pinned = loader_pinned
    stderr = trace(pinned) + b"dyld[123]: move delayed to loaded: libggml-cpu.dylib\n"
    assert profile.verify_loaded_images(stderr) == sorted(pinned)


def test_loader_rejects_delayed_image_without_full_record(loader_pinned: list[str]) -> None:
    pinned = loader_pinned
    stderr = trace(pinned[:2]) + b"dyld[123]: move delayed to loaded: libggml-cpu.dylib\n"
    with pytest.raises(ValueError):
        profile.verify_loaded_images(stderr)


def test_loader_allows_runtime_logs_without_treating_them_as_images(
    loader_pinned: list[str],
) -> None:
    pinned = loader_pinned
    stderr = b"runtime: initialising\n" + trace(pinned[:2])
    assert profile.verify_loaded_images(stderr) == sorted(pinned[:2])


def test_loader_accepts_reverse_transition_only_with_full_image(loader_pinned: list[str]) -> None:
    pinned = loader_pinned
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
        b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> C:\\fixture\\llama-cli\n",
        b"\xff",
        b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> /usr/lib/../private/evil.dylib\n",
    ],
)
def test_loader_rejects_malformed_or_unknown(loader_pinned: list[str], extra: bytes) -> None:
    pinned = loader_pinned
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace(pinned) + extra)


@pytest.mark.parametrize("kind", ["none", "missing", "unknown-backend", "fake-system"])
def test_loader_requires_attested_images(loader_pinned: list[str], kind: str) -> None:
    pinned = loader_pinned
    paths = {
        "none": [],
        "missing": pinned[1:],
        "unknown-backend": [*pinned, "/private/libggml-metal.dylib"],
        "fake-system": [*pinned, "/usr/library/evil.dylib"],
    }[kind]
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace(paths))


def test_loader_rejects_mixed_process_evidence(loader_pinned: list[str]) -> None:
    pinned = loader_pinned
    stderr = trace(pinned[:1]) + trace(pinned[1:]).replace(b"dyld[123]", b"dyld[456]")
    with pytest.raises(ValueError):
        profile.verify_loaded_images(stderr)


@pytest.mark.parametrize("suffix", ["/../evil", "//evil", "/./evil", "/evil\x00"])
def test_loader_rejects_noncanonical_system_paths(loader_pinned: list[str], suffix: str) -> None:
    pinned = loader_pinned
    with pytest.raises(ValueError):
        profile.verify_loaded_images(trace([*pinned, "/usr/lib" + suffix]))


def test_capture_success_fixed_invocation(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
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
    assert "raw_stdout_base64" in receipt
    assert isinstance(receipt["raw_stdout_base64"], str)
    assert base64.b64decode(receipt["raw_stdout_base64"]) == VERSION_OUTPUT
    assert "raw_stderr_base64" in receipt
    assert isinstance(receipt["raw_stderr_base64"], str)
    assert base64.b64decode(receipt["raw_stderr_base64"]) == trace(pinned)
    assert "stdout_sha256" in receipt
    assert receipt["stdout_sha256"] == hashlib.sha256(VERSION_OUTPUT).hexdigest()
    assert "stderr_sha256" in receipt
    assert receipt["stderr_sha256"] == hashlib.sha256(trace(pinned)).hexdigest()
    assert "stdout_bytes" in receipt
    assert receipt["stdout_bytes"] == len(VERSION_OUTPUT)
    assert "stderr_bytes" in receipt
    assert receipt["stderr_bytes"] == len(trace(pinned))


@pytest.mark.parametrize(
    ("system", "machine"), [("Linux", "arm64"), ("Darwin", "x86_64"), ("Windows", "AMD64")]
)
def test_capture_unsupported_never_executes(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch, system: str, machine: str
) -> None:
    monkeypatch.setattr(profile.platform, "system", lambda: system)
    monkeypatch.setattr(profile.platform, "machine", lambda: machine)
    receipt = profile.capture_version()
    assert receipt["status"] == "unsupported_platform"
    assert receipt["admitted"] is receipt["study_unlocked"] is False


@pytest.mark.parametrize(
    "damage",
    ["bad-version", "nonzero", "loader", "timeout", "launch", "file-drift", "profile-drift"],
)
def test_capture_fail_closed(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    from pathlib import Path

    options: ProcessOptions = {}
    if damage == "bad-version":
        options["out"] = b"version: 99999 (unknown)\n"
    elif damage == "nonzero":
        options["code"] = 2
    elif damage == "loader":
        options["err"] = trace([*pinned, "/private/unknown.dylib"])
    elif damage == "timeout":
        options["failure"] = subprocess.TimeoutExpired("private-launch", 60)
    elif damage == "launch":
        options["failure"] = OSError("private-launch")
    elif damage == "file-drift":
        options["mutate"] = lambda: Path(pinned[1]).write_bytes(b"changed")
    else:
        options["mutate"] = lambda: monkeypatch.setattr(profile, "LIBRARY_DIRS", ("/changed",))
    process(
        monkeypatch,
        pinned,
        out=options.get("out", VERSION_OUTPUT),
        err=options.get("err"),
        code=options.get("code", 0),
        failure=options.get("failure"),
        mutate=options.get("mutate"),
    )
    receipt = profile.capture_version()
    assert receipt["status"] == "profile_failed"
    assert receipt["admitted"] is receipt["study_unlocked"] is False
    assert "private-launch" not in json.dumps(receipt)


def test_capture_rejects_preexisting_file_damage(pinned: list[str]) -> None:
    from pathlib import Path

    Path(pinned[1]).unlink()
    assert profile.capture_version()["status"] == "profile_failed"


def test_capture_rejects_adapter_digest_drift(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    real_hash = profile._sha256
    adapter_calls: list[Path] = []

    def fake_hash(path: Path) -> str:
        if str(path) == profile.__file__:
            adapter_calls.append(path)
            return "a" * 64 if len(adapter_calls) == 1 else "b" * 64
        return real_hash(path)

    monkeypatch.setattr(profile, "_sha256", fake_hash)
    process(monkeypatch, pinned)
    result = profile.capture_version()
    assert result["status"] == "profile_failed"
    assert "pins_unchanged_after" in result
    assert result["pins_unchanged_after"] is False


def test_capture_exact_output_limit_is_retained(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    out = VERSION_OUTPUT + b" " * (1048576 - len(VERSION_OUTPUT))
    process(monkeypatch, pinned, out=out)
    receipt = profile.capture_version()
    assert receipt["status"] == "runtime_profile_observed"
    assert "raw_stdout_base64" in receipt
    assert isinstance(receipt["raw_stdout_base64"], str)
    assert base64.b64decode(receipt["raw_stdout_base64"]) == out
    assert "stdout_sha256" in receipt
    assert receipt["stdout_sha256"] == hashlib.sha256(out).hexdigest()


@pytest.mark.parametrize("stream", ["out", "err"])
def test_capture_oversize_not_partially_attested(
    pinned: list[str], monkeypatch: pytest.MonkeyPatch, stream: str
) -> None:
    oversized = b"x" * (1048576 + 1)
    if stream == "out":
        process(monkeypatch, pinned, out=oversized)
    else:
        process(monkeypatch, pinned, err=oversized)
    receipt = profile.capture_version()
    assert receipt["status"] == "profile_failed"
    key = "stdout" if stream == "out" else "stderr"
    assert f"raw_{key}_base64" in receipt
    assert receipt.get(f"raw_{key}_base64") is None
    assert f"{key}_sha256" in receipt
    assert receipt.get(f"{key}_sha256") is None
    assert receipt.get(f"{key}_bytes") == 1048577


def test_cli_exclusive_receipt_and_safe_summary(
    pinned: list[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    process(monkeypatch, pinned)
    destination = tmp_path / "receipt.json"
    assert profile.main(["--receipt", str(destination)]) == 0
    original = destination.read_bytes()
    assert json.loads(original)["status"] == "runtime_profile_observed"
    summary_text = capsys.readouterr().out
    assert str(tmp_path) not in summary_text
    assert json.loads(summary_text)["receipt_sha256"] == hashlib.sha256(original).hexdigest()
    assert profile.main(["--receipt", str(destination)]) != 0
    assert destination.read_bytes() == original


def test_cli_write_failure_is_safe(
    pinned: list[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    process(monkeypatch, pinned)
    assert profile.main(["--receipt", str(tmp_path / "missing" / "receipt.json")]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "receipt_write_failed"
    assert str(tmp_path) not in json.dumps(result)


def test_cli_existing_symlink_does_not_execute(pinned: list[str], tmp_path: Path) -> None:
    destination = tmp_path / "receipt.json"
    destination.symlink_to(tmp_path / "absent.json")
    assert profile.main(["--receipt", str(destination)]) == 1
    assert destination.is_symlink()


def test_cli_requires_receipt(pinned: list[str]) -> None:
    with pytest.raises(SystemExit):
        profile.main([])
