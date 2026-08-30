# Remaining-work agent-panel recommendations

Base revision: `9fcfab4e37d85aa1dffc1457ca605f24c558f21b`
Review date: 2026-08-30
Data: repository plans, specifications, governance decisions and preflight
source only; no new patient/employee case processing or study execution

## Panel and instructions

| Agent role | Task | Recommendation |
| --- | --- | --- |
| portfolio_acceptance | Audit legacy scoring/analysis and safe review substitution; distinguish H8 condition from review duty | Replace review roles; seek one prospective reduced-scope protocol decision |
| portfolio_evidence | Audit root scope, admission controls, remaining work and A/B/C contingencies | Harden admission first; recommend new synthetic Option B with C fallback |
| portfolio_security | Audit privacy, source rights, human/agent claims and accountable-authority boundaries | Approve review-only substitution now; preserve H8 and seek protocol decision for study changes |

All reviewers are agents; exact model revision is not exposed in their
submissions. They examined the same repository and may share model biases.
This was qualitative engineering review, not a blind numerical scoring study;
no kappa, alpha, human agreement or independent-human review is claimed.
The coordinating agent aggregated recommendations after receiving submissions.

## Agreement, differences and disposition

The panel agreed that external-human repository reviews can be replaced now,
but evidence generation and applicable authority cannot. Acceptance/evidence
agents preferred a new reduced-scope research study. The security agent
preferred immediate review-only substitution, with any study amendment handled
separately. The disposition implements the shared review change and presents
Option B as a pending decision, not an approved execution plan.

Findings retained in the plan:

- The historical H8 human comparator and H8P agent supplement must not be
  conflated or relabelled. The historical H8 descriptions also differ between
  reference investigations and commissioned human outputs; do not resolve that
  ambiguity by inventing a new interpretation of old evidence.
- Legacy preflights rely on absence of negative prose or a nonempty CSV, not
  affirmative, revision-bound admission. The next implementation slice must
  fail closed on empty, stale, malformed and fixture-only evidence.
- The historical audit's zero eligible slots is not a fresh inventory result.
- Repeated anchor revision until kappa passes risks retrospective tuning.
  Preserve original scores and revise prospectively instead.
- Root #1 needs its own acceptance map, not closure from child issue counts.

No study result, external authority, new source right, credential, provider
execution or private-data approval is created by this review.

## Amendment review

Acceptance and security reviewers passed the planning-only change. Evidence
review identified that non-admission does not prove non-execution: H8 is now
described as unverified/unadmitted, and Option A as incomplete/unadmitted.
No historical run is claimed absent merely because its evidence is incomplete.
The baseline full gate passed 473 tests with 92.35% coverage; repository
governance and diff checks also passed on the planning changes. Hosted
integration must be observed separately.

## Subsequent owner disposition

On 2026-08-30 the owner approved prospective Option B with Option C fallback
and reaffirmed agent review without repeated routine approvals. The pending
recommendation above is historical; current execution authority is recorded in
decision 20260830-002. Implementation, admission and actual study results are
not claimed by that approval.
