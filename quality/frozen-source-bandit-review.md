# Bandit review for versioned prospective source

The historical `prospective-agent-text-20260830` protocol was actually frozen
and consumed. Its [execution freeze](../conductor/tracks/eval-blocker-remediation_20260803/prospective-execution-freeze-20260831.md)
binds source S `e6c1453d68b562829b99f40b925de6d287496601`, review R
`cd09dba47704f3c87b95975a216a9a5be98158bd` and protocol SHA-256
`650186fd54dd832532ea995c954862026203b848bb520e8e0cae7a4af8c80628`.
The [readiness addendum](../conductor/tracks/eval-blocker-remediation_20260803/readiness-addendum-20260831.md)
records zero admitted observations out of two slots and forbids recovery under
the consumed protocol. Historical declarations and negative evidence must not
be rewritten to accommodate a scanner comment.

## Historical exact-source review

Bandit 1.9.4 reports B603 for these argument-vector subprocess calls. The calls
do not invoke a shell. The first uses a verified executable and a fixed
diagnostic choice; the second validates the comparator admission before passing
the selected executable, model path and synthetic prompt as separate arguments.
This interpretation does not attest the safety of an arbitrary executable,
loaded-code identity or operating-system isolation.

| Source | Line | Rule | Reviewed source SHA-256 |
| --- | --- | --- | --- |
| `tools/darwin_runtime_profile.py` | 192 | B603 | `c910b867fa1bb71c397fd466fe0f57931cfe1894f2b49a5752befb4d3b854998` |
| `tools/local_model_comparator.py` | 203 | B603 | `429ae531533c5a90f618c3eb2f4d8f04c745c06ebf993159603710cefd25b090` |

These source bytes and `tools/darwin_server_v030.py` were restored exactly from
pre-change integration base `50c8a81d1cbffc451380dd2cb973cb33c7cc74cd`; the only
quality-branch differences in the two targets were new inline scanner comments.
The restored server profile SHA-256 remains
`c5bdd37eb8391baedd191c482996210ebdfbd43888ab8afb578092fafd8896c1`.
No protocol, condition, frozen input, historical receipt, outcome or execution
permission is changed. No model or study execution was performed.

## Historical enforcement and revalidation

`quality/bandit-reviewed.json` is a native Bandit baseline containing exactly
these two observed findings and their review metadata. Its reviewed SHA-256 is
`550bd037fc3580d1081f294bf50f06ecb36fd83859c4ec68e55717a32b78e647`.
Bandit's native matching compares finding attributes rather than exact source
bytes or line numbers. Therefore `tools.quality_gate security-baseline` runs
before Bandit and checks both the baseline digest and both source digests.
Any change fails before the exceptions are applied. All other production
findings remain enforced under the existing policy.

The integrated `tools.quality_gate security` command runs that fixity gate,
creates a temporary native Bandit baseline, then invokes the pinned scanner.
Only finding filename separators change to the host's native convention,
because Bandit compares filename strings literally. The reviewed JSON and
source bytes remain unchanged. The temporary file is removed and the scanner's
exit status is propagated; Windows does not acquire broader exceptions.

Revalidation means examining the actual new source and scanner findings,
retaining the historical protocol and updating only a justified current
engineering configuration with review evidence. It is an ordinary code review,
not a new owner approval. Never generate a broad baseline from the full report
to make CI pass. Do not change old protocol pins to satisfy current-code checks.

Tests cover altered baseline bytes and altered bytes in each source. Existing
Darwin source-pin tests and prospective protocol consistency tests remain
enabled and must pass. This is agent engineering review with shared project
context, not independent clinical or research validation.

## FAW06 current engineering revalidation — 14 November 2026

The active implementation now has checked comparator boundaries and explicit
runtime receipt types. CLI and server profiles have distinct current engineering
identities `darwin-llama-0.3.0-typing-20261114` and
`darwin-llama-server-0.3.0-typing-20261114`. The server source inventory additionally
binds the existing `json_shapes.py` runtime dependency. Historical source S, the
consumed protocol, review and zero-admission result above remain unchanged.
The historical consistency test reconstructs declarations from S in an isolated
interpreter; current source-pin tests independently check the active files.

The actual current Bandit scan still reports exactly the following two B603
findings. Each call keeps argv separation, no shell and the existing process
limits. Runtime capture keeps pre/post source checks, and comparator admission
now rejects malformed collections and scoring fixtures before their execution.
This is ordinary current-source engineering revalidation, not runtime/model
qualification or permission to reuse the consumed protocol.

| Current source | Line | Rule | SHA-256 |
| --- | --- | --- | --- |
| `tools/darwin_runtime_profile.py` | 242 | B603 | `31f0627bd3386a164872f1c14640e14b26a5551b7f61c6c23795ce2427a5c3ee` |
| `tools/local_model_comparator.py` | 336 | B603 | `f27bf6dcf890887bf30112982ba78843828d58ce00b8a1b3481f23a1c2a49074` |

The current native two-finding baseline is SHA-256 `fe1dbcc8e0ba35b659e648889757cc8eded387ce2d78c7807627538892adaa9a`.
`tools.quality_gate security` checks this digest and both reviewed source hashes
before invoking Bandit; the previous fixity/tamper and cross-platform path tests
remain enforced. No other finding is admitted. The prior baseline and source
bytes remain available at the immutable historical revisions described above.
