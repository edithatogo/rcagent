"""Container guards must not be mistaken for recursive JSON/schema validation."""

from __future__ import annotations

import pytest

from tools.json_shapes import is_array, is_object, object_rows, require_object


@pytest.mark.parametrize("value", [None, [], (), "object", 1, {1: "wrong key"}])
def test_non_object_shapes_are_rejected(value: object) -> None:
    assert not is_object(value)
    with pytest.raises(ValueError, match="fixture must be a string-keyed object"):
        require_object(value, context="fixture")


def test_object_guard_preserves_identity_without_validating_nested_values() -> None:
    nested = object()
    value = {"nested": nested}
    assert is_object(value)
    assert require_object(value, context="fixture") is value
    assert value["nested"] is nested
    assert is_object({})


def test_array_guard_checks_container_without_narrowing_elements() -> None:
    assert is_array([object(), None, {1: "not a JSON object"}])
    assert not is_array((1, 2))
    assert not is_array("array")


def test_object_rows_preserve_original_objects_and_skip_invalid_shapes() -> None:
    valid = {"id": "fixture"}
    values: list[object] = [None, valid, {1: "invalid"}, []]
    rows = object_rows(values)
    assert rows == [valid]
    assert rows[0] is valid
    assert object_rows(None) == []
