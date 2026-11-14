"""Sole guarded primary entry; completed observations remain unadmitted."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path

from tools import json_shapes
from tools import prospective_execution_gate as gate
from tools import prospective_runner_contract as runner
from tools import prospective_server_session as session


@dataclass(frozen=True)
class _Context:
    plan: session.PrimaryPlan
    protocol_path: Path
    pin: str
    slot_id: str
    review_commit: str
    root: Path
    model_root: Path

    def verify(self) -> None:
        current = gate.verify_execution_plan(
            self.protocol_path,
            self.pin,
            self.slot_id,
            self.review_commit,
            self.root,
            self.model_root,
        )
        if current.payload != self.plan.payload:
            raise ValueError("primary_gate_changed")

    def finish(self, result: session.SessionResult) -> None:
        value = json_shapes.require_object(self.plan.value(), context="primary plan")
        result["primary_gate"] = json_shapes.require_object(
            value["evidence"], context="primary evidence"
        )
        try:
            self.verify()
            if result["error"] == "none":
                value = json_shapes.require_object(self.plan.value(), context="primary plan")
                request = json_shapes.require_object(value["request"], context="primary request")
                admission = json_shapes.require_object(
                    value["admission"], context="model admission"
                )
                model_id = admission["model_id"]
                if not isinstance(model_id, str):
                    raise TypeError("invalid_primary_model")
                completion = result.get("completion")
                if completion is None:
                    raise KeyError("completion")
                result["candidate"] = json_shapes.require_object(
                    runner.normalize_candidate(
                        request,
                        base64.b64decode(completion["body_base64"], validate=True),
                        slot_id=self.slot_id,
                        expected_slot_id=self.slot_id,
                        expected_model=model_id,
                    ),
                    context="primary candidate",
                )
                result["status"] = "primary_session_captured"
        except (
            ValueError,
            OSError,
            KeyError,
            TypeError,
            RuntimeError,
            ImportError,
            KeyboardInterrupt,
            SystemExit,
        ):
            result["primary_postflight_error"] = "primary_postflight_failed"
            if result["error"] == "none":
                result["error"] = "primary_postflight_failed"
            result["status"] = "session_failed"


def run_primary(
    protocol_path: Path,
    pin: str,
    slot_id: str,
    review_commit: str,
    root: Path,
    model_root: Path,
    receipt: Path,
) -> session.SessionResult:
    """Verify before all session resources, recheck under shared lock, then capture."""
    plan = gate.verify_execution_plan(protocol_path, pin, slot_id, review_commit, root, model_root)
    context = _Context(plan, protocol_path, pin, slot_id, review_commit, root, model_root)
    return session._capture_session(model_root, receipt, context)
