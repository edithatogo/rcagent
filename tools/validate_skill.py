"""Deterministic Agent Skill portability and project-profile validation."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import yaml

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_PATTERN = re.compile(r"`((?:references|assets|scripts)/[^`\s]+)`")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}


@dataclass(frozen=True)
class Diagnostic:
    requirement: str
    path: str
    message: str

    def render(self) -> str:
        return f"{self.requirement}: {self.path}: {self.message}"


def _frontmatter(skill_md: Path) -> tuple[dict[str, object], str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not terminated") from exc
    parsed = yaml.safe_load(raw)
    if not isinstance(parsed, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    return parsed, body


def validate_skill(skill_root: Path, *, portable_core: bool = True) -> list[Diagnostic]:
    # Reject links before resolving or reading any package bytes. Copy/archive
    # behaviour differs across clients, and following a resource link can read
    # material outside the supposedly self-contained package.
    if skill_root.is_symlink():
        return [Diagnostic("RCA-PORT-001", ".", "symbolic links are not portable package resources")]
    root = skill_root.resolve()
    skill_md = root / "SKILL.md"
    diagnostics: list[Diagnostic] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            diagnostics.append(
                Diagnostic(
                    "RCA-PORT-001",
                    path.relative_to(root).as_posix(),
                    "symbolic links are not portable package resources",
                )
            )
    if diagnostics:
        return diagnostics
    if not skill_md.is_file():
        return [Diagnostic("AS-SPEC-001", "SKILL.md", "required file is missing")]

    try:
        metadata, body = _frontmatter(skill_md)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [Diagnostic("AS-SPEC-001", "SKILL.md", str(exc))]

    unknown = sorted(set(metadata) - ALLOWED_FIELDS)
    for field in unknown:
        diagnostics.append(
            Diagnostic("RCA-EXT-001", "SKILL.md", f"unknown frontmatter field: {field}")
        )

    name = metadata.get("name")
    if (
        not isinstance(name, str)
        or len(name) > 64
        or not NAME_PATTERN.fullmatch(name)
        or name != root.name
    ):
        diagnostics.append(
            Diagnostic(
                "AS-SPEC-002",
                "SKILL.md:name",
                "must be 1-64 lowercase letters, digits, or single hyphens and match the directory",
            )
        )

    description = metadata.get("description")
    if not isinstance(description, str) or not (1 <= len(description) <= 1024):
        diagnostics.append(
            Diagnostic(
                "AS-SPEC-003",
                "SKILL.md:description",
                "must be a non-empty string no longer than 1024 characters",
            )
        )

    compatibility = metadata.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not (1 <= len(compatibility) <= 500)
    ):
        diagnostics.append(
            Diagnostic(
                "AS-SPEC-005",
                "SKILL.md:compatibility",
                "must be a string between 1 and 500 characters",
            )
        )

    custom = metadata.get("metadata")
    if custom is not None and (
        not isinstance(custom, dict)
        or any(not isinstance(key, str) or not isinstance(value, str) for key, value in custom.items())
    ):
        diagnostics.append(
            Diagnostic(
                "AS-SPEC-006",
                "SKILL.md:metadata",
                "must map string keys to string values",
            )
        )

    if portable_core and "allowed-tools" in metadata:
        diagnostics.append(
            Diagnostic(
                "AS-SPEC-007",
                "SKILL.md:allowed-tools",
                "experimental tool permissions belong in a tested client adapter, not the portable core",
            )
        )

    text = skill_md.read_text(encoding="utf-8")
    references = {match.group(1) for match in REFERENCE_PATTERN.finditer(text)}
    for reference in sorted(references):
        pure = PurePosixPath(reference)
        if ".." in pure.parts or pure.is_absolute() or "\\" in reference or ":" in reference:
            diagnostics.append(
                Diagnostic("AS-SPEC-008", reference, "reference escapes the skill root or is not portable")
            )
            continue
        if not (root / Path(*pure.parts)).exists():
            diagnostics.append(
                Diagnostic("AS-SPEC-008", reference, "referenced resource does not exist")
            )

    for directory in ("references", "scripts", "assets"):
        resource_root = root / directory
        if not resource_root.is_dir():
            continue
        for resource in sorted(path for path in resource_root.rglob("*") if path.is_file()):
            relative = resource.relative_to(root).as_posix()
            routed = any(
                relative == reference
                or (reference.endswith("/") and relative.startswith(reference))
                for reference in references
            )
            if not routed:
                diagnostics.append(
                    Diagnostic(
                        "RCA-RESOURCE-001",
                        relative,
                        "bundled resource is not routed from SKILL.md",
                    )
                )

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(content.splitlines(), 1):
            if WINDOWS_ABSOLUTE.match(line.strip()) or "/Users/" in line or "/home/" in line:
                diagnostics.append(
                    Diagnostic(
                        "RCA-PORT-001",
                        f"{relative}:{line_number}",
                        "absolute local path is not portable",
                    )
                )

    if len(text.splitlines()) >= 500:
        diagnostics.append(
            Diagnostic("AS-GUIDE-001", "SKILL.md", "must remain below 500 lines")
        )
    if not body.strip():
        diagnostics.append(
            Diagnostic("AS-SPEC-001", "SKILL.md", "instruction body is empty")
        )
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", type=Path)
    parser.add_argument(
        "--adapter",
        action="store_true",
        help="Allow adapter-specific experimental fields.",
    )
    args = parser.parse_args()
    diagnostics = validate_skill(args.skill_root, portable_core=not args.adapter)
    if diagnostics:
        for diagnostic in diagnostics:
            print(f"ERROR: {diagnostic.render()}")
        return 1
    print("Project Agent Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
