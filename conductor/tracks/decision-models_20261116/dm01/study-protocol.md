# DM01 reference study: synthetic intake completeness and escalation

This is the procedural freeze for **`dm01-synthetic-intake-v1`**, implementing DM01.3 of the
[decision-model plan](../plan.md). It specifies a bounded research study before any cases,
model responses or holdout results exist. The companion [JSON protocol](./study-protocol.json)
is the machine-readable numerical and procedural record. Neither document reports an executed study.

Procedural freeze date: **17 November 2026, Australia/Brisbane**. The established parent track ID
retains its original `20261116` date.

## 1. Authority, estimand and freeze state

The current instruction authorises DM01 context, source admission and study definition. No model
execution, case generation, participant recruitment, clinical deployment or private data access occurs
in this increment. Track 12 retains scientific ownership and Track 13 shared integration/assurance.

The estimand is **assistance quality on the frozen, deliberately balanced synthetic intake population**.
The proposed task helps patient-safety intake reviewers identify missing usable information and route
an explicitly defined synthetic severe concern to review. It does not estimate real incident prevalence,
clinical sensitivity, statutory duties, patient benefit or performance in an HHS. Its numerical margins
are research selection criteria, not clinical operating thresholds.

The [standing HDC decision](../../../decisions/20261107-001-cognitive-autopsy-programme.md) records
existing ethics authority for the established HDC corpus programme. That authority is preserved and
is not reopened. **This first study uses no HDC cases**, private incident reports or clinical records.
An HDC extension would need its own exact snapshot/task/rights/scope check under that existing record;
the approval reference remains in its protected record. No broader approval is inferred.

There are three distinct freezes:

| Freeze | State in DM01 | Required evidence before the next stage |
|---|---|---|
| P: procedural | Defined by this versioned MD/JSON pair and its Git commit/file hashes | Any substantive change creates a new protocol version with reasons; preserve prior bytes. |
| D: data/reference | Pending; zero case families created or accessed | DM04 records root-family lineage, source rights, all variants, independent reference labels, split assignments and canonical SHA-256 manifest. The holdout remains sealed from model/prompt developers. |
| M: model/analysis | Pending; no executable tuple admitted | Exact R/C/G/D/H definitions, assets, tokenizer/runtime/device, prompts, calibrators, thresholds, metric implementation and analysis hashes; no mutable alias. Freeze before the holdout is opened. |

The data freeze may be created after this procedural freeze, but its split counts, task definitions and
acceptance criteria cannot be chosen using candidate-system holdout performance. Missing hardware,
rights, independent families, references or model compatibility results in **not ready/infeasible**,
not a smaller unreported sample or a weaker margin. A later amendment is a new prospective study;
the existing holdout cannot become a fresh confirmatory test.

## 2. Bounded task and output

Each family has one canonical UTF-8 text packet: at most 8,192 raw bytes and 2,048 content tokens under
every selected tokenizer. Total prompt/state/question tokens must be at most 4,096. Both limits must
hold; over-limit inputs are repaired by the independent author before data freeze, never silently
truncated during testing. No retrieval corpus, ontology, image, audio or typed extraction is required.
Only the permitted packet is visible to each method; author/reference metadata is not model input.

The following seven questions have binary references. D returns separate native Noul `p_yes` values
in `[0,1]`; C and G return probability forecasts for the same questions, and H retains its selected
D/G forecasts. R returns binary labels or explicit unresolved states, never invented probabilities.
For D these are seven inference work units, even if a server accepts one HTTP request. All
preprocessing, calls, queueing and fallback costs belong to the full seven-question procedure.
Any batching/multiquestion optimisation requires separately admitted capability and paired output
equivalence checks; single-pass support for one primitive is not a whole-workflow single-pass claim.

| ID | Question identifier | Frozen meaning of a positive reference |
|---|---|---|
| DMQ01 | `event_description_usable` | The packet states an identifiable event/hazard, rather than only a category or empty assertion. |
| DMQ02 | `occurrence_time_usable` | A stated date/time or bounded relative interval identifies when it occurred; an explicit unknown remains unusable. |
| DMQ03 | `harm_information_usable` | Actual/potential harm is described, or explicitly reported absent; silence/unknown is unusable. |
| DMQ04 | `immediate_response_usable` | An immediate response is described, or explicitly reported not taken; silence/unknown is unusable. |
| DMQ05 | `ongoing_hazard_status_usable` | Current hazard persistence or resolution is explicitly described; silence/unknown is unusable. |
| DMQ06 | `consumer_concern_status_usable` | A patient/family concern or explicit absence of a reported concern is stated; silence/unknown is unusable. |
| DMQ07 | `synthetic_escalation_required` | At least one synthetic concern rule below is met in the packet's current evidential scope. |

