# Specification: Distribution, Registries, and Client Plugins

## Overview

Package the portable skill suite for trustworthy discovery and installation, then build optional Claude, Codex/OpenAI, and other client plugins without contaminating the standards-compliant core.

This track is coordinated by GitHub issue [#16](https://github.com/edithatogo/rcagent/issues/16) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Govern the registry and marketplace funnel
- Release the canonical portable skills
- Assess Agent Skills discovery routes
- Package for Claude Code
- Package for Codex and OpenAI
- Prepare the OpenAI universal directory submission
- Assess additional client ecosystems
- Operate compatibility and release governance

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- [agent-skills-living-conformance_20260731](../../tracks/agent-skills-living-conformance_20260731/index.md)

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [safety-systems-foundation_20260731](../../tracks/safety-systems-foundation_20260731/index.md)
- [privacy-security-assurance_20260731](../../archive/privacy-security-assurance_20260731/index.md)
- [benchmark-evaluation-harness_20260731](../../archive/benchmark-evaluation-harness_20260731/index.md)
- [interfaces-templates-action-loop_20260731](../../archive/interfaces-templates-action-loop_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Every public release, registry, marketplace, or plugin-directory submission
- Publisher verification, public legal/privacy policy, support commitment, credentials, or paid service
- Distribution through a community registry whose trust or ownership is not established

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. The canonical portable skill installs from a pinned GitHub release and passes isolated-copy conformance tests.
2. No roadmap claim assumes that the Agent Skills specification operates an official universal registry.
3. Registry and marketplace candidates are assessed for ownership, trust, security, licensing, telemetry, maintenance, review, discoverability, rollback, and terms.
4. Claude and OpenAI packages remain thin adapters over the portable core and pass client compatibility suites.
5. Submission requirements, positive and negative tests, privacy/support artefacts, and publisher evidence are current at the time of submission.
6. Every public mutation remains an explicit owner gate with a dry-run package and rollback plan.

## Out of Scope

- Submitting or publishing during roadmap creation
- Promising support for an untested client
- Bundling private data, credentials, or unlicensed source material
- Maintaining divergent copies of the portable core

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
