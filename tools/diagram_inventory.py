"""Read-only inventory of rcagent method guides and admitted Mermaid draft templates.

This reports supported source assets, not clinically validated diagrams or
installed native Mermaid specialist parsers. Admission remains owned by the
existing template-admission contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/rca-investigation")
TEMPLATE_DIR = Path("assets/templates/mermaid")
MANIFEST = Path("assets/template-admission.json")
METHOD_DIR = Path("references/methods")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class InventoryError(ValueError):
    """Fail-closed source inventory error."""


@dataclass(frozen=True)
class Method:
    slug: str
    guide: str
    templates: tuple[str, ...]
    issue: int


METHODS: tuple[Method, ...] = (
    Method("rca_squared", "rca-squared.md", (), 163),
    Method("five_whys", "five-whys.md", ("five-whys-chain.mmd",), 164),
    Method("fishbone", "fishbone.md", ("fishbone-ishikawa.mmd",), 165),
    Method("yorkshire", "yorkshire-framework.md", ("yorkshire-factors.mmd",), 166),
    Method("seips", "seips.md", ("seips-work-system.mmd",), 167),
    Method("swiss_cheese", "swiss-cheese.md", ("swiss-cheese-model.mmd",), 168),
    Method("bow_tie", "bow-tie.md", ("bow-tie-analysis.mmd",), 169),
    Method("barrier_analysis", "barrier-analysis.md", (), 169),
    Method("fmea", "fmea.md", ("fmea-priority-quadrant.mmd",), 170),
    Method("timeline", "timeline-analysis.md", ("timeline-chronology.mmd",), 171),
    Method("hfacs", "hfacs.md", ("hfacs-layers.mmd",), 172),
    Method("london_protocol", "london-protocol.md", (), 173),
    Method("accimap", "accimap.md", ("accimap-levels.mmd",), 139),
    Method("stamp_stpa", "stamp-stpa.md", ("stamp-control-structure.mmd",), 174),
)

TEMPLATE_SYNTAX: dict[str, str] = {
    "accimap-levels.mmd": "flowchart",
    "bow-tie-analysis.mmd": "flowchart",
    "fishbone-ishikawa.mmd": "mindmap",
    "five-whys-chain.mmd": "flowchart",
    "fmea-priority-quadrant.mmd": "quadrantChart",
    "hfacs-layers.mmd": "flowchart",
    "investigation-workflow.mmd": "flowchart",
    "seips-work-system.mmd": "flowchart",
    "stamp-control-structure.mmd": "flowchart",
    "swiss-cheese-model.mmd": "flowchart",
    "timeline-chronology.mmd": "timeline",
    "yorkshire-factors.mmd": "mindmap",
}

PROPOSED_DIAGRAMS: tuple[tuple[str, int], ...] = (
    ("faulttree-beta", 175),
    ("eventtree-beta", 176),
    ("causalloop-beta", 177),
    ("xmrchart-beta", 178),
    ("fram-beta", 179),
    ("bowtie-beta", 169),
    ("accimap-beta", 139),
    ("stamp-beta", 174),
    ("domainstorytelling-beta", 180),
)


class MethodRecord(TypedDict):
    id: str
    guide: str
    templates: list[str]
    issue: int


class TemplateRecord(TypedDict):
    name: str
    keyword: str
    status: str
    role: str
    methods: list[str]
    syntax_checked: bool


class ProposedRecord(TypedDict):
    keyword: str
    status: str
    issue: int


class InventoryReport(TypedDict):
    schema_version: str
    source: str
    admission_revision: str
    native_diagram_claim: str
    methods: list[MethodRecord]
    templates: list[TemplateRecord]
    proposed_diagrams: list[ProposedRecord]


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise InventoryError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _object(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise InventoryError(f"{context} must be a JSON object")
    return cast(dict[str, object], value)


def _keyword(source: str) -> str:
    for line in source.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("%%"):
            return stripped.split()[0]
    return ""


def build_inventory(root: Path) -> InventoryReport:
    """Refuse missing guides, unlisted templates, changed hashes or syntax drift."""
    skill_root = root / SKILL
    manifest_path = skill_root / MANIFEST
    if not manifest_path.is_file():
        raise InventoryError("missing template admission manifest")
    try:
        decoded = cast(
            object,
            json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InventoryError("invalid template admission manifest") from error
    manifest = _object(decoded, "manifest")
    if manifest.get("schema_version") != "1.0":
        raise InventoryError("unsupported manifest schema version")
    if manifest.get("admission") != "portable_draft_only":
        raise InventoryError("templates not admitted for portable draft")
    revision = manifest.get("revision")
    if not isinstance(revision, str) or not revision:
        raise InventoryError("missing manifest revision")
    raw_entries = manifest.get("files")
    if not isinstance(raw_entries, list):
        raise InventoryError("invalid manifest files")
    entries = cast(list[object], raw_entries)
    admitted: dict[str, str] = {}
    prefix = TEMPLATE_DIR.as_posix() + "/"
    for raw_entry in entries:
        entry = _object(raw_entry, "entry")
        name = entry.get("path")
        if not isinstance(name, str) or not name.startswith(prefix):
            continue
        filename = name.removeprefix(prefix)
        if "/" in filename or "\\" in filename:
            raise InventoryError("invalid Mermaid template path")
        if filename in admitted:
            raise InventoryError(f"duplicate admitted template: {filename}")
        digest = entry.get("sha256")
        if (
            entry.get("status") != "admitted_portable_draft"
            or not isinstance(digest, str)
            or not DIGEST.fullmatch(digest)
        ):
            raise InventoryError(f"unadmitted or invalid template: {filename}")
        admitted[filename] = digest
    expected = set(TEMPLATE_SYNTAX)
    actual = {p.name for p in (skill_root / TEMPLATE_DIR).glob("*.mmd") if p.is_file()}
    missing = sorted(expected - set(admitted))
    if missing:
        raise InventoryError(f"missing admitted template: {missing[0]}")
    extras = sorted((set(admitted) - expected) | (actual - expected))
    if extras:
        raise InventoryError(f"unregistered Mermaid file: {extras[0]}")
    missing_file = sorted(expected - actual)
    if missing_file:
        raise InventoryError(f"missing Mermaid file: {missing_file[0]}")
    for method in METHODS:
        if not (skill_root / METHOD_DIR / method.guide).is_file():
            raise InventoryError(f"missing method guide: {method.guide}")
        for name in method.templates:
            if name not in expected:
                raise InventoryError(f"unregistered method template: {name}")
    methods: list[MethodRecord] = [
        {
            "id": method.slug,
            "guide": method.guide,
            "templates": list(method.templates),
            "issue": method.issue,
        }
        for method in METHODS
    ]
    templates: list[TemplateRecord] = []
    for name in sorted(expected):
        template = skill_root / TEMPLATE_DIR / name
        raw = template.read_bytes()
        if hashlib.sha256(raw).hexdigest() != admitted[name]:
            raise InventoryError(f"digest mismatch for {name}")
        try:
            keyword = _keyword(raw.decode("utf-8"))
        except UnicodeDecodeError as error:
            raise InventoryError(f"invalid template UTF-8: {name}") from error
        if keyword != TEMPLATE_SYNTAX[name]:
            raise InventoryError(f"Mermaid keyword drift for {name}: {keyword}")
        linked = sorted(method.slug for method in METHODS if name in method.templates)
        if not linked and name != "investigation-workflow.mmd":
            raise InventoryError(f"unowned Mermaid template: {name}")
        templates.append(
            {
                "name": name,
                "keyword": keyword,
                "status": "admitted_portable_draft",
                "role": "workflow" if name == "investigation-workflow.mmd" else "method_fallback",
                "methods": linked,
                "syntax_checked": True,
            }
        )
    return {
        "schema_version": "diagram-inventory-1.0",
        "source": (SKILL / MANIFEST).as_posix(),
        "admission_revision": revision,
        "native_diagram_claim": "not-established",
        "methods": methods,
        "templates": templates,
        "proposed_diagrams": [
            {"keyword": name, "issue": issue, "status": "proposed-not-implemented"}
            for name, issue in PROPOSED_DIAGRAMS
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        report = build_inventory(args.repository)
    except InventoryError as error:
        print(f"diagram inventory: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
