from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/setup-capability.ps1"
PWSH = shutil.which("pwsh")


def _run(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    if PWSH is None:
        raise RuntimeError("pwsh (PowerShell) is required for capability-script tests")
    return subprocess.run(
        [PWSH, "-NoProfile", "-File", str(SCRIPT), *arguments],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def _write_marker(target: Path) -> None:
    target.mkdir()
    marker = {
        "schema_version": "1.0",
        "owner": "safety-systems-workbench",
        "installation_id": "fixture-installation",
        "source_revision": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip(),
        "repository_root": str(ROOT),
        "environment_path": str(target),
        "profile": "validate",
    }
    (target / ".safety-systems-capability.json").write_text(json.dumps(marker), encoding="utf-8")
    ownership = ROOT / ".capability-state" / "ownership"
    ownership.mkdir(parents=True, exist_ok=True)
    (ownership / "fixture-installation.json").write_text(json.dumps(marker), encoding="utf-8")


@pytest.mark.skipif(PWSH is None, reason="PowerShell 7 unavailable")
def test_preflight_is_read_only_and_machine_readable(tmp_path: Path) -> None:
    target = ROOT / ".capability-preflight-test"
    assert not target.exists()
    result = _run("-Action", "Preflight", "-EnvironmentPath", target.name)
    receipt = json.loads(result.stdout)
    assert receipt["result"] == "passed"
    assert receipt["target_state"] == "absent"
    assert receipt["network_authorized"] is False
    assert not target.exists()


@pytest.mark.skipif(PWSH is None, reason="PowerShell 7 unavailable")
def test_uninstall_dry_run_preserves_owned_target() -> None:
    target = ROOT / ".capability-owned-test"
    _write_marker(target)
    try:
        result = _run("-Action", "Uninstall", "-EnvironmentPath", target.name, "-DryRun")
        assert json.loads(result.stdout)["result"] == "preview-only-removal-not-implemented"
        assert target.exists()
    finally:
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(ROOT / ".capability-state", ignore_errors=True)


@pytest.mark.skipif(PWSH is None, reason="PowerShell 7 unavailable")
def test_uninstall_refuses_unowned_target() -> None:
    target = ROOT / ".capability-unowned-test"
    target.mkdir()
    try:
        result = _run("-Action", "Uninstall", "-EnvironmentPath", target.name, "-DryRun", check=False)
        assert result.returncode == 2
        assert json.loads(result.stdout)["result"] == "refused-unowned"
        assert target.exists()
    finally:
        target.rmdir()


@pytest.mark.skipif(PWSH is None, reason="PowerShell 7 unavailable")
def test_rollback_is_honestly_unavailable() -> None:
    result = _run("-Action", "Rollback", "-EnvironmentPath", ".capability-absent-test", check=False)
    assert result.returncode == 2
    assert json.loads(result.stdout)["result"] == "rollback-unavailable-no-prior-state"


@pytest.mark.skipif(PWSH is None, reason="PowerShell 7 unavailable")
def test_verify_rejects_owned_target_without_environment_python() -> None:
    target = ROOT / ".capability-invalid-test"
    _write_marker(target)
    try:
        result = _run("-Action", "Verify", "-EnvironmentPath", target.name, check=False)
        assert result.returncode == 2
        assert json.loads(result.stdout)["result"] == "invalid"
    finally:
        shutil.rmtree(target, ignore_errors=True)
        shutil.rmtree(ROOT / ".capability-state", ignore_errors=True)


def test_installer_has_fail_closed_safety_controls() -> None:
    script = SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "repositoryBoundary",
        "Refusing to modify an existing or unowned environment path",
        "AllowNetwork",
        "Invoke-CheckedNative",
        "$LASTEXITCODE",
        "ConvertTo-Json -Compress",
        ".safety-systems-capability.json",
        "preview-only-removal-not-implemented",
        "rollback-unavailable-no-prior-state",
    ):
        assert marker in script
