# Pinned server and bounded Unix-socket capture

Track `eval-blocker-remediation_20260803`, issue #1; base `1974763` (PR #87).
This slice establishes a server profile and transport foundation, not a model
runner, study observation, admission or completion of the historical evaluation.

## Reuse and provenance

`tools/darwin_server_v030.py` reuses the reviewed profile verifier, aliases,
backend inventory and 13 component-evidence pins. It excludes the CLI executable
and CLI implementation library, adds the independently hashed installed server,
and binds three imported source files. Static `otool -L` inspection found the
expected shared dependencies; actual loaded images require a separate receipt.
The server executable SHA-256 is
`07c17ec087076d582147208beadba5cbe534ae6e5015658e6f4c96d9457232f6`.
Existing CLI profiles, registry and raw receipts are unchanged.

Component rights evidence remains llama/ggml MIT, OpenSSL Apache-2.0 and libomp
Apache-2.0 with LLVM exception according to installed licence/header bytes.
The previously recorded libomp formula/SBOM disagreement is preserved, not
silently resolved. No runtime/model bytes or upstream source are redistributed.

## Transport contract

Exact upstream commit `c1d0e7a004015f23bc0233470b747b596f29b264`
[selects AF_UNIX for a `.sock` host](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-http.cpp),
with no TCP fallback on bind failure. This source inspection is not an
installed-binary build attestation or a live server transport observation.

`tools/unix_http_capture.py` adapts Python's standard HTTP/socket implementation.
It permits only `GET /health` or `POST /completion` over a canonical Unix socket
inside an owner-only `0700` directory. The path must be short, non-symlinked and
owned by the current user. Parent/socket device and inode identities are checked
before and after a complete response. It does not launch any process.

The request and response bodies are bounded at one MiB. Each underlying send or
receive uses the remaining absolute deadline, capped at 120 seconds, including
header reads. Python's bounded HTTP header parser is retained (64-KiB line and
100-header limits), with malformed-header defects rejected. Require one numeric
Content-Length and one JSON content type; reject transfer/content encodings,
duplicate framing and redirects. Non-200 bodies and partial bodies are retained
where available; unsupported framing is rejected before reading the body.
Parsed headers are retained, not original wire-header bytes.

This proves only a scoped HTTP observation. The helper does not authenticate the
peer process, validate JSON content, prove request origin, supervise a server,
enforce process-wide egress isolation or admit a study. Both admission flags
remain false. Same-user interference and replacement races remain limitations.

## Review and verification checkpoint

Main owns transport and integration. Agent `runtime_profile_tests` owns the
server profile. Agent `root_acceptance_map` reviewed source behaviour and both
implementations without a blocking finding in the stated foundation scope.
The profile agent independently reviewed transport and found an oversized
integer-deadline exception mismatch; main replaced the overflowing finite
conversion with safe range checks and added a regression. Parent traversal is
rejected before platform-specific path normalisation. Main also added strict
malformed-header rejection. The diagnostic CLI reserves a fresh receipt before
launch, permits only version/help and refuses unsafe or existing destinations.
No independent human review or clinical/organisational validation is claimed;
agent model revisions were not exposed and correlated errors remain possible.

Fixture-first imports failed before the corresponding modules existed. Pre-CI
profile/diagnostic tests (29) and transport tests (40) pass with full statement
and branch coverage. `uv run python -m tools.full_validation` passed 940 tests
at 93.53% coverage, Ruff, both type checkers, governance, gremlin scan and the
seven-case deterministic regression. Diagnostic code was committed as `d14c81b`
before diagnostics. Markdown style and thin-adapter strategy pass; no selected
client/platform guide applies. Baseline was 871 tests at 93.38%.

Initial PR #88 CI passed Linux but found Windows-only type-stub errors for Unix
APIs and a scheduling-sensitive partial-body fixture on macOS. Fix `348eca9`
uses explicit fail-closed capability checks, never a TCP default, and a
deterministic post-chunk timeout fixture. The real slow-header deadline test
remains. Both Windows-targeted type checkers and 41 transport tests pass; agent
re-review found no weakening of the transport boundary. Final full validation
passed 941 tests at 93.54% coverage, including all repository checks. Hosted
validation of this repair is pending at this checkpoint.

## Windows collection follow-up

