# FAW06 native-contract typing and enum-boundary receipt

Date: 13 November 2026, Australia/Brisbane. This bounded increment is recorded in
[PR #129](https://github.com/edithatogo/rcagent/pull/129), following PR #128 merged
as `4d17acece190888e364f30a645b79b53cf31d66d`. FAW06 remains in progress. The
[machine-readable measurement](../../../quality/typing-native-verification-20261113.json)
records per-file changes, commands, exact source identities and evidence hashes.

## Measured reduction

Both measurements use locked basedpyright 1.40.2, an empty external baseline and
`--baselinemode=discard`. The base is merged `4d17ace`. Published source/baseline
commit `d2a8b217e97fe427acbc21a70d94a7ca20e98bb3` has tree
`13a6e6947196d9ef94acaca97d286028e0a74fa4`, exactly matching local integration
`75454f4fbe7069f9d194cfdf1d105a6117b0522b`. Documentation follows separately;
hosted acceptance must bind to the final PR head.

| Scope | Before | After | Removed |
| --- | ---: | ---: | ---: |
| Production | 1,008 | 824 | 184 |
| Tests | 4,015 | 3,607 | 408 |
| **Total** | **5,023** | **4,431** | **592 (11.8%)** |
| Files with retained diagnostics | 96 | 91 | 5 |

The five newly debt-free files are `tools/native_completion.py`,
`tools/prospective_runner_contract.py`, `tests/test_native_completion.py`,
`tests/test_prospective_protocol.py` and `tests/test_prospective_study_inputs.py`.
The last improves through its producers without a source edit. The new
`tests/test_enum_boundary_rejections.py` also has zero strict diagnostics and no
baseline allowance. There are 153 Python files in the final analysis.

No file/rule count grows. Every policy cap equals its current measured count;
zero-count allowances are removed. Explicit `Any` name references across the
edited Python files decrease from 24 to 22. Remaining upstream uncertainty and
intentional private-helper access stay visible instead of being concealed by
new `Any` annotations, ignores, blanket casts or disabled diagnostics.

## Typed boundaries and preserved behaviour

Native completion now returns a `DecodedCompletion`. The runner contract exposes
`Artifact`, `RequestLimits`, `RequestPackage` and `NormalizedCandidate`.
Inputs enter through `object` and checked narrowing. Both production modules now
have zero strict diagnostics. Their existing tests still cover duplicate fields,
nonfinite/overflowing numbers, invalid UTF-8 and surrogates, oversized inputs,
cyclic or aliased structures, exact-type comparison and bounded reconstruction.

The implementation preserves exact-integer rejection of booleans, checking
lengths before traversal, and checking the exact type before equality. A custom
integer's equality method must not run when types differ. Untrusted cyclic,
huge or custom values are not serialized during request reconstruction. Returned
keys, canonical bytes, request limits and hashes remain unchanged.

Legacy and native protocols expose artifact, case, scoring, document and candidate
contracts. Native candidates retain `dict[str, RequestPackage]` request packages.
The structural guards run after the existing schema and exact-integer checks;
the schema remains authoritative for enum meanings and additional fields. These
guards establish structure, not scientific admissibility.

The protocol changes preserve a single protocol read and one read of each of the
five referenced artifacts, request creation from the already verified bytes,
case-insensitive artifact-path uniqueness, independent legacy/native schema
objects, exact versions/generation settings and the two-slot denominator.
The protocol production modules retain eight reports from unchanged upstream
inventory helpers and private API access; they are not claimed fully typed.

## Nine concrete enum/hashability repairs

Checked container shapes previously allowed collection-valued enum fields to
reach hashed membership or set construction. The validators now require a string
before those operations and return their existing field-specific errors.

| Validator | Repaired fields |
| --- | --- |
| Interface registry | Template rights, field canonical path, interface status |
| Runtime registry | Dependency class, support state, network, telemetry |
| Adaptation registry | Framework status |
| Dataset manifest | Split name |

Twenty concrete list/dictionary reproductions failed with `TypeError` on the
unchanged implementation. All now require the intended validation errors. Nine
Hypothesis cases vary bounded list/dictionary contents without suppressing health
checks. Two of the concrete cases add a malformed split alongside all required
valid split names, so a guard cannot simply ignore the malformed row. In total,
29 new enum tests and 113 existing related tests pass. This repairs the nine
recorded field patterns; it does not assert that every repository boundary has
been exhaustively checked.

## Current source inventories and historical integrity

`json_shapes.py` is now listed in the current freeze component inventory and the
current native-prerequisite source inventory because the typed modules consume
it. A direct freeze regression changes the helper after freezing and requires
`freeze_bytes_mismatch`; the existing prerequisite parameter matrix also gains
the helper-drift case. These are enumerated dependency inventories, not a claim
of complete repository attestation.

Historical protocols, reviews, source receipts and negative results remain
unchanged. The four pinned production files remain byte-identical to merged
`4d17ace`: `darwin_runtime_profile.py`, `local_model_comparator.py`,
`darwin_server_v030.py` and `darwin_runtime_v030.py`. Current engineering changes
do not requalify the consumed study or authorize its rerun.

## Reviewed baseline maintenance

The ordinary retained-baseline run surfaced one unmatched report at
`tools/prospective_protocol.py:170`: `reportUnknownArgumentType` on
`require_object(obj(...))`. The unchanged inventory helper still returns
`dict[Unknown, Unknown]`; the new checked boundary exposes that existing producer
uncertainty at its argument. Read-only review found no new incompatible operation.

Only that file was selectively re-anchored to its seven remaining reports,
down from 51. Its residuals are five unknown-variable imports, one unknown
argument and one private-use report. The selected maintenance changes the stored
total from 5,023 to 4,979; ordinary basedpyright then removes another 548 entries,
leaving exactly 4,431. The final retained run has zero unmatched diagnostics.
Baseline counts and policy caps exactly equal the independent empty-baseline
measurement by file/rule. No `--writebaseline`, new allowance or cap increase
was used. The original rollout `origin_commit` remains unchanged.

## Verification at publication

| Check | Observed result |
| --- | --- |
| Ruff, formatting, ty and retained-baseline basedpyright | Passed |
| Baseline/cap comparison against merged `4d17ace` | Passed; exactly 4,431 retained diagnostics |
| Hash-bound Bandit, Vulture and Unicode scan | Passed |
| Repository governance and deterministic benchmark | Passed; 7/7 benchmark cases |
| Live official skill validator, complete profile and monitored upstream drift | Passed; current conformance true |
| Existing native I/O suite | 180 passed before and after |
| Existing protocol suite | 64 passed before and after |
| Enum regressions and existing validator tests | 142 passed |
| Consumer and freeze tests | 103 passed |
| Full integrated pytest | 1,994 passed, 52 failed, 11 skipped; 93.34% branch-enabled coverage |
| Same 52 failed IDs on unchanged source | 52 failures; zero normalized-message differences |
| Collected test delta | 31 additions; no removed test IDs |

The local environment denies AF_UNIX socket operations. A fresh comparison
checkout has exactly the merged base tree, with module origins verified and
`python -m pytest` used to avoid importing the wrong editable checkout. Fifty
failure messages match verbatim; two differ only in generated session-directory
names. Normalization is restricted to `/tmp/rca-session-[a-z0-9_]{8}(?=/)`.
This is unchanged-source failure parity, not successful socket integration.

Final-head hosted Quality must still execute Linux Python 3.11 and 3.15.2,
macOS, Windows, the complete four-input branch-coverage union, mutation and
profiling. Dependency review, privacy/secrets and official conformance must also
succeed before merge. The separate self-hosted offline-security workflow is
unchanged; queued is not a completed scan. Hosted observations are recorded on
the exact PR head separately from this local publication snapshot.

PR #128's prior accepted head `d8da1cb63ec40ca7200ec2ff0cbe079dd9cb18a2` passed
[Quality 43416154826](https://github.com/edithatogo/rcagent/actions/runs/43416154826),
dependency review, privacy/secrets and official conformance before normal merge
as `4d17ace`. Its separate offline-security run remained queued. Prior acceptance
is retained as history and is not used to accept this increment.

## Review and next work

Two implementation lanes owned native I/O and legacy/native protocol contracts.
A read-only reviewer inspected both lanes, reproduced their 180 and 64 passing
tests, compared schema equality with the base, and reviewed root's enum,
dependency-inventory and consumer changes. Root owned integration, global gates,
the baseline/caps and the evidence record. Agent reviews share project context;
they are not independent human or model observations.

Next, type the upstream inventory/schema helpers and migrate observation-admission
and execution-gate contracts together with their consumers. Their production debt
is now 151 and 58 respectively. Continue reducing the largest remaining test
fixtures while retaining justified private API debt. Rollback is a normal revert
of this bounded implementation; preserve historical evidence and prior receipts.

The deterministic component demonstrations, hallucination-reduction comparisons,
death-review profiles and selective Rust experiment remain in their existing
Conductor tracks. This increment makes no clinical qualification, model-observation
or Rust-migration claim.
