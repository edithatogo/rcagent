"""Generated counterexamples for evidence references and disclosure boundaries."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

import pytest
from hypothesis import example, given, settings
from hypothesis import strategies as st

from tools.evidence_core import export_record, validate_record

FIXTURE = Path(__file__).parent / "fixtures/safety-work/valid-case.json"


def _record() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(FIXTURE.read_text(encoding="utf-8")))


# These properties parse and validate the full schema under branch coverage.
# Use a finite one-second correctness budget; the default 200 ms proved flaky
# (269 ms then 124 ms for the same input). Performance has its own profile gate.
@settings(deadline=1000)
@given(
    target=st.sampled_from(
        [
            ("artefacts", "source_id", "sources"),
            ("evidence", "source_id", "sources"),
            ("evidence", "artefact_id", "artefacts"),
            ("events", "actor_role_id", "roles"),
            ("events", "evidence_ids", "evidence"),
            ("reviews", "reviewer_role_ids", "roles"),
            ("reviews", "statement_ids", "statements"),
            ("outcomes", "evidence_ids", "evidence"),
            ("outcomes", "statement_id", "statements"),
            ("factors", "statement_id", "statements"),
        ]
    ),
    replacement_kind=st.sampled_from(
        [
            "roles",
            "sources",
            "artefacts",
            "evidence",
            "statements",
            "factors",
            "events",
            "reviews",
            "outcomes",
            "referrals",
        ]
    ),
)
def test_cross_kind_reference_substitution_is_rejected(
    target: tuple[str, str, str], replacement_kind: str
) -> None:
    """An ID existing elsewhere cannot satisfy an unrelated reference."""
    value = _record()
    collection, field, required_kind = target
    identifiers = {
        "roles": "role-reviewer",
        "sources": "source-synthetic-01",
        "artefacts": "artefact-record-01",
        "evidence": "evidence-record-01",
        "statements": "statement-observed-01",
        "factors": "factor-system-01",
        "events": "event-investigation-01",
        "reviews": "review-huddle-01",
        "outcomes": "outcome-learning-01",
        "referrals": "referral-policy-01",
    }
    identifier = identifiers[replacement_kind]
    value[collection][0][field] = [identifier] if field.endswith("_ids") else identifier
    errors = validate_record(value)
    if replacement_kind == required_kind:
        assert errors == []
    else:
        assert any(f"{collection}: unknown {field}" in error for error in errors)


@settings(deadline=1000)
@example(narrative="f\U00060ce2")
@given(narrative=st.text(min_size=1, max_size=1000))
def test_public_summary_is_independent_of_source_and_narrative_content(narrative: str) -> None:
    """Arbitrary Unicode text must not influence the disclosed view or its hash."""
    value = _record()
    value["privacy_mode"] = "public_remote"
    before = export_record(value, profile="public")
    value["statements"][0]["text"] = narrative
    value["statements"][1]["uncertainty"] = narrative
    value["sources"][0]["title"] = narrative
    value["sources"][0]["authority"] = narrative
    value["evidence"][0]["content"] = narrative
    value["relationships"][0]["rationale"] = narrative
    value["jurisdiction"] = narrative
    value["authority"] = narrative
    unchanged = deepcopy(value)
    assert export_record(value, profile="public") == before
    assert value == unchanged


@settings(deadline=1000)
@given(
    mode=st.sampled_from(["fully_local", "governed_hybrid", "air_gapped"]),
    narrative=st.text(min_size=1, max_size=1000),
)
def test_private_records_never_become_public_through_export(mode: str, narrative: str) -> None:
    value = _record()
    value["privacy_mode"] = mode
    value["statements"][0]["text"] = narrative
    unchanged = deepcopy(value)
    with pytest.raises(ValueError, match="private-mode conversion is prohibited"):
        export_record(value, profile="public")
    assert value == unchanged
    governed = export_record(value, profile="governed")
    assert governed["statements"][0]["text"] == narrative
    assert governed["privacy_mode"] == mode


@settings(deadline=1000)
@given(
    relation=st.sampled_from(["supports", "contradicts", "implements", "evaluates"]),
    role_is_source=st.booleans(),
)
def test_roles_cannot_be_used_as_evidence_or_claim_relationship_endpoints(
    relation: str, role_is_source: bool
) -> None:
    value = _record()
    endpoints = ["role-reviewer", "statement-observed-01"]
    if not role_is_source:
        endpoints.reverse()
    value["relationships"] = [
        {"from_id": endpoints[0], "relation": relation, "to_id": endpoints[1]}
    ]
    assert any("endpoint types" in error for error in validate_record(value))
