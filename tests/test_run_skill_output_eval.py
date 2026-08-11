from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

from tools.run_skill_output_eval import parse_response, run_outputs


ROOT = Path(__file__).parents[1]


def test_parse_response_uses_final_message() -> None:
    raw = "\n".join(
        [
            '{"type":"item.completed","item":{"type":"agent_message","text":"draft"}}',
            '{"type":"item.completed","item":{"type":"agent_message","text":"final"}}',
            '{"type":"turn.completed","usage":{"input_tokens":5,"output_tokens":2}}',
        ]
    )
    assert parse_response(raw) == (
        "final",
        {"input_tokens": 5, "output_tokens": 2},
        True,
    )


def test_generation_preserves_raw_and_defers_scoring(tmp_path, monkeypatch) -> None:
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
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=raw),
    )
    code, summary = run_outputs(ROOT, cases, tmp_path / "runs", timeout=1)
    assert code == 0
    assert summary["generation_complete"] is True
    assert summary["scoring_status"] == "pending_independent_assertion_review"
    assert (tmp_path / "runs/case.jsonl").is_file()
