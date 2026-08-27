"""Fail-closed Agent Skills upstream drift check."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

UPSTREAM_API = "https://api.github.com/repos/agentskills/agentskills/commits/main"
COMPARE_API = "https://api.github.com/repos/agentskills/agentskills/compare/{base}...{head}"
NORMATIVE_PATHS = (
    "docs/specification.mdx",
    "skills-ref/src/",
    "skills-ref/pyproject.toml",
    "skills-ref/uv.lock",
)
GUIDANCE_PATHS = (
    "docs/skill-creation/best-practices.mdx",
    "docs/skill-creation/optimizing-descriptions.mdx",
    "docs/skill-creation/evaluating-skills.mdx",
    "docs/skill-creation/using-scripts.mdx",
)


def _read_json(url: str, opener) -> Any:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rca-workbench"},
    )
    with opener(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _matches(path: str, monitored: tuple[str, ...]) -> bool:
    return any(path == candidate or path.startswith(candidate) for candidate in monitored)


def check_drift(
    baseline_path: Path,
    *,
    offline: bool = False,
    opener=urllib.request.urlopen,
) -> tuple[int, dict[str, object]]:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    receipt: dict[str, object] = {
        "checked_at": datetime.now(UTC).isoformat(),
        "baseline_revision": baseline["upstream_revision"],
        "current_conformance": False,
        "mode": "offline" if offline else "live",
        "sources": baseline["sources"],
    }
    if offline:
        receipt["status"] = "offline_not_current"
        receipt["message"] = "Offline validation cannot establish current upstream conformance."
        return 0, receipt

    try:
        current = _read_json(UPSTREAM_API, opener)["sha"]
    except (OSError, KeyError, TypeError, UnicodeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        receipt["status"] = "upstream_unavailable"
        receipt["message"] = str(exc)
        return 2, receipt

    receipt["resolved_revision"] = current
    if current == baseline["upstream_revision"]:
        receipt["status"] = "current"
        receipt["current_conformance"] = True
        receipt["message"] = "Upstream revision matches the reviewed baseline."
        return 0, receipt

    try:
        comparison = _read_json(
            COMPARE_API.format(base=baseline["upstream_revision"], head=current),
            opener,
        )
        changed_paths = [
            item["filename"]
            for item in comparison["files"]
            if isinstance(item, dict) and isinstance(item.get("filename"), str)
        ]
    except (OSError, KeyError, TypeError, UnicodeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        receipt["status"] = "upstream_unavailable"
        receipt["message"] = f"Unable to classify upstream changes: {exc}"
        return 2, receipt

    normative = [path for path in changed_paths if _matches(path, NORMATIVE_PATHS)]
    guidance = [path for path in changed_paths if _matches(path, GUIDANCE_PATHS)]
    receipt["changed_paths"] = changed_paths
    receipt["normative_paths"] = normative
    receipt["guidance_paths"] = guidance
    if normative:
        receipt["status"] = "normative_review_required"
        receipt["message"] = "Normative specification or validator paths changed."
        return 1, receipt
    if guidance:
        receipt["status"] = "guidance_review_advised"
        receipt["current_conformance"] = True
        receipt["message"] = "Creator guidance changed without a normative specification or validator change."
        return 0, receipt

    receipt["status"] = "upstream_change_irrelevant"
    receipt["current_conformance"] = True
    receipt["message"] = "Upstream changed only outside monitored specification, validator, and guidance paths."
    return 0, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path(
            "conductor/tracks/agent-skills-living-conformance_20260731/"
            "upstream-baseline.json"
        ),
    )
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    code, receipt = check_drift(args.baseline, offline=args.offline)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
