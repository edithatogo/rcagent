"""Synthetic process fixtures only; no actual model or network execution."""

import base64
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import BinaryIO, NotRequired, TypeAlias, TypedDict, Unpack

import pytest

from tests.prospective_fixture_types import ObjectMap
from tools import local_output_probe as probe


class ProcessOptions(TypedDict):
    stdin: int
    stdout: BinaryIO
    stderr: BinaryIO
    env: dict[str, str]
    timeout: int
    check: bool
    shell: NotRequired[bool]


class ProcessChanges(TypedDict, total=False):
    out: bytes
    failure: BaseException
    code: int


ProcessCall: TypeAlias = tuple[list[str], ProcessOptions]


@pytest.fixture
def ready(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    admission: probe.prospective_model.CLIModelAdmission = {
        "purpose": "local-artefact-eligibility-only",
        "local_artifact_eligible": True,
        "admitted": False,
        "study_unlocked": False,
        "registry_sha256": "a" * 64,
        "effective_manifest_sha256": "b" * 64,
        "original_runtime": {"name": "synthetic-historical-cli"},
        "runtime_overlay": {
            "name": "synthetic-cli",
            "version": "synthetic",
            "executable": "/synthetic/runtime",
            "executable_sha256": "a" * 64,
            "license": "MIT",
            "distribution": "synthetic",
            "runtime_dependencies": [],
        },
        "model_id": "synthetic-model",
        "model_revision": "c" * 40,
        "model_sha256": "d" * 64,
        "model_license_sha256": "e" * 64,
        "model_path": "/synthetic/model",
        "model_license_path": "/synthetic/LICENSE",
        "admission_sha256": "f" * 64,
    }

    def admit_fixture(_root: Path) -> probe.prospective_model.CLIModelAdmission:
        return admission.copy()

    def loaded_images(_raw: bytes) -> list[str]:
        return ["/synthetic/runtime"]

    monkeypatch.setattr(probe, "admit_model", admit_fixture)
    monkeypatch.setattr(probe, "source_pins", lambda: {"synthetic.py": "a" * 64})
    monkeypatch.setattr(probe.profile, "EXECUTABLE", "/synthetic/runtime")
    monkeypatch.setattr(probe.profile, "profile_digest", lambda: "b" * 64)
    monkeypatch.setattr(probe.profile, "verify_loaded_images", loaded_images)
    monkeypatch.setattr(probe.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(probe.platform, "machine", lambda: "arm64")

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("real execution forbidden")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    return tmp_path


def process(
    monkeypatch: pytest.MonkeyPatch,
    out: bytes = b"synthetic READY",
    err: bytes = b"synthetic loader",
    failure: BaseException | None = None,
    code: int = 0,
    mutate: Callable[[], None] | None = None,
) -> list[ProcessCall]:
    calls: list[ProcessCall] = []

    def run(
        args: list[str], **kwargs: Unpack[ProcessOptions]
    ) -> subprocess.CompletedProcess[bytes]:
        calls.append((args, kwargs))
        kwargs["stdout"].write(out)
        kwargs["stderr"].write(err)
        if mutate:
            mutate()
        if failure:
            raise failure
        return subprocess.CompletedProcess(args, code)

    monkeypatch.setattr(probe.subprocess, "run", run)
    return calls


def test_fixed_invocation_preserves_raw_and_locks(
    ready: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = process(monkeypatch)
    result = probe.run_probe(ready)
    assert result["status"] == "process_completed"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["purpose"] == "output-mode-probe-only"
    assert result["response_only_verified"] is False
    assert isinstance(result["raw_stdout_base64"], str)
    assert isinstance(result["raw_stderr_base64"], str)
    assert base64.b64decode(result["raw_stdout_base64"]) == b"synthetic READY"
    assert base64.b64decode(result["raw_stderr_base64"]) == b"synthetic loader"
    args, options = calls[0]
    assert result["arguments"] == args
    assert args[:5] == ["/synthetic/runtime", "-m", "/synthetic/model", "-p", probe.PROMPT]
    assert args[args.index("-n") + 1] == "16"
    assert args[args.index("-c") + 1] == "512"
    assert "--offline" in args
    assert "--no-escape" in args
    assert options["stdin"] == subprocess.DEVNULL
    assert options["timeout"] == 60
    assert options["env"] == probe.profile.profile_environment()
    assert not options.get("shell", False)


@pytest.mark.parametrize("kind", ["timeout", "launch", "nonzero", "empty", "oversize"])
def test_failed_execution(ready: Path, monkeypatch: pytest.MonkeyPatch, kind: str) -> None:
    kwargs: ProcessChanges = {}
    if kind == "timeout":
        kwargs["failure"] = subprocess.TimeoutExpired("private", 60)
    elif kind == "launch":
        kwargs["failure"] = OSError("private")
    elif kind == "nonzero":
        kwargs["code"] = 2
    elif kind == "empty":
        kwargs["out"] = b""
    else:
        kwargs["out"] = b"x" * (probe.MAX_OUTPUT + 1)
    process(
        monkeypatch,
        out=kwargs.get("out", b"synthetic READY"),
        failure=kwargs.get("failure"),
        code=kwargs.get("code", 0),
    )
    result = probe.run_probe(ready)
    assert result["status"] == "probe_failed"
    assert result["admitted"] is False
    assert "private" not in json.dumps(result)
    if kind == "oversize":
        assert result["raw_stdout_base64"] is result["stdout_sha256"] is None


@pytest.mark.parametrize("kind", ["source", "admission", "profile", "loader", "post-error"])
def test_drift_or_loader_failure(ready: Path, monkeypatch: pytest.MonkeyPatch, kind: str) -> None:
    def fail(*args: object) -> None:
        raise ValueError("synthetic_bad")

    def changed_admission(_root: Path) -> ObjectMap:
        return {"changed": True}

    def mutate() -> None:
        if kind == "source":
            monkeypatch.setattr(probe, "source_pins", lambda: {"synthetic.py": "b" * 64})
        elif kind == "admission":
            monkeypatch.setattr(probe, "admit_model", changed_admission)
        elif kind == "profile":
            monkeypatch.setattr(probe.profile, "profile_digest", lambda: "c" * 64)
        elif kind == "loader":
            monkeypatch.setattr(probe.profile, "verify_loaded_images", fail)
        else:
            monkeypatch.setattr(probe, "admit_model", fail)

    process(monkeypatch, mutate=mutate)
    assert probe.run_probe(ready)["status"] == "probe_failed"


def test_preflight_failure_and_platform(ready: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(probe.platform, "system", lambda: "Windows")
    assert probe.run_probe(ready)["status"] == "unsupported_platform"
    monkeypatch.setattr(probe.platform, "system", lambda: "Darwin")

    def fail(_root: Path) -> None:
        raise ValueError("private admission error")

    monkeypatch.setattr(probe, "admit_model", fail)
    result = probe.run_probe(ready)
    assert result["status"] == "admission_failed"
    assert "private" not in json.dumps(result)


def test_cli_reserves_before_launch(
    ready: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    receipt = ready / "receipt.json"

    def run(_root: Path) -> ObjectMap:
        assert receipt.exists()
        return {"status": "process_completed", "admitted": False, "study_unlocked": False}

    monkeypatch.setattr(probe, "run_probe", run)
    args = ["--model-root", str(ready), "--receipt", str(receipt)]
    assert probe.main(args) == 0
    assert json.loads(receipt.read_text())["admitted"] is False
    assert "receipt_sha256" in json.loads(capsys.readouterr().out)
    assert probe.main(args) == 1


@pytest.mark.parametrize("kind", ["missing-parent", "dangling", "directory", "parent-link"])
def test_cli_invalid_destination_never_launches(
    ready: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    receipt = ready / "receipt.json"
    if kind == "missing-parent":
        receipt = ready / "missing" / "receipt.json"
    elif kind == "dangling":
        receipt.symlink_to(ready / "missing.json")
    elif kind == "directory":
        receipt.mkdir()
    else:
        link = ready / "link"
        link.symlink_to(ready, target_is_directory=True)
        receipt = link / "receipt.json"
    assert probe.main(["--model-root", str(ready), "--receipt", str(receipt)]) == 1


def test_source_pins_cover_implementation() -> None:
    result = probe.source_pins()
    assert set(result) == {
        "local_output_probe.py",
        "darwin_runtime_v030.py",
        "darwin_runtime_profile.py",
        "prospective_model.py",
        "local_model_comparator.py",
        "json_shapes.py",
    }
    assert all(len(value) == 64 for value in result.values())


def test_source_module_without_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(probe.profile, "__file__", None)
    with pytest.raises(ValueError, match="source_file_unavailable"):
        probe.source_pins()


def test_shape_guard_change_changes_its_source_pin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    guard = tmp_path / "json_shapes.py"
    guard.write_bytes(b"synthetic first guard")
    monkeypatch.setattr(probe.json_shapes, "__file__", str(guard))
    before = probe.source_pins()
    guard.write_bytes(b"synthetic changed guard")
    after = probe.source_pins()
    assert before["json_shapes.py"] != after["json_shapes.py"]
    assert {key: value for key, value in before.items() if key != "json_shapes.py"} == {
        key: value for key, value in after.items() if key != "json_shapes.py"
    }


def test_cli_failed_probe_retained(
    ready: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def failed_probe(_root: Path) -> ObjectMap:
        return {"status": "probe_failed"}

    monkeypatch.setattr(probe, "run_probe", failed_probe)
    receipt = ready / "failed.json"
    assert probe.main(["--model-root", str(ready), "--receipt", str(receipt)]) == 1
    assert json.loads(receipt.read_text())["status"] == "probe_failed"
    assert json.loads(capsys.readouterr().out)["study_unlocked"] is False
