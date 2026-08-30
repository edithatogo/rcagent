# Native protocol candidate implementation

Track `eval-blocker-remediation_20260803`, issue #1. Parent PR #96 merged as
`3305c4b` with verified head/merge tree equality. Activation `73c6778` began on
`codex/prospective-native-protocol` while parent CI ran. Integration `290a146`
reconciled the verified parent. Squash ancestry produced documentation-only
conflicts; retaining the newer reviewed successor records preserved the exact
pre-integration tree `43273486d1d327005754b3a2e6f7b7cc9f61c8e0`.
No source/test bytes changed during integration. This is not model execution.

## Agent panel and scope

Main integrates and checks safety/records. `runtime_profile_tests` implements
the bounded source/tests; `root_acceptance_map` reviews acceptance independently
of implementation context. Exact agent model revisions are unavailable and
correlated errors remain possible. This records agent review, not human agreement.

The panel accepted a separate protocol version `2.0.0`, exact native JSON
normalization and explicit runner-contract version. Reuse a narrow shared
validator from the legacy module; retain validated reference bytes for request
construction without rereading protocol or reference files. Legacy schema, API,
CLI and result remain unchanged; no global schema mutation or circular import.
No atomic filesystem snapshot, freeze or execution is implied by read-once bytes.

## Validation in progress

Fixture-first command `uv run pytest -q --no-cov tests/test_prospective_native_protocol.py`
failed with exit 2 and one collection ImportError in 0.15 seconds because the new
module did not exist. Implementation and agent-panel review passed. Focused
validation passed 63 tests in 1.14 seconds, with 100% statement and branch
coverage across both native and shared/legacy modules (85 statements, 20
branches). Command: `COVERAGE_FILE=/tmp/rcagent-native-final-coverage uv run
pytest -q tests/test_prospective_native_protocol.py tests/test_prospective_protocol.py
--cov=tools.prospective_native_protocol --cov=tools.prospective_protocol
--cov-report=term-missing`. Ruff and native/Windows `ty` and `basedpyright` passed.
Implementation commit `29fce7c`. Full repository validation passed with exit 0: 1,218 tests in 81.37 seconds at
94.00% coverage, plus lint, types, governance and regression gates. Hosted
delivery remains pending.

Fixtures change protocol and reference files immediately after their validated
reads, then prove that request construction uses only retained original bytes.
They cover malformed markers, changed hashes, traversal, invalid UTF-8, duplicate
slots/cases/paths, generation types and values, missing or wrong runner versions,
exact legacy API/CLI results and false admission flags. Main added a legacy-version
declaration with only native normalization to isolate the legacy enum boundary.
Legacy freeze rejection is supported by its unchanged legacy-validator call path,
not a direct freeze test or an actual freeze operation.

Source SHA-256 values:

- Native: `5cac1ef02764a28e404315e81fba1a665a4db4fc6e853d7b7ccb795896d1432d`.
- Shared/legacy: `75ea1607b314e10087e7750c934c357eaa30fa8b8467a0bf99b1f63d3ef077b8`.
- Native tests: `259eb6dd98a3391b1ea8ad4ff856e77756f886436f59603653d984aba4b25581`.
- Legacy tests: `86e504da65bc57659fb359309fc7c8cf1aeb69fd6d244621edf3569d4d6cf026`.

Final agent re-review of the added compatibility case passed at these hashes.
The panel also accepted the prepared
[single-slot adapter context](../../context-packs/slot-session-20260831.md).

## Boundaries and next gates

Use only generated synthetic fixtures. Preserve all H0–H8/H8P and prior raw
evidence, including the negative READY result. No model probe, scoring, actual
freeze or admission is scoped. Leave the legacy freeze helper unchanged and
native-incompatible until a separately reviewed complete dependency closure
exists. Keep privacy, runtime identity, response binding and authority unverified.
Apache-2.0 and per-artefact rights remain unchanged. Agent review does not grant
clinical, legal, policy, regulatory, employment, cultural-safety, organisational
or deployment approval. Next: actual runner, full-component freeze and affirmative
admission-before-blinding. Rollback only the new validator and narrow extraction.
