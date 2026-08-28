from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.workbench import main, select_queue, validate_context, validate_receipt


def valid_context() -> dict[str, object]:
    return {
        "track_id": "track-01",
        "task_id": "phase-4",
        "base_revision": "abc123",
        "created_at": "2026-08-29T00:00:00Z",
        "fresh_until": "source-change",
        "privacy_mode": "fully_local",
        "context_budget": {"files": 12},
        "owned_files": ["tools/workbench.py"],
        "authoritative_inputs": ["conductor/index.md"],
        "excluded_context": ["private data"],
        "next_ready_step": "validate",
        "rollback": "revert the focused commit",
    }


def test_context_contract() -> None:
    assert validate_context(valid_context()) == []
    payload = valid_context()
    payload["privacy_mode"] = "unknown"
    payload["rollback"] = ""
    assert validate_context(payload) == ["missing rollback", "invalid privacy_mode"]


def test_queue_contract_releases_blocked_lane() -> None:
    payload = {
        "items": [
            {
                "id": "blocked",
                "track_id": "track-00",
                "status": "ready",
                "lane": "independent",
                "criticality": 9,
                "blocker": "licence",
            },
            {
                "id": "ready",
                "track_id": "track-01",
                "status": "ready",
                "lane": "independent",
                "criticality": 2,
            },
        ],
        "completed": [],
        "active": [],
        "lane_limits": {"integration": 1, "independent": 2},
    }
    assert select_queue(payload) == {"status": "ready", "selected": "ready"}
    del payload["lane_limits"]
    assert select_queue(payload) == {"status": "ready", "selected": "ready"}


def test_context_cli_is_machine_readable(tmp_path: Path, capsys) -> None:
    path = tmp_path / "context.json"
    path.write_text(json.dumps(valid_context()), encoding="utf-8")
    assert main(["context", str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "pass"


def test_receipt_and_evaluation_fail_closed(capsys: pytest.CaptureFixture[str]) -> None:
    receipt = {
        "task_id": "task",
        "revision": "abc",
        "timestamp": "2026-08-29T00:00:00Z",
        "privacy_mode": "fully_local",
        "commands": [["python", "-m", "pytest"]],
        "results": ["pass"],
        "limitations": ["hosted state not checked"],
        "rollback": "revert commit",
    }
    assert validate_receipt(receipt) == []
    assert main(["evaluate"]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "unavailable"
    assert output["model_execution"] is False
