# H4 hosted review repairs and boundary coverage

The hosted review of `a9df9ba581eeeeae9a777546125225fae2c88b25` found two
material admission defects. The same production bytes remained in portability
repair head `5317c64852aca80ecdf6005ccd0bf02124b979c0`. Independent author, test
and read-only review lanes reproduced both defects. Neither head was merged.
The earlier [review checkpoint](./h4-review.md) remains an actual historical
observation; these subsequent findings superseded its merge recommendation
until repaired and verified.

## Findings and repairs

| Finding | Reproduction | Bounded repair |
| --- | --- | --- |
| [Canonical support eligibility bypass](https://github.com/edithatogo/rcagent/pull/142#discussion_r4591654957) | An accepted finding with a direct canonical `supports` edge from a withdrawn factor was prepared when the profile omitted that support reference. | Apply the same eligibility guard to direct canonical support edges and supplementary profile support references. |
| [Case-insensitive detached filename collision](https://github.com/edithatogo/rcagent/pull/142#discussion_r4591654967) | A source cited as `STATUS.JSON`, with an allowed null snapshot locator and correctly bound bytes, produced both `STATUS.JSON` and generated `status.json`. | Reserve all six detached root filenames case-insensitively before reading/parsing construction inventory entries. |

Accepted findings cannot take positive support from withdrawn/rejected factors
or statements, a factor's directly referenced withdrawn/rejected statement, or
withdrawn evidence. Historical, contradictory and other non-support relations
remain representable, as do findings that are still drafts. The check does not
infer transitive support or establish clinical truth.

The reserved names are `manifest.json`, `decision.json`, `status.json`,
`verification.json`, `verification-input-manifest.json` and
`verification-input-status.json`. Similar unreserved names and ordinary nested
artifacts retain their existing treatment. Frozen H3 schemas and expectations
are unchanged.

## Independent review

The first two persistent regressions failed on the old production source and
passed after the repair. The separate read-only reviewer executed 28 targeted
API cases: 16 canonical/profile ineligible-support rejections, three historical
relationship positive controls, two draft-finding positive controls, six
uppercase reserved-channel rejections and one unchanged positive base case.
Every constructed case first passed canonical validation. Source hashes were
stable throughout that reproduction, and the base construction manifest
remained `82033516da3eabbd365952c04d6a7689130729470247c616d9c4952fe09ab4ca`.

The production repair changes only `tools/heaps_validation.py`, now SHA-256
`b927daa9f6e5edcbc4a1139349405fa73ffaa070601b7631d6bc052261235a4c`.
`tools/heaps.py` remains
`ea9fe374ae7f387d92d11ab7800bd2c636d947f5e62a03e88d5ed75c504dd55b`.

## Observed patch-coverage failure

The four platform/Python validation jobs passed on `5317c64`, including the
previously failing Windows job. Its separate
[Codecov check](https://github.com/edithatogo/rcagent/runs/133619071523) failed:
81.97832% patch coverage against the configured 90% target, with 70 missing and
63 partially covered lines. The complete-repository coverage result was not a
substitute for this patch result.

Additional tests exercise source availability and lineage, support eligibility,
portable filenames, exact template selection, semantic binding of historical
inputs and CLI publication failure. The separate CLI boundary module checks
actual public entry points; deliberate filesystem failure injection verifies
that competing output survives cleanup. These are development-visible synthetic
engineering controls. No threshold, ignore list, dependency, CI workflow or
typing allowance was changed.

## Verification and acceptance boundary

The current [input manifest](./h4-input-manifest.json) identifies the repaired
source and tests. Earlier execution/replay/conformance receipts retain their
original source identities. Fresh verification and hosted results must be bound
to the new revision; the earlier passing platform jobs do not approve changed
bytes. H5 and H6 remain separate, unaccepted stages, and the nonrequired offline
security job remains a pending scan until an actual runner result is observed.

## Repaired revision verification

The final focused run passed **304 tests**: 290 primary H4 cases and 14 CLI/API
boundary cases. Standard branch coverage was 95.71%; counting partially covered
lines as uncovered gives **706/754 = 93.63395%**, above the configured patch
target. This local calculation remains distinct from a hosted Codecov result.
Ruff, formatting, ty, Windows-target ty and basedpyright passed with zero typing
diagnostics or allowances.

[New oracle execution](./h4-revision-execution.json) matched all 25 cases / 38
variants against the repaired production source; literal H3 expectations remain
unchanged. [Two new actual CLI runs](./h4-revision-replay.json) on reconciled
master `8bf94873af22730e445fcbb1b7fb748cfd16ed25` again produced identical 16-file,
94,722-byte packets, with the unchanged output inventory hash
`b3e28fac0a5067151bae0a7d9a20d10e82bcddc4a7b46a71be46a8c60cda8172`.
This master includes the separately owned D2 implementation merged through
PR #150. No H4 production, fixture or runtime dependency identity changed during
that normal merge, and HEAPS does not compose D2.

The [integrated local gate](./h4-revision-validation.json) completed with exit 1:
**3,125 passed, 52 failed, 11 skipped; 93.54% coverage**. All pre-pytest strict
stages passed. The same four socket-restricted groups account for every failure;
no failing result is counted as a pass. A prior attempt on the earlier base lost
its execution session before a final result was observed; its incomplete log
identity is retained separately. The complete integrated run is the new local
observation. Hosted checks on the actual published revision still gate merging.
