"""Synthetic tests for non-study local execution capture; never execute a model."""

import base64
import hashlib
import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import local_execution_probe as probe
from tools.local_execution_probe import run_probe


@pytest.fixture
def admitted(tmp_path, monkeypatch):
    runtime = tmp_path / "private-runtime"
    runtime.write_bytes(b"synthetic-runtime")
    root = tmp_path / "private-models"
    models = []
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
                "license_sha256": probe._sha256(licence),
                "files": [
                    {
                        "path": weights.name,
                        "bytes": weights.stat().st_size,
                        "sha256": probe._sha256(weights),
                    }
                ],
            }
        )
    manifest = {
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
            "executable_sha256": probe._sha256(runtime),
            "license": "MIT",
            "version": "synthetic-test-version",
        },
        "models": models,
    }
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(manifest))
    monkeypatch.setattr(probe, "MANIFEST_PATH", registry)
    monkeypatch.setattr(probe, "REGISTRY_PIN", probe._sha256(registry))

    # No test is allowed to fall through to a real subprocess.
    def forbidden(*args, **kwargs):
        raise AssertionError("model execution is forbidden in tests")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    return root, runtime, registry


def install_process(monkeypatch, out=b"READY", err=b"", code=0, failure=None, mutate=None):
    calls = []

    def execute(args, **kwargs):
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


def test_admission_failure_never_executes(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "tools.local_execution_probe._admission",
        lambda *args: (_ for _ in ()).throw(ValueError("admission_failed")),
    )
    monkeypatch.setattr(
        "tools.local_execution_probe.subprocess.run",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not execute")),
    )
    result = run_probe(tmp_path)
    assert result["status"] == "admission_failed"
    assert result["study_unlocked"] is False
    assert result["execution_observed"] is False


def test_fixed_invocation_and_binary_receipt(admitted, monkeypatch):
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
def test_admission_rejects_before_process(admitted, damage):
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


def test_relocation_preserves_hash_and_registry(admitted, monkeypatch):
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
    "out,code,failure,exit_state,observed",
    [
        (b"", 0, None, 0, True),
        (b"READY", 3, None, 3, True),
        (b"partial", 0, subprocess.TimeoutExpired("redacted", 60), "timeout", True),
        (b"", 0, OSError("private-launch-path"), "launch_failed", False),
    ],
)
def test_failed_execution(admitted, monkeypatch, out, code, failure, exit_state, observed):
    install_process(monkeypatch, out=out, code=code, failure=failure)
    result = run_probe(admitted[0])
    assert result["status"] == "probe_failed"
    assert result["exit_state"] == exit_state
    assert result["execution_observed"] is observed
    assert result["admitted"] is result["study_unlocked"] is False
    assert "private-launch-path" not in json.dumps(result)


@pytest.mark.parametrize("stream", ["stdout", "stderr"])
def test_oversize_evidence_has_no_partial_hash(admitted, monkeypatch, stream):
    install_process(
        monkeypatch,
        out=b"x" * (probe.MAX_OUTPUT + 1) if stream == "stdout" else b"READY",
        err=b"x" * (probe.MAX_OUTPUT + 1) if stream == "stderr" else b"",
    )
    result = run_probe(admitted[0])
    assert result["status"] == "probe_failed"
    assert result["output_complete"] is False
    assert result[stream + "_bytes"] == probe.MAX_OUTPUT + 1
    assert result["stdout_base64"] is result["stdout_sha256"] is result["stderr_sha256"] is None


@pytest.mark.parametrize("target", ["runtime", "model", "registry", "adapter", "missing"])
def test_postrun_drift_fails(admitted, monkeypatch, target):
    root, runtime, registry = admitted

    def mutate():
        if target == "adapter":
            original_sha = probe._sha256
            monkeypatch.setattr(
                probe,
                "_sha256",
                lambda path: "0" * 64 if path == Path(probe.__file__) else original_sha(path),
            )
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


def test_cli_success_and_error(admitted, monkeypatch, capsys):
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
