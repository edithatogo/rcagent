# Two-slot controller and immediate observation admission

Heartbeat 2026-08-30T19:46:17Z resumed clean checkpoint `3ae9a3f` on
`codex/prospective-controller-admission`; activation `37331aa`. Parent PR #100
is merged as `135881d42b50a710744ff353c317af80316c8935`; post-merge conformance
`33330379127` and Quality `33330379125` were reverified successful at that
commit. Root issue #1 remains open. No overlapping writer or enabled lease was
found; unrelated Renovate PRs #93/#94 are untouched.

## Scope and agent review

The [bounded context](../../context-packs/controller-admission-20260831.md)
implements controller and admission together before actual freeze, so the
reviewed source closure includes the complete execution path. Reuse the primary
entry, protocol, runtime and normalisation contracts; no new dependency or
signing platform. The standing decisions 20260830-001/002 apply without another
routine approval.

Main owns integration, documentation and evidence review. Agent
`runtime_profile_tests` owns the controller/admission modules, their direct
tests and the narrow execution source-closure update. Agent
`root_acceptance_map` reviews acceptance; agent `runtime_security_review`
reviews safety/privacy and evidence integrity. Exact model revisions are
unavailable, and correlated errors remain possible. This is agent engineering
review, not human agreement or accountable external validation.

The panel agreed these implementation constraints:

- Derive one deterministic run directory from study/protocol/review identity
  within the explicit evidence root. Exclusively create private journal and
  admission files; the primary entry exclusively owns raw-receipt creation.
- Record and persist attempt-start before each primary invocation. Exceptions
  can follow real execution; preserve consumed/uncertain attempts and later
  not-attempted slots. Never retry automatically, overwrite or infer resume.
- Admit immediately only through a private, one-shot, non-serialisable owned
  capture capability after journal sealing/readback and both direct captures.
  Recompute raw/request/response and protocol/review consistency before passing.
- Supplied JSON, matching hashes or file-shaped journals cannot recreate that
  capability. Durable admission output is evidence to be carried by the trusted
  workflow, not a portable self-authorising input. Offline custody and scoring
  remain separate transitions.
- At-most-once is scoped to the selected evidence root and study/protocol/review
  identity, not a global guarantee against an owner selecting another root.
  Python introspection, hostile same-user replacement, OS and in-memory code
  attestation remain outside the guarantee.

## Implementation and validation history

Baseline `uv run python -m tools.full_validation` passed against unchanged
sources: 1,407 tests in 230.08 seconds, 94.29% coverage; log
`/tmp/rcagent-controller-baseline.log`. Fixture-first
`uv run pytest -q --no-cov tests/test_prospective_study_controller.py` failed
before module creation: exit 2, one missing-module ImportError in 0.11 seconds.
Implementation, final agent review and post-change validation are not yet
complete. No actual model/cache eligibility scan, model inference, study
freeze, observation admission, blinding or scoring has occurred in this slice.

Early main and acceptance review found a FIFO substitution could block a read
before regular-file checks. Require nonblocking/no-follow descriptor handling
and verify regularity, ownership, mode, link count and identity before bytes.
Controller review also requires full first-receipt validation before the next
launch, directory rechecks, persistence of the evidence-root directory entry
and raw-receipt bytes, and a bounded failure-stage record without private
exception text. These are active implementation findings, not yet claimed fixes.

The independent adversarial lane initially passed 31 tests and failed one:
a hard link introduced during the read escaped the initial-only link-count
check. Repeat post-read checks are required. A separate capability-copy test
confirmed `dataclasses.replace` must not register a second live witness; live
registration was moved from construction to the private issue function.
Final validation and review still govern completion of both fixes.

The corrected independent suite passed all 43 cases with `--no-cov`, Ruff and
basedpyright. Admission-source SHA-256 remained
`fa74efff497c91ebda129b26a7d1799c815d0498c651218fcc5a1db3cd426e0a`
before/after that run. This is intermediate evidence; composed controller
fixtures, final sources and the full gate still need validation.

