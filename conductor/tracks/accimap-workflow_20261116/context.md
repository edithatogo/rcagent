# Bounded context and fit-gap

## Authority, baseline and freshness

- Authority: user instruction on 16 November 2026 to incorporate and implement the
  AcciMap recommendations in rcagent.
- Issue: https://github.com/edithatogo/rcagent/issues/139
- Base: `c6892497aa0b03555d5145242c04965471eccc1d`, tree
  `8cfbe6e85d27d68f3ca3c4a3970823394d6c7999`.
- Branch: `feat/accimap-workflow-20261116`.
- Existing coordinator: conversation `6af6164f-cf84-8321-9f96-8b7d685aabe5`.
- Observed D0 PR #132 head: `4746027c7de6cd4e0ed1518241f847146d79faef`;
  verifier PR #133 head: `4057512f23a2301d6ffe4649e42fb055eeb83937`.
- Both D0 PRs are drafts and retain their owners; their tests/acceptance are not
  transferred to this increment. Shared integration and merges stay coordinator-owned.

## Smallest remaining gap

The existing incident system remains authoritative. A canonical safety-work
record already provides evidence, statement/factor identity and provenance.
`jsonschema` validates shapes; `tools.evidence_core` validates the record and
provides canonical JSON/fingerprints. Mermaid is the existing presentation
format. None of these should be replaced.

The remaining project-specific gap is an explicit AcciMap profile, typed
contributory connections and traceable diagram output. Use a thin companion
adapter; do not create a parallel evidence store, workflow engine or generic
graph framework. The bounded 128-node/256-edge graphs need only standard-library
set traversal. No new package or generic dependency defect is asserted.

Compatibility: current safety-work schema 1.1, Python >=3.11, existing locked
jsonschema 4.26.0; the companion is versioned `accimap-1.0`. Default fallback is a
labelled draft plus explicit gaps. Future shared-schema integration must preserve
these semantics or provide an explicit migration and qualified fixtures. This
adapter can be removed after such a replacement passes the same acceptance suite.

## Scope and parallelism

The user opened a separate AcciMap task. Local implementation and read-only
method/code review are internal to this bounded increment; they do not replace
either ordinary ChatGPT D0 worker or claim an additional D0 lane. Use only the
owned paths in [the specification](./spec.md). No global Conductor registry,
integration-map, D0, CI or dependency changes are applied here.

## Inputs and data boundary

Read root AGENTS/CONSTRAINTS, this track, the portable AcciMap guide,
`tools/evidence_core.py`, `tools/json_shapes.py` and the canonical safety-work
schema. Read additional source only to resolve a concrete interface question.
Use repository-authored synthetic fixtures. Reference public primary method
sources by link; do not copy third-party PDFs into the repository.

The companion requires generated-synthetic declarations in graph and record.
Those declarations cannot identify mislabelled private data. There is no network
processing or automatic publication in the adapter. An existing organisational
approval pathway remains necessary for any future real-data profile.

## Commands and handoff

Use locked validation/test/lint/assurance dependencies and an explicit supported
Python interpreter. Run `python -m pytest -q tests/test_accimap.py` during work,
then relevant shared tests, `python -m tools.full_validation`, and actual
`python -m tools.accimap` validate/render commands. Keep strict typing at zero.

Record the actual runtime and exceptions instead of transferring another
runtime's pass. Supply source/tree identities, checks, independent findings,
remaining gates and [the shared registry proposal](./registry-proposal.md).
Rollback is a scoped revert; no schema migration, release or model call is needed.
