# Context Pack: Pinned server and bounded local transport

Track `eval-blocker-remediation_20260803`, issue #1; base `1974763` (PR #87).
Branch `codex/server-capture-foundation`; no worktree lease enabled.
Fresh only while runtime, source and evidence hashes match their profiles.

## Scope, fit and ownership

Reuse the installed llama.cpp 0.3 server, shared profile checks and Python
standard HTTP/socket implementation. Do not build a server or patch upstream.
Agent `runtime_profile_tests` owns `tools/darwin_server_v030.py` and its tests.
Main owns `tools/unix_http_capture.py`, its tests, integration and track records.
Agent `root_acceptance_map` reviews transport/source/safety; a second agent
reviews final code. Existing CLI profiles and historical receipts stay unchanged.

Server profile must bind exact executable, shared libraries, backend inventory,
licence evidence and any imported source dependencies. Version/help diagnostics
may run only after file admission and fixture/panel checks; no model invocation
or persistent listener in this slice. A future model runner is a separate step.

For transport, adapt native HTTP over an owner-only Unix socket directory.
Reject TCP endpoints, proxies, redirects, unexpected routes, unsafe paths,
ambiguous framing and oversized bodies. Bound socket I/O by an absolute deadline,
not only an inactivity timeout. Retain response bytes separately from decoded
content; transport success never establishes runtime or request provenance.
Tests may use ephemeral synthetic Unix sockets, never real model servers.

## Authority and boundaries

Load track spec/plan/metadata, workflow/guidelines, current continuation cursor,
decisions 20260829-002 and 20260830-001/002, shared profiles and structured decoder.
Inspect exact upstream commit `c1d0e7a004015f23bc0233470b747b596f29b264` only
as source-contract evidence, not build attestation. Bound context to these
components and tests. No downloads, credentials, private data, external
inference, paid compute, global links, public raw logs or redistribution.
Apache-2.0 project licence and per-component rights evidence are unchanged.

## Acceptance and handoff

Fixture-first tests for profile drift, loader rejection, private socket
ownership/path checks, malformed/oversized/framing/timeout responses, exact
body preservation and failure handling. Run scoped lint/types, full validation,
agent review and bounded version/help diagnostics after code review.
No study invocation, protocol mode or admission/preflight unlock is enabled.
Record actual diagnostics separately from fixtures and declarations.
Next: bounded child-process lifecycle, model/runtime overlay, structured probe,
primary runner, full component freeze and affirmative admission. Roll back only
these additions, preserving prior raw receipts and fail-closed gates.
