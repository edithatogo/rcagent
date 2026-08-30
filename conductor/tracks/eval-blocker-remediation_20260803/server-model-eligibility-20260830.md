# Server-specific model eligibility prerequisite

## Scope and dependency

This slice addresses a concrete prerequisite identified by the agent panel:
the existing prospective model helper describes a CLI, not the server entrypoint.
The new helper will reuse the original comparator rights/file validator with a
separate server overlay. Neither a generic runtime selector nor a model execution
path is introduced. The [context pack](../../context-packs/server-model-eligibility-20260830.md)
defines owned files, tests and rollback.

Base `5a782e5` is PR #88's exact head. On this turn's initial readback, all six
checks were queued and the PR remained open/unmerged; one Windows runner later
started. Local baseline full validation passed 941 tests at 93.54% coverage.
These observations are not evidence that the hosted repair has passed.

## Panel preparation and next lifecycle contract

Main owns integration and safety scope; `root_acceptance_map` reviewed acceptance
and evidence, and `runtime_profile_tests` reviewed runtime safety and implements
the new helper. Their read-only preparation agreed on a small fixed-purpose
supervisor rather than extending the blocking version/help diagnostic function.
Exact model revisions were not exposed; correlated agent errors remain possible.

The runtime reviewer recommended bounded, independently drained output pipes
instead of temporary-file capture: existing files bound retained bytes but not
disk consumption. This adds supervision complexity without a new dependency.
The acceptance reviewer requires distinct fields for HTTP completion, model EOS,
intentional shutdown, cleanup and admission; a negative termination exit code
alone must not invalidate a completed response, but cleanup failure must prevent
a positive capture result. Main accepts these recommendations within the existing
approved synthetic-only envelope; no further owner decision is required.

Future lifecycle sequence: reserve fresh receipt; verify model/server/source pins;
create a private canonical socket directory; launch fixed argv and minimal
environment with null stdin and a new process session; use one absolute deadline
for health and one completion request; always terminate, escalate and reap within
bounded cleanup grace; verify loader PID/images and post-run pins; decode separately.
Clean only identity-checked owned paths, preserving unexpected entries. Test output
overflow, cancellation, partial response, early exit, loading hang, ignored TERM,
failed reaping, pin drift and cleanup errors. This paragraph is a reviewed design,
not an implemented supervisor or an execution receipt.

## Evidence and boundaries

Integration checkpoint: PR #88 passed all seven checks at `eeba35e` and merged
as `8918936`. Merge `bde18c7` preserved this helper and its tests byte-for-byte,
retained the exact parent transport/collection tests, and kept both evidence
histories. Both agent re-reviews passed; main fixed one Markdown blank line.
Combined-tree full validation passed 972 tests at 93.60% coverage. PR #89 then
passed all seven checks at `02eef75b717e0c7b93c9e879ebb350cdd6be75c5`, merged
as `1e6b9bcc2a9af03b462d8295f9dfd05eb3243699` at 2026-08-30T11:48:22Z, and
exact tree parity was verified (`f2161554410ce7e53b41841d07885487021fee57`).
Post-merge Quality `33309842839` and conformance `33309842815` passed. Local
master was fast-forwarded and completed branch refs removed after verification;
all content remains in the merged commit. This does not admit a study condition.

The helper (`34e56ae`) is implemented with deterministic receipts binding original registry,
effective server overlay, profile ID/digest and selected model/licence hashes.
It runs the original all-class validator twice and rejects observed profile,
parsed-registry, selected-file and canonical-root/inode drift. These sequential
checks are not atomic protection against concurrent replacement.

Acceptance review passed without a blocking finding. Main's safety review
requested final selected-file, profile-ID and root replacement fixtures; the
acceptance reviewer additionally requested parsed-registry read-race coverage.
All are included. The new 30 synthetic tests pass with 100% statement/branch
coverage. Ruff and both native/Windows-targeted type checkers pass. Final full
repository validation passed 971 tests at 93.60% coverage, including governance,
gremlin scan, type checks and seven-case deterministic regression. Final agent
re-review confirmed the requested fixtures and both exact hashes. Reviewed helper SHA-256:
`ccd415735613c85592d7f894514495dfa59446f1f95076d3e0d5d2b44f2cd13a`;
tests: `501c215b8ad277e6caf4ef5cdababd470e9f54d2f1f1a6300f77afafba518dcb`.
The future full-component freeze must include imported `prospective_model.py`
as well as the new helper, server profile and comparator validator.

Fixture-first `uv run pytest -q --no-cov tests/test_prospective_server_model.py`
failed collection with the expected missing-module import error before code existed.
Final commands included:

```sh
uv run pytest -q tests/test_prospective_server_model.py --cov=tools.prospective_server_model --cov-report=term-missing
uv run ty check tools/prospective_server_model.py tests/test_prospective_server_model.py
uv run basedpyright tools/prospective_server_model.py tests/test_prospective_server_model.py
uv run ty check --python-platform win32 tools/prospective_server_model.py tests/test_prospective_server_model.py
uv run basedpyright --pythonplatform Windows tools/prospective_server_model.py tests/test_prospective_server_model.py
uv run python -m tools.full_validation
```

Focused coverage used a separate temporary coverage file to avoid interference.
Markdown style and thin-adapter strategy pass; client-specific guides are not
applicable. Final documentation governance validation also passed.

All new tests use synthetic files; no real model inspection or launch occurred.
Root issue #1 remains open. Historical H0–H8/H8P, CLI helper, registry, study gates and Apache-2.0
repository licence remain unchanged. Eligibility does not establish source freeze,
tamper-proof identity, egress isolation, operational suitability or study admission.
