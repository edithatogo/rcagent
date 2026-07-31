"""Deterministic repository and Conductor roadmap validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_CONTEXT = (
    "conductor/index.md",
    "conductor/product.md",
    "conductor/product-guidelines.md",
    "conductor/tech-stack.md",
    "conductor/workflow.md",
    "conductor/autonomy.md",
    "conductor/autonomy.json",
    "conductor/capability-profiles.md",
    "conductor/capability-profiles.json",
    "conductor/roadmap.md",
    "conductor/roadmap.json",
    "conductor/tracks.md",
)

CONTINUOUS_CONTRACT_MARKERS = (
    "continue automatically",
    "do not ask for routine approval",
    "recommendation",
    "safe default",
)


def validate(root: Path) -> list[str]:
    """Return deterministic diagnostics; an empty list means validation passed."""
    errors: list[str] = []
    for relative in REQUIRED_CONTEXT:
        if not (root / relative).is_file():
            errors.append(f"missing required context: {relative}")

    roadmap_path = root / "conductor/roadmap.json"
    if not roadmap_path.is_file():
        return errors

    try:
        roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid conductor/roadmap.json: {exc}")
        return errors

    track_ids: set[str] = set()
    issue_numbers: set[int] = set()
    for track in roadmap.get("tracks", []):
        track_id = track.get("id")
        issue = track.get("issue")
        if not isinstance(track_id, str) or not track_id:
            errors.append("roadmap track has no valid id")
            continue
        if track_id in track_ids:
            errors.append(f"duplicate roadmap track id: {track_id}")
        track_ids.add(track_id)
        if not isinstance(issue, int) or issue < 1:
            errors.append(f"{track_id}: invalid GitHub issue")
        elif issue in issue_numbers:
            errors.append(f"duplicate GitHub issue mapping: #{issue}")
        issue_numbers.add(issue)

        track_root = root / "conductor/tracks" / track_id
        for filename in ("index.md", "metadata.json", "plan.md", "spec.md"):
            if not (track_root / filename).is_file():
                errors.append(f"{track_id}: missing {filename}")

        plan_path = track_root / "plan.md"
        if plan_path.is_file():
            plan = plan_path.read_text(encoding="utf-8")
            normalized_plan = " ".join(plan.split()).lower()
            for marker in CONTINUOUS_CONTRACT_MARKERS:
                if marker not in normalized_plan:
                    errors.append(
                        f"{track_id}: continuous execution contract missing {marker!r}"
                    )

        metadata_path = track_root / "metadata.json"
        if metadata_path.is_file():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{track_id}: invalid metadata.json: {exc}")
            else:
                expected = f"https://github.com/edithatogo/rcagent/issues/{issue}"
                if metadata.get("github", {}).get("issue") != expected:
                    errors.append(f"{track_id}: issue mapping does not match #{issue}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Repository governance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
