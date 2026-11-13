"""Malformed values must fail at the boundary where their types are established."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools import adaptation_readiness, interface_actions, runtime_lab
from tools.json_shapes import is_array, require_object

ROOT = Path(__file__).parents[1]


def fixture_object(relative: str) -> dict[str, object]:
    return require_object(json.loads((ROOT / relative).read_text()), context=relative)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("purpose", []),
        ("evidence_state", None),
        ("capability", "SEIPS"),
        ("capability", [None]),
        ("open_questions", [1]),
        ("evidence_signals", {"human_factors": True}),
        ("method_budget", True),
        ("method_budget", "2"),
        ("unrecognised", True),
    ],
)
def test_malformed_method_request_cannot_count_as_success(field: str, value: object) -> None:
    payload: dict[str, object] = {
        "purpose": "retrospective_incident",
        "evidence_state": "insufficient",
        "capability": [],
    }
    payload[field] = value
    registry = fixture_object("evaluation/interfaces/registry.json")
    result = interface_actions.evaluate_synthetic_journeys(
        registry, [{"id": "syn-invalid", "kind": "method_abstention", "payload": payload}]
    )
    cases = result["cases"]
    assert is_array(cases)
    assert len(cases) == 1
    assert require_object(cases[0], context="case")["passed"] is False


def test_missing_required_method_input_cannot_count_as_abstention() -> None:
    registry = fixture_object("evaluation/interfaces/registry.json")
    payload: dict[str, object] = {}
    result = interface_actions.evaluate_synthetic_journeys(
        registry, [{"id": "syn-missing", "kind": "method_abstention", "payload": payload}]
    )
    cases = result["cases"]
    assert is_array(cases)
    assert len(cases) == 1
    assert require_object(cases[0], context="case")["passed"] is False


@pytest.mark.parametrize("value", [None, 7, "text", {"invalid": True}])
def test_runtime_collection_shapes_fail_closed(value: object) -> None:
    registry = fixture_object("evaluation/runtime-lab/registry.json")
    runtimes = registry["runtimes"]
    assert is_array(runtimes)
    assert runtimes
    runtime = require_object(runtimes[0], context="runtime")
    runtime["failure_modes"] = value
    runtime["executable_names"] = value
    registry["models"] = [
        {
            "id": "syn-model",
            "task_fit": value,
            "input_limits": {"modalities": value},
        }
    ]
    errors = runtime_lab.validate_runtime_registry(registry)
    assert "runtimes[0].failure_modes must be a non-empty array" in errors
    assert "runtimes[0].executable_names must be a string array" in errors
    assert "models[0].task_fit must be a non-empty string array" in errors
    assert "models[0].input_limits must contain a non-empty modalities string array" in errors
    result = runtime_lab.route_request(
        {"model_id": "syn-model", "task": "timeline", "modality": "text"}, registry, {}
    )
    assert result["status"] == "no_capability"
    assert result["external_fallback"] is False
    assert result["model_executed"] is False


@pytest.mark.parametrize(
    "limitations", [None, 7, "no model promotion", {"no model promotion": True}]
)
def test_nonpromotion_claim_requires_an_array_of_limitations(
    tmp_path: Path, limitations: object
) -> None:
    manifest = fixture_object("evaluation/adaptation/dependencies.json")
    claims = manifest["claims"]
    assert is_array(claims)
    for value in claims:
        claim = require_object(value, context="dependency claim")
        if claim["id"] == "benchmark_comparators_nonpromotion":
            target = tmp_path / "comparator.json"
            target.write_text(
                json.dumps(
                    {
                        "scope": "internal_nonpromotion_synthetic_comparator",
                        "limitations": limitations,
                    }
                )
            )
            claim["path"] = target.name
            claim["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    errors = adaptation_readiness.validate_dependency_manifest(manifest, tmp_path)
    assert "benchmark non-promotion claim failed" in errors


@pytest.mark.parametrize("value", [{1: "unsafe-key"}, [object()], float("nan")])
def test_checked_containers_do_not_weaken_export_rejection(value: object) -> None:
    with pytest.raises(ValueError, match=r"unsafe export key|unsupported export value|non-finite"):
        interface_actions.sanitize_export(value)
