# Independent D2 temporal oracle

`d2_oracle.json` freezes 34 synthetic development cases across 15 families,
with 73 events, 74 clock assertions and all 46 unordered event pairs. The
accepted strict-order target contains 12 facts, including transitive relations.
The verifier specified literal UTC/local windows, summaries, pair orders,
cycle membership, infeasibility and amendment outcomes before reading or
executing either D2 producer. `freeze.json` records the exact oracle and
contract hashes and zero pre-freeze producer executions.

The cases cover source ordering and Unicode byte coordinates; separate event,
recording and recipient-availability clocks; missing and explicitly unknown
assertions; unresolved offsets and named-zone DST folds/gaps; explicit-offset
alternatives; equal, coarse, overlapping and touching windows; conflicting and
equivalent accounts; full asserted/transitive order; disconnected and self
cycles; one-second transitive infeasibility; union feasibility without extra
published order; explicit amendments, unamended revisions and amendment chains;
and invalid, partially invalid and unsupported clock expressions.

These fixtures use caller-declared synthetic event/clock associations. They do
not establish clinical occurrence, recipient understanding, automatically
extracted linkage, held-out performance or model qualification. Named timezones
remain unresolved. One-second inclusive windows represent uncertainty about a
single occurrence; display order is a deterministic presentation only.

## Scoring and execution

`evaluate_oracle()` and `score_cases()` in
`tests/test_faw09_independent_timeline.py` are callable independently. Only each
literal case's `input` is passed to the producer. Expected labels never enter
producer input, and no producer generator or clock parser supplies the oracle.
The scorer retains all event, clock, summary, pair and strict-order denominators,
including missing/failed executions. It scores the full implied strict-order
set, not merely direct graph edges or a display order. Duplicate or unexpected
strict orders are false positives. Undefined ratios are null. Scorer controls
reject all-unknown output and expose a missing transitive relation.

The 74 clock assertions include 61 usable UTC interpretations (58 resolved and
3 with explicit alternatives) and 13 unknown, invalid or unsupported
interpretations. Unknown and conflicting summaries have their own preservation
counts; they do not inflate UTC normalization recall. Feasibility must reject
impossible strict precedence without deleting alternatives or publishing an
internally selected point time. All 29 consistent and 5 inconsistent cases
remain in the case denominator.

Run with the existing locked environment:

```sh
uv run --no-sync python -m pytest tests/test_faw09_independent_timeline.py -q
```

The test suite additionally checks malformed containers and enum types, source
withdrawal and forged spans, typed domain references, duplicate identities,
unknown fields, exact resource boundaries, amendments, array permutations,
explicit association and recipient changes, replay tampering and real CLI
bytes/file hashes. These injected and metamorphic probes remain separate from
the literal temporal corpus metrics. No new dependency is required.

## Observed verification

[The verification receipt](./verification-receipt.json) accepts the bounded D2
contract at its recorded file hashes: 166 independent tests passed, all 73
events and 74 clocks were retained, every one of 46 pair rows matched, and
strict-order precision/recall were 12/12 with zero false positives or omissions.
All 61 usable UTC and 13 unresolved clock interpretations matched, as did all
158 summaries, including 105 unknown/unresolved summaries and 3 disagreements.
There were zero field errors, false blocking, false acceptance or execution
failures. The frozen oracle labels were not revised.

[The CLI execution record](./cli-execution-20261117.json) binds the complete
[96,602-byte stdout artifact](./d2-demo-receipt-20261117.json), including LF.
One fresh Linux subprocess took approximately 0.193 seconds and measured
peak child RSS of 25,280 KiB. These are individual execution observations,
not latency quantiles, a performance budget or a clinical workload estimate.
The producer's fixed demonstration is separate from the 34-case independent
corpus; its receipt carries its own exact counts and inputs.

The `attempts/` directory preserves the full initial producer outputs and the
initial comparison adapter's `clocks`/`clock_assertions` key mismatch. That was
a verifier integration error, not a production assembly failure. Correcting the
output-key mapping against the same saved results exposed no semantic mismatch.
Later passing tests and complete actual temporal outputs are separately bound
to final source hashes. Replay equality is not used as the independent oracle.

## Timestamp metadata correction

[Privacy run 43956603597](https://github.com/edithatogo/rcagent/actions/runs/43956603597)
reported one Presidio `PHONE_NUMBER` finding on the fractional timestamp in
`attempts/attempt-001-observations.json`. The
[metadata correction record](./metadata-correction-20261117.json) preserves the
published original commit, Git blob and byte hash, and binds the replacement.
The instant is now represented explicitly as `2026-11-16T20:55:14Z` plus
`observed_utc_microseconds=86646`. Adding that integer microsecond component
reconstructs the original instant exactly. Every other field, including all 34
actual case results, is unchanged. The frozen oracle, original verification
receipt and CLI artifact retain their hashes. No scanner rules, allowlists or
escape encodings were changed; the failed run remains part of the record.
