# H4 observed delivery and acceptance

H4's bounded synthetic packet consumer and its H2/H3 prerequisites were merged
through [PR #142](https://github.com/edithatogo/rcagent/pull/142), after the actual
source-head required checks, complete Quality matrix, Codecov, privacy/secrets
and conformance checks passed. This receipt records that observed implementation
merge; publication of this documentation is a separate commit.

## Accepted identities and merge

| Identity | Observed value |
| --- | --- |
| Source commit | `05975675467684f033e5d4df7320984a4c9eb3a1` |
| Tested source tree | `5c55fde1cbe324973b71413f63367c773391d523` |
| Immediately preceding master | `8a564826a3f51765f177f0d9823194718bacb7d9` |
| Actual merge commit | `006d98cb60c72143b0517f0e7a446641642ddd5a` |
| Actual merged tree | `5c55fde1cbe324973b71413f63367c773391d523` |
| GitHub merge time, UTC | `2026-11-16T21:39:59Z` |
| Acceptance observation, Brisbane | `2026-11-17T07:40:19+10:00` |

The normal merge used the expected source-head guard. The returned merge result
was observed, and the merged tree equals the tested tree. The active master
ruleset `21834601` required dependency review and Ubuntu/macOS/
Windows validation with strict up-to-date checking. No bypass was used.

## Hosted results before merge

| Check | Result | Evidence |
| --- | --- | --- |
| validate (ubuntu-latest) | success | [Job 133632634096](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133632634096) |
| Complete matrix branch coverage | success | [Job 133632471377](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133632471377) |
| codecov/patch | success | [Job 133631069347](https://github.com/edithatogo/rcagent/runs/133631069347) |
| Synthetic CPU and memory profile | success | [Job 133629494424](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494424) |
| validate (macos-latest) | success | [Job 133629494388](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494388) |
| Release boundary mutation gate | success | [Job 133629494242](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494242) |
| validate (windows-latest) | success | [Job 133629494070](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494070) |
| Python validation (3.15.2) | success | [Job 133629494042](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494042) |
| Python validation (3.11) | success | [Job 133629494036](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629494036) |
| Prose lint (Vale) | success | [Job 133629493477](https://github.com/edithatogo/rcagent/actions/runs/43961334353/job/133629493477) |
| privacy-and-secrets | success | [Job 133629213611](https://github.com/edithatogo/rcagent/actions/runs/43961334303/job/133629213611) |
| validate | success | [Job 133629212303](https://github.com/edithatogo/rcagent/actions/runs/43961334300/job/133629212303) |
| dependency-review | success | [Job 133629212105](https://github.com/edithatogo/rcagent/actions/runs/43961334352/job/133629212105) |

Quality run: [#43961334353](https://github.com/edithatogo/rcagent/actions/runs/43961334353).
The Ubuntu aggregate requires the complete Python/platform validation matrix,
mutation, profiling and combined branch coverage. The separately configured
offline AI security jobs remained queued for their self-hosted runner at this
observation; they were not required merge contexts and are not completed scans.
The machine receipt preserves those states separately from passing checks.
Automatic post-merge workflow states are later observations, not substitutes
for the checks that preceded this merge.

## Hosted test and coverage measurements

[Exact hosted metrics](./h4-hosted-ci-20261117.json) come from completed job logs
and the combined XML artifact, whose downloaded archive hash matches GitHub's
artifact metadata.

| Job | Passed | Platform skips | Total coverage |
| --- | --- | --- | --- |
| Linux Python 3.11 | 3,188 | 0 | 94.60% |
| Linux Python 3.15.2 | 3,188 | 0 | 94.60% |
| macOS | 3,188 | 0 | 94.63% |
| Windows | 2,927 | 261 | 88% rounded table value; floor deferred to the required combined gate |
| Combined four-member matrix | All required inputs present | — | 94.69%, above the 90% gate |

These per-job counts are repeated executions, not distinct cases to add together.
Codecov patch coverage is 93.63% against its 90% target. The repository release
boundary mutation gate killed all 24 mutants, with no excluded verdicts. Its
synthetic profiling result is a repository diagnostic, not an H4 latency or
clinical-performance guarantee.

## Implementation and engineering evidence

The delivered API and CLI prepare an original synthetic report, supplied
chronology, action register and exact-byte packet inventory. They preserve raw
ingress, source lineage, contrary accounts, uncertainty, separate clocks and
detached review/status/verification identities. Canonical validation precedes
rendering. Direct canonical support and profile support use the same eligibility
guard; detached output channels have case-insensitive name reservations.

The final H4 corpus has **304 passing tests**. All **25 frozen H3 cases / 38
variants** match the actual API, and two new clean CLI runs produce identical
**16-file / 94,722-byte packets**. The [current input manifest](./h4-input-manifest.json)
records 46 source/test/contract/dependency identities. The original H3 schemas,
oracle and literal expectations remain unchanged.

- [Hosted review repairs](./h4-hosted-review-repair.md)
- [Source-bound local validation](./h4-revision-validation.json)
- [Repaired-source oracle execution](./h4-revision-execution.json)
- [Repaired-source CLI replay](./h4-revision-replay.json)
- [Original checkpoint and its source identities](./h4.md)

The integrated local gate remains an actual failed observation: **3,125 passed,
52 failed, 11 skipped; 93.54% coverage; exit 1**. Its failures are the four
unchanged socket groups denied by the executor. The hosted matrix subsequently
passed on the accepted source. The first Windows typing failure, later Codecov
patch failure, both hosted review findings and an interrupted local attempt are
preserved. No failed or unavailable result has been relabelled as a pass.

## Scope and next stage

This accepts H4 engineering delivery for declared synthetic, fully local, safe
UTF-8 inputs. Source scope is record/reference integrity with raw artifact
bindings. H4.4 exact byte-span composition and H4.5 AcciMap composition remain
omitted and unqualified. D1 extraction and D2 timeline integration are also not
part of this HEAPS consumer, although their separately owned code is upstream.

**H5 is next:** independent qualification and engineering handoff against the
accepted revision. Its tasks remain unchecked; development-visible H4 controls
may be reused without becoming an H5 acceptance declaration. H6 still needs the
current authorised local instrument and applicable practice/data authority.
Clinical review, official-template conformity, operational effectiveness,
external submission, release and deployment are not established by this merge.

The broader track and issue #140 remain open. H1 shared receiving/ownership
tasks and portfolio registration remain separate; no portfolio number is
assigned by this receipt. Rollback uses a normal scoped revert while preserving
historical evidence and unrelated owner work.
