from __future__ import annotations

from pathlib import Path

from tools.validate_skill import validate_skill


def _skill(root: Path, name: str = "example-skill", extra: str = "") -> Path:
    skill = root / name
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: Perform an example task. Use when testing an Agent Skill.\n"
        f"{extra}"
        "---\n\n"
        "# Procedure\n\n"
        "Read `references/guide.md`.\n",
        encoding="utf-8",
    )
    (skill / "references").mkdir()
    (skill / "references/guide.md").write_text("# Guide\n", encoding="utf-8")
    return skill


def _requirements(skill: Path) -> set[str]:
    return {diagnostic.requirement for diagnostic in validate_skill(skill)}


def test_valid_minimal_fixture_passes(tmp_path: Path) -> None:
    assert validate_skill(_skill(tmp_path)) == []


def test_invalid_name_and_directory_mismatch_fail(tmp_path: Path) -> None:
    skill = _skill(tmp_path, name="example-skill")
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    (skill / "SKILL.md").write_text(
        text.replace("name: example-skill", "name: Invalid--Name"),
        encoding="utf-8",
    )
    assert "AS-SPEC-002" in _requirements(skill)


def test_long_description_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace(
            "Perform an example task. Use when testing an Agent Skill.",
            "x" * 1025,
        ),
        encoding="utf-8",
    )
    assert "AS-SPEC-003" in _requirements(skill)


def test_broken_and_escaping_references_fail(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    path = skill / "SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8")
        + "\nRead `references/missing.md` and `references/../secret.md`.\n",
        encoding="utf-8",
    )
    assert "AS-SPEC-008" in _requirements(skill)


def test_malformed_metadata_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path, extra="metadata:\n  count: 1\n")
    assert "AS-SPEC-006" in _requirements(skill)


def test_experimental_field_fails_in_core_but_not_adapter(tmp_path: Path) -> None:
    skill = _skill(tmp_path, extra="allowed-tools: Read\n")
    assert "AS-SPEC-007" in _requirements(skill)
    assert validate_skill(skill, portable_core=False) == []


def test_absolute_path_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    (skill / "references/guide.md").write_text(
        "# Guide\n\nC:\\private\\record.txt\n", encoding="utf-8"
    )
    assert "RCA-PORT-001" in _requirements(skill)
