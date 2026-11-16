# AcciMap specification

## Problem and intended outcome

At master `c6892497aa0b03555d5145242c04965471eccc1d`, rcagent has an AcciMap
method guide, a six-level healthcare Mermaid template, shared investigation and
action workflows, and executable method selection. It lacks a dedicated
record-to-diagram contract. Its guide also presents a particular healthcare
adaptation as six universal levels and compresses facilitation into five steps.

The user authorised incorporating the review recommendations into Conductor and
implementing feasible changes on 16 November 2026. Deliver a small companion to
the existing evidence record, a clearer portable method guide and synthetic
qualification. The users are investigation facilitators and repository
maintainers; an approved incident-management system remains the system of record.

## Requirements

1. Name the existing `rcagent-healthcare-six-v1` adaptation; preserve its existing
   template and labels. Provide `rasmussen-svedung-six-v1` as a separately named
   original hierarchy. Outcome is a node role, not an assumed bottom level.
2. Document scope/outcomes, evidence, factor consolidation, placement, links,
   gaps, causal-logic review, recommendations, human validation and effectiveness.
3. Bind every graph to one exact canonical record case, version and fingerprint.
   Reuse its factors, statements, evidence, roles and actions. Do not change the
   safety-work schema or turn its evidential `supports` relation into causation.
4. Preserve supported, hypothetical and contested contributory relationships,
   uncertainty and conflicting evidence. A valid incomplete draft stays a draft.
5. Check typed references, inactive material, duplicates, invalid levels,
   unsupported affirmative links and stale declared-review fingerprints.
6. Render deterministic Mermaid with safe internal identifiers and escaped text.
   Retain uncertainty, gaps, evidence references and declared review limits.
7. Exercise positive/negative controls, graph properties, the actual CLI, legacy
   compatibility and unmodified shared evidence/interface regressions.

## Implementation boundary

The implementation is a reversible, synthetic-only adapter using the current
Python, jsonschema, pytest, Hypothesis and Mermaid stack. It adds no dependency,
network access, model call, enterprise connector, private case or release.
Structural validation does not establish source truth, causal validity, review
authenticity, effectiveness, clinical safety or institutional approval.

Only these paths belong to this increment:

- `tools/accimap.py`
- `evaluation/accimap/**`
- `tests/test_accimap.py` and `tests/fixtures/accimap/**`
- `skills/rca-investigation/references/methods/accimap.md`
- `conductor/tracks/accimap-workflow_20261116/**`

Do not edit the D0 production/oracle paths, `tools/workbench.py`, shared evidence
core/schema, CI, manifests, locks, baselines, historical studies or other tracks.
Shared registry/roadmap changes go to the coordinator as an explicit proposal.

## Acceptance and dependencies

| Gate | Acceptance evidence |
|---|---|
| AM01 Method | Named profiles, source attribution, full facilitation and uncertainty guidance; independent methodology review |
| AM02 Contract | Machine-readable companion schema and executable reference/version binding; valid legacy record remains unchanged |
| AM03 Rendering | Actual CLI output; multiple paths/outcomes, skipped levels, unassigned factors and contested edges preserved; injection controls |
| AM04 Qualification | Synthetic example, discriminating negative/property tests, strict zero-debt typing, lint/security and existing regressions |
| AM05 Integration | Current exact-head hosted checks and coordinator acceptance; shared registry reconciliation before integrated-completion claim |

AM01–AM04 consume existing accepted evidence-core interfaces from master; they
do not depend on unfinished D0 extraction or its independent oracle. AM05 belongs
to the coordinator. Integration with future extraction/model studies consumes
their separately accepted outputs and remains pending.

## Risks, safeguards and rollback

- A graph can look more certain than its evidence: show claim kinds, link status,
  conflicts and gaps; never infer a supported link from layout/reachability.
- Typed review metadata can be forged: bind it to current bytes, label it a
  declared review and retain external human authority.
- Input text can inject diagram syntax: use generated identifiers and entity
  encoding; exercise hostile labels through the renderer.
- Parallel work can conflict: own only the paths above and retain the sole
  coordinator's merge authority. Fresh reconciliation precedes publication.

Rollback is a normal revert of this scoped change. No canonical-record migration
or historical-evidence rewrite is required. Replacing the adapter later must
preserve the versioned JSON contract, fixtures and unresolved evidence states.
