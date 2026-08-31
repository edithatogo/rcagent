# Historical case readiness reconciliation

## Scope and method

Read-only inventory base: `35d1fdfb3d103e418317e97db57fb951dd08779d`.
Observed on 2026-08-31; count/hash check at `2026-08-31T09:49:30Z`.
This bounded agent audit inspected the case-collection specification/plan,
dataset index, metadata and section structure. It counted whitespace-delimited
words between `## Case Narrative` and the next H2 using `awk`, and hashed the
seven existing case files using `shasum -a 256`. It did not fetch sources,
verify narrative accuracy, perform clinical scoring, assess individual privacy,
inspect historical raw execution bodies or run a model.

The accompanying change qualifies current documentation only. Historical case
bytes, ratings, findings, protocol identity and execution records are unchanged.
This is not a fresh Phase 4 admission inventory or a positive study receipt.

## Observations and unresolved acceptance

The actual directory is `evaluation/datasets/`, not a root `datasets/`
directory. Its README and seven NZ files already exist. Each case file has a
narrative, findings section and recorded severity/difficulty metadata. Thus the
case-collection plan's blanket unstarted formatting/index tasks are stale, but
those structures do not prove source fidelity, QA or admission.

| File under `evaluation/datasets/hdc-nz/` | Narrative whitespace words | SHA-256 |
| --- | ---: | --- |
| nz-case-01.md | 920 | `957cc3bf4754c30a9f718c32bf99c8bc3aefc42760436dca425e17635e70063a` |
| nz-case-02.md | 615 | `88d5437e8a8499b25852b11fbb743cb13c0f096470bddd87949e66b0b09b87df` |
| nz-case-03.md | 749 | `f8e09567aa5ba06e6c0ef0612adf87ab30109d8955e9963d73631177b653a541` |
| nz-case-04.md | 860 | `96816184a8585414881cf7108a18d8dae1255711bc25f223e5a11a372030a9ed` |
| nz-case-05.md | 599 | `44642f3c714ff87545901ce847284c4ac57fc4d7f5c3e6fe0a8080096cb76bd4` |
| nz-case-06.md | 575 | `339cd2b68e9c57bf96fa2273a4ad83f106508f1d3c7a40a408cbaa6c0d2dca94` |
| nz-case-07.md | 646 | `ac865bad89f46bf1598eeeaf62e24bb73da4a612aedf481e3d6acf5ebfa34c11` |

These are mechanical counts, not a finding that every counted word is eligible
clinical narrative. All seven exceed 500 by that bounded method.

- AU coverage is zero against at least two required; NZ count is seven against
  at least three. Total count alone does not establish overall coverage.
- Recorded difficulty counts are simple 1, moderate 3 and complex 3; the first
  two are below the specified targets of 2–3 and 4–5.
- Recorded severity counts are SAC 1: 3 and SAC 2: 4. These are historical
  classifications, not newly validated clinical judgements.
- The index's `Falls / patient safety` and `Surgical/procedural / perinatal`
  rows broaden the specified event types. Case 05 is labelled `fall` in metadata
  but patient-safety in the index; case 04 is labelled `surgical` in metadata
  but perinatal/neonatal in the index. Their eligibility is unresolved, not a
  verified pass. Do not change clinical classifications merely to fill quotas.
- Per-artefact source terms, source parity, privacy/QA and applicable authority
  were not established by this audit. Public availability is not rights or
  anonymity evidence. The retained cases are not synthetic.

## Review and authority

[Decision 001](../../decisions/20260830-001-legacy-agent-review.md) and the
workflow already replace independent human repository reviewers with agent
panels. No reviewer recruitment or repeat approval is needed for this repair.
Product-guideline human authority language concerns operational decisions; it
does not reinstate a human engineering-review requirement. H8 remains a genuine
historical human-comparator condition, separate from H8P and agent review.

[Decision 002](../../decisions/20260830-002-prospective-agent-study.md) permits
the separate synthetic B/C route, not relabelling these cases or historical
results. The [consumed-cohort readiness addendum](./readiness-addendum-20260831.md)
does not close historical case collection or Phase 4. The dated
[historical manifest audit](../../../evaluation/analysis/phase4-manifest-audit-receipt.md)
is retained as an earlier snapshot, not freshly verified here.

## Smallest useful next steps

1. Qualify the current dataset and selection documentation, retaining historical
   files and explicitly withdrawing unsupported ethics/privacy/rights
   assurances. This is the local repair accompanying this receipt.
2. Reconcile case-collection task state against the structural evidence above,
   keeping QA, source admission and incomplete coverage visibly unresolved.
3. If a historical study is pursued, first establish per-artefact permissible
   actions and missing provenance. A panel may audit evidence, not invent
   authorisations, raw observations or retrospective operator attestations.
4. Do not acquire more real cases merely to satisfy counts, reuse historical
   material in the synthetic study, retry the consumed prospective run, or
   declare root completion. Continue independently ready repository work and
   consolidate only genuinely new reserved decisions.

Validation and final three-role panel disposition belong to the integrating
change. Rollback affects only these documentation qualifications and this
receipt; it does not remove or alter historical evidence.
