"""Sole guarded primary entry; completed observations remain unadmitted."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path

from tools import prospective_execution_gate as gate
from tools import prospective_runner_contract as runner
from tools import prospective_server_session as session


@dataclass(frozen=True)
class _Context:
    plan: gate._Plan
    protocol_path: Path
    pin: str
    slot_id: str
    review_commit: str
    root: Path
    model_root: Path

    def verify(self) -> None:
        current = gate._verify(
            self.protocol_path,
            self.pin,
            self.slot_id,
            self.review_commit,
            self.root,
            self.model_root,
        )
        if current.payload != self.plan.payload:
            raise ValueError("primary_gate_changed")

    def finish(self, result: dict) -> None:
        result["primary_gate"] = self.plan.value()["evidence"]
        try:
            self.verify()
            if result["error"] == "none":
                value = self.plan.value()
                result["candidate"] = runner.normalize_candidate(
                    value["request"],
                    base64.b64decode(result["completion"]["body_base64"], validate=True),
                    slot_id=self.slot_id,
                    expected_slot_id=self.slot_id,
                    expected_model=value["admission"]["model_id"],
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
) -> dict:
    """Verify before all session resources, recheck under shared lock, then capture."""
    plan = gate._verify(protocol_path, pin, slot_id, review_commit, root, model_root)
    context = _Context(plan, protocol_path, pin, slot_id, review_commit, root, model_root)
    return session._capture_session(model_root, receipt, context)
