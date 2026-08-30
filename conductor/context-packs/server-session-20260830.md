# Context Pack: Fixed non-study server session

Track `eval-blocker-remediation_20260803`, issue #1. Base
`bb3c76b0985ee1590ccab519177009f12c5aad95` (PR #91), tree
`92369ef0d7967a8ffdd4e22a3aaec27dbfe4d541`, identical to reviewed head `b53b13b`.
Branch `codex/server-session`; no worktree lease enabled.

## Purpose, reuse and ownership

Compose the reviewed profile, model eligibility, graceful child capture and
Unix HTTP primitives into one fixed-purpose non-study session. Do not build a
generic service manager or expose arbitrary executable, argv, route, callback,
model or request options. Agent acceptance review recommends one owned capture
worker and synchronous bounded health/completion requests; main concurs.

Planned owned paths: `tools/prospective_server_session.py`, matching tests,
necessary narrow `tools/server_process.py` deadline support and linked records.
Main owns the deadline delta/tests, source checks, records, integration and safety;
`runtime_profile_tests` owns the session module/tests; `root_acceptance_map`
owns acceptance/integrity review. Preserve existing profiles, registry,
historical evidence and default capture/stop contracts.

Reuse `darwin_server_v030`, `prospective_server_model`, `server_process`,
`unix_http_capture` and `native_completion`. Read only their relevant contracts,
the parent receipts, selected spec/plan/metadata, index, guidelines/workflow,
root acceptance map and standing decisions 20260830-001/002.

## Required contract

Reserve an exclusive receipt before any launch. Verify the fixed model, profile
and source identities; select fixed local arguments and the profile environment.
Recheck exact upstream commit `c1d0e7a004015f23bc0233470b747b596f29b264`
before selecting flags. The linked server-capture receipt contains source URLs
and the known offline/no-agent/no-UI/no-MCP-proxy controls. No MCP/HF/docker/RPC
or tool options, inherited environment, TCP fallback or new resources.

Own one non-daemon capture worker, explicit stop/cancel events, sanitised
result/exception handoff and unconditional completion signalling. Worker alive
does not mean child started or server ready. Use a single absolute operation
deadline across startup, bounded health attempts and exactly one completion.
Relative timeout conversion must not silently extend that deadline after worker
queueing; add narrow absolute-deadline support if needed, with existing defaults
unchanged and tests for delayed worker startup.

Create a short canonical private directory (`0700`) and `.sock` path. Retain
directory/socket identities and reject replacement between health and completion,
not only within each request. Health is not peer PID attestation. Retain fixed
request bytes/hash, health observations, HTTP receipt, process streams and
post-execution profile/model identity checks. Bind loader PID to the actual child;
do not infer invocation or model identity from detokenised output.

On every path, preserve the first session failure and request graceful stop to
retain final logs where safe. Explicit abort/unsafe conditions use cancellation;
successful stopping never converts an HTTP failure to session success. Join the
worker before removing socket resources or claiming cleanup. A finite join cannot
force an OS/Popen-blocked thread to finish: record that failure, preserve paths,
prohibit replacement launches and make no cleanup/containment claim.

Remove only an identity-checked owned socket and empty owned directory after
worker completion and child reaping. Never recursively delete unexpected content.
Keep process outcome, HTTP completeness, model EOS, runtime checks, cleanup and
admission distinct. All study-admission flags remain false in this slice.

## Fixtures and checks

Use synthetic local children and owned Unix sockets only; no real model launch
in the implementation slice. Cover launch/worker exceptions, delayed readiness,
early exit, shared-deadline exhaustion, socket replacement, HTTP failure followed
by successful stop, stop/join failures, pin drift, incomplete logs and cleanup
refusal on changed paths. Tests must not leave child processes or threads running.

Run fixture-first tests, focused coverage, Ruff, native/Windows type checks,
full validation and final agent-panel review. Keep exact failed observations and
source provenance. No private data, credential, download, spend, global link,
external inference, redistribution or new owner approval is needed for fixtures.

## Handoff and rollback

After the fixture-tested fixed session passes, consider the separately scoped
structured non-study probe only after fresh eligibility and provenance checks.
Then implement the runner, full-component freeze and affirmative admission.
Neither this context nor fixture success enables study execution. Rollback only
the session additions and narrow deadline delta; preserve prior capture behaviour
and historical receipts. Update the continuation cursor at each handoff.
