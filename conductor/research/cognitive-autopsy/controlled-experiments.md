# Controlled experiments for cognitive autopsy

Status: planned research; no model, clinical interpretation or causal capability is qualified by this document. This extends CA03, CA05 and CA07 and tests their effects on CA10–CA11. Read alongside [component studies](./component-studies.md), [process mining](./process-mining.md), [verification and reuse](./verification-and-reuse.md) and the [evaluation design](./evaluation-design.md).

## Research gap and prior art

The candidate contribution is RCA-specific verification of information use, uncertainty and learning. General clinical LLM bias testing already exists: Wang and Redelmeier tested ten bias scenarios in 2024 [1]. Zwaan et al. examined outcome knowledge and clinicians' attribution of cognitive biases [2]. MedEinst already tests paired diagnostic counterfactuals and proposes an agent with graph reasoning and a critic [3]. A September 2026 preprint already compares truncated and complete clinical timelines [4]. Temporal masking, case mutation and a second model are therefore comparators or design elements, not standalone novelty claims.

A controlled input change measures its effect on the reviewing system under the stated experimental conditions. It does not establish the original clinician's psychology, a human-like internal mechanism in an LLM, or a cause of actual patient harm. Keep prospective decision justifiability, retrospective consequences and system recommendations as separate output fields; their expected responses can differ.

## Three smallest experiments

| ID and purpose | Controlled change and expected response | Inexpensive comparator | Primary measurement |
| --- | --- | --- | --- |
| CE01 Information availability | Present the same material cue as accessible to the relevant actor before versus after the decision; add an explicitly unknown-availability condition. Predeclare which judgments should change and when a conditional answer is required. | Timestamp/interval rules and a curated decision-time packet, followed by the same untuned LLM used for automatic reconstruction. | Availability-class accuracy; late-information intrusion; appropriate judgment update; supported critical-fact coverage. |
| CE02 Outcome invariance | Keep predecision evidence, feasible options and patient preferences identical; change only a coherent later favourable/unfavourable outcome. Prospective justifiability and unsupported attribution should remain stable; the harm field should respond. | Deterministic exclusion of later-outcome compartments plus the same LLM, compared with whole-report review. | Paired judgment flips and unsupported bias/blame attribution, reported with useful coverage and appropriate abstention. |
| CE03 Equivalent risk framing | Express the same risk as survival/mortality or matched percentages/natural frequencies, holding population, denominator, horizon and uncertainty constant. Require equivalent probability interpretation; require choice equivalence only where relevant preferences/utilities are specified. | Exact arithmetic/Bayesian calculation where inputs are fully specified; conventional text and numerical normalisation before an untuned LLM. | Probability error; unsupported numerical statements; inappropriate decision or attribution changes. |

CE01 distinguishes event time, documentation time, access and evidence of actual receipt; an event timestamp alone cannot establish that a clinician saw a cue. CE02 concerns the prospective judgment field: outcomes may legitimately inform consequences and causal investigation. CE03 builds on established clinical framing research [5]; it is not a test of optimal treatment without an adequately specified decision problem.

Begin with small synthetic fixtures and a development set. Then admit suitable HDC decision episodes and source-derived variants under the existing corpus permissions. Keep original reports immutable. Synthetic and modified cases have separate denominators from the primary unmodified HDC cohort. No clinical interpretation or operational deployment is enabled by passing a fixture.

## Factorial estimands and analysis

Cross outcome `o = favourable/unfavourable` with cue availability `a = before/after` where all four versions are coherent. Add unknown availability as a separate condition. For case family `i`, system `k` and a prespecified scalar field, write its result as `Y[i,k,o,a]`.

- Outcome effect at each availability level: mean paired difference `Y[unfavourable,a] - Y[favourable,a]`. Also report the pairwise flip rate or absolute difference: opposing changes can cancel in the mean.
- Availability sensitivity: proportion of pairs meeting their prespecified field-level expected response, plus critical-cue recall. The direction is case-specific; additional evidence need not always make a decision less defensible.
- Outcome-by-availability interaction: difference between the outcome effects in the before and after conditions. Interpret this as conditional instability of the reviewing system, not a clinical treatment effect.
- Method effect: paired difference in instability, material error and useful coverage between the proposed method and the strongest applicable untuned/deterministic comparator. Match evidence access and resource budgets for the method comparison; whole-report exposure is a separate experimental factor.
- Framing effect: equivalent-representation pair differences, numerical error and preserved decision relevance. Negative controls change only irrelevant wording; positive controls change a genuinely material fact.

