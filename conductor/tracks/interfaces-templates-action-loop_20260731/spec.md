# Specification: Interfaces, Templates, and Closed-Loop Actions

## Overview

Deliver usable, auditable workflows and templates for incident investigation, serious-adverse-event review, proactive systems analysis, open disclosure, recommendations, action ownership, and effectiveness monitoring.

This track is coordinated by GitHub issue [#14](https://github.com/edithatogo/rcagent/issues/14) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define users, journeys, and human factors
- Create workflow and method templates
- Build replaceable interfaces
- Embed disclosure, participation, and support
- Close the recommendation-to-effectiveness loop
- Produce auditable outputs
- Evaluate usability and oversight

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- [evidence-workflow-core_20260731](../evidence-workflow-core_20260731/index.md)
- [privacy-security-assurance_20260731](../privacy-security-assurance_20260731/index.md)
- [nsw-health-jurisdiction-pack_20260731](../nsw-health-jurisdiction-pack_20260731/index.md)

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [multimodal-capability-fabric_20260731](../multimodal-capability-fabric_20260731/index.md)
- [retrieval-knowledge-system_20260731](../retrieval-knowledge-system_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Clinical deployment or changes to mandated workflows or forms
- External disclosure, identifiable export, or organisation-specific branding
- Policy interpretations that affect operational roles, deadlines, or approval

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Interfaces expose evidence, uncertainty, citations, model involvement, limits, approvals, and outstanding reviews.
2. Workflows cover retrospective investigation and proactive systems methods without forcing one technique.
3. Templates are original or rights-cleared and map to the canonical data model.
4. Recommendations become owned, time-bounded actions with dependencies, assurance, and effectiveness review.
5. Open disclosure, consumers and families, staff support, accessibility, and Aboriginal cultural safety are designed in.
6. Usability, accessibility, failure recovery, separation of duties, and human oversight are evaluated.

## Out of Scope

- Replacing an enterprise incident management platform
- Unreviewed automated communication with patients, families, regulators, or staff
- Organisation-specific production deployment
- Assuming completion of an action proves effectiveness

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
