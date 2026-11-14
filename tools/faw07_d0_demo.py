"""FAW07/D0: deterministic, synthetic-only source and reference inspection.

No model, network, clinical interpretation or filesystem source acquisition.
The byte/offset contract uses UTF-8 byte positions, never character positions.
"""

from __future__ import annotations

from hashlib import sha256
from typing import Literal, TypedDict

from tools.evidence_core import canonical_bytes, fingerprint
from tools.json_shapes import is_array, is_object


class SourceObservation(TypedDict):
    source_id: str
    version: int
    state: Literal["present", "unknown"]
    sha256: str | None
    bytes: int | None


class SpanObservation(TypedDict):
    evidence_id: str
    source_id: str
    source_version: int
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
    task: Literal["FAW07/D0"]
    dataset: Literal["generated-synthetic-only"]
    command: str
    byte_coordinate_system: Literal["utf8-zero-based-half-open"]
    source_hash_algorithm: Literal["sha256"]
    case_count: int
    accepted: int
    rejected: int
    cases: list[CaseObservation]
    limitations: list[str]
    output_fingerprint: str


def _synthetic_cases() -> list[dict[str, object]]:
    """Generate finite examples separately from the independent oracle lane."""
    return [
        {
            "case_id": "d0-valid-span",
            "sources": [
                {"id": "src-a", "version": 1, "state": "present", "content": "Café: 12 mg."}
            ],
            "evidence": [
                {
                    "id": "ev-a",
                    "source_id": "src-a",
                    "source_version": 1,
                    "start_byte": 7,
                    "end_byte": 12,
                    "text": "12 mg",
                }
            ],
        },
        {
            "case_id": "d0-revised-source",
            "sources": [
                {"id": "src-b", "version": 1, "state": "present", "content": "Note: first"},
                {"id": "src-b", "version": 2, "state": "present", "content": "Note: revised"},
            ],
            "evidence": [
                {
                    "id": "ev-b",
                    "source_id": "src-b",
                    "source_version": 2,
                    "start_byte": 6,
                    "end_byte": 13,
                    "text": "revised",
                }
            ],
        },
        {
            "case_id": "d0-unknown-source",
            "sources": [{"id": "src-c", "version": 1, "state": "unknown"}],
            "evidence": [
                {
                    "id": "ev-c",
                    "source_id": "src-c",
                    "source_version": 1,
                    "start_byte": 0,
                    "end_byte": 4,
                    "text": "none",
                }
            ],
        },
        {
            "case_id": "d0-cross-version",
            "sources": [
                {"id": "src-d", "version": 1, "state": "present", "content": "old"},
                {"id": "src-d", "version": 2, "state": "present", "content": "new"},
            ],
            "evidence": [
                {
                    "id": "ev-d",
                    "source_id": "src-d",
                    "source_version": 1,
                    "start_byte": 0,
                    "end_byte": 3,
                    "text": "new",
                }
            ],
        },
        {
            "case_id": "d0-duplicate-evidence",
            "sources": [{"id": "src-e", "version": 1, "state": "present", "content": "seen"}],
            "evidence": [
                {"id": "ev-e", "source_id": "src-e", "source_version": 1,
                 "start_byte": 0, "end_byte": 4, "text": "seen"},
                {"id": "ev-e", "source_id": "src-e", "source_version": 1,
                 "start_byte": 0, "end_byte": 4, "text": "seen"},
            ],
        },
    ]


