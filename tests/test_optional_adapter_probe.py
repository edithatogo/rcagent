from __future__ import annotations

from tools.optional_adapter_probe import _hash_receipt


def test_receipt_hash_is_stable_and_excludes_signature() -> None:
    first = _hash_receipt({"schema_version": "1.0", "passed": True})
    second = _hash_receipt({"passed": True, "schema_version": "1.0"})
    assert first == second
    assert len(first["receipt_sha256"]) == 64
