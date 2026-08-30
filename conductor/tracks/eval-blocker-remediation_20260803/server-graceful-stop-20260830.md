# Graceful stop and final output drain

## Scope and evidence boundary

Base `8acbd6180bb12259060c4fe156a835b9fe93a226` (merged PR #90), context
checkpoint `ebf9dbf`, activation `d41ce25`, branch `codex/server-graceful-stop`.
The [context](../../context-packs/server-graceful-stop-20260830.md) limits this
slice to a distinct graceful-stop path in the internal POSIX capture primitive.
It does not implement fixed server launch, sockets, requests, loader identity,
model eligibility, a study runner, freeze or admission.

## Panel and design

Main implements and integrates the supervisor and reviews safety. Agent
`runtime_profile_tests` owns synthetic fixtures and adversarial checks; agent
`root_acceptance_map` reviews acceptance and evidence integrity. Exact underlying
model revisions are not exposed. Agent review is not independent human review;
correlated errors remain possible. No clinical, legal, policy, organisational,
deployment or study-validity approval is claimed.

The panel recommended a separate stop event rather than reinterpreting
cancellation or introducing a callback framework. Cancellation still stops
capture; graceful stop requests TERM once and continues bounded dual-pipe drain.
Stop-before-launch launches nothing. An exit observed before the stop transition
retains its natural/nonzero disposition. `process_stopped` requires full streams,
reaping, no errors and exit code zero or SIGTERM. KILL escalation remains failure.
Signal requests cannot establish delivery or causality in an exit race.

Stop uses a shared two-grace cleanup budget: TERM wait ends at the earlier of
the original execution deadline or one grace interval, and final drain/reap
cannot restart the budget. The original deadline still bounds capture. Cleanup
does not retry an already attempted signal. Original and cleanup errors remain
separate, and incomplete output has only prefix hashes. Direct-child and OS
scheduling limitations remain unchanged. Raw bytes require inspection before
publication; no private data is admitted by this helper.

## Validation observations

Fresh pre-implementation `uv run python -m tools.full_validation` passed 1,022
tests in 80.75 seconds at 93.71% coverage, including lint, types, governance
and seven deterministic regression cases. This is baseline evidence only.

Fixture-first `uv run pytest --no-cov -q tests/test_server_process_stop.py`
failed with exit 1: `capture_child` rejected the unsupported `stop_event`
keyword. After initial implementation, that pre-launch fixture and all 50
existing capture tests passed. Ruff and native type checks passed.

Main review found that the first implementation checked EOF/exit before TERM
grace expiry. The acceptance agent concurred that this could accept a completion
first observed too late. The check now occurs after grace-expiry classification,
without KILL when the child is already observed exited. A deterministic fake-clock
fixture now protects this ordering; final full validation passed below.

Current supervisor SHA-256 is
`bb9e0c561fc7eb5552606aa5def25611115dd308fe68911e8dbf2dc0e8afed92`.
Acceptance-agent final review passed with no further actionable defect in these
bytes and the final fixtures (SHA-256
`4b0e6d456ed5933beb02ceb61e323ecf80ac8940c399074ffa73247e0f4a5718`).
All 78 supervisor tests passed, including 28 new stop tests, at 99.24% module
coverage; only the existing defensive incomplete-output guard remains uncovered.
Ruff and native/Windows-targeted ty/basedpyright checks passed. Main concurs
with the acceptance and fixture reviews; no unresolved in-scope disagreement
or abstention remains. Implementation and review fix commit: `3d4f109`.
Final `uv run python -m tools.full_validation` passed all 1,050 tests in 79.44
seconds, with 93.77% overall branch-inclusive coverage on macOS arm64 / Python
3.14.5. Ruff, ty, basedpyright, gremlin scan, repository governance, benchmark
registry and all seven deterministic regression cases passed.

PR #91 passed all seven checks at exact head
`b53b13b305f4a9326befddf3b3143db4fdce18d3`, merged at 2026-08-30T13:55:50Z
as `bb3c76b0985ee1590ccab519177009f12c5aad95`. Head and merge trees match
`92369ef0d7967a8ffdd4e22a3aaec27dbfe4d541`. Local master was fast-forwarded;
obsolete local and remote-tracking refs were removed after remote absence and
merged tree verification. Recorded commits remain recoverable. Post-merge
Quality `33315490265` and conformance `33315490275` both passed, including
all three operating-system Quality jobs.
Quality again emitted the existing non-failing Node.js 20/forced-Node-24
annotation for pinned `actions/github-script`; no warning-remediation claim is
made by this supervisor slice.

Focused commands: `uv run pytest --no-cov -q tests/test_server_process.py
tests/test_server_process_stop.py`; isolated coverage adds
`--cov=tools.server_process --cov-report=term-missing` with a separate temporary
coverage file. Type checks use `uv run ty check` and `uv run basedpyright` over
both changed Python paths; Windows targeting uses `--python-platform win32`
and `--pythonplatform Windows`, respectively. No client-specific platform guide
applies to this internal primitive. Markdown guidance and governance checks
apply to the Conductor records.
No model, version/help diagnostic, download, inference, credential, new dependency
or private-data execution occurred. The wider lifecycle and study remain open.

## Next action and rollback

The [next context](../../context-packs/server-session-20260830.md) records the
agent-reviewed fixed session contract: one owned worker, shared deadlines,
private socket identities, no cleanup before join/reap and separate failure
dispositions. Recheck exact upstream source before selecting real arguments.
Rollback reverts this delta
without changing default capture or historical receipts.
