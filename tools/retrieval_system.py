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
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

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


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def content_checksum(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode()).hexdigest()


def byte_checksum(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def instruction_markers(value: Any) -> list[str]:
    raw = unicodedata.normalize(
        "NFKC", json.dumps(value, sort_keys=True, ensure_ascii=False).lower()
    )
    raw = "".join(character for character in raw if unicodedata.category(character) != "Cf")
    text = re.sub(r"[^a-z0-9]+", " ", raw)
    return [marker for marker in INSTRUCTION_MARKERS if marker in text]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, item.absolute_path))}: {item.message}"
        for item in validator.iter_errors(manifest)
    ]
    ids: list[str] = []
    corpus_compartment = manifest.get("compartment")
    for unit in manifest.get("units", []):
        if not isinstance(unit, dict):
            continue
        unit_id = unit.get("id")
        if isinstance(unit_id, str):
            ids.append(unit_id)
        if unit.get("checksum") != content_checksum(str(unit.get("content", ""))):
            errors.append(f"{unit_id}: content checksum mismatch")
        if unit.get("compartment") != corpus_compartment:
            errors.append(f"{unit_id}: cross-compartment unit")
        if unit.get("rights") in {"restricted", "unknown"}:
            errors.append(f"{unit_id}: rights not admitted")
        basis = unit.get("rights_basis", {})
        expected_basis = {"generated": "generated_origin"}.get(str(unit.get("rights")))
        if expected_basis and basis.get("kind") != expected_basis:
            errors.append(f"{unit_id}: rights basis does not admit {unit.get('rights')}")
        if unit.get("rights") == "approved_public":
            errors.append(f"{unit_id}: approved-public admission receipt registry unavailable")
        location = unit.get("location", {})
        location_requirements = {
            "chunk": "chunk_id",
            "page": "page",
            "section": "section",
            "table": "table_id",
            "transcript": "time_range",
            "image_region": "region",
            "signal_window": "window",
        }
        kind = location.get("kind") if isinstance(location, dict) else None
        if kind not in location_requirements or location_requirements.get(kind) not in location:
            errors.append(f"{unit_id}: unsupported or incomplete provenance location")
        markers = instruction_markers(unit)
        if markers and unit.get("status") != "quarantined":
            errors.append(f"{unit_id}: instruction-like source must be quarantined")
    for unit_id in sorted(set(ids)):
        if ids.count(unit_id) > 1:
            errors.append(f"duplicate unit id: {unit_id}")
    return sorted(errors)


def admitted_manifest(path: Path = CORPUS, *, compartment: str = "public") -> dict[str, Any]:
    raw = load_json(path)
    units = [
        unit
        for unit in raw.get("units", [])
        if unit.get("compartment") == compartment
        and unit.get("rights") in {"generated", "approved_public"}
    ]
    manifest = {
        "schema_version": "1.0",
        "corpus_id": raw["corpus_id"],
        "compartment": compartment,
        "units": units,
    }
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


