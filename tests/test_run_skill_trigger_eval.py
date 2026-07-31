import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools.run_skill_trigger_eval import parse_events, redact_workspace, run_evaluation


ROOT = Path(__file__).parents[1]


def test_parse_events_detects_actual_skill_read_and_usage() -> None:
    raw = "\n".join(
        [
            '{"type":"item.completed","item":{"type":"agent_message","text":"using skill"}}',
            '{"type":"item.completed","item":{"type":"command_execution","command":"Get-Content C:\\\\\\\\tmp\\\\\\\\rca-investigation\\\\\\\\SKILL.md"}}',
            '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":2}}',
        ]
    )
    assert parse_events(raw) == (True, 10, 2, True)


def test_parse_events_does_not_trust_self_report_or_malformed_lines() -> None:
    raw = "\n".join(
        [
            "not json",
            '{"type":"item.completed","item":{"type":"agent_message","text":"I used rca-investigation"}}',
            '{"type":"turn.completed","usage":{"input_tokens":3,"output_tokens":1}}',
        ]
    )
    assert parse_events(raw) == (False, 3, 1, True)


def test_workspace_redaction_handles_json_escaped_windows_path() -> None:
    workspace = Path(r"C:\Users\Example\AppData\Temp\run")
    raw = (
        r'{"command":"Get-Content C:\\Users\\Example\\AppData\\Temp\\run\\SKILL.md"}'
    )
    redacted = redact_workspace(raw, workspace)
    assert "Users" not in redacted
    assert "<EVAL_WORKSPACE>" in redacted


def _cases(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "thresholds": {
                    "minimum_trials": 1,
                    "positive_rate": 1.0,
                    "negative_rate": 0.0,
                },
                "cases": [
                    {
                        "id": "positive",
                        "partition": "held_out",
                        "expected": "trigger",
                        "prompt": "positive prompt",
                    },
                    {
                        "id": "negative",
                        "partition": "held_out",
                        "expected": "no_trigger",
                        "prompt": "negative prompt",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_run_evaluation_is_fail_closed_and_preserves_raw(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_run(command, **kwargs):
        activated = command[-1] == "positive prompt"
        command_event = (
            '{"type":"item.completed","item":{"type":"command_execution",'
            '"command":"Read C:\\\\\\\\tmp\\\\\\\\rca-investigation\\\\\\\\SKILL.md"}}\n'
            if activated
            else ""
        )
        raw = (
            command_event
            + '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":2}}\n'
        )
        return SimpleNamespace(returncode=0, stdout=raw)

    monkeypatch.setattr(subprocess, "run", fake_run)
    output = tmp_path / "runs"
    code, summary = run_evaluation(
        ROOT, _cases(tmp_path / "cases.json"), output, trials=1, timeout=10
    )
    assert code == 0
    assert summary["passed"] is True
    assert all(case["passed"] for case in summary["cases"])
    assert (output / "positive-trial-1.jsonl").is_file()
    assert json.loads((output / "summary.json").read_text(encoding="utf-8"))[
        "passed"
    ] is True


def test_timeout_cannot_pass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 1, output="")

    monkeypatch.setattr(subprocess, "run", timeout)
    code, summary = run_evaluation(
        ROOT, _cases(tmp_path / "cases.json"), tmp_path / "runs", trials=1, timeout=1
    )
    assert code == 1
    assert summary["passed"] is False
    assert all(case["activation_rate"] is None for case in summary["cases"])


def test_minimum_trial_contract_is_enforced(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="at least"):
        run_evaluation(
            ROOT, _cases(tmp_path / "cases.json"), tmp_path / "runs", trials=0, timeout=1
        )


def test_partition_selection_is_explicit(tmp_path: Path, monkeypatch) -> None:
    def fake_run(command, **kwargs):
        raw = '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        return SimpleNamespace(returncode=0, stdout=raw)

    monkeypatch.setattr(subprocess, "run", fake_run)
    code, summary = run_evaluation(
        ROOT,
        _cases(tmp_path / "cases.json"),
        tmp_path / "runs",
        trials=1,
        timeout=1,
        partitions={"held_out"},
    )
    assert code == 1
    assert summary["partitions"] == ["held_out"]
    assert [case["id"] for case in summary["cases"]] == ["positive", "negative"]
