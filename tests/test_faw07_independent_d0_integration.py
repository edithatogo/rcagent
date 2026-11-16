"""Execute D0 against literal independent expectations and raw-byte calculations.

The historical oracle is unchanged. Translation preserves missing/invalid values
and available source revisions; expected results never come from the producer.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools.faw07_d0_demo import inspect_case

ROOT = Path(__file__).parents[1]
ORACLE = ROOT / "tests/fixtures/faw07_independent/d0_oracle.json"
EXPECTED_DEMO = {
    "d0-valid-span": "accepted",
    "d0-revised-source": "accepted",
    "d0-unknown-source": "rejected",
    "d0-cross-version": "rejected",
    "d0-duplicate-evidence": "rejected",
}
REJECTION_ERRORS = {
    "R01-forged-digest": "evidence source fingerprint mismatch",
    "R02-stale-revision-digest": "evidence source fingerprint mismatch",
    "R03-cross-case": "source case mismatch",
    "R04-unknown-source": "unknown source identity",
    "R05-unknown-revision": "unknown source identity",
    "R06-negative-offset": "invalid byte span",
    "R07-out-of-bounds": "invalid byte span",
    "R08-reversed-span": "invalid byte span",
    "R09-wrong-span-text": "source span mismatch",
    "R10-utf8-split": "unaligned UTF-8 byte span",
    "R11-withdrawn": "withdrawn source",
    "R14-wrong-coordinate-system": "invalid coordinate system",
}


def _fixture() -> ObjectMap:
    value: object = json.loads(ORACLE.read_text(encoding="utf-8"))
    return mapping(value)


def _item(identifier: str) -> ObjectMap:
    return next(
        mapping(row) for row in sequence(_fixture()["cases"]) if mapping(row)["id"] == identifier
    )


def _prefixed(value: object) -> object:
    return "sha256:" + value if isinstance(value, str) else value


def _source(source: ObjectMap) -> ObjectMap:
    result: ObjectMap = {}
    fields = {
        "id": "id",
        "revision": "version",
        "case_id": "case_id",
        "text": "content",
        "sha256": "fingerprint",
    }
    for old, new in fields.items():
        if old in source:
            result[new] = _prefixed(source[old]) if old == "sha256" else source[old]
    if "state" in source:
        result["state"] = "present" if source["state"] == "admitted" else source["state"]
    return result


def _claim(claim: ObjectMap, identifier: str) -> ObjectMap:
    result: ObjectMap = {"id": identifier}
    fields = {
        "case_id": "case_id",
        "source_id": "source_id",
        "revision": "source_version",
        "digest": "source_sha256",
        "unit": "coordinate_system",
        "start": "start_byte",
        "end": "end_byte",
        "span_text": "text",
    }
    for old, new in fields.items():
        if old in claim:
            result[new] = _prefixed(claim[old]) if old == "digest" else claim[old]
    return result


def _payload(item: ObjectMap) -> ObjectMap:
    claim = mapping(item["claim"])
    sources = [mapping(row) for row in sequence(_fixture()["sources"])]
    selected = [row for row in sources if row["id"] == claim.get("source_id")]
    # A literal known source keeps unknown-ID tests at the reference boundary.
    if not selected:
        selected = [sources[0]]
    return {
        "case_id": claim.get("case_id"),
        "sources": [_source(source) for source in selected],
        "evidence": [_claim(claim, text_value(item["id"]))],
    }


@pytest.mark.parametrize(
    "identifier", ["A01-exact", "A02-repeat", "A03-revision", "A04-multibyte", "A05-other-case"]
)
def test_independent_valid_byte_spans(identifier: str) -> None:
    item = _item(identifier)
    claim = mapping(item["claim"])
    result = inspect_case(_payload(item))
    assert result["status"] == "accepted"
    assert result["errors"] == []
    assert len(result["spans"]) == 1
    span = result["spans"][0]
    assert span["text"] == claim["span_text"]
    assert span["start_byte"] == claim["start"]
    assert span["end_byte"] == claim["end"]
    assert span["source_sha256"] == _prefixed(claim["digest"])
    assert span["case_id"] == claim["case_id"]


@pytest.mark.parametrize("identifier", sorted(REJECTION_ERRORS))
def test_independent_adversarial_rejections(identifier: str) -> None:
    result = inspect_case(_payload(_item(identifier)))
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any(REJECTION_ERRORS[identifier] in error for error in result["errors"])


@pytest.mark.parametrize(
    ("identifier", "error"),
    [
        ("R12-missing-hash", "source_sha256 must be nonempty text"),
        ("R13-malformed-offset", "start_byte must be an integer"),
    ],
)
def test_independent_malformed_claims_have_specific_failures(identifier: str, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        inspect_case(_payload(_item(identifier)))


@pytest.mark.parametrize(
    "identifier", ["C01-duplicate-id-revision", "C02-two-revisions", "C03-independent-sources"]
)
def test_independent_collection_checks_preserve_duplicates_revisions_and_cases(
    identifier: str,
) -> None:
    fixture = _fixture()
    check = next(
        mapping(row)
        for row in sequence(fixture["collection_checks"])
        if mapping(row)["id"] == identifier
    )
    originals = sequence(fixture["sources"])
    partitions: dict[str, list[ObjectMap]] = {}
    for index in sequence(check["source_indices"]):
        assert isinstance(index, int)
        source = mapping(originals[index])
        partitions.setdefault(text_value(source["case_id"]), []).append(source)
    assert partitions
    for case_id, sources in partitions.items():
        claims = [
            mapping(row)
            for row in sequence(fixture["cases"])
            if mapping(row)["expected"] == "accept"
            and mapping(mapping(row)["claim"])["case_id"] == case_id
            and any(
                source["id"] == mapping(mapping(row)["claim"])["source_id"]
                and source["revision"] == mapping(mapping(row)["claim"])["revision"]
                for source in sources
            )
        ]
        assert claims
        payload: ObjectMap = {
            "case_id": case_id,
            "sources": [_source(source) for source in sources],
            "evidence": [_claim(mapping(item["claim"]), text_value(item["id"])) for item in claims],
        }
        result = inspect_case(payload)
        if check["expected"] == "accept":
            assert result["status"] == "accepted"
            assert len(result["spans"]) == len(claims)
        else:
            assert result["status"] == "rejected"
            assert result["spans"] == []
            assert any("duplicate source identity" in error for error in result["errors"])


def test_independent_cross_case_provenance_fails_closed() -> None:
    """Retain the original strict regression: never relocate a foreign source."""
    payload = _payload(_item("A05-other-case"))
    payload["case_id"] = "synthetic-case-a"
    result = inspect_case(payload)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any("source case mismatch" in error for error in result["errors"])


def test_independent_source_byte_tampering_invalidates_span() -> None:
    payload = _payload(_item("A01-exact"))
    source = mapping(sequence(payload["sources"])[0])
    source["content"] = text_value(source["content"]).replace("pulse 72.", "pulse 99.")
    result = inspect_case(payload)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any("source fingerprint mismatch" in error for error in result["errors"])


def test_independent_forged_source_digest_is_rejected() -> None:
    payload = _payload(_item("A01-exact"))
    mapping(sequence(payload["sources"])[0])["fingerprint"] = "sha256:" + "0" * 64
    result = inspect_case(payload)
    assert result["status"] == "rejected"
    assert result["spans"] == []
    assert any("source fingerprint mismatch" in error for error in result["errors"])


def test_independent_source_and_evidence_order_preserves_identity_verdicts() -> None:
    payload = _payload(_item("A01-exact"))
    evidence = sequence(payload["evidence"])
    evidence.append(_claim(mapping(_item("A03-revision")["claim"]), "revision-two"))
    before = deepcopy(payload)
    first = inspect_case(payload)
    sequence(payload["sources"]).reverse()
    evidence.reverse()
    second = inspect_case(payload)
    assert first["status"] == second["status"] == "accepted"
    assert {row["evidence_id"]: row for row in first["spans"]} == {
        row["evidence_id"]: row for row in second["spans"]
    }
    assert {row["version"]: row for row in first["sources"]} == {
        row["version"]: row for row in second["sources"]
    }
    assert inspect_case(before) == first


@settings(max_examples=60, deadline=None)
@given(
    prefix=st.text(alphabet=st.characters(codec="utf-8"), max_size=24),
    quote=st.text(alphabet=st.characters(codec="utf-8"), min_size=1, max_size=24),
    suffix=st.text(alphabet=st.characters(codec="utf-8"), max_size=24),
)
def test_independent_utf8_span_property_and_one_byte_tamper(
    prefix: str, quote: str, suffix: str
) -> None:
    content = prefix + quote + suffix
    raw = content.encode("utf-8")
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    start = len(prefix.encode("utf-8"))
    end = start + len(quote.encode("utf-8"))
    payload: ObjectMap = {
        "case_id": "property-case",
        "sources": [
            {
                "id": "source",
                "case_id": "property-case",
                "version": 1,
                "state": "present",
                "content": content,
                "fingerprint": digest,
            }
        ],
        "evidence": [
            {
                "id": "span",
                "case_id": "property-case",
                "source_id": "source",
                "source_version": 1,
                "source_sha256": digest,
                "coordinate_system": "utf8-byte",
                "start_byte": start,
                "end_byte": end,
                "text": quote,
            }
        ],
    }
    first = inspect_case(payload)
    assert first["status"] == "accepted"
    assert first["spans"][0]["text"] == quote
    assert first == inspect_case(deepcopy(payload))
    mapping(sequence(payload["sources"])[0])["content"] = content + "!"
    changed = inspect_case(payload)
    assert changed["status"] == "rejected"
    assert changed["spans"] == []
    assert any("source fingerprint mismatch" in error for error in changed["errors"])


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def _digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _run_demo(
    *, module: bool = False, extra: list[str] | None = None
) -> subprocess.CompletedProcess[bytes]:
    args = ["tools.faw07_d0_demo"] if module else ["tools.workbench", "d0-demo"]
    return subprocess.run(
        [sys.executable, "-m", *args, *(extra or [])],
        cwd=ROOT,
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "ascii"},
        timeout=20,
        check=False,
    )


def test_independent_actual_cli_bytes_and_all_receipt_bindings() -> None:
    first = _run_demo()
    second = _run_demo()
    module = _run_demo(module=True)
    assert first.returncode == second.returncode == module.returncode == 0
    assert first.stderr == second.stderr == module.stderr == b""
    assert first.stdout == second.stdout == module.stdout
    assert first.stdout.endswith(b"\n")
    receipt = mapping(json.loads(first.stdout))
    assert first.stdout == _canonical(receipt) + b"\n"
    assert b"Caf\xc3\xa9" in first.stdout
    assert receipt["schema_version"] == "faw07-d0-receipt-1.0"
    assert receipt["input_schema_version"] == "faw07-d0-input-1.0"
    assert receipt["rule_version"] == "faw07-d0-rules-1.0"
    assert receipt["generator_version"] == "faw07-d0-generator-2.0"
    assert receipt["task"] == "FAW07/D0"
    assert receipt["dataset"] == "generated-synthetic-only"
    assert receipt["permitted_view"] == "synthetic-d0-evidence-only"
    assert receipt["command"] == "uv run --no-sync python -m tools.workbench d0-demo"
    assert receipt["source_hash_algorithm"] == "sha256"
    assert receipt["byte_coordinate_system"] == "utf8-zero-based-half-open"
    assert receipt["limitations"]
    inputs = sequence(receipt["inputs"])
    cases = sequence(receipt["cases"])
    assert receipt["input_fingerprint"] == _digest(_canonical(inputs))
    unsigned = {key: value for key, value in receipt.items() if key != "output_fingerprint"}
    assert receipt["output_fingerprint"] == _digest(_canonical(unsigned))
    assert receipt["dependency_lock_sha256"] == _digest((ROOT / "uv.lock").read_bytes())
    files = mapping(receipt["implementation_files"])
    assert set(files) == {
        "tools/faw07_d0_demo.py",
        "tools/workbench.py",
        "tools/evidence_core.py",
        "tools/json_shapes.py",
    }
    for filename, digest in files.items():
        assert digest == _digest((ROOT / filename).read_bytes())
    assert receipt["case_count"] == len(inputs) == len(cases) == 5
    assert receipt["accepted"] == sum(mapping(case)["status"] == "accepted" for case in cases) == 2
    assert receipt["rejected"] == sum(mapping(case)["status"] == "rejected" for case in cases) == 3
    input_map = {text_value(mapping(case)["case_id"]): mapping(case) for case in inputs}
    for case_value in cases:
        case = mapping(case_value)
        case_id = text_value(case["case_id"])
        assert case["status"] == EXPECTED_DEMO[case_id]
        declared_sources = sequence(input_map[case_id]["sources"])
        source_map = {
            (text_value(mapping(source)["id"]), mapping(source)["version"]): mapping(source)
            for source in declared_sources
        }
        for observed_value in sequence(case["sources"]):
            observed = mapping(observed_value)
            source = source_map[(text_value(observed["source_id"]), observed["version"])]
            assert observed["case_id"] == case_id == source["case_id"]
            if observed["state"] == "unknown":
                assert "content" not in source
                assert observed["sha256"] is None
                assert observed["bytes"] is None
            else:
                raw = text_value(source["content"]).encode("utf-8")
                assert observed["sha256"] == source["fingerprint"] == _digest(raw)
                assert observed["bytes"] == len(raw)
        spans = sequence(case["spans"])
        if case["status"] == "rejected":
            assert spans == []
            assert case["errors"]
        else:
            assert spans
            assert case["errors"] == []
            for span_value in spans:
                span = mapping(span_value)
                source = source_map[(text_value(span["source_id"]), span["source_version"])]
                raw = text_value(source["content"]).encode("utf-8")
                start, end = span["start_byte"], span["end_byte"]
                assert isinstance(start, int)
                assert isinstance(end, int)
                assert raw[start:end].decode("utf-8") == span["text"]
                assert span["source_sha256"] == _digest(raw)
                assert span["verified"] is True


@pytest.mark.parametrize("module", [False, True])
@pytest.mark.parametrize(
    "extra", [["unexpected"], ["--case-file", "private.json"], ["--output", "receipt.json"]]
)
def test_independent_invalid_cli_argument_rejected(module: bool, extra: list[str]) -> None:
    result = _run_demo(module=module, extra=extra)
    assert result.returncode != 0
    assert result.stdout == b""
