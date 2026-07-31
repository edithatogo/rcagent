# Implementation Plan: Evidence Workflow Core

**GitHub:** [#7](https://github.com/edithatogo/rcagent/issues/7)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Define the canonical safety-work data model

- [ ] Task: Implement the phase scope
  - [ ] Model cases, events, people-as-roles, sources, artefacts, evidence items, claims, factors, findings, recommendations, actions, reviews, and outcomes
  - [ ] Define stable identifiers, versions, timestamps, authority, confidentiality, and jurisdiction fields
  - [ ] Separate observed fact, reported account, inference, hypothesis, finding, and decision types
  - [ ] Publish JSON Schema and human-readable semantic definitions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement evidence and claim provenance

- [ ] Task: Implement the phase scope
  - [ ] Define immutable source and evidence fingerprints with lawful redaction support
  - [ ] Represent citations, excerpts, transformations, model involvement, authorship, and reviewer decisions
  - [ ] Represent support, contradiction, uncertainty, relevance, and supersession relationships
  - [ ] Define chain-of-custody and tamper-evident receipt requirements

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Define workflow state machines

- [ ] Task: Implement the phase scope
  - [ ] Model intake, triage, review, investigation, consultation, approval, action, effectiveness, and closure states
  - [ ] Define transitions, preconditions, responsible roles, time constraints, and exception paths
  - [ ] Keep generic workflow semantics separate from jurisdiction-pack rules
  - [ ] Define reopen, correction, withdrawal, and appeal behaviours

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Specify persistence and interchange contracts

- [ ] Task: Implement the phase scope
  - [ ] Define validation, serialisation, versioning, import, export, and migration behaviour
  - [ ] Define local encrypted storage and public/private compartment interfaces without selecting one vendor
  - [ ] Define append-only audit events and reproducible derived views
  - [ ] Define bounded report and machine-readable export profiles

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Create fixtures and negative cases

- [ ] Task: Implement the phase scope
  - [ ] Create synthetic and de-identified complete, incomplete, conflicting, and multi-jurisdiction cases
  - [ ] Create broken provenance, invalid transition, duplication, redaction, and supersession fixtures
  - [ ] Define expected validation diagnostics and safe recovery for every invalid fixture
  - [ ] Test schema evolution and round trips across supported versions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Define adapter APIs

- [ ] Task: Implement the phase scope
  - [ ] Specify evidence-store, retrieval, capability, workflow, interface, and export ports
  - [ ] Define capability discovery, timeout, cancellation, retry, idempotency, and failure semantics
  - [ ] Define event and receipt contracts for local, hybrid, and remote execution
  - [ ] Add contract tests that prevent framework-specific types leaking into the core

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Verify provenance completeness

- [ ] Task: Implement the phase scope
  - [ ] Run all valid, invalid, migration, round-trip, and failure-path fixtures
  - [ ] Verify reports cannot silently convert inference into fact
  - [ ] Verify redaction and deletion policies preserve required audit meaning
  - [ ] Produce a schema and workflow compatibility receipt

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #7 and dependency evidence

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
