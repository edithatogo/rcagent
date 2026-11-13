from __future__ import annotations

import importlib.metadata
import json
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

import pytest

from tools.run_skill_conformance import (
    ValidatorProvenance,
    run_conformance,
    validator_provenance,
)
from tools.validate_skill_profile import TRACK


def _patch_provenance(monkeypatch: pytest.MonkeyPatch, *, verified: bool) -> None:
    def provenance(_root: Path) -> ValidatorProvenance:
        return {"verified": verified}

    monkeypatch.setattr("tools.run_skill_conformance.validator_provenance", provenance)


@pytest.fixture(autouse=True)
def verified_validator(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_provenance(monkeypatch, verified=True)


def _patch_checks(
    monkeypatch: pytest.MonkeyPatch,
    *,
    current: object = True,
    drift_code: int = 0,
    drift_status: str | None = None,
    profile_errors: list[str] | None = None,
) -> None:
    def validate(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0)

    def profile(_root: Path, *, require_complete: bool) -> list[str]:
        return [] if profile_errors is None else profile_errors

    def drift(_baseline_path: Path, *, offline: bool) -> tuple[int, dict[str, object]]:
        receipt = {"current_conformance": current}
        if drift_status is not None:
            receipt["status"] = drift_status
        return drift_code, receipt

    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", validate)
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", profile)
    monkeypatch.setattr("tools.run_skill_conformance.check_drift", drift)


@dataclass(frozen=True)
class _Distribution:
    direct_url: str

    def read_text(self, filename: str) -> str:
        assert filename == "direct_url.json"
        return self.direct_url


def _patch_distribution(monkeypatch: pytest.MonkeyPatch, text: str) -> None:
    def distribution(name: str) -> _Distribution:
        assert name == "skills-ref"
        return _Distribution(text)

    monkeypatch.setattr("tools.run_skill_conformance.importlib.metadata.distribution", distribution)


def test_live_conformance_requires_all_checks(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _patch_checks(monkeypatch)
    code, receipt = run_conformance(tmp_path)
    assert code == 0
    assert receipt["current_conformance"] is True


def test_offline_receipt_never_claims_current(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _patch_checks(monkeypatch, current=False)
    code, receipt = run_conformance(tmp_path, offline=True)
    assert code == 0
    assert receipt["local_validation_passed"] is True
    assert receipt["current_conformance"] is False


def test_offline_invalid_baseline_returns_nonzero(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _patch_checks(monkeypatch, current=False, drift_code=2, drift_status="baseline_invalid")
    code, receipt = run_conformance(tmp_path, offline=True)
    assert code == 1
    assert receipt["current_conformance"] is False


def test_profile_failure_returns_nonzero(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _patch_checks(monkeypatch, profile_errors=["RCA-PROFILE-004"])
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["project_profile"]["diagnostics"] == ["RCA-PROFILE-004"]


def test_missing_official_validator_is_a_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def missing(*_args: object, **_kwargs: object) -> NoReturn:
        raise FileNotFoundError("skills-ref")

    _patch_checks(monkeypatch)
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", missing)
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["official_validator"]["exit_code"] == 127


def test_custom_validator_cannot_certify_current(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _patch_checks(monkeypatch)
    code, receipt = run_conformance(tmp_path, validator="always-success")
    assert code == 1
    assert receipt["current_conformance"] is False
    assert receipt["official_validator"]["provenance"]["verified"] is False


def test_incomplete_profile_cannot_certify_current(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def incomplete_profile(_root: Path, *, require_complete: bool) -> list[str]:
        return ["pending"] if require_complete else []

    _patch_checks(monkeypatch)
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", incomplete_profile)
    code, receipt = run_conformance(tmp_path, require_complete=False)
    assert code == 1
    assert receipt["local_validation_passed"] is True
    assert receipt["project_profile"]["complete"] is False


def test_validator_timeout_fails_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def timeout(*_args: object, **kwargs: object) -> NoReturn:
        assert kwargs["timeout"] == 60
        raise subprocess.TimeoutExpired("validator", 60)

    _patch_checks(monkeypatch)
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", timeout)
    assert run_conformance(tmp_path)[0] == 1


@pytest.mark.parametrize(
    "override",
    [
        {},
        {"url": "https://example.invalid/fork.git"},
        {"subdirectory": "other"},
        {"vcs_info": {"vcs": "git", "commit_id": "b" * 40}},
    ],
)
def test_validator_installation_provenance(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, override: Mapping[str, object]
) -> None:
    baseline = tmp_path / TRACK / "upstream-baseline.json"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps({"upstream_revision": "a" * 40}))
    direct: dict[str, object] = {
        "url": "https://github.com/agentskills/agentskills.git",
        "subdirectory": "skills-ref",
        "vcs_info": {"vcs": "git", "commit_id": "a" * 40},
    }
    direct.update(override)
    _patch_distribution(monkeypatch, json.dumps(direct))
    assert validator_provenance(tmp_path)["verified"] is (not override)


def test_missing_provenance_is_unverified(tmp_path: Path) -> None:
    assert validator_provenance(tmp_path)["verified"] is False


@pytest.mark.parametrize(
    "direct", [None, [], {}, {"vcs_info": []}, {"vcs_info": {"commit_id": 12}}, "malformed"]
)
def test_invalid_installation_metadata_cannot_verify(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, direct: object
) -> None:
    baseline = tmp_path / TRACK / "upstream-baseline.json"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps({"upstream_revision": "a" * 40}))
    _patch_distribution(monkeypatch, "{" if direct == "malformed" else json.dumps(direct))
    assert validator_provenance(tmp_path)["verified"] is False


def test_absent_distribution_cannot_verify(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    baseline = tmp_path / TRACK / "upstream-baseline.json"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps({"upstream_revision": "a" * 40}))

    def unavailable(name: str) -> NoReturn:
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr("tools.run_skill_conformance.importlib.metadata.distribution", unavailable)
    assert validator_provenance(tmp_path)["verified"] is False


@pytest.mark.parametrize(
    ("offline", "verified", "drift_flag", "expected_code"),
    [(False, False, True, 1), (False, True, 1, 1), (True, True, True, 0)],
)
def test_current_claim_requires_literal_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    offline: bool,
    verified: bool,
    drift_flag: object,
    expected_code: int,
) -> None:
    def validate(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        assert command == [
            sys.executable,
            "-I",
            "-m",
            "skills_ref.cli",
            "validate",
            str(tmp_path / "skills/rca-investigation"),
        ]
        return subprocess.CompletedProcess(command, 0)

    _patch_checks(monkeypatch, current=drift_flag)
    _patch_provenance(monkeypatch, verified=verified)
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", validate)
    code, receipt = run_conformance(tmp_path, offline=offline)
    assert code == expected_code
    assert receipt["current_conformance"] is False


@pytest.mark.parametrize("write_file", [True, False])
def test_cli_preserves_failed_receipt(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    write_file: bool,
) -> None:
    from tools.run_skill_conformance import main

    receipt: dict[str, object] = {
        "current_conformance": False,
        "project_profile": {"complete": False},
    }

    def conformance(_root: Path, **_kwargs: object) -> tuple[int, dict[str, object]]:
        return 1, receipt

    monkeypatch.setattr("tools.run_skill_conformance.run_conformance", conformance)
    output = tmp_path / "nested/receipt.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["conformance", "--root", str(tmp_path)]
        + (["--output", str(output)] if write_file else []),
    )
    assert main() == 1
    rendered = output.read_text() if write_file else capsys.readouterr().out
    assert json.loads(rendered) == receipt
