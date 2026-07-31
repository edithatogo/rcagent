"""Fail-closed Agent Skills upstream drift check."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


UPSTREAM_API = "https://api.github.com/repos/agentskills/agentskills/commits/main"


def check_drift(
    baseline_path: Path,
    *,
    offline: bool = False,
    opener=urllib.request.urlopen,
) -> tuple[int, dict[str, object]]:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    receipt: dict[str, object] = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "baseline_revision": baseline["upstream_revision"],
        "current_conformance": False,
        "mode": "offline" if offline else "live",
        "sources": baseline["sources"],
    }
    if offline:
        receipt["status"] = "offline_not_current"
        receipt["message"] = "Offline validation cannot establish current upstream conformance."
        return 0, receipt

    request = urllib.request.Request(
        UPSTREAM_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "rca-workbench"},
    )
    try:
        with opener(request, timeout=30) as response:
            current = json.loads(response.read().decode("utf-8"))["sha"]
    except (OSError, KeyError, UnicodeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        receipt["status"] = "upstream_unavailable"
        receipt["message"] = str(exc)
        return 2, receipt

    receipt["resolved_revision"] = current
    if current != baseline["upstream_revision"]:
        receipt["status"] = "normative_review_required"
        receipt["message"] = "Upstream revision changed; refresh the normative matrix and validator evidence."
        return 1, receipt

    receipt["status"] = "current"
    receipt["current_conformance"] = True
    receipt["message"] = "Upstream revision matches the reviewed baseline."
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
