# Cognitive autopsy research programme and delivery

## Recommendation

Build one coordinated programme in the existing repositories. Start with a tightly scoped HDC documentary study of temporal reconstruction, source-grounded decision context and patient-relevant learning. Evaluate local models before adaptation; add a staged local pipeline only when an ablation demonstrates value. Keep optional cloud scheduling off the initial critical path.

Cognitive autopsy has an established clinical literature, including Croskerry's 2020 book, so the contribution cannot be the phrase or a prompt alone. The potential contribution is a reproducible, temporally controlled, provenance-aware and patient-centred evaluation with task-specific local-model qualification.

## Options and consequences

| Option | Value | Trade-off | Recommendation/contingency |
| --- | --- | --- | --- |
| HDC documentary methods and benchmark study | Uses the approved corpus and existing software; feasible first paper | Retrospective complaint selection and uncertain cognition | First project; report the actual evidence limits |
| Local staged RCA assistant | Tests extraction, reconstruction and verified learning together | Error propagation and integration burden | After component results; compare against best single model |
| Fine-tuned local specialist | May improve stable extraction/uncertainty errors at lower inference cost | Labels, leakage, memorisation, training/maintenance cost | Trigger only after residual error and paired-value evidence |
| Cognitive-autopsy education study with Peter Bourke | Directly addresses clinical reasoning, learning and decision review | Needs actual learners, educational outcomes and applicable governance | Follow-on if documentary feasibility is strong |
| Whole-RCA clinical effectiveness study | Most relevant to operational patient safety | Requires workflow observation, implementation and follow-up | Later stage; cannot be inferred from benchmark scores |

## Coding-agent delivery schedule

| Work package | Agent work | Human work | Planning duration |
| --- | --- | --- | --- |
| Contracts and corpus inventory | Locate/pin payloads, map schemas, source checks, protocol draft | Confirm only genuine scope ambiguities against existing approval | 1–2 working days |
| Local prototype | Packet builder, baseline adapters, source-linked review UI, deterministic checks | Consolidated review of intended claims and materiality definitions | 3–5 days, partly parallel |
| Pilot and frozen comparison | Run admitted local models, error clustering, resource measurement, sample-size calculation | Targeted adjudication only if needed for the intended validity claim | 3–5 days after inputs available |
| Main documentary evaluation | Batch execution, clustered statistics, robustness/contamination analysis | Adjudication/governance exceptions; authors interpret evidence | 1–2 weeks, hardware dependent |
| Optional adaptation | One bounded experiment and paired evaluation | Existing training/release scope applied; new reserved choices only | Add 3–7 days if justified |
| Manuscript and release preparation | Tables, figures, citations, reproducibility package and draft | Authorship, interpretation and final publication governance | Draft at roughly weeks 4–6 |

These are effort estimates, not a promise of journal submission or a powered clinical study in six weeks. Coding speed does not remove source quality, actual hardware execution or genuine human observations where required.

Use one integration agent and two independent implementation lanes with separate files. Agents can prepare almost everything, including structured evidence for rapid review. Repository engineering reviews use the existing three-role agent-panel policy. If a panel is unavailable, record that fact and retain the review task; do not silently replace it with alleged independent agreement.

## Patient-centred resource evaluation

The economic question is whether resources produce more trustworthy, actionable learning about patient care. Report time and cost alongside material errors, concern coverage, correction burden and usable-output rate. Model inference speed alone is not reviewer time saved. A source-linked review interface should record actual review/edit time locally when a user study occurs.

Avoid a single opaque weighted score that lets faster output compensate for a harmful unsupported conclusion. Present a cost-consequence table and quality/resource frontier. Any future cost-effectiveness model must state how text quality links to observed care changes and harms; those transitions are currently unmeasured.

## Publication strategy and realistic prospects

| Study achieved | Suitable targets | Assessment |
| --- | --- | --- |
| Reproducible HDC/local-model component evaluation with transparent limitations | BMC Medical Informatics and Decision Making; JAMIA Open; BMJ Health & Care Informatics | Credible fit if the benchmark/reference quality and clinical motivation are convincing |
| Strong evidence of changed safety-review quality, patient-relevant learning or workflow benefit | BMJ Quality & Safety; Journal of Patient Safety; The Joint Commission Journal on Quality and Patient Safety | More demanding; a prompt demo or agent-only ratings would be a weak submission |
| Educational intervention with authentic learning/transfer outcomes | The Clinical Teacher; BMC Medical Education; Medical Education for a stronger theory-driven study | Fits Peter's educational role if actual learner evidence is collected |
| Generalisable technical advance plus broad external validation | npj Digital Medicine or a relevant informatics methods venue | Stretch target; small HDC-only experiments are unlikely to justify this level alone |

These are editorial-fit judgements, not numerical acceptance probabilities. A well-designed negative fine-tuning or model comparison can be publishable. Agent-only scoring supports a narrower methods/feasibility claim; stronger journals will reasonably ask whether the reference and outcomes matter to patients.

