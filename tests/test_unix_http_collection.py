"""Keep collection metadata safe even when Unix-only tests skip on Windows."""

import subprocess
import sys
from pathlib import Path


def test_transport_node_ids_are_bounded():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-o",
            "addopts=",
            "tests/test_unix_http_capture.py",
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    node_ids = [line for line in result.stdout.splitlines() if "::test_" in line]
    assert node_ids
    # Pytest writes node IDs to PYTEST_CURRENT_TEST even for skipped tests.
    # Do not include arbitrarily large synthetic payloads in this metadata.
    assert max(map(len, node_ids)) < 512
