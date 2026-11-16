"""Boundary regressions for the bounded FAW07/D0 inspection seam."""

from __future__ import annotations

import hashlib
import io
import json
from copy import deepcopy

import pytest

from tests.prospective_fixture_types import ObjectMap, mapping, sequence
from tools import faw07_d0_demo as demo
from tools.workbench import main


def _case(content: str = "Café 12 mg") -> ObjectMap:
    digest = "sha256:" + hashlib.sha256(content.encode()).hexdigest()
    return {
        "case_id": "case-a",
        "sources": [
            {
                "id": "source-a",
                "version": 1,
                "case_id": "case-a",
                "state": "present",
                "content": content,
                "fingerprint": digest,
            }
        ],
        "evidence": [
            {
                "id": "evidence-a",
                "case_id": "case-a",
                "source_id": "source-a",
                "source_version": 1,
                "source_sha256": digest,
                "coordinate_system": "utf8-byte",
                "start_byte": 6,
                "end_byte": 11,
                "text": "12 mg",
            }
        ],
    }


def _row(case: ObjectMap, name: str) -> ObjectMap:
    return mapping(sequence(case[name])[0])


def test_receipt_is_deterministic_and_inspectable() -> None:
    first = demo.generate_receipt()
    assert first == demo.generate_receipt()
    assert first["case_count"] == 5
    assert first["accepted"] == 2
    assert first["rejected"] == 3
    assert len(first["inputs"]) == len(first["cases"]) == first["case_count"]
    assert first["permitted_view"] == "synthetic-d0-evidence-only"
    assert first["input_schema_version"] == "faw07-d0-input-1.0"
    assert first["generator_version"] == "faw07-d0-generator-2.0"
    assert "expected_outcomes" not in first
    assert "oracle_mismatches" not in first
    assert all(case["spans"] for case in first["cases"] if case["status"] == "accepted")
    assert all(
        case["errors"] and not case["spans"]
        for case in first["cases"]
        if case["status"] == "rejected"
    )


def test_utf8_byte_offsets_and_source_hash() -> None:
    case = _case()
    before = deepcopy(case)
    result = demo.inspect_case(case)
    assert case == before
    assert result["status"] == "accepted"
    span = result["spans"][0]
    assert span["text"] == "12 mg"
    assert span["start_byte"] == 6
    assert span["case_id"] == "case-a"
    assert span["source_sha256"] == "sha256:" + hashlib.sha256("Café 12 mg".encode()).hexdigest()


@pytest.mark.parametrize(
    ("collection", "field", "value", "error"),
    [
        ("sources", "case_id", "foreign-case", "source case mismatch"),
        ("evidence", "case_id", "foreign-case", "evidence case mismatch"),
        ("sources", "fingerprint", "sha256:" + "0" * 64, "source fingerprint mismatch"),
        ("evidence", "source_sha256", "sha256:" + "0" * 64, "evidence source fingerprint mismatch"),
        ("evidence", "coordinate_system", "unicode-codepoint", "invalid coordinate system"),
        ("evidence", "source_id", "evidence-a", "unknown source identity"),
        ("evidence", "source_version", 2, "unknown source identity"),
        ("evidence", "start_byte", -1, "invalid byte span"),
        ("evidence", "end_byte", 100, "invalid byte span"),
        ("evidence", "end_byte", 6, "invalid byte span"),
        ("evidence", "start_byte", 4, "unaligned UTF-8"),
        ("evidence", "end_byte", 4, "invalid byte span"),
        ("evidence", "text", "12 ml", "source span mismatch"),
        ("sources", "state", "unreviewed", "invalid source state"),
    ],
)
def test_semantic_rejections_are_atomic(
    collection: str, field: str, value: object, error: str
) -> None:
    case = _case()
    _row(case, collection)[field] = value
    result = demo.inspect_case(case)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any(error in message for message in result["errors"])


