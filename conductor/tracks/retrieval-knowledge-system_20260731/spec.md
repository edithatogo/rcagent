# Specification: Retrieval and Knowledge System

## Overview

Build citation-first, provenance-preserving knowledge retrieval that begins with a simple lexical baseline and earns embeddings, hybrid search, and reranking only through benchmark evidence.

This track is coordinated by GitHub issue [#12](https://github.com/edithatogo/rcagent/issues/12) and the portfolio rules in [roadmap.md](../../roadmap.md). It may proceed autonomously once its hard dependencies and definition of ready have objective evidence.

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

- Define source and corpus contracts
- Implement the lexical baseline
- Add optional local vector retrieval
- Evaluate hybrid search and reranking
- Ground answers and defend retrieval
- Implement lifecycle operations
- Produce retrieval assurance receipts

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

- [benchmark-evaluation-harness_20260731](../benchmark-evaluation-harness_20260731/index.md)
- [multimodal-capability-fabric_20260731](../multimodal-capability-fabric_20260731/index.md)

These dependencies gate the affected integration or validation phase without needlessly blocking independent foundation work.

## Autonomous Execution

Reversible work inside the approved scope proceeds without per-phase approval when evidence gates pass. Each phase records sources, versions, commands, results, limitations, risks, and changes to the dependency graph. The agent stops only at a declared owner gate or when safe in-scope progress is impossible.

### Owner Decision Gates

- Use of an external or rights-restricted corpus
- Cross-compartment queries or remote embedding services
- Material retrieval thresholds that change operational behaviour

Every decision request must include the recommended option, viable alternatives, evidence, rationale, trade-offs, reversibility, cost, safe default, and impact on dependencies.

## Acceptance Criteria

1. Every indexed unit preserves source, authority, rights, version, timestamp, location, transformation, and compartment metadata.
2. A deterministic full-text baseline exists before vector retrieval.
3. Embedding, hybrid, and reranking stages are optional and retained only when measured benefits exceed cost and risk.
4. Generated answers cite retrievable evidence, expose conflicts, and abstain when support is insufficient.
5. Public and private indexes cannot be accidentally joined.
6. Update, supersession, deletion, rebuild, injection, and source-drift tests pass.

## Out of Scope

- Indexing private clinical data during this track
- Assuming vectors are more accurate than lexical retrieval
- Copying restricted policy content without rights
- Replacing authoritative source review with model output

## Evidence Standard

Completion requires reproducible artefacts and durable receipts. GitHub hierarchy, dependency state, checklists, CI status, and prose claims are coordination signals; none is sufficient evidence on its own.
