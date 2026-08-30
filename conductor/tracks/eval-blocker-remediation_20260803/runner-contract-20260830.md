# Pure prospective runner contract

## Scope and baseline

Base `5b194a8` (PR #95), context checkpoint `770b62c`, activation `104cc1a`,
branch `codex/prospective-runner-contract`. The
[bounded context](../../context-packs/runner-contract-20260830.md) owns only
the new pure module, matching fixtures and linked records. The working tree
was clean, no overlapping writer was active, and both parent post-merge workflows
were successful. Open Renovate PRs #93/#94 are unrelated and were not changed.

Fresh baseline `uv run python -m tools.full_validation` passed 1,106 tests in
81.24 seconds at 93.91% coverage, with lint/types/governance and deterministic
regression gates passing. This predates the new implementation.

## Panel boundary and existing-system reuse

Main owns integration, safety and records; `runtime_profile_tests` implements
the module/fixtures; `root_acceptance_map` reviews acceptance and privacy.
The panel chose two pure functions, not a general service or execution runner:
deterministic request construction and normalization of supplied response bytes.
Exact agent model revisions are unavailable; correlated errors remain possible.

Reuse the existing `GENERATION` values and strict `native_completion` decoder.
The current protocol accepts only legacy normalization declarations. Reading it
and emitting a native candidate could imply unsupported compatibility, so this
slice deliberately consumes no protocol or files. Later explicit versioned
integration must reuse the existing protocol denominator/reference validators;
none are replaced or weakened here. Literal slot equality is only caller-label
consistency, not denominator membership, case-input provenance or execution.

The request package retains exact template/input/prompt/request bytes, counts
and hashes. Reconstruct it from retained template/input bytes before accepting
a supplied package; reject altered fields, types, flags or hashes. One insertion
marker is required in the template; input markers remain literal. Preserve
valid UTF-8, whitespace and Unicode without trimming or recursive substitution.
Byte-size limits are not token-window validation.

Normalize only with the existing strict decoder; never compare a detokenised
response prompt to the original request as provenance proof. Candidate records
keep execution, admission and study flags false and preserve unverified protocol,
denominator, request/response binding and model-identity boundaries. No model
probe, transport, subprocess, freeze, scoring or private-data operation occurs.
The prior 32-byte non-READY observation is neither rerun nor tuned into success.

## Validation and delivery

Fixture-first `uv run pytest -q --no-cov tests/test_prospective_runner_contract.py`
failed with exit 2 and one collection ImportError because the new module did not
exist. The implementation now passes 85 focused tests at 100% statement and
branch coverage. Command: `COVERAGE_FILE=/tmp/rcagent-runner-contract-coverage
uv run pytest -q tests/test_prospective_runner_contract.py
--cov=tools.prospective_runner_contract --cov-report=term-missing`.
Ruff formatting/lint and native/Windows `ty` and `basedpyright` checks passed.
Fresh full validation passed with exit 0: 1,191 tests in 83.34 seconds at 93.98%
coverage, including lint, types, governance and regression checks. A prior
validation session handle was unavailable after context recovery; no result was
inferred from it. The complete fresh gate above is the delivery evidence.
Implementation commit: `ec2b63e`. Hosted delivery remains pending.

Main review identified an input-bounding gap in the initial package verifier:
canonical serialization of the entire supplied package could allocate unbounded
altered-field data before rejecting it. The fix compares against the bounded
reconstructed shape using exact types/fields, without serializing arbitrary
incoming structures. An empty final prompt is rejected rather than presented
as a valid native candidate. Regression fixtures reject oversized and cyclic
fields and custom scalar types while spying on serialization to ensure only
the bounded newly generated request is serialized. All three false execution/
admission flags reject both `True` and integer-zero substitution.
Acceptance review also requires a bounded exact expected-model label retained
in the result, so the caller's comparison context is explicit without claiming
model identity. Privacy/data classification remains unverified.

Final acceptance agent review passed, and main safety/integration review concurs.
The source SHA-256 is
`7d01ff4b2e930a7d3a412fe3ee5e9f193139628ba32190db58bb015f45702b51`;
test SHA-256 is
`17e71bbd0cfe99ca7b8ad5c6ade643f2e6fbdc2690ce7592e9cfd460a1238005`.
No runtime, model, protocol file or raw historical evidence was read by the new
API or its fixtures. No external platform guide applies; the local Markdown
style guide and repository workflow govern the changed records.

## Remaining work and rollback

After verified delivery, integrate an explicit versioned native protocol mode,
complete the actual runner and full transitive component freeze, then implement
affirmative admission-before-blinding. These remain separate unfinished gates.
The panel reviewed and accepted the prepared
[native protocol context](../../context-packs/native-protocol-20260831.md),
which preserves the legacy API and keeps the existing freeze helper unchanged.
All historical H0–H8/H8P, raw evidence, Apache-2.0 choices and per-artefact rights
remain unchanged. Agent review is not human agreement or clinical, legal, policy,
regulatory, employment, cultural-safety, organisational or deployment approval.
Rollback only this pure contract and records; preserve parent implementation.
