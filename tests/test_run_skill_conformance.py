from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tools.run_skill_conformance import run_conformance


def test_live_conformance_requires_all_checks(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0))
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr("tools.run_skill_conformance.check_drift", lambda *a, **k: (0, {"current_conformance": True}))
    code, receipt = run_conformance(tmp_path)
    assert code == 0
    assert receipt["current_conformance"] is True


def test_offline_receipt_never_claims_current(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0))
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr("tools.run_skill_conformance.check_drift", lambda *a, **k: (0, {"current_conformance": False}))
    code, receipt = run_conformance(tmp_path, offline=True)
    assert code == 0
    assert receipt["local_validation_passed"] is True
    assert receipt["current_conformance"] is False


def test_profile_failure_returns_nonzero(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", lambda *a, **k: SimpleNamespace(returncode=0))
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: ["RCA-PROFILE-004"])
    monkeypatch.setattr("tools.run_skill_conformance.check_drift", lambda *a, **k: (0, {"current_conformance": True}))
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["project_profile"]["diagnostics"] == ["RCA-PROFILE-004"]


def test_missing_official_validator_is_a_failure(monkeypatch, tmp_path: Path) -> None:
    def missing(*args, **kwargs):
        raise FileNotFoundError("skills-ref")

    monkeypatch.setattr("tools.run_skill_conformance.subprocess.run", missing)
    monkeypatch.setattr("tools.run_skill_conformance.validate_profile", lambda *a, **k: [])
    monkeypatch.setattr("tools.run_skill_conformance.check_drift", lambda *a, **k: (0, {"current_conformance": True}))
    code, receipt = run_conformance(tmp_path)
    assert code == 1
    assert receipt["official_validator"]["exit_code"] == 127
