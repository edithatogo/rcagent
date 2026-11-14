"""Fail-closed multimodal capability contracts and synthetic probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from collections.abc import Iterable
from pathlib import Path
from typing import Literal, Protocol, TypedDict, TypeGuard, cast

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from tools import json_shapes

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "evaluation/multimodal/registry.json"
SCHEMA_PATH = ROOT / "conductor/schemas/multimodal-capability.schema.json"
SUPPORT_MATRIX_PATH = ROOT / "evaluation/multimodal/support-matrix-20260829.json"


class _RegistryValidator(Protocol):
    def iter_errors(self, _instance: object) -> Iterable[ValidationError]: ...


class Privacy(TypedDict):
    network: str
    remote_code: str


class Limits(TypedDict):
    device_classes: list[str]


class Profile(TypedDict):
    id: str
    modality: str
    framework: str
    revision: str
    governance: str
    status: str
    privacy: Privacy
    limits: Limits


class Fixture(TypedDict):
    id: str
    profile_id: str
    expected_provenance: list[json_shapes.JsonObject]


class Registry(TypedDict):
    profiles: list[Profile]
    fixtures: list[Fixture]


class DisclosureBody(TypedDict):
    schema_version: Literal["1.0"]
    profile_id: str
    fixture_id: str
    framework: str
    revision: str
    governance: str
    capability_status: str
    execution_mode: Literal["deterministic-contract-probe"]
    device: str
    network: Literal["disabled"]
    telemetry: Literal["none"]
    remote_code: Literal["prohibited"]
    interpretation_allowed: Literal[False]
    supported: bool
    output_provenance: list[json_shapes.JsonObject]
    limitations: list[str]


class ExecutionDisclosure(DisclosureBody):
    receipt_sha256: str


def _is_profile(value: object) -> TypeGuard[Profile]:
    if not json_shapes.is_object(value) or not all(
        isinstance(value.get(key), str)
        for key in ("id", "modality", "framework", "revision", "governance", "status")
    ):
        return False
    privacy, limits = value.get("privacy"), value.get("limits")
    if not json_shapes.is_object(privacy) or not all(
        isinstance(privacy.get(key), str) for key in ("network", "remote_code")
    ):
        return False
    if not json_shapes.is_object(limits):
        return False
    devices = limits.get("device_classes")
    return json_shapes.is_array(devices) and all(isinstance(item, str) for item in devices)


def _is_fixture(value: object) -> TypeGuard[Fixture]:
    if not json_shapes.is_object(value) or not all(
        isinstance(value.get(key), str) for key in ("id", "profile_id")
    ):
        return False
    provenance = value.get("expected_provenance")
    return json_shapes.is_array(provenance) and all(
        json_shapes.is_object(item) for item in provenance
    )


def _is_registry(value: object) -> TypeGuard[Registry]:
    if not json_shapes.is_object(value):
        return False
    profiles, fixtures = value.get("profiles"), value.get("fixtures")
    return (
        json_shapes.is_array(profiles)
        and all(_is_profile(item) for item in profiles)
        and json_shapes.is_array(fixtures)
        and all(_is_fixture(item) for item in fixtures)
    )


def _read(path: Path) -> json_shapes.JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not json_shapes.is_object(value):
        raise ValueError(f"{path}: expected an object")
    return value


def load_registry() -> Registry:
    registry = _read(REGISTRY_PATH)
    if not _is_registry(registry):
        raise ValueError("registry profiles and fixtures have invalid field shapes")
    return registry


def validate_registry(registry: object) -> list[str]:
    schema = _read(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    # jsonschema validates arbitrary instances; its overloaded stub leaves one
    # branch unknown. Narrow only that third-party interface, never the payload.
    validator = cast(_RegistryValidator, Draft202012Validator(schema))
    errors = [
        f"{'.'.join(map(str, error.absolute_path))}: {error.message}"
        for error in validator.iter_errors(registry)
    ]
    if not json_shapes.is_object(registry):
        return sorted(errors)
    # The schema pass diagnoses invalid containers; domain checks only traverse
    # immediate object rows and leave their values untrusted.
    profiles = json_shapes.object_rows(registry.get("profiles"))
    fixtures = json_shapes.object_rows(registry.get("fixtures"))
    profile_ids = [item.get("id") for item in profiles]
    fixture_ids = [item.get("id") for item in fixtures]
    for label, values in (("profiles", profile_ids), ("fixtures", fixture_ids)):
        errors.extend(
            f"{label}: duplicate id {value!r}"
            for value in sorted({item for item in values if isinstance(item, str)})
            if values.count(value) > 1
        )
    known_profiles = {item for item in profile_ids if isinstance(item, str)}
    for fixture in fixtures:
        profile_id = fixture.get("profile_id")
        if not isinstance(profile_id, str) or profile_id not in known_profiles:
            errors.append(f"fixtures: unknown profile {profile_id!r}")
    for profile in profiles:
        raw_privacy = profile.get("privacy")
        privacy = raw_privacy if json_shapes.is_object(raw_privacy) else {}
        if profile.get("status") != "supported" and privacy.get("network") not in (
            "disabled",
            "disabled until admitted",
        ):
            errors.append(f"profiles: unadmitted {profile.get('id')!r} must disable network")
        if privacy.get("remote_code") != "prohibited":
            errors.append(f"profiles: {profile.get('id')!r} must prohibit remote code")
        if profile.get("modality") in ("image", "signal") and (
            profile.get("governance") != "research_disabled" or profile.get("status") == "supported"
        ):
            errors.append(
                f"profiles: {profile.get('id')!r} interpretation must remain research-disabled"
            )
    if SUPPORT_MATRIX_PATH.is_file():
        matrix = _read(SUPPORT_MATRIX_PATH)
        matrix_profiles = matrix.get("profiles", [])
        if not json_shapes.is_array(matrix_profiles):
            errors.append("support matrix profiles must be an array")
            matrix_profiles = []
        matrix_id_values = [
            item.get("profile_id") for item in json_shapes.object_rows(matrix_profiles)
        ]
        matrix_ids = {value for value in matrix_id_values if isinstance(value, str)}
        if (
            any(not isinstance(value, str) for value in matrix_id_values)
            or matrix_ids != known_profiles
        ):
            errors.append("support matrix profile identifiers must match the registry")
        for item in matrix_profiles:
            if not json_shapes.is_object(item):
                errors.append("support matrix profile must be an object")
                continue
            registry_profile = next(
                (profile for profile in profiles if profile.get("id") == item.get("profile_id")),
                None,
            )
            if registry_profile is None:
                continue
            device_classes = item.get("device_classes", {})
            limits = registry_profile.get("limits")
            registry_devices = (
                limits.get("device_classes") if json_shapes.is_object(limits) else None
            )
            if (
                not json_shapes.is_object(device_classes)
                or not json_shapes.is_array(registry_devices)
                or not all(isinstance(device, str) for device in registry_devices)
                or set(device_classes) != set(registry_devices)
            ):
                errors.append(
                    f"support matrix device classes differ for {item.get('profile_id')!r}"
                )
            evidence_paths = item.get("evidence", [])
            if not json_shapes.is_array(evidence_paths):
                errors.append("support matrix evidence must be an array")
                continue
            for evidence in evidence_paths:
                if not isinstance(evidence, str) or not (ROOT / evidence).is_file():
                    errors.append(f"support matrix evidence missing: {evidence!r}")
        raw_boundaries = matrix.get("global_boundaries")
        boundaries = raw_boundaries if json_shapes.is_object(raw_boundaries) else {}
        if (
            boundaries.get("remote_code") != "prohibited"
            or boundaries.get("clinical_interpretation") != "disabled"
        ):
            errors.append("support matrix safety boundary mismatch")
    return sorted(errors)


def execution_disclosure(registry: object, profile_id: str, fixture_id: str) -> ExecutionDisclosure:
    errors = validate_registry(registry)
    if errors:
        raise ValueError("invalid registry: " + "; ".join(errors))
    if not _is_registry(registry):
        raise ValueError("invalid registry: profiles and fixtures have invalid field shapes")
    profile = next((item for item in registry["profiles"] if item["id"] == profile_id), None)
    fixture = next((item for item in registry["fixtures"] if item["id"] == fixture_id), None)
    if profile is None or fixture is None or fixture["profile_id"] != profile_id:
        raise ValueError("unknown or mismatched profile and fixture")
    disclosure: DisclosureBody = {
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
    return {**disclosure, "receipt_sha256": hashlib.sha256(payload).hexdigest()}


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
