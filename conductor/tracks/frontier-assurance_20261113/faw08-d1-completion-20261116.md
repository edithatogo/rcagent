# FAW08 / D1 source completion and integration record

This document retains the premerge source record. The subsequent
[observed acceptance](./faw08-d1-acceptance-20261117.md) records actual hosted
results, protected merge and master conformance. Pending statements below
describe the original source-verification time.

## Authority, scope and reconciliation

On 16 November 2026 Dylan instructed this conversation: **"Implement D1, open a
PR, check actions pass, then merge."** The [frozen contract](./faw08-d1-contract.md)
defines this bounded increment. Its base is
`d11548357baba6a1e20163139a366c6367a05432`, which includes D0 source delivery,
the D0 acceptance reconciliation and the independently merged ty/lock update.
The isolated branch is `feat/faw08-d1-extraction-20261116`.

No competing D1 owner or active D1 PR was present during live reconciliation.
AcciMap #141, HEAPS #142, the broader recommendations plan #143, StepSecurity
#146, the separate decision-model plan #147 and dependency-update PRs retain
their own scope. This assignment does not merge or replace those changes.

The source owner changed only the new D1 module, its narrow workbench hook,
D1 unit/regression tests and D1 Conductor records. The independent verifier
owned the separate literal oracle, scorer, tests and execution history. Two
other agents reviewed source semantics and reuse/provenance/resource limits
without editing production. These are agent engineering reviews; their errors
may be correlated, and they are not clinical reviewer or patient evidence.

## Implemented behavior and reuse

`tools.faw08_d1_extraction.extract_case(object)` now admits bounded synthetic
sources and emits atomic date, clock, range, quantity, relative-time and symptom
mention observations. It preserves invalid calendars, locale ambiguity,
missing years, unsupported number/unit forms, OCR corruption, uncertain scope
and unsupported attribution as explicit fields rather than filling gaps.

Every observation and its clause context has a verified, exact UTF-8 byte span,
case/source/version binding and raw-source SHA-256. Full-source D0 admission
witnesses are checked first and excluded from extraction counts. Nonempty
administrative text may therefore be admitted with zero observations. That
result does not establish absence of an incident or omitted care.

Relative time resolves only against an explicitly selected, verified local
date-time in the same source version. A T-separated date-time also retains its
separate date and clock mentions. Crossing-midnight clock ranges remain
ambiguous without a date. Decimal quantities preserve their scale as strings;
there is no float rounding, unit conversion or dose inference. Malformed signs,
comma-number suffixes and unsupported denominators cannot donate an apparently
valid scalar. Unsupported compound symptoms, such as `pain-free` or
`pain medication`, retain lexical mentions with uncertain polarity.

Source and anchor counts are bounded at 32, source text at 65,536 UTF-8 bytes,
and retained observations at 32 per case. Overflow fails explicitly instead
of returning a prefix. Relative integers have six digits at most; calendar
overflow produces a retained invalid observation. Case/source ordering cannot
choose a preferred account. Recording time, availability time, timezone and
event linkage remain null.

The implementation reuses the public D0 `inspect_case` boundary, existing
canonical evidence and checked JSON-shape helpers, Python `re`, calendar and
decimal types, and the existing pytest/Hypothesis environment. **No dependency,
lock, schema, quality allowance or workflow is added or changed.** The producer
does not contain expected labels. The independent lane owns semantic scoring;
`verify_extraction` is explicitly a deterministic replay-consistency check.

Run the fixed, synthetic demonstration with:

```sh
uv run --no-sync python -m tools.workbench d1-demo
```

The direct `python -m tools.faw08_d1_extraction` entry point emits the same
canonical UTF-8 JSON plus one LF. It accepts no input path, URL or model.
Receipts contain inspectable inputs/outputs, schema/rule/generator/view
versions, actual lock/implementation hashes and input/output fingerprints.
Argument, read and write failures remain nonzero.

## Independent oracle and retained failures

The verifier froze **28 synthetic development cases across 14 families** before
reading or executing the producer. All twelve required families have positive
and adverse variants. The oracle contains 54 literal observations: 37 lexically
resolved and 17 deliberately unresolved, plus two no-observation cases. Its
SHA-256 remains
`263143abe0c71bc02d7b04bd9593af3946f00c2ab64970786c922a005627aafe`.
Neither producer outputs nor its fixture generator supplied expected labels.

See the [independent verification receipt](../../../tests/fixtures/faw08_independent/verification-receipt.json),
[scoring definition](../../../tests/fixtures/faw08_independent/README.md),
[CLI execution record](../../../tests/fixtures/faw08_independent/cli-execution-20261116.json)
and [complete CLI artifact](../../../tests/fixtures/faw08_independent/d1-demo-receipt-20261116.json).
Those records bind their observations to exact source, lock, oracle and test
hashes. The current source requires its own receipt; earlier successful
development artifacts remain archived when code bytes change.

At the final source hash, three clean CLI processes produced the same
44,074-byte artifact (14 cases, 30 observations), including one LF; its SHA-256
is `19e4a8d28e62841fc15b31bd947f720b6016f35cf7030b51ead63c79147018a1`.
One independent Linux process measured 0.164604 seconds wall time and 25,148 KiB
peak child RSS. These single observations are not a latency distribution,
memory guarantee or clinical-workload measurement.

