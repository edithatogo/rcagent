# Development Workflow

## Purpose

This workflow is designed for one developer using agent assistance across a content, data, evaluation, and local-software repository. It maximises safe autonomous progress while reserving owner attention for decisions that genuinely require authority or preference.

GitHub and Conductor coordinate the work. Evidence, tests, sources, history, receipts, and actual external state prove it.

## Sources of Truth

| Concern | Authoritative record |
|---|---|
| Product and safeguards | `conductor/product.md` and `conductor/product-guidelines.md` |
| Architecture candidates and constraints | `conductor/tech-stack.md` plus accepted ADRs |
| Existing systems, dependencies, and fit-gap decisions | `conductor/integration-strategy.md` and `conductor/integration-map.json` |
| Continuous execution, decision engagement, recovery, and terminal state | `conductor/autonomy.md` and `conductor/autonomy.json` |
| Portfolio dependencies and sequencing | `conductor/roadmap.md` and track `metadata.json` |
| Track scope and acceptance | Track `spec.md` |
| Track task state | Track `plan.md` |
| Operational hierarchy and blockers | GitHub nested subissues and native dependencies |
| Decisions | `conductor/decisions/` plus linked GitHub `decision-needed` state |
| Proof | Tests, sources, Git history, receipts, CI logs, release records, and external verification |

When records disagree, stop claiming completion, preserve the conflict, and reconcile against the most direct evidence.

## Status Vocabulary

- `[ ]` not started
- `[~]` actively in progress
- `[x]` completed with linked evidence
- `[!]` blocked by a declared dependency or owner decision

A checkbox never proves that work passed. Completion requires its acceptance evidence.

## Continuous Autonomous Work Envelope

An instruction to implement, proceed, continue, resume, finish, or not stop is
standing authorisation to continue across ready tasks, phases, automatic
review and rework, documentation synchronization, and tracks. Do not ask for
routine confirmation at any of these boundaries.

An agent may proceed without per-task, per-phase, or per-track approval when all of the following are true:

- the work is reversible and inside an approved track;
- hard dependencies and the definition of ready have objective evidence;
- it uses synthetic, public, or already authorised data;
- it does not create a public release, submission, message, account, credential, or paid commitment;
- it does not make a new clinical, legal, policy, employment, regulatory, privacy-risk, or licence decision;
- it does not weaken a safety, privacy, security, human-review, or evidence gate; and
- the relevant tests and rollback path are available.

Normal in-scope implementation, local branches, isolated worktrees, fixtures, validation, documentation, and reversible refactoring are autonomous.

The complete dispatch, resume, retry, circuit-breaker, and terminal-state
rules are in [autonomy.md](./autonomy.md). A client or session boundary
requires a durable resume cursor; it does not create a new approval gate.

## Owner Decision Gates

Pause only the affected scope when progress requires one of these:

- clinical, legal, policy, privilege, records, employment, or regulatory interpretation;
- access to or use of real private, clinical, employee, consumer, or credential data;
- a new network-egress path, credential, paid service, compute spend, account, or contract;
- licence selection, rights exception, model/data distribution, or copying restricted material;
- a public release, registry or marketplace submission, publisher verification, external message, or support commitment;
- acceptance of residual privacy, security, cultural-safety, or clinical-safety risk;
- an irreversible architecture decision, destructive migration, deletion, or history rewrite; or
- a material product-scope choice with more than one reasonable outcome.

### Decision Request Contract

Apply the GitHub `decision-needed` label when available and create a record
from `conductor/decisions/template.md` containing:

1. a stable decision ID, the decision, and why it is needed now;
2. the recommended option first;
3. the recommendation rationale and supporting evidence;
4. at least one viable alternative where one exists;
5. assumptions, uncertainty, and trade-offs for every option;
6. reversibility, cost, privacy, safety, maintenance, and dependency impact;
7. the safe default if no decision is made;
8. the exact scope paused and the work that will continue;
9. the deadline or consequence of deferral; and
10. the response format required.

Ask one decision at a time unless decisions are inseparable. While waiting,
continue any other safe ready work. Release the WIP slot; do not keep a
decision-blocked task in an active implementation lane or repeat an unchanged
request.

## Autonomous Recovery and Plan Repair

Classify failures before acting. Retry transient failures with a bounded
budget and approved fallback. Diagnose deterministic failures and attempt up
to two evidence-led fixes. Repair incomplete plans autonomously when the
approved specification and acceptance criteria remain unchanged.

