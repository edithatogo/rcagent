# Implementation Plan: Evidence Workflow Core

**GitHub:** [#7](https://github.com/edithatogo/rcagent/issues/7)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Continuous Execution Contract

- Continue automatically through tasks, phase checkpoints, fresh-context
  review, bounded rework, documentation synchronization, and the next ready
  track.
- Do not ask for routine approval at task, phase, review, or track boundaries.
- If a decision gate is reached, pause only the affected scope, release its
  lane, continue safe independent work, and present options with a
  recommendation, rationale, evidence, trade-offs, reversibility, safe
  default, and dependency impact.
- Use bounded retry, autonomous plan repair, durable resume state, stale-lock
  recovery, and safety circuit breakers from `autonomy.md`.

## Phase 0: Existing-System Fit and Gap Closure

- [~] Task: Establish the system and dependency context
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [ ] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [ ] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [ ] Task: Select the smallest adequate intervention
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [ ] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [ ] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [ ] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [ ] Task: Define the dependency lifecycle
  - [ ] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [ ] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [ ] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [ ] Update `integration-map.json` with the selected status and evidence links
  - [ ] Test vendored sourceright as the candidate maintained system for citation and source verification; prefer a thin SourceRight adapter over any project-owned verifier

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify that no planned work duplicates an adequate existing capability
  - [ ] Verify the system-of-record and data-authority boundary
  - [ ] Verify the smallest remaining gap and ownership rationale
  - [ ] Record the fit-gap receipt and bounded handoff context
  - [ ] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [ ] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define the canonical safety-work data model

- [ ] Task: Implement the phase scope
  - [~] Model cases, events, people-as-roles, sources, artefacts, evidence items, claims, factors, findings, recommendations, actions, reviews, and outcomes
  - [ ] Model incident huddles, provisional risk and harm assessments, review teams, interviews, consultations, patient problem lists, incident problem lists, related-policy referrals, literature searches, and organisational-learning links
  - [x] Define stable identifiers, versions, timestamps, authority, confidentiality, and jurisdiction fields
  - [x] Separate observed fact, reported account, inference, hypothesis, finding, and decision types
  - [x] Publish JSON Schema and human-readable semantic definitions
  - [ ] Map incident exchange boundaries to applicable FHIR R5 resources without treating FHIR as the investigation ontology
  - [ ] Reuse W3C PROV entity, activity, agent, derivation, and attribution concepts where they fit
  - [ ] Profile CMMN for adaptive investigation cases, BPMN for predictable processes, and DMN for transparent decision tables
  - [ ] Preserve ims+ or another approved incident platform as the system of record and define reconciliation rather than shadow-state behaviour

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
  - [ ] Model submission, immediate response, huddle, provisional assessment, review-path selection, team formation, evidence acquisition, interviews, systems analysis, findings, literature-informed recommendations, related-policy pathways, learning, and reopen states
  - [ ] Keep lookback, cluster review, individual-worker review, cultural review, clinical risk, enterprise risk, quality improvement, and medicolegal pathways as explicit governed referrals rather than hidden subprocesses
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
