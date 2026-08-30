# Context Pack: Structured completion contract

Track `eval-blocker-remediation_20260803`, issue #1; base `0e0e66b` (PR #86).
Branch `codex/structured-completion-contract`; no worktree lease enabled.
Fresh only for upstream commit `c1d0e7a004015f23bc0233470b747b596f29b264`.

## Scope and fit

Exact public upstream CLI inspection shows irreversible presentation changes
and missing completion-status evidence. Do not implement banner stripping.
Reuse the installed runtime's native non-streaming completion JSON contract,
Python standard JSON decoding, and the existing fixed generation declaration.
Main owns a small read-only decoder, synthetic tests and linked track records.
Two agents review source semantics, provenance and acceptance independently.

This is a thin project-specific evidence checker, not a new inference system.
It checks an original JSON body's content, terminal state, prompt, model label
and selected settings without changing content whitespace. It cannot establish
transport, model/runtime identity, execution truth, privacy, freeze or admission.
An eventual runner must bind those independently. No live normalisation mode
or preflight is enabled here. Revisit/remove this pinned compatibility contract
when the admitted runtime changes; unsupported responses fail closed.

## Inputs and exclusions

Load the track spec/plan/metadata, workflow/guidelines, decisions 20260829-002
and 20260830-001/002, prior output-mode evidence and prospective protocol.
Inspect only exact upstream CLI/UI/server response sources and bounded local
runtime metadata. Source links are evidence, not build attestation.
No new model invocation, listener, runtime/model download, dependency, global
link, private data, credential, external inference, release or redistribution.
Old profiles, registry, raw receipts and H0–H8/H8P remain unchanged.
Bound context to these files and relevant tests; do not load raw model bytes.

## Acceptance, validation and handoff

Reject display transcripts, malformed/duplicate JSON, invalid Unicode,
oversized input, absent/contradictory terminal metadata, truncated/partial
responses, and prompt/model/selected-generation mismatch. Preserve decoded
content bytes and original body hashes; all results stay unadmitted/locked.
Use failing fixtures first, then scoped lint/types, full validation and agent
review. Fixture success is not an observed server response or live readiness.
Main records exact CI/merge state and updates the continuation cursor.
Rollback only this decoder extension. Next: separately pin the installed
server entrypoint, lifecycle/transport controls, structured probe, runner,
full component freeze and affirmative admission. No new routine approval.
