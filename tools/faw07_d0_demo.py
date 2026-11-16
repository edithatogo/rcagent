"""Inspect a fixed synthetic corpus under the FAW07/D0 byte-provenance contract.

The public Python seam admits bounded raw objects; the CLI accepts no inputs.
A verified span proves byte identity, not the truth of its source account.
"""

from __future__ import annotations

import argparse
import re
import sys
from hashlib import sha256
from pathlib import Path
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.json_shapes import JsonObject, is_array, require_object

ROOT = Path(__file__).parents[1]
MAX_SOURCES = 32
MAX_EVIDENCE = 64
MAX_SOURCE_BYTES = 65_536
IMPLEMENTATION_FILES = (
    "tools/faw07_d0_demo.py",
    "tools/workbench.py",
    "tools/evidence_core.py",
    "tools/json_shapes.py",
)
SourceState = Literal["present", "unknown", "withdrawn"]
SourceIdentity = tuple[str, str, int]
SourceBytes = tuple[SourceState, bytes | None, str | None]


class SourceObservation(TypedDict):
    case_id: str
    source_id: str
    version: int
    state: SourceState
    sha256: str | None
    bytes: int | None


class SpanObservation(TypedDict):
    case_id: str
    evidence_id: str
    source_id: str
    source_version: int
    coordinate_system: Literal["utf8-byte"]
    start_byte: int
    end_byte: int
    text: str
    source_sha256: str
    verified: Literal[True]


class CaseObservation(TypedDict):
    case_id: str
    status: Literal["accepted", "rejected"]
    sources: list[SourceObservation]
    spans: list[SpanObservation]
    errors: list[str]


class D0Receipt(TypedDict):
    schema_version: Literal["faw07-d0-receipt-1.0"]
    input_schema_version: Literal["faw07-d0-input-1.0"]
    rule_version: Literal["faw07-d0-rules-1.0"]
    generator_version: Literal["faw07-d0-generator-2.0"]
    task: Literal["FAW07/D0"]
    dataset: Literal["generated-synthetic-only"]
    command: str
    byte_coordinate_system: Literal["utf8-zero-based-half-open"]
    source_hash_algorithm: Literal["sha256"]
    inputs: list[JsonObject]
    input_fingerprint: str
    permitted_view: Literal["synthetic-d0-evidence-only"]
    privacy_mode: Literal["fully_local"]
    dependency_lock_sha256: str
    implementation_files: dict[str, str]
    case_count: int
    accepted: int
    rejected: int
    cases: list[CaseObservation]
    limitations: list[str]
    output_fingerprint: str


def _byte_digest(raw: bytes) -> str:
    return "sha256:" + sha256(raw).hexdigest()


def _generated_source(case_id: str, source_id: str, version: int, content: str) -> JsonObject:
    return {
        "id": source_id,
        "version": version,
        "case_id": case_id,
        "state": "present",
        "content": content,
        "fingerprint": _byte_digest(content.encode("utf-8")),
    }


def _generated_evidence(
    case_id: str,
    evidence_id: str,
    source_id: str,
    version: int,
    content: str,
    start: int,
    end: int,
    text: str,
) -> JsonObject:
    return {
        "id": evidence_id,
        "case_id": case_id,
        "source_id": source_id,
        "source_version": version,
        "source_sha256": _byte_digest(content.encode("utf-8")),
        "coordinate_system": "utf8-byte",
        "start_byte": start,
        "end_byte": end,
        "text": text,
    }


def _synthetic_cases() -> list[JsonObject]:
    """Versioned inputs without expected labels; the independent lane owns those."""
    valid = "d0-valid-span"
    revised = "d0-revised-source"
    unknown = "d0-unknown-source"
    stale = "d0-cross-version"
    duplicate = "d0-duplicate-evidence"
    unknown_claim = _generated_evidence(unknown, "ev-c", "src-c", 1, "", 0, 4, "none")
    # A declared claim digest does not supply unknown source bytes.
    unknown_claim["source_sha256"] = "sha256:" + "0" * 64
    repeated = _generated_evidence(duplicate, "ev-e", "src-e", 1, "seen", 0, 4, "seen")
    return [
        {
            "case_id": valid,
            "sources": [_generated_source(valid, "src-a", 1, "Café: 12 mg.")],
            "evidence": [
                _generated_evidence(valid, "ev-a", "src-a", 1, "Café: 12 mg.", 7, 12, "12 mg")
            ],
        },
        {
            "case_id": revised,
            "sources": [
                _generated_source(revised, "src-b", 1, "Note: first"),
                _generated_source(revised, "src-b", 2, "Note: revised"),
            ],
            "evidence": [
                _generated_evidence(revised, "ev-b", "src-b", 2, "Note: revised", 6, 13, "revised")
            ],
        },
        {
            "case_id": unknown,
            "sources": [{"id": "src-c", "version": 1, "case_id": unknown, "state": "unknown"}],
            "evidence": [unknown_claim],
        },
        {
            "case_id": stale,
            "sources": [
                _generated_source(stale, "src-d", 1, "old"),
                _generated_source(stale, "src-d", 2, "new"),
            ],
            "evidence": [_generated_evidence(stale, "ev-d", "src-d", 1, "old", 0, 3, "new")],
        },
        {
            "case_id": duplicate,
            "sources": [_generated_source(duplicate, "src-e", 1, "seen")],
            "evidence": [repeated, dict(repeated)],
        },
    ]


