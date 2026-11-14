# FAW06 typing completion evidence

Date: 14 November 2026 UTC. This increment completes the active typing migration
from PR #130's merged base `e6d95394241661db117dc429976aaa6204a1128b`.
Local verification and exact source-head hosted acceptance are complete.
The final documentation head remains gated by its own checks and protected merge. This is synthetic engineering evidence, with no clinical or
model qualification.

[PR #131](https://github.com/edithatogo/rcagent/pull/131) publishes source commit
`c3d26b0c70a65f06dcab9f878db99d351de7b758`, tree
`2e7c36c831a4f92e78d508e8b15d28f554536ccb`, exactly matching local source commit
`fd9623a211e18a679e68730776af2f71ac48865f`. This final documentation update
records observed source-head acceptance. Its own exact-head checks and protected
merge will be recorded on the PR, separately from this immutable publication snapshot.

## Measured typing result

The final **3,198 diagnostics are removed**: 482 in production and 2,716 in tests.
All **153 Python files** remain in scope and pass an empty external baseline with
zero errors, warnings or information diagnostics. Ordinary basedpyright shrank
the committed baseline to an empty `files` object; every policy allowance is
removed. The original measurement and rollout provenance remain unchanged.
No baseline re-anchoring, new exclusions, ignored diagnostics or disabled rules
were used for this completion.

`reportExplicitAny = "error"` now prevents explicit `Any` from concealing a raw
boundary. An actual temporary fault file produces `reportExplicitAny` and a
nonzero checker exit. An AST check finds zero explicit `Any` references in the
153 active files. The two static engines, runtime guards and adversarial tests
cover different failure modes; a zero checker count alone is not a proof of
runtime correctness.

The [machine-readable receipt](../../../quality/typing-completion-verification-20261114.json)
binds exact source/configuration hashes, measurements, the fault probe, reviews,
valid-output comparisons and final acceptance observations. The
[boundary comparison](../../../quality/typing-completion-boundaries-20261114.json)
preserves 43 independently executed before/after cases.

## Contracts and defects repaired

Distinct CLI and server model-admission contracts flow into phase-dependent
output, execution and runtime receipts. Raw JSON and native values remain
`object` or checked structural containers until their relevant fields are
validated. Optional adapters retain lazy imports, generated synthetic inputs
and conservative capability claims. Missing dependency methods cannot count as
successful malformed-input rejection.

Evidence, provenance, retrieval, benchmark, autonomy, jurisdiction, privacy,
agent-panel, runtime discovery, interface actions and evaluation code now have
typed producer/consumer contracts. Arbitrary evidence extension values survive
round trips. Valid governed/public exports, audit chains, migration results,
retrieval lifecycle receipts, benchmark hashes and autonomy checkpoint bytes
match the pre-change implementation in the recorded controlled comparisons.

Boundary regressions reject malformed containers and category values, including
extra invalid records beside complete valid coverage; invalid transcript text;
invalid human-review declarations; malformed native metadata; and incorrect
source/update cadence. Evaluator inputs require nonempty case sets, unique safe
identifiers and correctly typed bounded thresholds before installation,
process launch or output creation. Event parsing no longer converts command
objects into activation evidence or accepts invalid token counts.

The independent 43-case comparison executes exact base and current source in
isolated interpreters. It records **33 repaired behaviors and 10 unchanged
controls**. Malformed after-cases attempt zero process launches. Positive
controls preserve panel receipt hashes and agreement/gate values, comparator
scores, valid event extraction and recordable unavailable/out-of-scope controls.
These are synthetic boundary observations, not model-performance measurements.

## Package and lifecycle interfaces

Reviewed helpers have explicit supported names instead of cross-module private
access. Session ownership is exposed through a nonblocking context manager that
releases its lock in `finally`. Capture revocation only discards authority; it
cannot mint a live witness. Constructors still require their private origin,
copy/pickle protections remain, and consumption removes a live witness before
later validation. No persisted receipt becomes execution authority.

Tests use checked fixtures and explicit mock contracts while retaining malformed
runtime values for rejection tests. Read-only review found no removed test
functions or lost behavioral assertions. The full collection comparison below
records the final additions and any platform-specific skips.

## Current engineering and historical research identity

Current CLI/server profiles use the distinct `typing-20261114` identities. The
server inventory binds all four imported project modules, including
`json_shapes.py`. Repeated source/artifact checks, fixed argument-vector process
execution, bounded stream handling and raw-output withholding remain intact.

The two Bandit B603 argv findings remain the same narrow reviewed calls. Their
current source hashes and external baseline are rebound after review; the
baseline SHA is
`fe1dbcc8e0ba35b659e648889757cc8eded387ce2d78c7807627538892adaa9a`.
A fresh unbaselined scan finds exactly those two findings and no scanner errors;
tamper tests still require rejection on changed source or baseline bytes.

Consumed source `e6c1453d68b562829b99f40b925de6d287496601`, its protocol and
historical review remain immutable. The consistency test reconstructs original
source declarations in an isolated interpreter and checks their historical
profile hash separately from current source fixity. The negative study outcome
remains 0/2 admitted observations. Current engineering revalidation does not
revive the consumed protocol or qualify a new study.

## Verification and acceptance

| Check | Observed result |
| --- | --- |
| Empty external basedpyright baseline | 153 files, zero errors/warnings/information |
| Ordinary baseline shrink and cap ratchet | Empty baseline, zero allowances; no growth against merged base |
| Explicit `Any` fault probe | Correctly rejected with `reportExplicitAny`, exit 1; active AST references zero |
| Ruff, formatting, ty and retained basedpyright | Passed |
| Hash-bound Bandit, Vulture and Unicode scan | Passed |
| Repository governance and deterministic benchmark | Passed; 7/7 synthetic cases |
| Live official skill validator, complete profile and monitored drift | Passed; current conformance true |
| Full integrated pytest | 2,183 passed, 52 failed, 11 skipped; 93.27% branch-enabled coverage |
| Fresh unchanged-base full pytest | 2,006 passed, the same 52 failures, 11 skipped |
| Final collection comparison | All 2,069 original IDs retained; 177 additions, all passing |

The local host denies AF_UNIX operations. All 52 failed IDs and all 11 skip IDs
match the fresh base run. Fifty failure messages match verbatim; the other two
match after normalizing only the generated `/tmp/rca-session-*` directory token.
All shared test statuses and skip messages are unchanged. This is environment
failure parity, not a passing full local suite. Hosted tests retain those paths.
The final AST comparison also retains all 1,004 original test functions and adds
61. The collection adds 177 cases, including parametrized regressions.

## Hosted source acceptance

[Quality run43553845148](https://github.com/edithatogo/rcagent/actions/runs/43553845148) completed successfully for exact source
`c3d26b0c70a65f06dcab9f878db99d351de7b758`. All nine jobs passed. The
[hosted source receipt](../../../quality/typing-completion-hosted-source-20261114.json)
records jobs, verified artifacts, exact measurements and limitations.

| Hosted check | Observed result |
| --- | --- |
| Linux Python 3.11 | 2,246 passed; 94.54% coverage |
| Linux Python 3.15.2 | 2,246 passed; 94.54% coverage |
| macOS Python 3.15.2 | 2,246 passed; 94.57% coverage |
| Windows Python 3.15.2 | 1,986 passed, 260 platform skips; its floor is deferred to the combined gate |
| Complete matrix coverage | All four branch databases validated and combined; 95% rounded, above the 90% floor |
| Release-admission mutation | 24/24 real kills; zero survivors, timeouts, errors or pardons |
| Scalene synthetic workload | 300 completed iterations; 21.42615 seconds workload wall time, 22.455020427703857 seconds profiler elapsed time |
| Profiling validity | Actual CPU and allocation samples; 5.032926559448242 MB reported sampled allocation footprint |
| Dependency, privacy/secrets, official conformance | Passed for this exact source head |

The profile is one synthetic instrumented observation, not process peak RSS,
a performance budget, a comparative speed claim or evidence for Rust migration.
The dedicated offline-security runs remain queued and supply no completed scan.

## Final delivery boundary

FAW06's typing migration and engineering source acceptance are complete. The
final documentation commit records that observed result; it is not claimed to
have already passed its own future checks. Normal protected delivery requires
that exact final head to pass the required checks before merge. The final head,
its observed CI runs and merge commit will be recorded on [PR #131](https://github.com/edithatogo/rcagent/pull/131).
Historical receipts retain their original publication-time observations.

## Review, rollback and next work

Two implementation lanes owned non-overlapping batches. Root integrated them
and implemented shared/runtime/lifecycle and remaining boundary changes. A
read-only reviewer examined both lanes and root changes, independently reproduced
the 43-case comparison and caught the optional-header-reader false pass; its
regressions and fix were re-reviewed. The completed evidence lane independently
checked root source closure, historical identity, native Bandit findings and
tamper tests. These agent reviews share project context and are not independent
human or model observations.

Rollback is a normal revert of the implementation, preserving original receipts,
historical source and negative results. Current source pins and the Bandit
baseline must move together to their reviewed revision; never disable fixity or
restore a disclosure defect to make a check pass. New diagnostics have zero
allowance after completion.

FAW07–10 remain the next component demonstration work. The broader Track 13,
death-review composition, multimodal/multi-model research, hallucination-rate
evaluation and selective Rust spike retain their existing acceptance plans.
FAW06 does not complete those capabilities or establish a frontier claim.
