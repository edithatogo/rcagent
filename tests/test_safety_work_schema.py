"""Schema and fixture validation for the canonical safety-work record."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).parents[1]
SCHEMA = ROOT / "conductor/schemas/safety-work.schema.json"


def _load_sample() -> dict:
    """A minimal but complete valid record exercising every top-level section."""
    return {
        "schema_version": "1.1",
        "case_id": "case-2026-001",
        "version": 1,
        "state": "investigation",
        "jurisdiction": "AU-NSW",
        "privacy_mode": "fully_local",
        "authority": "Local health district clinical governance committee",
        "confidentiality": "privileged-quality-assurance",
        "roles": [
            {"role_id": "role-investigator", "role_type": "investigator", "authority": "appointed"}
        ],
        "sources": [
            {
                "source_id": "source-incident-report",
                "source_type": "record",
                "title": "Incident report [Case ID]",
                "fingerprint": "sha256:" + "0" * 64,
                "acquired_at": "2026-08-29T00:00:00Z",
                "authority": "ims+ system of record",
            }
        ],
        "artefacts": [],
        "evidence": [],
        "statements": [],
        "factors": [],
        "relationships": [],
        "events": [
            {
                "event_id": "event-intake",
                "event_type": "submission_received",
                "occurred_at": "2026-08-29T00:00:00Z",
                "actor_role_id": "role-investigator",
                "from_state": "intake",
                "to_state": "triage",
                "authority": "Local health district clinical governance committee",
            }
        ],
        "actions": [],
        "reviews": [
            {
                "review_id": "review-huddle",
                "review_type": "huddle",
                "reviewer_role_ids": ["role-investigator"],
                "status": "complete",
            }
        ],
        "outcomes": [],
        "referrals": [],
    }


def test_schema_is_valid_draft_2020_12() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)


def test_complete_sample_record_validates() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(_load_sample(), schema)


def test_evidence_withdrawal_event_may_retain_state() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    record = _load_sample()
    record["events"].append(
        {
            "event_id": "event-withdraw-evidence",
            "event_type": "evidence_withdrawn",
            "occurred_at": "2026-08-29T01:00:00Z",
            "actor_role_id": "role-investigator",
            "from_state": "triage",
            "to_state": "triage",
            "authority": "Local health district clinical governance committee",
        }
    )
    jsonschema.validate(record, schema)


def test_unknown_top_level_section_is_rejected() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    record = _load_sample()
    record["shadow_state"] = []
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(record, schema)


def test_invalid_state_enum_is_rejected() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    record = _load_sample()
    record["state"] = "on_hold"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(record, schema)


def test_schema_file_tracks_declared_sections() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    expected = {
        "roles", "sources", "artefacts", "evidence", "statements", "factors",
        "relationships", "events", "actions", "reviews", "outcomes", "referrals",
        "system_of_record",
    }
    assert expected <= set(schema["properties"]), "canonical model lost sections"
