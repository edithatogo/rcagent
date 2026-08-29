# Decision: Use Active NSW Incident Policy While Under Review

- **Decision ID:** `20260829-001-active-under-review-pd2020-047`
- **Status:** Proposed
- **Date raised:** 2026-08-29
- **Owner:** Repository owner
- **Track:** `nsw-health-jurisdiction-pack_20260731`
- **GitHub issue:** [#9](https://github.com/edithatogo/rcagent/issues/9)
- **Decision needed by:** Before Track 04 completion or activation of NSW incident-management rules

## Decision Needed

Decide whether the pack may activate narrowly paraphrased notification and serious-adverse-event-review mappings from `PD2020_047`. The document remains in NSW Health's Active PDS Documents and states that compliance is mandatory, while its cover status is `Review` with a review date of 14 June 2026. The track explicitly reserves use of under-review material to the owner.

## Recommendation

**Recommend: Approve bounded active-policy use with review safeguards.**

Keep `PD2020_047` visibly `under_review`, use only explicit requirements that are also supported by the current CEC incident-management page, require accountable human review, prohibit privilege inference, check every 30 days, and invalidate affected receipts on any material change. This reflects the current publishing authority without claiming that review has concluded.

## Options

| Option | Benefits | Risks and trade-offs | Reversibility | Cost and effort | Dependency impact |
|---|---|---|---|---|---|
| Approve bounded active-policy use | Provides a usable NSW mapping while preserving current PDS authority and review state | A replacement may require prompt remapping; local applicability still needs organisational confirmation | Fully reversible data-only profile | Low; automated 30-day drift queue plus human material-change review | Allows Track 04 completion; downstream profiles inherit an explicitly conditional NSW mapping |
| Keep NSW rules inactive until replacement or status change | Avoids operational use of under-review material | Track 04 cannot satisfy its NSW workflow acceptance; current mandatory publication is not represented operationally | Fully reversible | Ongoing monitoring | Blocks Track 04 completion and NSW-dependent work |
| Treat the document as simply current | Simplifies state | Conceals the source's `Review` status and violates the acceptance requirement to distinguish under-review material | Reversible but not acceptable under current safeguards | Low | Would create false completion and is not recommended |

## Evidence and Assumptions

- Official Active PDS PDF retrieved 2026-08-29; SHA-256 `206514440bf425ccb5fc0dc1743ea546f8b81d89f5007e27db4f988795d5d560`.
- PDF cover: publication 14 December 2020, review date 14 June 2026, status `Review`, and mandatory compliance statement.
- Current CEC incident-management page identifies `PD2020_047` as the policy and ims+ as the notification system.
- Assumption: publication under Active PDS means the directive remains the operative statewide source pending replacement; local implementation and legal interpretation remain outside this decision.

## Privacy, Safety, Legal, and Maintenance Impact

No private data, connector, external submission or legal interpretation is involved. Accountable NSW Health reviewers remain responsible for applicability, review-path selection, disclosure, privilege and system-of-record actions. The maintenance burden is a 30-day source check and human review of material drift.

## Safe Default if Deferred

Keep the NSW rules present as review candidates but do not complete or promote the profile. Retain the last verified source snapshot and continue no external behaviour.

## Execution Impact

- **Paused scope:** Track 04 final acceptance, completion, issue closure and archive.
- **Work continuing autonomously:** None remains inside Track 04; national and Queensland mappings, schema, tests, source registry and drift controls are complete.
- **Schedule and dependency effect:** NSW-dependent downstream work remains conditional; the generic core and Queensland profile are unaffected.
- **Wake condition:** Owner selects the recommended option or the issuing body publishes a replacement/status change.

## Response Requested

Reply `Approve bounded active-policy use` to select the recommendation, or select `Keep NSW rules inactive`.

## Owner Decision

- **Decision:** Pending
- **Conditions:** Pending
- **Date:** Pending
- **Recorded by:** Pending

## Follow-up

- [ ] Update affected specifications, plans, metadata, risks, tests and receipts
- [ ] Reconcile GitHub labels and dependencies
