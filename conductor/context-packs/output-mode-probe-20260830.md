# Context Pack: Fixed synthetic output-mode probe

Track `eval-blocker-remediation_20260803`, issue #1; base `f6178dc` (PR #85).
Branch `codex/synthetic-output-probe`; no worktree isolation lease enabled.
Fresh until any source, registry, model, licence or runtime pin changes.

## Scope and integration fit

Use the existing comparator validator and explicit runtime 0.3 profile, not a
new runtime or general execution framework. Main owns a small model-admission
overlay helper and its tests plus track records. Implementation agent owns
the fixed output-mode probe and its tests. Panel review is read-only.
Historical registry bytes and old probe APIs stay unchanged.

The overlay explicitly replaces only runtime identity on an in-memory copy
of the exact pinned comparator registry, records both original and effective
identity, and invokes all existing model class/licence/file admission checks.
It does not promote the new runtime from the old admission record.

## Acceptance and execution limits

One fixed synthetic READY prompt, admitted small Qwen model, seed 42,
temperature zero, 16 generated tokens, 512 context tokens, null stdin,
60-second timeout, one-MiB retained streams, cleared profile environment.
Use only flags observed in the retained 0.3 help receipt: offline, single-turn,
simple-io, no-display-prompt, no-show-timings, colour off, log-colours off,
log-disable, no-warmup and no-escape. No arbitrary extra flags or prompts.
Check registry/model/licence/runtime and source hashes before/after; retain
complete local stdout/stderr, loader evidence and all failure dispositions.
Reserve a new receipt exclusively before execution; never overwrite evidence.

Fixture tests and panel review precede live execution. This probe has a new
purpose: establish output grammar under documented suppression flags, not
repeat version/help or old READY observations. Never infer response-only
output from flags, word matching or a successful exit. Parser/normalisation
implementation follows observed evidence, not guessed banner stripping.

No acquisition, global links, credentials, private data, external inference,
paid compute, redistribution or public raw logs. Existing comparator decision
20260829-002 and prospective decisions 20260830-001/002 govern this slice.
Receipts remain non-study and unadmitted, regardless of process success.
OS/driver bytes, concurrent replacement and network egress remain limitations.

## Verification and handoff

Run fixture-first unit/adversarial tests, scoped Ruff/types and full validation;
record panel roles, results, disagreement and unavailable model revisions.
Main reconciles exact CI/merge state and updates the continuation cursor.
Rollback only this helper/probe extension; preserve all previous raw evidence.
Next: deterministic normalisation, runner, full component freeze and affirmative
admission. Unfinished engineering is not a no-admissible-condition fallback.
