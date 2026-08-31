# Local autonomy coordinator

The workbench records local phase, review, rework and synchronisation state in
an atomic JSON checkpoint. It returns the next instruction to the caller.
The caller performs authorised work and reconciles its evidence; this module
does not launch an agent, execute a command or grant external authority.

## Commands

```sh
python -m tools.workbench state initialise checkpoint.json --input plan.json
python -m tools.workbench state next checkpoint.json
python -m tools.workbench state advance checkpoint.json --root . --input event.json
python -m tools.workbench state resume checkpoint.json --root . --input resume.json
python -m tools.workbench state recover checkpoint.json --root . --input recovery.json
```

The parent checkpoint directory must already exist. Initialisation refuses an
existing checkpoint. A plan supplies `base_revision` (a full Git commit) and
`tracks`, each with a unique `id`, ordered `phases` and optional `dependencies`.
Unknown dependencies and cycles are rejected.

An advance event supplies a unique `event_id`, an `action` and a repository
relative `receipt` for pass/fail outcomes. The receipt identifies the exact
`track_id`, `phase_id`, `stage`, `base_revision` and `run_id` returned by the
coordinator, its `outcome`, and nonempty `artefacts` with `path` and `sha256`.
Hashes establish byte agreement, not the truth of a claimed test or approval.
Callers must check the actual results before submitting an outcome.

Passing the last implementation phase selects review, then synchronisation,
then a dependency-ready track. A failed stage selects bounded rework. Waits
require a `wake_condition` and allow independent tracks to proceed. A resume
event supplies `track_id`, `event_id` and a matching receipt with outcome
`resume`. Exhausted rework and circuit breakers require separate reconciliation.

## Ownership and recovery

Writers acquire an exclusive sibling lock recording owner, run, worktree,
heartbeat and expiry. Each short write holds POSIX advisory ownership. These
heartbeats do not supervise long-running clients. Explicit receipt-bound recovery is
supported on POSIX; Windows retains exclusive writes and refuses automatic
recovery. Existing active locks are never stolen.

Recovery input supplies a repository-relative `receipt`. Its `outcome` is
`recover`; it binds `base_revision`, `owner`, `run_id`, `worktree`,
`lock_sha256` and `checkpoint_sha256` to the original file bytes. Its artefacts
must include the roles `branch`, `diff` and `log`, each with a path and hash.
Preserve the actual branch/worktree and supply truthful observations of their
state. The API requires an expired lease and acquires nonblocking advisory
ownership to exclude a cooperating active writer. It copies and flushes the
checkpoint, lock, receipt and referenced artefacts to a unique sibling recovery
directory before releasing the unchanged lock. Changed ownership or evidence
causes refusal; preserved files remain available. Arbitrary hostile filesystem
writers and the truth of caller-supplied evidence are outside this guarantee.
An error after lock removal may occur while flushing directory metadata. Inspect
the current lock and retained recovery directory before retrying; an error does
not imply that the lock remained unchanged.
Replaying an identical event is idempotent; changed event content or evidence
is rejected. Checkpoint digests detect accidental corruption, not an attacker
able to rewrite both the state and its digest.

The coordinator has one serial instruction lane. The separate queue contract
enforces one integration lane and at most two independent lanes, rejects
overlapping portable paths, and prevents redispatch of active/completed tasks.
Neither component performs unattended stale-lock takeover or client execution.

## Context and receipt boundaries

Context validation checks types, portable paths, positive budgets and timestamp
freshness. A `fresh_until` value of `source-change` requires callers to reconcile
source revisions before reuse; structural validation cannot observe an external
source change. Receipt validation checks its structure and timestamp, not its
scientific, clinical, legal or organisational validity. Agent review applies to
repository engineering; reserved external authority remains separate.
