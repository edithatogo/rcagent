# Implementation Plan: Benchmark and Evaluation Harness

**GitHub:** [#10](https://github.com/edithatogo/rcagent/issues/10)

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

- [x] Task: Establish the system and dependency context — `7a7257e`
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention — `7a7257e`
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle — `7a7257e`
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define benchmark governance

- [x] Task: Implement the phase scope — `7a7257e`
  - [x] Define intended decisions, populations, jurisdictions, modalities, exclusions, and misuse risks
  - [x] Create dataset rights, consent, privacy, provenance, contamination, split, and version controls
  - [x] Define benchmark retirement, drift, challenge, and correction processes
  - [x] Map the legacy evaluation study without rewriting historical evidence

- [x] Task: Validate the phase deliverables — `7a7257e`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Define metrics and gates

- [x] Task: Implement the phase scope — `7a7257e`
  - [x] Define investigation, systems-thinking, recommendation, action, and effectiveness measures
  - [x] Define retrieval, citation, provenance, abstention, calibration, and robustness measures
  - [x] Define privacy, security, cultural-safety, clinical-safety, and harmful-output hard gates
  - [x] Define device latency, throughput, RAM, storage, context, power-proxy, and cost measures

- [x] Task: Validate the phase deliverables — `7a7257e`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Build benchmark cases and rubrics

- [x] Task: Implement the phase scope — `7a7257e`
  - [x] Create synthetic and de-identified text, document, audio, image, and signal fixtures at appropriate governance levels
  - [x] Create incomplete, conflicting, distracting, malicious, and policy-drift scenarios
  - [x] Define gold evidence graphs, acceptable alternatives, and explicit unknowns
  - [x] Create human-review rubrics and inter-rater calibration cases

- [x] Task: Validate the phase deliverables — `7a7257e`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Implement reproducible runners

- [x] Task: Implement the phase scope — `7a7257e`
  - [x] Define model, runtime, prompt, retrieval, tool, device, seed, and environment manifests
  - [x] Implement healthcare tasks, datasets, solvers, and scorers as Inspect AI extensions unless the fit-gap evidence rejects it
  - [x] Bridge applicable standard language-model benchmarks through EleutherAI's Language Model Evaluation Harness rather than copying them
  - [x] Assess local MLflow tracking for experiment and artefact lineage and Ragas or established retrieval measures for diagnostics
  - [x] Compose deterministic orchestration, retries, timeouts, sampling, sandboxing, and raw-result preservation from the selected frameworks
  - [x] Implement only project-specific scoring adapters, uncertainty intervals, clinical-safety gates, error taxonomy, and failure triage
  - [x] Emit signed or hashed result receipts without sensitive content

- [x] Task: Validate the phase deliverables — `7a7257e`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Run pilot baselines

- [!] Task: Implement the phase scope — deterministic baseline `7a7257e`; manifest fix `b954a33`
  - [x] Run deterministic and retrieval-only baselines before generative models
  - [!] Run representative small, medium, and larger generic-model comparators — decision `20260829-002-track05-comparator-staging`
  - [!] Measure repeated-run variance, human agreement, device feasibility, and failure modes — device proxy complete; model and human observations await the decision
  - [!] Calibrate thresholds without leaking held-out test cases — structural hard gates exist; operational thresholds require pilot evidence and owner authority

- [x] Task: Validate the available phase deliverables — `b954a33`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards after the decision
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically through unaffected work
  - [x] Apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Reconcile and calibrate the evaluation estate

- [!] Task: Implement the phase scope — `7a7257e`
  - [x] Map H0-H8 cases, conditions, outputs, and scoring into the new schemas
  - [x] Preserve incompatible historical results with explicit limitations
  - [!] Set promotion, regression, and blocking thresholds from pilot evidence — operational thresholds remain an owner gate
  - [x] Document which comparisons remain invalid or underpowered

- [x] Task: Validate the available phase deliverables — `b954a33`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards after the decision
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically through unaffected work
  - [x] Apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Automate regression and reporting

- [x] Task: Implement the phase scope — `7a7257e`
  - [x] Run bounded smoke, pull-request, release, device, privacy, and scheduled suites
  - [x] Detect benchmark, model, runtime, source, and policy drift
  - [x] Generate compact reports with raw evidence links and no unsupported ranking claims
  - [x] Require owner approval before external publication

- [x] Task: Validate the phase deliverables — `7a7257e`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `7a7257e`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [!] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence after decision `20260829-002-track05-comparator-staging`
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes

## Review Fixes

- [x] Task: Record the exact deterministic execution manifest — `b954a33`
  - [x] Record model, runtime, prompt, retrieval, tools, device, seed, sampling, retry, timeout, sandbox and network state
  - [x] Preserve a hashed receipt and explicit nonpublication limitations
  - [x] Use a cross-platform Python allocation peak instead of platform-specific resident-set APIs

- [x] Task: Close measurement and fixture-validation gaps — `03bd75e`
  - [x] Emit citation validity and robustness challenge outcomes in every case receipt
  - [x] Emit fixture storage bytes alongside latency, throughput, allocation peak, context and CPU-energy proxy
  - [x] Define recommendation, action-assurance and effectiveness measures without claiming human scores
  - [x] Reject malformed fixtures before runner execution
