"""D4 demonstrator has a deterministic inspectable comparison receipt."""

from __future__ import annotations

import json
import subprocess
import sys

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw11_d4_comparison import generate_receipt
from tools.json_shapes import is_array, require_object


def test_d4_demo_emits_an_explicitly_unqualified_four_arm_receipt() -> None:
    receipt = generate_receipt()
    assert receipt["schema_version"] == "faw11-d4-receipt-1.0"
    assert receipt["dataset"] == "generated-synthetic-only"
    assert receipt["command"] == "uv run --no-sync python -m tools.workbench d4-demo"
    assert receipt["task"] == "FAW11/D4"
    assert receipt["model_executed"] is False
    comparison = require_object(receipt["comparison"], context="D4 comparison")
    assert comparison["status"] == "incomplete_unqualified"
    assert comparison["paired_comparison_admissible"] is False
    assert comparison["model_executed"] is False
    assert comparison["clinical_qualification"] == "none"
    scores = require_object(comparison["scores"], context="D4 scores")
    assert require_object(scores["regex"], context="regex")["covered"] == 1
    for arm in ("token_section_context", "linear_classifier", "structured_generation"):
        assert require_object(scores[arm], context=arm)["status"] == "unavailable"
    view = require_object(receipt["arm_view"], context="arm input")
    events = view["events"]
    assert is_array(events)
    assert len(events) == 1
    assert "Later test result" not in str(view)
    assert "patient_family_concern" not in str(view)
    assert "future" not in str(view)
    assert receipt["receipt_fingerprint"] == fingerprint(
        {key: value for key, value in receipt.items() if key != "receipt_fingerprint"}
    )


def test_d4_demo_cli_has_exact_repeatable_utf8_receipt_bytes() -> None:
    argv = [sys.executable, "-m", "tools.workbench", "d4-demo"]
    first = subprocess.run(argv, capture_output=True, check=True).stdout
    second = subprocess.run(argv, capture_output=True, check=True).stdout
    assert first == second == canonical_bytes(generate_receipt()) + b"\n"
    parsed: object = json.loads(first)
    assert require_object(parsed, context="D4 CLI result")["task"] == "FAW11/D4"
