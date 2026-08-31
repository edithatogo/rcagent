from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools.run_skill_conformance import run_conformance, validator_provenance
from tools.validate_skill_profile import TRACK


@pytest.fixture(autouse=True)
def verified_validator(monkeypatch):
    monkeypatch.setattr(
        "tools.run_skill_conformance.validator_provenance", lambda root: {"verified": True}
    )


def test_live_conformance_requires_all_checks(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
    code, receipt = run_conformance(tmp_path)
    assert code == 0
    assert receipt["current_conformance"] is True


def test_offline_receipt_never_claims_current(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": False}),
    )
    code, receipt = run_conformance(tmp_path, offline=True)
    assert code == 0
    assert receipt["local_validation_passed"] is True
    assert receipt["current_conformance"] is False


def test_offline_invalid_baseline_returns_nonzero(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (2, {"current_conformance": False, "status": "baseline_invalid"}),
    )
    code, receipt = run_conformance(tmp_path, offline=True)
    assert code == 1
    assert receipt["current_conformance"] is False


def test_profile_failure_returns_nonzero(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr(
        "tools.run_skill_conformance.validate_profile", lambda *a, **k: ["RCA-PROFILE-004"]
    )
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["project_profile"]["diagnostics"] == ["RCA-PROFILE-004"]


def test_missing_official_validator_is_a_failure(monkeypatch, tmp_path: Path) -> None:
    def missing(*args, **kwargs):
        raise FileNotFoundError("skills-ref")

    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", missing)
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["official_validator"]["exit_code"] == 127


def test_custom_validator_cannot_certify_current(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
    code, receipt = run_conformance(tmp_path, validator="always-success")
    assert code == 1
    assert receipt["current_conformance"] is False
    assert receipt["official_validator"]["provenance"]["verified"] is False


def test_incomplete_profile_cannot_certify_current(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0)
    )
    monkeypatch.setattr(
        "tools.run_skill_conformance.validate_profile",
        lambda *a, **k: ["pending"] if k["require_complete"] else [],
    )
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
    code, receipt = run_conformance(tmp_path, require_complete=False)
    assert code == 1
    assert receipt["local_validation_passed"] is True
    assert receipt["project_profile"]["complete"] is False


def test_validator_timeout_fails_closed(monkeypatch, tmp_path):
    def timeout(*args, **kwargs):
        assert kwargs["timeout"] == 60
        raise subprocess.TimeoutExpired("validator", 60)

    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", timeout)
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr(
        "tools.run_skill_conformance.check_drift",
        lambda *a, **k: (0, {"current_conformance": True}),
    )
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
def test_validator_installation_provenance(monkeypatch, tmp_path, override):
    baseline = tmp_path / TRACK / "upstream-baseline.json"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps({"upstream_revision": "a" * 40}))
    direct = {
        "url": "https://github.com/agentskills/agentskills.git",
        "subdirectory": "skills-ref",
        "vcs_info": {"vcs": "git", "commit_id": "a" * 40},
    }
    direct.update(override)
    monkeypatch.setattr(
        "tools.run_skill_conformance.importlib.metadata.distribution",
        lambda name: SimpleNamespace(read_text=lambda filename: json.dumps(direct)),
    )
    assert validator_provenance(tmp_path)["verified"] is (not override)


def test_missing_provenance_is_unverified(tmp_path):
    assert validator_provenance(tmp_path)["verified"] is False
