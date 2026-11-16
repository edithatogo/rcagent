# FAW07 / D0 observed acceptance

Observed at `2026-11-16T21:31:16.000+10:00`. This receipt accepts the already merged D0 source from
[PR #144](https://github.com/edithatogo/rcagent/pull/144). It does not claim delivery of the later documentation
commit that records this observation. The [machine-readable observation](./faw07-d0-acceptance-20261116.json)
contains the retrieved run, job, merge and worker identities.

## Delivered source

- Source head: `29d099b6e8d8507250c360481adba0fef63f91bf`.
- Source and merged tree: `4a8a2849255b317ba97085608557e7bd8841b99a`.
- Master base: `c6892497aa0b03555d5145242c04965471eccc1d`.
- Actual merge: [`d3c10d607470c9a50c5410030b80aeab2cfa5430`](https://github.com/edithatogo/rcagent/commit/d3c10d607470c9a50c5410030b80aeab2cfa5430), observed merged at
  `2026-11-16T11:26:09Z`.
- Normal merge with the exact source-head guard and active strict-base rules;
  no bypass, gate reduction, dependency change or worker-history rewrite.

Dylan's 16 November instruction authorised implementation, PR, passing Actions
and this merge. The [premerge completion record](./faw07-d0-completion-20261116.md)
records that authority before source editing and retains the implementation,
independent review, failed local observation and rollback rationale.

The D0 implementation reuses the existing evidence-core serialization and fingerprint
primitives, checked JSON-shape helpers, standard library and locked test tools.
The project-specific gap is the published D0 identity/span contract. The
existing integration fit remains applicable; no dependency or lock change was
needed.

## Acceptance gates

| Gate | Observed evidence |
| --- | --- |
| A0 | Original worker heads and ownership reconciled; bounded owner completion authority recorded; original worker acknowledgement remains unobserved |
| A1 | Real deterministic command, source/case/version/digest/UTF-8 span checks, bounded inputs, atomic rejection and inspectable receipt |
| A2 | 130 focused tests, including 40 independent tests and bounded properties; independent artifact calculations and three agent reviews bound to source-file hashes |
| A3 | Full hosted strict engineering suite passed on the exact source head; local socket-denied failures remain a separate failed observation |
| A4 | All nine Quality jobs, dependency review and privacy/secrets passed before protected merge; unchanged conformance path filters handled through pinned local validation and successful automatic master conformance |
| A5 | Actual source/merge/tree, Actions, worker disposition and preserved historical evidence reconciled in this receipt |

### Exact source-head Actions

[Quality run 43854810949](https://github.com/edithatogo/rcagent/actions/runs/43854810949) completed successfully
for `29d099b6e8d8507250c360481adba0fef63f91bf`:

| Job | Result | Evidence |
| --- | --- | --- |
| Prose lint (Vale) | success | [Job 133256210764](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256210764) |
| validate (macos-latest) | success | [Job 133256211064](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211064) |
| Release boundary mutation gate | success | [Job 133256211169](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211169) |
| Python validation (3.15.2) | success | [Job 133256211253](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211253) |
| validate (windows-latest) | success | [Job 133256211283](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211283) |
| Synthetic CPU and memory profile | success | [Job 133256211291](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211291) |
| Python validation (3.11) | success | [Job 133256211326](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133256211326) |
| Complete matrix branch coverage | success | [Job 133260420305](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133260420305) |
| validate (ubuntu-latest) | success | [Job 133263087998](https://github.com/edithatogo/rcagent/actions/runs/43854810949/job/133263087998) |

[Dependency Review 43854810885](https://github.com/edithatogo/rcagent/actions/runs/43854810885) and
[Privacy and secrets 43854810860](https://github.com/edithatogo/rcagent/actions/runs/43854810860) also passed.
Linux Python 3.11 and 3.15.2 each passed 2,376 tests with 94.64% branch coverage;
macOS passed 2,376 with 94.66%; Windows recorded 2,116 passed and 260 skipped.
The existing combined gate requires four valid branch databases and the 90%
floor. Mutation and profiling retain their existing scope and thresholds; their
success is not D0-specific mutation or performance qualification.

### Official conformance and master observation

The PR conformance workflow was **not triggered** by its unchanged path filters.
The filtered source/configuration inputs were unchanged. The [pinned local receipt](./faw07-d0-conformance-20261116.json)
passed with official validator revision
`69ef37e9424c0a7ea9dd2293b559e43ec8176379` and a complete project profile.
The automatic [merged-master conformance run 43857726512](https://github.com/edithatogo/rcagent/actions/runs/43857726512)
completed successfully at `d3c10d607470c9a50c5410030b80aeab2cfa5430` before D0 acceptance.

The JSON observation records other master workflows separately as they stood
at the observation time. Queued offline AI security is not a completed scan.
No master result is inferred from the successful PR checks.

## Reconciled worker history

The source commit includes both original worker heads as parents. Original
branches, oracle labels and historical receipts remain preserved.

| Worker PR | Incorporated head | Observed disposition |
| --- | --- | --- |
| [#132](https://github.com/edithatogo/rcagent/pull/132) | `4746027c7de6cd4e0ed1518241f847146d79faef` | Automatically marked merged after PR #144 integration; original branch preserved |
| [#133](https://github.com/edithatogo/rcagent/pull/133) | `4057512f23a2301d6ffe4649e42fb055eeb83937` | Automatically marked merged after PR #144 integration; original branch preserved |

The historical 35-pass/one-failure assembled candidate, original findings and
unobserved worker acknowledgement remain in the coordination record. The
complete local gate still records **2,313 passed, 52 failed, 11 skipped and
93.39% coverage**, with a directly confirmed AF_UNIX restriction. Hosted success
does not rewrite that observation into a local pass.

## Use and limits

```sh
uv run --no-sync python -m tools.workbench d0-demo
```

The generated corpus has five synthetic cases: two accepted and three rejected.
The deterministic output is 6,835 bytes including its final LF, with SHA-256
`4a97ca2a6998dece2fdb6ac10ce20fdca81d722d49073771985bb0e09af62c89`.
The [execution receipt](../../../tests/fixtures/faw07_independent/verification-execution-20261116.json)
binds implementation/test/lock identities and independent artifact observations.

**FAW07 / D0 is complete.** Track 13 remains in progress. FAW08 / D1 is planned
and was not started under this D0 assignment. Model runs and qualified clinical
or model capabilities remain zero. D0 demonstrates synthetic source identity
and exact byte-span inspection; it establishes no semantic truth, clinical
effectiveness, independent corroboration or operational release.

Rollback is a normal revert of the D0 integration change, preserving FAW06,
historical negative studies and unrelated owner work.
