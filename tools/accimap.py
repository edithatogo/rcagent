"""Synthetic AcciMap validation and deterministic, evidence-linked draft diagrams.

This companion format does not change the canonical safety-work record. Its
explicit causal hypotheses are separate from canonical evidential relationships.
Structural admission, a declared review and a rendered diagram establish neither
causation nor authentic human review, source truth, privacy or deployment approval.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import NoReturn, Protocol, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from tools.evidence_core import canonical_bytes, fingerprint, validate_record
from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

SCHEMA_PATH = Path(__file__).parents[1] / "evaluation/accimap/accimap.schema.json"
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_RENDER_BYTES = 8 * 1024 * 1024
MAX_DEPTH = 64
MAX_VALUES = 100_000
PROFILES: dict[str, tuple[tuple[str, str], ...]] = {
    "rcagent-healthcare-six-v1": (
        ("government", "Government and policy"),
        ("regulators", "Regulatory bodies and associations"),
        ("management", "Hospital management"),
        ("environment", "Physical and technical environment"),
        ("staff", "Staff and operators"),
        ("patient", "Patient and activity"),
    ),
    "rasmussen-svedung-six-v1": (
        ("government", "Government"),
        ("regulators", "Regulators and associations"),
        ("company_management", "Company management"),
        ("operational_management", "Operational management"),
        ("processes", "Physical processes and actor activities"),
        ("equipment", "Equipment and surroundings"),
    ),
}
OUTCOME_STATEMENT_KINDS = {
    "observed_fact",
    "reported_account",
    "inference",
    "hypothesis",
    "finding",
}


class _Validator(Protocol):
    """Use jsonschema's supported validation method without an untyped boundary."""

    def iter_errors(self, _instance: object, /) -> Iterable[ValidationError]: ...


def _json_errors(value: object, context: str) -> list[str]:
    """Reject non-JSON values before schema validation or canonical hashing."""
    count = 0

    def walk(current: object, ancestors: set[int], depth: int) -> str | None:
        nonlocal count
        count += 1
        if count > MAX_VALUES:
            return "too many JSON values"
        if depth > MAX_DEPTH:
            return "JSON nesting exceeds 64 levels"
        if current is None or isinstance(current, (bool, int)):
            return None
        if isinstance(current, float):
            return None if math.isfinite(current) else "non-finite number"
        if isinstance(current, str):
            try:
                current.encode("utf-8")
            except UnicodeError:
                return "invalid Unicode scalar value"
            return None
        if not is_object(current) and not is_array(current):
            return "non-JSON value or non-string object key"
        identity = id(current)
        if identity in ancestors:
            return "cyclic JSON container"
        ancestors.add(identity)
        children: Iterable[object]
        if is_object(current):
            for key in current:
                if error := walk(key, ancestors, depth + 1):
                    return error
            children = current.values()
        else:
            children = current
        for child in children:
            if error := walk(child, ancestors, depth + 1):
                return error
        ancestors.remove(identity)
        return None

    if error := walk(value, set(), 0):
        return [f"{context}: {error}"]
    try:
        encoded = canonical_bytes(value)
    except (TypeError, ValueError, OverflowError, RecursionError):
        return [f"{context}: cannot encode canonical JSON"]
    if len(encoded) > MAX_INPUT_BYTES:
        return [f"{context}: canonical JSON exceeds 2 MiB"]
    return []


def _text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("validated text has an unexpected type")
    return value


def _strings(value: object) -> list[str]:
    if not is_array(value) or not all(isinstance(item, str) for item in value):
        raise ValueError("validated identifier list has an unexpected type")
    return [_text(item) for item in value]


def _index(record: JsonObject, collection: str, key: str) -> dict[str, JsonObject]:
    return {_text(row[key]): row for row in object_rows(record.get(collection))}


def _statement_unavailable(statement: JsonObject) -> bool:
    provenance = require_object(statement["provenance"], context="statement provenance")
    return statement.get("withdrawn") is True or provenance.get("review_state") in {
        "rejected",
        "withdrawn",
    }


def _statement_source_excluded(statement: JsonObject, sources: dict[str, JsonObject]) -> bool:
    provenance = require_object(statement["provenance"], context="statement provenance")
    source = sources[_text(provenance["source_id"])]
    return source.get("screening_state") == "excluded"


