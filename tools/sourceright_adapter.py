"""Thin, fail-closed subprocess adapter for the optional SourceRight CLI."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path

from tools.evidence_ports import Capability, Operation, OperationResult

Runner = Callable[..., subprocess.CompletedProcess[str]]
READ_ONLY_COMMANDS = {"bench", "report", "validate-csl", "citations", "provenance"}


class SourceRightAdapter:
    def __init__(self, executable: Path, runner: Runner = subprocess.run) -> None:
        self.executable = executable
        self._runner = runner

    def capabilities(self) -> tuple[Capability, ...]:
        available = self.executable.is_file() and os.access(self.executable, os.X_OK)
        return (Capability("citation-verification", "sourceright-0.1", available, ("fully_local", "air_gapped")),)

    def run_json(self, operation: Operation, arguments: Sequence[str]) -> OperationResult:
        if operation.privacy_mode not in {"fully_local", "air_gapped"}:
            return OperationResult("rejected", {}, diagnostic="unsupported privacy mode")
        if not arguments or arguments[0] not in READ_ONLY_COMMANDS or "--apply" in arguments:
            return OperationResult("rejected", {}, diagnostic="command is not in the read-only adapter profile")
        if not self.capabilities()[0].available:
            return OperationResult("unavailable", {}, retryable=False, diagnostic="SourceRight executable unavailable")
        try:
            completed = self._runner(
                [str(self.executable), *arguments],
                check=False,
                capture_output=True,
                text=True,
                timeout=operation.timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return OperationResult("timeout", {}, retryable=True, diagnostic="bounded SourceRight timeout")
        if completed.returncode != 0:
            return OperationResult("failed", {}, retryable=False, diagnostic=completed.stderr.strip()[:500])
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            return OperationResult("failed", {}, retryable=False, diagnostic="invalid SourceRight JSON")
        if not isinstance(payload, dict):
            return OperationResult("failed", {}, retryable=False, diagnostic="unexpected SourceRight payload")
        return OperationResult("succeeded", payload)
