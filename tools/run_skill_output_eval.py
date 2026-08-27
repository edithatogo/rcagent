"""Generate raw Codex outputs for frozen RCA skill evaluation cases."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from tools.install_skill_adapter import install_adapter
from tools.run_skill_trigger_eval import redact_workspace


def parse_response(raw: str) -> tuple[str | None, dict[str, int] | None, bool]:
    messages: list[str] = []
    usage = None
    completed = False
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
            messages.append(item["text"])
        if event.get("type") == "turn.completed":
            completed = True
            usage = event.get("usage")
    return (messages[-1] if messages else None), usage, completed


def run_outputs(
    repository: Path,
    cases_path: Path,
    output_dir: Path,
    *,
    timeout: int,
) -> tuple[int, dict[str, Any]]:
    document = json.loads(cases_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="rca-output-eval-") as workspace_text:
        workspace = Path(workspace_text)
        install_adapter(repository, "codex", workspace)
        for case in document["cases"]:
            command = [
                "codex",
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--disable",
                "plugins",
                "--disable",
                "apps",
                "--disable",
                "skill_search",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--json",
                "-C",
                str(workspace),
                case["prompt"],
            ]
            raw_path = output_dir / f"{case['id']}.jsonl"
            try:
                completed_process = subprocess.run(
                    command,
                    cwd=repository,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=timeout,
                    check=False,
                )
                raw = redact_workspace(completed_process.stdout, workspace)
                response, usage, completed = parse_response(raw)
                status = (
                    "completed"
                    if completed_process.returncode == 0 and completed and response
                    else "failed"
                )
            except subprocess.TimeoutExpired as exc:
                raw = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                raw = redact_workspace(raw, workspace)
                response, usage, _ = parse_response(raw)
                status = "timeout"
            raw_path.write_text(raw, encoding="utf-8")
            results.append(
                {
                    "id": case["id"],
                    "mode": case["mode"],
                    "status": status,
                    "assertions": case["assertions"],
                    "response": response,
                    "usage": usage,
                    "raw_path": raw_path.name,
                }
            )

    passed_generation = all(result["status"] == "completed" for result in results)
    summary = {
        "schema_version": "1.0",
        "client": "codex",
        "client_version": "0.145.0",
        "generation_complete": passed_generation,
        "scoring_status": "pending_independent_assertion_review",
        "cases": results,
    }
    (output_dir / "generation-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (0 if passed_generation else 1), summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("evaluations/skills/rca-investigation/output-cases.json"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    try:
        code, summary = run_outputs(
            args.repository.resolve(),
            args.cases.resolve(),
            args.output_dir.resolve(),
            timeout=args.timeout,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {
                "generation_complete": summary["generation_complete"],
                "cases": [
                    {"id": case["id"], "status": case["status"]}
                    for case in summary["cases"]
                ],
            }
        )
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
