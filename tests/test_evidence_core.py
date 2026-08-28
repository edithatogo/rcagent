from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from tools.evidence_core import can_transition, canonical_round_trip, load_schema, validate_record

FIXTURE = Path(__file__).parent / "fixtures/safety-work/valid-case.json"


def record() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_schema_and_round_trip() -> None:
    assert load_schema()["$defs"]["statement"]["properties"]["kind"]
    value = record()
    assert validate_record(value) == []
    assert canonical_round_trip(value) == value


def test_invalid_statement_kind_and_reference_fail() -> None:
    value = record()
    value["statements"][0]["kind"] = "truth"
    value["relationships"][0]["to_id"] = "missing-id"
    errors = validate_record(value)
    assert any("is not one of" in error for error in errors)
    assert "relationships: unknown to_id 'missing-id'" in errors
    with pytest.raises(ValueError, match="invalid safety-work record"):
        canonical_round_trip(value)


def test_lifecycle_is_explicit_and_fail_closed() -> None:
    assert can_transition("review", "investigation")
    assert can_transition("closed", "reopened")
    assert not can_transition("intake", "closed")
    assert not can_transition("unknown", "review")


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda value: value["roles"].append(deepcopy(value["roles"][0])), "identifiers: duplicate 'role-reviewer'"),
        (lambda value: value["events"][0].update(actor_role_id="missing-role"), "events: unknown actor_role_id 'missing-role'"),
        (lambda value: value["events"][0].update(from_state="intake", to_state="closed"), "events: invalid transition 'intake' -> 'closed'"),
        (lambda value: value.update(state="closed"), "state: does not match the final event to_state"),
    ],
)
def test_semantic_integrity_checks(mutator: Any, expected: str) -> None:
    value = record()
    mutator(value)
    assert expected in validate_record(value)
