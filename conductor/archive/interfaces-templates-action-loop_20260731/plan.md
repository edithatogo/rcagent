# Implementation Plan: Interfaces, Templates, and Closed-Loop Actions

**GitHub:** [#14](https://github.com/edithatogo/rcagent/issues/14)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Recorded outcome boundary

Checked items record completion of the bounded assessment or contract work, not operational availability. ims+/enterprise connectors, Microsoft 365 surfaces, FHIR exchange, workflow-engine execution, local UI, office/diagram exporters, Authentext formatting, private-data use, external communication, organisation-specific forms, human usability/accessibility research, and clinical deployment remain unavailable, unsupported, or outside repository completion. The implemented surface is generated-synthetic, local JSON validation and dry-run preparation only; exact limitations and negative results are in the evidence pack.

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

## Phase 1: Define users, journeys, and human factors

- [x] Task: Implement the phase scope
  - [x] Map investigator, reviewer, consumer, family, staff, governance, executive, administrator, and auditor journeys
  - [x] Map the end-to-end journey from submission, huddle, provisional risk and harm assessment, review team and evidence collection through findings, recommendations, actions, effectiveness, learning, and closure
  - [x] Define roles, separation of duties, approvals, collaboration, conflict, accessibility, and failure recovery
  - [x] Identify cognitive load, automation bias, anchoring, blame, hindsight, and confirmation risks
  - [x] Define explicit human checkpoints and usable abstention

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Create workflow and method templates

- [x] Task: Implement the phase scope
  - [x] Create modular intake, chronology, evidence, interview, analysis, finding, recommendation, action, and review workflows
  - [x] Add modular huddle, provisional assessment, review-team, patient problem-list, incident problem-list, consultation, literature-search, related-policy referral, and organisational-learning workflows
  - [x] Support RCA and systems approaches including SEIPS, AcciMap, FRAM, STPA, bow-tie, barrier analysis, and FMEA where appropriate
  - [x] Add method selection and combination guidance based on event, evidence, purpose, and capability
  - [x] Map each template field to evidence, workflow, jurisdiction, and provenance contracts
  - [x] Evaluate the vendored authentext skill module for professional-register report generation and adopt it behind a thin contract where it passes privacy, provenance, and conformance gates

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Build replaceable interfaces

- [x] Task: Implement the phase scope
  - [x] Add capability discovery and an agent-guided setup workflow that recommends the smallest adequate optional profile
  - [x] Require the interface to show profile status, limits, privacy mode, installation source, health, and rollback
  - [x] Define CLI and API workflows for intake, validation, investigation, review, export, and automation
  - [x] Define bounded read, export, import, and reconciliation adapters for ims+ or another approved incident system without creating a shadow registry
  - [x] Assess approved Microsoft 365, SharePoint, Teams, Power Automate, Dataverse, or comparable enterprise surfaces before building collaboration or approval features
  - [x] Assess CMMN, BPMN, and DMN models and an existing organisational engine or Flowable before implementing workflow execution
  - [x] Map applicable FHIR Task, Questionnaire, QuestionnaireResponse, and DocumentReference exchanges where a source system supports them
  - [x] Prototype an optional local user interface through a maintained framework only for a demonstrated privacy, analysis, or evidence-review gap
  - [x] Define import and export adapters for Markdown, JSON, CSV, office documents, diagrams, and jurisdictional artefacts
  - [x] Keep the portable core usable without a specific UI or agent client

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Embed disclosure, participation, and support

- [x] Task: Implement the phase scope
  - [x] Embed open-disclosure preparation while preserving required human communication
  - [x] Support consumer and family questions, accounts, review, disagreement, and feedback
  - [x] Embed staff support, Just Culture, procedural fairness, and wellbeing prompts
  - [x] Embed Aboriginal cultural safety, accessibility, language, interpreter, and consultation needs

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Close the recommendation-to-effectiveness loop

- [x] Task: Implement the phase scope
  - [x] Define recommendation strength, rationale, hazards, controls, hierarchy, feasibility, and unintended consequences
  - [x] Assign action owners, dependencies, resources, deadlines, assurance evidence, and escalation
  - [x] Define implementation verification, outcome/process/balancing measures, review periods, and residual risk
  - [x] Link recommendation rationale to searched literature where warranted while keeping bibliographic integrity, evidence appraisal, local applicability, and authorised acceptance distinct
  - [x] Prevent action closure or report publication from implying effectiveness

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Produce auditable outputs

- [x] Task: Implement the phase scope
  - [x] Generate investigation, executive, consumer-facing, action, and effectiveness views from shared evidence
  - [x] Expose sources, citations, uncertainty, conflicts, model/runtime use, privacy mode, limitations, and approvals
  - [x] Apply bounded export, redaction, watermark, access, and retention policies
  - [x] Validate diagrams and documents without silently changing meaning

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Evaluate usability and oversight

- [x] Task: Implement the phase scope
  - [x] Test representative novice and expert journeys with synthetic cases
  - [x] Test accessibility, recovery, interruption, collaboration, correction, and disagreement
  - [x] Measure automation bias, missed evidence, unsafe certainty, and review burden
  - [x] Record product limitations and block clinical deployment pending separate approval

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #14 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [x] Task: Complete the track evidence pack
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [x] Close the GitHub issue only after the completion receipt passes
