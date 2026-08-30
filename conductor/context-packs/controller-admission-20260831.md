# Context Pack: Two-slot controller and observation admission

Track `eval-blocker-remediation_20260803`, root issue #1. Prepared as the next
bounded implementation after the guarded primary adapter and execution gate.
Reconcile its delivery receipt, branch ownership and hosted checks before
activation. Preparation is not an actual study freeze, capture or admission.

Delivery reconciled: PR #100 merged as
`135881d42b50a710744ff353c317af80316c8935`, with reviewed/merged tree
`0eee20b1eda6d1596bb74082ae70ecbc8058f5e3`. All seven PR checks and post-merge
conformance `33330379127` and Quality `33330379125` passed. Completed branch
cleanup was verified; clean successor `codex/prospective-controller-admission`
starts at that merge. Prior agent file ownership is released; assign fresh
bounded ownership before source edits. Root issue #1 remains open.

Heartbeat 2026-08-30T19:46:17Z resumed clean checkpoint `3ae9a3f` on the
same branch. Parent merge and both hosted checks were reverified; no overlapping
writer or enabled lease was found. Main owns integration/docs and evidence;
`runtime_profile_tests` owns both proposed modules, their direct tests and the
gate source-closure update. `root_acceptance_map` reviews acceptance;
`runtime_security_review` reviews safety/privacy and evidence integrity.
Exact agent model revisions are unavailable; correlated errors remain possible.
Unrelated Renovate PRs #93/#94 remain untouched.

The panel selected immediate admission through a private, one-shot,
non-serialisable controller-owned capability, consumed internally only after
both direct captures and verified journal persistence. Supplied JSON, paths or
hashes cannot mint that capability. The durable result records immediate
admission but cannot recreate it in another process: trusted offline custody
and scoring transitions remain separate future work. Persist attempt-start
before calling the primary entry; an exception may occur after execution and
must consume the attempt. No automatic retry or inferred resume is permitted.
This is a stricter execution subset of the protocol's retry allowance, not a
change to historical protocols. Implementation and validation remain pending.

## Panel recommendation and sequencing repair

Implement the exact two-slot controller and affirmative admission together
before actual source/protocol freeze. Freezing now would omit controller and
admission dependencies subsequently added to the execution path. This is an
in-scope sequencing repair under standing decisions 20260830-001/002, not a new
owner decision or another candidate-only readiness wrapper.

Reuse `run_primary`, the native protocol/request contract, existing gate and
fixed Git/file identity checks. Keep the READY entrypoint and all historical
H0–H8/H8P unchanged. Main owns integration, evidence and safety; assign bounded
implementation and acceptance agents after checking current ownership.

## Bounded inputs and ownership

Read AGENTS and `conductor/index.md`, owning spec/plan/metadata/cursor, workflow,
guidelines, standing decisions and the primary gate receipt. Load only the
gate/identity/primary session, native protocol/runner, existing preflight and
prospective inventory contracts and directly relevant tests. Do not read raw
historical outputs, inspect model caches or run a model in this slice.

Proposed owned modules are `prospective_study_controller.py` and
`prospective_observation_admission.py`, matching tests, and the narrow gate
closure update required to include these real dependencies. Agree concrete
journal/admission contracts before implementation; no new platform or signing
infrastructure. Reuse existing review commit R after source S and actual panel
records under the trusted repository workflow.

## Controller acceptance

- Validate the exact two-slot denominator and protocol/review identity before
  creating run resources. Each primary entry still performs its fresh gate.
- Own an exclusive, hash-bound execution journal and both raw receipts with
  canonical paths and no overwrite. Bind slot, request, response, source/review
  and runtime provenance; preserve all failures and expected-slot dispositions.
- Call `run_primary` at most once per declared slot. No automatic retry, silent
  denominator reduction, selective replacement or inferred resume after partial
  execution. Existing outputs, duplicates, drift and interruptions fail closed.
- Stop safely if a child or cleanup is uncertain; do not launch the next slot
  around the shared circuit breaker. Retain not-attempted dispositions honestly.

## Admission acceptance

- Recompute request/response/raw-receipt consistency against the immutable
  journal, exact native protocol and committed review evidence. Preserve raw
  bytes and complete provenance; never replace failed evidence with fixtures.
- Require both expected slots and all capture/cleanup/identity checks before
  affirmative admission-before-blinding. Keep scoring-start, adjudication,
  unblinding and analysis gates distinct and locked until their own evidence.
- A supplied JSON object, journal-shaped file or `execution_permitted=True`
  alone is not execution provenance. State the trusted capture/journal boundary
  explicitly; schema/hash consistency cannot establish actual process truth.
- Positive synthetic tests validate mechanics only and cannot be submitted as
  actual primary observations. Fail closed on fixture evidence, missing/forged/
  duplicated slots, mismatched requests, incomplete captures, stale identities,
  replaced journals, premature transitions and interrupted runs.

Exercise a composed synthetic success and adversarial failures through actual
controller/gate/admission logic, with explicit mock boundaries for environment,
profile/model and review provenance. Do not claim a success merely because
individual mocked helpers pass. Require meaningful coverage, native/Windows
types, full validation and final agent acceptance; fix bounded findings.

## Remaining authority and handoff

Add the controller/admission source identities to the reviewed execution
closure before freezing anything. Next only after implementation passes:
prepare actual synthetic protocol/inputs/rubric, establish reviewed S/R with
complete closure and clean-interpreter evidence, then gated two-slot execution
and admission. Preserve no-admissible-condition fallback and all negative data;
unfinished engineering is not fallback evidence.

No actual model/cache eligibility, model run, study freeze, observation admission,
blinding or scoring occurs in this implementation slice. Preserve Apache-2.0,
per-artefact rights, privacy, credentials, spend and external-action boundaries.
Agent review/agreement is not human agreement or clinical, legal, policy,
regulatory, employment, cultural-safety, organisational or deployment validation.
Record exact implemented versus pending checks and a durable next-action cursor;
do not archive the owning track or close root #1 from local or hosted tests.
