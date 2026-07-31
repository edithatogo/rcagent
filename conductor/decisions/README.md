# Decision Records

Use a decision record only when owner authority or preference is genuinely required. Routine reversible implementation belongs in the track plan.

## Naming

`YYYYMMDD-NNN-short-decision.md`

## Lifecycle

1. Copy [template.md](./template.md).
2. Link the track, task, GitHub issue, evidence, risks, and dependencies.
3. Apply the GitHub `decision-needed` label.
4. Recommend one option and explain alternatives, reversibility, safe default, and impact.
5. State the rationale and evidence, exact paused scope, continuing work, and
   required response format.
6. Continue other ready work while waiting and release the affected lane.
7. Do not repeat an unchanged request.
8. Record the owner decision, conditions, date, and evidence.
9. Remove the label and update affected specifications, plans, ADRs, tests, and receipts.

Decision records do not replace legal, clinical, privacy, security, policy, or cultural-safety review.
