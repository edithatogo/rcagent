# AcciMap companion contract 1.0

## Record and profile

The graph is a companion to a valid canonical safety-work 1.1 record. It does
not modify or migrate that record. `schema_version` is `accimap-1.0`, `dataset`
is `generated-synthetic-only`, and the canonical `system_of_record.kind` must be
`generated-synthetic`. These are declarations, not automatic privacy detection.

`record_binding` contains the exact `case_id`, positive integer `version` and
canonical record `fingerprint`. Reject case/version/hash mismatch; do not repair
it silently. Use the existing evidence-core canonical serialization/fingerprint.
The binding detects a changed supplied record, not the truth of its contents or
the validity of source hashes inside it. D0 source-byte qualification is separate.

`profile_id` selects an immutable level vocabulary, in top-to-bottom order:

| Profile | Levels |
|---|---|
| `rcagent-healthcare-six-v1` | `government`, `regulators`, `management`, `environment`, `staff`, `patient` |
| `rasmussen-svedung-six-v1` | `government`, `regulators`, `company_management`, `operational_management`, `processes`, `equipment` |

The first names the existing repository adaptation without changing its legacy
Mermaid bytes. The second follows the original hierarchy. Outcome is a node role
independent of level; it is not forced into equipment/surroundings. Unknown
profiles/level identifiers reject. Null `level_id` means unassigned and produces
a visible review finding; it is not another methodological level.

## Nodes and links

Each node has `node_id`, `kind` (`factor` or `outcome`), `statement_id`,
`level_id`, and nonempty `placement_rationale`. Factor nodes also require
`factor_id`; the canonical factor must refer to the same statement. Outcome
nodes refer to incident-outcome statements, not the canonical record's learning
or effectiveness `outcomes`. Rejected/withdrawn statements and factors cannot
be admitted; represented statements must resolve to non-excluded provenance
sources. A withdrawn whole record may be inspected as historical synthetic
material, with its canonical case state visible in the diagram.
The nonempty `outcome_node_ids` list identifies exactly the outcome nodes.

Each edge has `edge_id`, `from_node_id`, `to_node_id`,
`relation=contributes_to`, `status`, `rationale`, `evidence_ids`,
`conflicting_evidence_ids`, and `uncertainty`. These are analyst-declared
contributory relationships, separate from evidential `supports`/`contradicts`.

| Status | Structural requirement | Presentation |
|---|---|---|
| `supported` | Nonempty valid evidence references; no declared conflicting evidence | Solid connection with explicit status and evidence IDs |
| `hypothesis` | Nonempty uncertainty; supporting evidence may be absent | Dotted connection with uncertainty and an evidence-gap finding when needed |
| `contested` | Nonempty uncertainty explaining the objection; retain any conflicting evidence references | Dotted connection with explicit contested status and conflicts |

All endpoints resolve to the correct entity types. Supporting and conflicting
references are unique, disjoint and resolve to active evidence. Node/edge IDs
are globally unique; reject self-links. Permit multiple paths, skipped levels,
same-level links and outcome-to-outcome links. Cycles across distinct nodes are
not silently deleted; traversal must terminate. Layout and reachability cannot
prove causation, necessity, sufficiency, completeness or preventability.

## Recommendations, gaps and declared review

Recommendations contain a canonical recommendation `statement_id`,
`target_node_ids`, `target_edge_ids`, `mechanism`, and `action_ids`. At least one
target must resolve. Actions must refer to that recommendation. Empty actions
or recommendations remain visible planning gaps; neither implies approval or
effectiveness. Recommendation-specific uncertainty remains in inspection and
rendered output. The diagram shows statement source IDs and review states, plus
linked action status/effectiveness state; the complete canonical record remains
the provenance/action record. Free-text `gaps` remain in inspection and diagram.

`review` is null or a declaration containing `reviewer_role_id`, `reviewed_at`,
`disposition` (`reviewed` or `reviewed_with_gaps`), `graph_fingerprint` and
`rationale`. The fingerprint covers the complete graph except `review`, including
the canonical-record binding. Any change invalidates the prior declaration.
The reviewer must resolve to a record role, but a typed identity/timestamp does
not authenticate the person or establish organisational approval. Every rendered
output retains a draft/synthetic structural-only caption.

## Public seams and failure behaviour

- `validate_accimap(graph, record)` returns a sorted list of errors; an empty
  list establishes structural validity only.
- `inspect_accimap(graph, record)` reports structural validity, errors, review
  findings, declared-review state and per-factor outcome reachability.
- `graph_fingerprint(graph)` binds a review to the graph excluding its `review`.
- `render_mermaid(graph, record)` validates before emitting any graph and raises
  `ValueError` on invalid input. Output is deterministic for identical inputs.
- `python -m tools.accimap validate GRAPH --record RECORD` prints inspection JSON;
  `render` prints Mermaid. Invalid input exits nonzero. No file is written by
  either command.

Reject non-JSON values, nonfinite numbers, invalid Unicode and duplicate JSON
keys. Bound file input to 2 MiB and rendered output to 8 MiB; graph arrays to 128
nodes and 256 edges. Reject oversized output rather than truncating it. Reject
unknown object fields rather than silently accepting a misspelled assertion.
Use safe internal diagram identifiers and encode user-controlled labels so
Mermaid directives, HTML and executable links cannot be introduced as syntax.
The canonical record/graph remain unchanged after validation and rendering.

## Qualification boundary

Fixtures use only generated synthetic cases, records and reviewers. Tests must
distinguish structurally valid drafts from errors and from unproven causal
claims. A declared review, graph path, successful parser, rendered diagram or
passing software suite does not confer scientific or clinical qualification.
