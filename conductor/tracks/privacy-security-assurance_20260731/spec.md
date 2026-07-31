# Specification: Privacy, Security, and Assurance

## Overview

Design and validate public/remote, governed hybrid, fully local, and air-gapped modes so private data remains in its authorised compartment while clinical, legal, cultural, and AI risks stay visible.

This track is coordinated by GitHub issue [#8](https://github.com/edithatogo/rcagent/issues/8) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Model threats, data flows, and harms
- Specify execution modes and compartments
- Design technical privacy and security controls
- Define AI and clinical-safety gates
- Define legal, records, cultural, and disclosure safeguards
- Build adversarial and recovery tests
- Produce mode-specific assurance cases

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

- [evidence-workflow-core_20260731](../evidence-workflow-core_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Use of real sensitive information or a new data class
- Network egress, credentials, security exceptions, or residual-risk acceptance
- Legal privilege interpretation, clinical deployment, or regulatory claims

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Data flows and trust boundaries are documented for every execution mode.
2. Private content cannot reach a remote service, remote log, telemetry sink, or public index in local-only modes.
3. The system fails closed when classification, routing, model provenance, or egress status is unknown.
4. Every model-assisted result exposes limitations and required human review.
5. Legal privilege is never inferred from a document label or tool output.
6. Security, privacy, cultural-safety, and clinical-safety tests produce reviewable assurance receipts.

## Out of Scope

- Organisation-specific legal advice
- Accreditation or certification claims
- Production processing of real clinical records
- Acceptance of residual risk on the owner's behalf

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
