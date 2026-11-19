"""Validate synthetic proposal SVG assets without evaluating or rendering them.

This is a structural and unsafe-content gate, not a visual, clinical, or
methodological correctness check. It deliberately uses the Python stdlib.
"""

from __future__ import annotations

import argparse
import math
import re
import xml.etree.ElementTree as ET  # nosec B405 - Reviewed checked-in SVGs only; reject DTD/ENTITY before parsing.
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISUALS_DIR = Path("docs/proposals/investigation-visuals")
EXPECTED_FILES = frozenset(
    {
        "issue-139-accimap.svg",
        "issue-167-seips.svg",
        "issue-168-swiss-cheese.svg",
        "issue-169-bowtie.svg",
        "issue-174-stamp.svg",
        "issue-175-fta.svg",
        "issue-176-eta.svg",
        "issue-177-cld.svg",
        "issue-178-xmr.svg",
        "issue-179-fram.svg",
    }
)
SVG_NS = "http://www.w3.org/2000/svg"
ALLOWED_TAGS = frozenset(
    {
        "svg",
        "defs",
        "marker",
        "rect",
        "text",
        "tspan",
        "path",
        "circle",
        "ellipse",
        "g",
        "line",
        "polygon",
        "polyline",
    }
)
LOCAL_URL = re.compile(r"^url\(#([A-Za-z_][A-Za-z0-9_.-]*)\)$")
URL_VALUE = re.compile(r"url\([^)]*\)", re.IGNORECASE)
PROHIBITED_DECLARATIONS = re.compile(r"<!\s*(?:doctype|entity)|<\?xml-stylesheet", re.IGNORECASE)


def _float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def _name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _geometry(element: ET.Element, width: float, height: float) -> bool:
    """Check only elementary geometry; paths and text extents need visual review."""
    tag = _name(element.tag)
    attributes: tuple[str, ...] = ()
    if tag == "rect":
        attributes = ("x", "y", "width", "height")
    elif tag in {"ellipse", "circle"}:
        attributes = ("cx", "cy", "rx", "ry") if tag == "ellipse" else ("cx", "cy", "r")
    elif tag == "line":
        attributes = ("x1", "y1", "x2", "y2")
    elif tag == "text":
        attributes = ("x", "y")
    if not attributes:
        return True
    values = [
        _float(element.get(attribute, "0" if tag == "rect" and attribute in {"x", "y"} else None))
        for attribute in attributes
    ]
    if any(value is None for value in values):
        return False
    coordinates = [float(value) for value in values if value is not None]
    if tag == "rect":
        x, y, w, h = coordinates
        return x >= 0 and y >= 0 and w > 0 and h > 0 and x + w <= width and y + h <= height
    if tag in {"ellipse", "circle"}:
        x, y, rx = coordinates[:3]
        ry = coordinates[3] if tag == "ellipse" else rx
        return (
            rx > 0
            and ry > 0
            and x - rx >= 0
            and x + rx <= width
            and y - ry >= 0
            and y + ry <= height
        )
    if tag == "line":
        x1, y1, x2, y2 = coordinates
        return all(0 <= x <= width for x in (x1, x2)) and all(0 <= y <= height for y in (y1, y2))
    x, y = coordinates
    return 0 <= x <= width and 0 <= y <= height


def validate_svg(source: str) -> list[str]:
    """Return deterministic errors for a synthetic, text-only SVG illustration."""
    errors: list[str] = []
    if PROHIBITED_DECLARATIONS.search(source):
        errors.append("prohibited XML declaration")
        return errors
    try:
        root = ET.fromstring(source)  # nosec B314 - Checked-in SVG only; DTD/entities rejected.
    except ET.ParseError:
        return ["invalid SVG XML"]
    if root.tag != f"{{{SVG_NS}}}svg":
        return ["root must be a namespaced SVG"]
    if root.get("role") != "img" or not (root.get("aria-label") or "").strip():
        errors.append("missing accessible image role or label")
    view_box = (root.get("viewBox") or "").replace(",", " ").split()
    dimensions = [_float(value) for value in view_box]
    if len(dimensions) != 4 or any(value is None for value in dimensions):
        errors.append("invalid viewBox")
        return errors
    x0, y0, width, height = (float(value) for value in dimensions if value is not None)
    if x0 != 0 or y0 != 0 or width <= 0 or height <= 0 or width > 4096 or height > 4096:
        errors.append("unsupported viewBox geometry")
        return errors
    if _float(root.get("width")) != width or _float(root.get("height")) != height:
        errors.append("root dimensions must match viewBox")
    ids: set[str] = set()
    references: set[str] = set()
    for element in root.iter():
        if not element.tag.startswith(f"{{{SVG_NS}}}") or _name(element.tag) not in ALLOWED_TAGS:
            errors.append(f"unsupported SVG element: {_name(element.tag)}")
        identifier = element.get("id")
        if identifier:
            if identifier in ids:
                errors.append(f"duplicate element id: {identifier}")
            ids.add(identifier)
        if not _geometry(element, width, height):
            errors.append(f"out-of-bounds or invalid geometry: {_name(element.tag)}")
        for key, value in element.attrib.items():
            attribute = _name(key).lower()
            lower_value = value.lower()
            if attribute.startswith("on") or attribute in {"href", "src", "style"}:
                errors.append(f"unsafe SVG attribute: {attribute}")
            if any(token in lower_value for token in ("javascript:", "data:", "<script")):
                errors.append(f"unsafe SVG attribute value: {attribute}")
            for url_match in URL_VALUE.finditer(value):
                local = LOCAL_URL.fullmatch(url_match.group())
                if local is None:
                    errors.append(f"external SVG URL: {attribute}")
                else:
                    references.add(local.group(1))
    missing_references = sorted(references - ids)
    errors.extend(
        f"missing internal SVG reference: {identifier}" for identifier in missing_references
    )
    visible_text = " ".join(
        "".join(element.itertext()) for element in root.iter() if _name(element.tag) == "text"
    )
    if "synthetic" not in (visible_text + " " + (root.get("aria-label") or "")).lower():
        errors.append("missing synthetic-data notice")
    if "boundary" not in visible_text.lower():
        errors.append("missing visible interpretation boundary")
    return errors


def validate_directory(repository: Path) -> list[str]:
    """Fail closed for a missing, extra, malformed or unsafe proposal SVG."""
    directory = repository / VISUALS_DIR
    if not directory.is_dir():
        return [f"missing proposal visual directory: {VISUALS_DIR}"]
    actual = {path.name for path in directory.glob("*.svg") if path.is_file()}
    errors = [f"missing illustration: {name}" for name in sorted(EXPECTED_FILES - actual)]
    errors.extend(f"unregistered illustration: {name}" for name in sorted(actual - EXPECTED_FILES))
    for name in sorted(EXPECTED_FILES & actual):
        path = directory / name
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{name}: unreadable SVG")
            continue
        errors.extend(f"{name}: {problem}" for problem in validate_svg(source))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    problems = validate_directory(args.repository)
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print(f"Verified {len(EXPECTED_FILES)} synthetic proposal SVG sources (structural checks only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
