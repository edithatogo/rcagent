"""Deterministic, compartment-bound retrieval contracts and SQLite FTS baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import tempfile
import time
import tracemalloc
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Literal, NotRequired, Protocol, Self, TypedDict, TypeGuard, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

ROOT = Path(__file__).parents[1]
CORPUS = ROOT / "evaluation/retrieval/synthetic-public-corpus.json"
PROFILES = ROOT / "evaluation/retrieval/profiles.json"
SCHEMA = ROOT / "conductor/schemas/retrieval-corpus.schema.json"
INSTRUCTION_MARKERS = ("ignore previous instructions", "system prompt", "disclose private")
PROFILE_REVISION = "lexical-sqlite-fts5 contract 1.1"
MANDATORY_UNSUPPORTED = [
    "typo correction",
    "vector retrieval",
    "hybrid retrieval",
    "model reranking",
    "external literature provider",
    "cross-compartment retrieval",
    "operational thresholds",
]


class _SchemaValidator(Protocol):
    """Non-deprecated object-validation API; the stub's other overload is untyped."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


class RetrievalUnit(TypedDict):
    id: str
    source: str
    authority: str
    jurisdiction: str
    rights: str
    rights_basis: JsonObject
    version: str
    timestamp: str
    location: JsonObject
    transformation: list[str]
    compartment: str
    status: str
    content: str
    checksum: str
    retention: str


class RetrievalManifest(TypedDict):
    schema_version: str
    corpus_id: str
    compartment: str
    units: list[RetrievalUnit]


class RetrievalHit(TypedDict):
    unit_id: str
    source: str
    authority: str
    jurisdiction: str
    rights: str
    rights_basis: JsonObject
    version: str
    timestamp: str
    location: JsonObject
    transformation: list[str]
    status: str
    checksum: str
    retention: str
    safety_flags: list[str]
    score: float


class _RetrievalFields(TypedDict):
    schema_version: Literal["1.0"]
    profile: Literal["lexical-sqlite-fts5"]
    query: str
    query_mode: str
    filters: dict[str, str]
    compartment: str
    limit: int
    results: list[RetrievalHit]
    network: Literal["disabled"]
    telemetry: Literal["none"]


class RetrievalReceipt(_RetrievalFields):
    receipt_sha256: str


class LifecycleEvent(TypedDict):
    sequence: int
    action: str
    unit_id: str | None
    compartment: str
    detail_sha256: str


class _LifecycleFields(TypedDict):
    schema_version: Literal["1.0"]
    compartment: str
    events: list[LifecycleEvent]


class LifecycleReceipt(_LifecycleFields):
    receipt_sha256: str


class GroundingResult(TypedDict):
    claims: list[JsonObject]
    conflicts: list[str]
    poisoned_content: list[str]
    abstained: bool
    grounding: Literal["claim_link_only"]
    clinical_interpretation: Literal[False]
    human_review_required: Literal[True]


class FusionResult(TypedDict):
    unit_id: str
    fusion_score: float


class DriftImpact(TypedDict):
    changed_units: list[str]
    affected_receipts: list[str]
    requires_rebuild: bool


class AssuranceCase(TypedDict):
    hits: int
    passed: bool


class AssuranceSuite(TypedDict):
    passed: bool
    mode: NotRequired[str]
    status: NotRequired[str]


class ProfileComparison(TypedDict):
    id: str
    status: str
    revision: str


class ResearchObservations(TypedDict):
    elapsed_ms: float
    allocation_peak_bytes: int
    integrity_scope: str


class _AssuranceFields(TypedDict):
    schema_version: Literal["1.0"]
    scope: Literal["deterministic_synthetic_ci_contract"]
    manifest_sha256: str
    profile_revision: str
    results: dict[str, AssuranceCase]
    suites: dict[str, AssuranceSuite]
    profile_comparison: list[ProfileComparison]
    research_observations: ResearchObservations
    network: Literal["disabled"]
    private_data: Literal[False]
    unsupported: list[str]


class AssuranceReceipt(_AssuranceFields):
    observation_sha256: str
    receipt_sha256: str


