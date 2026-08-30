# Context Pack: Bounded server process lifecycle

Track `eval-blocker-remediation_20260803`, issue #1; base
`1e6b9bcc2a9af03b462d8295f9dfd05eb3243699` (PR #89, exact tested-tree parity).
Branch `codex/server-process-lifecycle`; no worktree lease enabled.

## Scope and ownership

Implement the small lifecycle gap around the installed server, not a service
manager or replacement inference stack. Main owns integration and task records;
agent panels review acceptance/evidence and runtime safety.
Agent `runtime_profile_tests` owns the primitive and tests; main owns integration
and scope, and `root_acceptance_map` reviews acceptance and safety. Owned paths:
`tools/server_process.py`, `tests/test_server_process.py` and linked track records.
Keep existing profile/model helpers and historical receipts unchanged.

First bounded substep: a POSIX `capture_child` primitive with explicit argv/env,
nonblocking dual-pipe capture, cancellation/deadline/output caps and bounded direct
child cleanup. This is an internal building block with no CLI or model admission.
Do not claim descendant containment or safely signal a process group after its
leader has been reaped. Fixed admitted server launch, private socket ownership
and concurrent HTTP supervision remain a separate integration task; neither the
primitive nor its synthetic tests completes that server lifecycle contract.

Reuse Python subprocess/pipe facilities, `darwin_server_v030`,
`prospective_server_model`, `unix_http_capture` and `native_completion` rather
than duplicating their contracts. Fixture-first lifecycle supervision precedes
any real server probe. No real model launch is part of this initial slice.

## Required contract

Apply the reviewed design in the server-model-eligibility receipt: fixed-purpose
launch with no shell, null stdin, minimal environment and new process session;
fresh private canonical socket directory; independently drained, capped output
pipes; one monotonic execution deadline and separate bounded cleanup grace.
Always terminate, escalate and reap the owned child; preserve original failure
and cleanup failure separately. Do not recursively delete unexpected entries.

Test synthetic child early exit, loading hang, output overflow on either pipe,
cancellation, ignored termination, failed reaping and identity-sensitive cleanup.
Do not confuse HTTP completion, model EOS, intentional shutdown and successful
cleanup. Positive capture requires cleanup evidence, but is not study admission.
The eventual fixed probe must recheck model/profile/source pins, verify loader
PID/images and bind the captured request before decoder results are consumed.

## Inputs, checks and boundaries

Load index, guidelines/workflow, selected spec/plan/metadata, continuation cursor,
root acceptance map and decisions 20260829-002 and 20260830-001/002. Limit code
context to the four reused modules, shared runtime/comparator helpers and tests.
Recheck exact upstream source before selecting real server arguments.

Run focused tests, lint, native/Windows type checks and full validation; obtain
agent-panel review of code and evidence. Synthetic child tests do not establish
real model availability, OS/egress isolation, authenticated peer identity,
clinical/organisational validation, source freeze or study admission. No new
downloads, credentials, private data, spend, redistribution or global links.

## Handoff and rollback

Next after this fixture-tested slice: a fixed structured non-study probe, then
the primary runner, full-component freeze and affirmative admission gates.
Remove only the new supervisor/tests to roll back; retain existing receipts and
fail-closed study transitions. No probe is to be repeated without a new purpose.
