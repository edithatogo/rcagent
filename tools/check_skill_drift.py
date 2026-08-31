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
    receipt: dict[str, object] = {
        "checked_at": datetime.now(UTC).isoformat(),
        "current_conformance": False,
        "mode": "offline" if offline else "live",
    }
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        if (
            not isinstance(baseline, dict)
            or not isinstance(baseline.get("upstream_revision"), str)
            or not baseline["upstream_revision"]
        ):
            raise ValueError("Missing baseline revision")
        if not isinstance(baseline.get("sources"), list) or not baseline["sources"]:
            raise ValueError("Missing baseline sources")
        receipt["baseline_revision"] = baseline["upstream_revision"]
        receipt["sources"] = baseline["sources"]
    except (OSError, ValueError, TypeError):
        receipt["status"] = "baseline_invalid"
        receipt["message"] = "A valid readable upstream baseline is required."
        return 2, receipt
    if offline:
        receipt["status"] = "offline_not_current"
        receipt["message"] = "Offline validation cannot establish current upstream conformance."
        return 0, receipt

    try:
        current = _read_json(UPSTREAM_API, opener)["sha"]
        if not isinstance(current, str) or not current:
            raise ValueError("Invalid upstream revision")
    except (OSError, KeyError, TypeError, UnicodeError, ValueError, urllib.error.URLError) as exc:
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
        if not isinstance(comparison, dict) or comparison.get("status") != "ahead":
            raise ValueError("Upstream comparison must establish forward ancestry")
        files = comparison.get("files")
        # GitHub compare responses include at most 300 files, even with paging.
        # Do not infer absence of normative changes from a possibly capped list.
        if not isinstance(files, list) or len(files) >= 300:
            raise ValueError("Upstream changed-file list is invalid or potentially truncated")
        changed_paths: list[str] = []
        for item in files:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("filename"), str)
                or not item["filename"]
            ):
                raise ValueError("Malformed changed-file entry")
            changed_paths.append(item["filename"])
            if "previous_filename" in item:
                previous = item["previous_filename"]
                if not isinstance(previous, str) or not previous:
                    raise ValueError("Malformed renamed-file entry")
                changed_paths.append(previous)
    except (OSError, KeyError, TypeError, UnicodeError, ValueError, urllib.error.URLError) as exc:
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
        receipt["message"] = (
            "Creator guidance changed without a normative specification or validator change."
        )
        return 0, receipt

    receipt["status"] = "upstream_change_irrelevant"
    receipt["current_conformance"] = True
    receipt["message"] = (
        "Upstream changed only outside monitored specification, validator, and guidance paths."
    )
    return 0, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path(
            "conductor/tracks/agent-skills-living-conformance_20260731/upstream-baseline.json"
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
