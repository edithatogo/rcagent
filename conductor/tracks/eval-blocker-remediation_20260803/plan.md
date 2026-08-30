# Implementation Plan: Evaluation Blocker Remediation and Admission

Decision record: [decision-record.md](./decision-record.md)
Dispatch ledger: [dispatch-ledger.md](./dispatch-ledger.md)
Option A execution control: [option-a-execution-control.md](./option-a-execution-control.md)
External handoff: `evaluation/analysis/external-execution-request.md`

## Current review authority (2026-08-30)

[Approved agent-review substitution](../../decisions/20260830-001-legacy-agent-review.md)
governs repository reviews, overriding human-review appointments in the older
runbooks. Human comparator data, operator provenance and accountable authority
are not review duties. The historical Option A remains incomplete/unadmitted; the
[recommended prospective Option B](../../decisions/20260830-002-prospective-agent-study.md)
was explicitly approved on 2026-08-30 with readiness-only Option C fallback.
Implement the new synthetic study separately; historical Option A remains
incomplete. No further reviewer or routine phase approval is required.

## Next repository-owned slice

- [x] Replace external-human repository review requirements with the standing
  agent-panel protocol; preserve H8 and historical evidence identity.
- [~] Replace prose-regex preflights with affirmative, revision/hash-bound
  admission and scoring-completion receipts; distinguish before-blinding and
  scoring-start checks.
  - [x] Remove permissive legacy passes and separate fixture integrity from
    live transitions: [hardening boundary](./preflight-hardening-20260830.md).
  - [ ] Implement protocol-bound semantic validation before enabling live passes.
  - [x] Capture a bounded local non-study execution probe using existing
    comparator admission, with raw output and invocation provenance (`852c8d8`):
    [receipt and boundaries](./local-execution-provenance-20260830.md).
  - [x] Implement and verify a bounded pinned Darwin runtime dependency profile
    (`478f799`): [evidence](./runtime-profile-implementation-20260830.md).
    Retain OS/loader limitations; non-study success does not admit a study.
- [~] Add synthetic positive and adversarial fixtures, including empty prose,
  header-only CSV, stale hashes and fixture-as-study-evidence rejection.
- [~] Produce a fresh eligibility inventory; historical zero eligibility is
  not evidence of a current full inventory audit.
  - [x] Establish a separate prospective planning manifest and scoped inventory
    (`b0bbcc6`): [evidence](./prospective-inventory-20260830.md). No historical
    audit, executable-condition admission or study freeze implied.
- [x] Produce a root #1 acceptance map without closing it from child counts,
  and record the [durable continuation queue](./continuation-queue.md) (`3b2142f`).
- [x] Record owner approval of prospective Option B with Option C fallback.
- [ ] Implement the approved versioned protocol and admission gates; approval
  is not evidence of completed implementation or an admitted study cohort.
  - [x] Add a strict read-only prospective protocol-candidate contract and
    adversarial fixtures (`3114c01`): [evidence](./protocol-contract-20260830.md).
    Candidate consistency does not assert freeze or admission.
  - [x] Implement exact committed protocol/reference/component byte checks
    (`46dcf31`): [contract and boundaries](./freeze-verification-20260830.md).
    This consistency-only verifier neither admits nor unlocks execution; the
    actual runner/component closure and protocol freeze remain pending.
  - [x] Review fix: cover all freeze-verifier error paths (`a302486`), with
    30 focused tests at 100% statement/branch coverage; retain production gates.
  - [x] Add and verify a separate llama 0.3 runtime profile using exact installed
    bytes and component-level licence evidence; preserve the old profile.
    [Evidence](./runtime-v030-20260830.md): 739 tests, agent review and live
    version/help diagnostics; no model inference or study admission.
  - [x] Implement a fixed synthetic output-mode probe using an explicit runtime
    overlay and unchanged model-rights checks; establish observed output grammar
    before implementing normalisation (`a82acb1`).
    [Evidence](./output-mode-probe-20260830.md): 776 tests and one complete live
    probe; stdout remains wrapped, so response-only normalisation is unverified.
  - [~] Establish a strict, implementation-supported output grammar or separately
    admitted response-only entrypoint, then implement deterministic normalisation.
    - [x] Reject lossy CLI wrapper recovery and implement a read-only native JSON
      contract (`9038d51`): [source/panel/test evidence](./structured-completion-20260830.md).
      Both agent reviews passed; 871 full tests, 93.38% coverage, 95 decoder tests
      at 100%. Server entrypoint, runner, transport, protocol mode integration
      and actual study admission remain pending under the
      [bounded context](../../context-packs/structured-completion-20260830.md).
    - [~] Verify a separate server-entrypoint profile and implement bounded
      Unix-socket HTTP capture under the
      [server context](../../context-packs/server-capture-20260830.md).
      Child-process lifecycle and model probe remain separate pending work.