For DMQ01–06, contradictory accounts about the required fact count as unusable until reconciled.
An explicit unknown is preserved as unknown; it is never rewritten as absence of care or harm.
The output identifies each unusable/uncertain field by its question ID, without inventing missing facts.

DMQ07 is a **synthetic review-concern label**, not an SAC/ISR/P priority or a clinical judgement. It is
positive when the authored packet contains a current/relevant, non-negated report of death, lasting
major harm, life-sustaining intervention following the event, or an unresolved immediate serious hazard.
A current unresolved credible account of one of those concerns also requires review even where another
account conflicts. Purely hypothetical, negated, unrelated historical or different-person descriptions
do not satisfy this synthetic rule. The independent reference must identify the triggering source span,
scope and polarity. It cannot infer a diagnosis, causal link, preventability or statutory reporting duty.

Twenty per cent of severe-positive families in every split have an explicit synthetic hard-review flag
in the permitted packet; all arms honour it. The remaining severe positives require the bounded
narrative judgement. The flag never substitutes for the remaining reference procedure or makes model
accuracy irrelevant. No hard flag is deliberately false in the confirmatory population; corrupted,
cross-case and malicious flags belong to the separate contract-rejection suite.

The final disposition is `continue_bounded_intake`, `request_listed_clarifications`,
`escalate_to_review` or `abstain_with_review`. None closes an incident. A review disposition succeeds
for this offline endpoint only if its permitted destination, request/view binding and explicit retained
review receipt validate within the deadline. It represents a recorded synthetic handoff, not an observed
human response. Merely intending review, swallowing a timeout or returning no output is not success.

One deterministic postprocessor derives the final disposition for **every arm**. G emits only the
seven probabilities keyed by their fixed question IDs; it does not generate a disposition or a
clarification list. After source/view/permission admission, apply this common precedence:

1. A validated synthetic hard-review flag or a positive severe gate yields `escalate_to_review`,
   even if another question is missing or unresolved. R uses its severe label; C/D/G use their own
   applicable severe threshold; H uses the OR of every valid invoked component gate and the hard flag.
2. Otherwise, any missing, malformed, unavailable or invalid required result, any explicit R unresolved
   state, or any selected forecast in the closed interval `[0.40,0.60]` yields `abstain_with_review`.
   This uncertainty band applies to all seven selected forecasts, including DMQ07 when step 1 did not fire.
3. Otherwise, one or more unusable completeness fields yield `request_listed_clarifications`, with
   exactly those DMQ01–06 IDs in ascending order. No missing fact is supplied by the postprocessor.
4. Otherwise, yield `continue_bounded_intake`.

Retain all question results, validity and uncertainty states even when a higher-priority disposition
wins. A severe escalation cannot conceal invalid outputs or turn them into useful coverage. Failed
source/view/permission admission is never repaired by this postprocessor; the integrity stop applies.

## 3. Population, references and fixed sample

Only original synthetic text with synthetic identifiers/placeholders is admitted. Published policy and
method sources inform the protocol; their case narratives are not copied. There is no patient sample.
Cases cover varied documentary styles and settings without claiming representative clinical frequency.

| Partition | Independent root families | Severe positive | Non-severe | At least one unusable field |
|---|---:|---:|---:|---:|
| Exploratory pilot | 40 | 10 | 30 | 20 |
| Training/development | 320 | 80 | 240 | 160 |
| Probability calibration | 400 | 100 | 300 | 200 |
| Threshold selection | 400 | 100 | 300 | 200 |
| Sealed final holdout | 1,200 | 300 | 900 | 600 |
| **Total** | **2,360** | **590** | **1,770** | **1,180** |

Within each partition, half of each severe/non-severe stratum is incomplete. Each completeness question
has at least 50 negative and 50 positive examples in each 400-family calibration partition, and at least
150 negative and 150 positive examples in the final holdout. The 40-family pilot estimates feasibility,
instruction ambiguity and authoring burden only; no confirmatory inference or threshold comes from it.

