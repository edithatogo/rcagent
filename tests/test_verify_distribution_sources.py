from __future__ import annotations

import pytest

from tools.verify_distribution_sources import SOURCES, verify_sources


def _valid(url: str) -> tuple[str, bytes]:
    source = next(item for item in SOURCES if item["url"] == url)
    return url, " ".join(str(marker) for marker in source["markers"]).encode()


def test_source_verifier_emits_hash_bound_receipt() -> None:
    value = verify_sources(fetch=_valid, retrieved_at="2026-08-29T00:00:00Z")
    assert value["retrieved_at"] == "2026-08-29T00:00:00Z"
    assert len(value["sources"]) == len(SOURCES)
    assert all(record["status"] == "verified" for record in value["sources"])
    assert all(len(record["content_sha256"]) == 64 for record in value["sources"])


def test_source_verifier_fails_closed_on_network_or_marker_drift() -> None:
    with pytest.raises(ValueError, match="unavailable"):
        verify_sources(fetch=lambda _url: (_ for _ in ()).throw(OSError("offline")))
    with pytest.raises(ValueError, match="drifted"):
        verify_sources(fetch=lambda url: (url, b"unexpected"))
