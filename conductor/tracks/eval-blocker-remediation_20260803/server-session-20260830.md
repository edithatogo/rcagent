# Fixed non-study server-session integration

## Scope and baseline

Base `bb3c76b0985ee1590ccab519177009f12c5aad95` (PR #91); context checkpoint
`5170044`, activation `0c3d807`, branch `codex/server-session`. The
[context](../../context-packs/server-session-20260830.md) owns this implementation
slice. No real model serving, repeated diagnostic, study execution or admission
is authorised by this implementation receipt.

Fresh baseline `uv run python -m tools.full_validation` passed 1,050 tests in
77.22 seconds at 93.77% coverage, including lint, native types, governance and
seven deterministic regression cases. This predates the session changes.
Parent post-merge Quality and conformance were rechecked as successful.

## Source check and fixed contract

Main rechecked exact upstream commit
`c1d0e7a004015f23bc0233470b747b596f29b264` on 2026-08-30 UTC. The
[argument definitions](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/common/arg.cpp)
support a fixed local model path, context size 2048, one slot and a fixed API
alias, with offline mode and agent/UI/MCP-proxy features disabled. The minimal
profile environment excludes externally supplied MCP, HF, Docker, RPC and tool
configuration. These options do not attest OS-wide egress isolation.

The [HTTP implementation](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-http.cpp)
selects AF_UNIX for a `.sock` hostname and fails on unsuccessful binding without
falling back to TCP. The
[health handler](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-context.cpp)
returns the exact status-ok JSON object; loading/error handling belongs to
middleware. Health alone is neither model identity nor peer-process attestation.
Only source text was read; no upstream code or runtime bytes were executed or
redistributed. The existing synthetic READY prompt is not a study case.

## Agent panel and implementation boundaries

Main owns absolute-deadline support, source checks, integration and safety review.
`runtime_profile_tests` owns the fixed session and its synthetic fixtures;
`root_acceptance_map` reviews acceptance and integrity. Exact agent model
revisions are unavailable, and correlated errors remain possible. This is agent
engineering review, not human agreement or clinical/legal/organisational approval.

The panel requires exclusive private receipt creation before launch, bounded
health retries and a shared absolute operation deadline, stable socket identity
between health/completion/cleanup, joined worker and reaped child before cleanup,
complete loader logs with PID equal to the captured child, and identical pre/post
model-profile admission identity. Successful shutdown cannot erase HTTP, decoder,
runtime, persistence or cleanup failure. Preserve unexpected paths, and never
recursively delete them. A stuck OS/Popen call cannot be forcibly joined by Python;
fail closed and prohibit replacement launches in the owning process.

## Current validation

Fixture-first absolute-deadline tests failed (12 failures, exit 1) because
`capture_child` did not accept `deadline`. After the narrow implementation,
the existing 78 supervisor tests plus 12 new tests passed. Acceptance review
passed; a thirteenth fixture now verifies expiry during pre-launch setup.
All 13 deadline tests pass, as do Ruff and native/Windows type checks.
The execution timestamp bounds capture, not its separately bounded cleanup.

Functional implementation is committed as `4f561e7`.
The first session fixtures failed with ImportError before the module existed.
Initial implementation passed the first two synthetic composition fixtures.
Review then identified worker-start uncertainty: setting an ownership flag only
after `start()` returned could misclassify a launched worker when startup raised.
The panel requires ownership to remain uncertain until joined or explicitly
failed closed, with paths retained and no replacement launch. Receipt identity,
persistence errors, actual invocation provenance and readiness retry accounting
were hardened. Final production review passed session source SHA-256
`8c7353942a3c3c1bab492f70a8a892ea0b4d92eef80783c9778205a4dca17fc7`;
parent identity is observed before opening the receipt and rechecked after
flushing. The first integrated full run retained one stale test expectation
after that stricter post-flush check: 1 failed, 1,094 passed in 87.56 seconds,
93.60% coverage. The expectation is corrected to require the identity error,
with additional open-time parent and flush-time receipt replacement fixtures.
An intermittent synthetic HTTP fixture failure also exposed a test server that
closed before consuming the complete POST body; the production transport correctly
rejected it. The fixture now consumes the complete request body, without
weakening transport checks. All 35 session fixtures pass; Ruff and both native
and Windows-targeted type checkers pass. Final acceptance agent review passed
the unchanged session source and test SHA-256
`2f84fbc27a9321ed96b99123369ab87ea4865d8493f4b2404776820e3b32efd2`.
Main integration/safety review concurs. The actual synthetic Python-child test
exercises the real process supervisor, Unix HTTP capture and graceful shutdown;
eligibility, runtime-image verification and native decoding remain labelled
fixtures. The actual source inventory helper is also tested against repository
bytes. No real model or runtime executable was launched.

The deadline helper SHA-256 is
`a15475a09ffa1cd751ed9f28bd017540dbc209638b87c80d1e0f8bbcbda45f04`;
its test SHA-256 is
`adc095794a69d9a26c3318663c1409d073c5fdef53bf1a7fe602ce897ad7f250`.
Final `uv run python -m tools.full_validation` passed 1,098 tests in 82.90
seconds at 93.69% coverage, with all preceding lint, native types, governance
and deterministic benchmark gates passing. Main independently reran the 35
session plus 13 deadline tests: 48 passed in 1.76 seconds. Windows-targeted
`uv run ty check --python-platform windows tools tests` and
`uv run basedpyright --pythonplatform Windows` passed. Session module coverage
is 91% rounded; this is not exhaustive proof of every OS failure path.
Do not infer a real model execution receipt or study lifecycle completion from
synthetic validation. All historical H0–H8/H8P evidence remains unchanged.

## Next action

Deliver only the exact reviewed green head; hosted CI remains pending. A
distinct structured non-study probe comes
after fresh eligibility checks; runner, source freeze and affirmative admission
remain separate unfinished work. Rollback only this session/deadline delta.
