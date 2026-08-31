"""Deterministic command surface for the Safety Systems Workbench harness."""

from __future__ import annotations

import argparse
import json
import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools.autonomy_harness import WorkItem, paths_conflict, select_next_ready
from tools.autonomy_state import StateStore, next_action
from tools.validate_repository import validate

MODES = {"public_remote", "governed_hybrid", "fully_local", "air_gapped"}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(item) for item in value)


def _timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be text")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def doctor(root: Path) -> dict[str, Any]:
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


def validate_context(payload: dict[str, Any]) -> list[str]:
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
    if not isinstance(payload.get("privacy_mode"), str) or payload["privacy_mode"] not in MODES:
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
        not isinstance(budget, dict)
        or not budget
        or any(
            key not in {"files", "tokens", "bytes"} or type(value) is not int or value <= 0
            for key, value in budget.items()
        )
    ):
        errors.append("invalid context_budget")
    for field in ("owned_files", "authoritative_inputs"):
        if _strings(payload.get(field)):
            try:
                paths_conflict(payload[field], ())
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


def validate_receipt(payload: dict[str, Any]) -> list[str]:
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
    if not isinstance(payload.get("privacy_mode"), str) or payload["privacy_mode"] not in MODES:
        errors.append("invalid privacy_mode")
    for field in ("results", "limitations"):
        if not _strings(payload.get(field)):
            errors.append(f"invalid {field}")
    commands = payload.get("commands")
    if (
        not isinstance(commands, list)
        or not commands
        or not all(_strings(command) for command in commands)
    ):
        errors.append("invalid commands")
    try:
        if _timestamp(payload.get("timestamp")) > datetime.now(UTC):
            raise ValueError("future receipt")
    except ValueError:
        errors.append("invalid timestamp")
    return errors


def _work_item(payload: dict[str, Any]) -> WorkItem:
    if not isinstance(payload, dict):
        raise ValueError("work item must be an object")
    if any(not _text(payload.get(field)) for field in ("id", "track_id", "status", "lane")):
        raise ValueError("work item requires non-empty identity, status and lane")
    for field in ("dependencies", "owned_paths"):
        value = payload.get(field, [])
        if not isinstance(value, list) or any(not _text(item) for item in value):
            raise ValueError(f"invalid {field}")
    if any(type(payload.get(field, 0)) is not int for field in ("priority", "criticality")):
        raise ValueError("priority and criticality must be integers")
    if payload.get("blocker") is not None and not _text(payload["blocker"]):
        raise ValueError("blocker must be non-empty text or null")
    return WorkItem(
        id=str(payload["id"]),
        track_id=str(payload["track_id"]),
        status=str(payload["status"]),
        lane=str(payload["lane"]),
        priority=int(payload.get("priority", 0)),
        criticality=int(payload.get("criticality", 0)),
        dependencies=tuple(map(str, payload.get("dependencies", []))),
        owned_paths=tuple(map(str, payload.get("owned_paths", []))),
        blocker=str(payload["blocker"]) if payload.get("blocker") else None,
    )


def select_queue(payload: dict[str, Any]) -> dict[str, Any]:
    for field in ("items", "active", "completed"):
        if not isinstance(payload.get(field, []), list):
            raise ValueError(f"{field} must be an array")
    if any(not _text(item) for item in payload.get("completed", [])):
        raise ValueError("completed must contain task identifiers")
    items = [_work_item(item) for item in payload.get("items", [])]
    active = [_work_item(item) for item in payload.get("active", [])]
    configured_limits = payload.get("lane_limits")
    if configured_limits is not None and not isinstance(configured_limits, dict):
        raise ValueError("lane_limits must be an object")
    selected = select_next_ready(
        items,
        completed=set(map(str, payload.get("completed", []))),
        active=active,
        lane_limits=configured_limits,
    )
    return {
        "status": "ready" if selected else "no_ready_work",
        "selected": selected.id if selected else None,
    }


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
    state_parser = subparsers.add_parser("state")
    state_parser.add_argument(
        "operation", choices=("initialise", "next", "advance", "resume", "recover")
    )
    state_parser.add_argument("checkpoint", type=Path)
    state_parser.add_argument("--root", type=Path, default=Path.cwd())
    state_parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    if args.command == "state":
        store = StateStore(args.checkpoint)
        payload = _read_object(args.input) if args.input is not None else {}
        if args.operation == "initialise":
            state = store.initialise(payload["tracks"], base_revision=payload["base_revision"])
        elif args.operation == "advance":
            state = store.advance(
                root=args.root,
                event_id=payload["event_id"],
                action=payload["action"],
                receipt=payload.get("receipt"),
                wake_condition=payload.get("wake_condition"),
            )
        elif args.operation == "resume":
            state = store.resume(
                root=args.root,
                track_id=payload["track_id"],
                event_id=payload["event_id"],
                receipt=payload["receipt"],
            )
        elif args.operation == "recover":
            store.recover(root=args.root, receipt=payload["receipt"])
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
        result = doctor(args.root.resolve())
        if args.command == "reconcile":
            result["hosted_state_checked"] = False
            result["external_completion_claim"] = False
    elif args.command == "context":
        errors = validate_context(_read_object(args.input))
        result = {"status": "pass" if not errors else "fail", "errors": errors}
    elif args.command == "receipt":
        errors = validate_receipt(_read_object(args.input))
        result = {"status": "pass" if not errors else "fail", "errors": errors}
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
