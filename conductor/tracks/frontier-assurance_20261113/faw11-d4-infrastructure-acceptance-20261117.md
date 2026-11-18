# FAW11 / D4 — bounded comparison infrastructure acceptance

**The D4 source software is accepted, but the four-arm FAW11 scientific comparison is not completed or qualified.** [PR #156](https://github.com/edithatogo/rcagent/pull/156) preserved the original stacked implementation commits and reconciled them against accepted D3 and its Conductor acceptance. It passed all nine exact-head Quality jobs, dependency review, privacy/secrets and Codecov patch, then merged normally through branch protection.

| Verification | Observed result |
| --- | --- |
| Source PR / exact head | [#156](https://github.com/edithatogo/rcagent/pull/156) / `30cfd8a6cdfb3a793addb230d802564e535416d8` |
| Normal protected merge | `e420392480c2f26084aab2b456912df9c24f17a8` |
| Tested and merged Git tree | `f8d235a6e3ee3355cf3098dec02286f7d9f04243` (identical) |
| Source-hosted Quality | [44093541216](https://github.com/edithatogo/rcagent/actions/runs/44093541216) — all nine jobs successful |
| Dependency review | [44093540978](https://github.com/edithatogo/rcagent/actions/runs/44093540978) — success |
| Privacy/secrets | [44093541141](https://github.com/edithatogo/rcagent/actions/runs/44093541141) — success |
| Codecov patch | completed/success after negative-path coverage repairs |
| Linux Python 3.15.2 | **3,304 passing tests**; **94.72% branch coverage** |
| D4 comparator module coverage | **99%** reported in hosted suite |
| Master skill conformance | [44094558046](https://github.com/edithatogo/rcagent/actions/runs/44094558046) — success |
| Master Quality | [44094557952](https://github.com/edithatogo/rcagent/actions/runs/44094557952) — success |
| Master privacy | [44094557938](https://github.com/edithatogo/rcagent/actions/runs/44094557938) — success |
| Offline AI security | Queued; **not a completed scan** |

## Delivered bounded contract

The D4 input projection replays the D3 source-version, recipient and cutoff boundary. It withholds reference labels from arm-facing input; detects same-source cross-split leakage, invalid or duplicated predictions and reference labels, rejects unverified resource assertions, and reports complete-denominator accuracy, abstention, coverage and macro-F1. `uv run --no-sync python -m tools.workbench d4-demo` emits an inspectable deterministic synthetic receipt.

**Only the fixed regex comparator has an execution in this increment.** ConText/section NLP, conventional linear classification and structured local generation remain `unavailable`, without pinned execution, cost or empirical performance. All claims remain `incomplete_unqualified`, `paired_comparison_admissible=false`, `model_executed=false` and without clinical/model validation. This is **not** an assertion that the full FAW11 / D4 work package is finished.

The initial RED test commits, failed strict lint/typing, earlier Codecov patch failure and subsequent corrections remain in PR history. The source did not weaken or bypass any safety/quality gate. The shared Track 12 CAW04–09/21 programme and Checkpoint B remain open.

## Next work

FAW12 / D5 has begun separately as [draft PR #158](https://github.com/edithatogo/rcagent/pull/158). Its initial *synthetic-only* native/OCR/log representation and source-origin design reuses D3 evidence. No OCR, Docling, model or process-log engine execution is admitted by that draft. Keep D4's remaining three method arms and real labelled-source studies open, and do not mark D5 complete until separately accepted.

[Machine-readable acceptance receipt](./faw11-d4-infrastructure-acceptance-20261117.json).
