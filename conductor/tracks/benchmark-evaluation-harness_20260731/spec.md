# Specification: Benchmark and Evaluation Harness

## Overview

Create a benchmark-first assurance system for incident-analysis quality, retrieval, provenance, safety, privacy, calibration, multimodal capability, and device performance before model selection or fine-tuning.

This track is coordinated by GitHub issue [#10](https://github.com/edithatogo/rcagent/issues/10) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define benchmark governance
- Define metrics and gates
- Build benchmark cases and rubrics
- Implement reproducible runners
- Run pilot baselines
- Reconcile and calibrate the evaluation estate
- Automate regression and reporting

## Architecture and Delivery Principles

- Preserve a client-neutral, privacy-first portable core.
- Reuse maintained frameworks behind thin, versioned contracts and contract tests.
- Prefer the simplest component that passes declared quality, safety, privacy, device, and maintenance gates.
- Preserve provenance, raw evidence, uncertainty, negative results, and exact revisions.
- Treat remote, hybrid, local, and air-gapped modes as explicit capability profiles.
- Do not infer compliance, privilege, clinical validity, or release readiness from labels or checklist state.

## Hard Start Dependencies

- [evidence-workflow-core_20260731](../../archive/evidence-workflow-core_20260731/index.md)
- [privacy-security-assurance_20260731](../../archive/privacy-security-assurance_20260731/index.md)

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [nsw-health-jurisdiction-pack_20260731](../nsw-health-jurisdiction-pack_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Use of real cases or externally restricted benchmark data
- Gold-standard clinical judgements and operational acceptance thresholds
- Publication of comparative model or product claims

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Datasets, prompts, rubrics, models, runtimes, and results are versioned and contamination-aware.
2. Task, retrieval, citation, safety, privacy, calibration, robustness, latency, memory, and energy-proxy measures are reproducible.
3. Synthetic and de-identified cases cover incomplete, conflicting, adversarial, and jurisdictional uncertainty.
4. Human scoring exposes rater instructions, agreement, uncertainty, and unresolved disagreement.
5. A model or framework cannot be promoted solely from aggregate quality if it fails privacy or safety gates.
6. Legacy H0-H8 work is preserved and mapped into the canonical harness rather than silently discarded.

## Out of Scope

- Declaring a universal best model
- Publishing private or copyrighted case material
- Fine-tuning before readiness gates pass
- Hiding nondeterminism behind a single score

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
