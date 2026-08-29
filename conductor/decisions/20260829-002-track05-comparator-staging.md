# Decision: Stage generative model comparators after the canonical harness

- **Decision ID:** 20260829-002-track05-comparator-staging
- **Status:** Proposed
- **Date raised:** 2026-08-29
- **Owner:** Repository owner
- **Track:** benchmark-evaluation-harness_20260731
- **GitHub issue:** https://github.com/edithatogo/rcagent/issues/10
- **Decision needed by:** Before Track 05 completion

## Decision Needed

Decide whether Track 05 may complete with its validated deterministic and retrieval-contract baseline while small, medium, and larger generative model comparators move to Track 08, which owns model/runtime admission. Running those comparators now requires model and licence selection, substantial artefact acquisition, device/runtime choices, and potentially provider credentials or network egress.

## Recommendation

**Recommend: Approve staged comparator deferral**

This removes a circular sequencing problem: Track 08 depends on Track 05's benchmark contract, yet Track 05's current plan asks for model comparisons that require Track 08's governed admission work. The canonical harness, safety gates, fixtures, manifests, device measurements, legacy mapping, CI suites, and nonpublication boundary are implemented and independently reproducible. Deferral does not promote any model or create an operational threshold.

## Options

| Option | Benefits | Risks and trade-offs | Reversibility | Cost and effort | Dependency impact |
|---|---|---|---|---|---|
| Approve staged comparator deferral | Completes the benchmark contract without premature model or licence choices; unblocks Track 08 | Track 05 has no generative quality results and must say so prominently | Fully reversible by adding exact-revision receipts later | No new download, credential, service, or compute commitment | Unblocks Track 08; comparator evidence returns through its model-admission receipts |
| Approve bounded local comparator acquisition now | Produces early small/medium/larger observations | Requires separate model selections, licence/rights review, large downloads, runtime support, and device time; may duplicate Track 08 | Artefacts can be removed, but time and bandwidth are spent | Material local storage, bandwidth, and compute | Delays Track 05 and duplicates Track 08 |
| Keep Track 05 blocked | Preserves the literal original plan without scope adjustment | Leaves a circular dependency and blocks downstream model work | Fully reversible | No immediate cost | Track 08 remains blocked by Track 05 |

## Evidence and Assumptions

- `evaluation/benchmark/registry.json` records unadmitted framework candidates and the deterministic suite.
- `evaluation/benchmark/results/deterministic-v1.json` records a five-case local baseline with no model or network use.
- Track 08 metadata declares Track 05 as a hard dependency and owns local runtime/model admission.
- Assumption: model comparisons remain research evidence and will not become public or operational claims without their existing owner gates.

## Privacy, Safety, Legal, and Maintenance Impact

The recommendation is fail-closed: it acquires no model, uses no private data, accepts no licence, creates no egress, and makes no comparative claim. Track 08 must still verify exact model revisions, licences, remote code, telemetry, device support, calibration, and safety before any support statement.

## Safe Default if Deferred

Keep Track 05 blocked, retain only the deterministic internal baseline, and do not start generative comparator runs or claim model suitability.

## Execution Impact

- **Paused scope:** Track 05 Phase 5 generative comparators, repeated-run model variance, human agreement, and promotion-threshold calibration; final completion.
- **Work continuing autonomously:** Final deterministic review, validation, drift automation, legacy mapping, and evidence reconciliation.
- **Schedule and dependency effect:** Without approval, Track 08 cannot start because Track 05 remains incomplete.
- **Wake condition:** Explicit owner response approving one option.

## Response Requested

Respond exactly: `Approve staged comparator deferral`.

## Owner Decision

- **Decision:** Pending
- **Conditions:** Pending
- **Date:** Pending
- **Recorded by:** Pending

## Follow-up

- [ ] Update affected specifications, plans, metadata, risks, ADRs, tests, and receipts
- [ ] Reconcile GitHub labels and dependencies
