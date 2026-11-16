# FAW09 / D2 observed delivery and acceptance

**FAW09 / D2 is accepted for its bounded synthetic timeline contract.**
[PR #150](https://github.com/edithatogo/rcagent/pull/150) merged at
**07:18:50 Australia/Brisbane on 17 November 2026**, after all nine exact-head
Quality jobs, dependency review and privacy/secrets passed. Automatic master
conformance then passed on the actual merge before acceptance was recorded.
Track 13, Checkpoint B and the wider CAW10 / CS03 studies remain open; model
and clinical qualification remain zero.

This completes Dylan's instruction to implement D2, open a PR, check Actions
and merge. The [source completion record](./faw09-d2-completion-20261117.md)
retains the contract, development failures, reviews and local environment
restriction. The [machine acceptance](./faw09-d2-acceptance-20261117.json)
contains exact source, job and merge identities.

## Source identity and normal protected merge

| Item | Observed identity |
| --- | --- |
| Source PR | [#150](https://github.com/edithatogo/rcagent/pull/150) |
| Final tested source commit | `89425a12c15b4d533fb8610baed764fb429c86dc` |
| Merge commit | `8bf94873af22730e445fcbb1b7fb748cfd16ed25` |
| Tested and merged tree | `bda7e6384bca761842260a7a5c2dec64812dc2c3` |
| Merge base | `6f9cd9627adc52782a67fa6693f1cdb90c3c84a7` |
| Timeline SHA-256 | `254ea0ab87c30ab8ce568b1c892ae1c01c31ef46c8c6bc88778e92507b4eb020` |
| Clock parser SHA-256 | `b0e24b747cba8a6947cfeab39f22a8103c3251db6aa48cfcbe63269464e84855` |
| Frozen oracle SHA-256 | `dd3947ac70d54ccb5436040b1a190e19bba4f5b657a7b4781574eac76be13b92` |

The PR head, current master and active ruleset were checked immediately before
the normal expected-head merge. All required checks had succeeded. The observed
merge tree is identical to the tested source tree. No protection, review gate,
typing allowance, workflow or dependency lock was weakened or changed.

## Exact-head hosted results

| Gate | Observed result |
| --- | --- |
| [Quality 43957854760](https://github.com/edithatogo/rcagent/actions/runs/43957854760) | All nine jobs succeeded |
| Linux / Python 3.11 | 2,783 tests passed; 94.52% branch coverage |
| Linux / Python 3.15.2 | 2,783 tests passed; 94.52% branch coverage |
| macOS | 2,783 tests passed; 94.55% branch coverage |
| Windows | 2,523 passed; 260 platform skips; branch data retained for the required combined gate |
| Combined matrix coverage | All four nonempty branch databases validated; 95% rounded coverage, above the 90% floor |
| Release-boundary mutation | 24/24 mutants killed; no excluded verdicts |
| Synthetic CPU/memory profile | 300 actual iterations; measurement and workload gates passed |
| Prose lint and Ubuntu aggregate | Both succeeded |
| [Dependency review 43957855067](https://github.com/edithatogo/rcagent/actions/runs/43957855067) | Succeeded |
| [Privacy/secrets 43957854773](https://github.com/edithatogo/rcagent/actions/runs/43957854773) | Succeeded; zero Gitleaks findings and zero Presidio blocking/advisory findings across all 32 selected files |

The mutation gate covers the existing release boundary; it is not D2-wide
mutation coverage. The profile remains the repository's existing schema and
provenance workload, rather than a D2 or clinical latency estimate.

The full local gate remains recorded as **2,720 passed, 52 failed and 11
skipped**, with **93.38% branch coverage**. Its 52 failure lines exactly match
the prior D1 socket/session restriction; a direct AF_UNIX creation probe was
still denied. All 212 D2 tests passed locally, and the hosted suites above
passed with their unchanged socket tests. The local failure record is preserved.

## Retained first failure and metadata correction

The initial source `eb376cdb4144fbb91ac4db9c5ce2655059b8c4b7` passed all nine
jobs in [Quality 43956603499](https://github.com/edithatogo/rcagent/actions/runs/43956603499),
but [Privacy 43956603597](https://github.com/edithatogo/rcagent/actions/runs/43956603597)
flagged the generated fractional UTC timestamp in the first verifier execution
record as a phone number. Acceptance was withheld.

The [correction record](../../../tests/fixtures/faw09_independent/metadata-correction-20261117.json)
preserves the original published commit, blob and byte hash. Whole-second UTC
plus an explicit integer microsecond field reconstructs the exact original
instant, and all 34 actual results and every other field are unchanged. The
original oracle, verification receipt and CLI artifact keep their hashes.

An independent [component check](./faw09-d2-timestamp-check-20261117.json) used
the pinned phone-number dependency and inspected Presidio configuration. It
reproduced the original finding, found none in the corrected artifact, and
still detected the shared scanner's fictional positive control both alone and
beside the correction. The full hosted privacy workflow then passed on the
corrected head. No scanner setting, allowlist, exclusion or escape encoding was
changed. The [publication history](./faw09-d2-publication-attempts-20261117.json)
retains both observations.

## Master conformance

The PR's unchanged path filters did not trigger a separate conformance run.
Local pinned conformance had passed. Automatic
[master conformance 43958804476](https://github.com/edithatogo/rcagent/actions/runs/43958804476)
then succeeded on merge `8bf9487`:

- Validation job `133620370829` succeeded.
- The official validator and complete project profile passed.
- The installed validator revision was
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`.
- Actual contract-test logs reported **2,783 passed in 91.35 seconds**.

The separate automatic master Quality run was still in progress at this
acceptance observation; its snapshot is recorded accurately in the JSON.
Source-head Quality had passed before merge and the merged tree is identical.
A subsequent observation at 07:26:10 Australia/Brisbane confirmed all nine
jobs in [master Quality 43958804573](https://github.com/edithatogo/rcagent/actions/runs/43958804573)
and [master privacy 43958804670](https://github.com/edithatogo/rcagent/actions/runs/43958804670)
succeeded. The JSON retains both the earlier snapshot and this later result.
Offline AI security remains queued and is not a completed scan.

## Delivered capability and its limits

The focused suite contains **212 passing tests**, including **166 independent
tests**. The unchanged 34-case, 15-family oracle retains 73/73 events and 74/74
clock assertions. All 46 pairs and 158 summaries match, including 12 strict-order
true positives with zero false positives or omissions. All 61 usable UTC
interpretations and 13 unknown, invalid or unsupported interpretations match.
All 19 unknown pair orders, three disagreements and five inconsistent cases are
preserved; the 29 consistent cases have zero false blocking.

Supplementary review contributes 292 semantic probes and 109 malformed-input
rejections with separate resource, replay and positive controls. These are not
pooled into the frozen oracle's denominators. Agent review can share correlated
errors; these visible development fixtures do not establish held-out clinical
performance or a frontier result.

```sh
uv run --no-sync python -m tools.workbench d2-demo
```

The fixed command emits ten synthetic cases, 20 events and 41 clock assertions
as canonical UTF-8 JSON plus one LF. The 96,602-byte artifact has SHA-256
`30228ca7a438bda9327f1e6bbf3e6f8c7d4b78d8aad7e06a3ff19e0543ad3760`.
The module entry point emits identical bytes at these code/lock versions.

Event and clock linkage is explicitly supplied by synthetic annotations, with
exact D0 source provenance. Event, recording and each recipient's availability
stay separate. Coarse or conflicting times remain possible-time windows;
missing offsets and named zones remain unresolved. Graph constraints preserve
unknown order and inconsistency. Explicit amendments retain the original
assertions. The deterministic presentation adds no temporal evidence, and
availability does not prove reading, understanding or D3 decision entitlement.

## Next stage and rollback

**FAW10 / D3 is next and remains planned:** recipient/cutoff-scoped decision-time
packets and patient/family concern traceability, with future information hidden
through retrieval, verification and rendering. D3 and broader CAW10/CS03 studies
were not started by this assignment. Checkpoint B stays open.

A normal revert of the bounded D2 source increment is the rollback path.
Preserve D0/D1 acceptance, original independent labels, retained failures,
historical studies and other owners' work.
