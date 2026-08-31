from __future__ import annotations

import hashlib
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


@pytest.mark.parametrize(
    "field,value",
    [
        ("fresh_until", "2000-01-01T00:00:00Z"),
        ("created_at", "2999-01-01T00:00:00Z"),
        ("created_at", "2026-01-01"),
        ("privacy_mode", []),
        ("context_budget", {"files": -1}),
        ("context_budget", {"files": True}),
        ("owned_files", ["../secret"]),
        ("owned_files", ["src/a\u0000.py"]),
        ("owned_files", ["src/shared."]),
        ("owned_files", ["C:\\secret"]),
        ("authoritative_inputs", "conductor/index.md"),
        ("rollback", True),
    ],
)
def test_invalid_context_fails_closed(field, value):
    payload = valid_context()
    payload[field] = value
    assert validate_context(payload)


def test_malformed_receipt_rejected():
    assert validate_receipt(
        {
            key: True
            for key in (
                "task_id",
                "revision",
                "timestamp",
                "privacy_mode",
                "commands",
                "results",
                "limitations",
                "rollback",
            )
        }
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"items": "bad"},
        {"items": [False]},
        {"completed": [True]},
        {"lane_limits": []},
        {
            "items": [
                {
                    "id": "a",
                    "track_id": "t",
                    "status": "ready",
                    "lane": "independent",
                    "blocker": False,
                }
            ]
        },
        {
            "items": [
                {
                    "id": "a",
                    "track_id": "t",
                    "status": "ready",
                    "lane": "independent",
                    "dependencies": "done",
                }
            ]
        },
    ],
)
def test_invalid_queue_is_machine_readable_failure(tmp_path, capsys, payload):
    path = tmp_path / "queue.json"
    path.write_text(json.dumps(payload))
    assert main(["queue", str(path)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "fail"


def test_invalid_json_is_machine_readable_failure(tmp_path, capsys):
    path = tmp_path / "context.json"
    path.write_text("{")
    assert main(["context", str(path)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "fail"


def test_durable_state_cli_resumes_existing_checkpoint(tmp_path, capsys):
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps({"tracks": [{"id": "track", "phases": ["phase"]}], "base_revision": "a" * 40})
    )
    checkpoint = tmp_path / "checkpoint.json"
    assert main(["state", "initialise", str(checkpoint), "--input", str(plan)]) == 0
    initial = json.loads(capsys.readouterr().out)
    assert main(["state", "next", str(checkpoint)]) == 0
    assert json.loads(capsys.readouterr().out) == initial
    assert initial["next_action"]["stage"] == "implement"
    assert initial["model_execution"] is False
    assert main(["state", "initialise", str(checkpoint), "--input", str(plan)]) == 1


def test_state_cli_wait_resume_and_phase_completion(tmp_path, capsys):
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps({"tracks": [{"id": "track", "phases": ["phase"]}], "base_revision": "a" * 40})
    )
    checkpoint = tmp_path / "checkpoint.json"
    assert main(["state", "initialise", str(checkpoint), "--input", str(plan)]) == 0
    instruction = json.loads(capsys.readouterr().out)["next_action"]
    evidence = tmp_path / "evidence.txt"
    evidence.write_text("synthetic test observation")
    artefacts = [
        {"path": evidence.name, "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}
    ]
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps(
            {
                "event_id": "wait",
                "action": "waiting_external",
                "wake_condition": "synthetic readiness",
            }
        )
    )
    assert main(["state", "advance", str(checkpoint), "--input", str(event)]) == 0
    assert json.loads(capsys.readouterr().out)["next_action"] is None
    receipt = tmp_path / "receipt.json"
    receipt.write_text(
        json.dumps(
            {
                **instruction,
                "stage": "waiting_external",
                "outcome": "resume",
                "artefacts": artefacts,
            }
        )
    )
    event.write_text(
        json.dumps({"event_id": "resume", "track_id": "track", "receipt": receipt.name})
    )
    assert (
        main(["state", "resume", str(checkpoint), "--root", str(tmp_path), "--input", str(event)])
        == 0
    )
    assert json.loads(capsys.readouterr().out)["next_action"] == instruction
    receipt.write_text(json.dumps({**instruction, "outcome": "pass", "artefacts": artefacts}))
    event.write_text(json.dumps({"event_id": "pass", "action": "pass", "receipt": receipt.name}))
    assert (
        main(["state", "advance", str(checkpoint), "--root", str(tmp_path), "--input", str(event)])
        == 0
    )
    assert json.loads(capsys.readouterr().out)["next_action"]["stage"] == "review"
