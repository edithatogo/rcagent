# Specification: Evidence Workflow Core

## Overview

Create interoperable schemas and workflow contracts for cases, sources, evidence, claims, contributory factors, findings, recommendations, actions, reviews, and effectiveness outcomes with end-to-end provenance.

This track is coordinated by GitHub issue [#7](https://github.com/edithatogo/rcagent/issues/7) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define the canonical safety-work data model
- Implement evidence and claim provenance
- Define workflow state machines
- Specify persistence and interchange contracts
- Create fixtures and negative cases
- Define adapter APIs
- Verify provenance completeness

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- [safety-systems-foundation_20260731](../safety-systems-foundation_20260731/index.md)

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- None

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Changes to the clinical meaning of a canonical record
- Mandated retention or legal-status assertions
- Destructive or non-reversible schema migrations

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Every material statement can be traced to evidence, a transformation, an author, a timestamp, and a review state.
2. Conflicting, missing, late, superseded, and withdrawn evidence remain visible.
3. Case, investigation, recommendation, action, effectiveness, and closure states are explicit and validated.
4. Storage, retrieval, model, workflow, and client implementations remain replaceable behind versioned contracts.
5. Round-trip, migration, and failure fixtures pass without using sensitive data.
6. Exports preserve provenance and clearly distinguish observed facts, reported accounts, analysis, and decisions.

## Out of Scope

- A production user interface
- Organisation-specific record retention decisions
- A final NSW Health policy mapping
- Clinical conclusions from real cases

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
