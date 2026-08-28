# Autonomy Harness Receipt — 2026-08-29

## Implemented contracts

`tools.autonomy_harness` provides side-effect-free deterministic contracts for:

- criticality and priority ordered ready-task selection;
- hard-dependency admission without treating checkboxes as proof;
- integration and independent lane limits;
- nested owned-path conflict detection and traversal rejection;
- revision-bound idempotent run identifiers;
- exact owner and worktree lease classification;
- stale and inconsistent lease detection;
- bounded transient and deterministic recovery;
- external waits, decisions, and material-risk circuit breakers; and
- complete decision-packet field validation.

Blocked work is excluded from dispatch, releasing its lane for independent ready work. The module does not acquire a lease, mutate a worktree, retry a command, or take over stale work; callers must preserve work and apply the governed operational procedure.

## Validation

- `python -m pytest tests/test_autonomy_harness.py -q`: 13 passed.
- Ruff: passed.
- ty: passed.
- basedpyright: passed.

Fixtures cover priority, dependencies, WIP saturation, path conflict, traversal, held/stale/inconsistent leases, retry exhaustion, external wait, decision wait, circuit breaking, and missing decision fields.
