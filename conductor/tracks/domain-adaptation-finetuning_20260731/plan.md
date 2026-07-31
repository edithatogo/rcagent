# Implementation Plan: Domain Adaptation and Fine-Tuning

**GitHub:** [#15](https://github.com/edithatogo/rcagent/issues/15)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Establish adaptation readiness

- [ ] Task: Implement the phase scope
  - [ ] Define the target task, baseline gap, minimum meaningful improvement, risks, users, and rollback
  - [ ] Verify benchmark maturity, data need, rights, privacy, compute, licence, and maintenance capacity
  - [ ] Prefer deterministic, retrieval, prompting, and adapter changes before weight updates
  - [ ] Require an owner decision for any private data, spend, licence exception, or release

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Evaluate domain model comparators

- [ ] Task: Implement the phase scope
  - [ ] Identify current Microsoft medical and other relevant domain models by exact revision and evidence
  - [ ] Compare them with generic baselines on the same bounded benchmark
  - [ ] Assess knowledge, calibration, citations, context, privacy, licence, device fit, and failure modes
  - [ ] Reject vendor or leaderboard claims that cannot be reproduced

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Create governed adaptation data

- [ ] Task: Implement the phase scope
  - [ ] Define collection, rights, consent, purpose, minimisation, de-identification, lineage, and deletion
  - [ ] Create train, validation, held-out, challenge, and contamination-control splits
  - [ ] Assess representativeness, label reliability, leakage, bias, and hidden policy signals
  - [ ] Generate data cards and immutable manifests

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Run least-complexity experiments first

- [ ] Task: Implement the phase scope
  - [ ] Compare retrieval, prompt, structured-output, tool, and lightweight adapter approaches
  - [ ] Run LoRA or other parameter-efficient training only when readiness remains satisfied
  - [ ] Record exact code, configuration, seed, base revision, dependencies, compute, and intermediate artefacts
  - [ ] Stop experiments early for privacy, safety, instability, or non-material gains

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Evaluate gains and regressions

- [ ] Task: Implement the phase scope
  - [ ] Run held-out quality, retrieval, calibration, safety, privacy, fairness, robustness, and policy-drift suites
  - [ ] Measure device latency, memory, storage, energy proxy, context, and maintenance burden
  - [ ] Compare repeated runs and confidence intervals against every relevant baseline
  - [ ] Investigate regressions rather than averaging them away

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Document governance and lineage

- [ ] Task: Implement the phase scope
  - [ ] Create model cards, training and evaluation provenance, intended and out-of-scope uses, and licences
  - [ ] Document de-identification, residual re-identification risk, memorisation, and deletion limitations
  - [ ] State the research, clinical, and medical-device boundaries
  - [ ] Create incident, rollback, deprecation, and upstream-base-change procedures

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Promote, constrain, or reject

- [ ] Task: Implement the phase scope
  - [ ] Apply evidence-based quality, safety, privacy, licence, device, and maintenance gates
  - [ ] Select supported, experimental, research-only, constrained, or rejected status
  - [ ] Require owner approval before distribution, clinical claims, or use with private data
  - [ ] Preserve negative results and the decision rationale

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #15 and dependency evidence

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