class LexicalIndex:
    def __init__(self, path: Path | str = ":memory:", *, compartment: str) -> None:
        self.path = path
        self.compartment = compartment
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS index_metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        stored = self.connection.execute(
            "SELECT value FROM index_metadata WHERE key = 'compartment'"
        ).fetchone()
        if stored is None:
            self.connection.execute(
                "INSERT INTO index_metadata(key, value) VALUES ('compartment', ?)",
                (compartment,),
            )
            self.connection.commit()
        elif stored["value"] != compartment:
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

    def __enter__(self) -> LexicalIndex:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __del__(self) -> None:
        connection = getattr(self, "connection", None)
        if connection is not None:
            connection.close()

    def ingest(self, manifest: dict[str, Any]) -> None:
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError("; ".join(errors))
        if manifest["compartment"] != self.compartment:
            raise ValueError("index compartment mismatch")
        with self.connection:
            self._ingest_validated(manifest)

    def _ingest_validated(self, manifest: dict[str, Any]) -> None:
        for unit in manifest["units"]:
            self.connection.execute(
                "DELETE FROM units WHERE id = ? AND compartment = ?",
                (unit["id"], self.compartment),
            )
            flags = instruction_markers(
                {key: unit[key] for key in ("content", "source", "authority", "location")}
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

    def _audit(self, action: str, unit_id: str | None, detail: Any) -> None:
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
    ) -> dict[str, Any]:
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
        parameters: list[Any] = [expression, self.compartment]
        if "status" not in filters:
            filters["status"] = "current"
        for field in sorted(filters):
            where.append(f"{field} = ?")
            parameters.append(filters[field])
        parameters.append(limit)
        try:
            rows = self.connection.execute(
                f"SELECT id, source, authority, jurisdiction, rights, rights_basis, version, timestamp, location, transformation, status, checksum, retention, safety_flags, bm25(units) AS rank FROM units WHERE {' AND '.join(where)} ORDER BY rank, id LIMIT ?",  # noqa: S608 -- fields are allowlisted
                parameters,
            ).fetchall()
        except sqlite3.OperationalError as exc:
            raise ValueError("invalid FTS query") from exc
        results = [
            {
                "unit_id": row["id"],
                "source": row["source"],
                "authority": row["authority"],
                "jurisdiction": row["jurisdiction"],
                "rights": row["rights"],
                "rights_basis": json.loads(row["rights_basis"]),
                "version": row["version"],
                "timestamp": row["timestamp"],
                "location": json.loads(row["location"]),
                "transformation": json.loads(row["transformation"]),
                "status": row["status"],
                "checksum": row["checksum"],
                "retention": row["retention"],
                "safety_flags": json.loads(row["safety_flags"]),
                "score": round(-float(row["rank"]), 8),
            }
            for row in rows
        ]
        receipt: dict[str, Any] = {
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
        receipt["receipt_sha256"] = canonical_hash(receipt)
        return receipt

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

    def correct(self, unit: dict[str, Any]) -> None:
        previous = self.connection.execute(
            "SELECT checksum FROM units WHERE id = ? AND compartment = ?",
            (unit.get("id"), self.compartment),
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
                unit.get("id"),
                {"previous_checksum": previous["checksum"], "new_checksum": unit.get("checksum")},
            )

    def rebuild(self, manifest: dict[str, Any]) -> None:
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError("; ".join(errors))
        if manifest["compartment"] != self.compartment:
            raise ValueError("index compartment mismatch")
        with self.connection:
            self.connection.execute("DELETE FROM units WHERE compartment = ?", (self.compartment,))
            self._audit("rebuild", None, {"manifest_sha256": canonical_hash(manifest)})
            self._ingest_validated(manifest)

    def deterministic_export(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT id, source, authority, jurisdiction, rights, rights_basis, version, timestamp, location, transformation, status, checksum, compartment, retention, safety_flags FROM units WHERE compartment = ? ORDER BY id",
            (self.compartment,),
        ).fetchall()
        return [dict(row) for row in rows]

    def lifecycle_receipt(self) -> dict[str, Any]:
        rows = self.connection.execute(
            "SELECT sequence, action, unit_id, compartment, detail_sha256 FROM lifecycle_audit WHERE compartment = ? ORDER BY sequence",
            (self.compartment,),
        ).fetchall()
        receipt: dict[str, Any] = {
            "schema_version": "1.0",
            "compartment": self.compartment,
            "events": [dict(row) for row in rows],
        }
        receipt["receipt_sha256"] = canonical_hash(receipt)
        return receipt

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


def validate_literature_receipt(receipt: dict[str, Any]) -> list[str]:
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
    if not isinstance(sourceright_value, dict):
        errors.append("SourceRight receipt must be an object")
        sourceright: dict[str, Any] = {}
    else:
        sourceright = sourceright_value
    if sourceright.get("status") not in {
        "succeeded",
        "unavailable",
        "review_required",
    }:
        errors.append("invalid SourceRight status")
    elif sourceright.get("status") == "succeeded":
        errors.append("SourceRight success is not admitted without a checked Track07 execution")
    elif sourceright.get("status") == "unavailable" and not sourceright.get("diagnostic"):
        errors.append("unavailable SourceRight receipt lacks diagnostic")
    results_value = receipt.get("results", [])
    if not isinstance(results_value, list):
        errors.append("literature results must be an array")
        results: list[Any] = []
    else:
        results = results_value
    if any(
        not isinstance(item, dict)
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
        item["identifier"]
        for item in results
        if isinstance(item, dict) and isinstance(item.get("identifier"), str)
    ]
    if len(identifiers) != len(set(identifiers)):
        errors.append("duplicate literature identifier")
    screening_value = receipt.get("screening", [])
    if not isinstance(screening_value, list):
        errors.append("literature screening must be an array")
        screening: list[Any] = []
    else:
        screening = screening_value
    screened = {
        item["identifier"]
        for item in screening
        if isinstance(item, dict) and isinstance(item.get("identifier"), str)
    }
    if screened != set(identifiers):
        errors.append("screening/result identifier mismatch")
    if len(screening) != len(screened):
        errors.append("duplicate screening identifier")
    if any(
        not isinstance(item, dict)
        or not {"identifier", "decision", "reason"} <= item.keys()
        or not isinstance(item.get("identifier"), str)
        or item.get("decision") not in {"include", "exclude"}
        or not str(item.get("reason", "")).strip()
        for item in screening
    ):
        errors.append("screening decision is incomplete")
    quality_value = receipt.get("study_quality", [])
    if not isinstance(quality_value, list):
        errors.append("study quality must be an array")
        quality: list[Any] = []
    else:
        quality = quality_value
    if {item.get("identifier") for item in quality if isinstance(item, dict)} != set(identifiers):
        errors.append("study-quality/result identifier mismatch")
    if any(
        not isinstance(item, dict)
        or not {"identifier", "status", "reason"} <= item.keys()
        or not isinstance(item.get("identifier"), str)
        or item.get("status") not in {"not_assessed", "assessed"}
        or not str(item.get("reason", "")).strip()
        for item in quality
    ):
        errors.append("study-quality record is incomplete")
    if sourceright.get("status") == "unavailable" and (
        sourceright.get("revision") != "adapter 0.1 / clean vendored pin c5fa583"
        or "no Track07" not in str(sourceright.get("diagnostic", ""))
    ):
        errors.append("unavailable SourceRight boundary is not bound to the clean pin")
    referenced: set[Any] = set()
    for field in ("study_quality", "claim_links", "conflicts"):
        records = receipt.get(field, [])
        if not isinstance(records, list):
            errors.append(f"{field} must be an array")
            continue
        referenced.update(
            item.get("identifier")
            for item in records
            if isinstance(item, dict) and isinstance(item.get("identifier"), str)
        )
    if not referenced <= set(identifiers):
        errors.append("literature record references unknown identifier")
    return errors


def validate_profiles(profiles: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    items = profiles.get("profiles", [])
    identifiers = [item.get("id") for item in items if isinstance(item, dict)]
    expected = {
        "lexical-sqlite-fts5",
        "vector-local",
        "hybrid-fusion",
        "reranker-local",
        "literature-provider",
        "sourceright",
    }
    if set(identifiers) != expected or len(identifiers) != len(set(identifiers)):
        errors.append("profile coverage mismatch")
    for item in items:
        if not isinstance(item, dict):
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
    lexical = next(
        (
            item
            for item in items
            if isinstance(item, dict) and item.get("id") == "lexical-sqlite-fts5"
        ),
        {},
    )
    for field in ("install", "discover", "health_check", "uninstall", "rollback"):
        if not lexical.get(field):
            errors.append(f"lexical-sqlite-fts5: missing {field}")
    return errors


def grounded_answer(claims: list[dict[str, Any]], retrieved: dict[str, Any]) -> dict[str, Any]:
    available = {item["unit_id"]: item for item in retrieved.get("results", [])}
    valid_claims = []
    conflicts = []
    poisoned = []
    for claim in claims:
        evidence = set(claim.get("evidence", []))
        if not evidence or not evidence <= available.keys():
            continue
        if claim.get("conflict"):
            conflicts.append(claim["id"])
        flagged = any(available[item].get("safety_flags") for item in evidence)
        if flagged or instruction_markers(claim.get("text", "")):
            poisoned.append(claim["id"])
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


def validate_federated_request(request: dict[str, Any]) -> list[str]:
    required_true = (
        "authorised",
        "minimised",
        "deidentified_or_aggregated",
        "lineage_current",
        "retention_current",
        "fresh",
    )
    errors = [f"{field} required" for field in required_true if request.get(field) is not True]
    if request.get("purpose") not in {"synthetic_research", "quality_assurance"}:
        errors.append("purpose not admitted")
    if request.get("compartments") and len(set(request["compartments"])) != 1:
        errors.append("cross-compartment federation prohibited")
    if not request.get("compartments") or len(request["compartments"]) != 1:
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
) -> list[dict[str, Any]]:
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
    previous: dict[str, Any], current: dict[str, Any], receipts: list[dict[str, Any]]
) -> dict[str, Any]:
    for label, manifest in (("previous", previous), ("current", current)):
        errors = validate_manifest(manifest)
        if errors:
            raise ValueError(f"invalid {label} manifest: {'; '.join(errors)}")
    before = {item["id"]: item["checksum"] for item in previous.get("units", [])}
    after = {item["id"]: item["checksum"] for item in current.get("units", [])}
    changed = sorted(
        unit_id
        for unit_id in before.keys() | after.keys()
        if before.get(unit_id) != after.get(unit_id)
    )
    affected = sorted(
        receipt.get("receipt_sha256", "unhashed")
        for receipt in receipts
        if any(result.get("unit_id") in changed for result in receipt.get("results", []))
    )
    return {
        "changed_units": changed,
        "affected_receipts": affected,
        "requires_rebuild": bool(changed),
    }


