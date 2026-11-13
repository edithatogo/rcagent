"""Narrow immediate JSON container shapes without claiming domain validation.

These guards deliberately leave values as ``object``. A string-keyed object can
still contain malformed fields or non-JSON values; callers must check those at
their own schema and semantic boundaries.
"""

from __future__ import annotations

from typing import TypeAlias, TypeGuard, cast

JsonObject: TypeAlias = dict[str, object]


def is_object(value: object) -> TypeGuard[JsonObject]:
    """Check that a value is a dictionary whose current keys are all strings."""
    if not isinstance(value, dict):
        return False
    # A dictionary may contain arbitrary objects. Inspect its keys before
    # narrowing; do not infer anything about its nested values.
    return all(isinstance(key, str) for key in cast("dict[object, object]", value))


def is_array(value: object) -> TypeGuard[list[object]]:
    """Check the concrete list container, leaving every element unvalidated."""
    return isinstance(value, list)


def object_rows(value: object) -> list[JsonObject]:
    """Select object rows after a separate schema pass has diagnosed bad shapes."""
    if not is_array(value):
        return []
    return [item for item in value if is_object(item)]


def require_object(value: object, *, context: str) -> JsonObject:
    """Require the immediate object shape while preserving the original values."""
    if not is_object(value):
        raise ValueError(f"{context} must be a string-keyed object")
    return value
