# Committed native prerequisites

Track `eval-blocker-remediation_20260803`, issue #1. Clean checkpoint `c6b23db`
on `codex/prospective-prelaunch-gate`; merged parent PR #98 `234360d` and its
Quality/conformance workflows were rechecked successful. No overlapping writer
or enabled worktree lease. Unrelated Renovate PRs #93/#94 remain untouched.
Activation `162dfba`. Baseline full gate: 1,251 tests, 84.58 seconds, 94.02%.

## Scope and panel rationale

Main owns safety, evidence and integration; `runtime_profile_tests` implements
the checker/tests and narrow legacy freeze helper extraction; `root_acceptance_map`
reviews acceptance. Exact agent model revisions are unavailable; correlated
errors remain possible. No human-review or external-authority claim.

The primary adapter and complete dependency closure are absent. Rather than
claiming an always-failing full gate is complete, the panel selected useful
independently testable prerequisites: validate one native protocol, exact slot,
its five reference hashes and fixed known source subset against an explicit
commit. Reuse bounded Git and file verification from the legacy helper without
changing its public behavior. Preserve original validated hashes on all rereads.
Do not accept a caller component list, receipt, model root or bypass flag.

The known subset includes the checker, shared freeze helper, native/prospective
protocol, runner, decoder, inventory, preflight and package initialiser. It does
not claim the primary execution dependency closure. Return only enumerated
committed-byte consistency with permission/observation/admission/study flags false.
Primary adapter, full closure, agent review, fresh eligibility and loaded-code
attestation remain pending. No actual study protocol is frozen in this heartbeat.

## Validation and review

Fixture-first `uv run pytest -q --no-cov tests/test_prospective_native_prerequisites.py`
failed with exit 2, one missing-module collection ImportError in 0.12 seconds.
The final combined native/legacy suite passed 65 tests in 112.83 seconds.
A separate fresh coverage run passed 34 native tests in 62.18 seconds with
100% coverage (25 statements, 10 branches). An overlapping earlier coverage
artifact was discarded; it is not evidence. Ruff and native/Windows type checks
passed. Full `uv run python -m tools.full_validation` passed: 1,286 tests in
146.72 seconds, 94.05% coverage, plus lint, types, governance and regression
checks. Code commit `f2f76d0`.

## Hosted delivery

PR [#99](https://github.com/edithatogo/rcagent/pull/99) passed all seven checks
at exact head `74a995eb75b87a3fd7ca669a38c53153d09465c8` and merged on
2026-08-30 at 18:02:00Z as `acd251d19c4814f9f1b93a1cf3acf3718443e3dd`.
Reviewed and merged trees both equal `aa73b1e3e7706e66adbcc947897d6fdc1d766d8c`.
Local master fast-forwarded; remote completed branch absence was checked before
removing its local ref (recoverable from reviewed commit and PR). Successor
`codex/primary-session-gate` starts from the merged commit. Post-merge
conformance `33326897765` and Quality `33326897749` both passed on the exact
merged commit. Root issue #1 remains open. No owning-track archive is justified.
Positive fixtures use generated temporary Git repositories; bounded Git subprocesses are not model
execution. No actual model cache eligibility, model/runtime probe, raw historical
data read, receipt admission, blinding or scoring is performed.

Main review identified an ordering gap in the initial native implementation:
parsing before repository confinement could read an outside-root protocol before
rejecting it. Lexical parent traversal could similarly defer rejection until
the committed-file loop. Require confinement and parent-traversal rejection
before parsing, with no-read regression tests; preserve valid legacy behavior.
The fix is implemented and final acceptance review found no further actionable
gaps. Agent agreement concerns this bounded engineering slice, not study validity.

Reviewed source/test SHA-256 identities:

- Native checker: `8eb43a47e365aaa279a95cf2f3cdbd2654833b8f68570fabdfd3827f12937e79`
- Native tests: `879cb98e3021c2db71ca7f56a2159daa63f0e828920196728733c13a2a65f5e7`
- Shared freeze helper: `b3a4e7ec8c3a7c1f9f5ea005d5e243f2a2f5b786812c94d95f0c1319f7608272`
- Legacy tests: `03f1b9ca6b1a7a0ebf25201a6cd8ae4d900f74288f01c8c80a66cfb28fbd4f93`

## Remaining gates and rollback

Full pre-launch integration remains in progress after this prerequisite slice.
Keep actual adapter/review/source identity and fresh runtime eligibility separate;
no synthetic fixture or legacy freeze status can confer execution permission.
Preserve fixed READY behavior, historical H0–H8/H8P and all existing raw evidence.
Apache-2.0, private-data, credentials and per-artefact rights boundaries remain.
Agent engineering review is not clinical, legal, policy, regulatory, employment,
cultural-safety, organisational or deployment approval. Roll back only the new
checker and narrow extraction; preserve legacy behavior and historical receipts.

Next panel recommendation: implement the guarded single-slot primary adapter
and complete prelaunch verifier together. Define complete source/dependency
closure and trusted agent-review provenance first; do not add another cosmetic
readiness wrapper. See the [next context](../../context-packs/primary-session-gate-20260831.md).
