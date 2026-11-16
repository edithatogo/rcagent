# FAW07 / D0 completion and integration record

This document retains the **premerge source observation**. The later
[observed acceptance receipt](./faw07-d0-acceptance-20261116.md) records the actual
protected merge and hosted/master-conformance results; pending statements below
describe the original source-verification time.

## Bounded authority and source reconciliation

On 16 November 2026 Dylan instructed this conversation: **"Implement D0, open a
PR, check actions pass, then merge."** This is direct authority to complete and
integrate this D0 increment. It supersedes the earlier planning-only and
coordinator-only merge restriction for this specific assignment; it does not
transfer other rcagent tracks or expand D0 into D1–D3, model or clinical work.

Before editing production, the completion owner reconciled:

- Master `c6892497aa0b03555d5145242c04965471eccc1d`.
- Existing implementation PR #132, branch
  `feat/faw07-d0-demo-receipt-20261114`, head
  `4746027c7de6cd4e0ed1518241f847146d79faef`.
- Existing independent-verification PR #133, branch
  `test/faw07-d0-independent-verification-20261114`, head
  `4057512f23a2301d6ffe4649e42fb055eeb83937`.
- The published `faw07-d0-contract-1.0`, prior coordinator reviews and unchanged
  independent oracle. Prior worker acknowledgement remains unobserved; it is
  not inferred from this new owner instruction.

Both worker heads are incorporated into the isolated
`feat/faw07-d0-completion-20261116` integration branch. Their original branches
remain unchanged. This completion assignment owns repairs in the existing D0
module/unit tests, the narrow workbench D0 hook, the existing verifier adapter
and supplemental verification records, plus D0 Conductor reconciliation.
Read-only agent review does not create another production implementation lane.

The original oracle labels, historical provisional and failed verification
receipts, FAW06 acceptance, consumed research identities and negative results
remain preserved. AcciMap, HEAPS and the repository-review planning PR retain
their separate scopes.

## Acceptance status

Source implementation and independent verification are complete at the file
identities in the [execution observation](../../../tests/fixtures/faw07_independent/verification-execution-20261116.json).
FAW07 remains `[~]` until the contract's hosted-delivery and actual-merge gates
are observed. The integration PR records its exact committed head and Actions
results; a subsequent acceptance record must name the actual merge SHA before
marking FAW07 complete. This source receipt asserts no future check or merge.

## Implemented contract

The Python `inspect_case(object)` boundary now checks source/evidence case
binding, typed source versions, declared source and evidence digests, exact
UTF-8 byte coordinates, duplicate identities, unknown/withdrawn states and
nonempty inputs. It enforces 32 source rows, 64 evidence rows and 65,536 UTF-8
bytes for retained source text. Invalid integer bounds produce semantic
rejection; missing/wrong types, invalid digest syntax, encoding failures and
exceeded limits raise a documented `ValueError`. Every rejected case has
`spans=[]`, including mixed cases with a valid prefix.

The five generated inputs retain two accepted and three rejected examples.
Their representation is explicitly versioned as `faw07-d0-generator-2.0` after
adding the contract-required fields; the producer carries no expected labels.
Receipts contain inspectable inputs, source/input/output fingerprints,
input/rule/generator/view identifiers, the actual lock digest and hashes of the
demo, workbench and reused evidence/JSON-shape helpers. The module and workbench
share one binary UTF-8 output path ending in exactly one LF. Unsupported CLI
input and receipt read/write failures are nonzero.

Run the deterministic demonstration with:

```sh
uv run --no-sync python -m tools.workbench d0-demo
```

For these reviewed source bytes, two clean subprocesses emitted identical
6,835-byte artifacts, including the final LF, with SHA-256
`4a97ca2a6998dece2fdb6ac10ce20fdca81d722d49073771985bb0e09af62c89`.
Elapsed observations and interpreter/lock/source identities are in the execution
record. They are not performance guarantees.

## Verification and independent review

