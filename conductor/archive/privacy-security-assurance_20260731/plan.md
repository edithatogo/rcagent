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

## Phase 1: Model threats, data flows, and harms

- [x] Task: Implement the phase scope
  - [x] Create data-flow diagrams, trust zones, assets, actors, threat scenarios, and misuse cases
  - [x] Cover re-identification, inference, prompt injection, supply chain, unsafe output, and insider risks
  - [x] Create privacy, clinical-safety, cultural-safety, and information-governance impact methods
  - [x] Build de-identification sentinel fixtures covering both NSW Health and Queensland Health case formats, including QLD coronial data shapes
  - [x] Map controls to risks without claiming certification
  - [x] Profile applicable organisational security and privacy controls before adding project controls
  - [x] Map NIST AI RMF and Generative AI Profile, NIST Privacy Framework, OWASP GenAI guidance, MITRE ATLAS, and supply-chain standards to project risks
  - [x] Record where an enterprise platform control is authoritative, inherited, supplemented, unavailable, or out of scope

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Specify execution modes and compartments

- [x] Task: Implement the phase scope
  - [x] Define public remote, governed hybrid, fully local, and air-gapped mode contracts
  - [x] Separate public and private stores, indexes, caches, queues, logs, and receipts
  - [x] Define policy-based routing, capability discovery, and fail-closed defaults
  - [x] Define offline model, dependency, update, and time-source handling

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Design technical privacy and security controls

- [x] Task: Implement the phase scope
  - [x] Apply privacy, telemetry-off, egress, secrets, cache, retention, and deletion defaults to every optional capability installer
  - [x] Require agent-assisted setup to disclose downloads, external processing, storage, licences, and rollback before activation
  - [x] Specify encryption, key handling, secrets, access, session, and least-privilege controls
  - [x] Specify minimisation, de-identification, redaction, retention, deletion, backup, and recovery
  - [x] Disable or localise telemetry and prevent sensitive diagnostic output
  - [x] Define signed dependencies, model provenance, sandboxing, and remote-code restrictions

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence
  - [x] Reconcile the security elements of repository-hardening issues #17 and #18 without duplicating Track 01

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Define AI and clinical-safety gates

- [x] Task: Implement the phase scope
  - [x] Require execution disclosures before model or external-tool use
  - [x] Define evidence sufficiency, uncertainty, abstention, escalation, and reviewer checkpoints
  - [x] Separate assistance, analysis, policy mapping, clinical interpretation, and regulated-use boundaries
  - [x] Define unsafe-output quarantine and incident response

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Define legal, records, cultural, and disclosure safeguards

- [x] Task: Implement the phase scope
  - [x] Remove automatic privilege and blanket confidential-document claims
  - [x] Represent records, access, disclosure, open-disclosure, and consultation obligations as jurisdictional rules
  - [x] Embed Aboriginal cultural safety, consumer/family participation, staff support, and Just Culture principles
  - [x] Require unresolved legal or policy interpretation to remain an explicit decision

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Build adversarial and recovery tests

- [x] Task: Implement the phase scope
  - [x] Test egress, data leakage, prompt injection, malicious files, poisoned retrieval, and unsafe plugins
  - [x] Test de-identification, cross-compartment access, cache/log leakage, and deletion
  - [x] Test unavailable model, corrupt index, power/network loss, and recovery
  - [x] Test that denial, abstention, and escalation remain usable

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Produce mode-specific assurance cases

- [x] Task: Implement the phase scope
  - [x] Link risks, controls, tests, evidence, residual risks, owners, and review dates
  - [x] Create deployment checklists and incident, recovery, and key-compromise runbooks
  - [x] Verify assurance status is invalidated when dependencies or policies drift
  - [x] Record owner decisions without converting them into universal claims

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #8 and dependency evidence

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
  - [x] Close the GitHub issue only after the completion receipt and hosted integration pass

## Review Fixes

- [x] Task: Enforce fail-closed local-only and recovery boundaries — `a5ff002`
  - [x] Replace status-known booleans with explicit network and telemetry states
  - [x] Reject enabled network or telemetry in fully local and air-gapped modes
  - [x] Reject unknown destinations and preserve model-provenance denial
  - [x] Redact sensitive diagnostics and produce content-free deletion receipts
  - [x] Make model, index, network, power, and unknown recovery states fail closed
  - [x] Run 29 focused tests plus lint and type checks

- [x] Task: Remediate fresh-context false-completion findings — `aa597fe`
  - [x] Restrict public remote mode to public content
  - [x] Require complete, internally consistent model-result disclosures
  - [x] Require reviewable deletion verification without retaining resource identifiers
  - [x] Reject empty, duplicate, unavailable, stale, or evidence-free assurance cases
  - [x] Add executable malicious-artifact, poisoned-retrieval, and unsafe-plugin checks
  - [x] Add machine-readable security, privacy, cultural-safety, and clinical-safety assurance domains
  - [x] Correct the ledger's local-wall-clock-as-UTC evidence without rewriting append-only history
  - [x] Re-run focused and repository-wide validation, then review the corrected diff
  - [x] Close the hosted patch-coverage gap with fail-closed negative-path tests — `349e5f4`
  - [x] Pass hosted validation on exact head `17f28f4`, merge PR #45 as `ca07cfb`, and reconcile issue #8 closed

## Archival

- [x] Task: Archive the completed and revalidated track — `23a2463`; evidence `e78e022`
  - [x] Move the complete track without deleting its history or evidence
  - [x] Preserve the completed registry entry and redirect it to the archive
  - [x] Redirect roadmap, dependency, fixture, and integration-map links
  - [x] Re-run repository governance and the full applicable test suite after the move
  - [x] Teach repository governance to validate roadmap tracks in active or archived locations — `23a2463`
  - [x] Pass hosted checks, including Codecov patch, on exact archive content head `e78e022`