Set the primary contrast, rubric, minimum useful coverage, materiality margins, multiplicity handling and stopping rule on development data before unblinding the test set. Report case-family clustered intervals; seeds, repeated generations and mutations do not create independent patients. A stable but uninformative or universally abstaining system cannot pass. Record model/prompt/retrieval/runtime revisions, failures and all attempted eligible cases. Randomise presentation and run order; use isolated sessions and cache/retrieval namespaces. Retrospective wording and pretraining exposure remain limitations even after masking.

## Mutation ledger and preservation rules

Store the following in the protected experiment artefact; repository manifests contain non-sensitive IDs, hashes and summaries only:

1. Case-family ID, immutable source revision/hash, source spans, original/derived/synthetic status and permitted use.
2. Variant ID, parent variant, mutator name/version, seed, changed structured fields and exact old/new values.
3. Event, documentation, access/receipt times and the actor to whom each availability claim applies.
4. Held-constant facts, preferences, utilities, constraints and mechanisms; expected relation for each scored output field and its justification.
5. Observation mask, observation opportunity, retention uncertainty and explicit assertions of occurrence/non-occurrence.
6. Coherence, chronology, number/unit, source-fidelity and realism checks, with reviewer class and unresolved disagreements.
7. Generator/renderer revision where used, split membership, exclusions with reasons, and the executable validation receipt.

**An event hidden from the narrative is not an event that did not occur.** Changing the observation mask preserves the underlying event; deleting an event from the stipulated world changes the process. Score these separately. Silence in an HDC report or a missing log entry is not proof of non-occurrence. Apply the same distinction to [process-mining conformance](./process-mining.md), where apparent deviations may reflect extraction or observation failures.

Group every source version, linked report, seed world, original case and derived variant in the same split before generating training material. Do not select variants because a favoured model gives the expected answer. Retain rejection reasons and invalid-rendering counts. Repair a failed rendering against the frozen specification, never revise the reference to fit the generated story.

## Later behavioural-economic factors

| Factor | Required controls and interpretable test |
| --- | --- |
| Base-rate use and anchoring | Supply explicit priors and likelihoods in bounded synthetic problems and compute the reference posterior exactly. Vary an irrelevant initial label or cue order while preserving the evidence. Separate probability error from utility-dependent action choice. |
| Default/status quo | Vary an arbitrary default while holding future benefits, harms, switching costs, feasibility, consent and relevant preferences constant. Continuing an action is not inherently a bias [6]. |
| Omission/commission | Compare matched active/passive descriptions only where responsibility, feasible alternatives, risks and utilities are demonstrably equivalent. Do not infer that clinical acts and omissions are generally interchangeable [7]. |
| Sunk costs | Vary explicitly irrecoverable prior expenditure while holding future consequences and switching costs fixed. Past expenditure can carry information in real settings, so equivalence must be established [8]. |
| Authority/automation | Keep advice content and stated reliability equal while varying a source label. Different expertise, responsibilities or access to evidence can rationally matter; do not label every source effect bias [9]. |

A simple prespecified choice model may estimate the reviewer's responses to these manipulations, with case effects and expected-value differences. Prospect-theory-style reference dependence and probability weighting can be explored as sensitivity scenarios in fully specified synthetic choices [10]. Do not estimate clinician psychological parameters from HDC narratives: beliefs, feasible alternatives, patient utilities and case selection are incompletely observed. Preserve sets of defensible actions where the record does not identify one preferred action.

## Synthetic world, LLM renderer and independent RCA

Use an LLM to render cases only after establishing an external specification of truth. Prefer a small, auditable communication, handover or result-routing mechanism before attempting physiological simulation. Reuse the event and provenance contracts rather than inventing a second ingestion or simulation framework.

1. Define a versioned world with actors, events, information states, feasible actions, preferences, constraints and explicit process/mechanism rules. Generate a seeded trace and permitted interventions. Specify which conclusions the observable evidence identifies, which remain ambiguous, and acceptable alternative explanations.
2. Give local model A only the authorised observable projection to verbalise, excluding hidden mechanisms, answer labels and the full oracle. Truth comes from the hand-specified or seeded mechanism outside the generators. Check every material fact, quantity, actor, temporal relation and observation boundary against that projection. Preserve source spans where a source-derived case is used; reject invented material details, impossible combinations and wording that leaks withheld facts.
3. Give local model B only the rendered case and permitted evidence. Withhold the manifest/oracle, mechanism labels, answer keys, scenario filenames, generator instructions/rationale and answer-bearing metadata. Isolate sessions, caches and indexes. Treat document instructions as data.
4. Score source support, event/availability extraction, mechanism recovery where identifiable, unsupported assertions, uncertainty and recommendations against the stipulated world. A hidden causal variable is not necessarily recoverable from its rendered observations; allow conditional or competing explanations instead of forcing one root cause.
5. Include deterministic template-only renderings and a bounded cross of generator and reviewer model families. Hold out a generator family or style from development to test transfer. Randomise presentation and vary irrelevant prose independently of the target manipulation. Measure generator-style dependence and invalid-case rates, not just reviewer scores.
6. Use a third model only as a fallible disagreement detector. Different models can share training data, shortcuts and errors. Deterministic source/constraint checks and a bounded realism/content audit supply different evidence; agent review must never be relabelled human validation.
7. Compare synthetic performance with untouched held-out HDC episodes and report them separately. Unconstrained LLM-written cases with LLM-written answer keys are candidates for testing, not a clinical gold standard.