def _require_text(row: JsonObject, key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be nonempty text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{key} must be UTF-8 encodable") from exc
    return value


def _require_version(row: JsonObject, key: str) -> int:
    value = row.get(key)
    if type(value) is not int or value < 1:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _require_offset(row: JsonObject, key: str) -> int:
    value = row.get(key)
    if type(value) is not int:
        raise ValueError(f"{key} must be an integer")
    return value


def _require_digest(row: JsonObject, key: str) -> str:
    value = _require_text(row, key)
    if re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
        raise ValueError(f"{key} must be sha256: followed by 64 lowercase hex digits")
    return value


def _source_bytes(row: JsonObject) -> bytes:
    content = row.get("content")
    if not isinstance(content, str):
        raise ValueError("source content must be text")
    if len(content) > MAX_SOURCE_BYTES:
        raise ValueError("source content exceeds 65536 UTF-8 bytes")
    try:
        raw = content.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("source content must be UTF-8 encodable") from exc
    if len(raw) > MAX_SOURCE_BYTES:
        raise ValueError("source content exceeds 65536 UTF-8 bytes")
    return raw


def _rows(value: object, *, label: str, limit: int) -> list[JsonObject]:
    if not is_array(value) or not value:
        raise ValueError(f"{label} must be a nonempty array of objects")
    if len(value) > limit:
        raise ValueError(f"{label} exceeds {limit} entries")
    return [require_object(item, context=f"{label} entry") for item in value]


def _inspect_sources(
    rows: list[JsonObject], case_id: str
) -> tuple[list[SourceObservation], dict[SourceIdentity, SourceBytes], list[str]]:
    observations: list[SourceObservation] = []
    index: dict[SourceIdentity, SourceBytes] = {}
    seen: set[SourceIdentity] = set()
    errors: list[str] = []
    for row in rows:
        sid = _require_text(row, "id")
        version = _require_version(row, "version")
        source_case = _require_text(row, "case_id")
        state = _require_text(row, "state")
        identity = (source_case, sid, version)
        if identity in seen:
            errors.append(f"duplicate source identity: {sid}@{version}")
        seen.add(identity)
        if source_case != case_id:
            errors.append(f"source case mismatch: {sid}@{version}")
        if state not in ("present", "unknown", "withdrawn"):
            errors.append(f"invalid source state: {sid}@{version}")
            continue
        raw: bytes | None = None
        digest: str | None = None
        if state == "unknown":
            if "content" in row or "fingerprint" in row:
                raise ValueError("unknown source must omit content and fingerprint")
        elif state == "present" or "content" in row:
            raw = _source_bytes(row)
            digest = _byte_digest(raw)
            if (state == "present" or "fingerprint" in row) and (
                _require_digest(row, "fingerprint") != digest
            ):
                errors.append(f"source fingerprint mismatch: {sid}@{version}")
        elif "fingerprint" in row:
            raise ValueError("source fingerprint requires source content")
        observation: SourceObservation = {
            "case_id": source_case,
            "source_id": sid,
            "version": version,
            "state": state,
            "sha256": digest,
            "bytes": len(raw) if raw is not None else None,
        }
        observations.append(observation)
        index[identity] = (state, raw, digest)
    return observations, index, errors


def inspect_case(case: object) -> CaseObservation:
    """Inspect bounded raw input without mutating it.

    Malformed shapes, missing/wrong field types, malformed digests, encoding
    errors and exceeded limits raise ValueError. Well-shaped invalid evidence
    returns stable rejection errors, with no admitted spans for the whole case.
    """
    record = require_object(case, context="D0 case")
    case_id = _require_text(record, "case_id")
    source_rows = _rows(record.get("sources"), label="sources", limit=MAX_SOURCES)
    evidence_rows = _rows(record.get("evidence"), label="evidence", limit=MAX_EVIDENCE)
    sources, index, errors = _inspect_sources(source_rows, case_id)
    spans: list[SpanObservation] = []
    seen_evidence: set[tuple[str, str]] = set()
    for row in evidence_rows:
        eid = _require_text(row, "id")
        evidence_case = _require_text(row, "case_id")
        sid = _require_text(row, "source_id")
        version = _require_version(row, "source_version")
        claimed_digest = _require_digest(row, "source_sha256")
        coordinates = _require_text(row, "coordinate_system")
        start = _require_offset(row, "start_byte")
        end = _require_offset(row, "end_byte")
        quoted = _require_text(row, "text")
        evidence_identity = (evidence_case, eid)
        if evidence_identity in seen_evidence:
            errors.append(f"duplicate evidence identity: {eid}")
        seen_evidence.add(evidence_identity)
        if evidence_case != case_id:
            errors.append(f"evidence case mismatch: {eid}")
        if coordinates != "utf8-byte":
            errors.append(f"invalid coordinate system for {eid}")
        identity = (case_id, sid, version)
        if identity not in index:
            errors.append(f"unknown source identity for {eid}: {sid}@{version}")
            continue
        state, raw, digest = index[identity]
        if state == "withdrawn":
            errors.append(f"withdrawn source for {eid}: {sid}@{version}")
            continue
        if state == "unknown" or raw is None or digest is None:
            errors.append(f"unknown source bytes for {eid}: {sid}@{version}")
            continue
        if claimed_digest != digest:
            errors.append(f"evidence source fingerprint mismatch for {eid}: {sid}@{version}")
            continue
        if not 0 <= start < end <= len(raw):
            errors.append(f"invalid byte span for {eid}")
            continue
        try:
            decoded = raw[start:end].decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"unaligned UTF-8 byte span for {eid}")
            continue
        if decoded != quoted:
            errors.append(f"source span mismatch for {eid}")
            continue
        spans.append(
            {
                "case_id": case_id,
                "evidence_id": eid,
                "source_id": sid,
                "source_version": version,
                "coordinate_system": "utf8-byte",
                "start_byte": start,
                "end_byte": end,
                "text": decoded,
                "source_sha256": digest,
                "verified": True,
            }
        )
    return {
        "case_id": case_id,
        "status": "rejected" if errors else "accepted",
        "sources": sources,
        "spans": [] if errors else spans,
        "errors": sorted(errors),
    }


