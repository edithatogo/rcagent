"""Fail-closed multimodal capability contracts and synthetic probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "evaluation/multimodal/registry.json"
SCHEMA_PATH = ROOT / "conductor/schemas/multimodal-capability.schema.json"
SUPPORT_MATRIX_PATH = ROOT / "evaluation/multimodal/support-matrix-20260829.json"


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def load_registry() -> dict[str, Any]:
    return _read(REGISTRY_PATH)


def validate_registry(registry: dict[str, Any]) -> list[str]:
    schema = _read(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(registry)
    ]
    profiles = registry.get("profiles", [])
    fixtures = registry.get("fixtures", [])
    profile_ids = [item.get("id") for item in profiles if isinstance(item, dict)]
    fixture_ids = [item.get("id") for item in fixtures if isinstance(item, dict)]
    for label, values in (("profiles", profile_ids), ("fixtures", fixture_ids)):
        errors.extend(
            f"{label}: duplicate id {value!r}"
            for value in sorted({item for item in values if isinstance(item, str)})
            if values.count(value) > 1
        )
    known_profiles = {item for item in profile_ids if isinstance(item, str)}
    for fixture in fixtures:
        if isinstance(fixture, dict) and fixture.get("profile_id") not in known_profiles:
            errors.append(f"fixtures: unknown profile {fixture.get('profile_id')!r}")
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        privacy = profile.get("privacy", {})
        if profile.get("status") != "supported" and privacy.get("network") not in {
            "disabled",
            "disabled until admitted",
        }:
            errors.append(f"profiles: unadmitted {profile.get('id')!r} must disable network")
        if privacy.get("remote_code") != "prohibited":
            errors.append(f"profiles: {profile.get('id')!r} must prohibit remote code")
        if profile.get("modality") in {"image", "signal"} and (
            profile.get("governance") != "research_disabled" or profile.get("status") == "supported"
        ):
            errors.append(
                f"profiles: {profile.get('id')!r} interpretation must remain research-disabled"
            )
    if SUPPORT_MATRIX_PATH.is_file():
        matrix = _read(SUPPORT_MATRIX_PATH)
        matrix_profiles = matrix.get("profiles", [])
        matrix_ids = {item.get("profile_id") for item in matrix_profiles if isinstance(item, dict)}
        if matrix_ids != known_profiles:
            errors.append("support matrix profile identifiers must match the registry")
        for item in matrix_profiles:
            if not isinstance(item, dict):
                errors.append("support matrix profile must be an object")
                continue
            registry_profile = next(
                (profile for profile in profiles if profile.get("id") == item.get("profile_id")),
                None,
            )
            if registry_profile is None:
                continue
            if set(item.get("device_classes", {})) != set(
                registry_profile["limits"]["device_classes"]
            ):
                errors.append(
                    f"support matrix device classes differ for {item.get('profile_id')!r}"
                )
            for evidence in item.get("evidence", []):
                if not isinstance(evidence, str) or not (ROOT / evidence).is_file():
                    errors.append(f"support matrix evidence missing: {evidence!r}")
        boundaries = matrix.get("global_boundaries", {})
        if (
            boundaries.get("remote_code") != "prohibited"
            or boundaries.get("clinical_interpretation") != "disabled"
        ):
            errors.append("support matrix safety boundary mismatch")
    return sorted(errors)


def execution_disclosure(
    registry: dict[str, Any], profile_id: str, fixture_id: str
) -> dict[str, Any]:
    errors = validate_registry(registry)
    if errors:
        raise ValueError("invalid registry: " + "; ".join(errors))
    profile = next((item for item in registry["profiles"] if item["id"] == profile_id), None)
    fixture = next((item for item in registry["fixtures"] if item["id"] == fixture_id), None)
    if profile is None or fixture is None or fixture["profile_id"] != profile_id:
        raise ValueError("unknown or mismatched profile and fixture")
    disclosure: dict[str, Any] = {
        "schema_version": "1.0",
        "profile_id": profile_id,
        "fixture_id": fixture_id,
        "framework": profile["framework"],
        "revision": profile["revision"],
        "governance": profile["governance"],
        "capability_status": profile["status"],
        "execution_mode": "deterministic-contract-probe",
        "device": platform.platform(),
        "network": "disabled",
        "telemetry": "none",
        "remote_code": "prohibited",
        "interpretation_allowed": False,
        "supported": profile["status"] == "supported",
        "output_provenance": fixture["expected_provenance"],
        "limitations": [
            "synthetic descriptor probe only",
            "no upstream framework executed",
            "no clinical interpretation or support claim",
        ],
    }
    payload = json.dumps(disclosure, sort_keys=True, separators=(",", ":")).encode()
    disclosure["receipt_sha256"] = hashlib.sha256(payload).hexdigest()
    return disclosure


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    probe = sub.add_parser("probe")
    probe.add_argument("--profile", required=True)
    probe.add_argument("--fixture", required=True)
    args = parser.parse_args()
    registry = load_registry()
    if args.command == "validate":
        errors = validate_registry(registry)
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            return 1
        print("Multimodal capability registry validation passed.")
        return 0
    print(
        json.dumps(
            execution_disclosure(registry, args.profile, args.fixture), indent=2, sort_keys=True
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
