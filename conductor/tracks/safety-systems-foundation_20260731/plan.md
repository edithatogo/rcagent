# Implementation Plan: Safety Systems Foundation and Solo-Developer Harness

**GitHub:** [#6](https://github.com/edithatogo/rcagent/issues/6)

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

- [x] Task: Select the smallest adequate intervention
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [~] Task: Phase Verification & Checkpoint
  - [ ] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [ ] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [ ] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define the product and safety boundary

- [ ] Task: Implement the phase scope
  - [ ] Reconcile the repository mission, target users, use cases, exclusions, and safety principles
  - [ ] Separate the client-neutral workbench from optional agent-client adapters
  - [ ] Define public, governed hybrid, fully local, and air-gapped operating modes
  - [ ] Record non-goals including autonomous diagnosis, automatic privilege claims, and unreviewed clinical conclusions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Adopt the modular reference architecture

- [~] Task: Implement the phase scope
  - [ ] Define portable core, domain packs, capability adapters, interfaces, evaluation, and distribution layers
  - [ ] Map authoritative roles for ims+ or another incident system, enterprise content and identity, clinical systems, workflow platforms, and the local workbench
  - [ ] Create the integration register and require every later track to record fit, gap, dependency profile, upstream path, and exit strategy
  - [ ] Create architecture decision record conventions and a replace-before-fork framework policy
  - [ ] Define stable contracts between evidence, retrieval, model, workflow, and client layers
  - [ ] Define standards profiles and thin-adapter boundaries for FHIR, W3C PROV, CMMN, BPMN, DMN, evaluation frameworks, and client plugins
  - [x] Implement the capability-profile schema, keeping heavyweight and experimental components outside the portable core
  - [~] Define idempotent preflight, install, verify, update, rollback, and uninstall contracts for script and agent-assisted setup
  - [ ] Document failure isolation, safe fallback, and offline-first principles

- [~] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Engineer the solo-developer delivery system

- [ ] Task: Implement the phase scope
  - [ ] Encode one integration lane plus no more than two independent implementation lanes
  - [ ] Define hard-start dependencies, phase dependencies, WIP limits, and integration ownership
  - [ ] Define machine-readable definitions of ready, done, blocked, and decision-needed
  - [ ] Create an autonomous work-queue selection policy that never treats checkboxes as proof
  - [ ] Implement deterministic next-ready dispatch across task, phase, review, rework, and track boundaries
  - [ ] Implement idempotent run IDs, leases, heartbeats, stale-lock detection, safe takeover, and preserved-work recovery
  - [ ] Implement decision and external-wait queues that release blocked lanes and schedule unaffected work
  - [ ] Implement critical-path priority, owned-path conflict detection, and integration-lane convergence

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Build layered context engineering

- [ ] Task: Implement the phase scope
  - [ ] Add a short client-neutral AGENTS navigation contract and retain thin client adapters
  - [ ] Define authoritative project, track, task, source, risk, and evidence context layers
  - [ ] Create bounded task context-pack rules with freshness, provenance, and token budgets
  - [ ] Define handoff and recovery summaries that expose uncertainty and unresolved decisions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Specify the maximal harness

- [ ] Task: Implement the phase scope
  - [ ] Specify doctor, context, work-queue, validate, evaluate, receipts, and reconciliation entry points
  - [ ] Define deterministic preflight, fixture, link, schema, privacy, and policy-drift checks
  - [ ] Define durable command, environment, revision, source, result, and limitation receipts
  - [ ] Define local and CI execution with honest offline and unavailable-upstream states
  - [ ] Specify bounded retry classes, fallback, autonomous plan-repair outcomes, and repeated-attempt prevention
  - [ ] Specify safety circuit breakers for privacy, credentials, destructive changes, evidence integrity, and material harm
  - [ ] Specify resumable context cursors and session-boundary handoffs that do not create approval pauses
  - [ ] Specify automatic fresh-context track review and review-report-driven rework
  - [ ] Maintain the one-command repository validator and coverage-producing test harness
  - [ ] Configure Renovate, dependency review, Codecov, and stable required-check discovery without adding a team approval gate

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Create governance and decision ledgers

- [ ] Task: Implement the phase scope
  - [ ] Create ADR, decision, risk, source, assumption, and evidence record templates
  - [ ] Define decision packets with a stable ID, recommended option, rationale, evidence, alternatives, trade-offs, reversibility, safe default, paused scope, continuing work, and response format
  - [ ] Define owner gates for clinical, legal, privacy, licence, credential, spend, and release choices
  - [ ] Define automated freshness checks and escalation rules for stale authoritative context
  - [ ] Define decision deduplication, wake conditions, non-blocking status updates, and one-decision-at-a-time engagement

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Validate autonomous execution

- [ ] Task: Implement the phase scope
  - [ ] Run a representative ready-task selection and bounded context-pack dry run
  - [ ] Simulate uninterrupted continuation across multiple phases and into the next ready track
  - [ ] Simulate a blocked owner-decision lane while independent work continues
  - [ ] Simulate transient recovery, deterministic repair, plan rework, external wait, stale lock, interruption and resume, and circuit-breaker cases
  - [ ] Verify every decision request presents options, a recommendation, rationale, evidence, safe default, paused scope, and continuing work
  - [ ] Verify review findings become bounded automatic rework without a routine approval pause
  - [ ] Verify worktree, evidence receipt, integration, rollback, and handoff procedures
  - [ ] Reconcile repository hardening issues #17 and #18 against hosted rules, stable checks, recovery access, and evidence receipts
  - [ ] Record defects and close the foundation only when a fresh-context reproduction passes

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #6 and dependency evidence

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
