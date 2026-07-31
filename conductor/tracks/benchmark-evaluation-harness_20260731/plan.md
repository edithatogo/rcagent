# Implementation Plan: Benchmark and Evaluation Harness

**GitHub:** [#10](https://github.com/edithatogo/rcagent/issues/10)

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

## Phase 1: Define benchmark governance

- [ ] Task: Implement the phase scope
  - [ ] Define intended decisions, populations, jurisdictions, modalities, exclusions, and misuse risks
  - [ ] Create dataset rights, consent, privacy, provenance, contamination, split, and version controls
  - [ ] Define benchmark retirement, drift, challenge, and correction processes
  - [ ] Map the legacy evaluation study without rewriting historical evidence

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Define metrics and gates

- [ ] Task: Implement the phase scope
  - [ ] Define investigation, systems-thinking, recommendation, action, and effectiveness measures
  - [ ] Define retrieval, citation, provenance, abstention, calibration, and robustness measures
  - [ ] Define privacy, security, cultural-safety, clinical-safety, and harmful-output hard gates
  - [ ] Define device latency, throughput, RAM, storage, context, power-proxy, and cost measures

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Build benchmark cases and rubrics

- [ ] Task: Implement the phase scope
  - [ ] Create synthetic and de-identified text, document, audio, image, and signal fixtures at appropriate governance levels
  - [ ] Create incomplete, conflicting, distracting, malicious, and policy-drift scenarios
  - [ ] Define gold evidence graphs, acceptable alternatives, and explicit unknowns
  - [ ] Create human-review rubrics and inter-rater calibration cases

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Implement reproducible runners

- [ ] Task: Implement the phase scope
  - [ ] Define model, runtime, prompt, retrieval, tool, device, seed, and environment manifests
  - [ ] Implement healthcare tasks, datasets, solvers, and scorers as Inspect AI extensions unless the fit-gap evidence rejects it
  - [ ] Bridge applicable standard language-model benchmarks through EleutherAI's Language Model Evaluation Harness rather than copying them
  - [ ] Assess local MLflow tracking for experiment and artefact lineage and Ragas or established retrieval measures for diagnostics
  - [ ] Compose deterministic orchestration, retries, timeouts, sampling, sandboxing, and raw-result preservation from the selected frameworks
  - [ ] Implement only project-specific scoring adapters, uncertainty intervals, clinical-safety gates, error taxonomy, and failure triage
  - [ ] Emit signed or hashed result receipts without sensitive content

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Run pilot baselines

- [ ] Task: Implement the phase scope
  - [ ] Run deterministic and retrieval-only baselines before generative models
  - [ ] Run representative small, medium, and larger generic-model comparators
  - [ ] Measure repeated-run variance, human agreement, device feasibility, and failure modes
  - [ ] Calibrate thresholds without leaking held-out test cases

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Reconcile and calibrate the evaluation estate

- [ ] Task: Implement the phase scope
  - [ ] Map H0-H8 cases, conditions, outputs, and scoring into the new schemas
  - [ ] Preserve incompatible historical results with explicit limitations
  - [ ] Set promotion, regression, and blocking thresholds from pilot evidence
  - [ ] Document which comparisons remain invalid or underpowered

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Automate regression and reporting

- [ ] Task: Implement the phase scope
  - [ ] Run bounded smoke, pull-request, release, device, privacy, and scheduled suites
  - [ ] Detect benchmark, model, runtime, source, and policy drift
  - [ ] Generate compact reports with raw evidence links and no unsupported ranking claims
  - [ ] Require owner approval before external publication

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #10 and dependency evidence

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
