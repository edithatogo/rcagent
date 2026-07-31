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
    "conductor/clinical-governance-architecture.md",
    "conductor/clinical-governance-architecture.json",
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
    track_numbers: set[int] = set()
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
        number = track.get("number")
        if not isinstance(number, int) or number < 0:
            errors.append(f"{track_id}: invalid track number")
        elif number in track_numbers:
            errors.append(f"duplicate roadmap track number: {number}")
        else:
            track_numbers.add(number)
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

    architecture_path = root / "conductor/clinical-governance-architecture.json"
    if architecture_path.is_file():
        try:
            architecture = json.loads(architecture_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(
                f"invalid conductor/clinical-governance-architecture.json: {exc}"
            )
        else:
            layer_ids: set[str] = set()
            for layer in architecture.get("layers", []):
                layer_id = layer.get("id")
                if not isinstance(layer_id, str) or not layer_id:
                    errors.append("clinical governance layer has no valid id")
                    continue
                if layer_id in layer_ids:
                    errors.append(f"duplicate clinical governance layer id: {layer_id}")
                layer_ids.add(layer_id)
                for owner in layer.get("owner_tracks", []):
                    if owner not in track_numbers:
                        errors.append(
                            f"{layer_id}: unknown owner track number: {owner}"
                        )

            integration_ids: set[str] = set()
            for integration in architecture.get("integrations", []):
                integration_id = integration.get("id")
                if not isinstance(integration_id, str) or not integration_id:
                    errors.append("clinical governance integration has no valid id")
                    continue
                if integration_id in integration_ids:
                    errors.append(
                        f"duplicate clinical governance integration id: {integration_id}"
                    )
                integration_ids.add(integration_id)
                for field in ("owner_track", "validation_track"):
                    value = integration.get(field)
                    if value not in track_numbers:
                        errors.append(
                            f"{integration_id}: unknown {field} number: {value}"
                        )

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
