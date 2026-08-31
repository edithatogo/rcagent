from __future__ import annotations

from pathlib import Path

import pytest

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


def test_orphan_resource_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    (skill / "references/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    assert "RCA-RESOURCE-001" in _requirements(skill)


def test_explicit_directory_route_covers_nested_resources(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    path = skill / "SKILL.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "\nLoad only from `assets/templates/`.\n",
        encoding="utf-8",
    )
    nested = skill / "assets/templates"
    nested.mkdir(parents=True)
    (nested / "report.md").write_text("# Report\n", encoding="utf-8")
    assert validate_skill(skill) == []


def _symlink(link: Path, target: Path, *, directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=directory)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")


@pytest.mark.parametrize("target_kind", ["external", "internal", "missing"])
def test_linked_resources_fail_before_reading_package_bytes(
    tmp_path: Path, monkeypatch, target_kind: str
) -> None:
    skill = _skill(tmp_path)
    target = tmp_path / "outside.md"
    if target_kind == "external":
        target.write_text("Synthetic external resource", encoding="utf-8")
    elif target_kind == "internal":
        target = skill / "SKILL.md"
    guide = skill / "references/guide.md"
    guide.unlink()
    _symlink(guide, target)

    def unexpected_read(*args, **kwargs):
        pytest.fail("linked package must be rejected before reading any contents")

    monkeypatch.setattr(Path, "read_text", unexpected_read)
    assert "RCA-PORT-001" in _requirements(skill)


def test_linked_resource_directory_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "guide.md").write_text("Synthetic external resource", encoding="utf-8")
    _symlink(skill / "assets", outside, directory=True)
    assert "RCA-PORT-001" in _requirements(skill)


def test_linked_skill_file_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    source = tmp_path / "outside.md"
    (skill / "SKILL.md").rename(source)
    _symlink(skill / "SKILL.md", source)
    assert "RCA-PORT-001" in _requirements(skill)


def test_linked_skill_root_fails(tmp_path: Path) -> None:
    skill = _skill(tmp_path)
    links = tmp_path / "links"
    links.mkdir()
    linked = links / skill.name
    _symlink(linked, skill, directory=True)
    assert "RCA-PORT-001" in _requirements(linked)


@pytest.mark.parametrize("reference", [r"references/..\outside.md", "references/file:stream"])
def test_platform_specific_reference_paths_fail(tmp_path: Path, reference: str) -> None:
    skill = _skill(tmp_path)
    path = skill / "SKILL.md"
    path.write_text(path.read_text(encoding="utf-8") + f"\nRead `{reference}`.\n", encoding="utf-8")
    assert any(
        item.requirement == "AS-SPEC-008" and "not portable" in item.message
        for item in validate_skill(skill)
    )
