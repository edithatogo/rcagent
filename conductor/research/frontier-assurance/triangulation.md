# Triangulation across methods, models, modalities and evidence

Status: planned experimental capability. This contract extends Track 12's conventional NLP, verification and process studies; it does not qualify an ensemble or a multimodal model.

## What counts as corroboration

Record four separate axes: (1) source origin, (2) extraction/analysis method, (3) model family/training/runtime, and (4) modality/representation. Two models reading one copied note are two analyses of one source, not two independent witnesses. Native PDF text and OCR of that PDF can expose extraction error but cannot independently establish that its account is true. A medication administration record and a narrative may also share an upstream entry; preserve that origin relation.

Every candidate assertion carries its source-family ID, transformation chain, input/view hash and method/model revision. The comparison service groups candidates referring to the same event and records agreement, contradiction, additional information and unresolved absence. It must not average incompatible times or replace conflicting accounts with a synthetic consensus.

## Programmatic first layer

| Technique | Appropriate bounded use | Principal failure to test |
| --- | --- | --- |
| Regular expressions and finite dictionaries | Explicit date/time/unit/identifier patterns, headings, known structured fields | Locale ambiguity, malformed values, overmatching, catastrophic regex work, OCR substitutions |
| Calendar/unit/identity constraints | Validate parsed values, intervals, patient/case identity and arithmetic | A plausible value can still be attributed to the wrong event, source or patient |
| spaCy token/phrase/dependency rules | Context-sensitive event/action/actor extraction and phrase matching | Model/tokeniser changes, abbreviations, passive voice and incorrect dependencies |
| medspaCy/ConText-style rules | Negation, uncertainty, experiencer and section context | Scope errors, copied history, conditional plans, double negation and domain transfer |
| Classical supervised NLP | Task-specific TF-IDF/linear/sequence-label baseline | Rare categories, source leakage, poor calibration and dependence on labelled resources |
| Compact encoders/NLI | Bounded categorisation or candidate semantic support | Hypothesis-only shortcuts, domain mismatch and false entailment |
| Structured local LLM | Extract difficult relations and propose explicitly qualified hypotheses | Invented events/rationale, invalid attribution, future-information leakage and plausible unsupported prose |

Use maintained implementations through thin adapters. Pin rule/model/tokeniser/section dictionaries and record normalisation-to-original offsets. Regex and arithmetic may reject a candidate but cannot prove clinical meaning. No user-supplied pattern or parser configuration may escape input/time/memory budgets. spaCy documents the distinct roles of token rules, linguistic annotations and statistical models; those capabilities do not establish accuracy for this domain [T1].

## Use during development

Run alternative extractors on generated fixtures and authorised labelled development data. Store disagreements as candidate error cases; inspect their source spans. Generate adversarial cases with known, separately held oracles. Use model suggestions for case discovery only after confirming their ground truth. Keep case-family, template/rendering and source versions in the same split; a model that generated test answers cannot be the sole judge of those answers.

Ablate one factor at a time: rules alone; NLP alone; model alone; rules plus NLP; model plus deterministic verification; same-model critic; different-family critic; and selective cascade. Match total token/tool/compute budgets where comparing efficiency. Also publish unconstrained quality/cost curves when that is the scientific question. Different vendors or parameter counts do not automatically imply independent errors.

## Use during verification

Deterministic byte/span/entity/time/privacy failures are hard constraints. A model vote cannot override them. Semantic verifiers see the source, the claim and the same authorised view, and return supported, contradicted or insufficient with an evidence span. An additional model is useful only if it catches material errors missed by the existing verifier while preserving useful coverage.

Measure joint-error frequency, error overlap by category, conditional miss probability, false rejection, disagreement yield, calibration, selective risk/coverage, repair success and latency/cost. Estimate uncertainty by case family. Report judge identity and correlated-error limits. A majority decision is an agreement observation, not a factual or clinical adjudication. Research has shown limits of intrinsic self-correction without external feedback; treat this as a motivation to test independent evidence checks, not as proof that every current critic fails [T2].

## Use in an investigation workflow

Present candidate timeline rows with linked passages, explicit uncertainty and the reason for a discrepancy. Ask focused evidence questions only when they could change a material interpretation. Route unresolved items for accountable review; retain the original alternatives and correction provenance. Do not silently broaden data access, call a cloud model, or convert a disagreement into a finding about culpability.

Use a small deterministic/NLP pass for all cases. Escalate only predeclared hard cases to an admitted local model or second model. If the expensive arm does not improve the frozen primary contrast, retain the simpler path. Never suppress an unmeasured severe failure because average agreement is high.

## Multimodal sequence

1. Native document text versus rendered page layout and OCR: assess reading order, tables, footnotes, units, omitted pages and source coordinates.
2. Narrative versus structured orders, observations, medication administration, device or audit events: assess clock alignment, data provenance, missingness and common upstream origin.
3. Audio/transcript alignment where authorised: assess word/number/negation fidelity, diarisation and uncertain speaker identity; retain timecode links and avoid voice-identification claims.
4. Imaging/DICOM and physiologic signals: begin with metadata, data fidelity and already documented clinical interpretations. New diagnostic interpretation remains separately qualified and authorised.

For each added modality, test whether it contributes new evidence or merely restates the same source. Missing modality, image prompt injection, table/unit misalignment, speech recognition errors, contradictory measurements and metadata identifiers are explicit challenges. A text-only fallback remains available. An accurate modality adapter does not automatically qualify the assembled investigation.

## Reuse and sources

- T1: spaCy, Rule-based matching, primary documentation, checked 13 November 2026: https://spacy.io/usage/rule-based-matching
- T2: Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet, ICLR 2024, version 2: https://arxiv.org/abs/2310.01798v2
- T3: medspaCy primary project (candidate requiring exact-version admission): https://github.com/medspacy/medspacy
- T4: Existing [component studies](../cognitive-autopsy/component-studies.md), [controlled experiments](../cognitive-autopsy/controlled-experiments.md) and [process-mining contract](../cognitive-autopsy/process-mining.md).