@pytest.mark.parametrize("collection", ["sources", "evidence"])
def test_duplicates_reject_even_with_valid_prefix(collection: str) -> None:
    case = _case()
    rows = sequence(case[collection])
    rows.append(deepcopy(rows[0]))
    result = demo.inspect_case(case)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any("duplicate" in error for error in result["errors"])


def test_duplicate_identity_is_tracked_before_digest_validation() -> None:
    case = _case()
    sequence(case["sources"]).append(deepcopy(_row(case, "sources")))
    _row(case, "sources")["fingerprint"] = "sha256:" + "0" * 64
    errors = demo.inspect_case(case)["errors"]
    assert any("duplicate source identity" in error for error in errors)
    assert any("source fingerprint mismatch" in error for error in errors)


@pytest.mark.parametrize("state", ["unknown", "withdrawn"])
def test_unavailable_sources_preserve_unknown_bytes(state: str) -> None:
    case = _case()
    source = _row(case, "sources")
    source["state"] = state
    del source["content"]
    del source["fingerprint"]
    result = demo.inspect_case(case)
    assert result["status"] == "rejected"
    assert not result["spans"]
    observed = result["sources"][0]
    assert observed["state"] == state
    assert observed["sha256"] is None
    assert observed["bytes"] is None


@pytest.mark.parametrize("keep_fingerprint", [False, True])
def test_withdrawn_source_bytes_are_inspectable_not_admitted(keep_fingerprint: bool) -> None:
    case = _case()
    source = _row(case, "sources")
    source["state"] = "withdrawn"
    if not keep_fingerprint:
        del source["fingerprint"]
    result = demo.inspect_case(case)
    assert result["status"] == "rejected"
    assert not result["spans"]
    assert result["sources"][0]["state"] == "withdrawn"
    assert result["sources"][0]["bytes"] == 11
    assert any("withdrawn source" in error for error in result["errors"])


@pytest.mark.parametrize("value", [None, [], "case", 1, {1: "not-a-string-key"}])
def test_nonobject_case_has_documented_failure(value: object) -> None:
    with pytest.raises(ValueError, match="D0 case must be a string-keyed object"):
        demo.inspect_case(value)


@pytest.mark.parametrize("collection", ["sources", "evidence"])
@pytest.mark.parametrize("value", [None, [], {}, [None], [1]])
def test_malformed_or_empty_collections_fail(collection: str, value: object) -> None:
    case = _case()
    case[collection] = value
    with pytest.raises(ValueError, match=collection):
        demo.inspect_case(case)


@pytest.mark.parametrize(
    ("collection", "field"), [("sources", "version"), ("evidence", "source_version")]
)
@pytest.mark.parametrize("value", [True, False, 0, -1, "1", None])
def test_invalid_versions_are_not_coerced(collection: str, field: str, value: object) -> None:
    case = _case()
    _row(case, collection)[field] = value
    with pytest.raises(ValueError, match=f"{field} must be a positive integer"):
        demo.inspect_case(case)


@pytest.mark.parametrize("field", ["start_byte", "end_byte"])
@pytest.mark.parametrize("value", [True, False, "1", 1.0, None])
def test_malformed_offsets_are_not_coerced(field: str, value: object) -> None:
    case = _case()
    _row(case, "evidence")[field] = value
    with pytest.raises(ValueError, match=f"{field} must be an integer"):
        demo.inspect_case(case)


@pytest.mark.parametrize(
    ("collection", "field"), [("sources", "fingerprint"), ("evidence", "source_sha256")]
)
@pytest.mark.parametrize("value", ["sha256:" + "A" * 64, "0" * 64, "sha256:" + "0" * 63])
def test_malformed_digest_notation_fails(collection: str, field: str, value: str) -> None:
    case = _case()
    _row(case, collection)[field] = value
    with pytest.raises(ValueError, match="64 lowercase hex digits"):
        demo.inspect_case(case)