An independent family is a separately authored underlying event world. Copies, paraphrases, renderings,
same-episode accounts, reused semantic scenario templates and derivatives share the root family and
one split. A common file format alone does not make separate event worlds identical. Authors record
semantic-template ancestry and similarity screening before counting independent families. If a split has
fewer independent families than required, it fails readiness; new wording cannot manufacture sample size.

The reference team defines intended facts and severities before candidate responses exist. Two separate
agent reviewers independently label the source text with the frozen rubric and span/polarity/uncertainty
references; a third resolves disagreements by inspecting the packet and original author intent. They
must not see system predictions. Authorship, model/provider lineage, reference disagreements and
adjudication are recorded. Ambiguous author intent is repaired or excluded **before** the final manifest;
no case is excluded for being difficult for a candidate. Agent references establish synthetic rubric
truth only, not clinical truth, human agreement or independent human validation.

Assign families within the fixed strata by ascending SHA-256 of
`dm01-synthetic-intake-v1|partition-v1|root_family_id`, with lexicographic family-ID tie-breaking and
the fixed partition quotas. Root IDs are set before hashing; retain the complete assignment manifest
and do not regenerate IDs to obtain preferred splits. Related families are first collapsed to their
shared root. Freeze the semantic-ancestry and split audit with the reference manifest.

A prespecified secondary robustness subset takes the first 120 holdout root IDs under that same hash
order. Each has two equivalent presentation/order variants; 60 of those roots also have one variant
with a genuinely changed relevant fact and a correspondingly changed reference. Freeze these variants
and labels with D. The resulting additional 300 packets are **not** 300 independent cases and do not
enter the primary/severe denominators. Analyse them within family after canonical results are sealed.

## 4. Methods, comparator selection and resource reference

All arms receive identical permitted evidence and questions, obey the same hard vetoes, and use the same
120-second end-to-end deadline. There is at most one transient transport retry within that deadline;
contract/privacy/capability failures are not retryable. No remote fallback is allowed. Missing outcomes
and unsuccessful review dispatch remain failures in the original denominator.

| Arm | Frozen reference design |
|---|---|
| R | Deterministic required-field/lexical/negation rules written using training families only; rules and tests hash-frozen at M. Binary labels or explicit unresolved states, without probabilities. No access to hidden author labels at inference. |
| C | Seven binary TF-IDF + L2 logistic classifiers; word n-grams 1–2, maximum 20,000 features, `C=1`, no class weighting, fixed training seed. Fit vocabulary/models on training only. No encoder is needed for this first comparison. |
| G | One competent local generative structured-output comparator, seven probabilities keyed by fixed question IDs, maximum 512 output tokens, temperature 0. The common postprocessor supplies dispositions and clarification IDs. Self-reported probabilities remain predictions to be calibrated/evaluated, not native confidence guarantees. |
| D | One text Noul decision candidate, seven native probabilities; no multi-label, typed-answer, modality or narrative capability is assumed. |
| H | R/C/D first; use D forecasts only when C and D agree on all six completeness labels at 0.5 and the severe label at their selected component thresholds, and every calibrated probability is outside the closed interval `[0.10,0.90]`. Otherwise query the same G once on the original packet, without showing other models' answers. Preserve all method outputs and disagreement. |

The [candidate admission](./candidate-admission.json) identifies D's publisher-pinned discovery
candidate: `LiquidAI/d1-2B-GGUF@4a181094d1b6addfaa3a0956f78e7ab2aa406a0c`, Q8_0,
and `llama.cpp@8642541b255bfb5dc39cd351a178be09013a55d6` (b11960). These are not downloaded,
built or qualified by this protocol. Execution stays blocked until exact bytes, rights, compatibility,
isolation and measurement are admitted. A changed D tuple requires a prospective M record, not a silent substitution.

