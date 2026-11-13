"""Require complete, executable branch-coverage inputs before matrix combination."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath

from coverage import CoverageData
from coverage.exceptions import CoverageException

MATRIX_ARTIFACTS = frozenset(
    {
        "coverage-data-ubuntu-latest-py3.15.2",
        "coverage-data-ubuntu-latest-py3.11",
        "coverage-data-macos-latest-py3.15.2",
        "coverage-data-windows-latest-py3.15.2",
    }
)


def validate_inputs(directory: Path, *, repository: Path) -> list[Path]:
    """Reject missing, corrupt, empty or out-of-scope matrix measurements.

    Coverage's combine command can warn about an unreadable shard and continue.
    Validate every expected shard before that command can accept a partial union.
    The workflow downloads only artifacts from its own run and keeps one directory
    per matrix member, so different platforms cannot overwrite each other's data.
    """
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("coverage input directory is missing or invalid")
    children = {path.name: path for path in directory.iterdir()}
    if children.keys() != MATRIX_ARTIFACTS:
        raise ValueError("coverage inputs differ from the complete required matrix")
    paths: list[Path] = []
    for name in sorted(MATRIX_ARTIFACTS):
        folder = children[name]
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"coverage artifact directory is invalid: {name}")
        path = folder / ".coverage"
        if {item.name for item in folder.iterdir()} != {".coverage"}:
            raise ValueError(f"coverage artifact contents are invalid: {name}")
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"coverage database is missing or invalid: {name}")
        data = CoverageData(basename=str(path))
        try:
            data.read()
        except CoverageException as error:
            raise ValueError(f"coverage database is unreadable: {name}") from error
        measured = data.measured_files()
        if not measured or not data.has_arcs():
            raise ValueError(f"coverage database lacks branch measurements: {name}")
        if not any(data.arcs(filename) for filename in measured):
            raise ValueError(f"coverage database lacks executed branches: {name}")
        for filename in measured:
            relative = PurePosixPath(filename.replace("\\", "/"))
            if (
                relative.is_absolute()
                or not relative.parts
                or relative.parts[0] != "tools"
                or ".." in relative.parts
                or relative.suffix != ".py"
                or not (repository / relative).is_file()
            ):
                raise ValueError(f"coverage source is outside the current tools: {name}")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    paths = validate_inputs(args.directory, repository=Path.cwd())
    print(f"Validated branch measurements from all {len(paths)} required matrix members.")
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised through the workflow
    raise SystemExit(main())
