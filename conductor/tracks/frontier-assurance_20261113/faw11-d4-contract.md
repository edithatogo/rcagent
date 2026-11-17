# FAW11 / D4: matched comparator boundary — pending qualification

## Prerequisite and ownership

Track 13's FAW11 / D4 follows **accepted** FAW10 / D3. The predecessor
[source PR #155](https://github.com/edithatogo/rcagent/pull/155) merged as
`54c67551db712e1e9f8812156d574cad060501e6`, followed by successful master
conformance and the separately protected [Conductor acceptance PR #157](https://github.com/edithatogo/rcagent/pull/157)
merged as `5c06b5c7813cb25b23df1f1a287615cf0dcaf578`.
This D4 implementation preserves its original stacked worker commits and
reconciles their changed paths onto that exact accepted master by an explicit
two-parent integration commit; the final head must pass fresh Quality,
dependency and privacy checks before normal source merge. D3 retains its
accepted source without rollback or overwrite. Checkpoint B and Track 12's
CAW04–09/21 scientific work remain open; no other shared contracts,
dependency profiles or historical negative results are edited.

The implementation is a **synthetic comparison admission/scoring slice**, with an inspectable deterministic `d4-demo` workbench receipt,
not the full D4 comparative experiment. It exposes four required arm
dispositions: regex, token/section/ConText NLP, conventional linear
classifier and structured local generation. Only the deliberately weak,
fixed regex baseline is executable here. The other three arms return
`unavailable` until independently pinned and reproducibly executed.
A supplied prediction file does not certify a model run.

## Evidence compartment and arm inputs

1. `make_view(case, root_family_id, partition)` replays full D3 admission
   in a privileged synthetic evidence compartment. That stage checks
   original source hashes and spans, actor-specific source entitlement,
   evidence-time eligibility and a second construction of the
   actor/cutoff-scoped chronology. It never returns the raw D3 case.
2. The D4 model input includes only D3-visible event identifier, exact
   evidence text, source/version/digest and half-open UTF-8 byte span,
   plus actor, cutoff, case, root family, partition and D3 view hash.
   It **does not contain** D3 event-kind/speaker labels, raw source
   contents, unentitled event identifiers or reference labels.
3. `regex_predictions(case, view)` replays the original D3 case and
   compares the exact canonical view before executing the lexical
   baseline. A forged or stale view is rejected. Its fixed regex
   predictions are a weak **software reference arm**, never a
   semantic-accuracy or clinical claim.
4. `compare_arms(study, references, arms)` reconstructs every
   view from original synthetic cases in the evaluation compartment.
   All test events must have exactly one independently declared
   synthetic reference label and exactly one prediction per **executed**
   arm; abstentions are explicit `null`. Incorrect/absent/future
   event references, cross-view predictions, stale hashes, duplicate
   records, overlapping root families across splits and ambiguous
   method statuses are rejected without echoing source-specific
   exception text. A repeated source case may not masquerade as
   an independent family under a different root ID.
5. Test event denominators, number of independent root families,
   complete-population accuracy, conditional accuracy, macro-F1
   across all four fixed labels and abstention/coverage are
   kept separate. Unavailable arms are **not** counted as scored
   abstentions or given fictitious zero performance. The scorer
   never trains a model, accesses a global source index, decrypts
   records or executes a generator.

## Qualifying a real D4 comparison (not performed here)

- **Predeclare task and estimand.** Current harness demonstrates
  event-kind labels only. CS01 assertion/provider attribution,
  CS02 evidence support and CS03 chronology require their own
  independently annotated, versioned task references; a D3
  caller-declared event label is not a clinical gold standard.
- **Freeze data.** Enumerate case/episode/semantic-template root families,
  duplicate variants, source rights and independent reference provenance;
  allocate train, development/calibration and sealed test *by family*.
  No test-dependent rule revisions or prompt tuning; changes to
  frozen test labels invalidate a confirmatory comparison.
- **Admit the methods.** Reuse maintained spaCy/medspaCy ConText and
  section components, scikit-learn TF-IDF with regularised linear
  baselines and the existing pinned offline model/runner harness.
  Record exact versions, licences, frozen models/tokenizers, hardware
  and fitted training-only vocabulary and parameters. Do not add
  optional frameworks to the portable core or infer availability
  from package names.
- **Match inputs and budgets.** All arms receive an identical D3
  recipient/cutoff scope, source revision, permitted evidence,
  schema/output label set, family split and comparable annotation
  access; report rule-development hours, labelled exposure,
  prompt demonstrations, training and inference resource use
  (including failures, retrieval and retries). Structured output
  validity does not prove factual validity.
- **Independent results.** Produce committed/retained hash-bound
  method receipts, predictions, invalid outputs and missingness
  with actual execution proof. Score by root family, error
  severity, patient/family-voice omissions, decision-time
  leakage, useful coverage and resource burden. Analyse matched
  within-family differences and uncertainty. Report negative
  comparisons without replacing baselines after unblinding.
- **Gates.** Require all Quality matrix jobs (Linux 3.11/3.15,
  macOS, Windows, coverage, real mutation, profiling and
  aggregate), dependency review, privacy/secrets and applicable
  conformance. Do not waive strict typing, use new untyped
  allowances, bypass branch protection, classify queued jobs
  as passed or manufacture external/model execution receipts.
  A protected exact-head merge and a separate Conductor
  acceptance record are required for source delivery.

## Current acceptance status

**Pending complete hosted source acceptance; empirical comparison incomplete.** Only the synthetic D3-to-D4 input
projector, regex reference arm, four-method explicit disposition
contract, fail-closed scorer and negative/metamorphic tests are
being delivered in this draft. The synthetic demo's labels are
author-declared, not independently adjudicated observations.
The other three methods, a frozen independent case-family
split, measured resources, external model execution, held-out
performance estimates and three-role acceptance are missing.
The emitted schema deliberately fixes `status=incomplete_unqualified`,
`paired_comparison_admissible=false`,
`model_executed=false`, and both clinical and model qualification
to `none`.

To roll back, revert only the D4 source, tests and this
new contract. Preserve D0–D3, all earlier negative observations,
ongoing sibling PR ownership and the unexecuted comparison
record. No branch pruning is appropriate while this PR is open.
