# Read-only single-slot binding

Track `eval-blocker-remediation_20260803`, issue #1. Heartbeat resumed clean
checkpoint `1c1f86f` on `codex/prospective-slot-session` from merged PR #97
`09a9058`. Parent Quality `33321812059` and conformance `33321812017` were
rechecked successful. No overlapping writer or enabled worktree lease; unrelated
Renovate PRs #93/#94 remain untouched. Activation commit `744f850`.

## Panel choice and ownership

Main owns integration, evidence integrity and safety/privacy; implementation
agent `runtime_profile_tests` owns the new binder/tests and narrow private
native-validator helper extraction; `root_acceptance_map` reviews acceptance.
Exact model revisions are unavailable and correlated agent errors remain possible.
This is agent engineering review, not human agreement or external validation.

The panel selected the approved read-only fallback. An extracted primary
lifecycle would open an execution path before complete freeze and admission
controls. The new binder instead reads the native protocol once, selects exact
denominator membership and obtains filesystem eligibility internally via the
existing server-model helper. No caller eligibility receipt or callback is accepted.
Compare model ID/revision/hash, runtime executable hash, profile hash and registry
hash. Adapter identity is still unverified: do not substitute the READY session
or this binder's hash for a primary adapter. Return a bounded identity projection
without model/cache paths and preserve explicit false execution/admission flags.
Point-in-time filesystem consistency is not loaded identity or atomic attestation.

## Validation in progress

Baseline full gate passed 1,218 tests in 81.86 seconds at 94.00% coverage.
Fixture-first `uv run pytest -q --no-cov tests/test_prospective_slot_binding.py`
failed with exit 2 and a missing-module collection ImportError in 0.13 seconds.
Implementation and acceptance review passed. Focused validation passed 56 tests
in 1.54 seconds at 100% combined statement/branch coverage (49 statements, 12
branches). Command: `COVERAGE_FILE=/tmp/rcagent-slot-binding-coverage uv run
pytest -q tests/test_prospective_slot_binding.py tests/test_prospective_native_protocol.py
--cov=tools.prospective_slot_binding --cov=tools.prospective_native_protocol
--cov-report=term-missing`. Ruff and native/Windows `ty` and `basedpyright` passed.
Final full validation passed with exit 0: 1,251 tests in 80.73 seconds at 94.02%
coverage, with lint, types, governance and deterministic regression gates passing.
Implementation commit `0ca2a2f`. PR #98 passed all seven hosted checks at
`24a10ca4aa0dcfec60499606cf34d4fa594372a3`, then merged as
`234360de763515776ba50ea4542543b1004f712f` at 2026-08-30T16:58:01Z.
Exact head/merge tree equality was verified:
`97dc4df93a9690cbad6031c59f7a9f7b1fd4ab72`. Local master was fast-forwarded;
completed local and remote-tracking branch cleanup was verified after the exact
merge checks. Post-merge conformance `33323914284` and Quality `33323914292`
passed. The next pre-launch branch contains only a prepared context/cursor;
no gate implementation or usable execution permit is claimed.
Fixtures replace the existing eligibility I/O boundary; no actual model-cache
eligibility check or model invocation was performed in this heartbeat.

Fixtures cover membership-before-eligibility, all six condition mismatches,
receipt purpose/flags/digest/overlay consistency, model-check failures, altered
references, mutation after validation and during eligibility, unchanged native
public API, path/private-extra exclusion and no aliasing. No test substitutes a
mocked receipt for actual observed evidence. Main safety review concurs with the
acceptance panel; no source defect was identified.
Final test re-review and the prepared
[pre-launch gate context](../../context-packs/prelaunch-gate-20260831.md) passed.
The parent protocol/admission task is reconciled from pending to in progress;
its incomplete admission requirements still prevent closure.

Reviewed SHA-256 values:

- Binder: `a8d0f544f135bfde77adefba46e83df27ef5f97bc1ca10be0ea9bd0c85903bf1`.
- Binder tests: `08a652b627acd3df6f0317674242dc63984502badf42af0423443aaff213a760`.
- Native helper: `69838be7e8e730554e81219952146cf40b654bf5253e5a17ea19c579eef11064`.
- Native tests: `32eb98d7daa24e0a237f01645369f361e945fc9ddc9f57dc6aed432791ce37b6`.

No external platform guide applies. The local Markdown guide, workflow and
product boundaries govern changed records. Existing lifecycle source pins and
historical receipts remain untouched.

## Preserved boundaries and rollback

Preserve native public API and all legacy/session/process/transport source bytes.
No actual protocol freeze, scoring, blinding, study admission, new acquisition,
private clinical/employee data, credentials or publication is in scope. Historical
H0–H8/H8P and raw evidence, including negative READY equality, remain untouched.
Apache-2.0 and per-artefact rights are unchanged. Agent review is not clinical,
legal, policy, regulatory, employment, cultural-safety, organisational or deployment
approval. Roll back only the new binder and helper extraction. Full-component
freeze, actual lifecycle binding/orchestration and affirmative admission remain
unfinished; this slice cannot close the owning track or root issue.
