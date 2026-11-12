# Local model qualification for cognitive autopsy — 8 November 2026

## Reconciled ownership — 13 November 2026

This retained planning note feeds [Track 12](../cognitive-autopsy_20261107/index.md), the canonical scientific programme, and [Track 13](../frontier-assurance_20261113/index.md), its assurance/demonstration track. L1–L4 below map into existing CAW work packages; they are not additional owners or acceptance counters. Exact model names below are unverified candidates until the current model/runtime/rights admission passes. The [canonical integration contract](../../research/cognitive-autopsy/integration-contract.md) controls cross-repository ownership if an older name or scope below differs. No new model, corpus or runtime support is created by this note.

**Status: planned follow-on.** Preserve historical Track 05–10 acceptance and the explicit *empty supported local-runtime set* in archived Track 08. This is not a claim that an investigation engine, clinical model or endpoint has been validated. Model/runtime discovery lives in [models_lang](https://github.com/edithatogo/models_lang); this repository owns the domain tasks, evidence integrity, professional judgement and escalation thresholds.

## Component-level evaluation, not a single 'RCA accuracy' number

1. Intake and rights: record jurisdiction, source authority, privacy class, permitted processing, case scope and versioned input spans. Synthetic/public-rights-cleared examples first; no private reports in GitHub, Hugging Face or remote LLM prompts.
2. Extraction: event/date/time, actor/role, action/omission, treatment, organisational condition, procedure version, contemporaneous observation and documented uncertainty. Benchmark `LiquidAI/LFM3-1.7B` and other small models against deterministic baselines; measure omissions and exact-source span attribution.
3. Decision scoring: evaluate `LiquidAI/d1-2B` and `d1-Omni-2B` only for bounded label/probability tasks (evidence sufficiency, conflict, next evidence question, relevance, safety barrier); compare against generative classification, rules and expert annotations. Native versus GGUF output support must be separately proven; score calibration/abstention and high-severity false negatives.
4. Temporal/cognitive reconstruction: distinguish what was available to the decision-maker at the relevant instant from subsequent outcomes, retrospective expert views and undocumentable mental states. Prevent hindsight leakage with timeline-censored fixtures and reversed/outcome-masked tests.
5. Causal synthesis: test causal contributors, rival hypotheses, counterfactual uncertainty, system barriers, limitations and explicitly missing evidence. Compare retrieval + larger locally hosted reasoning model vs long-context whole-record reading; do not transform a language-model explanation into a finding of culpability.
6. Multimodal: OCR/extracted text and image/audio cases run in a separate track with integrity checks; no model use where imaging or speech support is unqualified.
7. Human review: investigator verifies material facts, disagreement, uncertainty and narrative; report generation and action tracking remain human-accepted activities. Compare solo and multidisciplinary adjudication and evaluate reviewer time.

## Work packages / acceptance

- **L1** Map existing benchmark and context-pack schema; design 25–50 synthetic/public licensed cases spanning extraction, negative cases, competing chronology, contradictory accounts, hidden-outcome variants and clinical/system factors. Split by case/source, not by passage.
- **L2** Build schema-validated benchmark interface and immutable run receipts, importing pinned `models_lang` results; isolation/no-egress tests, explicit model capability profiles and abstention pathway.
- **L3** Blind expert-scored pilot against rules, smaller models, a competent local general model and non-LLM workflow; preregister sensitivity to severe omissions, span fidelity, chronology leakage, calibration and reviewer burden.
- **L4** Do not enable operational cases unless security/clinical governance approval, actual hardware inference evidence, clear human authority, audited retention and appropriately sampled prospective validation exist.

Cross-repo interfaces: `learningfromharm` may supply *permitted* public NZ HDC corpus cases (rights review and independent annotations required); `careops-incidents` owns signal/workflow integration, not the investigator's findings. No cloud model receives restricted evidence.
