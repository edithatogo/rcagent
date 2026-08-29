from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.evidence_ports import Operation
from tools.sourceright_adapter import SourceRightAdapter


def operation(privacy_mode: str = "fully_local") -> Operation:
    return Operation("operation-01", 2.0, "idempotency-01", privacy_mode)


def test_adapter_is_fail_closed_when_unavailable(tmp_path: Path) -> None:
    adapter = SourceRightAdapter(tmp_path / "missing")
    assert not adapter.capabilities()[0].available
    result = adapter.run_json(operation(), ["bench", "--json"])
    assert result.status == "unavailable"
    assert not result.retryable


def test_adapter_accepts_only_local_profiles_and_json_contract(tmp_path: Path) -> None:
    executable = tmp_path / "sourceright"
    executable.touch()
    executable.chmod(0o700)

    def runner(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 0, json.dumps({"status": "pass"}), "")

    adapter = SourceRightAdapter(executable, runner=runner)
    assert adapter.run_json(operation("public_remote"), ["bench", "--json"]).status == "rejected"
    assert adapter.run_json(operation(), ["bench", "--json"]).payload == {"status": "pass"}
    assert adapter.run_json(operation(), ["citation-sync", "--apply"]).status == "rejected"


def test_adapter_classifies_timeout_failure_and_invalid_json(tmp_path: Path) -> None:
    executable = tmp_path / "sourceright"
    executable.touch()
    executable.chmod(0o700)

    def timeout(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired("sourceright", 2)

    assert SourceRightAdapter(executable, timeout).run_json(operation(), ["bench"]).status == "timeout"

    def failure(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 2, "", "fixture failure")

    assert SourceRightAdapter(executable, failure).run_json(operation(), ["bench"]).status == "failed"

    def invalid(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 0, "[]", "")

    result = SourceRightAdapter(executable, invalid).run_json(operation(), ["bench"])
    assert result.status == "failed"
    assert result.diagnostic == "unexpected SourceRight payload"

    def malformed(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], 0, "not-json", "")

    result = SourceRightAdapter(executable, malformed).run_json(operation(), ["bench"])
    assert result.status == "failed"
    assert result.diagnostic == "invalid SourceRight JSON"


def test_adapter_rejects_invalid_timeout_and_handles_execution_error(tmp_path: Path) -> None:
    executable = tmp_path / "sourceright"
    executable.touch()
    executable.chmod(0o700)

    invalid_timeout = Operation("operation-01", 0, "idempotency-01", "fully_local")
    result = SourceRightAdapter(executable).run_json(invalid_timeout, ["bench"])
    assert result.status == "rejected"
    assert result.diagnostic == "timeout must be finite and greater than zero"

    def unavailable(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise OSError("synthetic execution failure")

    result = SourceRightAdapter(executable, unavailable).run_json(operation(), ["bench"])
    assert result.status == "unavailable"
    assert result.diagnostic == "SourceRight execution unavailable: synthetic execution failure"
