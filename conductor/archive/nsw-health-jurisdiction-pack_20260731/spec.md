# Specification: NSW Health Jurisdiction Pack

## Overview

Build versioned jurisdiction packs that map authoritative national, NSW Health, CEC, ACI, and Queensland Health sources into usable serious-adverse-event workflows without silently converting guidance, drafts, or templates into binding requirements.

Jurisdiction strategy: national standards form the shared baseline tier that every state pack inherits rather than duplicates; NSW and Queensland packs then model only genuinely state-specific requirements on top of that baseline.

This track is coordinated by GitHub issue [#9](https://github.com/edithatogo/rcagent/issues/9) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Establish the national baseline tier from NSQHS, ACSQHC frameworks, relevant Commonwealth legislation, and the national accreditation scheme
- Create the authoritative source registry covering the national baseline plus NSW and Queensland source classes
- Register Queensland Health patient-safety, serious-adverse-event, open-disclosure, and clinical-governance sources alongside their NSW counterparts, including Clinical Excellence Queensland and the Coroners Court of Queensland
- Model authority, version, and drift
- Map incident and investigation workflows
- Map forms, templates, and evidence requirements
- Embed people, culture, and systems safeguards, including Aboriginal and Torres Strait Islander cultural safety as a national baseline requirement
- Validate the jurisdiction mapping across multi-jurisdiction scenarios
- Operationalise policy drift

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

- [evidence-workflow-core_20260731](../../archive/evidence-workflow-core_20260731/index.md)
- [privacy-security-assurance_20260731](../../archive/privacy-security-assurance_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Clinical or policy interpretation that is not explicit in an authoritative source
- Copying a restricted template or localising a state-wide process
- Privilege claims or use of superseded, under-review, or consultation material

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Every rule links to an authoritative source, exact version, authority level, rights status, retrieval date, and checksum where possible.
2. Current, under-review, draft, superseded, local, and advisory sources are visibly distinct.
3. The generic core remains independent of any single jurisdiction's terminology, workflow, or state-specific identifiers.
4. Serious-adverse-event, review, investigation, disclosure, escalation, and action requirements map to explicit state transitions.
5. Open disclosure, consumer/family involvement, staff support, and Aboriginal cultural safety are represented.
6. Material upstream drift opens a reviewable change request instead of silently changing behaviour.

## Out of Scope

- Legal advice or a declaration of statutory privilege
- Replacing ims+ or another incident management system
- Copying restricted state or Commonwealth material without rights evidence
- Organisation-specific approval of a local procedure

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
