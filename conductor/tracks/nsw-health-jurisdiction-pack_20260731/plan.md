# Implementation Plan: NSW Health Jurisdiction Pack

**GitHub:** [#9](https://github.com/edithatogo/rcagent/issues/9)

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

- [~] Task: Establish the system and dependency context — `dfaa8de`; review `6449410`
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention — `dfaa8de`; review `6449410`
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle — `dfaa8de`; review `6449410`
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Create the authoritative source registry

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Register applicable NSW Health policy directives including PD2020_047, PD2023_034, PD2025_032, PD2022_023, PD2025_031, and PD2026_001 for verification
  - [x] Register relevant CEC, ACI, ACSQHC, NSQHS, legislation, regulation, and local-policy source classes
  - [x] Promote national standards (NSQHS, ACSQHC frameworks, relevant Commonwealth legislation, national accreditation scheme) to a shared baseline tier that state packs inherit rather than duplicate
  - [x] Register Queensland Health and Clinical Excellence Queensland patient-safety, serious-adverse-event, open-disclosure, and clinical-governance source classes for verification before recording any directive identifiers
  - [x] Register Coroners Court of Queensland alongside NSW coronial sources
  - [x] Publish the generic jurisdiction-pack authoring guide and `jurisdiction-*` capability-profile registration workflow so additional states follow the same contracts without core changes
  - [x] Record issuer, authority, jurisdiction, status, version, dates, URLs, checksums, rights, and review cadence
  - [x] Link to source material rather than copying it until licence and operational need are clear
  - [x] Inventory ims+ and approved alternative incident-system fields, exports, imports, identifiers, workflow states, reports, and verified integration options
  - [x] Inventory approved Policy Distribution System, CEC, ACI, My Health Learning, SharePoint, and local procedure sources without duplicating their authoritative content
  - [x] Define which gaps require configuration or an authorised enterprise-system change rather than a workbench feature

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Model authority, version, and drift

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Define binding, mandatory, advisory, explanatory, draft, consultation, local, and superseded authority states
  - [x] Model commencement, review, replacement, conflict, and jurisdiction precedence
  - [x] Implement link, metadata, content-hash, and material-change detection
  - [x] Require human review for changes that alter policy meaning

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Map incident and investigation workflows

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Map notification, Severity Assessment Code, review type, serious-adverse-event, escalation, investigation, and closure steps
  - [x] Map initial submission, incident huddle, provisional checklist and harm assessment, review-team formation, interviews, consultation, findings, recommendations, actions, effectiveness, and closure requirements
  - [x] Map decision points and authority boundaries for lookback, cluster review, indicator review, individual-worker review, clinical risk, enterprise risk, cultural assessment, quality improvement, open disclosure, and medicolegal or regulatory pathways
  - [x] Map required roles, independence, consultation, timeframes, approvals, records, and exceptions
  - [x] Express rules through the canonical state and evidence contracts
  - [x] Expose policy uncertainty rather than inventing a missing rule

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Map forms, templates, and evidence requirements

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Inventory applicable CEC and NSW Health forms, tools, checklists, and reporting artefacts
  - [x] Map each field to the canonical data model and source requirement
  - [x] Create original interoperable templates only where permitted and useful
  - [x] Track restricted, linked-only, locally supplied, and generated artefacts

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Embed people, culture, and systems safeguards

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Map open disclosure and consumer/family participation requirements
  - [x] Map staff support, Just Culture, procedural fairness, and conflict-of-interest safeguards
  - [x] Embed Aboriginal cultural safety and appropriate consultation prompts
  - [x] Include proactive and systems methods alongside retrospective RCA

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Validate the jurisdiction mapping

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Trace every workflow rule and template field to current authority
  - [x] Test conflicting, missing, expired, under-review, and multi-jurisdiction scenarios
  - [x] Record unresolved interpretations as owner decisions with a recommended option
  - [x] Run policy and clinical-governance review without claiming organisational approval

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Operationalise policy drift

- [x] Task: Implement the phase scope — `dfaa8de`; review `6449410`
  - [x] Schedule authoritative-source checks with honest unavailable-upstream states
  - [x] Classify cosmetic, guidance, normative, and breaking changes
  - [x] Generate bounded review context and regression tests for material changes
  - [x] Invalidate affected compatibility and assurance receipts until review completes

- [x] Task: Validate the phase deliverables — `6449410`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #9 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `6449410`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [!] Task: Complete the track evidence pack
  - [ ] Resolve decision `20260829-001-active-under-review-pd2020-047`
  - [ ] Verify every acceptance criterion has direct evidence after the decision
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes

## Review Fixes

- [x] Task: Harden authority and drift gates — `6449410`
  - [x] Require strong authority before a rule may use mandatory language
  - [x] Require uncertainty disclosure for rules citing an under-review source
  - [x] Validate baseline and candidate snapshots before drift comparison
  - [x] Add a deterministic cadence queue and negative regression tests
