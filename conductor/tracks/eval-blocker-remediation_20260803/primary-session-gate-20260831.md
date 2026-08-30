# Guarded primary session implementation

Track `eval-blocker-remediation_20260803`, root issue #1. Heartbeat
2026-08-30T18:46:46Z resumed clean checkpoint `0c68b95` on
`codex/primary-session-gate`; activation `6f5423d`. Parent PR #99 merged as
`acd251d`; conformance `33326897765` and Quality `33326897749` were rechecked
successful at that exact commit. No overlapping writer or enabled worktree
lease was found. Unrelated Renovate PRs #93/#94 are untouched.

## Scope and agent panel

Implement the guarded single-slot primary entry and execution gate together,
using the [recorded design](../../context-packs/primary-session-gate-20260831.md).
Main owns integration, evidence and safety review; `runtime_profile_tests`
owns source/tests; `root_acceptance_map` performs acceptance review. Exact
agent model revisions are unavailable; correlated errors remain possible.
This is agent engineering agreement, not human agreement or external authority.
`runtime_security_review` owns the separate adversarial identity test file;
it makes no production changes. All reviewers are agents, not human validators.

The existing Unix-socket, process supervision, decoder and fixed READY session
are reused. Extract private lifecycle composition only; no generic server or
new dependency platform. Preserve READY constants, lock/circuit-breaker,
absolute deadlines, receipt/socket ownership and cleanup failure retention.
The public primary entry accepts a native protocol, exact slot and immutable
review commit, never supplied request bytes, callbacks, eligibility or a bypass.

The repository delivery process supplies the trust root: actual panel findings
are recorded after source commit S in a fixed-path record at review commit R.
Verify S ancestry and source-closure parity, not whole-tree equality. Bind exact
protocol/request/adapter/dependency and fresh internal eligibility identities
before any session receipt, directory, thread, socket or model process. Recheck
before reservation and after capture. Two checks do not eliminate filesystem
races or attest in-memory Python or OS containment. No new signing-key approval.

## Implementation and validation

Baseline full validation passed 1,286 tests in 181.40 seconds. Its reported
92.56% coverage included a new unexecuted identity source added during the run;
it is not a stable pre/post coverage comparison. Final full validation must use
stable completed sources. Fixture-first tests, implementation,
post-change full validation and final agent review remain pending. The author
also owns the bounded execution-identity helper and its fixtures. Actual model
cache eligibility, model inference, study freeze and observation admission are
not performed during this implementation. Synthetic positive fixtures are not
primary observations and cannot grant a production study permit.

Early review found boundedness gaps in the identity draft: cap reads before
allocation, prune excluded directories before walking them, and enforce a
whole-environment budget. Bind supported libpython bytes where applicable;
static import scanning cannot claim arbitrary dynamic-import closure. These
findings are under implementation review, not completed fixes yet.

Main and acceptance both found a wrong-checkout gap: hashing supplied checkout
A cannot attest the executing adapter imported from checkout B. Require exact
project module origins while retaining the in-memory-code limitation. A
read-only installed-metadata diagnostic confirmed Python 3.14.5 with no
`typing-extensions`: `referencing` requires it only below Python 3.13. The first
metadata query failed on that absent optional package; a bounded corrected query
confirmed the five installed validator distributions. No dependency was installed
or changed. Add supported-version dependency fixtures; do not turn an inactive
dependency into an impossible production gate.

The independent identity test lane initially observed 21 passes and four
failures: empty standard-library inventory, dependency spec-origin mismatch,
and project source count/aggregate budgets. The author fixed those checks
without weakening assertions; the expanded 33 synthetic tests now pass with
Ruff and basedpyright. Tests replace environment paths and metadata; no host
interpreter/standard-library or model-cache identity scan was run by that lane.

Gate fixtures initially mocked Git/file verification. A real temporary-Git
source-to-review fixture was added for ancestry, committed evidence and source
parity; a composed gate-to-synthetic-child/HTTP/decoder test remains required
before completion. Postflight dependency errors and interrupts must preserve
raw capture and earlier cleanup errors. Bind reviewer evidence to the same
source, protocol, closure and environment to reject stale-scope reuse.

