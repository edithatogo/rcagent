"""DM02 model-free contract red tests; all examples are invented synthetic data."""

from __future__ import annotations

import pytest

from tools import decision_model_contracts as dm


def test_dm02_wire_rejects_duplicate_keys_without_choosing_a_value() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        dm.strict_decode('{"message_type":"request","message_type":"result"}')


def test_dm02_unknown_registry_state_does_not_promote_capability() -> None:
    assert dm.registry_compatibility("unrecognised") is None
    assert dm.registry_compatibility("contract_tested") == "interface_contract"
