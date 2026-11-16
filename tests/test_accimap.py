"""Independent contract examples for the synthetic AcciMap companion."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from copy import deepcopy
from hashlib import sha256
from html import unescape
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tools.accimap import (
    graph_fingerprint,
    inspect_accimap,
    render_mermaid,
    validate_accimap,
)
from tools.evidence_core import validate_record
from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests/fixtures/accimap"


def _load(path: Path) -> JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    return require_object(value, context="test fixture")


def _fixture() -> tuple[JsonObject, JsonObject]:
    return _load(FIXTURES / "graph.json"), _load(FIXTURES / "record.json")


def _fingerprint(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    return "sha256:" + sha256(raw).hexdigest()


def _rebind(graph: JsonObject, record: JsonObject) -> None:
    graph["record_binding"] = {
        "case_id": record["case_id"],
        "version": record["version"],
        "fingerprint": _fingerprint(record),
    }


def _set(document: JsonObject, path: tuple[str | int, ...], value: object) -> None:
    current: object = document
    for part in path[:-1]:
        if is_object(current):
            assert isinstance(part, str)
            current = current[part]
        else:
            assert is_array(current)
            assert isinstance(part, int)
            current = current[part]
    last = path[-1]
    if is_object(current):
        assert isinstance(last, str)
        current[last] = value
    else:
        assert is_array(current)
        assert isinstance(last, int)
        current[last] = value


def _row(document: JsonObject, collection: str, index: int = 0) -> JsonObject:
    return object_rows(document[collection])[index]


def _text_view(mermaid: str) -> str:
    # Decode the documented Mermaid numeric entity syntax for display assertions.
    return unescape(re.sub(r"#([0-9]+);", lambda match: chr(int(match.group(1))), mermaid))


def _cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tools.accimap", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )


def test_literal_fixture_paths_and_fingerprints() -> None:
    graph, record = _fixture()
    expected = _load(FIXTURES / "expected.json")
    assert validate_record(record) == []
    assert validate_accimap(graph, record) == []
    actual = inspect_accimap(graph, record)
    for field in ("structurally_valid", "review_state", "outcome_paths"):
        assert actual[field] == expected[field]
    assert _fingerprint(record) == expected["record_fingerprint"]
    assert graph_fingerprint(graph) == expected["graph_fingerprint_without_review"]
    assert graph_fingerprint(graph) == _fingerprint(
        {key: value for key, value in graph.items() if key != "review"}
    )


def test_render_preserves_uncertainty_evidence_and_draft_state_without_mutation() -> None:
    graph, record = _fixture()
    before = deepcopy((graph, record))
    rendered = render_mermaid(graph, record)
    assert render_mermaid(graph, record) == rendered
    assert (graph, record) == before
    text = _text_view(rendered)
    for term in (
        "hypothesis",
        "contested",
        "evidence-conflict",
        "evidence-availability",
        "edge-policy-outcome",
        "Simulation accounts conflict; timing is unresolved.",
        "unassigned",
        "candidate",
        "No simulation timestamp establishes the hypothesised direct pathway.",
    ):
        assert term in text
    assert "draft" in text.lower()
    assert "synthetic" in text.lower()
    assert "-.->" in rendered or "-. " in rendered


@pytest.mark.parametrize(
    ("path", "value", "fragment"),
    [
        (("schema_version",), "accimap-9.0", "schema_version"),
        (("dataset",), "real-clinical-data", "dataset"),
        (("profile_id",), "invented-profile", "profile_id"),
        (("question",), "   ", "question"),
        (("record_binding", "case_id"), "case-other", "record_binding.case_id"),
        (("record_binding", "version"), 2, "record_binding.version"),
        (("record_binding", "version"), True, "version"),
        (("record_binding", "fingerprint"), "sha256:" + "0" * 64, "fingerprint"),
        (("nodes", 0, "level_id"), "invented-level", "graph.nodes.0.level_id"),
        (("nodes", 0, "statement_id"), "evidence-policy", "unknown statement_id"),
        (("nodes", 0, "factor_id"), "statement-policy", "unknown factor_id"),
        (("nodes", 0, "statement_id"), "statement-queue", "factor statement_id mismatch"),
        (("nodes", 0, "placement_rationale"), "\t", "placement_rationale"),
        (("nodes", 1, "node_id"), "node-policy", "duplicate graph identifier"),
        (("edges", 0, "edge_id"), "node-policy", "duplicate graph identifier"),
        (("outcome_node_ids",), ["node-policy"], "outcome_node_ids"),
        (("edges", 0, "from_node_id"), "factor-policy", "unknown node endpoint"),
        (("edges", 0, "to_node_id"), "node-policy", "self-link"),
        (("edges", 0, "relation"), "supports", "relation"),
        (("edges", 0, "evidence_ids"), [], "evidence_ids"),
        (("edges", 0, "evidence_ids"), ["source-policy"], "unknown evidence_id"),
        (("edges", 0, "evidence_ids"), ["evidence-policy", "evidence-policy"], "evidence_ids"),
        (
            ("edges", 0, "conflicting_evidence_ids"),
            ["evidence-conflict"],
            "conflicting_evidence_ids",
        ),
        (("edges", 2, "uncertainty"), " ", "uncertainty"),
        (("edges", 3, "conflicting_evidence_ids"), ["evidence-availability"], "overlap"),
        (("recommendations", 0, "statement_id"), "statement-policy", "recommendation"),
        (("recommendations", 0, "target_node_ids"), ["factor-policy"], "unknown target_node_id"),
        (("recommendations", 0, "target_edge_ids"), ["edge-missing"], "unknown target_edge_id"),
        (("recommendations", 0, "action_ids"), ["role-owner"], "unknown action_id"),
    ],
)
def test_graph_boundary_rejections(
    path: tuple[str | int, ...], value: object, fragment: str
) -> None:
    graph, record = _fixture()
    _set(graph, path, value)
    errors = validate_accimap(graph, record)
    assert errors == sorted(errors)
    assert any(fragment in error for error in errors), errors
    inspection = inspect_accimap(graph, record)
    assert inspection["structurally_valid"] is False
    assert inspection["outcome_paths"] == {}
    with pytest.raises(ValueError, match=r"(?i)invalid"):
        render_mermaid(graph, record)


@pytest.mark.parametrize(
    ("path", "value", "fragment"),
    [
        (("schema_version",), "1.0", "record.schema_version: must be 1.1"),
        (("system_of_record", "kind"), "clinical-system", "generated-synthetic"),
        (("factors", 0, "status"), "withdrawn", "rejected or withdrawn"),
        (("factors", 0, "status"), "rejected", "rejected or withdrawn"),
        (("statements", 0, "withdrawn"), True, "rejected or withdrawn"),
        (("statements", 0, "provenance", "review_state"), "rejected", "rejected or withdrawn"),
        (("evidence", 0, "custody_state"), "withdrawn", "withdrawn evidence"),
        (("sources", 0, "screening_state"), "excluded", "excluded source"),
        (("actions", 0, "recommendation_id"), "statement-policy", "recommendation"),
    ],
)
def test_canonical_boundary_rejections_after_explicit_rebinding(
    path: tuple[str | int, ...], value: object, fragment: str
) -> None:
    graph, record = _fixture()
    _set(record, path, value)
    _rebind(graph, record)
    errors = validate_accimap(graph, record)
    assert any(fragment in error for error in errors), errors


def test_legacy_unresolved_provenance_cannot_bypass_companion_admission() -> None:
    graph, record = _fixture()
    record["schema_version"] = "1.0"
    _set(record, ("statements", 4, "provenance", "source_id"), "external-source-absent")
    _rebind(graph, record)
    # The shared validator deliberately supports legacy external provenance.
    assert validate_record(record) == []
    assert any("must be 1.1" in error for error in validate_accimap(graph, record))
    assert inspect_accimap(graph, record)["structurally_valid"] is False
    with pytest.raises(ValueError, match=r"must be 1\.1"):
        render_mermaid(graph, record)


@pytest.mark.parametrize(
    ("statement_index", "error_prefix"), [(4, "nodes."), (5, "recommendations.")]
)
def test_excluded_statement_provenance_is_checked_without_an_edge_reference(
    statement_index: int, error_prefix: str
) -> None:
    graph, record = _fixture()
    excluded_source = deepcopy(_row(record, "sources", 5))
    excluded_source["source_id"] = "source-excluded-provenance-only"
    excluded_source["screening_state"] = "excluded"
    record["sources"] = [*object_rows(record["sources"]), excluded_source]
    _set(
        record,
        ("statements", statement_index, "provenance", "source_id"),
        excluded_source["source_id"],
    )
    _rebind(graph, record)
    assert validate_record(record) == []
    errors = validate_accimap(graph, record)
    assert any(error.startswith(error_prefix) and "excluded" in error for error in errors)
    with pytest.raises(ValueError, match="excluded"):
        render_mermaid(graph, record)


def test_recommendation_uncertainty_survives_inspection_and_rendering() -> None:
    graph, record = _fixture()
    uncertainty = (
        "SYNTHETIC REVIEW NOTE: proposed routing may worsen escalation delays under saturation."
    )
    _set(record, ("statements", 5, "uncertainty"), uncertainty)
    _rebind(graph, record)
    assert validate_accimap(graph, record) == []
    assert uncertainty in str(inspect_accimap(graph, record)["review_findings"])
    assert uncertainty in _text_view(render_mermaid(graph, record))


def test_diagram_preserves_case_provenance_and_action_effectiveness_state() -> None:
    graph, record = _fixture()
    record["state"] = "withdrawn"
    _set(record, ("events", 0, "to_state"), "withdrawn")
    _set(record, ("events", 0, "event_type"), "case_withdrawn")
    _set(record, ("statements", 0, "provenance", "review_state"), "unreviewed")
    _set(record, ("actions", 0, "status"), "withdrawn")
    _set(record, ("actions", 0, "effectiveness_state"), "harm_detected")
    _rebind(graph, record)
    assert validate_accimap(graph, record) == []
    rendered = _text_view(render_mermaid(graph, record))
    for term in ("withdrawn", "source-policy", "unreviewed", "action-fallback", "harm_detected"):
        assert term in rendered


def test_changed_record_invalidates_binding_even_with_unchanged_case_and_version() -> None:
    graph, record = _fixture()
    _set(record, ("statements", 0, "text"), "Changed synthetic evidence interpretation.")
    assert any("fingerprint: mismatch" in error for error in validate_accimap(graph, record))


def test_declared_review_is_bound_to_exact_current_graph() -> None:
    graph, record = _fixture()
    graph["review"] = {
        "reviewer_role_id": "role-reviewer",
        "reviewed_at": "2026-11-16T00:30:00Z",
        "disposition": "reviewed_with_gaps",
        "graph_fingerprint": _fingerprint(
            {key: value for key, value in graph.items() if key != "review"}
        ),
        "rationale": "Synthetic reviewer declaration; unresolved gaps remain.",
    }
    inspection = inspect_accimap(graph, record)
    assert inspection["structurally_valid"] is True
    assert inspection["review_state"] == "declared_review"
    assert inspection["review_findings"]
    assert "synthetic" in _text_view(render_mermaid(graph, record)).lower()
    graph["question"] = "A changed investigation question."
    assert any("stale" in error for error in validate_accimap(graph, record))
    _set(graph, ("review", "reviewer_role_id"), "role-unknown")
    assert any("unknown reviewer_role_id" in error for error in validate_accimap(graph, record))


def test_missing_recommendations_and_hypotheses_remain_valid_unreviewed_draft() -> None:
    graph, record = _fixture()
    graph["recommendations"] = []
    actual = inspect_accimap(graph, record)
    assert actual["structurally_valid"] is True
    assert actual["review_state"] == "unreviewed"
    findings = str(actual["review_findings"]).lower()
    assert "recommendation" in findings
    assert "hypothesis" in findings
    _row(graph, "edges")["status"] = "hypothesis"
    _row(graph, "edges")["uncertainty"] = "Evidence does not establish this interpretation."
    assert (
        require_object(inspect_accimap(graph, record)["outcome_paths"], context="paths")[
            "node-policy"
        ]
        == "hypothesis_or_contested"
    )


def test_original_profile_does_not_force_outcome_into_equipment() -> None:
    graph, record = _fixture()
    graph["profile_id"] = "rasmussen-svedung-six-v1"
    mapping = {
        "management": "company_management",
        "environment": "equipment",
        "staff": "processes",
        "patient": "processes",
    }
    for node in object_rows(graph["nodes"]):
        level = node["level_id"]
        if isinstance(level, str):
            node["level_id"] = mapping[level]
    assert validate_accimap(graph, record) == []
    assert (
        inspect_accimap(graph, record)["outcome_paths"]
        == _load(FIXTURES / "expected.json")["outcome_paths"]
    )
    rendered = _text_view(render_mermaid(graph, record))
    assert "Equipment" in rendered or "equipment" in rendered


def test_multiple_outcomes_skipped_levels_same_level_and_cycles() -> None:
    graph, record = _fixture()
    nodes = object_rows(graph["nodes"])
    outcome = deepcopy(nodes[-1])
    outcome["node_id"] = "node-second-outcome"
    outcome["level_id"] = "environment"
    graph["nodes"] = [*nodes, outcome]
    graph["outcome_node_ids"] = ["node-outcome", "node-second-outcome"]
    edges = object_rows(graph["edges"])
    for identifier, start, end in (
        ("edge-consequence", "node-outcome", "node-second-outcome"),
        ("edge-same-level", "node-queue", "node-second-outcome"),
        ("edge-feedback", "node-queue", "node-policy"),
    ):
        edges.append(
            {**deepcopy(edges[0]), "edge_id": identifier, "from_node_id": start, "to_node_id": end}
        )
    graph["edges"] = edges
    assert validate_accimap(graph, record) == []
    assert (
        require_object(inspect_accimap(graph, record)["outcome_paths"], context="paths")[
            "node-policy"
        ]
        == "supported"
    )


@pytest.mark.parametrize(
    "value", [None, True, 7, [], {"wrong": "shape"}, float("nan"), float("inf")]
)
def test_malformed_root_inputs_fail_without_unexpected_exceptions(value: object) -> None:
    graph, record = _fixture()
    assert validate_accimap(value, record)
    assert validate_accimap(graph, value)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "\ud800", object()])
def test_non_json_and_invalid_unicode_fail_before_rendering(value: object) -> None:
    graph, record = _fixture()
    graph["question"] = value
    assert validate_accimap(graph, record)
    with pytest.raises(ValueError, match=r"(?i)invalid"):
        render_mermaid(graph, record)


@pytest.mark.parametrize(
    ("case", "diagnostic"),
    [
        ("cycle", "cyclic JSON container"),
        ("depth", "JSON nesting exceeds 64 levels"),
        ("count", "too many JSON values"),
        ("bytes", "canonical JSON exceeds 2 MiB"),
    ],
)
def test_api_resource_limits_reject_before_schema_or_render(case: str, diagnostic: str) -> None:
    graph, record = _fixture()
    if case == "cycle":
        graph["question"] = graph
    elif case == "depth":
        nested: object = "leaf"
        for _ in range(65):
            nested = [nested]
        graph["question"] = nested
    elif case == "count":
        graph["gaps"] = [""] * 100_001
    else:
        graph["question"] = "x" * (2 * 1024 * 1024)
    assert validate_accimap(graph, record) == [f"graph: {diagnostic}"]
    with pytest.raises(ValueError, match=re.escape(diagnostic)):
        render_mermaid(graph, record)


@pytest.mark.parametrize(("collection", "count"), [("nodes", 129), ("edges", 257)])
def test_graph_cardinality_limits(collection: str, count: int) -> None:
    graph, record = _fixture()
    graph[collection] = [deepcopy(_row(graph, collection)) for _ in range(count)]
    errors = validate_accimap(graph, record)
    assert any(error.startswith(f"graph.{collection}:") and "too long" in error for error in errors)


def test_render_expansion_limit_rejects_without_returning_partial_diagram() -> None:
    graph, record = _fixture()
    _set(record, ("statements", 0, "text"), "Synthetic " + "x" * 100_000)
    nodes = object_rows(graph["nodes"])
    exemplar = deepcopy(nodes[0])
    for index in range(128 - len(nodes)):
        nodes.append({**deepcopy(exemplar), "node_id": f"node-repeat-{index}"})
    graph["nodes"] = nodes
    _rebind(graph, record)
    assert validate_accimap(graph, record) == []
    with pytest.raises(ValueError, match="rendered output exceeds 8 MiB; no diagram emitted"):
        render_mermaid(graph, record)


def test_renderer_cannot_interpret_hostile_statement_or_gap_as_syntax() -> None:
    graph, record = _fixture()
    hostile = '"]\nclick n0 "javascript:alert(1)"\n%%{init: {"securityLevel":"loose"}}%%\n<script>x</script>`'
    _set(record, ("statements", 0, "text"), hostile)
    graph["gaps"] = [hostile]
    _rebind(graph, record)
    rendered = render_mermaid(graph, record)
    for forbidden in ("\nclick ", "javascript:", "<script>", "%%{", 'securityLevel":"loose'):
        assert forbidden not in rendered
    assert "javascript:alert(1)" in _text_view(rendered)


@given(st.text(alphabet=st.characters(exclude_categories=("Cs",)), min_size=1, max_size=80))
def test_label_changes_preserve_topology_and_inputs(text: str) -> None:
    graph, record = _fixture()
    _set(record, ("statements", 0, "text"), "Synthetic label: " + text)
    _rebind(graph, record)
    before = deepcopy((graph, record))
    assert (
        inspect_accimap(graph, record)["outcome_paths"]
        == _load(FIXTURES / "expected.json")["outcome_paths"]
    )
    assert (graph, record) == before


@given(st.text(alphabet=st.characters(exclude_categories=("Cs",)), min_size=1, max_size=80))
def test_label_rendering_preserves_text_and_inputs(text: str) -> None:
    graph, record = _fixture()
    label = "Synthetic label: " + text
    _set(record, ("statements", 0, "text"), label)
    _rebind(graph, record)
    before = deepcopy((graph, record))
    rendered = render_mermaid(graph, record)
    assert label in _text_view(rendered)
    assert (graph, record) == before


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789", min_size=1, max_size=20))
def test_unresolved_evidence_never_produces_a_valid_graph(suffix: str) -> None:
    graph, record = _fixture()
    _set(graph, ("edges", 0, "evidence_ids"), ["missing-" + suffix])
    inspection = inspect_accimap(graph, record)
    assert "unknown evidence_id" in str(inspection["errors"])
    assert inspection["structurally_valid"] is False


def test_legacy_record_and_template_remain_compatible() -> None:
    legacy = _load(ROOT / "tests/fixtures/safety-work/valid-case.json")
    before = deepcopy(legacy)
    assert validate_record(legacy) == []
    assert legacy == before
    template = ROOT / "skills/rca-investigation/assets/templates/mermaid/accimap-levels.mmd"
    assert (
        sha256(template.read_bytes()).hexdigest()
        == "fce5ec864d2797d5caf7a42c26bf48442c0051df980954d8bf9ec264e494e82b"
    )


def test_actual_cli_validates_and_renders_repeatable_bytes() -> None:
    graph = str(FIXTURES / "graph.json")
    record = str(FIXTURES / "record.json")
    validation = _cli("validate", graph, "--record", record)
    assert validation.returncode == 0, validation.stderr
    result: object = json.loads(validation.stdout)
    assert require_object(result, context="CLI result")["structurally_valid"] is True
    first = _cli("render", graph, "--record", record)
    second = _cli("render", graph, "--record", record)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert re.search(r"^flowchart (?:TD|TB)$", first.stdout, re.MULTILINE)


@pytest.mark.parametrize("malformation", ["duplicate", "nonfinite", "syntax", "oversize"])
def test_cli_rejects_ambiguous_or_invalid_json(tmp_path: Path, malformation: str) -> None:
    text = (FIXTURES / "graph.json").read_text(encoding="utf-8")
    if malformation == "duplicate":
        text = '{"question":"duplicate",' + text[1:]
    elif malformation == "nonfinite":
        text = text.replace('"review": null', '"review": NaN')
    elif malformation == "syntax":
        text = "{"
    else:
        text = " " * (2 * 1024 * 1024 + 1)
    path = tmp_path / "invalid.json"
    path.write_text(text, encoding="utf-8")
    result = _cli("render", str(path), "--record", str(FIXTURES / "record.json"))
    assert result.returncode == 2
    assert "flowchart" not in result.stdout
    assert "Traceback" not in result.stderr


def test_cli_invalid_graph_missing_file_and_unknown_argument_fail(tmp_path: Path) -> None:
    graph, _record = _fixture()
    graph["profile_id"] = "unknown"
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(graph), encoding="utf-8")
    validation = _cli("validate", str(path), "--record", str(FIXTURES / "record.json"))
    assert validation.returncode == 2
    result: object = json.loads(validation.stdout)
    assert require_object(result, context="CLI result")["structurally_valid"] is False
    missing = _cli(
        "validate", str(tmp_path / "missing.json"), "--record", str(FIXTURES / "record.json")
    )
    assert missing.returncode == 2
    assert "Traceback" not in missing.stderr
    assert _cli("--unsupported").returncode == 2
