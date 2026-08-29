from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
TRACK = ROOT / "conductor/tracks/distribution-registries-plugins_20260731/evidence"


def test_route_assessment_has_complete_current_fields_and_no_universal_registry_claim() -> None:
    value = json.loads((TRACK / "current-route-assessment-20260829.json").read_text())
    required = {"id", "operator", "class", "status", "sources", "licence", "verification", "security_review", "telemetry", "maintenance", "discoverability", "versioning", "terms", "rollback"}
    assert value["retrieved_at"] == "2026-08-29"
    assert len(value["routes"]) == 5
    for route in value["routes"]:
        assert required <= set(route)
    agent_skills = next(route for route in value["routes"] if route["id"] == "agent-skills-specification")
    assert agent_skills["class"] == "official_specification_not_registry"
    assert "universal" not in agent_skills["discoverability"].lower()
    community = next(route for route in value["routes"] if route["id"] == "community-catalogues")
    assert community["status"] == "unsuitable"


def test_openai_packet_has_minimum_cases_and_preserves_external_states() -> None:
    value = json.loads((TRACK / "openai-submission-packet-20260829.json").read_text())
    assert value["state"] == "draft_incomplete_not_submitted"
    assert len(value["positive_tests"]) >= 5
    assert len(value["negative_tests"]) >= 3
    assert value["publisher"]["verification"] == "not_observed"
    assert all(value["public_material"][key] == "not_hosted" for key in value["public_material"])
    assert all({"expected_workflow", "expected_result_shape", "fixture"} <= set(case) for case in value["positive_tests"])
    assert all({"scenario", "expected_fallback", "rationale"} <= set(case) for case in value["negative_tests"])
    assert value["submission"] == {
        "portal": "https://platform.openai.com/apps-manage",
        "submitted": False,
        "approved": False,
        "published": False,
    }
    assert {"mcp", "credentials", "network", "telemetry", "private_data"} <= set(value["excluded"])


def test_claude_packet_is_skills_only_and_not_submitted() -> None:
    value = json.loads((TRACK / "claude-submission-packet-20260829.json").read_text())
    assert value["state"] == "prepared_not_submitted"
    assert value["package_type"] == "skills_only"
    assert value["submission"]["submitted"] is False
    assert value["submission"]["approved"] is False
    assert {"mcp", "hooks", "credentials", "network", "telemetry", "private_data"} <= set(value["excluded"])
