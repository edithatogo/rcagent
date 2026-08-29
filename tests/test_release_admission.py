from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.release_admission import release_input_paths, validate_release_inventory


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    repository = tmp_path / "repository"
    skill = repository / "skills/rca-investigation"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: fixture\n---\n")
    for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION"):
        (repository / name).write_text(f"{name}\n")
    records = []
    for path in release_input_paths(repository):
        records.append({
            "path": path.relative_to(repository).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "rights_basis": "repository_authored_or_apache_licensed",
            "author": "rcagent repository contributors",
            "source": "https://github.com/edithatogo/rcagent",
            "licence": "Apache-2.0",
            "data_class": "public_no_personal_data",
        })
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps({"schema_version": "1.0", "licence": "Apache-2.0", "files": records}))
    return repository, inventory


def test_release_admission_requires_exact_complete_inventory(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    validate_release_inventory(repository, inventory)
    (repository / "skills/rca-investigation/unexpected.md").write_text("unexpected")
    with pytest.raises(ValueError, match="stale or incomplete"):
        validate_release_inventory(repository, inventory)


def test_release_admission_rejects_hash_drift_and_sensitive_sentinel(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    skill = repository / "skills/rca-investigation/SKILL.md"
    skill.write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_release_inventory(repository, inventory)
    repository, inventory = _fixture(tmp_path / "second")
    skill = repository / "skills/rca-investigation/SKILL.md"
    skill.write_text("api_key=abcdefghijk")
    value = json.loads(inventory.read_text())
    record = next(item for item in value["files"] if item["path"].endswith("SKILL.md"))
    record["sha256"] = hashlib.sha256(skill.read_bytes()).hexdigest()
    inventory.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="credential or private-data"):
        validate_release_inventory(repository, inventory)
