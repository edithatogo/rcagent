# Continuous Autonomous Delivery Contract

## Intent

Once the owner says to implement, proceed, continue, or otherwise authorises
execution of the roadmap, the agent continues through ready tasks, phases, and
tracks without asking for routine confirmation.

Phase and track boundaries are evidence checkpoints, not conversational stop
points. Completing one track automatically triggers reconciliation, review,
bounded rework, documentation synchronization, selection of the next ready
track, and continued execution.

Autonomy changes delivery mechanics, not authority. It does not permit the
agent to make decisions reserved to the owner or to weaken privacy, safety,
security, evidence, licence, clinical, legal, policy, cultural-safety, records,
release, or human-review controls.

The machine-readable companion is
[`autonomy.json`](./autonomy.json).

## Standing Execution Authorisation

A clear instruction to begin or continue implementation authorises:

- every reversible task inside the approved specifications;
- autonomous movement between tasks, phases, reviews, rework, and tracks;
- selection of the highest-value ready work under the dependency graph;
- bounded plan repair that preserves the approved specification;
- routine project-document synchronization supported by completed evidence;
- commits, local branches, isolated worktrees, tests, receipts, and issue
  reconciliation that are normal parts of the approved workflow; and
- continued work in unaffected lanes when another lane is waiting.

The agent must not ask:

- whether to begin the next task, phase, or ready track;
- whether to run planned tests, validation, review, or safe rework;
- whether to record a checkpoint or synchronize factual project state;
- whether to retry a transient failure within the retry budget;
- whether to use a reversible implementation choice already covered by the
  specification and technical strategy; or
- whether to leave completed track artefacts in place.

Archiving is a reversible housekeeping action only when the roadmap explicitly
requires it. Deletion, destructive cleanup, public release, merge to a
protected branch, and other declared gates are never implied by standing
authorisation.

## Continuous Dispatch Loop

The portfolio runner repeatedly:

1. reconciles Conductor, Git, GitHub, CI, receipts, decisions, dependencies,
   external state, and active leases;
2. expires or repairs stale non-authoritative state without discarding work;
3. identifies ready tasks and calculates the critical path;
4. reserves one integration lane and up to two non-conflicting independent
   lanes;
5. builds a bounded, fresh context pack for each selected task;
6. marks the task and track active with an idempotent run identifier;
7. implements, validates, records evidence, and commits the bounded change;
8. performs phase verification and automatically fixes in-scope findings;
9. completes and reconciles the phase;
10. at track completion, performs an independent-context review, applies
    bounded rework, synchronizes project documents, and reconciles the issue;
11. releases the lane and selects the next ready task or track; and
12. stops only at a portfolio terminal condition.

Selection is deterministic where possible. The default priority order is:

1. safety, privacy, security, data-integrity, or supply-chain remediation;
2. work that unblocks the critical path;
3. contract, schema, harness, and fixture work needed by multiple tracks;
4. completion of already-started bounded work;
5. other ready work by roadmap order.

## Portfolio Terminal Conditions

The autonomous run ends only when:

1. all authorised roadmap work is objectively complete and reconciled;
2. every remaining ready path requires an owner decision;
3. every remaining path requires an unavailable external action and no safe
   independent work remains;
4. a safety circuit breaker identifies a credible risk of material harm,
   privacy breach, credential exposure, evidence corruption, destructive
   change, or uncontrolled external effect; or
5. the owner explicitly stops or changes the objective.

Token, context, session, or client boundaries are not project terminal
conditions. Before yielding to such a boundary, write a durable handoff and
resume cursor so the next run can continue without re-asking for approval.

## Decision-Only Engagement

Ask the owner only when a declared decision gate is actually reached and the
answer is necessary to advance the affected work.

Each request contains:

1. a stable decision ID and one-sentence question;
2. the track, task, dependency, and why the decision is needed now;
3. the recommended option first;
4. the rationale and evidence supporting the recommendation;
5. at least one viable alternative when one exists;
6. trade-offs, risks, uncertainty, cost, reversibility, and downstream impact
   for every option;
7. the safe default if the owner does not respond;
8. the exact scope that will pause;
9. the work that will continue autonomously;
10. the response format needed; and
11. links to the decision record and supporting evidence.

Ask one decision at a time unless decisions are inseparable. Do not turn a
status update, preference that can be inferred from approved context, or
ordinary implementation uncertainty into a decision request.

The default while waiting is to pause only the affected lane, release its WIP
slot, and continue every safe independent task. Never repeatedly ask the same
unchanged question.

## Autonomous Plan Repair

The agent may repair a plan without owner intervention when the repair:

- remains inside the approved specification and acceptance criteria;
- splits, reorders, clarifies, or adds missing verification and recovery work;
- does not add a new external effect, authority decision, system-of-record
  write, public commitment, or material dependency;
- preserves traceability to the original requirement; and
- is recorded in the plan and phase receipt.

Replanning uses an iteration budget and explicit outcomes:

- `success`: the plan is coherent, covered, ordered, and executable;
- `retry`: another bounded repair attempt is justified;
- `decision_needed`: owner authority or preference is required;
- `blocked_external`: an external action is required;
- `failed_safe`: continuing would be unsafe or evidence would be unreliable.

An agent may not silently change an approved specification. A material scope
change becomes a decision request.

## Failure, Retry, and Circuit-Breaker Policy

Classify every failure before acting:

