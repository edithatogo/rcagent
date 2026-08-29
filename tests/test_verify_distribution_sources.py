from __future__ import annotations

import pytest

from tools.verify_distribution_sources import SOURCES, verify_sources


def _valid(url: str) -> tuple[str, bytes]:
    source = next(item for item in SOURCES if item["url"] == url)
    return url, " ".join(str(marker) for marker in source["markers"]).encode()


def test_source_verifier_emits_hash_bound_receipt() -> None:
    value = verify_sources(fetch=_valid, retrieved_at="2026-08-29T00:00:00Z")
    assert value["retrieved_at"] == "2026-08-29T00:00:00Z"
    sources = value["sources"]
    assert isinstance(sources, list)
    assert len(sources) == len(SOURCES)
    assert all(isinstance(record, dict) and record["status"] == "verified" for record in sources)
    assert all(
        isinstance(record, dict)
        and isinstance(record["content_sha256"], str)
        and len(record["content_sha256"]) == 64
        for record in sources
    )


def test_source_verifier_fails_closed_on_network_or_marker_drift() -> None:
    with pytest.raises(ValueError, match="unavailable"):
        verify_sources(fetch=lambda _url: (_ for _ in ()).throw(OSError("offline")))
    with pytest.raises(ValueError, match="drifted"):
        verify_sources(fetch=lambda url: (url, b"unexpected"))
    with pytest.raises(ValueError, match="outside HTTPS"):
        verify_sources(fetch=lambda url: ("http://example.invalid", _valid(url)[1]))
