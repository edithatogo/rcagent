"""Collection-valued JSON enums produce field errors instead of hash errors."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tools import adaptation_readiness, interface_actions, runtime_lab
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]


@dataclass(frozen=True)
class BoundaryCase:
    name: str
    fixture: str
    path: tuple[str | int, ...]
    validate: Callable[[object], list[str]]
    error: str


CASES = (
    BoundaryCase(
        "template-rights",
        "evaluation/interfaces/registry.json",
        ("templates", 0, "rights"),
        interface_actions.validate_registry,
        "templates[0].rights is invalid",
    ),
    BoundaryCase(
        "canonical-path",
        "evaluation/interfaces/registry.json",
        ("templates", 0, "fields", 0, "canonical_path"),
        interface_actions.validate_registry,
        "templates[0].fields[0].canonical_path is invalid",
    ),
    BoundaryCase(
        "interface-status",
        "evaluation/interfaces/registry.json",
        ("interfaces", 0, "status"),
        interface_actions.validate_registry,
        "interfaces[0].status is invalid",
    ),
    BoundaryCase(
        "runtime-dependency",
        "evaluation/runtime-lab/registry.json",
        ("runtimes", 0, "dependency_class"),
        runtime_lab.validate_runtime_registry,
        "runtimes[0].dependency_class is invalid",
    ),
    BoundaryCase(
        "runtime-support",
        "evaluation/runtime-lab/registry.json",
        ("runtimes", 0, "support_state"),
        runtime_lab.validate_runtime_registry,
        "runtimes[0].support_state is invalid",
    ),
    BoundaryCase(
        "runtime-network",
        "evaluation/runtime-lab/registry.json",
        ("runtimes", 0, "network"),
        runtime_lab.validate_runtime_registry,
        "runtimes[0].network must be none or unknown",
    ),
    BoundaryCase(
        "runtime-telemetry",
        "evaluation/runtime-lab/registry.json",
        ("runtimes", 0, "telemetry"),
        runtime_lab.validate_runtime_registry,
        "runtimes[0].telemetry must be disabled or unknown",
    ),
    BoundaryCase(
        "framework-status",
        "evaluation/adaptation/registry.json",
        ("frameworks", 0, "status"),
        adaptation_readiness.validate_registry,
        "frameworks[0].status is invalid",
    ),
    BoundaryCase(
        "dataset-split-name",
        "evaluation/adaptation/dataset-manifest.json",
        ("splits", 0, "name"),
        adaptation_readiness.validate_dataset_manifest,
        "dataset splits are incomplete",
    ),
)


def _load(case: BoundaryCase) -> JsonObject:
    return require_object(json.loads((ROOT / case.fixture).read_text()), context=case.name)


def _replace(value: JsonObject, path: tuple[str | int, ...], replacement: object) -> None:
    current: object = value
    for part in path[:-1]:
        if isinstance(part, str):
            current = require_object(current, context="fixture path")[part]
        else:
            assert is_array(current)
            current = current[part]
    field = path[-1]
    assert isinstance(field, str)
    require_object(current, context="fixture field")[field] = replacement


@pytest.mark.parametrize("case", CASES, ids=[case.name for case in CASES])
@pytest.mark.parametrize("bad", [[], {}], ids=["array", "object"])
def test_unhashable_enum_values_report_the_intended_error(case: BoundaryCase, bad: object) -> None:
    value = _load(case)
    assert case.validate(value) == []
    _replace(value, case.path, bad)
    assert case.error in case.validate(value)


@pytest.mark.parametrize("case", CASES, ids=[case.name for case in CASES])
@given(
    bad=st.one_of(
        st.lists(st.integers(), max_size=5),
        st.dictionaries(st.text(max_size=8), st.integers(), max_size=5),
    )
)
def test_collection_contents_do_not_bypass_enum_rejection(case: BoundaryCase, bad: object) -> None:
    value = _load(case)
    _replace(value, case.path, bad)
    assert case.error in case.validate(value)


@pytest.mark.parametrize("bad", [[], {}], ids=["array", "object"])
def test_malformed_extra_split_is_not_ignored_when_required_names_exist(bad: object) -> None:
    case = CASES[-1]
    value = _load(case)
    assert case.validate(value) == []
    splits = value["splits"]
    assert is_array(splits)
    splits.append({"name": bad, "item_ids": [], "sha256": adaptation_readiness.canonical_hash([])})
    assert case.error in case.validate(value)
