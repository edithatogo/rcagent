"""Run repeatable Codex activation trials for the RCA Agent Skill."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from tools.install_skill_adapter import install_adapter


@dataclass(frozen=True)
class Trial:
    case_id: str
    trial: int
    expected: str
    status: str
    activated: bool
    input_tokens: int | None
    output_tokens: int | None
    raw_path: str


def parse_events(raw: str) -> tuple[bool, int | None, int | None, bool]:
    activated = False
    input_tokens = None
    output_tokens = None
    completed = False
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if item.get("type") == "command_execution":
            command = str(item.get("command", "")).replace("\\", "/").casefold()
            command = re.sub(r"/+", "/", command)
            if "/rca-investigation/skill.md" in command:
                activated = True
        if event.get("type") == "turn.completed":
            completed = True
            usage = event.get("usage", {})
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
    return activated, input_tokens, output_tokens, completed


def redact_workspace(raw: str, workspace: Path) -> str:
    workspace_text = str(workspace)
    # A Windows path may be processed on a POSIX CI host, where pathlib treats
    # the entire value as one path component. Cover the literal path and the
    # common JSON-escaping depths explicitly rather than relying on host path
    # parsing semantics.
    variants = {workspace_text, workspace.as_posix()}
    for multiplier in (2, 4, 8):
        variants.add(workspace_text.replace("\\", "\\" * multiplier))
    for variant in sorted(variants, key=len, reverse=True):
        raw = raw.replace(variant, "<EVAL_WORKSPACE>")
    if len(workspace.parts) >= 4:
        escaped_parts = [re.escape(part) for part in workspace.parts if part not in ("\\", "/")]
        separator = r"(?:\\+|/+)"
        raw = re.sub(separator.join(escaped_parts), "<EVAL_WORKSPACE>", raw)
    return raw


def run_evaluation(
    repository: Path,
    cases_path: Path,
    output_dir: Path,
    *,
    trials: int,
    timeout: int,
    partitions: set[str] | None = None,
    case_ids: set[str] | None = None,
) -> tuple[int, dict[str, object]]:
    cases_document = json.loads(cases_path.read_text(encoding="utf-8"))
    cases = cases_document["cases"]
    if partitions:
        cases = [case for case in cases if case["partition"] in partitions]
        if not cases:
            raise ValueError("partition selection matched no cases")
    if case_ids:
        cases = [case for case in cases if case["id"] in case_ids]
        if {case["id"] for case in cases} != case_ids:
            raise ValueError("case selection contains an unknown or excluded id")
    thresholds = cases_document["thresholds"]
    if trials < thresholds["minimum_trials"]:
        raise ValueError(f"at least {thresholds['minimum_trials']} trials are required")

    output_dir.mkdir(parents=True, exist_ok=True)
    observations: list[Trial] = []
    with tempfile.TemporaryDirectory(prefix="rca-trigger-eval-") as workspace_text:
        workspace = Path(workspace_text)
        install_adapter(repository, "codex", workspace)
        for case in cases:
            for trial_number in range(1, trials + 1):
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
                raw_name = f"{case['id']}-trial-{trial_number}.jsonl"
                raw_path = output_dir / raw_name
                try:
                    result = subprocess.run(
                        command,
                        cwd=repository,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=timeout,
                        check=False,
                    )
                    raw = redact_workspace(result.stdout, workspace)
                    raw_path.write_text(raw, encoding="utf-8")
                    activated, input_tokens, output_tokens, completed = parse_events(raw)
                    status = (
                        "completed"
                        if result.returncode == 0 and completed
                        else "failed"
                    )
                except subprocess.TimeoutExpired as exc:
                    raw = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                    raw = redact_workspace(raw, workspace)
                    raw_path.write_text(raw, encoding="utf-8")
                    activated, input_tokens, output_tokens, _ = parse_events(raw)
                    status = "timeout"
                observations.append(
                    Trial(
                        case_id=case["id"],
                        trial=trial_number,
                        expected=case["expected"],
                        status=status,
                        activated=activated,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        raw_path=raw_name,
                    )
                )

    case_results: list[dict[str, object]] = []
    passed = True
    for case in cases:
        relevant = [item for item in observations if item.case_id == case["id"]]
        completed = [item for item in relevant if item.status == "completed"]
        rate = (
            sum(item.activated for item in completed) / len(completed)
            if len(completed) == trials
            else None
        )
        expected_rate = (
            thresholds["positive_rate"]
            if case["expected"] == "trigger"
            else thresholds["negative_rate"]
        )
        case_pass = rate == expected_rate
        passed = passed and case_pass
        case_results.append(
            {
                "id": case["id"],
                "partition": case["partition"],
                "expected": case["expected"],
                "completed_trials": len(completed),
                "activation_rate": rate,
                "required_rate": expected_rate,
                "passed": case_pass,
            }
        )

    summary = {
        "schema_version": "1.0",
        "client": "codex",
        "client_version": "0.145.0",
        "isolation": {
            "ephemeral": True,
            "sandbox": "read-only",
            "plugins": False,
            "apps": False,
            "dynamic_skill_search": False,
        },
        "trials_per_case": trials,
        "partitions": sorted(partitions) if partitions else ["all"],
        "case_selection": sorted(case_ids) if case_ids else ["all"],
        "passed": passed,
        "cases": case_results,
        "observations": [asdict(item) for item in observations],
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (0 if passed else 1), summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("evaluations/skills/rca-investigation/trigger-cases.json"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--partition",
        action="append",
        dest="partitions",
        help="Run only this partition; repeat for multiple partitions.",
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="case_ids",
        help="Run only this case id; repeat for multiple cases.",
    )
    args = parser.parse_args()
    try:
        code, summary = run_evaluation(
            args.repository.resolve(),
            args.cases.resolve(),
            args.output_dir.resolve(),
            trials=args.trials,
            timeout=args.timeout,
            partitions=set(args.partitions) if args.partitions else None,
            case_ids=set(args.case_ids) if args.case_ids else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps({"passed": summary["passed"], "cases": summary["cases"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
