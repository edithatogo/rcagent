from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.validate_repository import REQUIRED_CONTEXT, main, validate


def _write_valid_repository(root: Path) -> None:
    for relative in REQUIRED_CONTEXT:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}" if path.suffix == ".json" else "# Context\n", encoding="utf-8")

    (root / "conductor/capability-profiles.json").write_text(
        json.dumps(
            {
                "$schema": "schemas/capability-profiles.schema.json",
                "schema_version": "1.0",
                "default_profile": "core",
                "policy": "optional-capabilities-must-not-weaken-core-safeguards",
                "installation_contract": {
                    "agent_assisted": True,
                    "scripted": True,
                    "idempotent": True,
                    "preflight_required": True,
                    "verification_required": True,
                    "receipt_required": True,
                    "rollback_required": True,
                    "uninstall_required": True,
                    "network_egress_requires_disclosure": True,
                    "telemetry_default": "off",
                    "planned_is_not_installable": True,
                },
                "profiles": [
                    {"id": "core", "class": "core", "status": "implemented", "default": True, "owner_track": 0}
                ],
            }
        ),
        encoding="utf-8",
    )

    track = root / "conductor/tracks/example_20260731"
    track.mkdir(parents=True)
    (track / "index.md").write_text("# Example\n", encoding="utf-8")
    (track / "spec.md").write_text("# Specification\n", encoding="utf-8")
    (track / "plan.md").write_text(
        "continue automatically.\n"
        "do not ask for routine approval.\n"
        "Present a recommendation and safe default.\n",
        encoding="utf-8",
    )
    (track / "metadata.json").write_text(
        json.dumps(
            {
                "github": {
                    "issue": "https://github.com/edithatogo/rcagent/issues/5"
                }
            }
        ),
        encoding="utf-8",
    )
    (root / "conductor/roadmap.json").write_text(
        json.dumps(
            {"tracks": [{"number": 0, "id": "example_20260731", "issue": 5}]}
        ),
        encoding="utf-8",
    )
    (root / "conductor/integration-map.json").write_text(
        json.dumps(
            {
                "tracks": [
                    {
                        "track_id": "example_20260731",
                        "candidate_systems": ["existing-system"],
                        "project_owned_gap": "bounded test gap",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (root / "conductor/clinical-governance-architecture.json").write_text(
        json.dumps(
            {
                "layers": [{"id": "lifecycle", "owner_tracks": [0]}],
                "integrations": [
                    {
                        "id": "citations",
                        "owner_track": 0,
                        "validation_track": 0
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_repository_fixture_passes(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    assert validate(tmp_path) == []


def test_capability_registry_matches_published_schema() -> None:
    root = Path(__file__).parents[1]
    schema = json.loads(
        (root / "conductor/schemas/capability-profiles.schema.json").read_text(encoding="utf-8")
    )
    registry = json.loads(
        (root / "conductor/capability-profiles.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(registry)


def test_missing_context_is_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    (tmp_path / "conductor/autonomy.json").unlink()
    assert "missing required context: conductor/autonomy.json" in validate(tmp_path)


def test_duplicate_issue_and_missing_contract_are_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    second = tmp_path / "conductor/tracks/second_20260731"
    second.mkdir()
    for name in ("index.md", "spec.md"):
        (second / name).write_text("# Example\n", encoding="utf-8")
    (second / "plan.md").write_text("# Plan\n", encoding="utf-8")
    (second / "metadata.json").write_text(
        json.dumps(
            {
                "github": {
                    "issue": "https://github.com/edithatogo/rcagent/issues/5"
                }
            }
        ),
        encoding="utf-8",
    )
    roadmap_path = tmp_path / "conductor/roadmap.json"
    roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
    roadmap["tracks"].append(
        {"number": 1, "id": "second_20260731", "issue": 5}
    )
    roadmap_path.write_text(json.dumps(roadmap), encoding="utf-8")

    errors = validate(tmp_path)
    assert "duplicate GitHub issue mapping: #5" in errors
    assert any("continuous execution contract missing" in error for error in errors)


def test_invalid_roadmap_json_is_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    (tmp_path / "conductor/roadmap.json").write_text("{", encoding="utf-8")
    assert any("invalid conductor/roadmap.json" in error for error in validate(tmp_path))


def test_invalid_track_fields_and_missing_files_are_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    roadmap_path = tmp_path / "conductor/roadmap.json"
    roadmap_path.write_text(
        json.dumps(
            {
                "tracks": [
                    {"number": 0, "id": "example_20260731", "issue": 5},
                    {"number": 1, "id": "example_20260731", "issue": 7},
                    {"number": 2, "id": "missing_20260731", "issue": 6},
                    {"number": 3, "id": "invalid_issue_20260731", "issue": 0},
                    {"number": 4, "id": "", "issue": 8},
                ]
            }
        ),
        encoding="utf-8",
    )
    errors = validate(tmp_path)
    assert "duplicate roadmap track id: example_20260731" in errors
    assert "roadmap track has no valid id" in errors
    assert any("missing index.md" in error for error in errors)
    assert any("invalid GitHub issue" in error for error in errors)


def test_unknown_clinical_governance_owners_are_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    architecture = tmp_path / "conductor/clinical-governance-architecture.json"
    architecture.write_text(
        json.dumps(
            {
                "layers": [
                    {"id": "lifecycle", "owner_tracks": [999]},
                    {"id": "lifecycle", "owner_tracks": []}
                ],
                "integrations": [
                    {
                        "id": "sourceright",
                        "owner_track": 999,
                        "validation_track": 0
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    errors = validate(tmp_path)
    assert "lifecycle: unknown owner track number: 999" in errors
    assert "duplicate clinical governance layer id: lifecycle" in errors
    assert "sourceright: unknown owner_track number: 999" in errors


def test_invalid_metadata_and_wrong_issue_mapping_are_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    metadata = tmp_path / "conductor/tracks/example_20260731/metadata.json"
    metadata.write_text("{", encoding="utf-8")
    assert any("invalid metadata.json" in error for error in validate(tmp_path))

    metadata.write_text(
        json.dumps(
            {
                "github": {
                    "issue": "https://github.com/edithatogo/rcagent/issues/999"
                }
            }
        ),
        encoding="utf-8",
    )
    assert any("issue mapping does not match #5" in error for error in validate(tmp_path))


def test_adopted_integration_requires_lifecycle_fields(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    integration_map = tmp_path / "conductor/integration-map.json"
    integration_map.write_text(
        json.dumps(
            {
                "tracks": [
                    {
                        "track_id": "example_20260731",
                        "status": "adapt",
                        "candidate_systems": ["existing-system"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    errors = validate(tmp_path)
    assert "example_20260731: adopted integration missing selected_system" in errors
    assert "example_20260731: adopted integration missing evidence" in errors


def test_unknown_and_duplicate_integration_tracks_are_reported(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    integration_map = tmp_path / "conductor/integration-map.json"
    integration_map.write_text(
        json.dumps(
            {
                "tracks": [
                    {"track_id": "unknown", "candidate_systems": ["one"]},
                    {"track_id": "unknown", "candidate_systems": []},
                ]
            }
        ),
        encoding="utf-8",
    )
    errors = validate(tmp_path)
    assert "integration-map has unknown track id: unknown" in errors
    assert "duplicate integration-map track id: unknown" in errors
    assert "unknown: candidate_systems must be non-empty" in errors


def test_capability_profile_semantics_are_enforced(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    path = tmp_path / "conductor/capability-profiles.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["profiles"].append(
        {"id": "core", "class": "optional", "status": "planned", "default": True, "owner_track": 99}
    )
    path.write_text(json.dumps(registry), encoding="utf-8")
    errors = validate(tmp_path)
    assert "duplicate capability profile id: core" in errors
    assert "core: non-implemented profile cannot be default" in errors
    assert "core: unknown owner track number" in errors
    assert "capability registry requires exactly one default profile" in errors
    assert "core capability profile must be implemented and class core" in errors


def test_implemented_optional_profile_requires_contract(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    path = tmp_path / "conductor/capability-profiles.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["profiles"].append(
        {"id": "validate", "class": "optional", "status": "implemented", "default": False, "owner_track": 0}
    )
    path.write_text(json.dumps(registry), encoding="utf-8")
    assert "validate: implemented profile requires implementation contract" in validate(tmp_path)


def test_capability_installation_safeguards_fail_closed(tmp_path: Path) -> None:
    _write_valid_repository(tmp_path)
    path = tmp_path / "conductor/capability-profiles.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["installation_contract"]["telemetry_default"] = "on"
    registry["installation_contract"]["planned_is_not_installable"] = False
    path.write_text(json.dumps(registry), encoding="utf-8")
    errors = validate(tmp_path)
    assert "capability installation_contract requires telemetry_default=off" in errors
    assert "capability installation_contract requires planned_is_not_installable=true" in errors


def test_missing_roadmap_returns_context_diagnostics(tmp_path: Path) -> None:
    errors = validate(tmp_path)
    assert "missing required context: conductor/roadmap.json" in errors


def test_main_reports_success_and_failure(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _write_valid_repository(tmp_path)
    monkeypatch.setattr(sys, "argv", ["validate_repository", "--root", str(tmp_path)])
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out

    (tmp_path / "conductor/autonomy.json").unlink()
    assert main() == 1
    assert "missing required context" in capsys.readouterr().out
