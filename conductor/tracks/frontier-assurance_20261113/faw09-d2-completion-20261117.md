# D2 source completion and verification — 17 November 2026

This record covers the bounded synthetic FAW09 / D2 implementation. Source
review and local engineering observation are complete. Exact-head hosted checks
and observed merge acceptance are recorded separately; an implementation or a
green focused test does not complete delivery.

## Authority and scope

Dylan explicitly requested: implement D2, open a PR, check Actions and merge.
The clean starting master was `6f9cd9627adc52782a67fa6693f1cdb90c3c84a7`, after
D1 source PR #148 and acceptance PR #149. No open PR owned D2. The active
AcciMap, HEAPS, broader planning, security and dependency PRs retain their owners.
The branch is `feat/faw09-d2-timeline-20261117`.

The [frozen contract](./faw09-d2-contract.md) defines this contribution to
CAW10 / CS03: explicitly linked event annotations, independently supported
event/recording/recipient-availability clocks, conservative partial ordering,
uncertainty, disagreement and amendments. D3 decision-cutoff entitlement,
Checkpoint B and wider study qualification remain open. No model, private data,
clinical decision or new dependency is included.

## Implementation and reuse

`tools.faw09_d2_timeline.assemble_timeline(case)` verifies every source and
selected span through the existing D0 public API. The new small clock parser
uses standard calendar and fixed-offset arithmetic. `graphlib.TopologicalSorter`
checks cycles and supplies one deterministic presentation; bounded reachability
and feasibility checks retain the actual partial-order constraints. Existing
JSON guards, canonical hashes, pytest and Hypothesis are reused. The dependency
lock and D0/D1 source modules are unchanged.

The event and clock associations are caller-declared synthetic annotations.
They are not automatic links extracted from nearby D1 mentions, and exact
source bytes do not prove the truth or semantic entailment of an account.
Event assertion text is preserved; actor, subject and polarity remain explicitly
uninterpreted. Every listed recipient has a separate availability summary.

| Input or relationship | Result |
| --- | --- |
| Event, recording and recipient availability differ | Three independent summaries; no clock substitutes for another |
| Minute/date precision or an explicit interval | Inclusive possible-time windows on a one-second grid |
| Separated, fully supported event-time windows | A strict ordering only when every admitted alternative agrees |
| Overlapping, touching or interleaved alternatives | Unknown order; no invented point time or physical simultaneity |
| Equal reported seconds | `same_reported_time`, with no extra physical precision claim |
| Missing offset or named IANA timezone | Local values retained; absolute chronology unresolved |
| Explicit fixed-offset alternatives around a DST fold | Alternatives retained and converted individually to UTC |
| Cycles or infeasible precedence | Inputs retained, inconsistency exposed, accepted display order withheld |
| Multiple versions without an amendment | Separate active accounts and visible disagreement |
| Explicit valid amendment | Original retained and deactivated for current order; replacement and amendment provenance retained |

Unknown clocks remain unbounded during the internal feasibility check, even at
calendar limits. The internal earliest-feasible assignment is never exported
as an observation. Ordering includes the full transitive closure of asserted
and interval-derived edges, without claiming additional relations obtained by
pruning time alternatives. Named-zone transition validity, relative-expression
resolution and activity durations remain outside this grammar.

Inputs are bounded to 32 sources of 65,536 UTF-8 bytes each, 16 events, 16
recipients, 32 clocks, 32 relations, 16 amendments and 64 domain spans in total.
Clock expressions are at most 512 bytes with at most four alternatives.
Case/version/digest/coordinate/view/endpoint failures reject the whole input;
there is no silent prefix, unknown-node creation or partial span admission.

Run the deterministic, input-free demonstration with:

```sh
uv run --no-sync python -m tools.workbench d2-demo
```

The direct `python -m tools.faw09_d2_timeline` entry point emits identical
canonical UTF-8 JSON plus one LF. Its ten fixed cases contain 20 events and 41
clock assertions, including separate clocks, uncertain/overlapping windows,
offset equivalence, explicit precedence, impossible constraints and an amendment.
The receipt includes inspectable inputs, outputs, provenance and current
implementation/lock fingerprints; the producer contains no expected labels or
accuracy metrics. `verify_timeline` is a deterministic replay check, separate
from independent semantic verification.

## Independent verification and retained failures

The independent lane froze 34 literal cases across 15 families before reading
or executing production. Oracle SHA-256:
`dd3947ac70d54ccb5436040b1a190e19bba4f5b657a7b4781574eac76be13b92`.
Expected labels include 73 events, 74 clock assertions, 46 unordered pairs,
12 strict-order facts and five inconsistent cases. The oracle remains unchanged.
Its [scoring protocol](../../../tests/fixtures/faw09_independent/README.md),
[freeze](../../../tests/fixtures/faw09_independent/freeze.json),
[verification receipt](../../../tests/fixtures/faw09_independent/verification-receipt.json)
and original execution attempts are retained under
`tests/fixtures/faw09_independent/`.

