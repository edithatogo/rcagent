# Implementation Plan: NSW Health Jurisdiction Pack

**GitHub:** [#9](https://github.com/edithatogo/rcagent/issues/9)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Create the authoritative source registry

- [ ] Task: Implement the phase scope
  - [ ] Register applicable NSW Health policy directives including PD2020_047, PD2023_034, PD2025_032, PD2022_023, PD2025_031, and PD2026_001 for verification
  - [ ] Register relevant CEC, ACI, ACSQHC, NSQHS, legislation, regulation, and local-policy source classes
  - [ ] Record issuer, authority, jurisdiction, status, version, dates, URLs, checksums, rights, and review cadence
  - [ ] Link to source material rather than copying it until licence and operational need are clear

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Model authority, version, and drift

- [ ] Task: Implement the phase scope
  - [ ] Define binding, mandatory, advisory, explanatory, draft, consultation, local, and superseded authority states
  - [ ] Model commencement, review, replacement, conflict, and jurisdiction precedence
  - [ ] Implement link, metadata, content-hash, and material-change detection
  - [ ] Require human review for changes that alter policy meaning

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Map incident and investigation workflows

- [ ] Task: Implement the phase scope
  - [ ] Map notification, Severity Assessment Code, review type, serious-adverse-event, escalation, investigation, and closure steps
  - [ ] Map required roles, independence, consultation, timeframes, approvals, records, and exceptions
  - [ ] Express rules through the canonical state and evidence contracts
  - [ ] Expose policy uncertainty rather than inventing a missing rule

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Map forms, templates, and evidence requirements

- [ ] Task: Implement the phase scope
  - [ ] Inventory applicable CEC and NSW Health forms, tools, checklists, and reporting artefacts
  - [ ] Map each field to the canonical data model and source requirement
  - [ ] Create original interoperable templates only where permitted and useful
  - [ ] Track restricted, linked-only, locally supplied, and generated artefacts

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Embed people, culture, and systems safeguards

- [ ] Task: Implement the phase scope
  - [ ] Map open disclosure and consumer/family participation requirements
  - [ ] Map staff support, Just Culture, procedural fairness, and conflict-of-interest safeguards
  - [ ] Embed Aboriginal cultural safety and appropriate consultation prompts
  - [ ] Include proactive and systems methods alongside retrospective RCA

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Validate the jurisdiction mapping

- [ ] Task: Implement the phase scope
  - [ ] Trace every workflow rule and template field to current authority
  - [ ] Test conflicting, missing, expired, under-review, and multi-jurisdiction scenarios
  - [ ] Record unresolved interpretations as owner decisions with a recommended option
  - [ ] Run policy and clinical-governance review without claiming organisational approval

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Operationalise policy drift

- [ ] Task: Implement the phase scope
  - [ ] Schedule authoritative-source checks with honest unavailable-upstream states
  - [ ] Classify cosmetic, guidance, normative, and breaking changes
  - [ ] Generate bounded review context and regression tests for material changes
  - [ ] Invalidate affected compatibility and assurance receipts until review completes

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #9 and dependency evidence

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
