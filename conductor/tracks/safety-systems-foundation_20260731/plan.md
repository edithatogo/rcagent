# Implementation Plan: Safety Systems Foundation and Solo-Developer Harness

**GitHub:** [#6](https://github.com/edithatogo/rcagent/issues/6)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 0: Existing-System Fit and Gap Closure

- [ ] Task: Establish the system and dependency context
  - [ ] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [ ] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [ ] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [ ] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [ ] Task: Select the smallest adequate intervention
  - [ ] Prefer existing-system configuration or a standards profile
  - [ ] Prefer a thin replaceable adapter when translation is the remaining gap
  - [ ] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [ ] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [ ] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [ ] Task: Define the dependency lifecycle
  - [ ] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [ ] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [ ] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [ ] Update `integration-map.json` with the selected status and evidence links

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify that no planned work duplicates an adequate existing capability
  - [ ] Verify the system-of-record and data-authority boundary
  - [ ] Verify the smallest remaining gap and ownership rationale
  - [ ] Record the fit-gap receipt and bounded handoff context
  - [ ] Continue automatically unless an enterprise connection, upstream communication, public dependency commitment, permanent fork, or new subsystem requires owner approval

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

- [ ] Task: Implement the phase scope
  - [ ] Define portable core, domain packs, capability adapters, interfaces, evaluation, and distribution layers
  - [ ] Map authoritative roles for ims+ or another incident system, enterprise content and identity, clinical systems, workflow platforms, and the local workbench
  - [ ] Create the integration register and require every later track to record fit, gap, dependency profile, upstream path, and exit strategy
  - [ ] Create architecture decision record conventions and a replace-before-fork framework policy
  - [ ] Define stable contracts between evidence, retrieval, model, workflow, and client layers
  - [ ] Define standards profiles and thin-adapter boundaries for FHIR, W3C PROV, CMMN, BPMN, DMN, evaluation frameworks, and client plugins
  - [ ] Document failure isolation, safe fallback, and offline-first principles

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

## Phase 3: Engineer the solo-developer delivery system

- [ ] Task: Implement the phase scope
  - [ ] Encode one integration lane plus no more than two independent implementation lanes
  - [ ] Define hard-start dependencies, phase dependencies, WIP limits, and integration ownership
  - [ ] Define machine-readable definitions of ready, done, blocked, and decision-needed
  - [ ] Create an autonomous work-queue selection policy that never treats checkboxes as proof

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
  - [ ] Define the recommended-option decision request contract and safe default behaviour
  - [ ] Define owner gates for clinical, legal, privacy, licence, credential, spend, and release choices
  - [ ] Define automated freshness checks and escalation rules for stale authoritative context

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
  - [ ] Simulate a reversible autonomous phase and a blocked owner-decision phase
  - [ ] Verify worktree, evidence receipt, integration, rollback, and handoff procedures
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
