# Implementation Plan: Retrieval and Knowledge System

**GitHub:** [#12](https://github.com/edithatogo/rcagent/issues/12)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Define source and corpus contracts

- [ ] Task: Implement the phase scope
  - [ ] Define ingestion manifests for authority, jurisdiction, rights, version, freshness, checksum, and compartment
  - [ ] Define chunk, page, section, table, transcript, image-region, and signal-window provenance
  - [ ] Define public, governed private, ephemeral, and excluded corpus states
  - [ ] Create deletion, supersession, correction, and re-index requirements

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement the lexical baseline

- [ ] Task: Implement the phase scope
  - [ ] Implement SQLite FTS or an equivalently portable full-text baseline behind a retrieval port
  - [ ] Support field, authority, jurisdiction, date, source, and status filters
  - [ ] Return stable citations, locations, scores, and query receipts
  - [ ] Benchmark exact, phrase, acronym, typo, and policy-version queries

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Add optional local vector retrieval

- [ ] Task: Implement the phase scope
  - [ ] Select encoder candidates through the CapabilityProfile and benchmark contracts
  - [ ] Version embeddings, chunking, normalisation, quantisation, index, and device metadata
  - [ ] Keep vector storage replaceable and local by default
  - [ ] Measure semantic gains, false neighbours, drift, memory, and rebuild cost

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Evaluate hybrid search and reranking

- [ ] Task: Implement the phase scope
  - [ ] Define deterministic fusion and candidate-set contracts
  - [ ] Evaluate local cross-encoder or model reranking only after baseline results exist
  - [ ] Measure quality, calibration, latency, memory, privacy, and failure regressions
  - [ ] Retain the simplest configuration meeting declared thresholds

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Ground answers and defend retrieval

- [ ] Task: Implement the phase scope
  - [ ] Require claim-evidence links, citation verification, conflict representation, and abstention
  - [ ] Detect instruction-like or poisoned content without erasing legitimate evidence
  - [ ] Separate source content from system and workflow instructions
  - [ ] Test malicious documents, misleading metadata, stale policies, and unsupported synthesis

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Implement lifecycle operations

- [ ] Task: Implement the phase scope
  - [ ] Implement incremental ingest, correction, supersession, delete, rebuild, backup, and restore
  - [ ] Verify public and private index separation through negative tests
  - [ ] Propagate source and policy drift to affected answers and receipts
  - [ ] Provide deterministic export and audit views

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Produce retrieval assurance receipts

- [ ] Task: Implement the phase scope
  - [ ] Run quality, citation, privacy, robustness, freshness, latency, memory, and recovery suites
  - [ ] Compare lexical, vector, hybrid, and reranked configurations transparently
  - [ ] Declare known blind spots, unsupported sources, and device limits
  - [ ] Approve no retrieval claim without exact source and benchmark evidence

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [ ] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence
  - [ ] Re-run the complete applicable validation and regression suite
  - [ ] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [ ] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes
