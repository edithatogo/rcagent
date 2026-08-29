# Specification: Local Runtime and Model Lab

## Overview

Create measured model and runtime recommendations for heterogeneous devices, including a 32 GB Intel CPU/iGPU system, Apple silicon with MLX, and larger hosts, without hard-coding unverified model assumptions.

This track is coordinated by GitHub issue [#13](https://github.com/edithatogo/rcagent/issues/13) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define devices and measurement protocol
- Implement thin runtime adapters
- Create the governed model registry
- Characterise quantisation and resource fit
- Run task and privacy benchmarks
- Implement routing and offline packaging
- Publish device recommendation matrices

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

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [retrieval-knowledge-system_20260731](../retrieval-knowledge-system_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Paid compute, large model downloads, or external inference
- Licence exceptions or execution of untrusted remote model code
- Promotion of an experimental runtime or model into a supported profile

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Device profiles and resource probes are reproducible and contain no sensitive identifiers.
2. Runtime adapters cover llama.cpp, ONNX Runtime, OpenVINO, and MLX where applicable; experimental MAX or Mojo work is isolated.
3. Every model entry names an exact revision, licence, provenance, task fit, context/input limits, quantisation, device evidence, and known failure modes.
4. Recommendations follow measured benchmark and resource evidence rather than parameter count or vendor claims.
5. Routing fails safely when resources or declared capabilities are unavailable.
6. Offline installation, verification, caching, updates, and rollback are documented for supported profiles.

## Out of Scope

- Guaranteeing that a named future or pre-release model exists
- Downloading every candidate model
- Production use of an unbenchmarked quantisation
- Fine-tuning models

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
