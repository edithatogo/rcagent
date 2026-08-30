# Bounded child-process capture foundation

## Scope and evidence boundary

Base `1e6b9bc` (PR #89), branch `codex/server-process-lifecycle`; plan activation
`49b9962`. The [context pack](../../context-packs/server-process-lifecycle-20260830.md)
defines the first lifecycle substep: concurrent bounded stdout/stderr capture
and cleanup of one explicitly supplied POSIX child. This is an internal primitive,
not an admitted model runner, a service manager or a public execution CLI.

Reuse Python subprocess, nonblocking pipes and selectors. Avoid changing the
already reviewed profile, model-rights, transport and decoder contracts. The
future fixed-purpose server adapter must compose those checks before any model
launch. No real model execution, socket/session probe, study freeze or admission
is part of this slice. The parent lifecycle task remains incomplete until fixed
server launch, socket ownership and concurrent request supervision are implemented.

## Agent design review

Main owns integration and safety scope; `runtime_profile_tests` implements the
primitive and fixtures; `root_acceptance_map` reviews acceptance and integrity.
Exact model revisions were not exposed; correlated agent errors remain possible.

The acceptance reviewer recommended direct-child cleanup rather than signalling
a process group after its leader has been reaped, when PID reuse can make the
target unsafe. This trades descendant containment for a narrow, honest guarantee.
The caller must not treat the new session flag as a process-tree sandbox.
Descendant-held pipes must hit the absolute drain deadline rather than hang;
any retained partial output must be labelled as a prefix, not a complete stream.

The implementation reviewer selected concurrent nonblocking reads, independently
capped streams and explicit caller-supplied argv/environment with no shell or
inherited environment. Main requires no environment-value echo in receipts,
pre-launch cancellation checks and separate original/cleanup errors. These
choices remain within approved synthetic engineering and require no new decision.

Capture stops at the first failure, so bytes emitted during termination grace
may not be retained. Complete-stream flags and hashes must not be inferred from
a retained prefix. Invocation arguments/environment are not bound by this
primitive receipt; the future admitted adapter must record their provenance
separately without exposing credentials or private values.

## Required validation and handoff

Fixture-first coverage must include early/nonzero exit, independent stream caps,
exact-cap success, overflow, deadline, cancellation, ignored TERM, failed KILL/reap,
selector/read errors and held-open streams. Cleanup must run even after capture
failure. OS process creation, scheduling and signal delivery are not hard-real-time
guarantees. Inspect raw captured bytes before publication; capture does not admit
private data or establish rights, runtime identity, egress isolation or suitability.

Fresh baseline full validation passed 972 tests at 93.60% coverage, including
lint, type checks, governance and the deterministic regression suite. This is
pre-implementation evidence, not validation of the new primitive.

Fixture-first execution (`uv run pytest --no-cov -q tests/test_server_process.py`)
failed at collection with ImportError before the module existed (exit 2).
Implementation then passed 50 focused synthetic tests. Isolated module branch
coverage was 98.89%; the unexercised defensive `incomplete_output` guard is not
reachable through a normal successful loop exit, which already requires EOF.
Native and Windows-targeted ty/basedpyright and Ruff checks passed. Review added
early/one-sided EOF, incomplete-prefix and cleanup-failure integration fixtures,
and removed scheduler-dependent startup assumptions from termination tests.

Implementation commit: `b995ecc`. Final integration command
`uv run python -m tools.full_validation` passed on macOS arm64 / Python 3.14.5:
1,022 tests in 67.87 seconds, 93.71% overall branch-inclusive coverage, Ruff,
ty, basedpyright, gremlin scan, governance, benchmark registry and all seven
deterministic regression cases. The helper retains 98.89% isolated coverage.
Hosted CI and merge are pending; local validation does not imply hosted delivery.
Retain all negative results.
Do not repeat the earlier real model/version diagnostics.
Next: fixed admitted server launch, private socket lifecycle and supervised HTTP
capture, followed by the separately reviewed structured non-study probe.

## Reviewed artefacts

Final acceptance/integrity agent review passed with no actionable defect; main
safety/integration review concurred. The implementation agent supplied fixture
results and explicit limits. No unresolved disagreement or abstention remains
inside this primitive's scope; wider server/study claims were not reviewed as
complete. No client-specific platform guide applies to this internal stdlib
primitive; Markdown guidance and project governance apply to these records.

- `tools/server_process.py` SHA-256:
  `e4e3ed7238c0c47c98e59cdde1c24cd46cd3fe2aa97e6c7e756a48c64793b8f4`.
- `tests/test_server_process.py` SHA-256:
  `3f146624a165e4f069986825733e9cb586c61c2f554458781b97f9f6417f69a9`.

Focused commands: `uv run pytest --no-cov -q tests/test_server_process.py`,
`uv run ruff check tools/server_process.py tests/test_server_process.py`,
`uv run basedpyright tools/server_process.py tests/test_server_process.py`,
`uv run ty check tools/server_process.py tests/test_server_process.py`, with
`--pythonplatform Windows` for basedpyright and `--python-platform win32` for ty.
Isolated coverage used `--cov=tools.server_process --cov-report=term-missing`
with a separate temporary coverage file. Synthetic fixtures use the local Python
interpreter, not llama-server or downloaded code.
