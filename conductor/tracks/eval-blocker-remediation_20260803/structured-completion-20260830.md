# Structured completion contract and CLI exclusion

Track `eval-blocker-remediation_20260803`, issue #1; base `0e0e66b` (PR #86).
Scope: read-only source analysis and synthetic contract implementation, not
runtime admission, model invocation, a protocol freeze or study execution.

## Evidence-led route repair

Public source inspection on 2026-08-30 used exact llama.cpp commit
`c1d0e7a004015f23bc0233470b747b596f29b264`, corresponding to the reported build
identity. This is not a reproducible-build attestation of installed bytes.

The [CLI renderer](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/cli/cli-ui.h)
conditionally appends a newline. Responses with and without a final LF can
produce identical display output. Wrapper removal cannot recover that lost
distinction. Reasoning transitions add further presentation text.
The [CLI loop](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/cli/cli-context.cpp)
does not use the completion function's Boolean result at the call site, and
its streaming callback does not retain finish reason. Exit zero cannot prove
natural completion. The output-file path also modifies trailing newlines.
Do not promote the prior READY transcript into primary byte-preserving evidence.

The [local server wrapper](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/cli/cli-server.h)
runs the server in a thread and addresses it over loopback; a stale comment
elsewhere calls it a child process. This does not establish egress isolation.

The [native final serializer](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-task.cpp)
exposes content, terminal state, generation settings and token counts in JSON.
The [execution implementation](https://raw.githubusercontent.com/ggml-org/llama.cpp/c1d0e7a004015f23bc0233470b747b596f29b264/tools/server/server-context.cpp)
uses accumulated text for non-streaming content. Its prompt field is detokenised
input, not the original request. Token-limit stopping is distinct from context
truncation: reject either, not just the truncation flag.

## Implementation and limitations

`tools/native_completion.py` decodes one bounded native JSON body with Python's
standard parser. It rejects duplicate keys, malformed/invalid Unicode,
non-finite numbers, unexpected top-level fields, missing metadata, streaming or
non-EOS completion, truncation, stopping words, invalid counts and mismatched
model labels/selected fixed generation settings. It preserves decoded content
without trimming or Unicode normalisation, with separate content/body hashes.
Returned detokenised prompt is hashed but never treated as a request echo.

The result is only `native_completion_consistent`; `admitted` and
`study_unlocked` always remain false. Raw JSON must be retained by the caller.
Model labels, settings and terminal fields are untrusted declarations, not
runtime/model/process attestation. Other sampling parameters remain unqualified;
context/timeout, HTTP status, process lifecycle, request binding, privacy and
review/freeze are not checked here. Decoded server text is not raw token bytes.
The protocol-candidate enum and existing live preflights are unchanged.

Strict top-level field checking deliberately rejects alternative endpoints,
response projections and probability extensions. Revisit this versioned thin
adapter if the admitted runtime/response shape changes. No new dependency,
source redistribution, listener or model process was introduced.

## Panel and validation

Main owns implementation and integration. Agents `protocol_contract_review`
and `root_acceptance_map` independently reviewed source semantics. Both rejected
wrapper parsing and recommended structured capture. The second reviewer found
the detokenised-prompt distinction; it was incorporated before implementation.
Rendered-transcript relabelling would weaken the intended evidence contract;
patching/rebuilding upstream would add avoidable binary-provenance work.
Neither is needed for this repository-owned decoder. No new owner decision.

Fixture-first test collection failed before the module existed. The subsequent
95 synthetic tests passed at 100% statement and branch coverage. They include
the newline collision, error text with a normal exit banner, malformed and
duplicate JSON, invalid metadata/settings, missing terminal evidence and exact
whitespace/Unicode preservation. These are fixtures, not observed server runs.
Both panel agents reviewed the implementation and tests with no blocking
findings in the declared consistency-only scope. Token-array/timing semantics
are not independently cross-validated; no execution attestation is claimed.
Initial type checks caught a negative test intentionally supplying non-bytes;
an explicit test-only cast preserves that runtime rejection fixture.
`uv run python -m tools.full_validation` then passed: 871 tests, 93.38% coverage,
Ruff, both type checkers, governance, gremlin scan and seven-case deterministic
regression. Markdown style and the thin-adapter technical strategy pass;
no selected client/platform guide applies to this local decoder.
Agent model revisions are not exposed; reviews have correlated-error limits
and are not independent human or clinical/organisational validation.

## Next and rollback

Separately verify the existing server executable and dependency/licence closure,
then implement bounded transport/process controls and a structured non-study
probe. Retain request, response, loader and lifecycle evidence. Only after that
implement the primary runner, bind every consumed component into a reviewed
freeze and add affirmative admission. Engineering remains ready; Option C is
not justified by an unfinished runner. Historical H0–H8/H8P remain unchanged.
Rollback only this decoder extension; retain prior raw receipts and findings.