@pytest.mark.parametrize(
    ("collection", "field"),
    [
        ("sources", "id"),
        ("sources", "case_id"),
        ("sources", "state"),
        ("sources", "fingerprint"),
        ("evidence", "id"),
        ("evidence", "case_id"),
        ("evidence", "source_id"),
        ("evidence", "source_sha256"),
        ("evidence", "coordinate_system"),
        ("evidence", "text"),
    ],
)
def test_required_text_does_not_fall_back_to_optional_fields(collection: str, field: str) -> None:
    case = _case()
    row = _row(case, collection)
    row["optional_" + field] = row.pop(field)
    with pytest.raises(ValueError, match=f"{field} must be nonempty text"):
        demo.inspect_case(case)


@pytest.mark.parametrize(("collection", "limit"), [("sources", 32), ("evidence", 64)])
def test_exact_collection_limits(collection: str, limit: int) -> None:
    case = _case()
    rows = sequence(case[collection])
    for index in range(1, limit):
        row = deepcopy(rows[0])
        mapping(row)["id"] = f"extra-{index}"
        rows.append(row)
    assert demo.inspect_case(case)["status"] == "accepted"
    rows.append(deepcopy(rows[-1]))
    with pytest.raises(ValueError, match=f"{collection} exceeds {limit} entries"):
        demo.inspect_case(case)


@pytest.mark.parametrize("content", ["a" * 65_536, "é" * 32_768])
def test_exact_utf8_size_limit(content: str) -> None:
    case = _case(content)
    evidence = _row(case, "evidence")
    evidence.update(start_byte=0, end_byte=len(content[0].encode()), text=content[0])
    assert demo.inspect_case(case)["status"] == "accepted"
    _row(case, "sources")["content"] = content + "x"
    with pytest.raises(ValueError, match="exceeds 65536 UTF-8 bytes"):
        demo.inspect_case(case)


@pytest.mark.parametrize("content", [None, 12, "\ud800"])
def test_invalid_source_content_has_documented_failure(content: object) -> None:
    case = _case()
    _row(case, "sources")["content"] = content
    with pytest.raises(ValueError, match="source content must be"):
        demo.inspect_case(case)


def test_invalid_text_encoding_has_documented_failure() -> None:
    case = _case()
    _row(case, "evidence")["text"] = "\udfff"
    with pytest.raises(ValueError, match="text must be UTF-8 encodable"):
        demo.inspect_case(case)


def test_unknown_source_cannot_supply_bytes_or_a_fabricated_digest() -> None:
    case = _case()
    _row(case, "sources")["state"] = "unknown"
    with pytest.raises(ValueError, match="unknown source must omit content and fingerprint"):
        demo.inspect_case(case)


def test_withdrawn_digest_without_bytes_has_documented_failure() -> None:
    case = _case()
    source = _row(case, "sources")
    source["state"] = "withdrawn"
    del source["content"]
    with pytest.raises(ValueError, match="source fingerprint requires source content"):
        demo.inspect_case(case)


def test_empty_source_cannot_support_nonempty_evidence() -> None:
    case = _case("")
    result = demo.inspect_case(case)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert result["sources"][0]["bytes"] == 0


def test_cli_emits_actual_receipt(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["d0-demo"]) == 0
    parsed: object = json.loads(capsys.readouterr().out)
    assert parsed == demo.generate_receipt()


def test_module_write_failure_is_nonzero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    class ShortWriter(io.BytesIO):
        def write(self, buffer: object) -> int:
            return 0

    class Output:
        buffer = ShortWriter()

    with monkeypatch.context() as scoped:
        scoped.setattr(demo.sys, "stdout", Output())
        result = demo.main([])
    assert result == 1
    assert "incomplete D0 receipt write" in capsys.readouterr().err


def test_missing_lock_is_nonzero_before_receipt_publication(
    tmp_path: object, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(demo, "ROOT", tmp_path)
    assert demo.main([]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "D0 receipt failed" in captured.err
