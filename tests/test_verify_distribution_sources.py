from __future__ import annotations

import sys
from pathlib import Path
from typing import Self
from unittest.mock import Mock

import pytest

from tests.prospective_fixture_types import mapping, sequence
from tools import verify_distribution_sources as source_module
from tools.verify_distribution_sources import SOURCES, verify_sources


def _valid(url: str) -> tuple[str, bytes]:
    source = next(item for item in SOURCES if item["url"] == url)
    return url, " ".join(str(marker) for marker in source["markers"]).encode()


def test_source_verifier_emits_hash_bound_receipt() -> None:
    value = verify_sources(fetch=_valid, retrieved_at="2026-08-29T00:00:00Z")
    assert value["retrieved_at"] == "2026-08-29T00:00:00Z"
    sources = [mapping(row) for row in sequence(value["sources"])]
    assert len(sources) == len(SOURCES)
    assert all(record["status"] == "verified" for record in sources)
    assert all(
        isinstance(record["content_sha256"], str) and len(record["content_sha256"]) == 64
        for record in sources
    )


def test_source_verifier_fails_closed_on_network_or_marker_drift() -> None:
    with pytest.raises(ValueError, match="unavailable"):
        verify_sources(fetch=Mock(side_effect=OSError("offline")))
    with pytest.raises(ValueError, match="drifted"):
        verify_sources(fetch=lambda url: (url, b"unexpected"))
    with pytest.raises(ValueError, match="outside HTTPS"):
        verify_sources(fetch=lambda url: ("http://example.invalid", _valid(url)[1]))


def test_source_verifier_cli_writes_receipt_and_reports_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "receipt.json"
    monkeypatch.setattr(source_module, "verify_sources", lambda: {"schema_version": "1.0"})
    monkeypatch.setattr(sys, "argv", ["verify-sources", "--output", str(output)])
    assert source_module.main() == 0
    assert '"schema_version": "1.0"' in output.read_text()

    def _fail() -> dict[str, object]:
        raise ValueError("source drift")

    monkeypatch.setattr(source_module, "verify_sources", _fail)
    monkeypatch.setattr(sys, "argv", ["verify-sources", "--output", str(tmp_path / "bad")])
    with pytest.raises(SystemExit) as error:
        source_module.main()
    assert error.value.code == 2
    assert "source drift" in capsys.readouterr().err


def test_default_fetcher_returns_final_url_and_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    class Response:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def geturl(self) -> str:
            return "https://example.invalid/final"

        def read(self) -> bytes:
            return b"payload"

    monkeypatch.setattr(source_module.urllib.request, "urlopen", Mock(return_value=Response()))
    assert source_module.fetch_source("https://example.invalid") == (
        "https://example.invalid/final",
        b"payload",
    )
