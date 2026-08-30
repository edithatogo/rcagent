# Bounded runtime profile implementation and observations

Base: `370d0689aebc0d440da723a21e9a044d20b3f860`; branch/PR:
`codex/prospective-continuation`, #83. This completes the bounded runtime
profile subtask, not prospective study admission or the parent track.

## Implemented boundary

`tools/darwin_runtime_profile.py` pins the original llama-cli executable,
direct libraries and five ggml backends: 16 non-system files in total.
It verifies canonical paths/hashes, loader aliases and the exact backend
directory inventory before and after execution. Only explicit old Cellar
directories enter the cleared child environment. No mutable global Homebrew
link, historical comparator registry, model or installed package was changed.

The helper captures a fixed version invocation with a 60-second timeout and
at most 1 MiB retained per stream. Complete raw stdout/stderr and their
hashes/counts remain in an exclusive local receipt. Missing/malformed traces,
unrecognised images, mismatched process IDs, unverified delayed-image names,
pin/alias/backend changes and process/output failures cannot pass. System
shared-cache/driver bytes are explicitly outside this profile; loader reports
are trusted diagnostics, not tamper-proof or atomic execution attestation.
Temporary storage is not a disk quota and egress is not independently enforced.

`tools/local_execution_probe.py --dependency-profile` reuses the same profile
with the existing full comparator/model admission, fixed synthetic READY
prompt, seed 42, temperature 0 and 16-token limit. Optional `--receipt` retains
raw evidence locally and prints only status/hash. Existing receipt paths stop
before execution; exclusive writes prevent overwriting a racing destination.
Legacy no-receipt CLI output remains available and must not be published
without inspection. All results remain `admitted: false`, `study_unlocked: false`.

## Failure preservation and bounded remediation

The first instrumented version invocation, at 06:38:42–06:38:43 UTC on
2026-08-30, exited 0 with unchanged checked pins, but correctly returned
`profile_failed`. Its complete 100,602-byte stderr trace contained macOS
`move loaded to delayed` transitions unsupported by the initial parser.
After adding that exact form, replay next rejected the previously unlisted
BLAS and Metal backends. Read-only hashes and `otool -L` identified them as
existing ggml 0.21.0 package files, not newly acquired dependencies.

Two evidence-led corrections added the reverse transition without weakening
full-image matching, then pinned those backends and rejected unexpected
backend-directory entries before discovery. The original failed receipt is
unchanged at local cache `probe-evidence/runtime-profile-20260830T0640.json`,
SHA-256 `2179bf741479a39683105d5ff9e9082b2865f890be6bcfcf75377c97c865a833`.
The filename is a run label; the receipt carries the actual times above.
Successful replay is recorded only as replay, not a retroactive successful run.

## Fresh local observations

After final validation and agent review, one fresh version invocation and one
fresh non-study model probe ran. Their full raw streams were decoded locally
and verified against every byte count/hash; no raw stream was changed.

| Observation | Actual result | Full local receipt SHA-256 |
| --- | --- | --- |
| Version, 06:50:15–06:50:16 UTC | `runtime_profile_observed`; 16 reported non-system images verified; complete 100,602-byte stderr; unchanged pins | `a112a78cadb10fb8b401048a87ecf47fc700fd585ccbacbccd7774ecdfe413a0` |
| Fixed READY probe, 06:51:03–06:51:16 UTC | `process_completed`; 16 reported images verified; 1,291 stdout and 100,500 stderr bytes; unchanged pins; generated READY observed | `591036271ffa803c27d64803c5484f34b3393a13750613d91523dffcee39969d` |

Full receipts remain outside Git under the existing local model cache's
`probe-evidence/runtime-profile-20260830-retry1.json` and
`probe-evidence/profiled-probe-20260830.json`. The inspected
[version projection](../../../evaluation/prospective/probes/runtime-profile-20260830.json)
and [probe projection](../../../evaluation/prospective/probes/profiled-local-execution-20260830.json)
declare omitted raw fields and bind their full receipt hashes. They do not
replace full raw evidence for any future admission. Stdout contains runtime
branding, a local model path, echoed prompt and performance text; deterministic
study normalisation/blinding is still required. No study case was processed.

Profile digest: `e2663ba51baf5f63434ed1644f9388452b9ef26ecad838ba0702d68b0bf4587b`.
The unchanged runtime/model registry pin and exact model identity are retained
in the probe receipt. The historical OpenSSL label discrepancy remains
documented; no historical receipt is rewritten to suggest a different package.

## Validation and review

Fixture-first import and optional-argument failures preceded implementation.
The new delayed-image regression also failed before its fix. Final focused
coverage: 114 tests across runtime/profile/protocol candidate modules, 100%
statement/branch coverage. Full `uv run python -m tools.full_validation` passed
681 tests, 93.02% coverage, lint, both type checks, governance and benchmark
checks on macOS/Python 3.14.5. Hosted checks must be refreshed on the new PR head.

The first implementation head `0df9b6f` passed hosted macOS and Linux checks
but failed ten Windows tests: native temporary paths were incorrectly used as
Darwin POSIX loader records, and a backend fixture used Windows separators.
The follow-up separates synthetic Darwin wire identities from real temporary
filesystem checks. Production runtime/probe sources and all retained receipt
hashes remain unchanged. The failed run is retained as
[hosted evidence](https://github.com/edithatogo/rcagent/actions/runs/33298138182);
it is not a passing cross-platform checkpoint.
The repaired fixtures pass 116 focused tests with 100% statement/branch
coverage, including two explicit malformed Windows-path loader records.
Agent security review confirms that native file checks and the real parser
remain exercised; the repair does not relax production admission boundaries.

`runtime_profile_tests` implemented adversarial tests; `runtime_security_review`
independently reproduced the delayed-image defect, reviewed the fixes and
replayed the retained trace, verifying all 16 local pins and aliases. The main
agent inspected the fresh receipts and output; the reviewer also independently
verified raw stream hashes/counts and exact public-projection parity. Exact agent model revisions
were unavailable; shared tooling and correlated errors remain possible.
Agent review does not constitute human agreement or clinical, legal, policy,
regulatory, employment, cultural-safety, organisational or deployment validation.

## Next and rollback

The [protocol-candidate validator](./protocol-contract-20260830.md) is also
implemented, but no actual study protocol is frozen. Next implement the
study-specific runner and deterministic normalisation, then commit a reviewed
protocol freeze and enable affirmative study-specific transitions only against
actual evidence. Historical H0–H8/H8P, root #1 and this parent track remain
incomplete. No acquisition, private data, credentials, release or merge occurred.

Rollback the new helper and optional integration without touching global links,
raw receipts or historical evidence. Retain all existing live study locks.