def assurance() -> dict[str, Any]:
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
    results = {
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
    changed = json.loads(json.dumps(manifest))
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
    receipt: dict[str, Any] = {
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
        "profile_comparison": [
            {"id": item["id"], "status": item["status"], "revision": item["revision"]}
            for item in profiles["profiles"]
        ],
        "research_observations": {
            "elapsed_ms": elapsed_ms,
            "allocation_peak_bytes": peak_bytes,
            "integrity_scope": "volatile descriptive observations excluded from receipt_sha256",
        },
        "network": "disabled",
        "private_data": False,
        "unsupported": MANDATORY_UNSUPPORTED,
    }
    receipt["observation_sha256"] = canonical_hash(receipt["research_observations"])
    receipt["receipt_sha256"] = canonical_hash(
        {
            key: value
            for key, value in receipt.items()
            if key not in {"research_observations", "observation_sha256"}
        }
    )
    return receipt


def verify_assurance(receipt: dict[str, Any]) -> list[str]:
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
    results = receipt.get("results", {})
    expected_hits = {"exact": 1, "phrase": 1, "acronym": 1, "version_filter": 1, "typo": 0}
    if set(results) != {"exact", "phrase", "acronym", "version_filter", "typo"} or any(
        item.get("passed") is not True for item in results.values()
    ):
        errors.append("assurance case coverage mismatch")
    if any(results.get(case, {}).get("hits") != hits for case, hits in expected_hits.items()):
        errors.append("assurance hit-count mismatch")
    suites = receipt.get("suites", {})
    if set(suites) != {
        "citation",
        "privacy",
        "robustness",
        "freshness",
        "recovery",
        "latency",
        "memory",
    } or any(item.get("passed") is not True for item in suites.values()):
        errors.append("assurance suite coverage mismatch")
    observations = receipt.get("research_observations", {})
    if not isinstance(observations.get("elapsed_ms"), (int, float)) or not isinstance(
        observations.get("allocation_peak_bytes"), int
    ):
        errors.append("research performance observations missing")
    if receipt.get("observation_sha256") != canonical_hash(observations):
        errors.append("research observation hash mismatch")
    profiles = load_json(PROFILES).get("profiles", [])
    expected_profiles = [
        {"id": item["id"], "status": item["status"], "revision": item["revision"]}
        for item in profiles
    ]
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
    if args.command == "validate":
        errors = validate_manifest(admitted_manifest()) + validate_profiles(load_json(PROFILES))
        result: Any = {"valid": not errors, "errors": errors}
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
