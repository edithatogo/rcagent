"""Independent FAW07/D0 synthetic oracle; does not certify a demo implementation."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from tests.prospective_fixture_types import ObjectMap, mapping, sequence, text_value

ORACLE = Path(__file__).parent / "fixtures/faw07_independent/d0_oracle.json"
EXPECTED_ACCEPTS = 5
EXPECTED_REJECTS = 14


def _catalogue() -> ObjectMap:
    value: object = json.loads(ORACLE.read_text(encoding="utf-8"))
    return mapping(value)


def _sources(catalogue: ObjectMap) -> list[ObjectMap]:
    return [mapping(value) for value in sequence(catalogue["sources"])]


def _check_claim(claim: ObjectMap, sources: list[ObjectMap]) -> str | None:
    """Reference verifier independently derived from byte-level invariants.

    This is the test oracle, not an adapter to the production command.
    """
    required_text = ("source_id", "case_id", "digest", "unit", "span_text")
    if any(not isinstance(claim.get(key), str) for key in required_text):
        return "malformed_claim"
    revision = claim.get("revision")
    start = claim.get("start")
    end = claim.get("end")
    if (
        not isinstance(revision, int)
        or isinstance(revision, bool)
        or not isinstance(start, int)
        or isinstance(start, bool)
        or not isinstance(end, int)
        or isinstance(end, bool)
    ):
        return "malformed_claim"
    source_id = claim["source_id"]
    matches_id = [row for row in sources if row.get("id") == source_id]
    if not matches_id:
        return "unknown_source"
    matches = [row for row in matches_id if row.get("revision") == revision]
    if not matches:
        return "unknown_revision"
    if len(matches) != 1:
        return "duplicate_source_version"
    source = matches[0]
    if claim["case_id"] != source["case_id"]:
        return "case_mismatch"
    if source["state"] != "admitted":
        return "source_not_admitted"
    if claim["unit"] != "utf8-byte":
        return "invalid_coordinate_system"
    raw = text_value(source["text"]).encode("utf-8")
    actual_digest = hashlib.sha256(raw).hexdigest()
    if claim["digest"] != actual_digest or source["sha256"] != actual_digest:
        return "digest_mismatch"
    if start < 0 or start >= end or end > len(raw):
        return "invalid_span"
    try:
        selected = raw[start:end].decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return "invalid_span"
    if selected != claim["span_text"]:
        return "span_mismatch"
    return None


def _check_collection(rows: list[ObjectMap]) -> str | None:
    keys: list[tuple[str, int]] = []
    for row in rows:
        identifier = row.get("id")
        revision = row.get("revision")
        if not isinstance(identifier, str) or not isinstance(revision, int):
            return "malformed_source"
        key = (identifier, revision)
        if key in keys:
            return "duplicate_source_version"
        keys.append(key)
    return None


def test_independent_oracle_sources_are_byte_locked() -> None:
    catalogue = _catalogue()
    assert catalogue["schema_version"] == "faw07-independent-oracle-1.0"
    assert catalogue["data_class"] == "synthetic-only"
    assert catalogue["coordinate_system"] == "utf8-byte-half-open"
    assert catalogue["source_digest_algorithm"] == "sha256-raw-utf8"
    for source in _sources(catalogue):
        actual = hashlib.sha256(text_value(source["text"]).encode("utf-8")).hexdigest()
        assert source["sha256"] == actual


def test_independent_oracle_finite_adversarial_matrix() -> None:
    catalogue = _catalogue()
    sources = _sources(catalogue)
    cases = [mapping(row) for row in sequence(catalogue["cases"])]
    assert len({text_value(row["id"]) for row in cases}) == len(cases)
    assert sum(row["expected"] == "accept" for row in cases) == EXPECTED_ACCEPTS
    assert sum(row["expected"] == "reject" for row in cases) == EXPECTED_REJECTS
    for item in cases:
        actual = _check_claim(mapping(item["claim"]), sources)
        expected = item["expected"]
        if expected == "accept":
            assert actual is None, item["id"]
        else:
            assert expected == "reject", item["id"]
            assert actual == item["reason"], item["id"]


def test_independent_oracle_collection_duplicates_and_revisions() -> None:
    catalogue = _catalogue()
    sources = _sources(catalogue)
    checks = [mapping(row) for row in sequence(catalogue["collection_checks"])]
    assert len(checks) == 3
    for item in checks:
        indices = sequence(item["source_indices"])
        selected: list[ObjectMap] = []
        for index in indices:
            assert isinstance(index, int) and not isinstance(index, bool)
            selected.append(sources[index])
        actual = _check_collection(selected)
        if item["expected"] == "accept":
            assert actual is None, item["id"]
        else:
            assert actual == item["reason"], item["id"]


@pytest.mark.parametrize("repetitions", [2, 5])
def test_independent_oracle_repeat_and_source_order_invariance(repetitions: int) -> None:
    catalogue = _catalogue()
    sources = _sources(catalogue)
    cases = [mapping(row) for row in sequence(catalogue["cases"])]
    baseline = [_check_claim(mapping(row["claim"]), sources) for row in cases]
    for _ in range(repetitions):
        reordered = list(reversed(deepcopy(sources)))
        rerun = [_check_claim(mapping(row["claim"]), reordered) for row in cases]
        assert rerun == baseline
        assert _sources(_catalogue()) == sources


def test_independent_oracle_tampered_source_bytes_fail_closed() -> None:
    catalogue = _catalogue()
    sources = _sources(catalogue)
    accepted = mapping(sequence(catalogue["cases"])[0])
    claim = mapping(accepted["claim"])
    mutated = deepcopy(sources)
    mutated[0]["text"] = text_value(mutated[0]["text"]).replace("72", "99")
    assert _check_claim(claim, mutated) == "digest_mismatch"
    assert _check_claim(claim, sources) is None