The final independent suite passes **166 tests** on the reviewed source. It
retains all 73 events and 74 clock assertions; all 46 pair records match,
including 12 strict-order true positives with zero false positives or omissions.
All 61 usable UTC interpretations and 13 unresolved/invalid/unsupported
interpretations match. All 158 summaries match, including 105 unknown or
unresolved summaries and three disagreements. All 19 unknown pair orders and
all five inconsistent cases are preserved; the 29 consistent cases have zero
false blocking. There are no field errors or execution failures. Together with
the 46 root tests, the focused D2 suite contains **212 passing tests**.

These are visible synthetic development examples. Missing/unknown and invalid
clocks remain in their denominators, with useful resolved output reported
separately. Correct abstention does not inflate order recall. Supplementary
reviewer probes are not pooled into the frozen-oracle metrics.

The root suite has 46 passing tests, including 35 generated day-shift examples.
The [agent review receipt](./faw09-d2-review-20261117.json) records two further
independent lanes: 292 semantic checks, including 256 small-graph assignment
and reachability cases; and 109 malformed/forged/resource rejections, seven
accepted boundary cases, nine replay rejections, four graph checks and two
positive amendment checks. Three clean CLI processes produced identical output.

Review found and repaired two concrete admission defects: string-like Python
objects could pass the view check or leak a serialization error from clock kind;
the first length guard could overflow on a huge non-object range. Each failure
was reproduced before repair and remains a permanent regression. Early test
helper and strict-typing failures are also retained in the attempt history.
No skip, xfail, allowance or reduced gate was introduced.

## First hosted publication and metadata correction

Initial source commit `eb376cdb4144fbb91ac4db9c5ce2655059b8c4b7` in
[PR #150](https://github.com/edithatogo/rcagent/pull/150) passed all nine jobs in
[Quality 43956603499](https://github.com/edithatogo/rcagent/actions/runs/43956603499)
and dependency review. [Privacy 43956603597](https://github.com/edithatogo/rcagent/actions/runs/43956603597)
reported one phone-number finding in the fractional timestamp of the first
independent execution record; Gitleaks was clean. Acceptance was withheld.

The [metadata correction](../../../tests/fixtures/faw09_independent/metadata-correction-20261117.json)
represents that generated instant as whole-second UTC plus a separate integer
microsecond field. Exact reconstruction and equality of every non-timestamp
field, including all 34 returned cases, passed. The original published commit,
blob and hash remain retrievable, and the correction binds both representations.
Two relevant independent tests passed. Production, tests, oracle, lock, original
verification receipt and CLI bytes are unchanged. The scanner and its rules are
unchanged; no suppression or exclusion was introduced. The
[publication attempt record](./faw09-d2-publication-attempts-20261117.json)
retains the failed observation and requires fresh exact-head hosted acceptance. The
[independent detector-component check](./faw09-d2-timestamp-check-20261117.json)
reproduced the original finding, found none in the corrected artifact, and
still detected the shared scanner's documented fictional positive control
both alone and beside the corrected metadata. It executed the exact pinned
phonenumbers component, not the complete Presidio/Gitleaks workflow; hosted
privacy acceptance remains required.

## Engineering evidence and delivery boundary

The exact reviewed source SHA-256 identities are:

| File | SHA-256 |
| --- | --- |
| Timeline | `254ea0ab87c30ab8ce568b1c892ae1c01c31ef46c8c6bc88778e92507b4eb020` |
| Clock parser | `b0e24b747cba8a6947cfeab39f22a8103c3251db6aa48cfcbe63269464e84855` |
| Workbench | `122152d01584ff72749c8f3ce3f2e6f0efaafdeddd1699b72a55418ed05a9dd2` |
| Dependency lock | `ad939a067ac2eb2f0558e06f748b780f03dbe0c9046feb3a66e92888c6ff8e1c` |

Focused Ruff, ty and strict basedpyright pass. The
[official conformance receipt](./faw09-d2-conformance-20261117.json) passes local
profile validation and the pinned upstream validator
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`. Its live drift check found changes only
outside the monitored specification, validator and guidance paths.

The [full local gate receipt](./faw09-d2-local-engineering-20261117.json)
records all eleven pre-pytest gates passing, followed by **2,720 passed, 52
failed and 11 skipped tests**, with **93.38% branch coverage**. The 52 failure
lines exactly match the D1 environment receipt; a fresh direct AF_UNIX probe
still raises `PermissionError: [Errno 1] Operation not permitted`. The complete
local gate therefore did not pass. All 212 D2 tests passed, and the unchanged
hosted matrix must establish acceptance without disabling socket tests.

All nine exact-head Quality jobs, dependency review, privacy/secrets and normal
protected merge remain delivery gates. The existing conformance path filters
are unchanged; automatic master conformance is inspected after source merge.
Queued offline AI security is not a completed scan. Historical D0/D1 artifacts,
negative studies and earlier source receipts remain immutable.

A normal revert of this bounded increment removes the D2 modules, dispatcher
and related tests without altering D0/D1 or other owners' work. No model or
clinical capability is qualified. The next planned increment is FAW10 / D3:
recipient/cutoff-scoped decision-time packets and concern traceability.
