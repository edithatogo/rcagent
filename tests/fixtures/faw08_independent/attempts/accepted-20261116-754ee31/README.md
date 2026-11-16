# Independent D1 synthetic oracle

`d1_oracle.json` freezes 28 development cases across 14 semantic families. All
twelve families required by the D1 capability ladder have positive and adverse
variants. The additional families cover Unicode byte coordinates and invalid
clock components. There are 54 expected observations: 37 lexically resolved
and 17 partial, ambiguous, invalid or unsupported. Two cases have no supported
observation.

The verifier authored the literal texts, interpretations and context labels
before importing, executing or reading the D1 producer. Byte coordinates and
source digests were calculated directly from those literal UTF-8 strings with
Python's standard library. `freeze.json` records the exact oracle hash, base
revision and contract hash. No producer fixture generator supplies labels.
The producer owner received contract clarifications and the frozen hash/counts,
not the full expected fixture contents for implementation.

These are visible synthetic development fixtures. They do not establish
held-out performance, natural clinical error rates, clinical qualification,
model quality, chronology or decision-time entitlement. Unknown clocks and
linkage remain unknown. Full-source D0 admission witnesses are not included in
observation counts.

## Scoring

The callable `evaluate_oracle()` in
`tests/test_faw08_independent_extraction.py` submits only each case's `input`
object to `extract_case`. It returns the raw results and `score_cases()` metrics.
The independent scorer uses one-to-one exact case/source/version/hash,
coordinate-system, byte-interval and kind matching. Duplicates and unexpected
observations are false positives. Missing observations are false negatives.
Missing or failed executions retain their expected denominator.

Semantic field errors are reported separately from span/kind precision and
recall. Correct resolved output requires every expected normalized, lexical,
polarity, attribution, context and anchor field to match. Normalization recall
uses the 37 expected resolved observations as its denominator. Useful resolved
coverage uses all 54 expected observations. Correct uncertainty recognition
uses the 17 unresolved observations and never increases normalization recall.
No-observation controls retain false-positive opportunities. Undefined ratios
are null. Scorer controls demonstrate that all-abstention cannot pass.

The test module also checks malformed/forged input and anchor admission,
resource bounds, candidate overflow, every output field's replay binding,
source/revision/order/content identity, Unicode prefixes, clause-local polarity
and attribution, explicit anchor removal, and actual subprocess stdout and file
hashes. Replay verification is tested as deterministic consistency, not used as
the independent semantic judge. No new dependency is required.

## Reproduction and attempt history

Run the independent tests with the existing locked environment:

```sh
uv run --no-sync python -m pytest tests/test_faw08_independent_extraction.py -q
```

The `attempts/` directory retains complete stdout/stderr and hashes for observed
pytest runs, plus separately identified literal-result evaluations. First-run
failures are retained. A run whose source changed during execution is explicitly
development history, not a stable-source acceptance verdict. Changes to the
semantic labels after the freeze require an explicit revision record; no such
label changes have been made.

Injected corruption and metamorphic probes are engineering boundary checks.
Their outcomes are not pooled into the literal corpus's extraction metrics.
Elapsed time for one test subprocess is a recorded execution observation, not a
latency distribution, memory bound or clinical workload performance claim.

## Observed verification, 16 November 2026

[The verification receipt](./verification-receipt.json) accepts the bounded
synthetic contract at its recorded file hashes. All 140 independent tests pass.
The unchanged oracle has 54 exact span/kind true positives, zero false positives,
zero omissions and zero semantic field errors. All 37 expected lexical
normalizations and all 17 expected uncertainty states match. The two
no-observation controls produce no false positives.

[The CLI execution record](./cli-execution-20261116.json) binds the complete
[44,074-byte stdout artifact](./d1-demo-receipt-20261116.json), including its
final LF, to the measured implementation and lock. The single Linux execution
took approximately 0.123 seconds and recorded peak child RSS of 25,004 KiB.
These are one execution's observations, not performance thresholds or a
clinical workload estimate. Complete actual oracle outputs and earlier failures
remain in the attempt history; the frozen labels have not changed.
