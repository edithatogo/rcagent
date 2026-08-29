from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools import build_client_plugins as plugin_module
from tools import build_distribution as distribution_module
from tools import build_release_candidate as candidate_module
from tools.build_release_candidate import build_release_candidate

ROOT = Path(__file__).parents[1]
REVISION = "2" * 40


@pytest.fixture(autouse=True)
def _unit_release_source(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(plugin_module, "verify_release_source", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(distribution_module, "verify_release_source", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(candidate_module, "validate_release_inventory", lambda *_args, **_kwargs: {})


def test_release_candidate_is_deterministic_hash_bound_and_public_only(tmp_path: Path) -> None:
    first = build_release_candidate(ROOT, tmp_path / "first", version="0.1.0", source_revision=REVISION)
    second = build_release_candidate(ROOT, tmp_path / "second", version="0.1.0", source_revision=REVISION)
    assert [path.name for path in first.files] == [path.name for path in second.files]
    for left, right in zip(first.files, second.files, strict=True):
        assert left.read_bytes() == right.read_bytes()
    assert first.manifest["release_state"] == "candidate_not_published"
    assert first.manifest["private_data"] is False
    assert first.manifest["third_party_controlled_bytes"] is False
    lines = (first.destination / "MANIFEST.sha256").read_text().splitlines()
    for line in lines:
        digest, name = line.split("  ", 1)
        assert hashlib.sha256((first.destination / name).read_bytes()).hexdigest() == digest
    checked = json.loads((first.destination / "release-candidate.json").read_text())
    assert checked == first.manifest


def test_release_candidate_refuses_nonempty_destination(tmp_path: Path) -> None:
    destination = tmp_path / "candidate"
    destination.mkdir()
    (destination / "preserve").write_text("preserve")
    with pytest.raises(FileExistsError, match="empty"):
        build_release_candidate(ROOT, destination, version="0.1.0", source_revision=REVISION)
