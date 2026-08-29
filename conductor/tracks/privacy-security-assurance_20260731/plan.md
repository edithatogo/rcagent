# Implementation Plan: Privacy, Security, and Assurance

**GitHub:** [#8](https://github.com/edithatogo/rcagent/issues/8)

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

## Phase 1: Model threats, data flows, and harms

- [ ] Task: Implement the phase scope
  - [ ] Create data-flow diagrams, trust zones, assets, actors, threat scenarios, and misuse cases
  - [ ] Cover re-identification, inference, prompt injection, supply chain, unsafe output, and insider risks
  - [ ] Create privacy, clinical-safety, cultural-safety, and information-governance impact methods
  - [ ] Build de-identification sentinel fixtures covering both NSW Health and Queensland Health case formats, including QLD coronial data shapes
  - [ ] Map controls to risks without claiming certification
  - [ ] Profile applicable organisational security and privacy controls before adding project controls
  - [ ] Map NIST AI RMF and Generative AI Profile, NIST Privacy Framework, OWASP GenAI guidance, MITRE ATLAS, and supply-chain standards to project risks
  - [ ] Record where an enterprise platform control is authoritative, inherited, supplemented, unavailable, or out of scope

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
  - [ ] Apply privacy, telemetry-off, egress, secrets, cache, retention, and deletion defaults to every optional capability installer
  - [ ] Require agent-assisted setup to disclose downloads, external processing, storage, licences, and rollback before activation
  - [ ] Specify encryption, key handling, secrets, access, session, and least-privilege controls
  - [ ] Specify minimisation, de-identification, redaction, retention, deletion, backup, and recovery
  - [ ] Disable or localise telemetry and prevent sensitive diagnostic output
  - [ ] Define signed dependencies, model provenance, sandboxing, and remote-code restrictions

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #8 and dependency evidence
  - [ ] Reconcile the security elements of repository-hardening issues #17 and #18 without duplicating Track 01

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
