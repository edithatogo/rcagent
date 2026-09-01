# Implementation Plan: Safety Systems Foundation and Solo-Developer Harness

**GitHub:** [#6](https://github.com/edithatogo/rcagent/issues/6)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Continuous Execution Contract

Current review state (2026-08-31): **accepted and archived**. Delivery is tracked
separately in PR #111; archive eligibility is not a claim of merged delivery.
The specification has eleven acceptance criteria. Earlier checkmarks and the
retained completion receipt document prior contract-level evidence, not proof
that the durable coordination work passed. Preserve that receipt; the dated
review receipt below records the new implementation and passing validation.

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

- [x] Task: Establish the system and dependency context
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

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

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define the product and safety boundary

- [x] Task: Implement the phase scope
  - [x] Reconcile the repository mission, target users, use cases, exclusions, and safety principles
  - [x] Separate the client-neutral workbench from optional agent-client adapters
  - [x] Define public, governed hybrid, fully local, and air-gapped operating modes
  - [x] Record non-goals including autonomous diagnosis, automatic privilege claims, and unreviewed clinical conclusions

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Adopt the modular reference architecture

- [x] Task: Implement the phase scope
  - [x] Define portable core, domain packs, capability adapters, interfaces, evaluation, and distribution layers
  - [x] Map authoritative roles for ims+ or another incident system, enterprise content and identity, clinical systems, workflow platforms, and the local workbench
  - [x] Create the integration register and require every later track to record fit, gap, dependency profile, upstream path, and exit strategy
  - [x] Create architecture decision record conventions and a replace-before-fork framework policy
  - [x] Define stable contracts between evidence, retrieval, model, workflow, and client layers
  - [x] Define standards profiles and thin-adapter boundaries for FHIR, W3C PROV, CMMN, BPMN, DMN, evaluation frameworks, and client plugins
  - [x] Implement the capability-profile schema, keeping heavyweight and experimental components outside the portable core
  - [x] Define idempotent preflight, install, verify, update, rollback, and uninstall contracts for script and agent-assisted setup
  - [x] Document failure isolation, safe fallback, and offline-first principles

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Engineer the solo-developer delivery system

- [x] Task: Implement the phase scope
  - [x] Encode one integration lane plus no more than two independent implementation lanes
  - [x] Define hard-start dependencies, phase dependencies, WIP limits, and integration ownership
  - [x] Define machine-readable definitions of ready, done, blocked, and decision-needed
  - [x] Create an autonomous work-queue selection policy that never treats checkboxes as proof
  - [x] Implement deterministic next-ready dispatch across task, phase, review, rework, and track boundaries
  - [x] Implement idempotent run IDs, leases, heartbeats, stale-lock detection, safe takeover, and preserved-work recovery
  - [x] Implement decision and external-wait queues that release blocked lanes and schedule unaffected work
  - [x] Implement critical-path priority, owned-path conflict detection, and integration-lane convergence

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Build layered context engineering

- [x] Task: Implement the phase scope
  - [x] Add a short client-neutral AGENTS navigation contract and retain thin client adapters
  - [x] Define authoritative project, track, task, source, risk, and evidence context layers
  - [x] Create bounded task context-pack rules with freshness, provenance, and token budgets
  - [x] Define handoff and recovery summaries that expose uncertainty and unresolved decisions

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Specify the maximal harness

- [x] Task: Implement the phase scope
  - [x] Specify doctor, context, work-queue, validate, evaluate, receipts, and reconciliation entry points
  - [x] Define deterministic preflight, fixture, link, schema, privacy, and policy-drift checks
  - [x] Define durable command, environment, revision, source, result, and limitation receipts
  - [x] Define local and CI execution with honest offline and unavailable-upstream states
  - [x] Specify bounded retry classes, fallback, autonomous plan-repair outcomes, and repeated-attempt prevention
  - [x] Specify safety circuit breakers for privacy, credentials, destructive changes, evidence integrity, and material harm
  - [x] Specify resumable context cursors and session-boundary handoffs that do not create approval pauses
  - [x] Specify automatic fresh-context track review and review-report-driven rework
  - [x] Maintain the one-command repository validator and coverage-producing test harness
  - [x] Configure Renovate, dependency review, Codecov, and stable required-check discovery without adding a team approval gate

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Create governance and decision ledgers

- [x] Task: Implement the phase scope
  - [x] Create ADR, decision, risk, source, assumption, and evidence record templates
  - [x] Define decision packets with a stable ID, recommended option, rationale, evidence, alternatives, trade-offs, reversibility, safe default, paused scope, continuing work, and response format
  - [x] Define owner gates for clinical, legal, privacy, licence, credential, spend, and release choices
  - [x] Define automated freshness checks and escalation rules for stale authoritative context
  - [x] Define decision deduplication, wake conditions, non-blocking status updates, and one-decision-at-a-time engagement

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Validate autonomous execution

- [x] Task: Implement the phase scope
  - [x] Run a representative ready-task selection and bounded context-pack dry run
  - [x] Simulate uninterrupted continuation across multiple phases and into the next ready track
  - [x] Simulate a blocked owner-decision lane while independent work continues
  - [x] Simulate transient recovery, deterministic repair, plan rework, external wait, stale lock, interruption and resume, and circuit-breaker cases
  - [x] Verify every decision request presents options, a recommendation, rationale, evidence, safe default, paused scope, and continuing work
  - [x] Verify review findings become bounded automatic rework without a routine approval pause
  - [x] Verify worktree, evidence receipt, integration, rollback, and handoff procedures
  - [x] Reconcile repository hardening issues #17 and #18 against hosted rules, stable checks, recovery access, and evidence receipts
  - [x] Record defects and close the foundation only when a fresh-context reproduction passes

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #6 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

- [x] Task: Review Fixes
  - [x] Restore governed default lane limits when queue input omits an override
  - [x] Add a regression assertion for omitted lane limits

## Final Track Verification

- [x] Task: Complete the track evidence pack
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [x] Close the GitHub issue only after the completion receipt passes

## Review Fixes — 2026-08-31

Code fixes: `b39f5632c6f7dabc03be48c12958bd29af62355a`.
Current evidence: [review receipt](./evidence/review-20260831.md).

- [x] Task: Reconcile all eleven acceptance criteria against direct evidence.
  - [x] Correct the current index's obsolete protection/licence claims and
    contradictory duplicate phase-dependency section.
  - [x] Record the eleven-criterion evidence map and supersede outdated
    completion conclusions without rewriting the historical receipt.
  - [x] Reconcile GitHub #6's stale hard dependency on #5 with the specified
    phase-only dependency; retain Track 00's own unresolved acceptance scope.
- [x] Task: Implement and review durable local coordination.
  - [x] Establish evidence for persisted state, ownership, recovery and bounded
    next-step coordination; do not infer it from side-effect-free contracts.
  - [x] Record positive and negative tests for the integrated implementation.
  - [x] Pass targeted, full repository and exact-head hosted validation, or
    explicitly retain any unavailable or failed gate.
- [x] Task: Complete fresh agent-panel review and current status reconciliation.
  - [x] Record exact revisions, commands, findings, limitations and rollback.
  - [x] Archive only after complete acceptance and applicable validation pass;
    update current locators together and preserve hash-bound historical receipts.
