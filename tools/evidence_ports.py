"""Replaceable ports for evidence workflow integrations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from tools.json_shapes import JsonObject


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
    payload: JsonObject
    retryable: bool = False
    diagnostic: str | None = None


class EvidenceStore(Protocol):
    def put(self, operation: Operation, record: Mapping[str, object]) -> OperationResult: ...
    def get(self, operation: Operation, case_id: str) -> OperationResult: ...


class RetrievalPort(Protocol):
    def verify(
        self, operation: Operation, references: Sequence[Mapping[str, object]]
    ) -> OperationResult: ...


class CapabilityPort(Protocol):
    def capabilities(self) -> tuple[Capability, ...]: ...


class WorkflowPort(Protocol):
    def transition(
        self, operation: Operation, case_id: str, event: Mapping[str, object]
    ) -> OperationResult: ...


class ExportPort(Protocol):
    def export(
        self, operation: Operation, record: Mapping[str, object], profile: str
    ) -> OperationResult: ...