def _text(value: object, *, context: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{context}: expected text")
    return value


def _texts(value: object, *, context: str) -> list[str]:
    if not is_array(value) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{context}: expected an array of text")
    return [item for item in value if isinstance(item, str)]


def _is_unit(value: object) -> TypeGuard[RetrievalUnit]:
    """Narrow fields used by the index after separate domain validation."""
    if not is_object(value):
        return False
    text_fields = (
        "id",
        "source",
        "authority",
        "jurisdiction",
        "rights",
        "version",
        "timestamp",
        "compartment",
        "status",
        "content",
        "checksum",
        "retention",
    )
    transformation = value.get("transformation")
    return (
        all(isinstance(value.get(field), str) for field in text_fields)
        and is_object(value.get("rights_basis"))
        and is_object(value.get("location"))
        and is_array(transformation)
        and all(isinstance(item, str) for item in transformation)
    )


def _checked_units(value: object) -> list[RetrievalUnit]:
    if not is_array(value):
        raise ValueError("units must be an array")
    units: list[RetrievalUnit] = []
    for unit in value:
        if not _is_unit(unit):
            raise ValueError("invalid validated retrieval unit shape")
        units.append(unit)
    return units


def _row(value: object) -> sqlite3.Row:
    if not isinstance(value, sqlite3.Row):
        raise ValueError("index query did not return a SQLite row")
    return value


def _row_text(row: sqlite3.Row, field: str) -> str:
    return _text(row[field], context=f"index {field}")


def _row_json(row: sqlite3.Row, field: str) -> object:
    return json.loads(_row_text(row, field))


def _profile_comparison(profiles: Mapping[str, object]) -> list[ProfileComparison]:
    values = profiles.get("profiles")
    if not is_array(values):
        raise ValueError("profiles must be an array")
    result: list[ProfileComparison] = []
    for value in values:
        profile = require_object(value, context="retrieval profile")
        result.append(
            {
                "id": _text(profile["id"], context="profile id"),
                "status": _text(profile["status"], context="profile status"),
                "revision": _text(profile["revision"], context="profile revision"),
            }
        )
    return result


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def content_checksum(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode()).hexdigest()


def byte_checksum(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def instruction_markers(value: object) -> list[str]:
    raw = unicodedata.normalize(
        "NFKC", json.dumps(value, sort_keys=True, ensure_ascii=False).lower()
    )
    raw = "".join(character for character in raw if unicodedata.category(character) != "Cf")
    text = re.sub(r"[^a-z0-9]+", " ", raw)
    return [marker for marker in INSTRUCTION_MARKERS if marker in text]


def load_json(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not is_object(value):
        raise ValueError(f"{path}: expected an object")
    return value


def validate_manifest(manifest: Mapping[str, object]) -> list[str]:
    schema = load_json(SCHEMA)
    # Adapt the library method only; input values remain unchecked until validation.
    validator = cast(_SchemaValidator, Draft202012Validator(schema, format_checker=FormatChecker()))
    errors = [
        f"{'.'.join(map(str, item.absolute_path))}: {item.message}"
        for item in validator.iter_errors(manifest)
    ]
    ids: list[str] = []
    corpus_compartment = manifest.get("compartment")
    for unit in object_rows(manifest.get("units", [])):
        unit_id = unit.get("id")
        if isinstance(unit_id, str):
            ids.append(unit_id)
        if unit.get("checksum") != content_checksum(str(unit.get("content", ""))):
            errors.append(f"{unit_id}: content checksum mismatch")
        if unit.get("compartment") != corpus_compartment:
            errors.append(f"{unit_id}: cross-compartment unit")
        if unit.get("rights") in ("restricted", "unknown"):
            errors.append(f"{unit_id}: rights not admitted")
        basis_value = unit.get("rights_basis", {})
        basis = basis_value if is_object(basis_value) else {}
        expected_basis = {"generated": "generated_origin"}.get(str(unit.get("rights")))
        if expected_basis and basis.get("kind") != expected_basis:
            errors.append(f"{unit_id}: rights basis does not admit {unit.get('rights')}")
        if unit.get("rights") == "approved_public":
            errors.append(f"{unit_id}: approved-public admission receipt registry unavailable")
        location_value = unit.get("location", {})
        location = location_value if is_object(location_value) else {}
        location_requirements = {
            "chunk": "chunk_id",
            "page": "page",
            "section": "section",
            "table": "table_id",
            "transcript": "time_range",
            "image_region": "region",
            "signal_window": "window",
        }
        kind = location.get("kind")
        if (
            not isinstance(kind, str)
            or kind not in location_requirements
            or location_requirements[kind] not in location
        ):
            errors.append(f"{unit_id}: unsupported or incomplete provenance location")
        markers = instruction_markers(unit)
        if markers and unit.get("status") != "quarantined":
            errors.append(f"{unit_id}: instruction-like source must be quarantined")
    for unit_id in sorted(set(ids)):
        if ids.count(unit_id) > 1:
            errors.append(f"duplicate unit id: {unit_id}")
    return sorted(errors)


def admitted_manifest(path: Path = CORPUS, *, compartment: str = "public") -> RetrievalManifest:
    raw = load_json(path)
    raw_units = raw.get("units", [])
    if not is_array(raw_units):
        raise ValueError("units must be an array")
    units = [
        unit
        for value in raw_units
        if (unit := require_object(value, context="source unit"))
        if unit.get("compartment") == compartment
        and unit.get("rights") in ("generated", "approved_public")
    ]
    manifest: JsonObject = {
        "schema_version": "1.0",
        "corpus_id": raw["corpus_id"],
        "compartment": compartment,
        "units": units,
    }
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema_version": "1.0",
        "corpus_id": _text(raw["corpus_id"], context="corpus id"),
        "compartment": compartment,
        "units": _checked_units(units),
    }


class LexicalIndex:
    def __init__(self, path: Path | str = ":memory:", *, compartment: str) -> None:
        self.path = path
        self.compartment = compartment
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS index_metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        stored: object = self.connection.execute(
            "SELECT value FROM index_metadata WHERE key = 'compartment'"
        ).fetchone()
        if stored is None:
            self.connection.execute(
                "INSERT INTO index_metadata(key, value) VALUES ('compartment', ?)",
                (compartment,),
            )
            self.connection.commit()
        elif _row_text(_row(stored), "value") != compartment:
            self.connection.close()
            raise ValueError("persistent index compartment mismatch")
        self.connection.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS units USING fts5(id UNINDEXED, content, source UNINDEXED, authority UNINDEXED, jurisdiction UNINDEXED, rights UNINDEXED, rights_basis UNINDEXED, version UNINDEXED, timestamp UNINDEXED, location UNINDEXED, transformation UNINDEXED, status UNINDEXED, checksum UNINDEXED, compartment UNINDEXED, retention UNINDEXED, safety_flags UNINDEXED)"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS lifecycle_audit(sequence INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, unit_id TEXT, compartment TEXT NOT NULL, detail_sha256 TEXT NOT NULL)"
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __del__(self) -> None:
        connection = getattr(self, "connection", None)
        if connection is not None:
            connection.close()

    def ingest(self, manifest: Mapping[str, object]) -> None:
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError("; ".join(errors))
        if manifest["compartment"] != self.compartment:
            raise ValueError("index compartment mismatch")
        units = _checked_units(manifest["units"])
        with self.connection:
            self._ingest_validated(units)

    def _ingest_validated(self, units: list[RetrievalUnit]) -> None:
        for unit in units:
            self.connection.execute(
                "DELETE FROM units WHERE id = ? AND compartment = ?",
                (unit["id"], self.compartment),
            )
            flags = instruction_markers(
                {
                    "content": unit["content"],
                    "source": unit["source"],
                    "authority": unit["authority"],
                    "location": unit["location"],
                }
            )
            self.connection.execute(
                "INSERT INTO units VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    unit["id"],
                    unit["content"],
                    unit["source"],
                    unit["authority"],
                    unit["jurisdiction"],
                    unit["rights"],
                    json.dumps(unit["rights_basis"], sort_keys=True),
                    unit["version"],
                    unit["timestamp"],
                    json.dumps(unit["location"], sort_keys=True),
                    json.dumps(unit["transformation"], sort_keys=True),
                    unit["status"],
                    unit["checksum"],
                    unit["compartment"],
                    unit["retention"],
                    json.dumps(flags),
                ),
            )
            self._audit("ingest", unit["id"], unit)

    def _audit(self, action: str, unit_id: str | None, detail: object) -> None:
        self.connection.execute(
            "INSERT INTO lifecycle_audit(action, unit_id, compartment, detail_sha256) VALUES (?, ?, ?, ?)",
            (action, unit_id, self.compartment, canonical_hash(detail)),
        )

    def search(
        self,
        query: str,
        *,
        filters: dict[str, str] | None = None,
        limit: int = 10,
        mode: str = "literal",
    ) -> RetrievalReceipt:
        if not query.strip() or limit < 1 or limit > 100:
            raise ValueError("query must be non-empty and limit must be between 1 and 100")
        if mode not in {"literal", "expert_fts"}:
            raise ValueError("unsupported query mode")
        filters = dict(filters or {})
        allowed = {"authority", "jurisdiction", "version", "timestamp", "status", "source"}
        if set(filters) - allowed:
            raise ValueError("unsupported filter")
        expression = '"' + query.replace('"', '""') + '"' if mode == "literal" else query
        where = ["units MATCH ?", "compartment = ?"]
        parameters: list[str | int] = [expression, self.compartment]
        if "status" not in filters:
            filters["status"] = "current"
        for field in sorted(filters):
            where.append(f"{field} = ?")
            parameters.append(filters[field])
        parameters.append(limit)
        try:
            rows: list[object] = self.connection.execute(
                f"SELECT id, source, authority, jurisdiction, rights, rights_basis, version, timestamp, location, transformation, status, checksum, retention, safety_flags, bm25(units) AS rank FROM units WHERE {' AND '.join(where)} ORDER BY rank, id LIMIT ?",  # nosec B608 # identifiers are allowlisted; all values use SQL parameters
                parameters,
            ).fetchall()
        except sqlite3.OperationalError as exc:
            raise ValueError("invalid FTS query") from exc
        results: list[RetrievalHit] = []
        for value in rows:
            row = _row(value)
            rank: object = row["rank"]
            if not isinstance(rank, (float, int)):
                raise ValueError("index rank must be numeric")
            results.append(
                {
                    "unit_id": _row_text(row, "id"),
                    "source": _row_text(row, "source"),
                    "authority": _row_text(row, "authority"),
                    "jurisdiction": _row_text(row, "jurisdiction"),
                    "rights": _row_text(row, "rights"),
                    "rights_basis": require_object(
                        _row_json(row, "rights_basis"), context="index rights basis"
                    ),
                    "version": _row_text(row, "version"),
                    "timestamp": _row_text(row, "timestamp"),
                    "location": require_object(
                        _row_json(row, "location"), context="index location"
                    ),
                    "transformation": _texts(
                        _row_json(row, "transformation"), context="index transformation"
                    ),
                    "status": _row_text(row, "status"),
                    "checksum": _row_text(row, "checksum"),
                    "retention": _row_text(row, "retention"),
                    "safety_flags": _texts(
                        _row_json(row, "safety_flags"), context="index safety flags"
                    ),
                    "score": round(-float(rank), 8),
                }
            )
        receipt: _RetrievalFields = {
            "schema_version": "1.0",
            "profile": "lexical-sqlite-fts5",
            "query": query,
            "query_mode": mode,
            "filters": filters,
            "compartment": self.compartment,
            "limit": limit,
            "results": results,
            "network": "disabled",
            "telemetry": "none",
        }
        return {**receipt, "receipt_sha256": canonical_hash(receipt)}

    def delete(self, unit_id: str) -> None:
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM units WHERE id = ? AND compartment = ?",
                (unit_id, self.compartment),
            )
            if cursor.rowcount != 1:
                raise ValueError("unit not found in index compartment")
            self._audit("delete", unit_id, {"unit_id": unit_id})

    def supersede(self, unit_id: str) -> None:
        with self.connection:
            cursor = self.connection.execute(
                "UPDATE units SET status = 'superseded' WHERE id = ? AND compartment = ?",
                (unit_id, self.compartment),
            )
            if cursor.rowcount != 1:
                raise ValueError("unit not found in index compartment")
            self._audit("supersede", unit_id, {"unit_id": unit_id})

    def correct(self, unit: Mapping[str, object]) -> None:
        unit_id = unit.get("id")
        if not isinstance(unit_id, str):
            raise ValueError("unit not found in index compartment")
        previous: object = self.connection.execute(
            "SELECT checksum FROM units WHERE id = ? AND compartment = ?",
            (unit_id, self.compartment),
        ).fetchone()
        if previous is None:
            raise ValueError("unit not found in index compartment")
        self.ingest(
            {
                "schema_version": "1.0",
                "corpus_id": "correction",
                "compartment": self.compartment,
                "units": [unit],
            }
        )
        with self.connection:
            self._audit(
                "correct",
                unit_id,
                {
                    "previous_checksum": _row_text(_row(previous), "checksum"),
                    "new_checksum": unit.get("checksum"),
                },
            )

    def rebuild(self, manifest: Mapping[str, object]) -> None:
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError("; ".join(errors))
        if manifest["compartment"] != self.compartment:
            raise ValueError("index compartment mismatch")
        units = _checked_units(manifest["units"])
        with self.connection:
            self.connection.execute("DELETE FROM units WHERE compartment = ?", (self.compartment,))
            self._audit("rebuild", None, {"manifest_sha256": canonical_hash(manifest)})
            self._ingest_validated(units)

    def deterministic_export(self) -> list[dict[str, str]]:
        rows: list[object] = self.connection.execute(
            "SELECT id, source, authority, jurisdiction, rights, rights_basis, version, timestamp, location, transformation, status, checksum, compartment, retention, safety_flags FROM units WHERE compartment = ? ORDER BY id",
            (self.compartment,),
        ).fetchall()
        exported: list[dict[str, str]] = []
        for value in rows:
            row = _row(value)
            fields = row.keys()
            exported.append({field: _row_text(row, field) for field in fields})
        return exported

    def lifecycle_receipt(self) -> LifecycleReceipt:
        rows: list[object] = self.connection.execute(
            "SELECT sequence, action, unit_id, compartment, detail_sha256 FROM lifecycle_audit WHERE compartment = ? ORDER BY sequence",
            (self.compartment,),
        ).fetchall()
        events: list[LifecycleEvent] = []
        for value in rows:
            row = _row(value)
            sequence: object = row["sequence"]
            if not isinstance(sequence, int):
                raise ValueError("lifecycle sequence must be an integer")
            unit_id: object = row["unit_id"]
            events.append(
                {
                    "sequence": sequence,
                    "action": _row_text(row, "action"),
                    "unit_id": None
                    if unit_id is None
                    else _text(unit_id, context="lifecycle unit id"),
                    "compartment": _row_text(row, "compartment"),
                    "detail_sha256": _row_text(row, "detail_sha256"),
                }
            )
        receipt: _LifecycleFields = {
            "schema_version": "1.0",
            "compartment": self.compartment,
            "events": events,
        }
        return {**receipt, "receipt_sha256": canonical_hash(receipt)}

    def backup(self, destination: Path) -> None:
        if self.path == ":memory:":
            target = sqlite3.connect(destination)
            self.connection.backup(target)
            target.close()
        else:
            self.connection.commit()
            shutil.copy2(self.path, destination)

    @classmethod
    def restore(cls, source: Path, destination: Path, *, compartment: str) -> LexicalIndex:
        if destination.exists():
            raise ValueError("restore destination must not exist")
        shutil.copy2(source, destination)
        restored = cls(destination, compartment=compartment)
        with restored.connection:
            restored._audit("restore", None, {"source_sha256": byte_checksum(source.read_bytes())})
        return restored