Initial direct controller fixtures passed eight cases, including immediate
two-slot admission with scoring/study-unlock flags still false, no inferred resume,
exceptions/interruptions consuming the first attempt, and first-slot cleanup,
journal-byte or directory-permission damage preventing the second launch.
These substitute the primary capture with explicit synthetic receipt bytes;
they are not composed child-process execution evidence. A composed synthetic
child test remains required. Review also requires durable post-seal failure
outcomes without rewriting the sealed journal and checked directory persistence
before reporting a successful admission.

The expanded independent suite passed 72 cases with Ruff and basedpyright.
It covers deep receipt-type/normalisation mutations, changed journals, capability
reuse and sealed failure evidence. Source hashes were stable across that run;
the final full validation below must still cover the released combined sources.
If a late persistence failure leaves an admission file, preserve it alongside
the locked failure outcome rather than overwriting evidence. A file's positive
field alone is never offline admission authority or successful controller delivery.

## Final reviewed implementation

All reported source findings are resolved. The first released focused run
passed 98 tests in 2.82 seconds, with 91% targeted branch coverage (admission
91%, controller 92%). Ruff and the author's scoped native/Windows type checks passed.
The composed test restores the real primary entry, child process, Unix HTTP,
native decoder, controller, journal and immediate admission. Git, eligibility,
profile, project closure/import origins and environment identity are synthetic
boundaries; neither that fixture nor its passing result is a primary observation.

Final acceptance requested two additional regressions: START-record fsync
failure before any primary call, and fresh gate drift specifically during
admission after both captures. These were absent from the earlier 98-test
snapshot; do not retrospectively claim them. Both now pass: the final focused
`uv run pytest --no-cov -q tests/test_prospective_study_controller.py
tests/test_prospective_admission_adversarial.py` passed 100 tests in 5.28 seconds.
Source bytes did not change. Final acceptance and main source review found no
outstanding implementation blocker. Functional commit: `a1e4399`.

Main's repository-wide Windows-targeted basedpyright run subsequently found
six direct POSIX-only constant references in the independent tests. Replace
those attribute references with `getattr`, retaining the exact flag assertions
and POSIX capability skips; the reviewer confirmed no weakening. Production
sources are unchanged. Windows-targeted basedpyright then passed with zero
errors, and the complete focused suite passed 100 tests in 7.15 seconds. Ty's
Windows-targeted check also passed. This supersedes any broader reading of the
earlier scoped Windows-check claim. The first `getattr` form then failed Ruff
B009; adding a zero default resolves the lint/type conflict without weakening
the flag assertion (a missing required flag still fails). Ruff, Windows-targeted
basedpyright and all 100 focused tests passed afterward (4.27 seconds).

Released SHA-256 identities:

- Admission: `ba5b6142f39d747ac659598a4872fc3a2e552ded1dcca1dfa096e7b4cec9e936`
- Controller: `b9844ae590f496a256bf5ccbcaf98e16d491373b1303f774faaf9bdfd044475d`
- Gate: `600dd38881d579ba14dc1e2b9551f38d77c64f57252ab94ec64bf3b2d02cdfd4`
- Direct tests: `1e49a61f144f6195daf5a3a3d302b6380e4864121a0a338c97eb551326f691e8`
- Adversarial tests: `6eb44ca0dda556243f7d3b37fa46aa346fd9196e9ce743475d30c1789e81d286`

The full gate already running when the two tests were added passed 1,505 tests
in 275.63 seconds at 94.16% coverage. This pre-extension run is not validation
of the final test set. The fresh `uv run python -m tools.full_validation` passed
against the final stable identities: 1,507 tests in 232.06 seconds, 94.18%
coverage, plus lint, types, governance and benchmark regression checks. Log:
`/tmp/rcagent-controller-final.log`. No actual model/cache scan or study operation
occurred. Hosted delivery remains pending.