G assets remain **unselected/unadmitted**. Before M, consider at most three local generative candidates
that meet the hardware, licence, no-remote-code and structured-output boundaries; each may use at most
two predeclared prompts. Evaluate these at most six configurations on the 320 training families only.
Select lexicographically by lowest intent-to-evaluate material-decision error, highest useful coverage,
lowest full-procedure p95 latency, then stable configuration ID. Minimum training readiness is useful
coverage at least 0.70 and schema-valid responses at least 0.99. If no candidate meets it, the comparison
is blocked; do not silently choose a weaker model. Exact model/code/weight/prompt/runtime hashes are
required at M. D may compare at most two wording configurations on those same training families;
no arm sees calibration or holdout labels during model/prompt selection. C parameters are fixed, not
searched. Record these different, bounded development budgets rather than claiming identical tuning.

For this **training-only configuration ranking**, use raw, uncalibrated probabilities: `p >= 0.5`
is positive for both completeness and the severe gate, with the same closed `[0.40,0.60]` unresolved
band and common disposition precedence above. The severe gate therefore takes precedence when a
raw severe probability is at least 0.5, including values inside that band. Hard flags, validity checks,
review receipts, deadlines and the material-error/useful-coverage definitions are unchanged. R supplies
its labels directly. Neither provisional thresholds nor raw forecasts are fitted on calibration data;
the final calibrated severe thresholds are selected later by section 5. Do not rerank G/D configurations
using those later outcomes or substitute a new configuration after selection.

After component calibration, completeness predictions use `p >= 0.5`; selected probabilities in the
closed interval `[0.40,0.60]` retain unresolved status and follow the common postprocessor above.
H retains the selected D/G forecast without pretending its selection mixture is calibrated;
its calibration is measured on the entire held-out cascade. H escalates if **any invoked** R/C/D/G
severe gate fires. No majority can cancel a concern. Invalid C/D/G observations cause explicit review
fallback; no invalid probability is repaired. Such fallback is not useful automatic coverage.

The planned reference hardware is an **Intel Core Ultra 7 155H, 32 GiB RAM, local SSD, Windows 11
x86-64, CPU-only with eight inference threads and no GPU/NPU offload**. This is a test target, not an
observed available machine or a claim of compatibility. Exact OS build, firmware, runtime build, power
mode and available memory are recorded at M. If unavailable, defer the hardware claim; another target
is a separately versioned profile. Do not generalise results across devices or quantisation.

Use ten training-only warm-up packets; measure cold start separately. Rotate R/C/G/D/H execution order
by root-family index modulo five, with deterministic ordering frozen before results. Record model
residency/loading, queue/preprocessing/serialization, all seven inference tasks, retries and fallback
latency, p50/p95/p99, throughput at concurrency one, peak RSS, output/input usage and total run cost.
There is no asserted 100–200 ms target or purchased compute authority. Resource differences are
secondary; they cannot compensate for failing a correctness/coverage criterion.

## 5. Calibration and threshold selection

Fit one sigmoid calibrator per question per C/D/G arm using only the 400 probability-calibration
families. Input is the logit of raw probability clipped to `[1e-6,1-1e-6]`; retain raw values separately.
Use L2 logistic regression with `C=1e6`, no class weighting, intercept enabled, `lbfgs`, tolerance
`1e-10`, maximum 1,000 iterations. Failure to converge, missing a class or invalid predictions means
calibration infeasible; do not change the method after inspecting thresholds/holdout. Reuse the
maintained scikit-learn implementation and pin its actual version at M. No calibrator is fitted for R
and no synthetic probabilities are invented for it. No separate H calibrator is fitted in v1.

For each C/D/G severe-concern gate independently, examine the fixed grid `0.00, 0.01, …, 1.00` on the
separate 400-family threshold set. A score at or above a candidate threshold escalates. Include hard
flags and actual validated review fallbacks in gate outcomes; invalid observations without successful
explicit review are unsafe misses. Choose the **largest** threshold with zero unsafe misses among
the 100 severe positives and no more than 20% escalations/review fallbacks among the 300 non-severe
families. If none qualifies, report infeasible and do not run a confirmatory holdout. This selection
does not establish a 1% FNR bound: zero of 100 has a 95% upper bound about 2.95%.

H uses those already selected component thresholds with its fixed OR rule and invocation policy;
it does not search another threshold. H must also have zero threshold-set unsafe severe misses,
non-severe unnecessary review at most 20%, and useful coverage at least 0.75 overall and 0.75 among
non-severe families. G must meet those same coverage criteria. A failure blocks the declared comparison;
it is retained as a negative development result, not repaired using final-test data.