Every repair records its reason, attempt, result, and next action. Repeated
identical attempts without new evidence are prohibited. A material scope
change, new external effect, or reserved authority choice becomes a decision
request.

Stop writes only in the affected lane when context, lock, branch, worktree,
receipt, or external state conflicts. Preserve work, reconcile against direct
evidence, and resume. Trip the safety circuit breaker for credible privacy,
credential, destructive, evidence-integrity, or material-harm risk.

## Dependency Semantics

`hard_dependencies` in track metadata and GitHub's native **blocked by** relation determine whether a track may start.

`phase_dependencies` gate only the phase that consumes another track's contract or evidence. They allow independent foundation work to proceed without inventing false parallelism.

A dependency is satisfied only when:

- its acceptance criteria have direct evidence;
- the completion receipt is current;
- required artefacts and contracts are accessible;
- no unresolved defect invalidates the consuming work; and
- Conductor, GitHub, Git, tests, and receipts have been reconciled.

A closed issue or green workflow alone is insufficient.

## Existing-System Fit and Gap Gate

Every track begins with the acquisition ladder in
[integration-strategy.md](./integration-strategy.md):

1. use the current organisational system;
2. configure or profile it;
3. map an open standard;
4. adopt a maintained dependency;
5. add a thin adapter;
6. contribute a generic gap upstream;
7. implement only the small project-specific gap; and
8. build a new subsystem only by approved exception.

The track must identify its system-of-record boundary and candidates in
[integration-map.json](./integration-map.json), then test them against its
acceptance fixtures. A project-owned implementation cannot start until the
remaining gap, ownership rationale, dependency profile, compatibility window,
upstream path, and exit strategy are recorded.

If a dependency has a generic gap, reproduce it with a non-sensitive fixture,
check current versions and upstream issues, and prefer an authorised upstream
issue or contribution. Any local shim must be isolated, contract-tested,
time-limited, and linked to its removal condition.

Adding a new enterprise connector, upstream message, public dependency
commitment, permanent fork, or project-owned subsystem is an owner decision
gate.

## Single-Developer Parallelism

Use no more than:

- **one integration lane** for the current convergence point; and
- **two independent implementation lanes** for tracks with non-overlapping files and stable contracts.

The integration lane owns dependency reconciliation, shared schemas, validation, and merge order. A lane blocked on an owner decision or external state releases its WIP slot.

Prefer isolated branches and worktrees outside synchronised folders such as OneDrive. Each lane has:

- one track and GitHub issue;
- a bounded context pack;
- explicit owned files;
- a base revision and dependency receipts;
- local validation commands;
- a handoff note; and
- a rollback path.

Do not parallelise work that changes the same schema, authority source, workflow contract, or generated artefact unless one lane is explicitly the integrator.

## Context Engineering

Load the smallest authoritative context that can safely execute the task:

1. repository navigation and non-negotiable safeguards;
2. product and architecture context relevant to the task;
3. the track specification, plan, metadata, dependencies, and issue;
4. a bounded task context pack from `conductor/context-packs/template.md`;
5. exact source, schema, fixture, risk, decision, and evidence records; and
6. client-specific instructions only when that client is in scope.

Every context pack records purpose, base revision, authoritative inputs, exclusions, assumptions, decisions, token or size budget, freshness, owned files, commands, acceptance checks, and handoff state.

Do not dump the whole repository into model context. Prefer indices, stable identifiers, summaries with source pointers, deterministic retrieval, and on-demand loading.

## Definition of Ready

A task is ready when:

- its scope, deliverables, owner, and issue are clear;
- hard dependencies pass and relevant phase dependencies are available;
- inputs, sources, rights, schemas, and fixtures are accessible;
- the current system of record, applicable standards, maintained dependencies, and smallest remaining gap are recorded;
- privacy mode and permitted data are declared;
- decisions and risks are known or explicitly deferred;
- validation and rollback paths exist;
- owned files do not conflict with another active lane; and
- the bounded context pack is current.

If readiness cannot be established, mark the task blocked with the missing evidence.

## Task Lifecycle

### 1. Select

Choose the highest-priority ready task from the dependency graph, not merely the next checkbox. Prefer work that unblocks the most downstream value or reduces the largest safety uncertainty.

### 2. Preflight

Run the applicable doctor and context checks. Record the base revision, working tree, dependencies, tool/model versions, privacy mode, network status, sources, and expected validation.

### 3. Mark Active

