# Synthetic signal-error fixture hardening

Base `e7f2dac`; activation `4e0b492`. This repairs only
`test_signal_error_is_preserved_without_leaking_child` in
`tests/test_server_process_stop.py`. Preserve the first local listing-validation
failure (1 failed/1,535 passed), focused diagnostic pass and unchanged full
recheck recorded in the [listing receipt](./listing-packet-delta-20260831.md).

## Change and limits

The fixture now retains its created process and original bound kill/wait
methods. After sending the real signal, it boundedly waits for exit before
raising the injected `OSError`. This makes signal-error preservation distinct
from a race to observe exit inside the production 0.1-second cleanup budget.
The production budget is unchanged. A test-level `finally` uses the original
methods to kill an owned child if still running and wait even if that cleanup
kill fails. Cleanup exceptions are not swallowed. Waits are bounded to five
seconds; a host unable to finish cleanup in that limit still fails visibly.

Expected original error, `terminate_failed`/`kill_failed`, single injected call
and `reaped=True` assertions remain. Existing deadline/reap-timeout fixtures
retain responsibility for latency and negative cleanup behaviour. This is not
a production-runtime fix or a claim of real-time scheduling guarantees.

`git diff --exit-code cd09dba47704f3c87b95975a216a9a5be98158bd -- tools evaluation conductor/reviews/primary-execution.json`
passed before/after the scoped work: complete frozen execution files and pins
remain unchanged. Only the intended test differs under `tools/` and `tests/`
relative to the base. No model/cache access, actual study attempt, production
deadline change, source/review repin or external action occurred.

## Review and validation

- Focused two parameter cases: 2 passed in 5.89 seconds.
- Surrounding stop suite: 28 passed in 22.14 seconds.
- Ruff and ty for the changed test: passed.
- Agent acceptance `runtime_profile_tests`: passed; original error/call counts
  preserved, deterministic exit observation, explicit final cleanup.
- Agent safety `runtime_security_review`: passed; owned handles/original
  methods, bounded waits, visible cleanup failures, frozen-source parity.
- Full repository validation is running; hosted checks/delivery are pending.

Agents reviewed read-only and did not run tests. A cleanup exception can become
the primary traceback while Python retains the original exception context;
the test does not silently accept either failure. Review concerns this fixture
only, not clinical/legal/policy/employment/cultural-safety/organisational or
deployment validation. Historical H0–H8/H8P and failed prospective evidence
remain unchanged; no admission, scoring, root completion or archive is claimed.

After exact-head delivery/post-merge checks, continue read-only first-party
listing-route verification using the delivered README and packet delta. No
hosting, legal terms adoption, credentials or submission is implicit. Rollback
only this test change and append its evidence; never remove original failures.
