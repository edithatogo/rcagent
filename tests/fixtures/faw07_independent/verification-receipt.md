# FAW07 / D0 independent synthetic verification — provisional receipt

## Scope and ownership

Independent verifier only. Owned files:
- `tests/fixtures/faw07_independent/d0_oracle.json`
- `tests/test_faw07_independent_oracle.py`
- `tests/fixtures/faw07_independent/verification-receipt.md`

No production code, production unit tests, shared schemas, Conductor registries, baseline/caps, CI definitions or historical studies are changed. The integration coordinator owns acceptance and merge. Separate implementation branch: `feat/faw07-d0-demo-receipt-20261114`.

## Revision and evidence status

- Starting master: `419c04d7e1c0a16e924e0b7058604671855625a2`; source tree `c0ff3fa9ce5cc78232d3987431ff857c43d1aa68`.
- Implementation target SHA: **not yet available**. At initial inspection the implementation branch was identical to master.
- Scope: independent synthetic byte-integrity oracle and adversarial matrix; not yet an execution of the production D0 demonstration command.
- No network, models, AGY credits, private patient cases or D1–D8 capabilities are required.
- Qualification: **unverified against implementation**. Do not claim D0 acceptance on this receipt.

## Predeclared synthetic acceptance matrix

The fixture catalogue has five accept and fourteen reject examples, plus three source-collection integrity checks. Every source has a committed literal UTF-8 payload and a precomputed SHA-256 digest; spans are half-open **UTF-8 byte** coordinates. Cases include:

| Family | Acceptance assertion |
| --- | --- |
| Exact source span, repeat run | Identical source-linked content is accepted consistently |
| Versioned revision | Revision 1 and 2 retain distinct digests and values |
| Unicode | Multibyte `café` is resolved with byte rather than character offsets |
| Other valid case | Correctly bound independent-case evidence is accepted |
| Forged or stale digest | Content and revision substitution are rejected |
| Cross-case / unknown ID / unknown revision | No fallback to a similarly named source |
| Negative, reversed, out-of-bounds and broken UTF-8 spans | Rejection without fabricated extracted text |
| Wrong span content and coordinate system | Exact bytes and declared coordinate semantics required |
| Withdrawn source | Previously known but inadmissible provenance is not silently accepted |
| Missing hash and incorrectly typed offset | Malformed input returns a failure, not implicit success |
| Duplicate ID/version | Duplicate registration rejected; genuine distinct revisions accepted |

Independent fixture tests evaluate this oracle, source order invariance, repeated evaluation and source-byte tampering. These tests do **not** call the production CLI and must not be represented as product conformance. The 5/14 count is an oracle denominator, not empirical precision, recall or clinical performance.

## Integration acceptance requirements not yet observed

1. Pin the implementation **full commit SHA**, CLI invocation, exact input/receipt schema, dependency lock digest, source bytes and configuration.
2. Run the production D0 command twice from a clean checkout using the same synthetic inputs. Compare canonical semantic receipt fields and outputs; ignore explicitly documented volatile measurements only, not digest, status or provenance fields.
3. Independently verify every emitted source hash and byte span against original fixture bytes, including revisions. Re-run with reordered input, changed irrelevant ordering and a modified source byte.
4. Confirm fail-closed error status and nonzero exit (or a clearly documented typed rejection result) for each malformed/adversarial case. Do not assume an exit-zero status means admitted evidence.
5. Inspect receipt for input/source hashes, source version, command, schema/extractor version, runtime/dependency lock, expected/actual output, error totals, limitations and resource measurements.
6. Preserve all existing gates: locked installation, Ruff/format, ty, strict basedpyright with empty allowances, Bandit, Vulture, property checks, full pytest and coverage matrix, mutation/profiling, dependency/privacy/secrets and conformance. Hosted checks must be read at the **final head**.
7. Record failures, unsupported paths and skipped runs in the denominator; leave historical negative evidence unchanged. No clinical or model capability claim follows from D0.

## Reproduction

Run oracle-only tests with:

```sh
uv sync --locked --extra validate --extra test --extra lint --extra assurance
uv run --no-sync python -m pytest -q tests/test_faw07_independent_oracle.py
uv run --no-sync python -m tools.full_validation
```

The second command is an independent finite-oracle integrity check only. Production-command acceptance is **pending**, and its SHA must be recorded before running it. Integration and merges are reserved for the coordinator.

## Results

- Initial source review: performed on the master SHA above, issue #125, Track 13 plan/spec and the capability-ladder and admission contracts.
- Oracle fixture/test commit: `419887b52d8a5e71f0c5d0befc0b41fe62407155` (pre-receipt branch head).
- Local/hosted fixture-test execution: **not yet observed** at receipt authoring.
- Production D0 execution: **not performed**.
- Independent acceptance judgement: **withheld** until production SHA and observed runs are available.

This file is a historical provisional evidence record; append a new final-head verification record rather than rewriting a failure or asserting future CI results.