Change the task to `[~]`, link the branch or worktree and issue, and reserve its owned files.

### 4. Implement

Work fixture-first where possible. Configure, profile, map, adapt, or
contribute before writing a replacement. Keep frameworks behind project
contracts. Preserve unrelated and historical material. Record material
assumptions and deviations immediately.

### 5. Validate

Run the smallest fast checks during implementation, then the full applicable phase gate:

- schemas, formatting, links, references, and frontmatter;
- unit, property, fixture, contract, integration, migration, and round-trip tests;
- privacy, egress, security, prompt-injection, cultural-safety, and clinical-safety tests;
- benchmark, calibration, citation, robustness, device, and resource tests;
- source, policy, standard, model, framework, and marketplace drift checks; and
- clean-context reproduction.

Warnings, unavailable upstream evidence, unsupported combinations, and offline checks must not be reported as current passes.

### 6. Record Evidence

Create or update a receipt with:

- task, issue, revision, timestamp, environment, privacy mode, and device class;
- exact commands, tools, dependencies, models, datasets, sources, and versions;
- results, raw-evidence locations, failures, warnings, uncertainty, and negative findings;
- decision and risk links;
- changed artefacts and compatibility impact; and
- rollback and follow-up work.

Never place credentials, private content, or direct identifiers in receipts.

### 7. Reconcile and Integrate

Compare the plan, issue, native dependencies, files, tests, Git history, CI, receipts, and relevant external state. Review the diff, preserve user changes, merge in dependency order, and rerun integration checks.

### 8. Complete

Change `[~]` to `[x]` only after acceptance evidence passes. Update the issue and dependency graph. A task with incomplete evidence remains `[~]` or `[!]` even if implementation appears finished.

## Phase Completion

When a phase passes:

1. record the phase receipt;
2. reconcile all acceptance checks and unresolved risks;
3. update Conductor and GitHub;
4. update the fit-gap record and integration map;
5. create a bounded handoff context; and
6. continue automatically to the next ready phase.

Ask the owner only if the next step reaches a declared decision gate. Phase boundaries are evidence checkpoints, not mandatory approval pauses.

## Track Completion

Before closing a track:

- all specification acceptance criteria have direct evidence;
- full applicable validation passes;
- privacy, safety, legal, policy, licence, and release limitations remain visible;
- hard and phase dependencies are reconciled;
- documentation, migration, compatibility, and rollback paths are current;
- the system-of-record boundary, adopted dependencies, upstream gaps, local shims, and replacement paths are reconciled;
- a clean reviewer can reproduce the result; and
- the GitHub issue, Conductor plan, Git state, receipts, and external state agree.

After the track passes, automatically run a fresh-context review, append and
fix bounded in-scope rework, synchronize evidence-backed project documents,
reconcile the issue and dependencies, release the lane, select the next ready
track, and continue. Do not ask whether to review, archive, clean up, or start
the next track. Leave completed track artefacts in place unless an approved
retention rule says otherwise.

Close parent workstreams and the roadmap only after their native subissues and portfolio-level acceptance evidence pass.

## Framework and Experimental Technology Policy

- Prefer maintained upstream frameworks and declarative standards.
- Integrate through thin adapters, capability discovery, contract tests, and safe fallback.
- Prefer an upstream issue or contribution for a generic gap; project code owns only safety, privacy, jurisdiction, and domain-specific extensions.
- Pin supported compatibility windows and monitor upstream drift.
- Keep experimental components, including Mojo or MAX, behind disabled-by-default adapters.
- Do not fork an upstream stack unless a documented ADR proves no maintained alternative and the owner accepts the maintenance burden.
- Give every local compatibility shim an owner, upstream reference, expiry condition, and removal test.
- Remove an experiment cleanly when it does not pass quality, safety, privacy, device, or maintenance gates.

## Commit and Review Convention

Use focused commits:

```text
feat: add [capability]
fix: correct [defect]
refactor: revise [architecture]
docs: document [topic]
test: add [validation]
chore(conductor): register [track or roadmap change]
conductor(plan): update [task state]
conductor(checkpoint): record [phase evidence]
```

Review staged files and the exact diff before committing. Do not stage unrelated user work. Public push, pull request, release, or submission status must be reported separately from local completion.

## Legacy Evaluation Work

The existing H0-H8 evaluation tracks remain historical records. Track 05 will map their cases, conditions, outputs, and scoring into the canonical benchmark contracts while preserving the original artefacts and explicitly labelling incomparable or incomplete results.