def validate_literature_receipt(receipt: Mapping[str, object]) -> list[str]:
    required = {
        "schema_version",
        "query",
        "provider",
        "date",
        "filters",
        "results",
        "screening",
        "sourceright",
        "conflicts",
        "study_quality",
        "claim_links",
        "recommendation_rationales",
        "limitations",
        "receipt_sha256",
    }
    errors = [f"missing {field}" for field in sorted(required - receipt.keys())]
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if receipt.get("receipt_sha256") != canonical_hash(unsigned):
        errors.append("receipt hash mismatch")
    if receipt.get("schema_version") != "1.0":
        errors.append("invalid schema version")
    sourceright_value = receipt.get("sourceright", {})
    if not is_object(sourceright_value):
        errors.append("SourceRight receipt must be an object")
        sourceright: JsonObject = {}
    else:
        sourceright = sourceright_value
    if sourceright.get("status") not in (
        "succeeded",
        "unavailable",
        "review_required",
    ):
        errors.append("invalid SourceRight status")
    elif sourceright.get("status") == "succeeded":
        errors.append("SourceRight success is not admitted without a checked Track07 execution")
    elif sourceright.get("status") == "unavailable" and not sourceright.get("diagnostic"):
        errors.append("unavailable SourceRight receipt lacks diagnostic")
    results_value = receipt.get("results", [])
    if not is_array(results_value):
        errors.append("literature results must be an array")
        results: list[object] = []
    else:
        results = results_value
    if any(
        not is_object(item)
        or not {"title", "authors", "year", "identifier", "source"} <= item.keys()
        or not isinstance(item.get("identifier"), str)
        for item in results
    ):
        errors.append("incomplete exact reference metadata")
    if receipt.get("network") != "disabled" or receipt.get("private_data") is not False:
        errors.append("literature execution boundary mismatch")
    if not isinstance(receipt.get("query"), str) or not str(receipt.get("query", "")).strip():
        errors.append("literature query must be non-empty")
    if not isinstance(receipt.get("provider"), str) or not str(receipt.get("provider", "")).strip():
        errors.append("literature provider must be non-empty")
    try:
        date.fromisoformat(str(receipt.get("date", "")))
    except ValueError:
        errors.append("literature date must be ISO YYYY-MM-DD")
    identifiers = [
        identifier
        for item in results
        if is_object(item) and isinstance(identifier := item.get("identifier"), str)
    ]
    if len(identifiers) != len(set(identifiers)):
        errors.append("duplicate literature identifier")
    screening_value = receipt.get("screening", [])
    if not is_array(screening_value):
        errors.append("literature screening must be an array")
        screening: list[object] = []
    else:
        screening = screening_value
    screened = {
        identifier
        for item in screening
        if is_object(item) and isinstance(identifier := item.get("identifier"), str)
    }
    if screened != set(identifiers):
        errors.append("screening/result identifier mismatch")
    if len(screening) != len(screened):
        errors.append("duplicate screening identifier")
    if any(
        not is_object(item)
        or not {"identifier", "decision", "reason"} <= item.keys()
        or not isinstance(item.get("identifier"), str)
        or item.get("decision") not in ("include", "exclude")
        or not str(item.get("reason", "")).strip()
        for item in screening
    ):
        errors.append("screening decision is incomplete")
    quality_value = receipt.get("study_quality", [])
    if not is_array(quality_value):
        errors.append("study quality must be an array")
        quality: list[object] = []
    else:
        quality = quality_value
    if {
        identifier
        for item in quality
        if is_object(item) and isinstance(identifier := item.get("identifier"), str)
    } != set(identifiers):
        errors.append("study-quality/result identifier mismatch")
    if any(
        not is_object(item)
        or not {"identifier", "status", "reason"} <= item.keys()
        or not isinstance(item.get("identifier"), str)
        or item.get("status") not in ("not_assessed", "assessed")
        or not str(item.get("reason", "")).strip()
        for item in quality
    ):
        errors.append("study-quality record is incomplete")
    if sourceright.get("status") == "unavailable" and (
        sourceright.get("revision") != "adapter 0.1 / clean vendored pin c5fa583"
        or "no Track07" not in str(sourceright.get("diagnostic", ""))
    ):
        errors.append("unavailable SourceRight boundary is not bound to the clean pin")
    referenced: set[str] = set()
    for field in ("study_quality", "claim_links", "conflicts"):
        records = receipt.get(field, [])
        if not is_array(records):
            errors.append(f"{field} must be an array")
            continue
        referenced.update(
            identifier
            for item in records
            if is_object(item) and isinstance(identifier := item.get("identifier"), str)
        )
    if not referenced <= set(identifiers):
        errors.append("literature record references unknown identifier")
    return errors