The 10:41 UTC heartbeat found Windows job `99237298852` still reporting the
test step after more than 70 minutes. The other six checks passed. Quality run
`33304040763` was cancelled to stop the stalled log output. Direct job logs
revealed a real collection/skip-teardown error, not a transport failure: pytest
expanded the 1 MiB oversized-body parameter into `PYTEST_CURRENT_TEST`, exceeding
Windows' 32,767-character environment-value limit. The log recorded 900 passed,
41 skipped and one error; no Windows pass is claimed.

A portable collect-only regression reproduced a 1,048,669-character node ID
before repair. Explicit short IDs now retain the unchanged oversized-body and
invalid-deadline parameters. The regression limits collected node IDs to fewer
than 512 characters and does not execute Unix socket tests. Both agent reviewers
checked this test-only repair; no transport, model, rights or admission behaviour
changed. Repair commit: `fc1ca0f`; 42 focused tests passed. Full validation passed
942 tests at 93.54% coverage, including lint, both type checkers, governance and
the seven-case deterministic regression. Windows-targeted ty and basedpyright
also passed. The new exact-head hosted run remains required.

## Hosted delivery

All seven PR checks passed at `eeba35e2c27af21938b33fff8ea35b238f079e21`,
including Windows job `99246036418` (completed 2026-08-30T10:49:19Z).
PR #88 merged at 2026-08-30T11:42:11Z as
`89189363b9a1764264bac97b870eb1975ce0d1b1`. Exact head/merge tree parity was
verified: `18a1869c3379fe81fb3e753b1515cc1b4b1158c5`. Local master was
fast-forwarded before integrating the preserved model-eligibility branch.
Post-merge Quality `33309589305` and conformance `33309589298` both passed.
The remote parent branch was absent; its local and stale remote-tracking refs
were removed after tree verification. Content remains in the merged commit;
the downstream branch was preserved. No study admission is implied.

## Actual non-study diagnostics

The version diagnostic ran 09:13:56–09:13:57 UTC on 2026-08-30 (1.25 seconds);
help ran 09:14:09–09:14:10 UTC (0.47 seconds). Both exited zero, retained complete
streams and verified all 15 reported non-system images. Pre/post runtime,
evidence and source pins were unchanged. No model argument or serving session
was used. Version markers matched 0.3.0/commit c1d0e7a00. Help confirms host
Unix-socket support and offline/no-agent/no-ui/no-ui-mcp-proxy flags; those flags
are not themselves network-isolation or serving-compatibility evidence.

Both receipts are local-only in
`/Volumes/PortableSSD/rcagent-model-cache/probe-evidence/`:

| Diagnostic | Receipt filename | Receipt SHA-256 |
| --- | --- | --- |
| Version | `server-version-v030-20260830.json` | `57645b29b022681ddea0f3addd78a9a7780a2ac63b4df79a7480dd71e3b111fa` |
| Help | `server-help-v030-20260830.json` | `7fb573b0b0a7f460fad0c4f2aecd1e7681427677a78c5fee53f52c54b71d31d5` |

Version stdout/stderr sizes were 0/100,488 bytes; help sizes were
56,616/100,386 bytes. Profile digest:
`c5bdd37eb8391baedd191c482996210ebdfbd43888ab8afb578092fafd8896c1`.
Profile module source SHA-256:
`419d4fb56e00f4117b637f5b31eb1961179f8b649a155e366e8db5fd53259acb`.
Complete raw hashes, arguments, timestamps and limitations remain in each
receipt. This public projection omits raw streams. OS/driver bytes, loader
attestation, concurrent replacement and process-wide egress remain limitations.
Both receipts are unadmitted and study-locked; do not repeat these diagnostics
without a new evidentiary purpose.

## Next execution boundary

The future server runner must use a fresh private socket directory and cleared
environment, fixed local model path, offline mode, disabled agent/UI/MCP proxy,
no MCP config/HF/docker/RPC/tools parameters, and bounded child-process cleanup.
`--no-agent` alone does not clear separately configured MCP connections.
Ordinary server routes still exist; the two-route limit is the client's limit.
The pinned [MCP configuration implementation](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-mcp.cpp)
and [argument definitions](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/common/arg.cpp)
support these configuration controls.
[Signal handlers are installed after model loading](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server.cpp), so kill-and-reap fallback
must cover loading hangs. These are required future controls, not implemented
claims of this transport helper. Then run a distinct structured non-study probe,
implement the primary runner, bind all components into the protocol freeze and
implement affirmative admission. Unfinished engineering does not justify Option C.

Rollback only these additions; preserve previous negative and positive receipts.
