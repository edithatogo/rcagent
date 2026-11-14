"""Synthetic tests for non-study local execution capture; never execute a model."""

import base64
import hashlib
import json
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import BinaryIO, Literal, Never, TypeAlias, TypedDict, Unpack

import pytest

from tools import json_shapes
from tools import local_execution_probe as probe
from tools.local_execution_probe import run_probe
from tools.local_model_comparator import _sha256 as file_hash

Admitted: TypeAlias = tuple[Path, Path, Path]


class ProcessOptions(TypedDict):
    stdin: int
    stdout: BinaryIO
    stderr: BinaryIO
    env: dict[str, str]
    timeout: int
    check: Literal[False]


ProcessCall: TypeAlias = tuple[list[str], ProcessOptions]


@pytest.fixture
def admitted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Admitted:
    runtime = tmp_path / "private-runtime"
    runtime.write_bytes(b"synthetic-runtime")
    root = tmp_path / "private-models"
    models: list[dict[str, object]] = []
    for size in ("small", "medium", "larger"):
        directory = root / size
        directory.mkdir(parents=True)
        licence = directory / "LICENSE"
        licence.write_bytes(b"synthetic-license")
        weights = directory / "model.gguf"
        weights.write_bytes(size.encode())
        models.append(
            {
                "id": probe.MODEL_ID if size == "small" else size,
                "revision": "a" * 40,
                "size_class": size,
                "license": "Apache-2.0",
                "admission_status": "admitted_local_research_only",
                "cache_subdirectory": size,
                "license_sha256": file_hash(licence),
                "files": [
                    {
                        "path": weights.name,
                        "bytes": weights.stat().st_size,
                        "sha256": file_hash(weights),
                    }
                ],
            }
        )
    manifest: dict[str, object] = {
        "admission_policy": {
            "data_class": "synthetic_only",
            "network": "disabled",
            **dict.fromkeys(
                (
                    "external_inference",
                    "remote_code",
                    "telemetry",
                    "redistribution",
                    "publication",
                    "promotion_eligible",
                ),
                False,
            ),
        },
        "runtime": {
            "executable": str(runtime),
            "executable_sha256": file_hash(runtime),
            "license": "MIT",
            "version": "synthetic-test-version",
        },
        "models": models,
    }
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(manifest))
    monkeypatch.setattr(probe, "MANIFEST_PATH", registry)
    monkeypatch.setattr(probe, "REGISTRY_PIN", file_hash(registry))

    # No test is allowed to fall through to a real subprocess.
    def forbidden(*_args: object, **_kwargs: object) -> Never:
        raise AssertionError("model execution is forbidden in tests")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    return root, runtime, registry


def install_process(
    monkeypatch: pytest.MonkeyPatch,
    out: bytes = b"READY",
    err: bytes = b"",
    code: int = 0,
    failure: BaseException | None = None,
    mutate: Callable[[], None] | None = None,
) -> list[ProcessCall]:
    calls: list[ProcessCall] = []

    def execute(args: list[str], **kwargs: Unpack[ProcessOptions]) -> SimpleNamespace:
        calls.append((args, kwargs))
        kwargs["stdout"].write(out)
        kwargs["stderr"].write(err)
        if mutate:
            mutate()
        if failure:
            raise failure
        return SimpleNamespace(returncode=code)

    monkeypatch.setattr(probe.subprocess, "run", execute)
    return calls


