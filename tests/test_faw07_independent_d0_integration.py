"""Black-box D0 verification against the independent synthetic fixture catalogue.

This file imports public D0 functions but never imports their fixture generator or
uses implementation-produced values as expected ground truth.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value
from tools.faw07_d0_demo import generate_receipt, inspect_case

ROOT = Path(__file__).parents[1]
ORACLE = ROOT / "tests/fixtures/faw07_independent/d0_oracle.json"


def _fixture() -> ObjectMap:
    value: object = json.loads(ORACLE.read_text(encoding="utf-8"))
    return mapping(value)


def _source_for(claim: ObjectMap, *, state: str | None = None) -> ObjectMap:
    candidates = [
        mapping(row)
        for row in sequence(_fixture()["sources"])
        if mapping(row)["id"] == claim["source_id"]
        and mapping(row)["revision"] == claim["revision"]
    ]
    if not candidates:
        return {
            "id": "source-a",
            "version": 1,
            "state": "present",
            "content": "[Patient A] synthetic evidence: pulse 72.\n",
        }
    source = candidates[0]
    return {
        "id": source["id"],
        "version": source["revision"],
        "state": state if state is not None else (
            "present" if source["state"] == "admitted" else source["state"]
        ),
        "content": source["text"],
        "case_id": source["case_id"],
        "sha256": source["sha256"],
    }


def _payload(claim: ObjectMap, *, source: ObjectMap | None = None) -> ObjectMap:
    selected = _source_for(claim) if source is None else source
    return {
        "case_id": claim["case_id"],
        "sources": [selected],
        "evidence": [
            {
                "id": "evidence-independent",
                "source_id": claim["source_id"],
                "source_version": claim["revision"],
                "start_byte": claim["start"],
                "end_byte": claim["end"],
                "text": claim["span_text"],
            }
        ],
    }


@pytest.mark.parametrize(
    "case_id",
    ["A01-exact", "A02-repeat", "A03-revision", "A04-multibyte", "A05-other-case"],
)
def test_independent_valid_byte_spans(case_id: str) -> None:
    item = next(
        mapping(row)
        for row in sequence(_fixture()["cases"])
        if mapping(row)["id"] == case_id
    )
    claim = mapping(item["claim"])
    result = inspect_case(_payload(claim))
    assert result["status"] == "accepted", case_id
    assert result["errors"] == [], case_id
    assert len(result["spans"]) == 1, case_id
    span = result["spans"][0]
    assert span["text"] == claim["span_text"]
    assert span["start_byte"] == claim["start"]
    assert span["end_byte"] == claim["end"]
    source = _source_for(claim)
    raw = text_value(source["content"]).encode("utf-8")
    assert span["source_sha256"] == "sha256:" + hashlib.sha256(raw).hexdigest()


@pytest.mark.parametrize(
    "case_id",
    [
        "R04-unknown-source",
        "R05-unknown-revision",
        "R07-out-of-bounds",
        "R08-reversed-span",
        "R09-wrong-span-text",
        "R10-utf8-split",
        "R11-withdrawn",
    ],
)
def test_independent_adversarial_rejections(case_id: str) -> None:
    item = next(
        mapping(row)
        for row in sequence(_fixture()["cases"])
        if mapping(row)["id"] == case_id
    )
    result = inspect_case(_payload(mapping(item["claim"])))
    assert result["status"] == "rejected", case_id
    assert result["spans"] == [], case_id
    assert result["errors"], case_id


@pytest.mark.parametrize("case_id", ["R06-negative-offset", "R13-malformed-offset"])
def test_independent_malformed_offsets_fail_without_acceptance(case_id: str) -> None:
    item = next(
        mapping(row)
        for row in sequence(_fixture()["cases"])
        if mapping(row)["id"] == case_id
    )
    with pytest.raises(ValueError, match="start_byte must be a nonnegative integer"):
        inspect_case(_payload(mapping(item["claim"])))


def test_independent_source_byte_tampering_invalidates_span() -> None:
    case = mapping(sequence(_fixture()["cases"])[0])
    claim = mapping(case["claim"])
    source = deepcopy(_source_for(claim))
    original = text_value(source["content"])
    source["content"] = original.replace("pulse 72.", "pulse 99.")
    result = inspect_case(_payload(claim, source=source))
    assert result["status"] == "rejected"
    assert any("source span mismatch" in error for error in result["errors"])


def test_independent_receipt_hash_and_repeatability() -> None:
    first = generate_receipt()
    assert first == generate_receipt()
    assert first == generate_receipt()
    assert first["accepted"] + first["rejected"] == first["case_count"]
    assert first["case_count"] >= 1
    assert first["dataset"] == "generated-synthetic-only"
    assert first["byte_coordinate_system"] == "utf8-zero-based-half-open"
    unsigned = {key: value for key, value in first.items() if key != "output_fingerprint"}
    canonical = json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    assert first["output_fingerprint"] == "sha256:" + hashlib.sha256(canonical).hexdigest()


def _run_demo(extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tools.workbench", "d0-demo", *(extra or [])],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )


def test_independent_actual_cli_runs_are_identical_and_inspectable() -> None:
    first = _run_demo()
    second = _run_demo()
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout
    parsed: object = json.loads(first.stdout)
    receipt = mapping(parsed)
    assert receipt["schema_version"] == "faw07-d0-receipt-1.0"
    assert receipt["task"] == "FAW07/D0"
    assert receipt["cases"]
    assert receipt["limitations"]


def test_independent_invalid_cli_argument_rejected() -> None:
    result = _run_demo(["unexpected"])
    assert result.returncode != 0
    assert '"schema_version":"faw07-d0-receipt-1.0"' not in result.stdout


def test_independent_cross_case_provenance_fails_closed() -> None:
    """A foreign-case source must not become admitted merely by being supplied.

    Intentionally strict: source.case_id is an independent attribution assertion.
    Do not accept or xfail this test simply because the current parser ignores it.
    """
    item = next(
        mapping(row)
        for row in sequence(_fixture()["cases"])
        if mapping(row)["id"] == "A05-other-case"
    )
    claim = mapping(item["claim"])
    payload = _payload(claim)
    payload["case_id"] = "synthetic-case-a"
    result = inspect_case(payload)
    assert result["status"] == "rejected"