Installed-source review confirmed `jsonschema` imports optional format modules
at import time, even without a format checker. The supported execution identity
must reject loaded or discoverable optional format extras rather than omit their
dependencies. This introduces no install/uninstall action. The check protects
the model lifecycle boundary; it cannot retroactively prevent earlier Python
imports or attest in-memory code. Execution still requires a clean reviewed
interpreter under the trusted repository workflow; there is no Python sandbox
or hostile-owner defence claim.

The expanded identity lane passed 65 tests including every optional format
module as loaded and discoverable. Two further regressions then exposed missing
origin checks for the `attr` alias and `jsonschema` submodules; the author is
closing that gap. A read-only check of the actual repository's static source
closure and imported project origins passed, without environment hashing or
model/cache access.

The combined real-Git gate and synthetic Python/Unix-HTTP/decoder integration
captured, decoded and reaped successfully. Its first failure was only a test
comparison of in-memory tuples against serialised JSON arrays; canonical JSON
comparison corrects that assertion without changing runtime behaviour. Final
combined tests, stable coverage and final acceptance are still pending.
That integration substitutes the complete project-identity helper, environment,
eligibility/profile, session source-pin observation and fixed executable for
synthetic equivalents. It is not an actual installed-runtime attestation. The
separate actual-repository static-closure check does not erase those fixture
boundaries or turn the synthetic response into a study observation.

## Final reviewed implementation

Fixture-first `uv run pytest -q --no-cov tests/test_prospective_execution_gate.py`
failed before the gate module existed: exit 2, one collection ImportError in
0.47 seconds. No separate pre-implementation RED is claimed for the primary
session module. Final fast focused run: 160 passed, four integration cases
deselected, 98.30% combined coverage; identity and primary modules reached 100%,
gate 97%. Those four real-Git/synthetic-child cases passed in the preceding
153-test combined run (100.06 seconds, 96.47%). The final loaded-submodule fix
then passed 69 independent identity tests and the actual-repository static
closure check. The authoritative full `uv run python -m tools.full_validation`
passed against stable sources: 1,407 tests in 230.14 seconds, 94.29% coverage,
plus lint, types, governance and regression checks. Code commit `1d01242`.
Hosted delivery remains pending.
Ruff and native/Windows basedpyright and ty passed.

Final acceptance review passed with all reported findings resolved. Main
confirmed the same source/test hashes; no code changed after this review.

- Gate: `68911f37e065a0e57620d9dd9fee71b89f71799d67f2b6e8ed0cdbb1d15f1c15`
- Identity: `f021984950cef86aec95cbab74b962985c21350f5c103a6e0e35c8a6bdedcae0`
- Primary adapter: `0c166718febbd9656f2cb713a51c414ada74ce9b5fd85e6d87b84cca8c3c12c0`
- Shared session: `997f5d2c549af7819a1504263cd4b842351a1bdbf3c59d76284d6e57a93e9941`
- Gate tests: `222f68da8fdc376a2565c551b3c103973516e8ca1eb8dd8b8d1e2587e8d8a2e4`
- Primary tests: `06f1cde22ba27325f4405c50244607264258d555bf3de566dd9ead08178328ca`
- Identity tests: `de310da36a9504538fa61da9c8997bed39f176944e4a13f9b426eab0276ab85b`

## Remaining boundary and rollback

The next [controller/admission context](../../context-packs/controller-admission-20260831.md)
records the panel's sequencing repair: implement those dependencies before
actual freeze so S/R binds the complete execution path. This remains approved
repository engineering; no repeat owner decision is needed.

No completion claim for the primary gate, owning track or root issue until
applicable acceptance evidence passes. Actual protocol/closure review and freeze,
governed two-slot capture and affirmative admission precede blinding and scoring.
Keep failures, raw evidence and historical H0–H8/H8P unchanged. Keep Apache-2.0,
per-artefact rights, private-data, credentials, spend and external-action gates.
Agent review is not clinical, legal, policy, regulatory, employment,
cultural-safety, organisational or deployment validation. Roll back only this
new primary composition and restore the compatible fixed session behaviour;
never alter historical evidence to fit new checks.