@pytest.fixture
def profiled(admitted: Admitted, monkeypatch: pytest.MonkeyPatch) -> bytes:
    from tools import darwin_runtime_profile as profile

    _, runtime, _ = admitted
    name = str(runtime.resolve())
    monkeypatch.setattr(profile, "EXECUTABLE", name)
    monkeypatch.setattr(profile, "PINNED_FILES", {name: file_hash(runtime)})
    monkeypatch.setattr(profile, "REQUIRED_IMAGES", {name})
    monkeypatch.setattr(profile, "LOAD_ALIASES", {})
    monkeypatch.setattr(profile.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(profile.platform, "machine", lambda: "arm64")
    # The real temporary file verifies host filesystem behaviour; the loader
    # wire format remains Darwin/POSIX even when this test runs on Windows.
    wire_name = "/synthetic-darwin/private-runtime"
    verify_loaded_images = profile.verify_loaded_images

    def verify_trace(stderr: bytes) -> list[str]:
        with monkeypatch.context() as patch:
            patch.setattr(profile, "PINNED_FILES", {wire_name: file_hash(runtime)})
            patch.setattr(profile, "REQUIRED_IMAGES", {wire_name})
            return verify_loaded_images(stderr)

    monkeypatch.setattr(profile, "verify_loaded_images", verify_trace)
    return f"dyld[123]: <12345678-1234-1234-1234-123456789ABC> {wire_name}\n".encode()


def test_profiled_probe_captures_verified_loader(
    admitted: Admitted, profiled: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tools import darwin_runtime_profile as profile

    root, runtime, _ = admitted
    calls = install_process(monkeypatch, b"READY", profiled)
    result = run_probe(root, runtime, dependency_profile=True)
    assert result["status"] == "process_completed"
    assert "dependency_profile" in result
    dependency = result["dependency_profile"]
    assert dependency["status"] == "observed"
    assert dependency["profile_sha256"] == profile.profile_digest()
    raw_stderr = dependency["raw_stderr_base64"]
    assert isinstance(raw_stderr, str)
    assert base64.b64decode(raw_stderr) == profiled
    assert calls[0][1]["env"] == profile.profile_environment()
    assert result["study_unlocked"] is result["admitted"] is False


@pytest.mark.parametrize("damage", ["missing-trace", "new-image", "drift", "oversized"])
def test_profiled_probe_fails_closed(
    admitted: Admitted, profiled: bytes, monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    from tools import darwin_runtime_profile as profile

    root, runtime, _ = admitted
    err = b"" if damage == "missing-trace" else profiled
    if damage == "new-image":
        err += b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> /private/evil.so\n"
    if damage == "oversized":
        err = b"x" * (profile.MAX_OUTPUT + 1)
    mutate = (
        (lambda: profile.PINNED_FILES.update({str(runtime.resolve()): "0" * 64}))
        if damage == "drift"
        else None
    )
    install_process(monkeypatch, b"READY", err, mutate=mutate)
    result = run_probe(root, runtime, dependency_profile=True)
    assert result["status"] == "probe_failed"
    assert result["study_unlocked"] is False


def test_profiled_probe_checks_before_execution(
    admitted: Admitted, profiled: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tools import darwin_runtime_profile as profile

    root, runtime, _ = admitted
    monkeypatch.setattr(profile, "EXECUTABLE", "/wrong-runtime")
    result = run_probe(root, runtime, dependency_profile=True)
    assert result["status"] == "admission_failed"
    assert result["execution_observed"] is False


def test_profiled_probe_unsupported_host(
    admitted: Admitted, profiled: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, runtime, _ = admitted
    monkeypatch.setattr(probe.platform, "system", lambda: "Linux")
    assert run_probe(root, runtime, dependency_profile=True)["status"] == "admission_failed"


def test_profiled_probe_profile_digest_drift(
    admitted: Admitted, profiled: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tools import darwin_runtime_profile as profile

    root, runtime, _ = admitted
    install_process(
        monkeypatch,
        err=profiled,
        mutate=lambda: monkeypatch.setattr(profile, "LIBRARY_DIRS", ("/changed",)),
    )
    assert run_probe(root, runtime, dependency_profile=True)["status"] == "probe_failed"


def test_profiled_cli_local_receipt_only(
    admitted: Admitted,
    profiled: bytes,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root, runtime, _ = admitted
    install_process(monkeypatch, err=profiled)
    path = tmp_path / "receipt.json"
    args = [
        "--model-root",
        str(root),
        "--runtime-path",
        str(runtime),
        "--dependency-profile",
        "--receipt",
        str(path),
    ]
    assert probe.main(args) == 0
    data = path.read_bytes()
    summary = json.loads(capsys.readouterr().out)
    assert summary["receipt_sha256"] == hashlib.sha256(data).hexdigest()
    assert "raw_stderr_base64" not in summary

    def no_rerun(*_args: object, **_kwargs: object) -> Never:
        pytest.fail("no rerun")

    monkeypatch.setattr(probe, "run_probe", no_rerun)
    assert probe.main(args) == 1
    assert path.read_bytes() == data


def test_cli_unwritable_receipt_fails(
    admitted: Admitted,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root, _, _ = admitted
    install_process(monkeypatch)
    assert (
        probe.main(["--model-root", str(root), "--receipt", str(tmp_path / "missing/out.json")])
        == 1
    )
    assert json.loads(capsys.readouterr().out)["status"] == "receipt_write_failed"


def test_admission_failure_never_executes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def reject_admission(*_args: object) -> Never:
        raise ValueError("admission_failed")

    def reject_execution(*_args: object, **_kwargs: object) -> Never:
        raise AssertionError("must not execute")

    monkeypatch.setattr("tools.local_execution_probe._admission", reject_admission)
    monkeypatch.setattr("tools.local_execution_probe.subprocess.run", reject_execution)
    result = run_probe(tmp_path)
    assert result["status"] == "admission_failed"
    assert result["study_unlocked"] is False
    assert result["execution_observed"] is False


def test_fixed_invocation_and_binary_receipt(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, runtime, _ = admitted
    monkeypatch.setenv("SECRET_API_TOKEN", "must-not-inherit")
    out, err = b"READY\xff\x00\r\n", b"private-stderr\xff"
    calls = install_process(monkeypatch, out, err)
    result = run_probe(root)
    args, kwargs = calls[0]
    assert args == [
        str(runtime),
        "-m",
        str(root / "small/model.gguf"),
        "-p",
        probe.PROMPT,
        "-n",
        "16",
        "--seed",
        "42",
        "--temp",
        "0",
        "--no-display-prompt",
        "--log-disable",
        "--single-turn",
    ]
    assert kwargs["env"] == {"PATH": os.defpath, "LANG": "C"}
    assert kwargs["stdin"] == subprocess.DEVNULL
    assert kwargs["timeout"] == 60
    assert kwargs["check"] is False
    assert result["status"] == "process_completed"
    assert result["execution_observed"] is True
    assert result["study_unlocked"] is result["admitted"] is False
    assert result["pins_unchanged_after"] is result["output_complete"] is True
    assert result["stdout_base64"] == base64.b64encode(out).decode("ascii")
    assert result["stdout_sha256"] == hashlib.sha256(out).hexdigest()
    assert result["stderr_sha256"] == hashlib.sha256(err).hexdigest()
    assert result["stdout_bytes"] == len(out)
    assert result["stderr_bytes"] == len(err)
    assert result["elapsed_ns"] >= 0
    assert result["quantisation"] == "Q4_K_M"
    assert set(result["device"]) == {"system", "release", "machine", "python"}
    assert all(isinstance(value, str) for value in result["device"].values())
    assert result["started_at"] <= result["finished_at"]
    assert str(root.parent) not in json.dumps(result)
    assert "private-stderr" not in json.dumps(result)
    assert result["arguments_without_local_paths"][0:3] == [
        "<pinned-runtime>",
        "-m",
        "<pinned-model>",
    ]


@pytest.mark.parametrize("damage", ["pin", "runtime", "model", "licence", "missing-registry"])
def test_admission_rejects_before_process(admitted: Admitted, damage: str) -> None:
    root, runtime, registry = admitted
    if damage == "pin":
        registry.write_bytes(registry.read_bytes() + b" ")
    elif damage == "missing-registry":
        registry.unlink()
    elif damage == "runtime":
        runtime.write_bytes(b"changed")
    elif damage == "model":
        (root / "larger/model.gguf").write_bytes(b"changed")
    else:
        (root / "medium/LICENSE").unlink()
    assert run_probe(root)["status"] == "admission_failed"


@pytest.mark.parametrize("field", ["runtime-version", "model-revision", "model-id"])
@pytest.mark.parametrize("value", [None, [], True])
def test_invalid_metadata_cannot_cross_admission(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch, field: str, value: object
) -> None:
    root, _, registry = admitted
    parsed: object = json.loads(registry.read_bytes())
    manifest = json_shapes.require_object(parsed, context="synthetic manifest")
    if field == "runtime-version":
        runtime = json_shapes.require_object(manifest["runtime"], context="synthetic runtime")
        runtime["version"] = value
    else:
        models = manifest["models"]
        assert json_shapes.is_array(models)
        selected = json_shapes.require_object(models[0], context="synthetic model")
        selected["revision" if field == "model-revision" else "id"] = value
    # The existing rights/file validator does not validate these metadata types.
    assert probe.validate_admission(manifest, root) == []
    registry.write_text(json.dumps(manifest))
    monkeypatch.setattr(probe, "REGISTRY_PIN", hashlib.sha256(registry.read_bytes()).hexdigest())
    result = run_probe(root)
    assert result["status"] == "admission_failed"
    assert result["execution_observed"] is False


def test_missing_selected_model_cannot_cross_admission(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _, registry = admitted
    parsed: object = json.loads(registry.read_bytes())
    manifest = json_shapes.require_object(parsed, context="synthetic manifest")
    models = manifest["models"]
    assert json_shapes.is_array(models)
    selected = json_shapes.require_object(models[0], context="synthetic model")
    selected["id"] = "other"
    assert probe.validate_admission(manifest, root) == []
    registry.write_text(json.dumps(manifest))
    monkeypatch.setattr(probe, "REGISTRY_PIN", hashlib.sha256(registry.read_bytes()).hexdigest())
    result = run_probe(root)
    assert result["status"] == "admission_failed"
    assert result["execution_observed"] is False


def test_relocation_preserves_hash_and_registry(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, runtime, registry = admitted
    original = registry.read_bytes()
    relocated = runtime.with_name("relocated")
    relocated.write_bytes(runtime.read_bytes())
    runtime.unlink()
    calls = install_process(monkeypatch)
    assert run_probe(root, relocated)["status"] == "process_completed"
    assert calls[0][0][0] == str(relocated.resolve())
    assert registry.read_bytes() == original
    relocated.write_bytes(b"wrong runtime")
    assert run_probe(root, relocated)["status"] == "admission_failed"
    relocated.unlink()
    assert run_probe(root, relocated)["status"] == "admission_failed"
    assert len(calls) == 1


@pytest.mark.parametrize(
    ("out", "code", "failure", "exit_state", "observed"),
    [
        (b"", 0, None, 0, True),
        (b"READY", 3, None, 3, True),
        (b"partial", 0, subprocess.TimeoutExpired("redacted", 60), "timeout", True),
        (b"", 0, OSError("private-launch-path"), "launch_failed", False),
    ],
)
def test_failed_execution(
    admitted: Admitted,
    monkeypatch: pytest.MonkeyPatch,
    out: bytes,
    code: int,
    failure: BaseException | None,
    exit_state: int | str,
    observed: bool,
) -> None:
    install_process(monkeypatch, out=out, code=code, failure=failure)
    result = run_probe(admitted[0])
    assert result["status"] == "probe_failed"
    assert result["exit_state"] == exit_state
    assert result["execution_observed"] is observed
    assert result["admitted"] is result["study_unlocked"] is False
    assert "private-launch-path" not in json.dumps(result)


@pytest.mark.parametrize("stream", ["stdout", "stderr"])
def test_oversize_evidence_has_no_partial_hash(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch, stream: Literal["stdout", "stderr"]
) -> None:
    install_process(
        monkeypatch,
        out=b"x" * (probe.MAX_OUTPUT + 1) if stream == "stdout" else b"READY",
        err=b"x" * (probe.MAX_OUTPUT + 1) if stream == "stderr" else b"",
    )
    result = run_probe(admitted[0])
    assert result["status"] == "probe_failed"
    assert result["output_complete"] is False
    observed_bytes = result["stdout_bytes"] if stream == "stdout" else result["stderr_bytes"]
    assert observed_bytes == probe.MAX_OUTPUT + 1
    assert result["stdout_base64"] is result["stdout_sha256"] is result["stderr_sha256"] is None


@pytest.mark.parametrize("target", ["runtime", "model", "registry", "adapter", "missing"])
def test_postrun_drift_fails(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch, target: str
) -> None:
    root, runtime, registry = admitted

    def mutate() -> None:
        if target == "adapter":
            original_sha = file_hash

            def changed_sha(path: Path) -> str:
                return "0" * 64 if path == Path(probe.__file__) else original_sha(path)

            monkeypatch.setattr(probe, "_sha256", changed_sha)
        elif target == "missing":
            runtime.unlink()
        else:
            path = {"runtime": runtime, "model": root / "small/model.gguf", "registry": registry}[
                target
            ]
            path.write_bytes(b"changed")

    install_process(monkeypatch, mutate=mutate)
    result = run_probe(root)
    assert result["status"] == "probe_failed"
    assert result["pins_unchanged_after"] is False


def test_cli_success_and_error(
    admitted: Admitted, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root, runtime, _ = admitted
    install_process(monkeypatch)
    assert probe.main(["--model-root", str(root), "--runtime-path", str(runtime)]) == 0
    assert json.loads(capsys.readouterr().out)["study_unlocked"] is False
    runtime.unlink()
    assert probe.main(["--model-root", str(root)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "admission_failed"
    with pytest.raises(SystemExit) as exc:
        probe.main([])
    assert exc.value.code == 2
