# Context Pack: Prospective execution provenance

Track: eval-blocker-remediation_20260803; issue #1. Base:
`b10abeb68df1258b3d82beec73aacc790ebce6b2` (merged PR #83, exact tree matched).
Branch: `codex/prospective-study-runner`. Created 2026-08-30; fresh until
code, protocol, input, runtime or model bytes change. Context budget: selected
track, standing decisions, runtime/protocol modules and focused tests only.

## Objective and fit

Reuse existing protocol candidate checks, comparator admission, pinned Darwin
profile and standard-library Git/subprocess capture. Implement only the missing
study-specific freeze/provenance and deterministic execution boundary, not a
new inference framework. Own new `tools/prospective_freeze.py`, its tests,
prospective runner/normalisation modules and tests, and this track's records.
Keep individual agent file ownership disjoint. No worktree isolation lease is
configured; do not infer a lease from this document.

## Inputs and acceptance

Use decisions 20260830-001/002, the active spec/plan, prospective protocol
contract, existing local comparator admission and runtime profile. Validate
exact committed protocol/reference/component bytes before accepting a freeze;
candidate consistency alone must not permit execution. Require fixture-first
positive/adversarial tests, agent-panel review and full repository validation.
The runner must preserve raw evidence, fixed settings, declared slots and failed
attempts. Output extraction must be verified against the exact runtime grammar.
No generic stripping, retrospective score tuning or synthetic primary receipts.

## Current evidence and limits

PR #83 is merged with seven passing exact-head checks and 683 local tests at
93.02% coverage. A fresh pre-execution check now fails because pinned executable,
libomp and ggml backend files are missing. No help/model process launched.
Earlier receipts remain historical evidence for their recorded source/runtime
bytes, not proof of current availability. Inspect only existing local caches
for exact recovery; do not substitute updated binaries or modify global links.
Synthetic/public research only; no credentials, private data, downloads or
distribution. Historical H0-H8/H8P, scoring and external authority stay separate.

## Commands and handoff

Run focused pytest, Ruff, type checks and `uv run python -m tools.full_validation`.
Use separate coverage data files for concurrent tests, or run serially.
Record complete negative findings and concrete next steps. Rollback only new
modules and this checkpoint's records, preserving original receipts. Next:
freeze verification and exact-runtime extraction, then protocol-bound admission.
