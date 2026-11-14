"""Focused implementation tests for FAW07/D0; independent oracle fixtures are separate."""

from __future__ import annotations

import hashlib
import json

import pytest

from tools.faw07_d0_demo import generate_receipt, inspect_case
from tools.json_shapes import is_array, is_object
from tools.workbench import main


def _case(content: str = "Café 12 mg") -> dict[str, object]:
    return {
        "case_id": "case-a",
        "sources": [
            {
                "id": "source-a",
                "version": 1,
                "state": "present",
                "content": content,
                "fingerprint": "sha256:" + hashlib.sha256(content.encode()).hexdigest(),
            }
        ],
        "evidence": [
            {
                "id": "evidence-a",
                "source_id": "source-a",
                "source_version": 1,
                "start_byte": 6,
                "end_byte": 11,
                "text": "12 mg",
            }
        ],
    }


def test_receipt_is_deterministic_and_inspectable() -> None:
    first = generate_receipt()
    assert first == generate_receipt()
    assert first["case_count"] == 5
    assert first["accepted"] == 2
    assert first["rejected"] == 3
    assert first["accepted"] + first["rejected"] == first["case_count"]
    assert first["output_fingerprint"].startswith("sha256:")
    assert first["input_fingerprint"].startswith("sha256:")
    assert first["oracle_mismatches"] == []
    assert all(
        case["status"] == first["expected_outcomes"][case["case_id"]]
        for case in first["cases"]
    )
    assert all(case["sources"] for case in first["cases"])
    assert all(case["errors"] for case in first["cases"] if case["status"] == "rejected")


def test_utf8_byte_offsets_and_source_hash() -> None:
    result = inspect_case(_case())
    assert result["status"] == "accepted"
    span = result["spans"][0]
    assert span["text"] == "12 mg"
    assert span["start_byte"] == 6
    assert span["source_sha256"] == "sha256:" + hashlib.sha256("Café 12 mg".encode()).hexdigest()


def test_unaligned_utf8_and_forged_span_reject() -> None:
    bad = _case()
    evidence = bad["evidence"]
    assert is_array(evidence)
    row = evidence[0]
    assert is_object(row)
    row["start_byte"] = 4
    assert "unaligned UTF-8" in " ".join(inspect_case(bad)["errors"])
    row["start_byte"] = 6
    row["text"] = "12 ml"
    assert "mismatch" in " ".join(inspect_case(bad)["errors"])


def test_forged_source_fingerprint_is_rejected() -> None:
    bad = _case()
    sources = bad["sources"]
    assert is_array(sources)
    row = sources[0]
    assert is_object(row)
    row["fingerprint"] = "sha256:" + "0" * 64
    result = inspect_case(bad)
    assert result["status"] == "rejected"
    assert "source fingerprint mismatch" in " ".join(result["errors"])
    assert result["spans"] == []


def test_missing_version_unknown_bytes_and_duplicates_reject() -> None:
    bad = _case()
    rows = bad["evidence"]
    assert is_array(rows)
    row = rows[0]
    assert is_object(row)
    row["source_version"] = 2
    assert "unknown source identity" in " ".join(inspect_case(bad)["errors"])
    row["source_version"] = 1
    rows.append(dict(row))
    assert "duplicate evidence" in " ".join(inspect_case(bad)["errors"])
    sources = bad["sources"]
    assert is_array(sources)
    sources[0] = {"id": "source-a", "version": 1, "state": "unknown"}
    assert "unknown source bytes" in " ".join(inspect_case(bad)["errors"])


@pytest.mark.parametrize("value", [True, 0, -1, "1"])
def test_invalid_versions_are_not_coerced(value: object) -> None:
    bad = _case()
    rows = bad["sources"]
    assert is_array(rows)
    row = rows[0]
    assert is_object(row)
    row["version"] = value
    with pytest.raises(ValueError, match="positive integer"):
        inspect_case(bad)


def test_cli_emits_actual_receipt(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["d0-demo"]) == 0
    parsed = json.loads(capsys.readouterr().out)
    assert parsed == generate_receipt()
    assert parsed["cases"][0]["spans"][0]["verified"] is True