def _require_text(row: dict[str, object], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be nonempty text")
    return value


def _require_version(row: dict[str, object], key: str) -> int:
    value = row.get(key)
    if type(value) is not int or value < 1:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _require_offset(row: dict[str, object], key: str) -> int:
    value = row.get(key)
    if type(value) is not int or value < 0:
        raise ValueError(f"{key} must be a nonnegative integer")
    return value


def _rows(value: object, *, label: str) -> list[dict[str, object]]:
    if not is_array(value):
        raise ValueError(f"{label} must contain objects")
    rows: list[dict[str, object]] = []
    for item in value:
        if not is_object(item):
            raise ValueError(f"{label} must contain objects")
        rows.append(item)
    return rows


def inspect_case(case: dict[str, object]) -> CaseObservation:
    """Reject invalid links without asserting the underlying report is true."""
    case_id = _require_text(case, "case_id")
    sources: list[SourceObservation] = []
    spans: list[SpanObservation] = []
    errors: list[str] = []
    index: dict[tuple[str, int], bytes | None] = {}
    seen_evidence: set[str] = set()

    for row in _rows(case.get("sources"), label="sources"):
        sid = _require_text(row, "id")
        version = _require_version(row, "version")
        identity = (sid, version)
        if identity in index:
            errors.append(f"duplicate source identity: {sid}@{version}")
            continue
        state = row.get("state")
        if state == "unknown" and "content" not in row:
            index[identity] = None
            sources.append(
                {"source_id": sid, "version": version, "state": "unknown",
                 "sha256": None, "bytes": None}
            )
        elif state == "present" and isinstance(row.get("content"), str):
            content = row["content"]
            if not isinstance(content, str):
                raise ValueError("present source content must be text")
            raw = content.encode("utf-8")
            index[identity] = raw
            sources.append(
                {"source_id": sid, "version": version, "state": "present",
                 "sha256": f"sha256:{sha256(raw).hexdigest()}", "bytes": len(raw)}
            )
        else:
            errors.append(f"invalid source state/content: {sid}@{version}")

    for row in _rows(case.get("evidence"), label="evidence"):
        eid = _require_text(row, "id")
        sid = _require_text(row, "source_id")
        version = _require_version(row, "source_version")
        start = _require_offset(row, "start_byte")
        end = _require_offset(row, "end_byte")
        quoted = _require_text(row, "text")
        if eid in seen_evidence:
            errors.append(f"duplicate evidence identity: {eid}")
            continue
        seen_evidence.add(eid)
        identity = (sid, version)
        if identity not in index:
            errors.append(f"unknown source identity for {eid}: {sid}@{version}")
            continue
        raw = index[identity]
        if raw is None:
            errors.append(f"unknown source bytes for {eid}: {sid}@{version}")
            continue
        if end <= start or end > len(raw):
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
                "evidence_id": eid, "source_id": sid, "source_version": version,
                "start_byte": start, "end_byte": end, "text": decoded,
                "source_sha256": f"sha256:{sha256(raw).hexdigest()}",
                "verified": True,
            }
        )

    return {
        "case_id": case_id, "status": "rejected" if errors else "accepted",
        "sources": sources, "spans": spans, "errors": sorted(errors),
    }


def generate_receipt() -> D0Receipt:
    cases = [inspect_case(case) for case in _synthetic_cases()]
    base: D0Receipt = {
        "schema_version": "faw07-d0-receipt-1.0",
        "task": "FAW07/D0",
        "dataset": "generated-synthetic-only",
        "command": "python -m tools.workbench d0-demo",
        "byte_coordinate_system": "utf8-zero-based-half-open",
        "source_hash_algorithm": "sha256",
        "case_count": len(cases),
        "accepted": sum(case["status"] == "accepted" for case in cases),
        "rejected": sum(case["status"] == "rejected" for case in cases),
        "cases": cases,
        "limitations": [
            "synthetic byte-span and identity demonstration only",
            "not a clinical, semantic, chronology or model validation",
            "unknown source bytes are rejected rather than reconstructed",
            "no external acquisition, model invocation or network",
        ],
        "output_fingerprint": "",
    }
    base["output_fingerprint"] = fingerprint({k: v for k, v in base.items() if k != "output_fingerprint"})
    return base


def main(argv: list[str] | None = None) -> int:
    """Emit a canonical receipt; unsupported arguments fail closed."""
    if argv:
        raise ValueError("D0 accepts no external inputs")
    receipt = generate_receipt()
    print(canonical_bytes(receipt).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