def graph_fingerprint(graph: object) -> str:
    """Hash graph content excluding ``review``; this helper does not admit a map.

    Raises ValueError for non-object, non-JSON, excessive or invalid Unicode input.
    The record binding remains in the hash so a review cannot transfer to a new
    record revision. Array order is part of this exact-content review identity.
    """
    if errors := _json_errors(graph, "graph"):
        raise ValueError("; ".join(errors))
    value = require_object(graph, context="graph")
    return fingerprint({key: item for key, item in value.items() if key != "review"})


def _schema_errors(graph: JsonObject) -> list[str]:
    raw_schema: object = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema = require_object(raw_schema, context="AcciMap schema")
    Draft202012Validator.check_schema(schema)
    validator = cast(_Validator, Draft202012Validator(schema, format_checker=FormatChecker()))
    return [
        f"graph.{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in validator.iter_errors(graph)
    ]


def _node_errors(graph: JsonObject, record: JsonObject) -> list[str]:
    errors: list[str] = []
    statements = _index(record, "statements", "statement_id")
    factors = _index(record, "factors", "factor_id")
    sources = _index(record, "sources", "source_id")
    profile = PROFILES[_text(graph["profile_id"])]
    levels = {identifier for identifier, _ in profile}
    outcomes: set[str] = set()
    for node in object_rows(graph["nodes"]):
        node_id = _text(node["node_id"])
        prefix = f"nodes.{node_id}"
        level = node["level_id"]
        if level is not None and level not in levels:
            errors.append(f"{prefix}: unknown level_id for selected profile")
        statement = statements.get(_text(node["statement_id"]))
        if statement is None:
            errors.append(f"{prefix}: unknown statement_id")
        elif _statement_unavailable(statement):
            errors.append(f"{prefix}: statement is rejected or withdrawn")
        elif _statement_source_excluded(statement, sources):
            errors.append(f"{prefix}: statement has excluded source")
        if node["kind"] == "outcome":
            outcomes.add(node_id)
            if statement is not None and statement["kind"] not in OUTCOME_STATEMENT_KINDS:
                errors.append(f"{prefix}: outcome requires an incident-outcome statement kind")
        else:
            factor = factors.get(_text(node["factor_id"]))
            if factor is None:
                errors.append(f"{prefix}: unknown factor_id")
            elif factor["statement_id"] != node["statement_id"]:
                errors.append(f"{prefix}: factor statement_id mismatch")
            elif factor["status"] in {"rejected", "withdrawn"}:
                errors.append(f"{prefix}: factor is rejected or withdrawn")
    if set(_strings(graph["outcome_node_ids"])) != outcomes:
        errors.append("outcome_node_ids: must exactly identify all outcome nodes")
    return errors


def _edge_errors(graph: JsonObject, record: JsonObject) -> list[str]:
    errors: list[str] = []
    nodes = _index(graph, "nodes", "node_id")
    evidence = _index(record, "evidence", "evidence_id")
    sources = _index(record, "sources", "source_id")
    for edge in object_rows(graph["edges"]):
        prefix = f"edges.{_text(edge['edge_id'])}"
        source, target = _text(edge["from_node_id"]), _text(edge["to_node_id"])
        if source not in nodes or target not in nodes:
            errors.append(f"{prefix}: unknown node endpoint")
        if source == target:
            errors.append(f"{prefix}: self-link is not permitted")
        supporting = set(_strings(edge["evidence_ids"]))
        conflicting = set(_strings(edge["conflicting_evidence_ids"]))
        if supporting & conflicting:
            errors.append(f"{prefix}: supporting and conflicting evidence overlap")
        for evidence_id in sorted(supporting | conflicting):
            item = evidence.get(evidence_id)
            if item is None:
                errors.append(f"{prefix}: unknown evidence_id {evidence_id}")
                continue
            if item["custody_state"] == "withdrawn":
                errors.append(f"{prefix}: withdrawn evidence {evidence_id}")
            evidence_source = sources.get(_text(item["source_id"]))
            if evidence_source is None:
                errors.append(f"{prefix}: evidence source is unresolved for {evidence_id}")
            elif evidence_source.get("screening_state") == "excluded":
                errors.append(f"{prefix}: excluded source for evidence {evidence_id}")
    return errors


