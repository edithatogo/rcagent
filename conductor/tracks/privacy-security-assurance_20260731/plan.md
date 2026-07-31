# Implementation Plan: Privacy, Security, and Assurance

**GitHub:** [#8](https://github.com/edithatogo/rcagent/issues/8)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Model threats, data flows, and harms

- [ ] Task: Implement the phase scope
  - [ ] Create data-flow diagrams, trust zones, assets, actors, threat scenarios, and misuse cases
  - [ ] Cover re-identification, inference, prompt injection, supply chain, unsafe output, and insider risks
  - [ ] Create privacy, clinical-safety, cultural-safety, and information-governance impact methods
  - [ ] Map controls to risks without claiming certification

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Specify execution modes and compartments

- [ ] Task: Implement the phase scope
  - [ ] Define public remote, governed hybrid, fully local, and air-gapped mode contracts
  - [ ] Separate public and private stores, indexes, caches, queues, logs, and receipts
  - [ ] Define policy-based routing, capability discovery, and fail-closed defaults
  - [ ] Define offline model, dependency, update, and time-source handling

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Design technical privacy and security controls

- [ ] Task: Implement the phase scope
  - [ ] Specify encryption, key handling, secrets, access, session, and least-privilege controls
  - [ ] Specify minimisation, de-identification, redaction, retention, deletion, backup, and recovery
  - [ ] Disable or localise telemetry and prevent sensitive diagnostic output
  - [ ] Define signed dependencies, model provenance, sandboxing, and remote-code restrictions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Define AI and clinical-safety gates

- [ ] Task: Implement the phase scope
  - [ ] Require execution disclosures before model or external-tool use
  - [ ] Define evidence sufficiency, uncertainty, abstention, escalation, and reviewer checkpoints
  - [ ] Separate assistance, analysis, policy mapping, clinical interpretation, and regulated-use boundaries
  - [ ] Define unsafe-output quarantine and incident response

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Define legal, records, cultural, and disclosure safeguards

- [ ] Task: Implement the phase scope
  - [ ] Remove automatic privilege and blanket confidential-document claims
  - [ ] Represent records, access, disclosure, open-disclosure, and consultation obligations as jurisdictional rules
  - [ ] Embed Aboriginal cultural safety, consumer/family participation, staff support, and Just Culture principles
  - [ ] Require unresolved legal or policy interpretation to remain an explicit decision

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Build adversarial and recovery tests

- [ ] Task: Implement the phase scope
  - [ ] Test egress, data leakage, prompt injection, malicious files, poisoned retrieval, and unsafe plugins
  - [ ] Test de-identification, cross-compartment access, cache/log leakage, and deletion
  - [ ] Test unavailable model, corrupt index, power/network loss, and recovery
  - [ ] Test that denial, abstention, and escalation remain usable

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Produce mode-specific assurance cases

- [ ] Task: Implement the phase scope
  - [ ] Link risks, controls, tests, evidence, residual risks, owners, and review dates
  - [ ] Create deployment checklists and incident, recovery, and key-compromise runbooks
  - [ ] Verify assurance status is invalidated when dependencies or policies drift
  - [ ] Record owner decisions without converting them into universal claims

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence

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
