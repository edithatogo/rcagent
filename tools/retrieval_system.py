"""Deterministic, compartment-bound retrieval contracts and SQLite FTS baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import time
import tracemalloc
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).parents[1]
CORPUS = ROOT / "evaluation/retrieval/synthetic-public-corpus.json"
PROFILES = ROOT / "evaluation/retrieval/profiles.json"
SCHEMA = ROOT / "conductor/schemas/retrieval-corpus.schema.json"
INSTRUCTION_MARKERS = ("ignore previous instructions", "system prompt", "disclose private")


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def content_checksum(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode()).hexdigest()


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
            "CREATE VIRTUAL TABLE IF NOT EXISTS units USING fts5(id UNINDEXED, content, source UNINDEXED, authority UNINDEXED, jurisdiction UNINDEXED, rights UNINDEXED, version UNINDEXED, timestamp UNINDEXED, location UNINDEXED, transformation UNINDEXED, status UNINDEXED, checksum UNINDEXED, compartment UNINDEXED, retention UNINDEXED)"
        )

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
            for unit in manifest["units"]:
                self.connection.execute("DELETE FROM units WHERE id = ?", (unit["id"],))
                self.connection.execute(
                    "INSERT INTO units VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        unit["id"],
                        unit["content"],
                        unit["source"],
                        unit["authority"],
                        unit["jurisdiction"],
                        unit["rights"],
                        unit["version"],
                        unit["timestamp"],
                        json.dumps(unit["location"], sort_keys=True),
                        json.dumps(unit["transformation"], sort_keys=True),
                        unit["status"],
                        unit["checksum"],
                        unit["compartment"],
                        unit["retention"],
                    ),
                )

    def search(
        self, query: str, *, filters: dict[str, str] | None = None, limit: int = 10
    ) -> dict[str, Any]:
        if not query.strip() or limit < 1 or limit > 100:
            raise ValueError("query must be non-empty and limit must be between 1 and 100")
        filters = filters or {}
        allowed = {"authority", "jurisdiction", "version", "timestamp", "status", "source"}
        if set(filters) - allowed:
            raise ValueError("unsupported filter")
        where = ["units MATCH ?", "compartment = ?"]
        parameters: list[Any] = [query, self.compartment]
        for field in sorted(filters):
            where.append(f"{field} = ?")
            parameters.append(filters[field])
        parameters.append(limit)
        rows = self.connection.execute(
            f"SELECT id, source, authority, jurisdiction, rights, version, timestamp, location, transformation, status, checksum, retention, bm25(units) AS rank FROM units WHERE {' AND '.join(where)} ORDER BY rank, id LIMIT ?",  # noqa: S608 -- fields are allowlisted
            parameters,
        ).fetchall()
        results = [
            {
                "unit_id": row["id"],
                "source": row["source"],
                "authority": row["authority"],
                "jurisdiction": row["jurisdiction"],
                "rights": row["rights"],
                "version": row["version"],
                "timestamp": row["timestamp"],
                "location": json.loads(row["location"]),
                "transformation": json.loads(row["transformation"]),
                "status": row["status"],
                "checksum": row["checksum"],
                "retention": row["retention"],
                "score": round(-float(row["rank"]), 8),
            }
            for row in rows
            if row["status"] == "current"
        ]
        receipt: dict[str, Any] = {
            "schema_version": "1.0",
            "profile": "lexical-sqlite-fts5",
            "query": query,
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
            self.connection.execute("DELETE FROM units WHERE id = ?", (unit_id,))

    def rebuild(self, manifest: dict[str, Any]) -> None:
        with self.connection:
            self.connection.execute("DELETE FROM units")
        self.ingest(manifest)

    def deterministic_export(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT id, checksum, status, compartment FROM units ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    def backup(self, destination: Path) -> None:
        if self.path == ":memory:":
            target = sqlite3.connect(destination)
            self.connection.backup(target)
            target.close()
        else:
            self.connection.commit()
            shutil.copy2(self.path, destination)


def validate_literature_receipt(receipt: dict[str, Any]) -> list[str]:
    required = {
        "query",
        "provider",
        "date",
        "filters",
        "results",
        "screening",
        "sourceright",
        "conflicts",
    }
    errors = [f"missing {field}" for field in sorted(required - receipt.keys())]
    if receipt.get("sourceright", {}).get("status") not in {
        "succeeded",
        "unavailable",
        "review_required",
    }:
        errors.append("invalid SourceRight status")
    if any(
        not {"title", "authors", "year", "identifier", "source"} <= item.keys()
        for item in receipt.get("results", [])
    ):
        errors.append("incomplete exact reference metadata")
    if receipt.get("network") != "disabled" or receipt.get("private_data") is not False:
        errors.append("literature execution boundary mismatch")
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
    available = {item["unit_id"] for item in retrieved.get("results", [])}
    valid_claims = []
    conflicts = []
    poisoned = []
    for claim in claims:
        evidence = set(claim.get("evidence", []))
        if not evidence or not evidence <= available:
            continue
        if claim.get("conflict"):
            conflicts.append(claim["id"])
        text = str(claim.get("text", "")).lower()
        if any(marker in text for marker in INSTRUCTION_MARKERS):
            poisoned.append(claim["id"])
            continue
        valid_claims.append(claim)
    return {
        "claims": valid_claims,
        "conflicts": conflicts,
        "poisoned_content": poisoned,
        "abstained": not valid_claims or bool(conflicts),
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
    started = time.perf_counter()
    tracemalloc.start()
    index.ingest(manifest)
    cases = {
        "exact": index.search("uncertainty"),
        "phrase": index.search('"evidence citations"'),
        "acronym": index.search("SAC"),
        "version_filter": index.search("policy", filters={"version": "2.0"}),
        "typo": index.search("uncertanty"),
    }
    index.close()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    results = {
        name: {
            "hits": len(receipt["results"]),
            "passed": bool(receipt["results"]) if name != "typo" else not receipt["results"],
        }
        for name, receipt in cases.items()
    }
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "scope": "deterministic_synthetic_ci_contract",
        "manifest_sha256": canonical_hash(manifest),
        "profile_revision": "lexical-sqlite-fts5 contract 1.0",
        "results": results,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "allocation_peak_bytes": peak,
        "network": "disabled",
        "private_data": False,
        "unsupported": [
            "typo correction",
            "vector retrieval",
            "hybrid retrieval",
            "model reranking",
            "external literature provider",
            "cross-compartment retrieval",
            "operational thresholds",
        ],
    }
    receipt["receipt_sha256"] = canonical_hash(receipt)
    return receipt


def verify_assurance(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if receipt.get("receipt_sha256") != canonical_hash(unsigned):
        errors.append("receipt hash mismatch")
    if receipt.get("network") != "disabled" or receipt.get("private_data") is not False:
        errors.append("execution boundary mismatch")
    results = receipt.get("results", {})
    if set(results) != {"exact", "phrase", "acronym", "version_filter", "typo"} or any(
        item.get("passed") is not True for item in results.values()
    ):
        errors.append("assurance case coverage mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "assure", "search"))
    parser.add_argument("--query", default="evidence")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_manifest(admitted_manifest()) + validate_profiles(load_json(PROFILES))
        result: Any = {"valid": not errors, "errors": errors}
    elif args.command == "assure":
        result = assurance()
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
