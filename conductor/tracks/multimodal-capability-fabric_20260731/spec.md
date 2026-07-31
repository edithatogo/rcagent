# Specification: Multimodal Capability Fabric

## Overview

Define a replaceable capability fabric for OCR and layout, encoders, speech transcription and diarisation, medical images and DICOM, and ECG or time-series data, with explicit limits, privacy behaviour, and governance status.

This track is coordinated by GitHub issue [#11](https://github.com/edithatogo/rcagent/issues/11) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define capability and disclosure contracts
- Evaluate document and OCR adapters
- Evaluate encoder and reranker adapters
- Evaluate speech and diarisation adapters
- Prototype medical image and DICOM ingestion
- Prototype ECG and time-series ingestion
- Benchmark and certify adapter claims

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

The track cannot start until each hard dependency has a passing completion receipt, not merely a closed issue.

## Later Phase Dependencies

- [benchmark-evaluation-harness_20260731](../benchmark-evaluation-harness_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Clinical interpretation of images, waveforms, or audio
- Remote code, restrictive licences, network model downloads, or external inference
- Promotion of a research-only capability into operational use

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Every adapter implements a versioned CapabilityProfile and emits a pre-run ExecutionDisclosure.
2. Exact model and framework revisions, licences, inputs, outputs, limits, resource needs, privacy behaviour, and failure modes are recorded.
3. The portable core does not depend on one multimodal framework.
4. Document, speech, image, and signal outputs retain source coordinates or timestamps where technically possible.
5. Medical image and ECG interpretation remain research-disabled until separately governed.
6. Contract, privacy, safety, and benchmark tests pass for each declared device class.

## Out of Scope

- Autonomous radiology, cardiology, diagnosis, or treatment advice
- Claiming medical-device status or clinical validation
- Maintaining forks of upstream frameworks
- Supporting a modality without measured fixtures

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
