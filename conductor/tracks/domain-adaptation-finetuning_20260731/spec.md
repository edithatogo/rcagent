# Specification: Domain Adaptation and Fine-Tuning

## Overview

Assess medical and domain models and pursue retrieval adaptation, prompting, adapters, LoRA, or fine-tuning only when benchmark evidence shows a justified gap and data rights, privacy, and governance conditions are satisfied.

This track is coordinated by GitHub issue [#15](https://github.com/edithatogo/rcagent/issues/15) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Establish adaptation readiness
- Evaluate domain model comparators
- Create governed adaptation data
- Run least-complexity experiments first
- Evaluate gains and regressions
- Document governance and lineage
- Promote, constrain, or reject

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- [benchmark-evaluation-harness_20260731](../../archive/benchmark-evaluation-harness_20260731/index.md)
- [multimodal-capability-fabric_20260731](../../archive/multimodal-capability-fabric_20260731/index.md)
- [retrieval-knowledge-system_20260731](../retrieval-knowledge-system_20260731/index.md)
- [local-runtime-model-lab_20260731](../local-runtime-model-lab_20260731/index.md)

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [privacy-security-assurance_20260731](../../archive/privacy-security-assurance_20260731/index.md)
- [nsw-health-jurisdiction-pack_20260731](../nsw-health-jurisdiction-pack_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Training-data use, de-identification adequacy, or private-case adaptation
- Compute spend, model licence, or distribution of adapted weights
- Clinical claims or promotion beyond a bounded research profile

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. A readiness gate proves a material baseline gap and a justified adaptation hypothesis.
2. Generic, retrieval-augmented, prompting, adapter, and domain-model baselines are compared before fine-tuning.
3. Training and evaluation data have rights, provenance, de-identification, split, contamination, and deletion records.
4. Improvements are accompanied by safety, privacy, calibration, robustness, device, and maintenance analysis.
5. Every adapted artefact has a model card, lineage, exact training recipe, licence, limitations, and rollback.
6. An adaptation may be rejected; completion does not require shipping a tuned model.

## Out of Scope

- Fine-tuning merely because infrastructure exists
- Training on unapproved clinical records
- Claiming clinical validation or medical-device status
- Publishing weights or datasets without owner approval

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
