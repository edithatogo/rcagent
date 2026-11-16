# FAW08 / D1 observed delivery and acceptance

**FAW08 / D1 is accepted for the bounded synthetic extraction contract.**
[PR #148](https://github.com/edithatogo/rcagent/pull/148) was merged at
**00:11:31 Australia/Brisbane on 17 November 2026** after every required
source-head check succeeded. Automatic master conformance then passed before
this acceptance was recorded. The wider Track 13, Checkpoint B and scientific
CAW02/04/08 packages remain open; model and clinical qualification remain zero.

This records observed delivery under Dylan's instruction to implement D1,
open a PR, check Actions and merge. The earlier
[source completion record](./faw08-d1-completion-20261116.md) retains the
contract, repairs, review, local restriction and failed development attempts.
The [machine-readable acceptance](./faw08-d1-acceptance-20261117.json) contains
the exact job identities and observations.

## Source identity and protected merge

| Item | Observed identity |
| --- | --- |
| Source PR | [#148](https://github.com/edithatogo/rcagent/pull/148) |
| Source commit | `3627e3a82424f18a19c865a380cb90181e648729` |
| Merge commit | `33ab6d20f294fd86de2b39659aea53b0941e80e9` |
| Tested and merged tree | `99d641040b0016deeb5e4b241747a7aec4ed0991` |
| Merge base | `d11548357baba6a1e20163139a366c6367a05432` |
| Implementation SHA-256 | `e03eeaa2ab5d235bdc8f20048c3bd9d15c7369a324f4575d865a7d893551e119` |
| Frozen oracle SHA-256 | `263143abe0c71bc02d7b04bd9593af3946f00c2ab64970786c922a005627aafe` |

The PR head, current master base and active ruleset were rechecked immediately
before merge. All nine Quality jobs plus dependency review and privacy/secrets
had succeeded. The normal merge used the expected-head guard. The observed
merge tree is byte-identical to the tested source tree; branch protection and
quality gates were not weakened.

## Exact-head hosted evidence

| Gate | Observed result |
| --- | --- |
| [Quality 43880194216](https://github.com/edithatogo/rcagent/actions/runs/43880194216) | All nine jobs succeeded |
| Linux / Python 3.11 | 2,571 tests passed; 94.55% branch coverage |
| Linux / Python 3.15.2 | 2,571 tests passed; 94.55% branch coverage |
| macOS | 2,571 tests passed; 94.57% branch coverage |
| Windows | 2,311 passed; 260 platform-specific skips; coverage collected for the required combined gate |
| Combined matrix coverage | All four nonempty branch databases combined; 90% floor passed |
| Release-boundary mutation | 24/24 mutants killed; no excluded verdicts |
| Synthetic CPU/memory profile | 300 actual iterations completed; profile gate passed |
| Prose lint and Ubuntu aggregate | Both succeeded |
| [Dependency review 43880194232](https://github.com/edithatogo/rcagent/actions/runs/43880194232) | Succeeded |
| [Privacy/secrets 43880194259](https://github.com/edithatogo/rcagent/actions/runs/43880194259) | Succeeded |

The 300-iteration profile remains the repository's existing schema/provenance
workload. Its observed timing does not establish a D1 or clinical-workload
latency guarantee. The mutation result covers the existing release boundary;
it is not repository-wide or D1-specific mutation coverage.

The full local gate remains recorded as **2,508 passed, 52 failed and 11
skipped**, with 93.35% branch coverage. Those failures are the existing
Unix-socket/session groups in an executor that denies AF_UNIX socket creation.
The hosted suites above ran unchanged and passed. The local failure record is
preserved rather than replaced by the hosted result.

## Master conformance

The PR's unchanged path filters did not trigger a separate conformance run.
Local pinned conformance had already passed. Automatic
[master conformance 43883158837](https://github.com/edithatogo/rcagent/actions/runs/43883158837)
then succeeded on the actual merge `33ab6d2`:

- Validation job `133354114485` completed successfully.
- The official validator and complete project profile passed.
- The installed validator revision was
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`.
- Actual contract-test logs report **2,571 passed in 70.23 seconds**.

The separate automatic master Quality run was still in progress at this
acceptance observation and is identified as such in the JSON record. It is
not counted as a completed run. Source-head Quality had fully passed before
merge, and the merged tree is identical. Offline AI security remains queued
and is not represented as a completed scan.

## Bounded verification and delivered command

The final focused suite passed **195 tests**, including **140 independent
tests**. The independently frozen 28-case, 14-family oracle produced 54/54
exact source/span/kind matches with zero false positives, omissions or field
errors. All 37 expected lexical normalizations and 17 expected unresolved
interpretations matched. Useful lexically resolved coverage is 37/54 (68.5%);
correct uncertainty never inflates normalization recall.

All three agent review roles accepted the final source bytes. Their additional
27 semantic and 33 lexical review probes remain separate from the frozen
corpus denominator. Original labels, failing attempts, earlier successful
source-bound receipts, D0 history and consumed research identities are retained.
These visible synthetic development results do not establish held-out clinical
performance or a frontier claim.

```sh
uv run --no-sync python -m tools.workbench d1-demo
```

The command emits 14 fixed synthetic cases and 30 lexical observations as
canonical UTF-8 JSON plus one LF. The verified 44,074-byte artifact has SHA-256
`19e4a8d28e62841fc15b31bd947f720b6016f35cf7030b51ead63c79147018a1`.
The module entry point emits identical bytes at these source/lock versions.
No dependency, lock, canonical schema, workflow or quality allowance changed.

## Next stage and rollback

**FAW09 / D2 is next and remains planned:** timeline and partial-order assembly
with separate event, recording and recipient-availability clocks, preserving
disagreement and unknown order. D1 emits atomic observations and leaves those
clock/linkage fields unknown. D2 and later work have not been started by this
assignment; no other owner's PR or track was merged here.

A normal revert of the D1 source increment is the rollback path. Preserve the
D0 acceptance, original independent oracle and failed observations, earlier
studies and other owner work.