Hash-freeze calibrators, selected grid points, rubric, question wording, candidate procedure, model tuple,
threshold outcomes and analysis implementation in M. A different source packet invalidates its cached
decision but does not fit a new calibrator; a changed task/model/procedure/population outside this
declared envelope invalidates the qualification binding.

## 6. Outcomes and prespecified numerical criteria

The primary unit is one canonical root family. The denominator contains **all 1,200 sealed eligible
families**, including timeouts, errors, missing outputs and abstentions. An unsuccessful run does not
delete a family. All seven task results and final dispositions remain available for adjudication.

For arm A, `E_A=1` when its returned candidate incorrectly marks an unusable field usable, loses a
required severe-review disposition, invents a factual assertion, violates the source/view binding, or
fails to return an outcome without a successful explicit review disposition. Valid abstention with a
validated review disposition has no false reassurance but is unresolved; it is reported separately
and contributes **zero useful coverage**. False missing-field judgements and unnecessary reviews are
burden/error outcomes even when they do not satisfy this material-error definition. Report each error
component, unresolved fraction and their union as well as the primary composite.

**Useful coverage** means all six completeness judgements are correct and resolved, DMQ07 has the
correct escalatory/non-escalatory disposition, and the valid source-bound result completes in time
without generic review fallback. Correctly requesting genuinely missing fields or correctly escalating
a severe concern can be useful triage; it does not mean the incident was resolved. Also report ordinary
valid-output coverage and material error on the automatically handled subset. Never use subset error
as the intent-to-evaluate rate. All-review, all-abstain and all-fields-missing strategies cannot pass.

| Criterion | Frozen research requirement |
|---|---|
| Primary benefit | `I = mean(E_G - E_H)`; one-sided 95% paired-family lower confidence bound **strictly greater than 0.02**. This supports more than a two-percentage-point reduction only for this synthetic population. |
| Useful coverage | Lower bound at least **0.70** overall and among 900 non-severe families, for both G and H. Overall uses the conservative stratified bound below; non-severe uses its one-sided exact 95% bound. |
| Coverage trade-off | One-sided paired-family lower bound of `coverage_H - coverage_G` at least **−0.05**. Reduction in work completed cannot silently explain a material-error gain. |
| Unsafe severe non-escalation | For H, one-sided exact 95% upper FNR bound at most **0.01** among all 300 severe-positive families. Missing/errors count unsafe unless explicit validated review succeeds. |
| Non-severe unnecessary review | For H, one-sided exact 95% upper bound at most **0.25** among all 900 non-severe families. Genuine missing-field clarification is reported separately from escalation/generic review. |
| Probabilistic calibration | H maximum per-question ECE point estimate at most **0.05**, with each one-sided bootstrap upper bound at most **0.08**; mean seven-question binary Brier at most **0.15**, with bootstrap upper bound at most **0.18**. These are synthetic research checks, not clinical calibration guarantees. |
| Integrity | No accepted privacy/source-view/permission/hard-veto violation. One such violation stops the run and prevents qualification. |

All criteria are conjunctive. A failed criterion is a negative result; inadequate precision is
inconclusive. Retain simpler methods when the hybrid does not earn its added complexity. R/C/D are
reported with the same denominators and metrics where applicable, but the only confirmatory contrast
is H versus G. Other pairwise/subgroup comparisons and robustness results are exploratory.

For every arm and task, report binary Brier `sum((p-y)^2)/n`, positive-class reliability and ECE using
ten fixed equal-width bins: `[0,0.1)`, …, `[0.9,1]`. ECE is
`sum_b(n_b/n * abs(mean(p_b)-mean(y_b)))`; empty bins contribute zero and counts are displayed.
Macro Brier/ECE weight the seven questions equally; severe-task metrics are also shown separately.
No usable probability means the probability metric is unavailable, not zero; disclose missingness and
failure denominators alongside it. H's selected forecasts and its conservative OR escalation rule are
distinct quantities; do not report the maximum score as a calibrated posterior.
If any canonical family lacks a usable forecast for a question, that question's confirmatory ECE/Brier
criterion is unavailable and cannot pass. Available-case scores may be reported only as exploratory,
with their actual denominator; they cannot replace the complete 1,200-family criterion.

