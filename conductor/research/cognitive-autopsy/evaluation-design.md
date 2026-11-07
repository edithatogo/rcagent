# Cognitive autopsy evaluation design

## Question, estimand and claim boundary

Can an explicitly identified local model configuration produce more faithful, useful and appropriately uncertain reconstructions of documented healthcare decisions than deterministic extraction or an untuned structured baseline, without increasing patient-relevant material error?

The primary study is retrospective documentary evaluation in HDC cases. Its estimand is performance on the eligible sampled reports and decision tasks, not population clinical error, clinician cognition, preventable harm incidence or patient benefit. HDC publication and complaint selection constrain generalisation. Official findings are an important comparison source; they are neither a complete contemporaneous record nor an infallible clinical gold standard.

## Data and experimental units

Start with a 20–30-case development pilot, then plan approximately 80–120 independent held-out cases if the corpus supports them. This is a planning range, not a power calculation. Use pilot estimates of paired differences, event prevalence and within-case correlation to calculate the required precision before freezing the main cohort. Report a smaller feasibility study if the available evidence is insufficient.

Stratify by specialty/setting, decision task, report length, documentation quality, year and findings category. Include no-breach/mixed findings and defensible decisions within adverse cases where available. Include diagnosis, escalation, treatment/monitoring, communication and coordination; do not reduce the concept to diagnosis.

Group versions, linked reports, encounters, participants where identifiable within permitted data, and all derived variants before splitting. Partition at case-family level. Keep final test data, expert labels and source-bearing test retrieval out of training/development. A later temporal or different-setting holdout tests transportability. Multiple decisions and repeats are clustered observations, not extra independent patients.

## Temporal isolation

- Packet A: evidence plausibly available at the specified decision point, with source spans and uncertainty about availability.
- Packet B: subsequent events and outcomes.
- Packet C: later expert/Commissioner appraisal and recommendations.

Run A, A+B and A+B+C conditions in independent sessions. A is built by a separate offline preparation process; identifiers, headings, filenames, frontmatter, index snippets and hidden tool context are scrubbed of answer cues. Each condition gets a separate permitted retrieval view and cache namespace. Fail closed on uncertain packet separation; do not ask a model to ignore information it has already seen.

The original document remains unchanged. Reports were written retrospectively and models may have memorised public cases. Masking cannot eliminate those risks. Record residual wording cues, compare recent/less exposed cases, test title-only/identifier-only recognition with non-sensitive authorised data, and report contamination sensitivity analyses. Optional original synthetic variants can isolate outcome-label effects; keep them outside the primary HDC denominator.

Test two different behaviours: stability when only irrelevant outcome valence changes, and appropriate change when genuinely decision-relevant evidence changes. Complete invariance can be rigidity rather than good reasoning.

## Experimental arms and ablations

| Arm | Purpose |
| --- | --- |
| D0 deterministic extraction/template | Establish the value of rules, chronology and evidence links without generation |
| L0 untuned model + fixed structured prompt | Establish each candidate's baseline with schema-constrained output |
| L1 same model + local scoped retrieval | Test whether evidence access fixes errors before changing weights |
| L2 local extractor + reasoner + bounded critic | Test task routing/composition against the best single model; critic disagreement triggers review, never a vote that proves truth |
| F0/F1 conditional adapted model without/with the same retrieval | Test incremental adaptation value, if the trigger is met |

Use a development tournament, then freeze a small number of finalists and one primary contrast for the test set. Match evidence access, output schema, feasible context envelope and search budget. Report both quality at a common resource budget and the practical quality/resource frontier. Do not force incompatible models into an invalid common chat template. Test quantisation and truncation as factors; log actual tokens and failures.

Use supplied primary models, native templates and exact licences. Keep deterministic scoring separate from generative judging. Local model judges can screen disagreements and propose labels, but evaluated-model self-scoring is not independent evidence. Freeze rubric, judge instructions and submissions; retain disagreements and blinded post-submission adjudication.

## Patient-centred endpoint hierarchy

**Primary:** proportion of cases containing at least one material error in the decision reconstruction or learning output: a clinically material omission, unsupported attribution/rationale, or conclusion/recommendation that could misdirect a safety response. Preserve all three categories separately and predefine severity with examples. The denominator includes attempted eligible cases; failures and abstentions are shown explicitly, not silently removed.

