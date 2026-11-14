"""Version-specific evidence checks; no real runtime invocation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest

from tools import darwin_runtime_v030 as runtime


def test_distinct_profile_preserves_legacy() -> None:
    from tools import darwin_runtime_profile as legacy

    assert runtime.EXECUTABLE != legacy.EXECUTABLE
    assert runtime.PINNED_FILES[runtime.EXECUTABLE] != legacy.PINNED_FILES[legacy.EXECUTABLE]
    assert runtime.profile_digest() != legacy.profile_digest()
    assert len(runtime.REQUIRED_IMAGES) == 11
    assert len(runtime.PINNED_FILES) == 16


def test_digest_covers_evidence_and_version(monkeypatch: pytest.MonkeyPatch) -> None:
    original = runtime.profile_digest()
    with monkeypatch.context() as patch:
        patch.setattr(runtime, "EVIDENCE_FILES", {})
        assert runtime.profile_digest() != original
    monkeypatch.setattr(runtime, "VERSION_LINE", b"different")
    assert runtime.profile_digest() != original


@pytest.mark.parametrize("damage", ["none", "missing", "changed", "symlink"])
def test_evidence_file_checks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, damage: str) -> None:
    source = tmp_path / "licence.txt"
    source.write_bytes(b"synthetic licence")
    monkeypatch.setattr(
        runtime, "EVIDENCE_FILES", {str(source): hashlib.sha256(source.read_bytes()).hexdigest()}
    )
    monkeypatch.setattr(runtime.core, "verify_files", Mock(return_value=None))
    if damage == "none":
        runtime.verify_files()
        return
    source.unlink()
    if damage == "changed":
        source.write_bytes(b"changed")
    elif damage == "symlink":
        target = tmp_path / "target"
        target.write_bytes(b"synthetic licence")
        source.symlink_to(target)
    with pytest.raises(ValueError):
        runtime.verify_files()


def test_wrappers_select_explicit_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    import sys

    module = sys.modules[runtime.__name__]

    def environment(adapter: ModuleType) -> dict[str, str]:
        return {"selected": adapter.__name__}

    monkeypatch.setattr(runtime.core, "profile_environment", environment)

    def images(raw: bytes, adapter: ModuleType) -> list[str]:
        return [adapter.__name__, raw.decode()]

    monkeypatch.setattr(runtime.core, "verify_loaded_images", images)
    assert runtime.profile_environment() == {"selected": module.__name__}
    assert runtime.verify_loaded_images(b"fixture") == [module.__name__, "fixture"]


@pytest.mark.parametrize("diagnostic", ["version", "help"])
def test_cli_fixed_diagnostic_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    diagnostic: str,
) -> None:
    calls: list[tuple[str, str]] = []

    def capture(adapter: ModuleType, *, diagnostic: str) -> dict[str, object]:
        calls.append((adapter.__name__, diagnostic))
        return {"status": "runtime_profile_observed", "admitted": False, "study_unlocked": False}

    monkeypatch.setattr(runtime.core, "capture_version", capture)
    destination = tmp_path / "receipt.json"
    assert runtime.main(["--diagnostic", diagnostic, "--receipt", str(destination)]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["receipt_sha256"] == hashlib.sha256(destination.read_bytes()).hexdigest()
    assert calls == [(runtime.__name__, diagnostic)]
    assert runtime.main(["--receipt", str(destination)]) == 1
    assert len(calls) == 1


def test_cli_failed_capture_and_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        runtime.core, "capture_version", Mock(return_value={"status": "profile_failed"})
    )
    assert runtime.main(["--receipt", str(tmp_path / "receipt.json")]) == 1
    assert runtime.main(["--receipt", str(tmp_path / "absent" / "receipt.json")]) == 1


def test_cli_rejects_unknown_diagnostic(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        runtime.main(["--receipt", str(tmp_path / "receipt.json"), "--diagnostic", "execute"])


def test_cli_preserves_dangling_symlink(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    destination = tmp_path / "receipt.json"
    destination.symlink_to(tmp_path / "absent")
    monkeypatch.setattr(
        runtime.core, "capture_version", Mock(side_effect=AssertionError("must not execute"))
    )
    assert runtime.main(["--receipt", str(destination)]) == 1
    assert Path(destination).is_symlink()