def _recommendation_errors(graph: JsonObject, record: JsonObject) -> list[str]:
    errors: list[str] = []
    statements = _index(record, "statements", "statement_id")
    sources = _index(record, "sources", "source_id")
    actions = _index(record, "actions", "action_id")
    nodes = _index(graph, "nodes", "node_id")
    edges = _index(graph, "edges", "edge_id")
    for index, recommendation in enumerate(object_rows(graph["recommendations"])):
        prefix = f"recommendations.{index}"
        statement_id = _text(recommendation["statement_id"])
        statement = statements.get(statement_id)
        if statement is None:
            errors.append(f"{prefix}: unknown recommendation statement")
        elif statement["kind"] != "recommendation":
            errors.append(f"{prefix}: must reference a recommendation")
        elif _statement_unavailable(statement):
            errors.append(f"{prefix}: recommendation is rejected or withdrawn")
        elif _statement_source_excluded(statement, sources):
            errors.append(f"{prefix}: recommendation has excluded source")
        if any(
            identifier not in nodes for identifier in _strings(recommendation["target_node_ids"])
        ):
            errors.append(f"{prefix}: unknown target_node_id")
        if any(
            identifier not in edges for identifier in _strings(recommendation["target_edge_ids"])
        ):
            errors.append(f"{prefix}: unknown target_edge_id")
        for action_id in _strings(recommendation["action_ids"]):
            action = actions.get(action_id)
            if action is None:
                errors.append(f"{prefix}: unknown action_id {action_id}")
            elif action["recommendation_id"] != statement_id:
                errors.append(f"{prefix}: action recommendation_id mismatch for {action_id}")
    return errors


def validate_accimap(graph: object, record: object) -> list[str]:
    """Return sorted structural/identity errors without modifying either input."""
    errors = _json_errors(graph, "graph") + _json_errors(record, "record")
    if errors:
        return sorted(set(errors))
    if not is_object(graph):
        errors.append("graph: must be a string-keyed object")
    if not is_object(record):
        errors.append("record: must be a string-keyed object")
    if not is_object(graph) or not is_object(record):
        return sorted(errors)
    errors.extend(_schema_errors(graph))
    if record.get("schema_version") != "1.1":
        errors.append("record.schema_version: must be 1.1")
    errors.extend(f"record: {error}" for error in validate_record(record))
    if errors:
        return sorted(set(errors))
    system_of_record = record.get("system_of_record")
    if not is_object(system_of_record) or system_of_record.get("kind") != "generated-synthetic":
        errors.append("record.system_of_record.kind: must be generated-synthetic")
    binding = require_object(graph["record_binding"], context="record_binding")
    if binding["case_id"] != record["case_id"]:
        errors.append("record_binding.case_id: mismatch")
    if type(binding["version"]) is not int or type(record["version"]) is not int:
        errors.append("record_binding.version: must bind positive integers, not booleans or floats")
    if binding["version"] != record["version"]:
        errors.append("record_binding.version: mismatch")
    if binding["fingerprint"] != fingerprint(record):
        errors.append("record_binding.fingerprint: mismatch")
    identifiers = [
        _text(item[key])
        for collection, key in (("nodes", "node_id"), ("edges", "edge_id"))
        for item in object_rows(graph[collection])
    ]
    seen: set[str] = set()
    for identifier in identifiers:
        if identifier in seen:
            errors.append(f"duplicate graph identifier: {identifier}")
        seen.add(identifier)
    errors.extend(_node_errors(graph, record))
    errors.extend(_edge_errors(graph, record))
    errors.extend(_recommendation_errors(graph, record))
    review = graph["review"]
    if is_object(review):
        roles = _index(record, "roles", "role_id")
        if _text(review["reviewer_role_id"]) not in roles:
            errors.append("review: unknown reviewer_role_id")
        if review["graph_fingerprint"] != graph_fingerprint(graph):
            errors.append("review.graph_fingerprint: stale")
    return sorted(set(errors))


