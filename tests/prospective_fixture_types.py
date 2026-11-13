"""Checked structural contracts for synthetic prospective-test fixtures.

These helpers narrow only the shape they check. They do not turn fabricated
fixture receipts into admitted observations or validate clinical semantics.
"""

from collections.abc import Callable
from functools import wraps
from pathlib import Path
from threading import Event
from typing import ParamSpec, Protocol, TypeAlias, TypedDict, cast

ObjectMap: TypeAlias = dict[str, object]
HttpArgs: TypeAlias = tuple[Path, str, str, bytes]
HttpCall: TypeAlias = tuple[Path, str, str, bytes, float]
ProcessArgs: TypeAlias = tuple[list[str], dict[str, str]]
ProcessCall: TypeAlias = tuple[list[str], dict[str, str], float]
VerifyArgs: TypeAlias = tuple[Path, str, str, str, Path, Path]
PrimaryArgs: TypeAlias = tuple[Path, str, str, str, Path, Path, Path]
StudyArgs: TypeAlias = tuple[Path, str, str, Path, Path, Path]


class HttpOptions(TypedDict):
    deadline: float


class ProcessOptions(TypedDict, total=False):
    timeout: float
    output_limit: int
    cleanup_grace: float
    cancel: Event | None
    stop_event: Event | None
    deadline: float | None


class Plan(Protocol):
    def value(self) -> object: ...


class HttpCapture(Protocol):
    def __call__(
        self, path: Path, method: str, route: str, body: bytes, *, deadline: float
    ) -> object: ...


class ProcessCapture(Protocol):
    def __call__(
        self,
        argv: list[str],
        environment: dict[str, str],
        *,
        timeout: float = 60,
        output_limit: int = 1048576,
        cleanup_grace: float = 1,
        cancel: Event | None = None,
        stop_event: Event | None = None,
        deadline: float | None = None,
    ) -> object: ...


class PrimaryCapture(Protocol):
    def __call__(
        self,
        protocol: Path,
        pinned: str,
        slot: str,
        review: str,
        repo: Path,
        model_root: Path,
        receipt: Path,
    ) -> ObjectMap: ...


SessionFixture: TypeAlias = tuple[Path, Path, list[HttpCall], list[ProcessCall], dict[str, str]]
PrimaryFixture: TypeAlias = tuple[
    Path, Path, list[HttpCall], list[ProcessCall], Plan, list[VerifyArgs]
]
GateFixture: TypeAlias = tuple[
    Path, Path, ObjectMap, ObjectMap, dict[str, bytes], list[ObjectMap], ObjectMap, ObjectMap
]
CaptureFixture: TypeAlias = tuple[StudyArgs, list[str], PrimaryCapture]


def mapping(value: object) -> ObjectMap:
    """Retain the exact mutable mapping after checking its container/key shape."""
    assert isinstance(value, dict), "fixture value must be a mapping"
    # isinstance establishes the container; keys are checked before the more
    # specific cast. Values intentionally remain object until separately checked.
    untyped = cast("dict[object, object]", value)
    assert all(isinstance(key, str) for key in untyped), "fixture keys must be strings"
    return cast("ObjectMap", value)


def sequence(value: object) -> list[object]:
    assert isinstance(value, list), "fixture value must be a list"
    # No element shape is claimed; preserve identity for adversarial mutations.
    return cast("list[object]", value)


def text_value(value: object) -> str:
    assert isinstance(value, str), "fixture value must be text"
    return value


P = ParamSpec("P")


def mapping_call(function: Callable[P, object]) -> Callable[P, ObjectMap]:
    """Keep a legacy callable's parameters while checking its returned mapping."""

    @wraps(function)
    def checked(*args: P.args, **kwargs: P.kwargs) -> ObjectMap:
        return mapping(function(*args, **kwargs))

    return checked
