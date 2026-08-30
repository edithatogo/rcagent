"""Synthetic process fixtures only; no actual model or network execution."""

import base64
import json
import subprocess

import pytest

from tools import local_output_probe as probe


@pytest.fixture
def ready(tmp_path, monkeypatch):
    admission = {
        "registry_sha256": "a" * 64,
        "effective_manifest_sha256": "b" * 64,
        "runtime_overlay": {"executable": "/synthetic/runtime"},
        "model_id": "synthetic-model",
        "model_revision": "c" * 40,
        "model_sha256": "d" * 64,
        "model_license_sha256": "e" * 64,
        "model_path": "/synthetic/model",
        "model_license_path": "/synthetic/LICENSE",
        "admission_sha256": "f" * 64,
    }
    monkeypatch.setattr(probe, "admit_model", lambda root: admission.copy())
    monkeypatch.setattr(probe, "source_pins", lambda: {"synthetic.py": "a" * 64})
    monkeypatch.setattr(probe.profile, "EXECUTABLE", "/synthetic/runtime")
    monkeypatch.setattr(probe.profile, "profile_digest", lambda: "b" * 64)
    monkeypatch.setattr(probe.profile, "verify_loaded_images", lambda err: ["/synthetic/runtime"])
    monkeypatch.setattr(probe.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(probe.platform, "machine", lambda: "arm64")

    def forbidden(*args, **kwargs):
        raise AssertionError("real execution forbidden")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    return tmp_path


def process(
    monkeypatch, out=b"synthetic READY", err=b"synthetic loader", failure=None, code=0, mutate=None
):
    calls = []

    def run(args, **kwargs):
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


def test_fixed_invocation_preserves_raw_and_locks(ready, monkeypatch):
    calls = process(monkeypatch)
    result = probe.run_probe(ready)
    assert result["status"] == "process_completed"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["purpose"] == "output-mode-probe-only"
    assert result["response_only_verified"] is False
    assert base64.b64decode(result["raw_stdout_base64"]) == b"synthetic READY"
    assert base64.b64decode(result["raw_stderr_base64"]) == b"synthetic loader"
    args, options = calls[0]
    assert result["arguments"] == args
    assert args[:5] == ["/synthetic/runtime", "-m", "/synthetic/model", "-p", probe.PROMPT]
    assert args[args.index("-n") + 1] == "16"
    assert args[args.index("-c") + 1] == "512"
    assert "--offline" in args and "--no-escape" in args
    assert options["stdin"] == subprocess.DEVNULL
    assert options["timeout"] == 60
    assert options["env"] == probe.profile.profile_environment()
    assert not options.get("shell", False)


@pytest.mark.parametrize("kind", ["timeout", "launch", "nonzero", "empty", "oversize"])
def test_failed_execution(ready, monkeypatch, kind):
    kwargs = {}
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
    process(monkeypatch, **kwargs)
    result = probe.run_probe(ready)
    assert result["status"] == "probe_failed"
    assert result["admitted"] is False
    assert "private" not in json.dumps(result)
    if kind == "oversize":
        assert result["raw_stdout_base64"] is result["stdout_sha256"] is None


@pytest.mark.parametrize("kind", ["source", "admission", "profile", "loader", "post-error"])
def test_drift_or_loader_failure(ready, monkeypatch, kind):
    def fail(*args):
        raise ValueError("synthetic_bad")

    def mutate():
        if kind == "source":
            monkeypatch.setattr(probe, "source_pins", lambda: {"synthetic.py": "b" * 64})
        elif kind == "admission":
            monkeypatch.setattr(probe, "admit_model", lambda root: {"changed": True})
        elif kind == "profile":
            monkeypatch.setattr(probe.profile, "profile_digest", lambda: "c" * 64)
        elif kind == "loader":
            monkeypatch.setattr(probe.profile, "verify_loaded_images", fail)
        else:
            monkeypatch.setattr(probe, "admit_model", fail)

    process(monkeypatch, mutate=mutate)
    assert probe.run_probe(ready)["status"] == "probe_failed"


def test_preflight_failure_and_platform(ready, monkeypatch):
    monkeypatch.setattr(probe.platform, "system", lambda: "Windows")
    assert probe.run_probe(ready)["status"] == "unsupported_platform"
    monkeypatch.setattr(probe.platform, "system", lambda: "Darwin")

    def fail(root):
        raise ValueError("private admission error")

    monkeypatch.setattr(probe, "admit_model", fail)
    result = probe.run_probe(ready)
    assert result["status"] == "admission_failed"
    assert "private" not in json.dumps(result)


def test_cli_reserves_before_launch(ready, monkeypatch, capsys):
    receipt = ready / "receipt.json"

    def run(root):
        assert receipt.exists()
        return {"status": "process_completed", "admitted": False, "study_unlocked": False}

    monkeypatch.setattr(probe, "run_probe", run)
    args = ["--model-root", str(ready), "--receipt", str(receipt)]
    assert probe.main(args) == 0
    assert json.loads(receipt.read_text())["admitted"] is False
    assert "receipt_sha256" in json.loads(capsys.readouterr().out)
    assert probe.main(args) == 1


@pytest.mark.parametrize("kind", ["missing-parent", "dangling", "directory", "parent-link"])
def test_cli_invalid_destination_never_launches(ready, monkeypatch, kind):
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


def test_source_pins_cover_implementation():
    result = probe.source_pins()
    assert set(result) == {
        "local_output_probe.py",
        "darwin_runtime_v030.py",
        "darwin_runtime_profile.py",
        "prospective_model.py",
        "local_model_comparator.py",
    }
    assert all(len(value) == 64 for value in result.values())


def test_source_module_without_file(monkeypatch):
    monkeypatch.setattr(probe.profile, "__file__", None)
    with pytest.raises(ValueError, match="source_file_unavailable"):
        probe.source_pins()


def test_cli_failed_probe_retained(ready, monkeypatch, capsys):
    monkeypatch.setattr(probe, "run_probe", lambda root: {"status": "probe_failed"})
    receipt = ready / "failed.json"
    assert probe.main(["--model-root", str(ready), "--receipt", str(receipt)]) == 1
    assert json.loads(receipt.read_text())["status"] == "probe_failed"
    assert json.loads(capsys.readouterr().out)["study_unlocked"] is False
