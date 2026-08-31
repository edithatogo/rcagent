# Specification: Safety Systems Foundation and Solo-Developer Harness

## Overview

Reframe the repository as a client-neutral Safety Systems Workbench and establish the architecture, dependency graph, context layers, autonomous work queue, evidence receipts, and maximal harness needed by a single developer.

This track is coordinated by GitHub issue [#6](https://github.com/edithatogo/rcagent/issues/6) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

## Autonomous Execution Requirement

Execution follows [autonomy.md](../../autonomy.md) and
[autonomy.json](../../autonomy.json). Once implementation is authorised, work
continues across tasks, phases, automatic review and rework, documentation
synchronization, and the next ready track without routine confirmation.

Only the affected scope pauses at an owner decision gate. Its request must
present a recommended option first, rationale and evidence, viable
alternatives, trade-offs, reversibility, safe default, paused scope,
continuing work, and dependency impact. Safe independent work continues.

## Integration-First Requirement

This track follows [integration-strategy.md](../../integration-strategy.md) and
its candidates in [integration-map.json](../../integration-map.json). It must
identify the authoritative organisational system and applicable standards,
test maintained dependencies and extension points, and own only the smallest
safety-, privacy-, jurisdiction-, or domain-specific gap.

Configuration, profiling, standards mapping, a thin adapter, or an authorised
upstream contribution takes precedence over a project implementation. Any
local shim requires contract tests, an upstream reference, an expiry or
removal condition, and a replacement path. A new subsystem or permanent fork
requires a fit-gap record and an approved Architecture Decision Record.

## In Scope

- Define the product and safety boundary
- Adopt the modular reference architecture
- Engineer the solo-developer delivery system
- Build layered context engineering
- Specify the maximal harness
- Create governance and decision ledgers
- Validate autonomous execution

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- None.

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [agent-skills-living-conformance_20260731](../../tracks/agent-skills-living-conformance_20260731/index.md)
  gates only licence declarations, redistribution, public release, registry or
  marketplace actions, and clinical-validity claims. Reversible local
  foundation work is admitted by the Track 00 technical-baseline receipt at
  merged commit `c943269c2407c338b3c2993fe92074fa4ddfbf7b`.

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds continuously across tasks,
phases, automatic review and rework, documentation synchronization, and ready
tracks when evidence gates pass. Each phase records sources, versions,
commands, results, limitations, risks, and changes to the dependency graph.

Only the affected lane pauses at a declared owner gate or safety circuit
breaker. External waits, transient failures, invalid plans, and stale state
use bounded recovery, release blocked WIP, and do not stop independent work.

### Owner Decision Gates

- Material changes to the approved product boundary or public claims
- Irreversible architecture or repository-governance choices
- New credentials, paid services, public releases, or destructive migrations

Every decision request must include a stable ID, the recommended option first,
viable alternatives, evidence, rationale, trade-offs, reversibility, cost,
safe default, paused scope, continuing work, required response, and impact on
dependencies.

## Acceptance Criteria

1. The product boundary covers incident investigation, learning, action effectiveness, and proactive safety analysis without presenting the system as an autonomous clinical decision-maker.
2. A machine-readable, acyclic dependency graph agrees with Conductor and GitHub.
3. A fresh-context agent can select the next ready task from bounded context without loading the whole repository.
4. Doctor, context, queue, validation, evaluation, and receipt command contracts are documented and testable.
5. Autonomous work and owner-only decisions are distinguished by an enforceable policy.
6. Architecture, source, risk, decision, and evidence records have owners and freshness rules.
7. A passing phase automatically dispatches the next ready phase and a passing track automatically dispatches review, bounded rework, synchronization, and the next ready track.
8. A decision-blocked or externally waiting lane releases its slot while independent ready work continues.
9. Retry budgets, plan repair, resumable state, leases, stale-lock recovery, idempotency, and safety circuit breakers pass positive and negative fixtures.
10. Decision packets always present options, a recommendation and rationale, evidence, trade-offs, reversibility, safe default, paused scope, continuing work, and dependency impact.
11. Upstream Conductor experimental features remain replaceable research adapters until compatibility and robustness gates pass.

## Out of Scope

- Implementing every downstream capability
- Selecting a production model or vector store
- Submitting the project to a public registry
- Using real clinical or employee information

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
