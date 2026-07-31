# Implementation Plan: Benchmark and Evaluation Harness

**GitHub:** [#10](https://github.com/edithatogo/rcagent/issues/10)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

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
  - [ ] Implement deterministic orchestration, retries, timeouts, sampling, and raw-result preservation
  - [ ] Implement scoring adapters, uncertainty intervals, error taxonomy, and failure triage
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