def _outcome_paths(graph: JsonObject) -> dict[str, str]:
    outcomes = set(_strings(graph["outcome_node_ids"]))
    edges = object_rows(graph["edges"])

    def reaches_outcome(start: str, *, supported_only: bool) -> bool:
        adjacency: dict[str, set[str]] = {}
        for edge in edges:
            if not supported_only or edge["status"] == "supported":
                adjacency.setdefault(_text(edge["from_node_id"]), set()).add(
                    _text(edge["to_node_id"])
                )
        pending, visited = [start], set[str]()
        while pending:
            node_id = pending.pop()
            if node_id in outcomes:
                return True
            if node_id in visited:
                continue
            visited.add(node_id)
            pending.extend(adjacency.get(node_id, set()) - visited)
        return False

    paths: dict[str, str] = {}
    for node in sorted(object_rows(graph["nodes"]), key=lambda item: _text(item["node_id"])):
        if node["kind"] == "factor":
            node_id = _text(node["node_id"])
            if reaches_outcome(node_id, supported_only=True):
                paths[node_id] = "supported"
            elif reaches_outcome(node_id, supported_only=False):
                paths[node_id] = "hypothesis_or_contested"
            else:
                paths[node_id] = "unconnected"
    return paths


def _inspect_valid(graph: JsonObject, record: JsonObject) -> dict[str, object]:
    paths = _outcome_paths(graph)
    findings = [f"Declared gap: {gap}" for gap in _strings(graph["gaps"])]
    factors = _index(record, "factors", "factor_id")
    actions = _index(record, "actions", "action_id")
    statements = _index(record, "statements", "statement_id")
    for node in object_rows(graph["nodes"]):
        node_id = _text(node["node_id"])
        if node["level_id"] is None:
            findings.append(f"Node {node_id}: level is unassigned; review placement.")
        if node["kind"] == "factor" and factors[_text(node["factor_id"])]["status"] == "candidate":
            findings.append(f"Factor node {node_id}: canonical factor remains candidate.")
    for node_id, status in paths.items():
        if status == "unconnected":
            findings.append(
                f"Factor node {node_id}: no directed path to a declared incident outcome."
            )
        elif status == "hypothesis_or_contested":
            findings.append(
                f"Factor node {node_id}: outcome path includes hypothesis or contested links."
            )
    for edge in object_rows(graph["edges"]):
        edge_id = _text(edge["edge_id"])
        if edge["status"] != "supported":
            findings.append(
                f"Edge {edge_id}: {_text(edge['status'])}; {_text(edge['uncertainty'])}"
            )
        if not edge["evidence_ids"]:
            findings.append(f"Edge {edge_id}: no supporting evidence is recorded.")
    recommendations = object_rows(graph["recommendations"])
    if not recommendations:
        findings.append("No recommendations are linked; review whether system changes are needed.")
    for recommendation in recommendations:
        statement_id = _text(recommendation["statement_id"])
        statement = statements[statement_id]
        if "uncertainty" in statement:
            findings.append(
                f"Recommendation {statement_id}: statement uncertainty: "
                f"{_text(statement['uncertainty']) or 'none recorded'}."
            )
        if not recommendation["action_ids"]:
            findings.append(f"Recommendation {statement_id}: no implementation action is linked.")
        for action_id in _strings(recommendation["action_ids"]):
            action = actions[action_id]
            if action["status"] == "withdrawn":
                findings.append(f"Action {action_id}: linked implementation action is withdrawn.")
            effectiveness = _text(action["effectiveness_state"])
            if effectiveness in {"partly_effective", "ineffective", "harm_detected"}:
                findings.append(
                    f"Action {action_id}: recorded effectiveness_state is {effectiveness}; "
                    "requires review."
                )
    review_state = "declared_review" if graph["review"] is not None else "unreviewed"
    if review_state == "unreviewed":
        findings.append("Map has no declared review.")
    return {
        "structurally_valid": True,
        "errors": [],
        "review_findings": sorted(set(findings)),
        "review_state": review_state,
        "outcome_paths": paths,
    }


def _invalid_inspection(errors: list[str]) -> dict[str, object]:
    return {
        "structurally_valid": False,
        "errors": sorted(set(errors)),
        "review_findings": [],
        "review_state": "unreviewed",
        "outcome_paths": {},
    }


def inspect_accimap(graph: object, record: object) -> dict[str, object]:
    """Report structural validity and review gaps, without claiming causal truth."""
    if errors := validate_accimap(graph, record):
        return _invalid_inspection(errors)
    return _inspect_valid(
        require_object(graph, context="graph"), require_object(record, context="record")
    )