Report severe predictive misses/abstentions separately from unsafe handoff misses, precision/F1,
per-field false completeness/false missing, confusion matrices, PPV, escalation workload and
risk–coverage curves. A severe concern safely deferred by fallback is not a correct model prediction.
R has no calibration metric unless an explicitly declared probabilistic variant exists in a new study.

## 7. Uncertainty, precision and stopping

Use exact Clopper–Pearson one-sided 95% intervals for within-severity-stratum binary safety/coverage/burden
rates under the declared independent-family binomial sampling model, using maintained SciPy. For
overall useful coverage, use `0.25*L_severe + 0.75*L_nonsevere`, where each L is a one-sided 97.5%
Clopper–Pearson lower bound; the union bound gives conservative 95% joint coverage without pretending
the fixed mixed strata are a single homogeneous binomial sample. For I, coverage differences, ECE and
Brier, resample **whole root families**, stratified into 300 severe/900 non-severe, with 20,000 paired
bootstrap replicates, fixed PCG64 seed `2026111601` and nearest-rank 5th/95th percentile bounds.
Both arms and all seven questions travel together. These bootstrap intervals are not called exact.
If independent-family assumptions fail, reject the confirmatory independence claim and report a
cluster-aware exploratory analysis; do not keep the original effective n. Correlated references and
synthetic construction limit external validity even if the numerical gates pass.

Pure local mathematical verification during DM01 produced:

| Calculation | Result | Interpretation |
|---|---:|---|
| `1 - 0.05**(1/300)` | 0.009936081944457711 | Zero unsafe misses in 300 independent positives meets the proposed 1% upper-bound criterion. |
| One-miss Clopper–Pearson upper bound, n=300 | 0.015714554891583965 | One unsafe miss fails the proposed criterion. |
| `ceil(log(0.05)/log(0.99))` | 299 | Minimum zero-miss independent positives for this one-sided bound; the study reserves 300. |
| `1 - 0.05**(1/100)` | 0.029513049607039932 | Threshold-selection zero misses alone does not establish the final safety precision. |
| `1.6448536269514722/sqrt(1200)` | 0.04748283421489823 | Worst-case approximate one-sided 95% half-width for a paired difference in `[-1,1]`. |
| `1.959963984540054/sqrt(1200)` | 0.05657928670380858 | Corresponding worst-case approximate two-sided half-width. |
| Assumed discordance 0.20 and improvement 0.05 | 0.021101833099359008 | Illustrative one-sided half-width using variance `0.20 - 0.05**2`; these are planning assumptions, not observations or a power guarantee. |

The 1,200-family holdout is selected principally for the severe-positive precision and a bounded first
study. It does **not** guarantee resolution of a two-point paired margin. The actual discordance may
make the contrast inconclusive. Do not extend the sample, change the margin, omit failed families or
replace G after viewing any holdout result. No clinical or population-safety inference follows from
the synthetic binomial calculation.

Stop immediately for evidence leakage, private content, unapproved egress, accepted hard-veto failure,
manifest mismatch or model/runtime identity drift. Ordinary timeouts/errors remain outcomes; stop a
run for infrastructure repair if more than 5 of the first 50 attempted canonical families have
infrastructure failures, or if any later fixed block of 50 exceeds 10%. Preserve consumed observations;
an interruption does not reset the holdout. Resume only the same frozen configuration and unchanged
unattempted IDs after documented repair; a substantive change ends the confirmatory run as incomplete.
There is no efficacy/futility peeking and no early success declaration. No final-test labels or aggregate
effect estimates are inspected before all planned canonical outcomes are sealed, except an independent
integrity monitor may inspect suspected safety/integrity violations and record that access.

## 8. DM01 completion and remaining work

DM01 freezes the procedure, numeric margins and sample arithmetic. It generates no scenarios, labels,
model outputs or operational decisions. D/M remain pending and model comparison is blocked until
exact admission and manifests exist. DM02 defines executable contracts, DM03 admits measured local
tuples, DM04 creates independent fixtures/references, and DM08/DM09 fit/freeze/run the study in order.

Primary methodological sources are retained in [the track source register](../sources.md): scikit-learn
calibration/grouping (S24), Inspect (S25), calibration research (S30), selective risk/coverage (S31) and
SciPy intervals (S32). The protocol proposes selection criteria; those sources do not certify the chosen
synthetic margins. Reviewer class, data/model rights, limits and negative results remain in every receipt.
