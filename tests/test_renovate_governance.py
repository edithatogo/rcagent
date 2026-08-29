from __future__ import annotations

import json
from pathlib import Path


def test_inherited_renovate_config_cannot_automerge_before_ruleset() -> None:
    root = Path(__file__).parents[1]
    config = json.loads((root / "renovate.json").read_text(encoding="utf-8"))
    assert "github>edithatogo/renovate-config" in config["extends"]
    safety_override = config["packageRules"][-1]
    assert safety_override["matchPackageNames"] == ["*"]
    assert safety_override["automerge"] is False
    assert safety_override["platformAutomerge"] is False
