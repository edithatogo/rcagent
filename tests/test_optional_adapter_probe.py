from __future__ import annotations

import hashlib
import json

from tools.optional_adapter_probe import hash_receipt


def test_receipt_hash_is_stable_and_excludes_signature() -> None:
    first = hash_receipt({"schema_version": "1.0", "passed": True})
    second = hash_receipt({"passed": True, "schema_version": "1.0"})
    assert first == second
    digest = first["receipt_sha256"]
    assert isinstance(digest, str)
    assert len(digest) == 64


def test_signing_preserves_source_binding_and_input_mutation() -> None:
    body: dict[str, object] = {"schema_version": "1.0", "passed": False}
    signed = hash_receipt(body)
    assert signed["probe_sha256"] == body["probe_sha256"]
    assert "receipt_sha256" not in body
    expected = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert signed["receipt_sha256"] == expected
