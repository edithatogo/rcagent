"""Complete matrix evidence must precede the unchanged combined coverage floor."""

from __future__ import annotations

import gc
import subprocess
import sys
import warnings
from pathlib import Path

import pytest
from coverage import CoverageData

from tools.coverage_inputs import MATRIX_ARTIFACTS, main, validate_inputs

TRUE_ARCS = [(-1, 1), (1, 2), (2, 3), (3, -1)]
FALSE_ARCS = [(-1, 1), (1, 2), (2, 5), (5, -1)]


def write_data(path: Path, *, filename: str = "tools/sample.py", arcs: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = CoverageData(basename=str(path))
    if arcs:
        data.add_arcs({filename: TRUE_ARCS})
    else:
        data.add_lines({filename: [1, 2, 3]})
    data.write()


@pytest.fixture
def matrix(tmp_path: Path) -> tuple[Path, Path]:
    repository = tmp_path / "repo"
    (repository / "tools").mkdir(parents=True)
    (repository / "tools/sample.py").write_text(
        "flag = True\nif flag:\n    result = 1\nelse:\n    result = 2\n", encoding="utf-8"
    )
    (repository / "pyproject.toml").write_text(
        '[tool.coverage.run]\nbranch = true\nrelative_files = true\nsource = ["tools"]\n'
        "[tool.coverage.report]\nfail_under = 90\n",
        encoding="utf-8",
    )
    directory = repository / "coverage-inputs"
    for name in MATRIX_ARTIFACTS:
        write_data(directory / name / ".coverage")
    return repository, directory


def test_all_required_branch_inputs_are_retained(
    matrix: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repository, directory = matrix
    paths = validate_inputs(directory, repository=repository)
    assert len(paths) == 4
    assert all(path.is_file() for path in paths)
    monkeypatch.chdir(repository)
    assert main([str(directory)]) == 0
    assert "all 4 required matrix members" in capsys.readouterr().out


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_partial_or_unexpected_matrix_cannot_pass(matrix: tuple[Path, Path], change: str) -> None:
    repository, directory = matrix
    if change == "missing":
        folder = directory / min(MATRIX_ARTIFACTS)
        (folder / ".coverage").unlink()
        folder.rmdir()
    else:
        (directory / "unexpected-platform").mkdir()
    with pytest.raises(ValueError, match="complete required matrix"):
        validate_inputs(directory, repository=repository)


@pytest.mark.parametrize("change", ["missing", "corrupt", "line-only", "empty-branches"])
def test_non_measurement_shard_cannot_pass(matrix: tuple[Path, Path], change: str) -> None:
    repository, directory = matrix
    path = directory / min(MATRIX_ARTIFACTS) / ".coverage"
    path.unlink()
    if change == "corrupt":
        path.write_bytes(b"not a coverage database")
    elif change == "line-only":
        write_data(path, arcs=False)
    elif change == "empty-branches":
        data = CoverageData(basename=str(path))
        data.add_arcs({"tools/sample.py": []})
        data.write()
    with pytest.raises(ValueError, match=r"coverage (artifact|database)"):
        validate_inputs(directory, repository=repository)


def test_corrupt_database_rejection_closes_its_connection(matrix: tuple[Path, Path]) -> None:
    repository, directory = matrix
    path = directory / min(MATRIX_ARTIFACTS) / ".coverage"
    path.write_bytes(b"not a coverage database")
    gc.collect()
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always", ResourceWarning)
        with pytest.raises(ValueError, match="coverage database is unreadable"):
            validate_inputs(directory, repository=repository)
        gc.collect()
    assert not [warning for warning in observed if issubclass(warning.category, ResourceWarning)]


@pytest.mark.parametrize(
    "filename", ["/tmp/sample.py", "tools/../sample.py", "unrelated.py", "tools/missing.py"]
)
def test_foreign_or_missing_source_cannot_supply_coverage(
    matrix: tuple[Path, Path], filename: str
) -> None:
    repository, directory = matrix
    path = directory / min(MATRIX_ARTIFACTS) / ".coverage"
    path.unlink()
    write_data(path, filename=filename)
    with pytest.raises(ValueError, match="outside the current tools"):
        validate_inputs(directory, repository=repository)


def test_missing_input_directory_cannot_pass(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="directory is missing"):
        validate_inputs(tmp_path / "missing", repository=tmp_path)


@pytest.mark.parametrize("cover_other_branch", [False, True])
def test_real_combine_normalises_platform_paths_and_enforces_ninety_percent(
    matrix: tuple[Path, Path], cover_other_branch: bool
) -> None:
    repository, directory = matrix
    windows = directory / "coverage-data-windows-latest-py3.15.2" / ".coverage"
    windows.unlink()
    data = CoverageData(basename=str(windows))
    data.add_arcs({r"tools\sample.py": FALSE_ARCS if cover_other_branch else TRUE_ARCS})
    data.write()
    paths = validate_inputs(directory, repository=repository)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "combine", "--keep", *map(str, paths)],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    combined = CoverageData(basename=str(repository / ".coverage"))
    combined.read()
    measured = combined.measured_files()
    assert len(measured) == 1
    assert {name.replace("\\", "/") for name in measured} == {"tools/sample.py"}
    assert all(path.is_file() for path in paths)
    report = subprocess.run(
        [sys.executable, "-m", "coverage", "report", "--fail-under=90"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    assert report.returncode == (0 if cover_other_branch else 2), report.stdout + report.stderr