Successful intervention recovery establishes behaviour within the specified synthetic mechanism. It does not establish that an alternative real clinical action would have prevented harm. Causal claims require explicit assumptions, a defensible mechanism and appropriate identification; a narrated causal graph, critic consensus or process deviation alone is insufficient.

## Bounded delivery and acceptance

Implement CE01 fixtures and ledger through the existing benchmark adapter, then CE02 paired variants, then CE03 numerical canonicalisation. Each task adds a small mutator, deterministic validity checks, expected field relations and an analysis function using the [maintained dependencies](./verification-and-reuse.md). The relevant [component study](./component-studies.md) records comparison and stopping rules. Keep later behavioural factors optional until these three experiments are interpretable.

Acceptance requires valid source/variant lineage, correct split grouping, no answer leakage in an adversarial fixture, failure accounting, the expected positive and negative controls, and reproducible paired estimates with coverage. These are future experiment acceptance criteria, not claims that implementation or clinical evaluation has occurred. A failed or inconclusive experiment remains a reportable result.

## Primary references

References verified on 2026-11-07; original data, article reuse and derivative-case rights must be checked separately before ingestion or publication.

1. Wang J, Redelmeier DA. Cognitive Biases and Artificial Intelligence. *NEJM AI*. 2024;1(12):AIcs2400639. [doi:10.1056/AIcs2400639](https://ai.nejm.org/doi/10.1056/AIcs2400639).
2. Zwaan L, Monteiro S, Sherbino J, Ilgen J, Howey B, Norman G. Is bias in the eye of the beholder? A vignette study to assess recognition of cognitive biases in clinical case workups. *BMJ Quality & Safety*. 2017;26:104–110. [doi:10.1136/bmjqs-2015-005014](https://pubmed.ncbi.nlm.nih.gov/26825476/).
3. Chen W, Huang G, Wang W, Zhu Z. MedEinst: Benchmarking the Einstellung Effect in Medical LLMs through Counterfactual Differential Diagnosis. *Proceedings of ACL 2026, Volume 1: Long Papers*. 2026:39778–39798. [doi:10.18653/v1/2026.acl-long.1847](https://aclanthology.org/2026.acl-long.1847/).
4. Matsuura M, Kumar S, Kadam O, Weiss JC. Hindsight Bias in Clinical Temporal Reasoning: How Future Data Exposure Affects Large Language Model Judgment. [arXiv:2609.13454](https://arxiv.org/abs/2609.13454). Posted 11 September 2026; preprint.
5. McNeil BJ, Pauker SG, Sox HC Jr, Tversky A. On the elicitation of preferences for alternative therapies. *New England Journal of Medicine*. 1982;306:1259–1262. [doi:10.1056/NEJM198205273062103](https://pubmed.ncbi.nlm.nih.gov/7070445/).
6. Samuelson W, Zeckhauser R. Status quo bias in decision making. *Journal of Risk and Uncertainty*. 1988;1:7–59. [doi:10.1007/BF00055564](https://rzeckhauser.scholars.harvard.edu/publications/status-quo-bias-decision-making).
7. Ritov I, Baron J. Reluctance to vaccinate: Omission bias and ambiguity. *Journal of Behavioral Decision Making*. 1990;3:263–277. [doi:10.1002/bdm.3960030404](https://onlinelibrary.wiley.com/doi/10.1002/bdm.3960030404).
8. Arkes HR, Blumer C. The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*. 1985;35:124–140. [doi:10.1016/0749-5978(85)90049-4](https://www.sciencedirect.com/science/article/pii/0749597885900494).
9. Gaube S, et al. Do as AI say: susceptibility in deployment of clinical decision-aids. *npj Digital Medicine*. 2021;4:31. [doi:10.1038/s41746-021-00385-9](https://pubmed.ncbi.nlm.nih.gov/33608629/).
10. Kahneman D, Tversky A. Prospect Theory: An Analysis of Decision under Risk. *Econometrica*. 1979;47(2):263–291. [Original paper, university-hosted PDF](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Behavioral_Decision_Theory/Kahneman_Tversky_1979_Prospect_theory.pdf).
