from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from tools.run_skill_output_eval import parse_response, run_outputs

ROOT = Path(__file__).parents[1]


def test_parse_response_uses_final_message() -> None:
    raw = '{"type":"item.completed","item":{"type":"agent_message","text":"draft"}}\n{"type":"item.completed","item":{"type":"agent_message","text":"final"}}\n{"type":"turn.completed","usage":{"input_tokens":5,"output_tokens":2}}'
    assert parse_response(raw) == (
        "final",
        {"input_tokens": 5, "output_tokens": 2},
        True,
    )


def test_generation_preserves_raw_and_defers_scoring(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(
        json.dumps(
            {
                "cases": [
                    {
                        "id": "case",
                        "mode": "investigate",
                        "prompt": "prompt",
                        "assertions": ["safe"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    raw = (
        '{"type":"item.completed","item":{"type":"agent_message","text":"response"}}\n'
        '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
    )
    monkeypatch.setattr(
        subprocess,
        "run",
        Mock(return_value=SimpleNamespace(returncode=0, stdout=raw)),
    )
    code, summary = run_outputs(ROOT, cases, tmp_path / "runs", timeout=1)
    assert code == 0
    assert summary["generation_complete"] is True
    assert summary["scoring_status"] == "pending_independent_assertion_review"
    assert (tmp_path / "runs/case.jsonl").is_file()


def test_response_ignores_malformed_objects_and_usage_without_fabricating_text() -> None:
    values: tuple[object, ...] = (
        [],
        None,
        {"item": None},
        {"item": {"type": "agent_message", "text": None}},
        {"type": "turn.completed", "usage": {"input_tokens": True}},
    )
    raw = "\n".join(json.dumps(item) for item in values)
    assert parse_response(raw) == (None, None, True)


@pytest.mark.parametrize(
    "cases",
    [
        [],
        None,
        [{"id": "../escape", "mode": "test", "prompt": "synthetic", "assertions": ["safe"]}],
    ],
)
def test_empty_or_unsafe_output_cases_never_execute(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cases: object
) -> None:
    path = tmp_path / "cases.json"
    path.write_text(json.dumps({"cases": cases}))
    launch = Mock(side_effect=AssertionError("must not execute"))
    monkeypatch.setattr(subprocess, "run", launch)
    output = tmp_path / "runs"
    with pytest.raises(ValueError, match="output"):
        run_outputs(ROOT, path, output, timeout=1)
    launch.assert_not_called()
    assert not output.exists()
