# Prospective producer and admission typing increment

Date: 14 November 2026, Australia/Brisbane. Track 13 FAW06 remains the
user-directed priority. This is engineering evidence over synthetic fixtures;
it does not qualify a clinical capability or a historical study.

[PR #130](https://github.com/edithatogo/rcagent/pull/130) continues from PR #129,
merged at `388a4c610b2d38643890d5db28bc2d0241cb5926`. The published source and
baseline commit is `377d65346f6ebdaa099ea779633aa159b555fe86`; its tree
`e37b29c5b8ed91a587083686590589f2544421ba` exactly matches local commit
`7d200d818f0186b635b529978c454b0f7ca8d3a4`. The
[machine-readable receipt](../../../quality/typing-producers-verification-20261114.json)
binds source hashes, measurements, baseline maintenance, tests and limitations.
Final-head hosted observations are recorded separately on the PR.

## Result

Strict basedpyright diagnostics decreased from **4,431 to 3,198**, removing
**1,233**. Production debt decreased from **824 to 482**; test debt decreased
from **3,607 to 2,716**. All 153 Python files remain in scope. There are no new
file/rule/message signatures and no increased file/rule counts. The baseline
and every policy cap exactly equal the independently measured remainder.

| Boundary | Production before → after | Corresponding tests before → after |
| --- | --- | --- |
| Inventory and freeze | 82 → 4 | 116 → 5 |
| Execution identity | 16 → 0 | 12 → 5 |
| Server model eligibility | 6 → 2 | 215 → 0 |
| Slot binding | 20 → 2 | 172 → 1 |
| Reviewed execution plan | 58 → 10 | 213 → 8 |
| Owned observation admission | 151 → 12 | 221 → 51 |

Producer contracts also removed uncertainty from unchanged consumers, including
the study controller (71 → 49 production diagnostics), protocol and native
prerequisite checks. The three newly debt-free files are the inventory tests,
server-model tests and execution-identity producer. Explicit `Any` name
references in edited Python decreased from three to zero. Existing private API
usage and six uncertain adversarial dataclass-fixture reports remain visible.

## Contracts and preserved behaviour

Inventory now returns checked planning, submission, artifact-reference and
inventory results. `read_json` exposes its raw result as `object`. Schema values
remain equal to the prior implementation. The third-party JSON Schema adapter
narrows only its validator method; it does not cast a payload to a domain schema.

Freeze publishes `CommittedFile` as exactly `path` and `sha256`; execution
identity's separate file record also contains `bytes`. Freeze retains the
independent second protocol read and pin comparison before reference access.
The new regression presents a malformed second payload with the wrong pin and
requires `protocol_changed_during_verification`, so validation-order drift fails.

Model admission, runtime overlay, slot eligibility, review envelopes and
execution evidence have explicit contracts. A plan keeps immutable payload
bytes. Each `value()` call parses and checks a fresh nested object, including
request, model admission and evidence shapes, before returning it. Eleven new
tests reject incomplete or malformed plan structures. Structural checks do not
reattest model artifacts; the existing pin, rights, source-closure, environment,
review and repeated model checks retain that responsibility.

Observation admission types its journal events, receipts, issuer context and
returned summaries. Plan and receipt tuples remain variable-length before the
two-slot check. `_consume` accepts `object`, removes the live witness before
later validation, and preserves rejection on reuse. The checked plan getter
follows the existing early capture-flag rejection. Persisted nested fields are
narrowed at first use, keeping exception wrapping and health/completion/process
validation order intact. No persisted JSON receipt is treated as live authority.

All four frozen Darwin/comparator sources remain byte-identical to the base.
Historical protocols, reviews and negative outcomes were not rewritten. The
new project imports already belong to the current source closure; no historical
declaration was updated to accommodate changed engineering code.

## Baseline maintenance

Measurements used an empty external baseline with `--baselinemode=discard`.
The first retained run surfaced four relocated private-use reports and one
newly visible argument report. The argument report was repaired by typing the
constructed unsigned model-test dictionary, retaining its existing uncertain
producer values. No allowance was added for it.

A read-only reviewer traced the four private-use reports to existing qualified
uses, now expressed as explicit test imports or the variadic `Plans` alias.
Only two files were re-anchored: admission coverage tests (161 → 14) and the
admission producer (151 → 12). Their 312 entries became 26; no rule was added
or increased. This changed the stored total from 4,431 to 4,145. Ordinary
basedpyright then removed another 947 resolved entries, leaving 3,198. The final
retained run has zero unmatched diagnostics. No `--writebaseline`, enlarged
cap or new-file allowance was used; the original rollout `origin_commit` remains
`718b418eba3c17f149d52124b97532240870c0b1`.

## Verification at publication

| Check | Observed result |
| --- | --- |
| Ruff, formatting, ty and retained basedpyright | Passed |
| Exact baseline/cap ratchet against merged master | Passed; 3,198 retained diagnostics |
| Hash-bound Bandit, Vulture and Unicode scan | Passed |
| Repository governance and deterministic benchmark | Passed; 7/7 synthetic benchmark cases |
| Live official skill validator, complete profile and monitored upstream drift | Passed; current conformance true |
| Inventory/freeze | 83 passed before, 84 after |
| Execution producers | 169 passed before, 180 after |
| Admission fixtures | 86 passed before and after |
| Model-fixture annotation follow-up | 16 passed |
| Full integrated pytest | 2,006 passed, 52 failed, 11 skipped; 93.32% branch-enabled coverage |
| Fresh unchanged-base full pytest | 1,994 passed, the same 52 failures, 11 skipped |
| Collected test delta | 12 additions; no removed IDs |

The local host denies AF_UNIX operations. All 52 final failed IDs match the
fresh base run; 50 messages match verbatim, and two differ only in generated
session directories. Normalization is restricted to
`/tmp/rca-session-[a-z0-9_]{8}(?=/)`. Module origins and the base tree were checked,
and tests used `python -m pytest` with the shared locked environment. This is
unchanged-source failure parity, not a passing full local suite.

Full integration initially exposed another incomplete positive fixture in the
primary-session tests. It produced `invalid_execution_plan` before the intended
payload-drift and socket paths. The fixture now supplies complete model admission
and execution evidence, preserves all four original session values and shallow
copy behaviour, and leaves every assertion and shared fixture type unchanged.
The final rerun restored exact base failure parity.

Final-head hosted Quality must run Linux Python 3.11 and 3.15.2, macOS and
Windows, the four-input branch-coverage union, mutation and profiling. Dependency
review, privacy/secrets and official conformance must pass before normal merge.
The dedicated self-hosted offline-security workflow remains separate; a queued
run is not a completed scan. PR #129's complete hosted acceptance is appended to
the [prior receipt](./typing-native-evidence.md), without changing its original
machine-readable publication snapshot.

## Review and next work

Two implementation lanes owned inventory/freeze and execution producers with
their tests; the completed inventory lane then typed the admission tests.
A separate read-only reviewer checked source contracts, schema equality,
validation order, literal guards, fresh reconstruction, witness consumption,
fixture aliases, assertions and residual baseline reports. Root owned integration,
the admission producer, final consumer corrections, caps and delivery evidence.
Agent reviews share context; they are not independent human or model observations.

The next bounded lanes are:

1. Publish a distinct CLI model-admission contract in `prospective_model.py`,
   then type `local_output_probe.py` and their fixtures. The CLI overlay and
   receipt do not have all server-admission fields; do not reuse that schema.
2. Type `local_execution_probe._admission` before its phase-dependent capture
   and optional dependency-profile receipts. Preserve early rejection, timeout
   and launch-failure states, oversized-stream hash withholding and post-run pins.

Both scopes can use existing synthetic fixtures without model/hardware execution.
Next comes the static preflight/native-prerequisite tail, then the independent
retrieval and benchmark producers. Retain private-access debt until its API/test
design is deliberately reviewed. Rollback is a normal revert of this bounded
batch; preserve historical evidence and prior receipts.

FAW07–10 component demonstrations, triangulation and hallucination-reduction
experiments, Track 14 death-review profiles and the selective Rust spike remain
in their existing plans. This increment supplies no clinical validation, model
observation, measured hallucination-rate reduction or Rust-migration result.
