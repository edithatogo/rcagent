"""Tests for the gremlins invisible-character scanner."""

from __future__ import annotations

from pathlib import Path

from tools.check_gremlins import main, scan


def _write(tmp_path: Path, name: str, content: str) -> Path:
    target = tmp_path / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def test_clean_repo_returns_no_findings(tmp_path: Path) -> None:
    _write(tmp_path, "ok.md", "# Clean\n\nNo gremlins here.\n")
    assert scan(tmp_path) == []


def test_zero_width_space_is_detected_with_location(tmp_path: Path) -> None:
    _write(tmp_path, "bad.md", "hidden\u200bcharacter\n")
    findings = scan(tmp_path)
    assert len(findings) == 1
    assert "ZERO WIDTH SPACE" in findings[0]
    assert ":1:7:" in findings[0]


def test_bidi_override_is_detected(tmp_path: Path) -> None:
    sneaky = tmp_path / "tricky.txt"
    sneaky.write_text("value\u202ereversed\n", encoding="utf-8")
    findings = scan(tmp_path)
    assert any("RIGHT-TO-LEFT OVERRIDE" in f for f in findings)


def test_nbsp_allowed_in_markdown_but_flagged_in_python(tmp_path: Path) -> None:
    _write(tmp_path, "doc.md", "wide\u00a0space is fine in prose\n")
    assert scan(tmp_path) == []
    _write(tmp_path, "code.py", "x = 'a\u00a0b'\n")
    assert any("NO-BREAK SPACE" in f for f in scan(tmp_path))


def test_txt_files_are_scanned(tmp_path: Path) -> None:
    _write(tmp_path, "notes.txt", "plain text with\u200bzero width\n")
    findings = scan(tmp_path)
    assert len(findings) == 1
    assert "ZERO WIDTH SPACE" in findings[0]


def test_gitlink_paths_are_not_scanned(tmp_path: Path) -> None:
    (tmp_path / ".gitmodules").write_text(
        '[submodule "ext"]\n\tpath = vendor/ext\n\turl = https://example.com/ext.git\n',
        encoding="utf-8",
    )
    third_party = tmp_path / "vendor" / "ext"
    third_party.mkdir(parents=True)
    (third_party / "upstream.md").write_text("hidden\u200bgremlin\n", encoding="utf-8")
    first_party = tmp_path / "local.md"
    first_party.write_text("clean\u200bshould-still-scan\n", encoding="utf-8")
    findings = scan(tmp_path)
    assert len(findings) == 1
    assert str(first_party) in findings[0]


def test_skip_dirs_are_not_scanned(tmp_path: Path) -> None:
    hidden = tmp_path / ".git"
    hidden.mkdir()
    (hidden / "config.py").write_text("x = '\u200b'\n", encoding="utf-8")
    assert scan(tmp_path) == []


def test_invalid_utf8_reported_once(tmp_path: Path) -> None:
    target = tmp_path / "broken.csv"
    target.write_bytes(b"a,b\n\xff\xfe,c\n")
    findings = scan(tmp_path)
    assert len(findings) == 1
    assert "not valid UTF-8" in findings[0]


def test_main_exit_codes(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    _write(tmp_path, "clean.py", "value = 1\n")
    assert main([str(tmp_path)]) == 0
    _write(tmp_path, "dirty.md", "a\u200bb\n")
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert "gremlin(s) found" in captured.err
    assert main([str(tmp_path / "missing")]) == 2