def _mermaid_text(text: str) -> str:
    """Quote both Mermaid syntax and HTML: decoded label text remains HTML-safe.

    Numeric Mermaid entities keep quotes, newlines, directives, brackets and
    backticks out of the diagram grammar. HTML escaping happens first so a later
    entity-decoding/rendering stage cannot turn user text into an HTML element.
    """
    return "".join(
        character
        if character.isascii() and (character.isalnum() or character == " ")
        else f"#{ord(character)};"
        for character in html.escape(text, quote=True)
    )


def _statement_context(statement: JsonObject) -> list[str]:
    provenance = require_object(statement["provenance"], context="statement provenance")
    parts = [
        f"source {_text(provenance['source_id'])}",
        f"statement review_state {_text(provenance['review_state'])}",
    ]
    if "uncertainty" in statement:
        parts.append(f"statement uncertainty: {_text(statement['uncertainty']) or 'none recorded'}")
    return parts


def _node_label(
    node: JsonObject, statements: dict[str, JsonObject], factors: dict[str, JsonObject]
) -> str:
    statement = statements[_text(node["statement_id"])]
    parts = [
        f"{_text(node['node_id'])}: {_text(statement['text'])}",
        f"statement {_text(node['statement_id'])}; kind {_text(statement['kind'])}",
        f"node role {_text(node['kind'])}",
    ]
    parts.extend(_statement_context(statement))
    if node["kind"] == "factor":
        factor_id = _text(node["factor_id"])
        parts.append(f"factor {factor_id}: {_text(factors[factor_id]['status'])}")
    parts.append(f"placement: {_text(node['placement_rationale'])}")
    return _mermaid_text("; ".join(parts))


def render_mermaid(graph: object, record: object) -> str:
    """Render a bounded, deterministic synthetic draft; raise ValueError on failure.

    All graph relationships remain explicit input. There is no derivation of
    causal edges from canonical `supports` relationships, no link repair and no
    graph acyclicity assumption. Empty profile levels are omitted from drawing.
    """
    if errors := validate_accimap(graph, record):
        raise ValueError("invalid AcciMap: " + "; ".join(errors))
    value = require_object(graph, context="graph")
    canonical_record = require_object(record, context="record")
    inspection = _inspect_valid(value, canonical_record)
    lines: list[str] = []
    output_bytes = 0

    def emit(line: str) -> None:
        nonlocal output_bytes
        output_bytes += len(line.encode("utf-8")) + 1
        if output_bytes > MAX_RENDER_BYTES:
            raise ValueError("rendered output exceeds 8 MiB; no diagram emitted")
        lines.append(line)

    emit("%% DRAFT: generated-synthetic-only; structural checks do not prove causation.")
    emit("%% Synthetic declarations are metadata, not privacy or source-truth proof.")
    emit("%% Declared review is not authenticated human or organisational approval.")
    emit(f"%% Record fingerprint: {fingerprint(canonical_record)}")
    emit(f"%% Graph fingerprint: {graph_fingerprint(value)}")
    emit("flowchart TB")
    caption = (
        "DRAFT SYNTHETIC ACCIMAP; structural checks only; no causal or organisational approval; "
        f"canonical case status: {_text(canonical_record['state'])}; "
        f"profile {_text(value['profile_id'])}; question: {_text(value['question'])}; "
        f"review: {_text(inspection['review_state'])}"
    )
    emit(f'  context_note["{_mermaid_text(caption)}"]')
    nodes = sorted(object_rows(value["nodes"]), key=lambda item: _text(item["node_id"]))
    node_names = {_text(node["node_id"]): f"n{index}" for index, node in enumerate(nodes)}
    statements = _index(canonical_record, "statements", "statement_id")
    factors = _index(canonical_record, "factors", "factor_id")
    actions = _index(canonical_record, "actions", "action_id")
    levels: list[tuple[str | None, str]] = list(PROFILES[_text(value["profile_id"])])
    if any(node["level_id"] is None for node in nodes):
        levels.append((None, "Unassigned level - requires review"))
    for index, (level_id, label) in enumerate(levels):
        grouped = [node for node in nodes if node["level_id"] == level_id]
        if not grouped:
            continue
        emit(f'  subgraph level_{index}["{_mermaid_text(label)}"]')
        for node in grouped:
            name = node_names[_text(node["node_id"])]
            emit(f'    {name}["{_node_label(node, statements, factors)}"]')
        emit("  end")
    for edge in sorted(object_rows(value["edges"]), key=lambda item: _text(item["edge_id"])):
        label = (
            f"{_text(edge['edge_id'])}; {_text(edge['relation'])}; status {_text(edge['status'])}; "
            f"evidence: {', '.join(_strings(edge['evidence_ids'])) or 'none recorded'}; "
            f"conflicting evidence: {', '.join(_strings(edge['conflicting_evidence_ids'])) or 'none recorded'}; "
            f"rationale: {_text(edge['rationale'])}; uncertainty: {_text(edge['uncertainty']) or 'none recorded'}"
        )
        arrow = "-->" if edge["status"] == "supported" else "-.->"
        source = node_names[_text(edge["from_node_id"])]
        target = node_names[_text(edge["to_node_id"])]
        emit(f'  {source} {arrow}|"{_mermaid_text(label)}"| {target}')
    for index, recommendation in enumerate(
        sorted(object_rows(value["recommendations"]), key=lambda item: _text(item["statement_id"]))
    ):
        statement_id = _text(recommendation["statement_id"])
        statement = statements[statement_id]
        parts = [
            f"Recommendation {statement_id}: {_text(statement['text'])}",
            f"statement kind {_text(statement['kind'])}",
            *_statement_context(statement),
            f"mechanism: {_text(recommendation['mechanism'])}",
            f"target nodes: {', '.join(_strings(recommendation['target_node_ids'])) or 'none'}",
            f"target edges: {', '.join(_strings(recommendation['target_edge_ids'])) or 'none'}",
        ]
        for action_id in sorted(_strings(recommendation["action_ids"])):
            action = actions[action_id]
            parts.append(
                f"action {action_id}: status {_text(action['status'])}; "
                f"recorded effectiveness_state {_text(action['effectiveness_state'])}"
            )
        if not recommendation["action_ids"]:
            parts.append("actions: none linked")
        parts.append("action completion does not establish effectiveness")
        emit(f'  recommendation_{index}["{_mermaid_text("; ".join(parts))}"]')
    review = value["review"]
    if is_object(review):
        label = (
            f"Declared review: {_text(review['disposition'])}; reviewer role {_text(review['reviewer_role_id'])}; "
            f"at {_text(review['reviewed_at'])}; rationale: {_text(review['rationale'])}; "
            "declaration is not authenticated human or organisational approval"
        )
        emit(f'  review_note["{_mermaid_text(label)}"]')
    for index, finding in enumerate(_strings(inspection["review_findings"])):
        emit(f'  finding_{index}["{_mermaid_text(finding)}"]')
    return "\n".join(lines) + "\n"


