from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.json_shapes import JsonObject, is_array, require_object
from tools.release_admission import release_input_paths, validate_release_inventory


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    repository = tmp_path / "repository"
    skill = repository / "skills/rca-investigation"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: fixture\n---\n")
    for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION"):
        (repository / name).write_text(f"{name}\n")
    records: list[dict[str, str]] = []
    for path in release_input_paths(repository):
        records.append(
            {
                "path": path.relative_to(repository).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "rights_basis": "repository_authored_or_apache_licensed",
                "author": "rcagent repository contributors",
                "source": "https://github.com/edithatogo/rcagent",
                "licence": "Apache-2.0",
                "data_class": "public_no_personal_data",
            }
        )
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps({"schema_version": "1.0", "licence": "Apache-2.0", "files": records})
    )
    return repository, inventory


def test_release_admission_requires_exact_complete_inventory(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    assert validate_release_inventory(repository, inventory) == json.loads(inventory.read_text())
    (repository / "skills/rca-investigation/unexpected.md").write_text("unexpected")
    with pytest.raises(ValueError, match="stale or incomplete"):
        validate_release_inventory(repository, inventory)


def test_release_admission_rejects_hash_drift_and_sensitive_sentinel(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    skill = repository / "skills/rca-investigation/SKILL.md"
    skill.write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_release_inventory(repository, inventory)


def _files(value: JsonObject) -> list[object]:
    records = value["files"]
    assert is_array(records)
    return records


@pytest.mark.parametrize(
    ("target", "field", "replacement", "message"),
    [
        ("inventory", "schema_version", "2.0", "metadata"),
        ("inventory", "files", "wrong", "files"),
        ("record", "path", 123, "record is invalid"),
        ("duplicate", "", None, "duplicate"),
        ("record", "rights_basis", "unknown", "rights"),
        ("record", "author", "unknown", "authorship"),
        ("record", "licence", "unknown", "data or licence"),
        ("record", "sha256", "bad", "hash is invalid"),
        ("record", "sha256", int("1" * 64), "hash is invalid"),
    ],
)
def test_release_admission_rejects_malformed_records(
    tmp_path: Path, target: str, field: str, replacement: object, message: str
) -> None:
    repository, inventory = _fixture(tmp_path)
    value = require_object(json.loads(inventory.read_text()), context="fixture inventory")
    if target == "inventory":
        value[field] = replacement
    elif target == "record":
        require_object(_files(value)[0], context="fixture record")[field] = replacement
    else:
        assert target == "duplicate"
        _files(value).append(dict(require_object(_files(value)[0], context="fixture record")))
    inventory.write_text(json.dumps(value))
    with pytest.raises(ValueError, match=message):
        validate_release_inventory(repository, inventory)


@pytest.mark.parametrize("value", [None, []])
def test_release_inventory_requires_an_object(tmp_path: Path, value: object) -> None:
    repository, inventory = _fixture(tmp_path)
    inventory.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="inventory metadata is invalid"):
        validate_release_inventory(repository, inventory)


def test_release_inventory_requires_object_records(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    value = require_object(json.loads(inventory.read_text()), context="fixture inventory")
    _files(value)[0] = None
    inventory.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="inventory record is invalid"):
        validate_release_inventory(repository, inventory)


def test_release_admission_rejects_sensitive_content_with_matching_hash(tmp_path: Path) -> None:
    repository, inventory = _fixture(tmp_path)
    skill = repository / "skills/rca-investigation/SKILL.md"
    skill.write_text("api_key=abcdefghijk")
    value = require_object(json.loads(inventory.read_text()), context="fixture inventory")
    records = [require_object(item, context="fixture record") for item in _files(value)]
    record = next(item for item in records if item["path"] == "skills/rca-investigation/SKILL.md")
    record["sha256"] = hashlib.sha256(skill.read_bytes()).hexdigest()
    inventory.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="credential or private-data"):
        validate_release_inventory(repository, inventory)
