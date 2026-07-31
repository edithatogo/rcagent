# Implementation Plan: Interfaces, Templates, and Closed-Loop Actions

**GitHub:** [#14](https://github.com/edithatogo/rcagent/issues/14)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Define users, journeys, and human factors

- [ ] Task: Implement the phase scope
  - [ ] Map investigator, reviewer, consumer, family, staff, governance, executive, administrator, and auditor journeys
  - [ ] Define roles, separation of duties, approvals, collaboration, conflict, accessibility, and failure recovery
  - [ ] Identify cognitive load, automation bias, anchoring, blame, hindsight, and confirmation risks
  - [ ] Define explicit human checkpoints and usable abstention

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Create workflow and method templates

- [ ] Task: Implement the phase scope
  - [ ] Create modular intake, chronology, evidence, interview, analysis, finding, recommendation, action, and review workflows
  - [ ] Support RCA and systems approaches including SEIPS, AcciMap, FRAM, STPA, bow-tie, barrier analysis, and FMEA where appropriate
  - [ ] Add method selection and combination guidance based on event, evidence, purpose, and capability
  - [ ] Map each template field to evidence, workflow, jurisdiction, and provenance contracts

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Build replaceable interfaces

- [ ] Task: Implement the phase scope
  - [ ] Define CLI and API workflows for intake, validation, investigation, review, export, and automation
  - [ ] Prototype an optional local user interface through a maintained framework rather than a bespoke platform
  - [ ] Define import and export adapters for Markdown, JSON, CSV, office documents, diagrams, and jurisdictional artefacts
  - [ ] Keep the portable core usable without a specific UI or agent client

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Embed disclosure, participation, and support

- [ ] Task: Implement the phase scope
  - [ ] Embed open-disclosure preparation while preserving required human communication
  - [ ] Support consumer and family questions, accounts, review, disagreement, and feedback
  - [ ] Embed staff support, Just Culture, procedural fairness, and wellbeing prompts
  - [ ] Embed Aboriginal cultural safety, accessibility, language, interpreter, and consultation needs

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Close the recommendation-to-effectiveness loop

- [ ] Task: Implement the phase scope
  - [ ] Define recommendation strength, rationale, hazards, controls, hierarchy, feasibility, and unintended consequences
  - [ ] Assign action owners, dependencies, resources, deadlines, assurance evidence, and escalation
  - [ ] Define implementation verification, outcome/process/balancing measures, review periods, and residual risk
  - [ ] Prevent action closure or report publication from implying effectiveness

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Produce auditable outputs

- [ ] Task: Implement the phase scope
  - [ ] Generate investigation, executive, consumer-facing, action, and effectiveness views from shared evidence
  - [ ] Expose sources, citations, uncertainty, conflicts, model/runtime use, privacy mode, limitations, and approvals
  - [ ] Apply bounded export, redaction, watermark, access, and retention policies
  - [ ] Validate diagrams and documents without silently changing meaning

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Evaluate usability and oversight

- [ ] Task: Implement the phase scope
  - [ ] Test representative novice and expert journeys with synthetic cases
  - [ ] Test accessibility, recovery, interruption, collaboration, correction, and disagreement
  - [ ] Measure automation bias, missed evidence, unsafe certainty, and review burden
  - [ ] Record product limitations and block clinical deployment pending separate approval

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #14 and dependency evidence

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
