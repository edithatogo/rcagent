"""Keep dependency pinning separate from the supported Python contract."""

import json
import tomllib
from pathlib import Path

import pytest
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("version", ["3.11.0", "3.13.15", "3.14.5"])
def test_dependency_pins_preserve_supported_python(version):
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    constraint = project["project"]["requires-python"]
    assert version in SpecifierSet(constraint)
    assert lock["requires-python"] == constraint


def test_renovate_does_not_pin_python_compatibility_floor():
    config = json.loads((ROOT / "renovate.json").read_text())
    rules = config["packageRules"]
    assert any(
        rule.get("matchManagers") == ["pep621"]
        and rule.get("matchDepTypes") == ["requires-python"]
        and rule.get("enabled") is False
        for rule in rules
    )
    assert config["rangeStrategy"] == "pin"
    assert config["minimumReleaseAge"] == "7 days"