| Class | Default response |
|---|---|
| Transient network, service, lock, or rate failure | Retry with bounded backoff and jitter; try an approved equivalent path |
| Deterministic code, test, schema, or content failure | Diagnose, apply up to two evidence-led fixes, rerun the smallest check, then the required suite |
| Invalid or incomplete plan | Run bounded autonomous plan repair |
| Stale context or state conflict | Stop writes in the affected lane, refresh sources, reconcile, then resume |
| Dependency or upstream regression | Pin or roll back within the supported window, isolate the adapter, preserve evidence, and continue unaffected work |
| External wait | Record a wake condition, release the lane, and continue independent work |
| Owner decision | Create one decision packet, pause only the affected scope, and continue independent work |
| Safety, privacy, credential, destructive, or evidence-integrity risk | Trip the circuit breaker, preserve state, and request the necessary decision |

Retry budgets are bounded by failure class and recorded in the run receipt.
Repeated identical attempts without new evidence are prohibited. A failure is
not escalated merely because the first command failed; safe diagnosis,
self-correction, fallback, and independent work are exhausted first.

## Durable State and Resume

Every active lane records:

- run and idempotency IDs;
- track, phase, task, issue, branch, worktree, and base revision;
- owner, lease time, heartbeat, and stale-lock policy;
- current status and last verified checkpoint;
- changed and owned paths;
- commands, results, retries, and remaining checks;
- decisions, external waits, wake conditions, and safe defaults;
- assumptions, risks, context-pack revision, and source freshness; and
- the exact next action.

State transitions are append-only or otherwise recoverable. Checkboxes and
locks are coordination signals, not proof. On resume, reconcile durable state
against files, Git history, tests, receipts, remote refs, and external state
before continuing.

An expired lease may be reclaimed only after verifying that no writer remains
active and preserving its branch, worktree, diff, logs, and receipt.

## Isolation, Concurrency, and Integration

Use an isolated branch or worktree when concurrent or high-risk changes could
overlap. Each lane declares owned paths and shared contracts before writing.

- One integration lane owns shared schemas, dependency reconciliation, and
  ordered integration.
- At most two independent lanes may run when their writes do not overlap and
  their contracts are stable.
- A decision-blocked or externally waiting lane releases its slot.
- Lock takeover requires stale-owner evidence and a receipt.
- Integration reruns checks against the actual combined revision.
- Merge conflicts, dirty worktrees, and remote divergence are reconciled, not
  overwritten.

Parallelism is an optimisation, not a reason to invent false independence.

## Automatic Review and Rework

Every phase receives objective verification. Every completed track receives a
fresh-context review against its specification, plan, product constraints,
technical strategy, security/privacy rules, and tests.

In-scope findings are appended as tracked rework and fixed automatically.
Review does not pause the roadmap merely to ask whether fixes should be
applied. Escalate only when a finding requires an owner decision, changes the
approved scope, or leaves a material risk that cannot be safely resolved.

No track is marked complete from checkboxes alone. Completion requires
reproducible evidence, reconciled state, and no unresolved applicable
high-severity finding.

## Upstream Conductor Assessment

The local Codex adaptation is bundled from upstream Conductor `0.3.0` at
`fb6212e8faee3f9ecb69f0ee19bd5b2a0765bb0a`. A live review on 2026-07-31
found upstream `main` at
[`99ba10e`](https://github.com/gemini-cli-extensions/conductor/commit/99ba10e1a11130fc159f681b7ba8803489239cbf).
The stable implement protocol remains interactive at track selection,
documentation synchronization, cleanup, and review handoff, so it does not by
itself satisfy this portfolio's continuous cross-track requirement.

Useful experimental branches are:

| Experiment | Useful pattern | Adoption status |
|---|---|---|
| [`feat/ralph-loop`](https://github.com/gemini-cli-extensions/conductor/tree/feat/ralph-loop) at `b843867` | Iteration-bounded architect loop, hook-managed state, explicit success/retry/stuck outcomes, autonomous task execution, and plan repair | Adopt semantics behind the project harness; do not depend on the unmerged hook implementation |
| [`feature/asdd`](https://github.com/gemini-cli-extensions/conductor/tree/feature/asdd) at `5ea8c01` | Persistent project state, track locks, DAG analysis, isolated and standard modes, explicit discard, and review-lock handoff | Prototype behind contracts after Track 01 validation |
| [`feature/isolation-worktree`](https://github.com/gemini-cli-extensions/conductor/tree/feature/isolation-worktree) at `c1ae65f` | Resumable per-track worktrees, isolated documentation updates, review reports, and rework loops | Reuse safe worktree patterns; correct Windows, dirty-tree, path, and integration edge cases locally |

These branches are research inputs, not production dependencies. Before
enabling any upstream implementation, verify its current merge status,
licence, client compatibility, failure handling, state integrity, Windows
behaviour, security posture, and replacement path.

## Conformance Tests

The delivery harness must prove:

- phase completion selects the next phase without owner input;
- track completion selects the next ready track without owner input;
- a blocked lane does not stall independent ready work;
- only declared decision gates generate owner questions;
- decision packets contain options, recommendation, rationale, alternatives,
  safe default, scope, and impact;
- transient and deterministic failures use bounded recovery;
- repeated failures trip the correct circuit breaker;
- interrupted runs resume from reconciled evidence;
- stale locks cannot overwrite active work;
- review findings become automatic bounded rework;
- no protected external action occurs without authority; and
- completion cannot be claimed from checkboxes, green CI, or local state
  alone.