## Hosted review repair

PR #101 at `0f5d562` passed all six hosted Actions checks but failed patch
coverage (88.95%, target 90%). Hosted agent comment 3890431238 also found a
valid P1 missed by the initial local panel: a raw receipt file was synced, but
its directory entry could remain unsynced until after the second capture.
The controller now syncs the run directory immediately after each raw receipt
readback, before validation, success/failure completion events or another launch.
Both successful and failed first-receipt sync faults are regression-tested.
No separate pre-fix RED run was performed for this repair.

The author added 11 controller cases; a separate agent added 14 admission
rejection cases. Acceptance re-review passed the narrow production change and
direct tests. All 125 focused tests passed in 3.56 seconds. The first main
focused invocation named a nonexistent test file and collected nothing; the
corrected invocation used `test_prospective_admission_adversarial.py`.
Native/Windows type checks and Ruff passed in the respective agent lanes.
Coverage targets and authority boundaries are unchanged. Full validation and
new exact-head hosted checks remained pending at that checkpoint.

Repair commit `1c33af4` passed final agent acceptance on all three changed
source/test files and the documentation delta. Fresh full validation passed
1,532 tests in 235.79 seconds at 94.56% coverage, plus lint, types, governance
and benchmark checks; log `/tmp/rcagent-controller-repair-full.log`. Both new
production modules have complete local statement/branch coverage. This does
not substitute for hosted patch coverage or observed study evidence.

Repair identities:

- Controller: `05e6d0e7ef4cff578479d4588bb51924e2faf346e7b2eded7529f01ab0e7c62a`
- Direct tests: `c23e949bb20ec89aefe296e5c511d709af1739416a650d68bf98ec68dba36940`
- Admission coverage tests: `c71852c13019663feac4be8864121d7ed7bf839f13abe218ddc17f7b6ed2774b`

## Remaining boundary and rollback

PR #101 passed all seven checks on reviewed head
`1618d912a49f11e231c7fd10cc2e46ca65c0579e` and merged at
2026-08-30T20:33:12Z as `4d621e6427b7024012f631a77f197ac117690f26`.
Reviewed and merged trees both equal `e11a46b693c9c49fd7b49fc058fc05a2b0aa10f6`.
Hosted conformance `33333822490`, Quality `33333824090`, dependency review
`33333824072` and patch coverage passed. Local master was fast-forwarded.
Post-merge conformance `33333964501` and Quality `33333964444` passed.
The completed local branch and stale remote-tracking reference were removed
after exact merge/tree verification; the remote branch was already absent.
Successor branch `codex/prospective-execution-freeze` is prepared. These checks
complete delivery of this implementation, not the owning track or actual study.

Do not close the owning track or root issue from this implementation. Actual
complete source/protocol review and freeze, eligible two-slot capture, custody,
blinding, agent scoring and analysis require their own passing evidence.
Historical H0–H8/H8P and all negative/raw evidence remain unchanged. Preserve
Apache-2.0, per-artefact rights, privacy, credentials, spend and external-action
boundaries. Agent review is not clinical, legal, policy, regulatory, employment,
cultural-safety, organisational or deployment approval. Rollback removes only
the new controller/admission composition and retains raw run directories and
the prior fail-closed primary and historical preflight contracts.

Acceptance review confirms the sequencing boundary: after this implementation
passes, actual synthetic protocol/input/rubric preparation becomes ready. A
complete execution S/R freeze need not wait for an independent offline scoring
implementation if that later path leaves the frozen execution modules unchanged
and has its own reviewed custody/source closure. If it requires changes to the
controller or gate imports, make those changes before freezing. A future trusted
custody record can bind raw/journal/admission bytes and S/R before blinding;
the saved admission JSON alone must never unlock that later transition.
Historical Track 5/6 wrappers remain fail-closed and unchanged.
