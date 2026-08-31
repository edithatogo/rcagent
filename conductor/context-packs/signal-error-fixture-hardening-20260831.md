# Context: Deterministic signal-error fixture cleanup

Prepared successor to local listing-material delivery, not activated. First
verify PR #105 exact-head merge and post-merge checks; reconcile the current
cursor before writing. Start at AGENTS/index, owning remediation plan and
[retained validation evidence](../tracks/eval-blocker-remediation_20260803/listing-packet-delta-20260831.md).
Merge base is `de8c67ad07bbcfdc33df79f88c093de1d8bdc483`, prepared branch
`codex/signal-error-fixture-hardening`. Post-merge run IDs: Quality
`33352822749`, conformance `33352822798`. The unchanged full recheck passed
1,536 tests; the first failed run remains retained. Do not duplicate either.

## Bounded change

Only `tests/test_server_process_stop.py`, specifically
`test_signal_error_is_preserved_without_leaking_child`, needs implementation.
The first full local listing gate had one failed kill-case reap assertion at
cleanup grace 0.1 seconds; the unchanged focused two-case rerun passed. Agent
diagnosis found a race in the fixture's observation, not a demonstrated
production defect. Preserve both negative and subsequent validation evidence.

Retain each created synthetic `Popen` handle and original bound kill/wait
methods. The injected signal method should record its call, send the real
signal, boundedly observe/reap the child, then raise the intended `OSError`.
Add test-level `finally` cleanup using original methods so failures cannot
leave its owned child unreaped. Do not swallow cleanup failures. Preserve
original-error, signal-failed, single-injection and reaped assertions. Explain
that this tests error preservation, not a real-time latency guarantee; existing
deadline/reap-timeout fixtures retain their separate responsibility.

No production code, runtime deadline, protocol, input, model, cache, source S,
review R or execution-closure pin may change. This is synthetic test execution,
never a retry of the consumed study. Before and after the patch, prove no
`tools/` diff and complete frozen-file parity with S/R. Do not broaden to a
generic test framework or unrelated fixture refactor.

Main owns integration and the one test file; use separate read-only agent
acceptance/safety reviews. Run the two focused cases, the surrounding stop
suite, then repository full validation and hosted checks. Keep bounded failure
budgets and preserve all outcomes. Deliver exact-head reviewed green changes,
verify merge/post-merge parity and update the cursor. Rollback only this test
change, never raw receipts. No extra owner approval is needed for this fixture
repair. Afterwards resume read-only first-party listing-route verification,
with no implicit hosting, terms adoption, credentials or submission.