def validate_profiles(profiles: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    values = profiles.get("profiles", [])
    if not is_array(values):
        errors.append("profiles must be an array")
        items: list[object] = []
    else:
        items = values
    raw_identifiers = [item.get("id") for item in items if is_object(item)]
    identifiers = [identifier for identifier in raw_identifiers if isinstance(identifier, str)]
    expected = {
        "lexical-sqlite-fts5",
        "vector-local",
        "hybrid-fusion",
        "reranker-local",
        "literature-provider",
        "sourceright",
    }
    if (
        len(identifiers) != len(raw_identifiers)
        or set(identifiers) != expected
        or len(identifiers) != len(set(identifiers))
    ):
        errors.append("profile coverage mismatch")
    for item in items:
        if not is_object(item):
            errors.append("profile must be an object")
            continue
        if item.get("network") != "disabled" or item.get("telemetry") != "none":
            errors.append(f"{item.get('id')}: execution boundary mismatch")
        if (
            item.get("id") != "lexical-sqlite-fts5"
            and item.get("status") == "supported_ci_contract"
        ):
            errors.append(f"{item.get('id')}: optional profile cannot be supported")
        for field in ("owner", "upstream", "removal_condition"):
            if not item.get(field):
                errors.append(f"{item.get('id')}: missing {field}")
    empty_profile: JsonObject = {}
    lexical = next(
        (item for item in items if is_object(item) and item.get("id") == "lexical-sqlite-fts5"),
        empty_profile,
    )
    for field in ("install", "discover", "health_check", "uninstall", "rollback"):
        if not lexical.get(field):
            errors.append(f"lexical-sqlite-fts5: missing {field}")
    return errors


def grounded_answer(
    claims: Sequence[Mapping[str, object]], retrieved: Mapping[str, object]
) -> GroundingResult:
    available = {
        _text(item["unit_id"], context="retrieved unit id"): item
        for item in object_rows(retrieved.get("results", []))
    }
    valid_claims: list[JsonObject] = []
    conflicts: list[str] = []
    poisoned: list[str] = []
    for claim in claims:
        evidence = set(_texts(claim.get("evidence", []), context="claim evidence"))
        if not evidence or not evidence <= available.keys():
            continue
        if claim.get("conflict"):
            conflicts.append(_text(claim["id"], context="claim id"))
        flagged = any(available[item].get("safety_flags") for item in evidence)
        if flagged or instruction_markers(claim.get("text", "")):
            poisoned.append(_text(claim["id"], context="claim id"))
            continue
        # A search receipt proves a link, not the semantics or exact bytes of
        # caller-supplied claim text. No synthesis is admitted at this port.
    return {
        "claims": valid_claims,
        "conflicts": conflicts,
        "poisoned_content": poisoned,
        "abstained": not valid_claims or bool(conflicts),
        "grounding": "claim_link_only",
        "clinical_interpretation": False,
        "human_review_required": True,
    }


def validate_federated_request(request: Mapping[str, object]) -> list[str]:
    required_true = (
        "authorised",
        "minimised",
        "deidentified_or_aggregated",
        "lineage_current",
        "retention_current",
        "fresh",
    )
    errors = [f"{field} required" for field in required_true if request.get(field) is not True]
    if request.get("purpose") not in ("synthetic_research", "quality_assurance"):
        errors.append("purpose not admitted")
    compartments = request.get("compartments")
    valid_compartments = is_array(compartments) and all(
        isinstance(item, str) for item in compartments
    )
    if compartments and (
        not valid_compartments
        or len(set(_texts(compartments, context="federated compartments"))) != 1
    ):
        errors.append("cross-compartment federation prohibited")
    if not is_array(compartments) or len(compartments) != 1:
        errors.append("exactly one compartment required")
    if request.get("access_decision") != "synthetic_contract_admitted" or not request.get("role"):
        errors.append("explicit access decision and role required")
    if request.get("compartments") != ["public"] or request.get("role") != "test-harness":
        errors.append("federation remains public synthetic contract-only")
    if request.get("causal_finding") is True:
        errors.append("cross-case retrieval cannot create a causal finding")
    return errors


def reciprocal_rank_fusion(
    candidate_sets: list[list[str]], *, rank_constant: int = 60
) -> list[FusionResult]:
    """Fuse declared candidate identifiers without adding retrieval or model behaviour."""
    if rank_constant < 1 or not candidate_sets:
        raise ValueError("rank constant and candidate sets must be non-empty")
    scores: dict[str, float] = {}
    for candidates in candidate_sets:
        if len(candidates) != len(set(candidates)):
            raise ValueError("candidate set contains duplicate identifiers")
        for rank, identifier in enumerate(candidates, start=1):
            scores[identifier] = scores.get(identifier, 0.0) + 1.0 / (rank_constant + rank)
    return [
        {"unit_id": identifier, "fusion_score": round(score, 12)}
        for identifier, score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    ]


def drift_impact(
    previous: Mapping[str, object],
    current: Mapping[str, object],
    receipts: Sequence[Mapping[str, object]],
) -> DriftImpact:
    for label, manifest in (("previous", previous), ("current", current)):
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError(f"invalid {label} manifest: {'; '.join(errors)}")
    before = {item["id"]: item["checksum"] for item in _checked_units(previous["units"])}
    after = {item["id"]: item["checksum"] for item in _checked_units(current["units"])}
    changed = sorted(
        unit_id
        for unit_id in before.keys() | after.keys()
        if before.get(unit_id) != after.get(unit_id)
    )
    affected = sorted(
        _text(receipt.get("receipt_sha256", "unhashed"), context="retrieval receipt hash")
        for receipt in receipts
        if any(
            result.get("unit_id") in changed for result in object_rows(receipt.get("results", []))
        )
    )
    return {
        "changed_units": changed,
        "affected_receipts": affected,
        "requires_rebuild": bool(changed),
    }


def assurance() -> AssuranceReceipt:
    manifest = admitted_manifest()
    index = LexicalIndex(compartment="public")
    index.ingest(manifest)
    started = time.perf_counter()
    tracemalloc.start()
    cases = {
        "exact": index.search("uncertainty"),
        "phrase": index.search("evidence citations"),
        "acronym": index.search("SAC"),
        "version_filter": index.search("policy", filters={"version": "2.0"}),
        "typo": index.search("uncertanty"),
    }
    results: dict[str, AssuranceCase] = {
        name: {
            "hits": len(receipt["results"]),
            "passed": bool(receipt["results"]) if name != "typo" else not receipt["results"],
        }
        for name, receipt in cases.items()
    }
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    citation = all(
        {"source", "location", "checksum", "rights_basis"} <= item.keys()
        for receipt in cases.values()
        for item in receipt["results"]
    )
    malformed_controlled = False
    try:
        index.search('"', mode="expert_fts")
    except ValueError:
        malformed_controlled = True
    changed = deepcopy(manifest)
    changed["units"][0]["content"] += " Revised synthetic source."
    changed["units"][0]["checksum"] = content_checksum(changed["units"][0]["content"])
    freshness = drift_impact(manifest, changed, [cases["exact"]])
    with tempfile.TemporaryDirectory() as directory:
        backup = Path(directory) / "backup.sqlite"
        restored_path = Path(directory) / "restored.sqlite"
        index.backup(backup)
        restored = LexicalIndex.restore(backup, restored_path, compartment="public")
        recovery = restored.deterministic_export() == index.deterministic_export()
        restored.close()
    index.close()
    profiles = load_json(PROFILES)
    receipt: _AssuranceFields = {
        "schema_version": "1.0",
        "scope": "deterministic_synthetic_ci_contract",
        "manifest_sha256": canonical_hash(manifest),
        "profile_revision": PROFILE_REVISION,
        "results": results,
        "suites": {
            "citation": {"passed": citation},
            "privacy": {
                "passed": validate_federated_request(
                    {
                        "purpose": "quality_assurance",
                        "authorised": True,
                        "minimised": True,
                        "deidentified_or_aggregated": True,
                        "lineage_current": True,
                        "retention_current": True,
                        "fresh": True,
                        "compartments": ["public", "governed_private"],
                        "access_decision": "synthetic_contract_admitted",
                        "role": "test-harness",
                        "causal_finding": False,
                    }
                )
                != []
            },
            "robustness": {"passed": malformed_controlled},
            "freshness": {
                "passed": freshness["requires_rebuild"] is True
                and freshness["changed_units"] == ["policy-current"],
                "mode": "validated-manifest drift contract",
            },
            "recovery": {"passed": recovery},
            "latency": {"passed": elapsed_ms >= 0, "status": "descriptive_not_thresholded"},
            "memory": {"passed": peak_bytes > 0, "status": "descriptive_not_thresholded"},
        },
        "profile_comparison": _profile_comparison(profiles),
        "research_observations": {
            "elapsed_ms": elapsed_ms,
            "allocation_peak_bytes": peak_bytes,
            "integrity_scope": "volatile descriptive observations excluded from receipt_sha256",
        },
        "network": "disabled",
        "private_data": False,
        "unsupported": MANDATORY_UNSUPPORTED,
    }
    receipt_hash = canonical_hash(
        {
            key: value
            for key, value in receipt.items()
            if key not in {"research_observations", "observation_sha256"}
        }
    )
    return {
        **receipt,
        "observation_sha256": canonical_hash(receipt["research_observations"]),
        "receipt_sha256": receipt_hash,
    }


def verify_assurance(receipt: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    unsigned = {
        key: value
        for key, value in receipt.items()
        if key not in {"receipt_sha256", "research_observations", "observation_sha256"}
    }
    if receipt.get("receipt_sha256") != canonical_hash(unsigned):
        errors.append("receipt hash mismatch")
    if receipt.get("network") != "disabled" or receipt.get("private_data") is not False:
        errors.append("execution boundary mismatch")
    if receipt.get("manifest_sha256") != canonical_hash(admitted_manifest()):
        errors.append("manifest binding mismatch")
    if receipt.get("profile_revision") != PROFILE_REVISION:
        errors.append("profile revision mismatch")
    if receipt.get("unsupported") != MANDATORY_UNSUPPORTED:
        errors.append("unsupported capability declaration mismatch")
    results_value = receipt.get("results", {})
    results = results_value if is_object(results_value) else {}
    expected_hits = {"exact": 1, "phrase": 1, "acronym": 1, "version_filter": 1, "typo": 0}
    if set(results) != {"exact", "phrase", "acronym", "version_filter", "typo"} or any(
        not is_object(item) or item.get("passed") is not True for item in results.values()
    ):
        errors.append("assurance case coverage mismatch")
    if any(
        not is_object(item := results.get(case)) or item.get("hits") != hits
        for case, hits in expected_hits.items()
    ):
        errors.append("assurance hit-count mismatch")
    suites_value = receipt.get("suites", {})
    suites = suites_value if is_object(suites_value) else {}
    if set(suites) != {
        "citation",
        "privacy",
        "robustness",
        "freshness",
        "recovery",
        "latency",
        "memory",
    } or any(not is_object(item) or item.get("passed") is not True for item in suites.values()):
        errors.append("assurance suite coverage mismatch")
    observations_value = receipt.get("research_observations", {})
    observations = observations_value if is_object(observations_value) else {}
    if not isinstance(observations.get("elapsed_ms"), (int, float)) or not isinstance(
        observations.get("allocation_peak_bytes"), int
    ):
        errors.append("research performance observations missing")
    if receipt.get("observation_sha256") != canonical_hash(observations_value):
        errors.append("research observation hash mismatch")
    expected_profiles = _profile_comparison(load_json(PROFILES))
    if receipt.get("profile_comparison") != expected_profiles:
        errors.append("profile comparison mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "assure", "search"))
    parser.add_argument("--query", default="evidence")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    exit_code = 0
    result: Mapping[str, object]
    if args.command == "validate":
        errors = validate_manifest(admitted_manifest()) + validate_profiles(load_json(PROFILES))
        result = {"valid": not errors, "errors": errors}
        exit_code = 1 if errors else 0
    elif args.command == "assure":
        result = assurance()
        exit_code = 1 if verify_assurance(result) else 0
    else:
        index = LexicalIndex(compartment="public")
        index.ingest(admitted_manifest())
        result = index.search(args.query)
        index.close()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
