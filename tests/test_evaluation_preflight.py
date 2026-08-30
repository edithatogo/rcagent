"""Synthetic contract tests: no fixture can authorise a study transition."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tools.evaluation_preflight import ROLES, check_envelope, main


def fixture(root: Path, stage: str = "admission") -> tuple[Path, dict]:
    files = []
    for role in sorted(ROLES[stage]):
        path = root / f"{role}.txt"
        path.write_text(f"Synthetic {role} contract placeholder", encoding="utf-8")
        files.append(
            {
                "role": role,
                "path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    payload = {
        "schema_version": "1.0",
        "purpose": "contract-fixture",
        "study_id": "synthetic-test-only",
        "revision": "a" * 40,
        "stage": stage,
        "files": files,
    }
    receipt = root / "receipt.json"
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    return receipt, payload


def pinned(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    "field,value",
    [
        ("role", []),
        ("role", "unknown"),
        ("path", None),
        ("path", ""),
        ("path", "bad\u0000path"),
        ("path", "C:/raw"),
        ("sha256", None),
    ],
)
def test_invalid_entry_values(tmp_path: Path, field: str, value: object) -> None:
    receipt, payload = fixture(tmp_path)
    payload["files"][0][field] = value
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")


@pytest.mark.parametrize("change", ["id", "revision", "entry", "role", "path"])
def test_structural_rejections(tmp_path: Path, change: str) -> None:
    receipt, payload = fixture(tmp_path)
    if change == "id":
        payload["study_id"] = None
    elif change == "revision":
        payload["revision"] = None
    elif change == "entry":
        payload["files"][0] = None
    else:
        payload["files"][1][change] = payload["files"][0][change]
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")


def test_missing_receipt_and_resource_limits(tmp_path: Path, monkeypatch) -> None:
    assert main(["--stage", "admission", "--check-fixture"]) == 1
    receipt = tmp_path / "receipt.json"
    for data in [b"\xff", b"[" * 2000]:
        receipt.write_bytes(data)
        with pytest.raises(ValueError, match="invalid_json"):
            check_envelope(receipt, pinned(receipt), "admission")
    monkeypatch.setattr("tools.evaluation_preflight.MAX_BYTES", 2)
    receipt.write_bytes(b"123")
    with pytest.raises(ValueError, match="artifact_size_out_of_bounds"):
        check_envelope(receipt, pinned(receipt), "admission")


def test_io_error_is_sanitised(tmp_path: Path, monkeypatch) -> None:
    receipt, _ = fixture(tmp_path)
    digest = pinned(receipt)

    def denied(*args, **kwargs):
        raise PermissionError("private path must not leak")

    monkeypatch.setattr(Path, "open", denied)
    with pytest.raises(ValueError, match="^unreadable_artifact$"):
        check_envelope(receipt, digest, "admission")


@pytest.mark.parametrize("stage", sorted(ROLES))
def test_fixture_envelope_never_unlocks_study(tmp_path: Path, stage: str) -> None:
    receipt, _ = fixture(tmp_path, stage)
    result = check_envelope(receipt, pinned(receipt), stage)
    assert result == {"status": "fixture_pass", "stage": stage, "study_unlocked": False}
    assert (
        main(
            [
                "--stage",
                stage,
                "--receipt",
                str(receipt),
                "--expected-sha256",
                pinned(receipt),
                "--check-fixture",
            ]
        )
        == 0
    )
    assert (
        main(["--stage", stage, "--receipt", str(receipt), "--expected-sha256", pinned(receipt)])
        == 1
    )


@pytest.mark.parametrize("content", ["", "PASS", "{}", "[]", "null", "slot_id\n"])
def test_empty_prose_and_csv_cannot_pass(tmp_path: Path, content: str) -> None:
    receipt = tmp_path / "receipt.json"
    receipt.write_text(content, encoding="utf-8")
    assert (
        main(
            [
                "--stage",
                "admission",
                "--receipt",
                str(receipt),
                "--expected-sha256",
                pinned(receipt),
                "--check-fixture",
            ]
        )
        == 1
    )


@pytest.mark.parametrize(
    "change",
    [
        "purpose",
        "revision",
        "stage",
        "missing-role",
        "duplicate-role",
        "extra-field",
        "bad-hash",
        "absolute",
        "traversal",
        "backslash",
        "wrong-type",
    ],
)
def test_invalid_envelopes_fail_closed(tmp_path: Path, change: str) -> None:
    receipt, value = fixture(tmp_path)
    if change == "purpose":
        value["purpose"] = "study-evidence"
    elif change == "revision":
        value["revision"] = "master"
    elif change == "stage":
        value["stage"] = "analysis"
    elif change == "missing-role":
        value["files"].pop()
    elif change == "duplicate-role":
        value["files"].append(value["files"][0])
    elif change == "extra-field":
        value["approved"] = True
    elif change == "bad-hash":
        value["files"][0]["sha256"] = "0" * 64
    elif change == "absolute":
        value["files"][0]["path"] = str(tmp_path / "raw.txt")
    elif change == "traversal":
        value["files"][0]["path"] = "../raw.txt"
    elif change == "backslash":
        value["files"][0]["path"] = "..\\raw.txt"
    else:
        value["files"] = "not a list"
    receipt.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")


def test_pins_missing_empty_and_modified_artifacts(tmp_path: Path) -> None:
    receipt, value = fixture(tmp_path)
    with pytest.raises(ValueError):
        check_envelope(receipt, "0" * 64, "admission")
    artifact = tmp_path / value["files"][0]["path"]
    artifact.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")
    artifact.write_bytes(b"")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")
    artifact.unlink()
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")


def test_duplicate_json_and_symlink_are_rejected(tmp_path: Path) -> None:
    receipt, value = fixture(tmp_path)
    receipt.write_text('{"stage":"admission", "stage":"analysis"}', encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")
    receipt.write_text(json.dumps(value), encoding="utf-8")
    target = tmp_path / value["files"][0]["path"]
    alias = tmp_path / "alias.txt"
    try:
        alias.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable for this account")
    value["files"][0]["path"] = alias.name
    receipt.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        check_envelope(receipt, pinned(receipt), "admission")


def test_live_mode_does_not_read_supplied_evidence(tmp_path: Path, capsys) -> None:
    assert main(["--stage", "analysis", "--receipt", str(tmp_path / "absent")]) == 1
    output = capsys.readouterr().out
    assert "semantic_admission_not_implemented" in output
    assert str(tmp_path) not in output


@pytest.mark.parametrize(
    "script", ["phase4_admission_preflight.ps1", "track5_preflight.ps1", "track6_preflight.ps1"]
)
def test_legacy_entrypoints_never_accept_positive_prose(tmp_path: Path, script: str) -> None:
    pwsh = shutil.which("pwsh")
    if not pwsh:
        pytest.skip("PowerShell not available; Python gate covered on every platform")
    receipt = tmp_path / "positive.md"
    receipt.write_text("PASS: everything complete", encoding="utf-8")
    root = Path(__file__).parents[1]
    result = subprocess.run(
        [
            pwsh,
            "-NoProfile",
            "-File",
            str(root / "tools" / script),
            "-Receipt",
            str(receipt),
            "-PythonExecutable",
            sys.executable,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "semantic_admission_not_implemented" in result.stdout


@pytest.mark.parametrize(
    "script,alias",
    [
        ("phase4_admission_preflight.ps1", "AuditPath"),
        ("track5_preflight.ps1", "ManifestAudit"),
        ("track6_preflight.ps1", "ClaimsBoundary"),
    ],
)
def test_wrapper_cannot_trust_successful_interpreter(
    tmp_path: Path, script: str, alias: str
) -> None:
    pwsh = shutil.which("pwsh")
    if not pwsh:
        pytest.skip("PowerShell unavailable")
    stub = tmp_path / "success.ps1"
    stub.write_text("exit 0", encoding="utf-8")
    for executable in [str(stub), str(tmp_path / "missing-executable")]:
        result = subprocess.run(
            [
                pwsh,
                "-NoProfile",
                "-File",
                str(Path(__file__).parents[1] / "tools" / script),
                f"-{alias}",
                "missing-receipt",
                "-PythonExecutable",
                executable,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0
