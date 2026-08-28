"""Deterministic command surface for the Safety Systems Workbench harness."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from typing import Any

from tools.autonomy_harness import WorkItem, select_next_ready
from tools.validate_repository import validate


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
    modes = {"public_remote", "governed_hybrid", "fully_local", "air_gapped"}
    if payload.get("privacy_mode") not in modes:
        errors.append("invalid privacy_mode")
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
    return [f"missing {field}" for field in sorted(required) if payload.get(field) in (None, "", [])]


def _work_item(payload: dict[str, Any]) -> WorkItem:
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
    items = [_work_item(item) for item in payload.get("items", [])]
    active = [_work_item(item) for item in payload.get("active", [])]
    configured_limits = {
        key: int(value) for key, value in payload.get("lane_limits", {}).items()
    }
    selected = select_next_ready(
        items,
        completed=set(map(str, payload.get("completed", []))),
        active=active,
        lane_limits=configured_limits or None,
    )
    return {"status": "ready" if selected else "no_ready_work", "selected": selected.id if selected else None}


def main(argv: list[str] | None = None) -> int:
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
    args = parser.parse_args(argv)
    if args.command in {"doctor", "validate", "reconcile"}:
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


if __name__ == "__main__":
    raise SystemExit(main())