The finite oracle result is 54 exact source/span/kind true positives, zero
false positives, zero false negatives and zero field errors. All 37 expected
lexical normalizations and all 17 unresolved interpretations are correct.
Normalization recall is 37/37; useful resolved coverage is 37/54 (68.5%).
Correct uncertainty does not inflate that numerator. The two no-observation
controls have no false positives; false blocking and execution failures are
zero. Missing outputs, failed executions, duplicates and all-abstention remain
in the scorer's denominators, with undefined ratios represented as null.

These are visible development fixtures, not held-out performance or a clinical
error-rate estimate. A lexically resolved mention is not clinical truth,
decision-time entitlement or an assembled event.

Failure history is retained rather than rewritten:

- Root tests initially failed at import because the producer did not yet exist.
- The first producer run had one failure and 26 passes: a broad OCR number
  pattern misread a word as a quantity. A numeric witness guard fixed it.
- The verifier's first run had six failures and 131 passes while source bytes
  changed; its raw output and before/after hashes identify it as development
  history. A later stable evaluation had three field errors across two
  observations: an ambiguity reason and compound-negation scope. Source
  repairs resolved them without changing oracle labels.
- The unchanged Bandit gate rejected seven internal assertion statements.
  Explicit checked failures replaced them; no suppression or allowance was
  introduced.
- Reviewer counterexamples produced three initial semantic regression failures
  and 19 failures in a separate 20-case adversarial set. Repairs covered T-form
  token boundaries, later actors, postposed conditions, malformed signs and
  denominators, OCR case variants and comma relative expressions. A quadratic
  negation pattern was replaced with bounded cue matching and a linear marker
  scan.
- A final three-case probe rejected falsely affirmed compound assertions.
  The new guard preserves the mention and marks its unsupported context
  uncertain. The preceding successful source receipt is archived, rather than
  relabelled as evidence for the repaired bytes.

## Source review and engineering verification

The final production module SHA-256 is
`e03eeaa2ab5d235bdc8f20048c3bd9d15c7369a324f4575d865a7d893551e119`;
the workbench SHA-256 is
`79c40c57e75d6c3fe2fb39f6d50d6a4a40616ff561d87e45d1c4748dab1aed92`.
The contract remains
`402d01b52aaccbf5a0181aec1cc30d815f8c3386652cc4fc982e5b666741efb0`.

The focused root/independent suite has **195 passing tests**: 55 unit/regression
cases and 140 independent cases, including bounded generated Unicode/calendar
examples, hostile source/anchor admission, every observation-field replay
mutation and real subprocess receipts. Supplemental reviewer probes are
reported separately from the 28-case oracle rather than pooled into accuracy.

The semantic reviewer accepted all 27 targeted checks at the final source
hash. The reuse/resource reviewer independently checked source/anchor/replay
boundaries, malformed lexical forms, large inputs and real receipt hashes;
the final disposition and counts are retained in the
[review record](./faw08-d1-review-20261116.json). All three agents accepted the
final source bytes. The resource review passed 33 lexical probes, nine large
input probes, 12 source/case/anchor corruptions and six replay corruptions,
with three matching CLI processes and two rejected input-file arguments.

The strict engineering gate remains unchanged: Ruff lint/format, ty, strict
basedpyright with zero baseline/allowances, Bandit, Vulture, governance,
benchmarks, branch coverage, mutation and profiling. The final local full-gate
[observation](./faw08-d1-local-engineering-20261116.json) is **not a pass**:
all pre-pytest gates passed, then pytest reported **2,508 passed, 52 failed and
11 skipped**, with **93.35% branch coverage**. The failures are the existing
Unix-socket/session groups; direct AF_UNIX socket creation also raises
`PermissionError: [Errno 1] Operation not permitted`. No test was removed,
skipped or weakened. The unchanged full hosted matrix is required before merge.
Repository governance was checked again after adding the final source/review
records.

The [pinned official conformance receipt](./faw08-d1-conformance-20261116.json)
records a successful project profile and official validator revision
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`, with live upstream drift confined
to paths outside the monitored specification, validator and guidance.
Conformance PR path filters remain unchanged; the automatic master run is
inspected after source merge when no PR conformance run is triggered.

## Delivery, remaining stages and rollback

Before acceptance, verify all nine exact-head Quality jobs, dependency review
and privacy/secrets, recheck the current base and active branch rules, and merge
normally with the expected-head guard. Queued offline security is not a
completed scan. Record actual check and merge identities in the acceptance
receipt; no pending run is promoted to success.

D1 contributes to CAW02/04/08 without completing those scientific work packages
or Checkpoint B. D2 timeline/partial-order assembly is next; D3 recipient and
decision-time packets, D4 NLP/model comparisons and subsequent stages remain
planned. No model run, private data, clinical qualification, publication or
deployment is introduced by this increment.

Rollback is a normal revert of the D1 source increment. Preserve D0's original
oracle, negative observations and source/lock-bound receipts, previous studies
and other owners' work. A newly generated D0 artifact legitimately binds the
current workbench and lock; it need not equal the old whole-artifact hash.

## Subsequent observed acceptance

PR #148 merged as `33ab6d20f294fd86de2b39659aea53b0941e80e9` after all nine
exact source-head Quality jobs, dependency review and privacy/secrets succeeded.
Automatic master conformance run 43883158837 then passed, including 2,571
contract tests. See the [acceptance receipt](./faw08-d1-acceptance-20261117.md)
for actual check and merge identities. The local socket failures and earlier
failed development observations above remain preserved.
