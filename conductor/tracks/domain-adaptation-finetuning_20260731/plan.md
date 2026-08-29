# Implementation Plan: Domain Adaptation and Fine-Tuning

**GitHub:** [#15](https://github.com/edithatogo/rcagent/issues/15)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Recorded outcome boundary

Checked items record completion of the bounded assessment, contract, or stop-path disposition. They do not claim that comparator runs, data admission, de-identification, training, gain measurement, model-card creation, adapted weights, promotion, or release occurred. Current repository outcome: `not_ready_reject_weight_adaptation`; all model/framework candidates remain unavailable or contract-only, the synthetic split manifest is validator test evidence only, and no training recipe is executable.

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

## Phase 1: Establish adaptation readiness

- [x] Task: Implement the phase scope
  - [x] Assess target-task readiness; record target task, users, minimum meaningful improvement, and target-specific risks as not defined, so the pre-experiment stop disposition applies
  - [x] Verify benchmark maturity, data need, rights, privacy, compute, licence, and maintenance capacity
  - [x] Prefer deterministic, retrieval, prompting, and adapter changes before weight updates
  - [x] Require an owner decision for any private data, spend, licence exception, or release

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Evaluate domain model comparators

- [x] Task: Implement the phase scope
  - [x] Assess Microsoft medical and other domain-model candidates; admit no exact revision without local primary evidence
  - [x] Assess common-baseline availability; record comparison as not executed because no eligible exact model baseline exists
  - [x] Assess knowledge, calibration, citations, context, privacy, licence, device fit, and failure modes
  - [x] Reject vendor or leaderboard claims that cannot be reproduced

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Create governed adaptation data

- [x] Task: Implement the phase scope
  - [x] Define collection, rights, consent, purpose, minimisation, de-identification, lineage, and deletion
  - [x] Define empty generated-synthetic train, validation, held-out, challenge, and contamination-control split contract slots; create no fixtures and admit no training dataset
  - [x] Assess representativeness, label reliability, leakage, bias, and hidden policy signals
  - [x] Record the data-card requirements as not reached and create a hash-bound, unmaterialised dataset-contract manifest

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Run least-complexity experiments first

- [x] Task: Implement the phase scope
  - [x] Assess whether retrieval, prompt, structured-output, tool, and lightweight adapter approaches can be compared; record comparison as not executed because no eligible common baseline exists
  - [x] Evaluate the training-path admission gate; select no framework because no exact maintained revision is admitted
  - [x] Evaluate the run-lineage gate; use no tracker because no experiment is authorised or executed
  - [x] Apply the readiness stop rule before LoRA or other parameter-efficient training; no framework is selected and no training runs
  - [x] Record the dry-run contract, negative readiness receipt, exact dependency hashes, zero compute, and absence of base revisions or intermediate artefacts
  - [x] Apply the pre-experiment readiness stop gate; no experiment starts and no privacy, safety, instability, or gain condition is observed

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Evaluate gains and regressions

- [x] Task: Implement the phase scope
  - [x] Record held-out quality, retrieval, calibration, safety, privacy, fairness, robustness, and policy-drift suites as not reached with null metrics because no run exists
  - [x] Record device latency, memory, storage, energy proxy, context, and maintenance burden as not measured because no run exists
  - [x] Record repeated-run and confidence-interval comparison as not reached because no eligible common baseline or run exists
  - [x] Record regression investigation as not reached; preserve null metrics rather than inventing or averaging results

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Document governance and lineage

- [x] Task: Implement the phase scope
  - [x] Record the conditional model-card and training-provenance requirements in a rejection card; create no model card for a nonexistent artefact
  - [x] Document de-identification, residual re-identification risk, memorisation, and deletion limitations
  - [x] State the research, clinical, and medical-device boundaries
  - [x] Record conditional incident, rollback, deprecation, and upstream-base-change requirements in the rejection card; no operational procedure or artefact was activated

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Promote, constrain, or reject

- [x] Task: Implement the phase scope
  - [x] Apply evidence-based quality, safety, privacy, licence, device, and maintenance gates
  - [x] Select supported, experimental, research-only, constrained, or rejected status
  - [x] Require owner approval before distribution, clinical claims, or use with private data
  - [x] Preserve negative results and the decision rationale

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #15 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [ ] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence
  - [ ] Re-run the complete applicable validation and regression suite
  - [ ] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [ ] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes
