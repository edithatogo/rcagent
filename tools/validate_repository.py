"""Deterministic repository and Conductor roadmap validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.json_shapes import JsonObject, is_array, is_object, require_object

REQUIRED_CONTEXT = (
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "conductor/index.md",
    "conductor/product.md",
    "conductor/product-guidelines.md",
    "conductor/tech-stack.md",
    "conductor/workflow.md",
    "conductor/autonomy.md",
    "conductor/autonomy.json",
    "conductor/capability-profiles.md",
    "conductor/capability-profiles.json",
    "conductor/schemas/capability-profiles.schema.json",
    "conductor/clinical-governance-architecture.md",
    "conductor/clinical-governance-architecture.json",
    "conductor/integration-map.json",
    "conductor/harness.md",
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

ADOPTED_INTEGRATION_FIELDS = (
    "selected_system",
    "dependency_class",
    "compatibility_window",
    "safe_fallback",
    "replacement_path",
    "evidence",
    "project_owned_gap",
)

PROFILE_CLASSES = {"core", "optional", "experimental", "enterprise", "research-only"}
PROFILE_STATUSES = {"implemented", "planned", "blocked", "unavailable"}
EVIDENCE_REQUIRED_FIELDS = {
    "schema_version": str,
    "event": str,
    "timestamp": str,
    "track_id": str,
}


def _load_document(path: Path) -> JsonObject:
    return require_object(json.loads(path.read_text(encoding="utf-8")), context=path.name)


def _rows(document: JsonObject, field: str, *, label: str, errors: list[str]) -> list[JsonObject]:
    """Return checked rows while recording malformed containers as failures."""
    values = document.get(field, [])
    if not is_array(values):
        errors.append(f"{label}: {field} must be an array")
        return []
    rows: list[JsonObject] = []
    for value in values:
        if not is_object(value):
            errors.append(f"{label}: {field} entry must be an object")
        else:
            rows.append(value)
    return rows


def _validate_track_directories(root: Path) -> list[str]:
    errors: list[str] = []
    track_roots: list[Path] = []
    seen: set[str] = set()
    for container in (root / "conductor/tracks", root / "conductor/archive"):
        if not container.is_dir():
            continue
        for track_root in sorted(path for path in container.iterdir() if path.is_dir()):
            if track_root.name in seen:
                errors.append(f"{track_root.name}: present in both tracks and archive")
                continue
            seen.add(track_root.name)
            track_roots.append(track_root)
    for track_root in track_roots:
        track_id = track_root.name
        if not (track_root / "index.md").is_file():
            errors.append(f"{track_id}: missing index.md")
        metadata_path = track_root / "metadata.json"
        if not metadata_path.is_file():
            continue
        try:
            metadata = _load_document(metadata_path)
        except (OSError, ValueError):
            continue
        if metadata.get("evidence_schema") != "1.0":
            continue
        ledger_path = track_root / "evidence.jsonl"
        if not ledger_path.is_file():
            errors.append(f"{track_id}: missing evidence.jsonl")
            continue
        for line_number, line in enumerate(
            ledger_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            try:
                event: object = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{track_id}: invalid evidence.jsonl line {line_number}: {exc.msg}")
                continue
            if not is_object(event):
                errors.append(
                    f"{track_id}: invalid evidence.jsonl line {line_number}: event must be an object"
                )
                continue
            for field, expected_type in EVIDENCE_REQUIRED_FIELDS.items():
                value = event.get(field)
                if not isinstance(value, expected_type) or not value.strip():
                    errors.append(
                        f"{track_id}: invalid evidence.jsonl line {line_number}: missing {field}"
                    )
            if event.get("schema_version") != "1.0":
                errors.append(
                    f"{track_id}: invalid evidence.jsonl line {line_number}: "
                    "schema_version must be 1.0"
                )
            if event.get("track_id") != track_id:
                errors.append(
                    f"{track_id}: invalid evidence.jsonl line {line_number}: track_id mismatch"
                )
    return errors


def _validate_capability_profiles(registry: object, track_numbers: set[int]) -> list[str]:
    errors: list[str] = []
    if not is_object(registry):
        return ["capability profile registry must be an object"]
    if registry.get("schema_version") != "1.0":
        errors.append("capability registry requires schema_version=1.0")
    if registry.get("$schema") != "schemas/capability-profiles.schema.json":
        errors.append("capability registry requires its local schema reference")
    if registry.get("policy") != "optional-capabilities-must-not-weaken-core-safeguards":
        errors.append("capability registry policy weakens core safeguards")
    contract = registry.get("installation_contract")
    required_true = (
        "agent_assisted",
        "scripted",
        "idempotent",
        "preflight_required",
        "verification_required",
        "receipt_required",
        "rollback_required",
        "uninstall_required",
        "network_egress_requires_disclosure",
        "planned_is_not_installable",
    )
    if not is_object(contract):
        errors.append("capability installation_contract must be an object")
    else:
        for field in required_true:
            if contract.get(field) is not True:
                errors.append(f"capability installation_contract requires {field}=true")
        if contract.get("telemetry_default") != "off":
            errors.append("capability installation_contract requires telemetry_default=off")
    profiles = registry.get("profiles")
    if not is_array(profiles) or not profiles:
        return [*errors, "capability profiles must be a non-empty array"]
    ids: set[str] = set()
    defaults: list[str] = []
    by_id: dict[str, JsonObject] = {}
    for profile in profiles:
        if not is_object(profile):
            errors.append("capability profile must be an object")
            continue
        profile_id = profile.get("id")
        if not isinstance(profile_id, str) or not profile_id:
            errors.append("capability profile has no valid id")
            continue
        if profile_id in ids:
            errors.append(f"duplicate capability profile id: {profile_id}")
        ids.add(profile_id)
        by_id[profile_id] = profile
        profile_class = profile.get("class")
        if not isinstance(profile_class, str) or profile_class not in PROFILE_CLASSES:
            errors.append(f"{profile_id}: invalid capability class")
        status = profile.get("status")
        if not isinstance(status, str) or status not in PROFILE_STATUSES:
            errors.append(f"{profile_id}: invalid capability status")
        if not isinstance(profile.get("default"), bool):
            errors.append(f"{profile_id}: default must be boolean")
        elif profile["default"]:
            defaults.append(profile_id)
        if status in ("planned", "blocked", "unavailable") and profile.get("default") is True:
            errors.append(f"{profile_id}: non-implemented profile cannot be default")
        if status == "implemented" and profile_id != "core":
            implementation = profile.get("implementation")
            if not is_object(implementation) or not all(
                isinstance((value := implementation.get(field)), str) and value.strip()
                for field in ("entrypoint", "support_scope")
            ):
                errors.append(f"{profile_id}: implemented profile requires implementation contract")
        owner = profile.get("owner_track")
        if not isinstance(owner, (int, float)) or owner not in track_numbers:
            errors.append(f"{profile_id}: unknown owner track number")
    if len(defaults) != 1:
        errors.append("capability registry requires exactly one default profile")
    declared_default = registry.get("default_profile")
    if defaults and declared_default != defaults[0]:
        errors.append("default_profile does not match the flagged default profile")
    core = by_id.get("core")
    if not core or core.get("class") != "core" or core.get("status") != "implemented":
        errors.append("core capability profile must be implemented and class core")
    return errors


def validate(root: Path) -> list[str]:
    """Return deterministic diagnostics; an empty list means validation passed."""
    errors: list[str] = []
    for relative in REQUIRED_CONTEXT:
        context_path = root / relative
        if not context_path.is_file():
            errors.append(f"missing required context: {relative}")
        elif not context_path.read_text(encoding="utf-8").strip():
            errors.append(f"empty required context: {relative}")

    errors.extend(_validate_track_directories(root))

    roadmap_path = root / "conductor/roadmap.json"
    if not roadmap_path.is_file():
        return errors

    try:
        roadmap = _load_document(roadmap_path)
    except (OSError, ValueError) as exc:
        errors.append(f"invalid conductor/roadmap.json: {exc}")
        return errors

    track_ids: set[str] = set()
    track_numbers: set[int] = set()
    issue_numbers: set[int] = set()
    for track in _rows(roadmap, "tracks", label="roadmap", errors=errors):
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
        else:
            issue_numbers.add(issue)

        active_root = root / "conductor/tracks" / track_id
        archive_root = root / "conductor/archive" / track_id
        if active_root.is_dir() and archive_root.is_dir():
            errors.append(f"{track_id}: present in both tracks and archive")
        track_root = active_root if active_root.is_dir() else archive_root
        for filename in ("index.md", "metadata.json", "plan.md", "spec.md"):
            if not (track_root / filename).is_file():
                errors.append(f"{track_id}: missing {filename}")

        plan_path = track_root / "plan.md"
        if plan_path.is_file():
            plan = plan_path.read_text(encoding="utf-8")
            normalized_plan = " ".join(plan.split()).lower()
            for marker in CONTINUOUS_CONTRACT_MARKERS:
                if marker not in normalized_plan:
                    errors.append(f"{track_id}: continuous execution contract missing {marker!r}")

        metadata_path = track_root / "metadata.json"
        if metadata_path.is_file():
            try:
                metadata = _load_document(metadata_path)
            except (OSError, ValueError) as exc:
                errors.append(f"{track_id}: invalid metadata.json: {exc}")
            else:
                expected = f"https://github.com/edithatogo/rcagent/issues/{issue}"
                github = metadata.get("github")
                if not is_object(github) or github.get("issue") != expected:
                    errors.append(f"{track_id}: issue mapping does not match #{issue}")

    architecture_path = root / "conductor/clinical-governance-architecture.json"
    if architecture_path.is_file():
        try:
            architecture = _load_document(architecture_path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid conductor/clinical-governance-architecture.json: {exc}")
        else:
            layer_ids: set[str] = set()
            for layer in _rows(architecture, "layers", label="clinical governance", errors=errors):
                layer_id = layer.get("id")
                if not isinstance(layer_id, str) or not layer_id:
                    errors.append("clinical governance layer has no valid id")
                    continue
                if layer_id in layer_ids:
                    errors.append(f"duplicate clinical governance layer id: {layer_id}")
                layer_ids.add(layer_id)
                owners = layer.get("owner_tracks", [])
                if not is_array(owners):
                    errors.append(f"{layer_id}: owner_tracks must be an array")
                    continue
                for owner in owners:
                    if not isinstance(owner, (int, float)) or owner not in track_numbers:
                        errors.append(f"{layer_id}: unknown owner track number: {owner}")

            integration_ids: set[str] = set()
            for integration in _rows(
                architecture, "integrations", label="clinical governance", errors=errors
            ):
                integration_id = integration.get("id")
                if not isinstance(integration_id, str) or not integration_id:
                    errors.append("clinical governance integration has no valid id")
                    continue
                if integration_id in integration_ids:
                    errors.append(f"duplicate clinical governance integration id: {integration_id}")
                integration_ids.add(integration_id)
                for field in ("owner_track", "validation_track"):
                    value = integration.get(field)
                    if not isinstance(value, (int, float)) or value not in track_numbers:
                        errors.append(f"{integration_id}: unknown {field} number: {value}")

    integration_map_path = root / "conductor/integration-map.json"
    if integration_map_path.is_file():
        try:
            integration_map = _load_document(integration_map_path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid conductor/integration-map.json: {exc}")
        else:
            integration_track_ids: set[str] = set()
            for integration in _rows(
                integration_map, "tracks", label="integration-map", errors=errors
            ):
                track_id = integration.get("track_id")
                if not isinstance(track_id, str) or not track_id:
                    errors.append("integration-map track has no valid track_id")
                    continue
                if track_id in integration_track_ids:
                    errors.append(f"duplicate integration-map track id: {track_id}")
                integration_track_ids.add(track_id)
                if track_id not in track_ids:
                    errors.append(f"integration-map has unknown track id: {track_id}")
                candidates = integration.get("candidate_systems")
                if not is_array(candidates) or not candidates:
                    errors.append(f"{track_id}: candidate_systems must be non-empty")
                if integration.get("status") in ("adopt", "adapt", "project-extension"):
                    for field in ADOPTED_INTEGRATION_FIELDS:
                        value = integration.get(field)
                        if not isinstance(value, str) or not value.strip():
                            errors.append(f"{track_id}: adopted integration missing {field}")

    capability_path = root / "conductor/capability-profiles.json"
    if capability_path.is_file():
        try:
            capability_registry = _load_document(capability_path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid conductor/capability-profiles.json: {exc}")
        else:
            errors.extend(_validate_capability_profiles(capability_registry, track_numbers))

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
