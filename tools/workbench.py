"""Deterministic command surface for the Safety Systems Workbench harness."""

from __future__ import annotations

import argparse
import json
import platform
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, NotRequired, TypedDict, TypeGuard

from tools.autonomy_harness import WorkItem, paths_conflict, select_next_ready
from tools.autonomy_state import StateStore, next_action
from tools.faw07_d0_demo import generate_receipt
from tools.json_shapes import JsonObject, is_array, is_object
from tools.validate_repository import validate

MODES = {"public_remote", "governed_hybrid", "fully_local", "air_gapped"}


class DoctorResult(TypedDict):
    status: Literal["pass", "fail"]
    root: str
    python: str
    governance_errors: list[str]
    network_checked: Literal[False]
    credentials_checked: Literal[False]
    model_execution: Literal[False]
    hosted_state_checked: NotRequired[Literal[False]]
    external_completion_claim: NotRequired[Literal[False]]


class QueueSelection(TypedDict):
    status: Literal["ready", "no_ready_work"]
    selected: str | None


def _text(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and bool(value.strip())


def _text_array(value: object) -> TypeGuard[list[str]]:
    return is_array(value) and all(_text(item) for item in value)


def _strings(value: object) -> TypeGuard[list[str]]:
    return _text_array(value) and bool(value)


def _timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be text")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def _read_object(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not is_object(value):
        raise ValueError("input must be a JSON object")
    return value


def doctor(root: Path) -> DoctorResult:
    errors = validate(root)
    return {
        "status": "pass" if not errors else "fail",
        "root": str(root),
        "python": platform.python_version(),
        "governance_errors": errors,
        "network_checked": False,
        "credentials_checked": False,
        "model_execution": False,
    }


def validate_context(payload: Mapping[str, object]) -> list[str]:
    required = {
        "track_id",
        "task_id",
        "base_revision",
        "created_at",
        "fresh_until",
        "privacy_mode",
        "context_budget",
        "owned_files",
        "authoritative_inputs",
        "excluded_context",
        "next_ready_step",
        "rollback",
    }
    errors = [f"missing {field}" for field in sorted(required) if not payload.get(field)]
    privacy_mode = payload.get("privacy_mode")
    if not isinstance(privacy_mode, str) or privacy_mode not in MODES:
        errors.append("invalid privacy_mode")
    for field in required - {
        "context_budget",
        "owned_files",
        "authoritative_inputs",
        "excluded_context",
        "privacy_mode",
    }:
        if payload.get(field) and not _text(payload[field]):
            errors.append(f"invalid {field}")
    for field in ("owned_files", "authoritative_inputs", "excluded_context"):
        if not _strings(payload.get(field)):
            errors.append(f"invalid {field}")
    budget = payload.get("context_budget")
    if (
        not is_object(budget)
        or not budget
        or any(
            key not in {"files", "tokens", "bytes"} or type(value) is not int or value <= 0
            for key, value in budget.items()
        )
    ):
        errors.append("invalid context_budget")
    for field in ("owned_files", "authoritative_inputs"):
        values = payload.get(field)
        if _strings(values):
            try:
                paths_conflict(values, ())
            except ValueError:
                errors.append(f"non-portable {field}")
    try:
        created = _timestamp(payload.get("created_at"))
        now = datetime.now(UTC)
        if created > now:
            raise ValueError("future creation")
        if payload.get("fresh_until") != "source-change":
            expires = _timestamp(payload.get("fresh_until"))
            if expires <= now or expires < created:
                raise ValueError("expired context")
    except ValueError:
        errors.append("invalid or stale context timestamps")
    return errors


def validate_receipt(payload: Mapping[str, object]) -> list[str]:
    required = {
        "task_id",
        "revision",
        "timestamp",
        "privacy_mode",
        "commands",
        "results",
        "limitations",
        "rollback",
    }
    errors = [
        f"missing {field}" for field in sorted(required) if payload.get(field) in (None, "", [])
    ]
    for field in required - {"commands", "results", "limitations", "privacy_mode"}:
        if not _text(payload.get(field)):
            errors.append(f"invalid {field}")
    privacy_mode = payload.get("privacy_mode")
    if not isinstance(privacy_mode, str) or privacy_mode not in MODES:
        errors.append("invalid privacy_mode")
    for field in ("results", "limitations"):
        if not _strings(payload.get(field)):
            errors.append(f"invalid {field}")
    commands = payload.get("commands")
    if not is_array(commands) or not commands or not all(_strings(command) for command in commands):
        errors.append("invalid commands")
    try:
        if _timestamp(payload.get("timestamp")) > datetime.now(UTC):
            raise ValueError("future receipt")
    except ValueError:
        errors.append("invalid timestamp")
    return errors


def _work_item(payload: object) -> WorkItem:
    if not is_object(payload):
        raise ValueError("work item must be an object")
    identities: dict[str, str] = {}
    for field in ("id", "track_id", "status", "lane"):
        value = payload.get(field)
        if not _text(value):
            raise ValueError("work item requires non-empty identity, status and lane")
        identities[field] = value
    arrays: dict[str, list[str]] = {}
    for field in ("dependencies", "owned_paths"):
        value = payload.get(field, [])
        if not _text_array(value):
            raise ValueError(f"invalid {field}")
        arrays[field] = value
    priority, criticality = payload.get("priority", 0), payload.get("criticality", 0)
    if type(priority) is not int or type(criticality) is not int:
        raise ValueError("priority and criticality must be integers")
    blocker = payload.get("blocker")
    if blocker is not None and not _text(blocker):
        raise ValueError("blocker must be non-empty text or null")
    return WorkItem(
        id=identities["id"],
        track_id=identities["track_id"],
        status=identities["status"],
        lane=identities["lane"],
        priority=priority,
        criticality=criticality,
        dependencies=tuple(arrays["dependencies"]),
        owned_paths=tuple(arrays["owned_paths"]),
        blocker=blocker,
    )


def select_queue(payload: Mapping[str, object]) -> QueueSelection:
    collections: dict[str, list[object]] = {}
    for field in ("items", "active", "completed"):
        value = payload.get(field, [])
        if not is_array(value):
            raise ValueError(f"{field} must be an array")
        collections[field] = value
    completed = collections["completed"]
    if not _text_array(completed):
        raise ValueError("completed must contain task identifiers")
    items = [_work_item(item) for item in collections["items"]]
    active = [_work_item(item) for item in collections["active"]]
    configured_limits = payload.get("lane_limits")
    if configured_limits is not None and not is_object(configured_limits):
        raise ValueError("lane_limits must be an object")
    selected = select_next_ready(
        items,
        completed=set(completed),
        active=active,
        lane_limits=configured_limits,
    )
    return {
        "status": "ready" if selected else "no_ready_work",
        "selected": selected.id if selected else None,
    }


def _input_text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("command field must be text")
    return value


def _optional_input_text(value: object) -> str | None:
    return None if value is None else _input_text(value)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--root", type=Path, default=Path.cwd())
    for name in ("context", "queue", "receipt"):
        command = subparsers.add_parser(name)
        command.add_argument("input", type=Path)
    subparsers.add_parser("validate").add_argument("--root", type=Path, default=Path.cwd())
    subparsers.add_parser("reconcile").add_argument("--root", type=Path, default=Path.cwd())
    subparsers.add_parser("evaluate")
    subparsers.add_parser("d0-demo")
    state_parser = subparsers.add_parser("state")
    state_parser.add_argument(
        "operation", choices=("initialise", "next", "advance", "resume", "recover")
    )
    state_parser.add_argument("checkpoint", type=Path)
    state_parser.add_argument("--root", type=Path, default=Path.cwd())
    state_parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    result: Mapping[str, object]
    if args.command == "state":
        store = StateStore(args.checkpoint)
        payload: JsonObject = _read_object(args.input) if args.input is not None else {}
        if args.operation == "initialise":
            state = store.initialise(payload["tracks"], base_revision=payload["base_revision"])
        elif args.operation == "advance":
            state = store.advance(
                root=args.root,
                event_id=_input_text(payload["event_id"]),
                action=payload["action"],
                receipt=_optional_input_text(payload.get("receipt")),
                wake_condition=_optional_input_text(payload.get("wake_condition")),
            )
        elif args.operation == "resume":
            state = store.resume(
                root=args.root,
                track_id=_input_text(payload["track_id"]),
                event_id=_input_text(payload["event_id"]),
                receipt=_input_text(payload["receipt"]),
            )
        elif args.operation == "recover":
            store.recover(root=args.root, receipt=_input_text(payload["receipt"]))
            state = store.load()
        else:
            state = store.load()
        result = {
            "status": "pass",
            "next_action": next_action(state),
            "model_execution": False,
            "circuit_breaker": state["circuit_breaker"],
        }
    elif args.command in {"doctor", "validate", "reconcile"}:
        diagnosis = doctor(args.root.resolve())
        if args.command == "reconcile":
            diagnosis["hosted_state_checked"] = False
            diagnosis["external_completion_claim"] = False
        result = diagnosis
    elif args.command == "context":
        errors = validate_context(_read_object(args.input))
        result = {"status": "pass" if not errors else "fail", "errors": errors}
    elif args.command == "receipt":
        errors = validate_receipt(_read_object(args.input))
        result = {"status": "pass" if not errors else "fail", "errors": errors}
    elif args.command == "d0-demo":
        receipt = generate_receipt()
        print(
            json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        )
        return 1 if receipt["oracle_mismatches"] else 0
    elif args.command == "evaluate":
        result = {
            "status": "unavailable",
            "reason": "model and human evaluation require separately admitted execution evidence",
            "model_execution": False,
        }
    else:
        result = select_queue(_read_object(args.input))
    print(json.dumps(result, sort_keys=True))
    if result["status"] in {"pass", "ready", "no_ready_work"}:
        return 0
    return 2 if result["status"] == "unavailable" else 1


def main(argv: list[str] | None = None) -> int:
    try:
        return _main(argv)
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"status": "fail", "errors": ["invalid input or inaccessible file"]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
