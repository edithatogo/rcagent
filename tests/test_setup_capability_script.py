from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/setup-capability.ps1"


@pytest.mark.skipif(shutil.which("pwsh") is None, reason="PowerShell 7 unavailable")
def test_preflight_is_read_only_and_machine_readable(tmp_path: Path) -> None:
    target = ROOT / ".capability-preflight-test"
    assert not target.exists()
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Action", "Preflight", "-EnvironmentPath", target.name],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = json.loads(result.stdout)
    assert receipt["result"] == "passed"
    assert receipt["target_state"] == "absent"
    assert receipt["network_authorized"] is False
    assert not target.exists()


def test_installer_has_fail_closed_safety_controls() -> None:
    script = SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "repositoryBoundary",
        "Refusing to modify an existing or unowned environment path",
        "AllowNetwork",
        "Invoke-CheckedNative",
        "$LASTEXITCODE",
        "ConvertTo-Json -Compress",
    ):
        assert marker in script