The original independent oracle, oracle self-tests, provisional receipt and
14 November observations are byte-identical to verifier head
`4057512f23a2301d6ffe4649e42fb055eeb83937`. Only the transparent production adapter
was corrected to preserve claim hashes, coordinates, case attribution, missing
values, source revisions and duplicates. It now executes all five positive,
fourteen negative and three collection definitions. Receipt checks use actual
subprocess output and standard-library calculations, not producer-derived
expected labels.

```sh
uv run --no-sync python -m pytest -q \
  tests/test_faw07_independent_oracle.py \
  tests/test_faw07_independent_d0_integration.py \
  tests/test_faw07_d0_demo.py
```

Observed: **130 passed**, including 60 bounded Hypothesis examples for Unicode
spans and source tampering. The independent-only subset has 40 passing tests.

| Agent reviewer | Independent evidence on the bound source bytes | Disposition |
|---|---|---|
| `plan_gap_review` | Contract A0–A2 review; 40 verifier tests; all 196 byte-bound pairs on a literal Unicode source; decomposed-quote and stale-digest negatives; independent receipt hashes | No blocking scoped defect; proceed to hosted/merge gates |
| `dependency_audit` | 150 separate boundary observations: 41 accepted, 86 semantic rejections, 23 malformed-input rejections; three matching subprocesses and invalid-argument checks | No blocking scoped defect; proceed to hosted/merge gates |
| `frontier_research` | 288 independent scratch checks covering the historical oracle, collections, Unicode intervals, exact limits, case/digest/bounds, atomic rejection and receipt identities; reviewed transparent adapter | A2 accepted for the reviewed file bytes; A3–A5 separate |

Reviewers are agents and may share correlated errors. Their supplementary
counts are not independent clinical cases, empirical accuracy estimates or
model qualification. The third review retained its initial 287/288 observation:
its harness incorrectly demanded exactly three implementation-file entries,
then independently verified the additional reused JSON helper. No producer
change or oracle-label change was made to obtain that correction.

## Engineering and conformance

Ruff lint/format, ty, strict basedpyright, the empty typing baseline, Bandit,
Vulture, repository governance and the seven deterministic benchmark regressions
passed. No source schema, dependency lock, CI, quality allowance or historical
study identity changed.

The complete local `tools.full_validation` command **did not pass** in this
executor: pytest reported **2,313 passed, 52 failed and 11 skipped**. The failures
are in existing Unix-socket/session groups; a direct AF_UNIX creation probe also
raises `PermissionError: [Errno 1] Operation not permitted`. No test was removed,
skipped or weakened to bypass this restriction. The complete required hosted
matrix remains necessary before merge.

The [pinned official conformance receipt](./faw07-d0-conformance-20261116.json)
records successful local validation with official validator revision
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`, complete project profile and live
upstream-drift inspection. Changes were confined to upstream paths outside the
monitored specification, validator and guidance. PR path filters are unchanged;
if the separate conformance workflow is not triggered, record that explicitly
and inspect the automatic master run after merge.

## Remaining delivery and rollback

Run every required hosted check on the exact integration head, inspect the
current-base merge conditions, merge normally with the expected-head guard, and
then record the actual merge/acceptance. Historical negative studies and later
D1–D8 tasks remain unchanged. Superseded worker PRs retain their history and
receive the integration reference after merge.

Rollback is a normal revert of the D0 integration change. This does not undo
FAW06, the earlier contract, independent negative observations or unrelated
method/profile work. D0 qualifies only the demonstrated synthetic identity and
byte-span contract; it establishes no semantic truth, clinical/model validity,
operational isolation or release.

## Subsequent observed acceptance

PR #144 was merged as `d3c10d607470c9a50c5410030b80aeab2cfa5430` after its exact source head passed every
Quality job, dependency review and privacy/secrets. Automatic master conformance
run 43857726512 passed before acceptance. See the [acceptance receipt](./faw07-d0-acceptance-20261116.md)
for actual identities and worker reconciliation. The failed local full-gate
observation and all earlier evidence above remain unchanged.