## Historical design and current execution choice

The active execution runbook is
`evaluation/analysis/phase4-evidence-remediation-plan-20260808.md`. It governs
historical-evidence recovery versus canonical reruns and preserves the
fail-closed admission boundary.

| Option | Benefit | Trade-off | Contingency | Recommendation |
|---|---|---|---|---|
| A. Full primary evaluation | Preserves approved design and complete comparisons | Requires all operator/human evidence and credentials | Quarantine unrecoverable conditions and reassess under protocol governance | **Recommended** |
| B. Amended reduced scope | Produces bounded results when capacity is permanently unavailable | Requires protocol amendment; excludes comparisons and reduces denominators | Publish exclusions and revise claims boundary | Authorised decision required |
| C. Evidence-readiness closeout | Preserves implementation, validation, and governance outputs | Produces no Track 5/6 performance results | Retain handoff as a restart package | Use if execution is not feasible or authorised |

The table records the historical alternatives, not a new approval request.
Current execution follows approved decision 20260830-002: implement a separate
synthetic Option B study and use Option C if no condition is admissible.
Historical Option A evidence remains preserved and incomplete. Do not recruit
human reviewers or re-request B/C selection. Licence, credential and other
reserved actions still require applicable exact-scope authority.

## Phase 1: Baseline and controls

- [x] Record the current Phase 4 zero-eligibility audit.
- [x] Create the external operator/human evidence request.
- [x] Add Track 5 fail-closed preflight.
- [x] Add Track 6 fail-closed preflight.
- [x] Add Phase 4 admission preflight.
- [ ] Re-run the manifest audit after every external evidence submission.

## Phase 2: External evidence admission

### Phase 2A: Make Option A operational

- [ ] Record accountable study/protocol owner and condition execution roles;
  H8 coordinator applies only if the historical human condition is retained.
- [ ] Assign repository review/scoring-custody roles to agents and record
  revisions, isolation, conflicts, evidence hashes and correlated-error limits;
  retain separate accountable-authority and operator provenance receipts.
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
- [ ] Run blind agent research scoring under the approved versioned study
  protocol; report agent agreement, not human reliability.
- [ ] Retain low agreement and original scores; version rubric revisions
  prospectively and record unsupported outcomes rather than tuning to pass.
- [ ] Complete fresh-context agent-panel Track 5 closure review.

## Phase 4: Track 6 unlock

- [ ] Run `tools/track6_preflight.ps1` and require pass.
- [ ] Unblind the sealed dataset and record exclusions/missingness.
- [ ] Compute reproducible descriptive statistics and visualisations.
- [ ] Complete deterministic failure-mode analysis and agent-panel claims audit.
- [ ] Keep H8P separately labelled.

## Phase 5: Independent Agent Skills workstream

- [x] Pin and run `skills-ref` validation.
- [x] Bundle approved workflow files and validate isolated portability.
- [x] Validate portable archive extraction.
- [x] Define and validate trigger/output fixture schemas.
- [x] Run Codex smoke and held-out fixture trials.
- [x] Run drift and privacy sentinels.
- [ ] Complete Gemini trials after trust/authentication approval.
- [ ] Complete agent-panel client compatibility and conformance review using
  actual client trial receipts; no panel vote replaces missing execution.

## Stop conditions

Stop and return a blocked receipt for missing raw evidence, unresolved joins,
absent authority, unavailable credentials, failed validation, licence
uncertainty, or any attempt to score/unblind before the relevant preflight.

## Decision and contingency gate

- [x] Record full-evaluation, reduced-scope, and readiness-only options.
- [x] Record rationale, contingencies, and decision authority.
- [x] Preserve the historical Option A decision; the approved new synthetic
  study does not retrospectively complete or relabel its observations.
- [x] Obtain an authorised protocol decision — decision 20260830-002 approves
  a new synthetic Option B study with Option C fallback; no repeat request.
- [ ] Implement the new study manifest, acceptance criteria and claims boundary
  under approved Option B, with an evidence-backed Option C fallback.
