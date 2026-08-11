# Implementation Plan: Evaluation Blocker Remediation and Admission

Decision record: [decision-record.md](./decision-record.md)
Dispatch ledger: [dispatch-ledger.md](./dispatch-ledger.md)
Option A execution control: [option-a-execution-control.md](./option-a-execution-control.md)
External handoff: `evaluation/analysis/external-execution-request.md`

## Blocker strategy and trade-offs

The active execution runbook is
`evaluation/analysis/phase4-evidence-remediation-plan-20260808.md`. It governs
historical-evidence recovery versus canonical reruns and preserves the
fail-closed admission boundary.

| Option | Benefit | Trade-off | Contingency | Recommendation |
|---|---|---|---|---|
| A. Full primary evaluation | Preserves approved design and complete comparisons | Requires all operator/human evidence and credentials | Quarantine unrecoverable conditions and reassess under protocol governance | **Recommended** |
| B. Amended reduced scope | Produces bounded results when capacity is permanently unavailable | Requires protocol amendment; excludes comparisons and reduces denominators | Publish exclusions and revise claims boundary | Authorised decision required |
| C. Evidence-readiness closeout | Preserves implementation, validation, and governance outputs | Produces no Track 5/6 performance results | Retain handoff as a restart package | Use if execution is not feasible or authorised |

Decision rule: remain on A while execution is recoverable; select B only through
an authorised protocol amendment; select C when neither execution nor amendment
is feasible. Automation must not resolve human, licence, credential, or
protocol decisions by assumption.

## Phase 1: Baseline and controls

- [x] Record the current Phase 4 zero-eligibility audit.
- [x] Create the external operator/human evidence request.
- [x] Add Track 5 fail-closed preflight.
- [x] Add Track 6 fail-closed preflight.
- [x] Add Phase 4 admission preflight.
- [ ] Re-run the manifest audit after every external evidence submission.

## Phase 2: External evidence admission

### Phase 2A: Make Option A operational

- [ ] Appoint the study owner, admission custodian, condition operators,
  H8 evaluator coordinator, scoring custodian, IRR analyst, and reviewers.
- [ ] Record appointment, independence, authority, and conflict receipts.
- [ ] Complete harness-specific credential, trust, version, model, endpoint,
  parameter, retry, cost, and smoke-run preflights for H2-H7.
- [ ] Complete the H8 evaluator authority, confidentiality, conflict, and
  evidence-capture preflight.
- [ ] Start the T0 schedule and record all submission/escalation deadlines.
- [x] Implement the atomic slot-package admission validator and package template.
- [ ] Obtain and validate a complete positive primary-slot fixture.
- [ ] Apply the two-remediation-cycle rule and T0+22 irrecoverability review.

### Phase 2B: Execute and admit evidence

- [ ] Obtain H2 Claude Code/Opus raw runs and complete receipts.
- [ ] Obtain H3 Gemini raw runs and complete receipts.
- [ ] Resolve H4/H5 raw-to-normalized joins with attestations or reruns.
- [ ] Resolve H6/H7 harness identity and raw evidence.
- [ ] Obtain nine H8 Human Expert raw receipts and attestations.
- [ ] Remediate H0/H1 metadata and H0 path anomaly.
  - [x] Generate an evidence-only H0/H1 run manifest without reconstructing metadata.
  - [ ] Obtain operator dispositions and immutable metadata receipts or rerun affected slots.
- [ ] Admit only evidence satisfying the canonical manifest gate.
- [ ] Issue batch admission/quarantine receipts with diagnostics and owners.
- [ ] Obtain the final manifest admission receipt and pass Track 5 preflight.

## Phase 3: Track 5 unlock

- [ ] Run `tools/track5_preflight.ps1` and require pass.
- [ ] Freeze provisional scores and create sealed blinding IDs.
- [ ] Score admitted outputs blind with D1-D8 rationales.
- [ ] Run independent IRR scoring and weighted Cohen kappa.
- [ ] Remediate any dimension below kappa 0.60.
- [ ] Complete independent Track 5 closure review.

## Phase 4: Track 6 unlock

- [ ] Run `tools/track6_preflight.ps1` and require pass.
- [ ] Unblind the sealed dataset and record exclusions/missingness.
- [ ] Compute reproducible descriptive statistics and visualisations.
- [ ] Complete failure-mode analysis and claims audit.
- [ ] Keep H8P separately labelled.

## Phase 5: Independent Agent Skills workstream

- [x] Pin and run `skills-ref` validation.
- [x] Bundle approved workflow files and validate isolated portability.
- [x] Validate portable archive extraction.
- [x] Define and validate trigger/output fixture schemas.
- [x] Run Codex smoke and held-out fixture trials.
- [x] Run drift and privacy sentinels.
- [ ] Complete Gemini trials after trust/authentication approval.
- [ ] Complete client compatibility and final conformance review.

## Stop conditions

Stop and return a blocked receipt for missing raw evidence, unresolved joins,
absent authority, unavailable credentials, failed validation, licence
uncertainty, or any attempt to score/unblind before the relevant preflight.

## Decision and contingency gate

- [x] Record full-evaluation, reduced-scope, and readiness-only options.
- [x] Record rationale, contingencies, and decision authority.
- [x] Keep Option A active while H2-H8 execution is recoverable.
- [ ] Obtain an authorised protocol decision before selecting Option B or C.
- [ ] Update the manifest, acceptance criteria, and claims boundary if Option B
  or C is selected.