Prepare one coherent initial paper rather than several thin model comparisons. Proposed title: “Cognitive autopsy with local language models: temporally controlled reconstruction of healthcare decisions in New Zealand HDC reports.” A separate education paper should answer a distinct question with new observations.

## Literature and source anchors

- Croskerry P. The Cognitive Autopsy: A Root Cause Analysis of Medical Decision Making. Oxford University Press; 2020. [DOI](https://doi.org/10.1093/med/9780190088743.001.0001).
- Zwaan L and colleagues. Is bias in the eye of the beholder? BMJ Quality & Safety; 2017. [DOI](https://doi.org/10.1136/bmjqs-2015-005014). Outcome-dependent bias attribution is a core design concern.
- Chen and colleagues. AI-driven analysis of patient safety reports. BMJ Quality & Safety; 2026. [Primary record](https://pubmed.ncbi.nlm.nih.gov/41617612/); [DOI](https://doi.org/10.1136/bmjqs-2025-019495).
- Sirago and colleagues. Large Language Models as Raters. The Joint Commission Journal on Quality and Patient Safety; 2026. [Primary record](https://pubmed.ncbi.nlm.nih.gov/42888060/); [DOI](https://doi.org/10.1016/j.jcjq.2026.09.002). Do not assume model voting removes correlated error.
- Wang and Redelmeier. Artificial intelligence chain-of-thought reasoning and model intransigence. BMJ Quality & Safety; 2026. [Primary record](https://pubmed.ncbi.nlm.nih.gov/41285583/); [DOI](https://doi.org/10.1136/bmjqs-2025-019299). Test appropriate updating as well as stability.
- Matsuura and colleagues. Hindsight Bias in Clinical Temporal Reasoning: How Future Data Exposure Affects Large Language Model Judgment. [arXiv:2609.13454](https://arxiv.org/abs/2609.13454), 2026 preprint. Temporal masking itself should not be claimed as new.
- Journal scope: [BMC Medical Informatics and Decision Making](https://link.springer.com/journal/12911/aims-and-scope), [JAMIA Open](https://academic.oup.com/jamiaopen/pages/about), [BMJ Health & Care Informatics](https://informatics.bmj.com/pages/authors), [The Clinical Teacher](https://onlinelibrary.wiley.com/page/journal/1743498x/homepage/productinformation.html).

Sources reviewed for planning on 2026-11-07. Full dataset references are maintained separately. Verify publication metadata and journal requirements again at manuscript submission.

## Refined positioning and first experiments

The closest literature now includes explicit LLM RCA on public radiation-oncology reports ([Wang et al., 2026](https://doi.org/10.1371/journal.pdig.0001740)), local clinical agents ([Nature Medicine, 2026](https://doi.org/10.1038/s41591-026-04609-x)), paired diagnostic counterfactuals ([MedEinst, ACL 2026](https://doi.org/10.18653/v1/2026.acl-long.1847)), and NLP/generative extraction of object-centric logs ([Buss et al., 2026](https://doi.org/10.1016/j.is.2026.102713)). Temporal masking and uncertainty-aware conformance also have direct precedents. Do not claim the first AI cognitive autopsy, first temporal masking, first text-to-log method, or first controlled model-bias experiment.

Prioritise three small linked studies:
1. Source-supported assertion and account attribution: rules/medspaCy, classical TF-IDF/linear, optional encoder and local LLM.
2. Exact and semantic claim verification: measure generator-plus-verifier errors, false rejection, critical omissions and useful coverage.
3. Information availability and hindsight: outcome-by-availability controlled tests with source-linked three-clock reconstruction.

A fourth bounded extension tests how event-extraction/ordering errors change the downstream investigation; reuse existing process algorithms. Behavioural economics supplies experimentally controlled frames, defaults, base rates and information-acquisition models, not retrospective estimates of individual clinicians' psychological parameters.

These are plausible task-specific gaps; a targeted search on 2026-11-07 did not establish an exhaustive absence of previous applications. Search strings included dataset names MedNLI/NLI4CT/THYME with root cause analysis or cognitive autopsy, clinical bias titles, patient-safety NLP classifiers and text-to-event-log literature. Maintain a reproducible search through Searchright when preparing the paper. Novelty depends on comparison with close prior work and actual held-out results.

The [component plan](./component-studies.md), [controlled experiments](./controlled-experiments.md), [process plan](./process-mining.md) and [verification/reuse plan](./verification-and-reuse.md) define the methods. The [25 bounded work packages](../../tracks/cognitive-autopsy_20261107/work-packages.md) place simple reusable components first. Code/fixture preparation can take days; source audit, necessary annotation and actual study evidence determine elapsed publication time.

Prefer one coherent methods paper on faithful decision reconstruction and verification. A process-methods paper is justified only by a distinct uncertainty/error-propagation result; an education paper needs transfer observations. Existing datasets in a new domain are not by themselves a frontier claim. Journal fit remains an assessment, not an acceptance probability.
