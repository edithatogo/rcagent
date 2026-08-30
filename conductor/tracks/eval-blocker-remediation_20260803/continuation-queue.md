# Approved prospective continuation queue

This is the durable resume cursor for the approved synthetic Option B work,
not a new approval or a second task-status authority. The [plan](./plan.md)
owns task state; direct receipts prove completion. Start each run at
`conductor/index.md`, then reconcile this cursor with Git, open PRs, hosted
checks, decisions and the [root acceptance map](./root-acceptance-map-20260830.md).

## Resume cursor

- Run ID: `prospective-freeze-20260830`; reviewer class: agent.
- Implementation base: `b10abeb68df1258b3d82beec73aacc790ebce6b2`.
- Owning track: `eval-blocker-remediation_20260803`; issue #1 remains open.
- Integration branch: `codex/prospective-study-runner`; no worktree lease is
  enabled. This record is not a lock and does not authorise concurrent writes.
- Completed slice: [bounded runtime profile and live non-study observations](./runtime-profile-implementation-20260830.md)
  plus [read-only protocol-candidate validation](./protocol-contract-20260830.md).
  The original failed diagnostic is preserved. No study observation or score
  was generated; no actual protocol has been frozen.
- Implemented: [exact-commit protocol/reference/component verification](./freeze-verification-20260830.md)
  (`46dcf31`), with 19 focused tests and agent review. Full integration evidence
  must be checked against the enclosing PR's exact head before merging.
  The fresh runtime precheck failed before launch: the old executable, libomp
  and ggml backends are missing. Earlier successful observations remain valid
  only for their recorded time and bytes; do not infer current availability.
  [Recovery inspection](./runtime-drift-20260830.md) recommends a separately
  versioned installed-runtime candidate; exact component rights and pins must
  be reconciled before admission. Never overwrite the historical profile.
- Next implementation: a study-specific runner with deterministic output
  extraction, reusing the pinned runtime profile. Verify the pinned CLI's
  output-only mode or an exact wrapper parser on non-study fixtures, then bind
  actual adapter/input/rubric identities into a reviewed, committed protocol
  freeze. Implement affirmative admission separately; do not use READY probe
  output or candidate consistency as primary study evidence.
- Prior checkpoint: 683 local tests, 93.02% coverage; 116 focused tests at 100%.
  All seven hosted checks passed PR #83 head `2cc31da`; merged as `b10abeb`
  with exact tree parity. Both post-merge workflows passed. Its local branch
  was removed; GitHub had already removed the remote branch. These results do
  not validate later freeze-verifier changes.
- Scope ownership: the new freeze verifier/tests and linked records belong to
  this slice; the [context pack](../../context-packs/prospective-execution-20260830.md)
  records the runtime check and exclusions. Preserve overlapping active work.
- No unresolved owner decision for local implementation of this queue. The study execution gate is
  unfinished implementation and evidence, not missing reviewer approval.

## Dependency-ordered delivery

| Step | Deliverable and completion evidence | Failure or contingency |
| --- | --- | --- |
| 1. Runtime profile | Exact cached executable and non-system dependency pins, process-local selection, observed loader verification, bounded diagnostics and adversarial tests. Reuse the comparator adapter; no general dependency resolver or global Homebrew edits. | Missing or changed artefacts fail closed. Diagnose up to two evidence-led fixes; do not silently accept newer libraries. Record a concrete blocked condition, then continue protocol/fixture work. |
| 2. Implement study runner and freeze protocol | Implement and fixture-test deterministic raw capture/normalisation; then bind the actual adapter to a separate versioned synthetic study ID/condition, exact input/rubric bytes, denominator, generation settings, blinding method, three-agent scoring roles, adjudication and conservative non-operational thresholds. Agent-panel review and immutable hash-bound freeze precede study execution. | Candidate validation alone verifies none of the executable identities or Git freeze. Retain public-case exposure and correlated-agent limits; no held-out validity, full identity blinding, human reliability or statistical-power claim. |
| 3. Implement transitions | Positive/adversarial fixtures and affirmative protocol-bound admission-before-blinding, scoring-start and analysis validators; reject fixtures, stale hashes, omitted slots, incomplete raw joins and premature transitions. | Existing live preflights stay locked until their respective real receipts pass. Do not infer execution truth from schema/hash consistency alone. |
| 4. Execute and admit | Fresh synthetic slots under the frozen condition with complete raw/provenance packages, inspected public projections, exact scoped inventory and owned dispositions for every expected slot. | Preserve failures and denominators. No condition admissible after bounded recovery permits approved Option C readiness-only evidence, not invented results or fallback because code is unfinished. |
| 5. Score and analyse | Admission, blinded evidence packages, three independent-context agent submissions sealed before adjudication, preserved original scores/dissent, closure review, then gated unblinding and reproducible descriptive analysis. | Report agent agreement and unsupported/low-agreement results; do not tune scores/thresholds retrospectively to pass. Keep raw identity/custody separate from scorer context. |
| 6. Reconcile completion | Recheck owning and root acceptance maps, supported modes, current historical inventory gaps and concrete external prerequisites. Review and fix automatically; archive only when the owning acceptance criteria actually pass. | New study completion cannot close historical H0–H8/H8P or root #1 by implication. Preserve unavailable client execution and other external boundaries. |

Steps 1–3 are repository-owned implementation. Step 4 additionally requires
passing live condition/protocol admission. Steps 5–6 consume actual evidence;
they are not promised passes. The [standing decision](../../decisions/20260830-002-prospective-agent-study.md)
covers routine preparation, review, rework and the bounded fallback. No new
credentials, downloads, provider access, private data, rights exception,
distribution or spend is introduced by this queue. Apply any separately
recorded release/submission authority only to its exact eligible action.

## Continuation mechanism and stop rules

The Codex app confirmed creation of the hourly, same-task heartbeat
`continue-rcagent-approved-delivery` on 2026-08-30. Its configuration was
read back as active and bound to this task. This proves scheduling only, not
a future run, uninterrupted execution, admission or completion. Host/app
availability and usage limits can delay work. No separate task or repository
cron job was created. The app owns scheduling; this file owns only the cursor.

On each wake, resume an existing branch/PR before creating another. If another
writer owns overlapping work, skip the run without taking over its state.
Proceed across ready tasks, tests, agent reviews and bounded fixes without
another owner prompt. Update the cursor and evidence at every handoff; never
restart completed probes merely because a session resumed.

The owner's active goal explicitly authorises committing, opening PRs, waiting
for CI, merging and branch/worktree cleanup, one track at a time. Apply that
standing authority to reviewed exact-head green changes; do not ask again per
commit. It does not waive source rights, evidence, private-data or accountable
external-authority boundaries, and green checks alone do not prove completion.

Pause the heartbeat when the approved ready queue is exhausted, a safety
circuit breaker fires, or all remaining paths require genuinely new authority
or unavailable external action with no independent ready work. Record one
stable decision or wake condition rather than repeated unchanged requests.
Do not use missing historical human observations to block independent new
study engineering, or treat agent review as those observations.

## Review, authority and rollback

Use agent panels, not independent human repository reviewers. Clinical, legal,
policy, regulatory, employment, cultural-safety, organisational and deployment
validation remain outside repository completion. Private clinical/employee
data and credentials remain excluded. The approved Apache-2.0 licence and
per-artefact third-party rights controls are unchanged.

Rollback preserves all historical evidence and fail-closed preflights. Revert
only this documentation slice if needed; pause the app heartbeat separately
because a Git revert cannot stop a scheduled app task.
