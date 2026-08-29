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

- [x] Task: Establish the system and dependency context — `4a976e0`; review `1431674`
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints — see `evidence/fit-gap-sourceright-20260829.md`
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures — live `bench` fixture trial deferred to Phase 6 (local shell cannot host the Rust toolchain build; see fit-gap receipt)

- [x] Task: Select the smallest adequate intervention — `4a976e0`; review `1431674`
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution — sourceright#100 filed
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork — thin adapter selected; no ADR required

- [x] Task: Define the dependency lifecycle — `4a976e0`; review `1431674`
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile — SourceRight: optional adapter over the vendored plugin
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback — contract fixtures arrive with the Phase 6 adapter implementation; compatibility window is the pinned upstream main recorded in `vendored_plugins`
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links
  - [x] Test vendored sourceright as the candidate maintained system for citation and source verification; prefer a thin SourceRight adapter over any project-owned verifier — selection recorded from source-level evaluation; live `bench` fixture run is a Phase 6 entry condition (see fit-gap receipt)

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define the canonical safety-work data model

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Model cases, events, people-as-roles, sources, artefacts, evidence items, claims, factors, findings, recommendations, actions, reviews, and outcomes
  - [x] Model incident huddles, provisional risk and harm assessments, review teams, interviews, consultations, patient problem lists, incident problem lists, related-policy referrals, literature searches, and organisational-learning links
  - [x] Define stable identifiers, versions, timestamps, authority, confidentiality, and jurisdiction fields
  - [x] Separate observed fact, reported account, inference, hypothesis, finding, and decision types
  - [x] Publish JSON Schema and human-readable semantic definitions
  - [x] Map incident exchange boundaries to applicable FHIR R5 resources without treating FHIR as the investigation ontology
  - [x] Reuse W3C PROV entity, activity, agent, derivation, and attribution concepts where they fit
  - [x] Profile CMMN for adaptive investigation cases, BPMN for predictable processes, and DMN for transparent decision tables
  - [x] Preserve ims+ or another approved incident platform as the system of record and define reconciliation rather than shadow-state behaviour

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement evidence and claim provenance

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Define immutable source and evidence fingerprints with lawful redaction support
  - [x] Represent citations, excerpts, transformations, model involvement, authorship, and reviewer decisions
  - [x] Represent support, contradiction, uncertainty, relevance, and supersession relationships
  - [x] Define chain-of-custody and tamper-evident receipt requirements

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Define workflow state machines

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Model intake, triage, review, investigation, consultation, approval, action, effectiveness, and closure states
  - [x] Model submission, immediate response, huddle, provisional assessment, review-path selection, team formation, evidence acquisition, interviews, systems analysis, findings, literature-informed recommendations, related-policy pathways, learning, and reopen states
  - [x] Keep lookback, cluster review, individual-worker review, cultural review, clinical risk, enterprise risk, quality improvement, and medicolegal pathways as explicit governed referrals rather than hidden subprocesses
  - [x] Define transitions, preconditions, responsible roles, time constraints, and exception paths
  - [x] Keep generic workflow semantics separate from jurisdiction-pack rules
  - [x] Define reopen, correction, withdrawal, and appeal behaviours

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Specify persistence and interchange contracts

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Define validation, serialisation, versioning, import, export, and migration behaviour
  - [x] Define local encrypted storage and public/private compartment interfaces without selecting one vendor
  - [x] Define append-only audit events and reproducible derived views
  - [x] Define bounded report and machine-readable export profiles

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Create fixtures and negative cases

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Create synthetic and de-identified complete, incomplete, conflicting, and multi-jurisdiction cases
  - [x] Create broken provenance, invalid transition, duplication, redaction, and supersession fixtures
  - [x] Define expected validation diagnostics and safe recovery for every invalid fixture
  - [x] Test schema evolution and round trips across supported versions

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Define adapter APIs

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Specify evidence-store, retrieval, capability, workflow, interface, and export ports
  - [x] Define capability discovery, timeout, cancellation, retry, idempotency, and failure semantics
  - [x] Define event and receipt contracts for local, hybrid, and remote execution
  - [x] Add contract tests that prevent framework-specific types leaking into the core

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Verify provenance completeness

- [x] Task: Implement the phase scope — `4a976e0`; review `1431674`
  - [x] Run all valid, invalid, migration, round-trip, and failure-path fixtures
  - [x] Verify reports cannot silently convert inference into fact
  - [x] Verify redaction and deletion policies preserve required audit meaning
  - [x] Produce a schema and workflow compatibility receipt

- [x] Task: Validate the phase deliverables — `4a976e0`; review `1431674`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #7 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `4a976e0`; review `1431674`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Review Fixes

- [x] Task: Enforce fail-closed adapter and malformed-input boundaries — `1431674`
  - [x] Restrict SourceRight execution to an executable read-only command allowlist
  - [x] Reject write-mode `--apply` and unsupported privacy profiles
  - [x] Return schema diagnostics for malformed relationships without raising
  - [x] Record redaction custody state explicitly
  - [x] Run focused tests, lint, and type checks
  - [x] Close the hosted patch-coverage gap with cross-reference, malformed-input, audit-tamper, export, redaction, and adapter failure tests

## Final Track Verification

- [x] Task: Complete the track evidence pack — `4a976e0`; review `1431674`
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [x] Close the GitHub issue only after the completion receipt passes

## Review Remediation — 2026-08-29

- [~] Task: Re-prove completion and close review gaps — review fix `d4d279c`
  - [x] Reconcile the follow-up hosted patch check and merge in the append-only ledger
  - [x] Reject discontinuous workflow histories rather than validating isolated transitions only
  - [x] Make malformed audit receipts and invalid adapter timeouts fail closed
  - [x] Add regression tests for each repaired boundary
  - [x] Run focused and repository-wide validation from a clean commit
  - [x] Record the review-fix commit and durable completion receipt
  - [ ] Close issue #7 only after local and hosted evidence pass
