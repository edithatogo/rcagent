# Approved prospective continuation queue

This is the durable resume cursor for the approved synthetic Option B work,
not a new approval or a second task-status authority. The [plan](./plan.md)
owns task state; direct receipts prove completion. Start each run at
`conductor/index.md`, then reconcile this cursor with Git, open PRs, hosted
checks, decisions and the [root acceptance map](./root-acceptance-map-20260830.md).

## Resume cursor

- Run ID: `server-capture-20260830`; reviewer class: agent.
- Implementation base: `19747637b248b82b4522551caf44fab7c87469ba`.
- Owning track: `eval-blocker-remediation_20260803`; issue #1 remains open.
- Integration branch: `codex/server-capture-foundation`; no worktree lease is
  enabled. This record is not a lock and does not authorise concurrent writes.
- Completed slice: [bounded runtime profile and live non-study observations](./runtime-profile-implementation-20260830.md)
  plus [read-only protocol-candidate validation](./protocol-contract-20260830.md).
  The original failed diagnostic is preserved. No study observation or score
  was generated; no actual protocol has been frozen.
- Implemented: [exact-commit protocol/reference/component verification](./freeze-verification-20260830.md)
  (`46dcf31`), with agent review and expanded 30-test/100%-coverage fixtures
  (`a302486`). PR #84 passed all seven checks at head `8e70082`, merged as
  `4582b8e` with exact tree parity, and passed both post-merge workflows.
  Its obsolete local branch was removed after verification.
  The fresh runtime precheck failed before launch: the old executable, libomp
  and ggml backends are missing. Earlier successful observations remain valid
  only for their recorded time and bytes; do not infer current availability.
  [Recovery inspection](./runtime-drift-20260830.md) recommends a separately
  versioned installed-runtime candidate; exact component rights and pins must
  be reconciled before admission. Never overwrite the historical profile.
- Completed slice: [explicit runtime 0.3.0 profile](./runtime-v030-20260830.md).
  Agent panel checked installed component/licence bytes and preserved metadata
  contradictions. Legacy defaults remain unchanged. Initial 739 tests passed
  (93.19% coverage); live version/help diagnostics passed all 16 loaded-image
  pins. PR #85 additionally fixed benchmark CLI false success and isolated its
  serialization test without changing live thresholds. Final 740 tests passed;
  all seven checks passed head `5440076`, merged as `f6178dc` with exact tree
  parity. Both post-merge workflows passed; completed branch cleanup verified.
  No model inference, study admission or freeze was claimed by that slice.
- Completed slice: fixed synthetic output-mode probe and explicit model/runtime
  eligibility overlay. Preserve original registry and model-rights controls;
  [live output-grammar evidence](./output-mode-probe-20260830.md) now records
  one successful complete non-study probe with all 16 loader pins verified.
  Stdout remains wrapped despite suppression flags. Local full validation:
  776 tests, 93.33% coverage. PR #86 passed all seven checks at `c1acfce`, merged
  as `0e0e66b` with exact tree parity, and both post-merge workflows succeeded
  (33301407812 and 33301407802). Completed branch cleanup was verified.
  Do not repeat the probe without a distinct new evidentiary purpose.
- Completed slice: [structured completion contract](./structured-completion-20260830.md).
  Exact upstream source and agent-panel review show irreversible CLI newline
  changes and missing completion-status evidence. Do not implement wrapper
  stripping or use the output-file path as byte-preserving evidence.
  A read-only native JSON decoder passed both agent reviews and full validation
  (871 tests, 93.38% coverage; decoder 95 tests at 100%). It does not verify
  transport, runtime identity, request binding, freeze or admission.
  PR #87 passed all seven checks at `eea531a`, merged as `1974763` with exact
  tree parity, and both post-merge workflows passed (33302547251, 33302547218).
  Completed local/remote-tracking branch cleanup was verified; master was clean.
- Current slice: [separate server profile and Unix-socket capture](./server-capture-20260830.md).
  The server executable is distinct from the CLI; its profile retains exact
  dependency/licence/source pins. The transport uses only a private Unix socket,
  strict bounded HTTP framing and an absolute I/O deadline. Fixture results do
  not prove a real model server or its process/egress lifecycle.
  Code `d14c81b` passed 940 tests (93.53% coverage); both new modules have full
  statement/branch coverage. Version/help diagnostics then passed with all 15
  image pins and unchanged pre/post identity. Local receipts are linked in the
  evidence record. CI portability/timing repair `348eca9` subsequently passed
  941 tests at 93.54% coverage and both Windows-targeted type checkers; agent
  re-review passed. Reconcile PR #88's exact hosted/merge state on resume;
  do not repeat diagnostics without a distinct new purpose.
  Follow-up: Windows run `33304040763` was cancelled after a >70-minute test/log
  stall. Logs revealed an oversized pytest parameter ID exceeding Windows'
  environment limit (900 passed, 41 skipped, one error). Test-only repair
  `fc1ca0f` gives bounded IDs and a portable collection regression. Reconcile
  the new PR head; do not reuse `5a782e5` as a passing head.
  Preserve downstream branch `codex/server-model-eligibility` at `062b776`,
  already pushed with its separate helper and 971-test receipt. After PR #88
  passes and merges, integrate the parent fix into that branch without dropping
  its unique commits, then deliver its new slice before lifecycle implementation.
- Next implementation: implement bounded child-process lifecycle and the
  server-specific model/runtime overlay, then a structured non-study probe and
  primary study runner. Use the reviewed Unix-socket route, no TCP fallback.
  Bind actual adapter/normaliser/profile/model-helper/registry and input/rubric
  identities into a reviewed full-component freeze. Implement affirmative
  admission separately. The existing protocol enum does not yet enable the new
  decoder. Do not use READY output or candidate consistency as primary evidence.
- Prior checkpoint: 713 local tests, 93.10% coverage for PR #84; freeze helper
  30 focused tests at 100%. These results do not validate this runtime slice.
- Scope ownership: the server profile, Unix-socket transport, their tests and
  linked records belong to this slice; the
  [context pack](../../context-packs/server-capture-20260830.md) records its
  checks and exclusions. Preserve overlapping active work.
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