def _unique_object(pairs: list[tuple[str, object]]) -> JsonObject:
    result: JsonObject = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON number: {value}")


def _read_json(path: Path) -> object:
    if not path.is_file():
        raise ValueError("input must be a readable regular file")
    with path.open("rb") as stream:
        payload = stream.read(MAX_INPUT_BYTES + 1)
    if len(payload) > MAX_INPUT_BYTES:
        raise ValueError("input file exceeds 2 MiB")
    value: object = json.loads(
        payload.decode("utf-8"), object_pairs_hook=_unique_object, parse_constant=_reject_constant
    )
    if errors := _json_errors(value, "input"):
        raise ValueError("; ".join(errors))
    return value


def main(argv: Sequence[str] | None = None) -> int:
    """Validate or render supplied synthetic files; never write or contact a service."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "render"))
    parser.add_argument("graph", help="AcciMap companion JSON file")
    parser.add_argument(
        "--record", required=True, help="Bound canonical synthetic safety-work JSON"
    )
    args = parser.parse_args(argv)
    command: object = args.command
    graph_path: object = args.graph
    record_path: object = args.record
    try:
        graph = _read_json(Path(_text(graph_path)))
        record = _read_json(Path(_text(record_path)))
        if command == "render":
            output = render_mermaid(graph, record)
            print(output, end="")
            return 0
        inspection = inspect_accimap(graph, record)
    except (OSError, ValueError, RecursionError) as error:
        inspection = _invalid_inspection([f"input/render: {error}"])
    print(
        json.dumps(inspection, sort_keys=True),
        file=sys.stderr if command == "render" else sys.stdout,
    )
    return 0 if inspection["structurally_valid"] is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
