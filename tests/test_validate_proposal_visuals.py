from __future__ import annotations

from pathlib import Path

import pytest

from tools.validate_proposal_visuals import (
    EXPECTED_FILES,
    ROOT,
    VISUALS_DIR,
    validate_directory,
    validate_svg,
)

VALID = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"
width="200" height="100" role="img" aria-label="Synthetic safety diagram">
<defs><marker id="arr" markerWidth="5" markerHeight="5"><path d="M0 0 L5 2 L0 5Z"/></marker></defs>
<rect x="10" y="10" width="180" height="50"/>
<text x="20" y="40">Synthetic example: boundary is not evidence</text>
<path d="M20 20 L50 20" marker-end="url(#arr)"/>
</svg>"""


def test_valid_synthetic_svg() -> None:
    assert validate_svg(VALID) == []


@pytest.mark.parametrize(
    ("mutated", "message"),
    [
        (VALID.replace('role="img"', 'role="button"'), "missing accessible"),
        (VALID.replace('aria-label="Synthetic safety diagram"', ""), "missing accessible"),
        (VALID.replace('viewBox="0 0 200 100"', 'viewBox="0 0 0 100"'), "unsupported viewBox"),
        (VALID.replace('viewBox="0 0 200 100"', 'viewBox="not-a-box"'), "invalid viewBox"),
        (VALID.replace('width="180"', 'width="260"'), "out-of-bounds"),
        (VALID.replace("<rect ", '<rect onload="alert(1)" '), "unsafe SVG attribute"),
        (VALID.replace("<rect ", "<foreignObject/><rect "), "unsupported SVG element"),
        (VALID.replace("url(#arr)", "url(https://example.org/evil.svg)"), "external SVG URL"),
        (VALID.replace("url(#arr)", "url(#missing)"), "missing internal SVG reference"),
        (VALID.replace("<rect ", '<rect id="arr" '), "duplicate element id"),
        (
            VALID.replace("boundary is not evidence", "uncertain"),
            "missing visible interpretation boundary",
        ),
        (
            VALID.replace("Synthetic safety diagram", "Safety diagram").replace(
                "Synthetic example:", "Example:"
            ),
            "missing synthetic-data notice",
        ),
        (VALID.replace("<svg", "<html").replace("</svg>", "</html>"), "root must be"),
        (VALID + "<script/>", "invalid SVG XML"),
        ('<!DOCTYPE svg [<!ENTITY pwn "x">]>' + VALID, "prohibited XML declaration"),
        (VALID.replace('marker-end="url(#arr)"', 'style="x:y"'), "unsafe SVG attribute"),
    ],
)
def test_rejects_unsafe_or_misleading_input(mutated: str, message: str) -> None:
    assert any(message in problem for problem in validate_svg(mutated))


def test_directory_missing_is_not_pass(tmp_path: Path) -> None:
    assert "missing proposal visual directory" in validate_directory(tmp_path)[0]


def test_missing_or_unregistered_figure_is_rejected(tmp_path: Path) -> None:
    directory = tmp_path / VISUALS_DIR
    directory.mkdir(parents=True)
    (directory / "unexpected.svg").write_text(VALID)
    problems = validate_directory(tmp_path)
    assert sum("missing illustration" in p for p in problems) == len(EXPECTED_FILES)
    assert "unregistered illustration: unexpected.svg" in problems


def test_registered_synthetic_figures_pass(tmp_path: Path) -> None:
    directory = tmp_path / VISUALS_DIR
    directory.mkdir(parents=True)
    for filename in EXPECTED_FILES:
        (directory / filename).write_text(VALID, encoding="utf-8")
    assert validate_directory(tmp_path) == []


def test_malformed_registered_figure_fails_directory(tmp_path: Path) -> None:
    directory = tmp_path / VISUALS_DIR
    directory.mkdir(parents=True)
    for filename in EXPECTED_FILES:
        (directory / filename).write_text(VALID, encoding="utf-8")
    first = min(EXPECTED_FILES)
    (directory / first).write_text(VALID.replace("url(#arr)", "url(#bad)"), encoding="utf-8")
    assert any(
        first in p and "missing internal SVG reference" in p for p in validate_directory(tmp_path)
    )


@pytest.mark.parametrize(
    "element",
    [
        '<ellipse cx="60" cy="50" rx="30" ry="20"/>',
        '<circle cx="60" cy="50" r="10"/>',
        '<line x1="0" y1="0" x2="200" y2="100"/>',
        '<text x="100" y="60">Valid</text>',
    ],
)
def test_all_supported_shape_geometries(element: str) -> None:
    source = VALID.replace('<rect x="10" y="10" width="180" height="50"/>', element)
    assert validate_svg(source) == []


@pytest.mark.parametrize(
    "element",
    [
        '<ellipse cx="20" cy="50" rx="30" ry="20"/>',
        '<circle cx="190" cy="50" r="15"/>',
        '<line x1="-2" y1="0" x2="200" y2="100"/>',
        '<text x="201" y="60">Invalid</text>',
        '<rect x="10" y="10" width="NaN" height="50"/>',
        '<rect x="10" y="10" width="0" height="50"/>',
    ],
)
def test_geometry_rejects_off_canvas_shapes(element: str) -> None:
    source = VALID.replace('<rect x="10" y="10" width="180" height="50"/>', element)
    assert any("out-of-bounds" in item for item in validate_svg(source))


def test_directory_reports_actual_malformed_svg(tmp_path: Path) -> None:
    directory = tmp_path / VISUALS_DIR
    directory.mkdir(parents=True)
    for name in EXPECTED_FILES:
        (directory / name).write_text(VALID, encoding="utf-8")
    invalid = min(EXPECTED_FILES)
    (directory / invalid).write_text("<svg xmlns='http://www.w3.org/2000/svg'", encoding="utf-8")
    assert f"{invalid}: invalid SVG XML" in validate_directory(tmp_path)


def test_main_cli_on_valid_directory(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from tools.validate_proposal_visuals import main

    directory = tmp_path / VISUALS_DIR
    directory.mkdir(parents=True)
    for name in EXPECTED_FILES:
        (directory / name).write_text(VALID, encoding="utf-8")
    assert main([str(tmp_path)]) == 0
    assert "Verified 10 synthetic" in capsys.readouterr().out


def test_main_cli_reports_missing_directory(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from tools.validate_proposal_visuals import main

    assert main([str(tmp_path)]) == 1
    assert "missing proposal visual directory" in capsys.readouterr().out


def test_checked_in_proposal_assets_pass_all_structural_gates() -> None:
    # This checks actual PR source assets, not just the isolated synthetic test fixtures.
    assert validate_directory(ROOT) == []