def generate_receipt() -> D0Receipt:
    """Bind deterministic observations to inspectable inputs and current code bytes."""
    inputs = _synthetic_cases()
    cases = [inspect_case(case) for case in inputs]
    base: D0Receipt = {
        "schema_version": "faw07-d0-receipt-1.0",
        "input_schema_version": "faw07-d0-input-1.0",
        "rule_version": "faw07-d0-rules-1.0",
        "generator_version": "faw07-d0-generator-2.0",
        "task": "FAW07/D0",
        "dataset": "generated-synthetic-only",
        "command": "uv run --no-sync python -m tools.workbench d0-demo",
        "byte_coordinate_system": "utf8-zero-based-half-open",
        "source_hash_algorithm": "sha256",
        "inputs": inputs,
        "input_fingerprint": fingerprint(inputs),
        "permitted_view": "synthetic-d0-evidence-only",
        "privacy_mode": "fully_local",
        "dependency_lock_sha256": _byte_digest((ROOT / "uv.lock").read_bytes()),
        "implementation_files": {
            path: _byte_digest((ROOT / path).read_bytes()) for path in IMPLEMENTATION_FILES
        },
        "case_count": len(cases),
        "accepted": sum(case["status"] == "accepted" for case in cases),
        "rejected": sum(case["status"] == "rejected" for case in cases),
        "cases": cases,
        "limitations": [
            "synthetic source identity and byte-span inspection only; hashes do not prove truth",
            "no accepted finding, chronology, clinical or model validity is established",
            "unknown and withdrawn sources cannot support an admitted span",
            "equal text does not establish independent corroboration",
            "no legal protection or public-disclosure authority is established",
            "no external source acquisition, model invocation or network",
        ],
        "output_fingerprint": "",
    }
    base["output_fingerprint"] = fingerprint(
        {key: value for key, value in base.items() if key != "output_fingerprint"}
    )
    return base


def main(argv: list[str] | None = None) -> int:
    """Emit UTF-8 bytes plus one LF; unsupported input and write failures are nonzero."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        payload = canonical_bytes(generate_receipt()) + b"\n"
        written = sys.stdout.buffer.write(payload)
        if written != len(payload):
            raise OSError("incomplete D0 receipt write")
        sys.stdout.buffer.flush()
    except (OSError, ValueError) as exc:
        print(f"D0 receipt failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
