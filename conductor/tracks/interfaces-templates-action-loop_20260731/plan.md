# Implementation Plan: Interfaces, Templates, and Closed-Loop Actions

**GitHub:** [#14](https://github.com/edithatogo/rcagent/issues/14)

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
  - [ ] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [ ] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define users, journeys, and human factors

- [ ] Task: Implement the phase scope
  - [ ] Map investigator, reviewer, consumer, family, staff, governance, executive, administrator, and auditor journeys
  - [ ] Map the end-to-end journey from submission, huddle, provisional risk and harm assessment, review team and evidence collection through findings, recommendations, actions, effectiveness, learning, and closure
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
  - [ ] Add modular huddle, provisional assessment, review-team, patient problem-list, incident problem-list, consultation, literature-search, related-policy referral, and organisational-learning workflows
  - [ ] Support RCA and systems approaches including SEIPS, AcciMap, FRAM, STPA, bow-tie, barrier analysis, and FMEA where appropriate
  - [ ] Add method selection and combination guidance based on event, evidence, purpose, and capability
  - [ ] Map each template field to evidence, workflow, jurisdiction, and provenance contracts
  - [ ] Evaluate the vendored authentext skill module for professional-register report generation and adopt it behind a thin contract where it passes privacy, provenance, and conformance gates

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
  - [ ] Add capability discovery and an agent-guided setup workflow that recommends the smallest adequate optional profile
  - [ ] Require the interface to show profile status, limits, privacy mode, installation source, health, and rollback
  - [ ] Define CLI and API workflows for intake, validation, investigation, review, export, and automation
  - [ ] Define bounded read, export, import, and reconciliation adapters for ims+ or another approved incident system without creating a shadow registry
  - [ ] Assess approved Microsoft 365, SharePoint, Teams, Power Automate, Dataverse, or comparable enterprise surfaces before building collaboration or approval features
  - [ ] Assess CMMN, BPMN, and DMN models and an existing organisational engine or Flowable before implementing workflow execution
  - [ ] Map applicable FHIR Task, Questionnaire, QuestionnaireResponse, and DocumentReference exchanges where a source system supports them
  - [ ] Prototype an optional local user interface through a maintained framework only for a demonstrated privacy, analysis, or evidence-review gap
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
  - [ ] Link recommendation rationale to searched literature where warranted while keeping bibliographic integrity, evidence appraisal, local applicability, and authorised acceptance distinct
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