**Key supporting outcomes:** coverage of source-supported critical information; supported-claim precision; documented patient/family concern recall; preservation of uncertainty and reasonable alternatives; unsupported blame or bias labels; recommendation traceability, feasibility and foreseeable burden; calibration and risk/coverage curves. An all-abstaining system cannot win on error rate alone: require prespecified minimum useful coverage and report the joint outcome.

**Equity:** examine error patterns by documented language/access needs, setting and relevant population groups where lawful, sufficiently represented and actually recorded. Do not infer ethnicity or other sensitive attributes. Small strata are descriptive with uncertainty, not fairness certification.

**Secondary:** reviewer minutes, correction burden, processing latency, failure/retry rates, peak memory, energy when measured, compute and staff cost. Compare cost per usable, adequately supported review output and present a cost-consequence table alongside material errors and concern coverage. Do not monetise hypothetical harm averted or infer QALYs from text scores.

Patient-centred framing concerns what the system gets right for patients. It does not turn retrospective text metrics into observed patient outcomes. Patient/family acceptability, learning retention and harm reduction need actual participant/follow-up observations if claimed.

## Scoring and statistical analysis

Use exact source checks for provenance and temporal leakage, plus an anchored rubric for materiality and learning. Establish an evidence hierarchy: source-verified deterministic attributes; existing expert appraisals as comparison; blinded human judgements where actually obtained; explicitly labelled agent ratings. Report performance against each reference separately.

For the documentary feasibility paper, automated/agent-assisted annotation is permissible when disclosed and its limitations are central. To make claims about clinical validity or user performance, use a bounded stratified human audit: random cases plus high-risk/disagreement cases. Maintain a separate random audit denominator, report selection probabilities, and do not estimate unbiased overall accuracy from a selected disagreement sample. Human workload can be reduced by source-linked preannotations and active learning, but not represented as zero while claiming human validation.

Report paired case-level differences and confidence intervals using case-family clustered bootstrap or an appropriate prespecified mixed model. Use paired binary analysis for case-level material error. Report agreement with an appropriate statistic and confidence intervals, not just raw agreement; separate reference reliability from model accuracy. Report number of independent case families, decisions, repeats and evaluable outputs separately.

Predeclare hierarchy/multiplicity handling, missingness, sensitivity analyses and subgroup limits. All timeouts, malformed outputs and cancellations belong in the run ledger. Keep clinical-quality and latency comparisons interpretable when output lengths differ.

## Fine-tuning decision rule

First identify a repeated error that better retrieval, prompts, constraints or context allocation have not resolved. Good targets include source-backed structured extraction, assertion/availability classification and calibrated abstention. Do not train a model to imitate unverified blame labels or free-form invented thought processes.

Before training, freeze the base revision, authorised training material, grouped splits, maximum experiment budget, primary contrast, minimum useful gain, non-inferiority margins, useful coverage and stopping rule. Numerical margins must be chosen from pilot evidence and the intended task before test unblinding; they are not asserted to be validated thresholds in this plan.

Adopt only if the adapted model beats the strongest untuned comparator by the prespecified paired material-error/quality criterion, while meeting all safety and privacy hard gates, the coverage requirement, and prespecified non-inferiority for critical source recall, unsupported attribution, equity and out-of-domain performance. Account for uncertainty, training cost, maintenance and latency. An inconclusive result retains the untuned version. Do not transfer synthetic v1 thresholds to HDC.

Use PEFT/LoRA first; any preference optimisation or distillation is later, separately justified. Teacher-generated labels carry provenance and require audit; they are not ground truth. Evaluate memorisation, canary extraction and membership risk before sharing weights, since locally trained weights can encode sensitive text.

## Promotion and contingencies

A passed component receipt applies only to its declared context. Test the composed system for error propagation and correlated failures before a whole-RCA research claim. Actual workflow evaluation and organisational deployment are later evidence levels.

If judges disagree, improve the rubric on development data, retain original scores, and rerun a versioned blinded comparison. If all models fail, preserve the negative study and deterministic tools. If corpus coverage is limited, publish bounded feasibility rather than fabricate power. If fine-tuning fails, the study still completes. The research programme is designed to produce an informative result under each outcome.
