"""Replaceable ports for evidence workflow integrations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Capability:
    name: str
    version: str
    available: bool
    privacy_modes: tuple[str, ...]


@dataclass(frozen=True)
class Operation:
    operation_id: str
    timeout_seconds: float
    idempotency_key: str
    privacy_mode: str


@dataclass(frozen=True)
class OperationResult:
    status: str
    payload: dict[str, Any]
    retryable: bool = False
    diagnostic: str | None = None


class EvidenceStore(Protocol):
    def put(self, operation: Operation, record: dict[str, Any]) -> OperationResult: ...
    def get(self, operation: Operation, case_id: str) -> OperationResult: ...


class RetrievalPort(Protocol):
    def verify(self, operation: Operation, references: list[dict[str, Any]]) -> OperationResult: ...


class CapabilityPort(Protocol):
    def capabilities(self) -> tuple[Capability, ...]: ...


class WorkflowPort(Protocol):
    def transition(self, operation: Operation, case_id: str, event: dict[str, Any]) -> OperationResult: ...


class ExportPort(Protocol):
    def export(self, operation: Operation, record: dict[str, Any], profile: str) -> OperationResult: ...
