# Context Pack: Graceful child stop and final output drain

Track `eval-blocker-remediation_20260803`, issue #1. Base
`8acbd6180bb12259060c4fe156a835b9fe93a226` (PR #90); reviewed head `1696db1`
and merge have identical tree `87d084cc7a430af7cb47d423692dd7a09021c192`.
Branch `codex/server-graceful-stop`; no worktree lease enabled.

## Purpose and smallest gap

The synchronous child-capture primitive stops draining on cancellation. A future
server worker must not reinterpret cancelled/incomplete logs as a successful
serving session. Acceptance-agent design review therefore recommends a distinct
graceful-stop event before composing the fixed server adapter. Main concurs.
Reuse the stdlib supervisor rather than introduce callbacks or a service manager.

Owned files: main owns `tools/server_process.py` and linked track records;
`runtime_profile_tests` owns `tests/test_server_process_stop.py` and fixture review;
`root_acceptance_map` owns read-only acceptance/integrity review. Existing
`tests/test_server_process.py` remains the default/cancel regression contract.
Main also owns integration and safety review.

## Required contract and fixtures

Validate a separate stop event. Check stop/cancel before launch, with cancellation
remaining failure. On an active stop, send TERM once and keep draining both pipes
under the existing independent caps. Bound escalation, final drain and reap;
never reset the original execution deadline indefinitely. Preserve original
failure separately from cleanup failure, and reject incomplete full-stream claims.

Use a distinct stopped disposition, not natural zero exit, model EOS or admission.
Record observed return code, stop request, TERM/KILL actions and stream completeness.
Unexpected early/nonzero exit must not be laundered by a racing stop request.
Do not signal a reaped PID or claim descendant containment. Keep worker ownership,
request provenance and socket lifecycle outside this primitive's completion.

Fixture-first checks: final stdout/stderr from a TERM handler, ignored TERM,
held-open pipes, overflow while stopping, simultaneous cancel/stop, pre-launch
stop, early exit/stop races, read/cleanup failure, absolute deadline and bounded
final drain. Use readiness signals rather than tight Python-startup assumptions;
do not spawn leaking grandchildren. Existing 50 tests must continue to pass.

## Inputs and validation

Read index, guidelines/workflow, selected spec/plan/metadata, continuation cursor,
standing decisions 20260830-001/002 and the parent lifecycle receipt. Limit code
context to the supervisor/tests and the existing Unix HTTP/profile/model contracts
where their composition matters. No real server flags are selected here.

Run focused tests and coverage, Ruff, native and Windows-targeted type checks,
full validation and final agent-panel review. No model launch, version/help probe,
download, new dependency, credential, private data, network inference or spend.
No new authority is required for this reversible synthetic-only substep.

## Handoff and rollback

After graceful stop, compose owned worker and bounded synchronous Unix HTTP in
the fixed admitted server adapter; verify exact upstream flags before selecting
real launch arguments. Private socket ownership/cleanup, request/runtime binding,
structured non-study probe, runner, freeze and admission remain unfinished.
Rollback only the graceful-stop delta; retain the merged default capture contract
and all historical evidence. A checkpoint is not study completion.
