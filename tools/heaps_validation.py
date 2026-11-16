"""Strict, bounded admission helpers for the synthetic HEAPS packet consumer."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from datetime import UTC, date, datetime
from hashlib import sha256
from pathlib import Path
from typing import Protocol, cast

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from tools.evidence_core import COLLECTION_IDS, fingerprint, validate_record
from tools.interface_actions import sanitize_export
from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

ROOT = Path(__file__).parents[1]
MAX_INPUT_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
MAX_DEPTH = 64
PATH_RE = re.compile(r"^(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9][A-Za-z0-9_.-]*$")
UTC_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])"
)
KINDS = {
    "roles": "role",
    "sources": "source",
    "artefacts": "artefact",
    "evidence": "evidence",
    "factors": "factor",
    "actions": "action",
    "reviews": "review",
    "outcomes": "outcome",
    "referrals": "referral",
}
INTEGER_KEYS = {
    "version",
    "profile_version",
    "offset",
    "bytes",
    "input_items",
    "usable_items",
    "abstained_items",
}
DATE_KEYS = {
    "acquired_at",
    "recorded_at",
    "occurred_at",
    "due_at",
    "review_at",
    "reconciled_at",
    "reviewed_at",
    "deadline",
    "evaluation_at",
    "issued_at",
    "expires_at",
    "evaluated_at",
}


class _Validator(Protocol):
    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


def obj(value: object, context: str = "object") -> JsonObject:
    return require_object(value, context=context)


def text(value: object, context: str = "text") -> str:
    if not isinstance(value, str):
        raise ValueError(f"{context}: expected text")
    return value


def rows(value: object) -> list[JsonObject]:
    return object_rows(value)


def json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode("utf-8")


def raw_hash(value: bytes) -> str:
    return sha256(value).hexdigest()


def _pairs(pairs: list[tuple[str, object]]) -> JsonObject:
    result: JsonObject = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON ingress: duplicate object key")
        result[key] = value
    return result


def _constant(_value: str) -> object:
    raise ValueError("JSON ingress: nonfinite number")


def walk(value: object, depth: int = 0) -> Iterable[object]:
    if depth > MAX_DEPTH:
        raise ValueError("JSON ingress: nesting exceeds 64 levels")
    yield value
    if is_object(value):
        for key, item in value.items():
            yield key
            yield from walk(item, depth + 1)
    elif is_array(value):
        for item in value:
            yield from walk(item, depth + 1)


def ensure_bytes(payload: object) -> bytes:
    if not isinstance(payload, bytes):
        raise ValueError("artifact: payload must be bytes")
    return payload


def parse_json(payload: bytes, context: str) -> JsonObject:
    payload = ensure_bytes(payload)
    if not payload or len(payload) > MAX_INPUT_BYTES:
        raise ValueError(f"{context}: empty or oversized JSON ingress")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{context}: JSON byte-order mark is forbidden")
    try:
        value: object = json.loads(
            payload.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant
        )
        for item in walk(value):
            if isinstance(item, str):
                item.encode("utf-8")
            if isinstance(item, float) and not math.isfinite(item):
                raise ValueError("nonfinite number")
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError):
            reason = (
                str(exc)
                if str(exc).startswith("JSON ingress:")
                else "invalid UTF-8, surrogate, finite-number or nesting boundary"
            )
        else:
            reason = "invalid UTF-8, JSON syntax or nesting boundary"
        raise ValueError(f"{context}: {reason}") from None
    return obj(value, context)


def schema_errors(name: str, value: JsonObject) -> list[str]:
    schema = parse_json((ROOT / "evaluation/heaps" / f"{name}.schema.json").read_bytes(), "schema")
    validator = cast(_Validator, Draft202012Validator(schema))
    # Do not reflect untrusted values in diagnostics.
    return sorted(
        {
            f"{name}: {'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.validator}"
            for error in validator.iter_errors(value)
        }
    )


def safe_path(value: object) -> str:
    path = text(value, "artifact path")
    if len(path) > 240 or PATH_RE.fullmatch(path) is None:
        raise ValueError("artifact path: unsafe relative path")
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    if any(
        part.endswith((".", " ")) or part.split(".")[0].upper() in reserved
        for part in path.split("/")
    ):
        raise ValueError("artifact path: nonportable reserved name")
    return path


def utc_time(value: object, context: str) -> datetime:
    stamp = text(value, context)
    if UTC_RE.fullmatch(stamp) is None:
        raise ValueError(f"{context}: requires strict UTC second timestamp")
    try:
        return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        raise ValueError(f"{context}: impossible timestamp") from None


def timestamp(value: object, context: str) -> None:
    stamp = text(value, context)
    if TIMESTAMP_RE.fullmatch(stamp) is None:
        raise ValueError(f"{context}: invalid RFC3339 timestamp")
    try:
        datetime.fromisoformat(stamp)
    except ValueError:
        raise ValueError(f"{context}: impossible timestamp") from None


def strict_fields(value: object) -> None:
    for item in walk(value):
        if not is_object(item):
            continue
        for key, field in item.items():
            if key in INTEGER_KEYS and field is not None and type(field) is not int:
                # Snapshot version is explicitly a nullable string, unlike case versions.
                if key == "version" and "snapshot_id" in item and isinstance(field, str):
                    continue
                raise ValueError(f"{key}: requires a true integer")
            if key in DATE_KEYS and field is not None:
                timestamp(field, key)
        if {"state", "value", "precision", "basis_refs", "uncertainty"} <= set(item):
            if item["state"] != "known":
                continue
            value_text = text(item["value"], "time assertion")
            precision = item["precision"]
            try:
                if precision == "day" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value_text):
                    date.fromisoformat(value_text)
                elif precision == "minute" and re.fullmatch(
                    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z", value_text
                ):
                    datetime.strptime(value_text, "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC)
                elif precision == "second":
                    utc_time(value_text, "time assertion")
                else:
                    raise ValueError("unsupported precision")
            except ValueError:
                raise ValueError("time assertion: impossible date/time or precision") from None
            if not item["basis_refs"]:
                raise ValueError("time assertion: known value requires a source basis")


def reference_index(case: JsonObject) -> dict[str, tuple[str, JsonObject]]:
    index: dict[str, tuple[str, JsonObject]] = {}
    for collection, key in COLLECTION_IDS.items():
        for row in rows(case.get(collection)):
            kind = (
                text(row.get("kind"))
                if collection == "statements"
                else KINDS.get(collection, "event")
            )
            index[text(row.get(key))] = (kind, row)
    return index


def check_references(value: object, index: Mapping[str, tuple[str, JsonObject]]) -> None:
    for item in walk(value):
        if not is_object(item) or set(item) != {"kind", "id"}:
            continue
        target = index.get(text(item["id"]))
        if target is None:
            raise ValueError(
                "reference.unresolved: typed target does not resolve in the bound case"
            )
        if target[0] != item["kind"]:
            raise ValueError("reference.kind: typed target kind mismatch")


def target(value: object, index: Mapping[str, tuple[str, JsonObject]]) -> JsonObject:
    ref = obj(value, "typed reference")
    return index[text(ref["id"])][1]


def _require_eligible_support(
    kind: str, support: JsonObject, index: Mapping[str, tuple[str, JsonObject]]
) -> None:
    if kind == "factor":
        if support["status"] in {"withdrawn", "rejected"}:
            raise ValueError(
                f"factor.promotion: {support['factor_id']} is {support['status']}; cannot support accepted finding"
            )
        # Factor meaning is carried by its directly referenced canonical
        # statement. Do not infer support through further graph relationships.
        statement = index[text(support["statement_id"])][1]
        _require_eligible_statement(statement)
    elif kind == "evidence" and support["custody_state"] == "withdrawn":
        raise ValueError("finding support: withdrawn evidence cannot support accepted finding")
    else:
        _require_eligible_statement(support)


def _require_eligible_statement(statement: JsonObject) -> None:
    if statement.get("withdrawn") is True or (
        is_object(statement.get("provenance"))
        and obj(statement["provenance"]).get("review_state") in {"withdrawn", "rejected"}
    ):
        raise ValueError(
            "finding support: withdrawn or rejected statement cannot support accepted finding"
        )


def admit_case_profile(case: JsonObject, profile: JsonObject) -> dict[str, tuple[str, JsonObject]]:
    core_errors = validate_record(case)
    if core_errors:
        # The shared validator includes payloads in some messages; only emit a safe boundary.
        raise ValueError(
            "canonical record: schema, reference, duplicate identity or transition validation failed"
        )
    if case.get("schema_version") != "1.1" or case.get("privacy_mode") != "fully_local":
        raise ValueError("canonical record: safety-work 1.1 and fully_local are required")
    errors = schema_errors("heaps-profile", profile)
    if errors:
        raise ValueError("; ".join(errors[:16]))
    strict_fields(case)
    strict_fields(profile)
    binding = obj(profile["case_binding"])
    for key in ("case_id", "version"):
        if binding[key] != case[key]:
            raise ValueError(f"case_binding.{key}: stale or wrong case binding")
    if binding["fingerprint"] != fingerprint(case):
        raise ValueError("case_binding.fingerprint: stale canonical binding")
    # Preserve the established shared safety restriction for every rendered value.
    sanitize_export(case)
    sanitize_export(profile)
    index = reference_index(case)
    check_references(profile, index)
    for relationship in rows(case.get("relationships")):
        if relationship["relation"] != "supports":
            continue
        target_kind, finding = index[text(relationship["to_id"])]
        if target_kind == "finding" and obj(finding["provenance"])["review_state"] == "accepted":
            support_kind, support = index[text(relationship["from_id"])]
            _require_eligible_support(support_kind, support, index)
    return index


def validate_profile_semantics(
    profile: JsonObject, index: Mapping[str, tuple[str, JsonObject]]
) -> None:
    snapshots = rows(profile["source_snapshots"])
    snapshot_index: dict[str, JsonObject] = {}
    source_ids: set[str] = set()
    for snapshot in snapshots:
        sid = text(snapshot["snapshot_id"])
        source_id = text(snapshot["source_id"])
        if sid in snapshot_index or source_id in source_ids:
            raise ValueError("source snapshot: duplicate snapshot or source identity")
        if source_id not in index or index[source_id][0] != "source":
            raise ValueError("source snapshot: unresolved canonical source")
        snapshot_index[sid] = snapshot
        source_ids.add(source_id)
    canonical_sources = {identifier for identifier, (kind, _) in index.items() if kind == "source"}
    if source_ids != canonical_sources:
        raise ValueError(
            "source snapshots: every canonical source requires an explicit availability state"
        )
    families: dict[str, JsonObject] = {}
    for family in rows(profile["source_families"]):
        source_id = text(obj(family["source_ref"])["id"])
        if source_id in families:
            raise ValueError("source family: duplicate source identity")
        families[source_id] = family
    if set(families) != source_ids:
        raise ValueError("source family: every canonical source requires a lineage entry")
    for snapshot in snapshots:
        family = families.get(text(snapshot["source_id"]))
        if family is None or family["family_id"] != snapshot["source_family_id"]:
            raise ValueError("source family: snapshot lineage mismatch or missing")
    for source_id, family in families.items():
        for parent in rows(family["derived_from"]):
            parent_id = text(parent["id"])
            if parent_id == source_id or parent_id not in families:
                raise ValueError("source family: invalid derivation")
            if families[parent_id]["family_id"] != family["family_id"]:
                raise ValueError("source family: derivative must retain family identity")
    for start in families:
        pending = [text(row["id"]) for row in rows(families[start]["derived_from"])]
        visited: set[str] = set()
        while pending:
            current = pending.pop()
            if current == start:
                raise ValueError("source family: cyclic derivation")
            if current not in visited:
                visited.add(current)
                pending.extend(text(row["id"]) for row in rows(families[current]["derived_from"]))
    app = obj(profile["applicability"])
    for field, purpose in (("procedure_snapshot_id", "procedure"),):
        sid = app[field]
        if sid is not None and (
            sid not in snapshot_index
            or purpose not in text_list(snapshot_index[text(sid)]["purposes"])
        ):
            raise ValueError("applicability: unresolved procedure snapshot")
    obligation_ids = app["obligation_snapshot_ids"]
    if is_array(obligation_ids):
        for sid in obligation_ids:
            snapshot = snapshot_index.get(text(sid))
            if snapshot is None or "obligation" not in text_list(snapshot["purposes"]):
                raise ValueError("applicability: unresolved obligation snapshot")
    clocks = obj(profile["clocks"])
    deadlines = rows(profile["deadlines"])
    deadline_ids = [text(row["deadline_id"]) for row in deadlines]
    if len(deadline_ids) != len(set(deadline_ids)):
        raise ValueError("deadline: duplicate identity")
    for deadline in deadlines:
        for field in ("source_snapshot_id", "calendar_snapshot_id"):
            sid = deadline[field]
            if sid is not None and sid not in snapshot_index:
                raise ValueError(f"deadline: unresolved {field}")
        if deadline["state"] != "specified_unverified":
            continue
        trigger = obj(clocks[text(deadline["trigger_clock"])])
        if trigger["state"] != "known" or not trigger["basis_refs"]:
            raise ValueError("deadline.trigger: known sourced trigger is required")
        if deadline["time_zone"] != "UTC":
            raise ValueError(
                "deadline.calendar: only the explicit UTC synthetic timezone is supported"
            )
        for field, purpose in (
            ("source_snapshot_id", "obligation"),
            ("calendar_snapshot_id", "calendar"),
        ):
            snapshot = snapshot_index[text(deadline[field])]
            if (
                snapshot["state"] != "available"
                or not snapshot["version"]
                or not snapshot["raw_sha256"]
                or purpose not in text_list(snapshot["purposes"])
                or snapshot["applicability"] != "applies_synthetic"
            ):
                raise ValueError(
                    f"deadline.calendar: {purpose} source/version/applicability is unresolved"
                )
    for context in rows(profile["action_context"]):
        if context["deadline_id"] is not None and context["deadline_id"] not in deadline_ids:
            raise ValueError("action context: unresolved deadline")
        action = target(context["action_ref"], index)
        if action["recommendation_id"] != obj(context["recommendation_ref"])["id"]:
            raise ValueError("action context: recommendation does not match canonical action")
    for context in rows(profile["finding_context"]):
        finding = target(context["finding_ref"], index)
        if obj(finding["provenance"])["review_state"] != "accepted":
            continue
        for ref in rows(context["supporting_refs"]):
            _require_eligible_support(text(ref["kind"]), target(ref, index), index)
    for assignment in rows(profile["factor_assignments"]):
        if assignment["state"] != "mapped":
            continue
        candidates = [
            snapshot
            for snapshot in snapshots
            if assignment["taxonomy_id"] in {snapshot["snapshot_id"], snapshot["source_id"]}
        ]
        if len(candidates) != 1:
            raise ValueError(
                "taxonomy: mapped assignment requires an explicit captured taxonomy snapshot"
            )
        taxonomy = candidates[0]
        if (
            taxonomy["state"] != "available"
            or "taxonomy" not in text_list(taxonomy["purposes"])
            or taxonomy["version"] != assignment["taxonomy_version"]
            or not taxonomy["raw_sha256"]
        ):
            raise ValueError("taxonomy: source purpose, version or available bytes do not match")
    mapping = obj(profile["template_mapping"])
    sid = mapping["source_snapshot_id"]
    if sid is not None and sid not in snapshot_index:
        raise ValueError("template mapping: unresolved source snapshot")
    for field, refkey in (
        ("roles", "role_ref"),
        ("participation", "role_ref"),
        ("factor_assignments", "factor_ref"),
        ("finding_context", "finding_ref"),
        ("action_context", "action_ref"),
    ):
        ids = [text(obj(row[refkey])["id"]) for row in rows(profile[field])]
        if len(ids) != len(set(ids)):
            raise ValueError(f"{field}: duplicate referenced identity")


def text_list(value: object) -> list[str]:
    if not is_array(value) or not all(isinstance(item, str) for item in value):
        raise ValueError("expected a text array")
    return [text(item) for item in value]


def artifact_descriptor(artifact_id: str, path: str, payload: bytes) -> JsonObject:
    return {
        "artifact_id": artifact_id,
        "path": safe_path(path),
        "sha256": raw_hash(payload),
        "bytes": len(payload),
    }


def read_artifact(descriptor: JsonObject, artifacts: Mapping[str, bytes]) -> tuple[str, bytes]:
    path = safe_path(descriptor["path"])
    payload = artifacts.get(path)
    if payload is None:
        raise ValueError("artifact.raw_byte_identity: required artifact is missing")
    if not payload or len(payload) > MAX_INPUT_BYTES:
        raise ValueError("artifact.raw_byte_identity: empty or oversized artifact")
    if (
        type(descriptor["bytes"]) is not int
        or descriptor["bytes"] != len(payload)
        or descriptor["sha256"] != raw_hash(payload)
    ):
        raise ValueError("artifact.raw_byte_identity: stale bytes, size or hash")
    return path, payload


def manifest_inventory(manifest: JsonObject, artifacts: Mapping[str, bytes]) -> dict[str, bytes]:
    errors = schema_errors("packet-manifest", manifest)
    if errors:
        raise ValueError("; ".join(errors[:16]))
    strict_fields(manifest)
    consumed: dict[str, bytes] = {}
    identifiers: set[str] = set()
    casefold_paths: set[str] = set()
    components = obj(manifest["components"])
    for name in (
        "case",
        "profile",
        "sources",
        "supporting_artifacts",
        "mapping",
        "template",
        "reports",
    ):
        group = components[name]
        entries = rows(group) if is_array(group) else [obj(group)]
        paths = [text(entry["path"]) for entry in entries]
        if paths != sorted(paths) or len(paths) != len(set(paths)):
            raise ValueError("manifest: inventory must have unique ascending paths")
        for entry in entries:
            path = safe_path(entry["path"])
            if path.casefold() in {
                "manifest.json",
                "decision.json",
                "status.json",
                "verification.json",
                "verification-input-manifest.json",
                "verification-input-status.json",
            }:
                raise ValueError("manifest: self or later receipt is forbidden")
            path, payload = read_artifact(entry, artifacts)
            candidate: JsonObject | None = None
            if path.endswith(".json"):
                candidate = parse_json(payload, "manifest artifact")
            else:
                detection_bytes = payload[3:] if payload.startswith(b"\xef\xbb\xbf") else payload
                if detection_bytes.lstrip().startswith(b"{"):
                    try:
                        candidate = parse_json(detection_bytes, "manifest artifact")
                    except ValueError:
                        candidate = None
            if candidate is not None and candidate.get("schema_version") in {
                "heaps-packet-manifest-1.0",
                "heaps-review-decision-1.0",
                "heaps-status-receipt-1.0",
                "heaps-verification-1.0",
            }:
                raise ValueError("manifest: self or later receipt payload is forbidden")
            identifier = text(entry["artifact_id"])
            if path.casefold() in casefold_paths or identifier in identifiers:
                raise ValueError("manifest: duplicate path or artifact identity")
            casefold_paths.add(path.casefold())
            identifiers.add(identifier)
            consumed[path] = payload
    if sum(map(len, consumed.values())) > MAX_TOTAL_BYTES:
        raise ValueError("manifest: total consumed bytes exceeds 32 MiB")
    return consumed
