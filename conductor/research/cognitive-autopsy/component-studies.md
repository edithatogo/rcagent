# Small component studies and conventional NLP comparators

Status: proposed research, checked against primary sources on 2026-11-07. No dataset is admitted, model run completed or capability qualified by this document. The [candidate register](./component-datasets.json) records eight NLP dataset families and two process-log datasets; [component references](./component-references.bib) supplement the existing [dataset bibliography](./datasets.bib).

## Purpose and literature gap

Test whether established extraction and verification methods transfer to contested, retrospective HDC narratives, and whether a local large language model (LLM) adds useful accuracy at an acceptable resource cost. The owner-confirmed HDC ethics approval remains the primary study authority; supplementary datasets have separate terms and need not block HDC work.

Clinical assertion, temporal extraction, incident classification and controlled perturbation are established tasks. The 2010 i2b2 challenge reported strong assertion classification with uneven rare-class performance ([Uzuner et al.](https://doi.org/10.1136/amiajnl-2011-000203)); conventional classifiers have also been evaluated on patient-safety reports ([Evans et al.](https://doi.org/10.1177/1460458219833102)). A local-LLM versus rules comparison for German clinical negation already exists ([Zowalla and Wiesner](https://doi.org/10.3233/SHTI251374)). Avoid a first-ever comparison claim.

The plausible contribution is field-level provenance and availability reconstruction in HDC, evaluated through material attribution, omission and leakage errors. This bounded search does not establish that an external dataset has never been used for RCA. Reuse the medication-incident concepts in [MRIRA](https://doi.org/10.3389/fdgth.2026.1712526) where appropriate; its annotated NHS records are not available for sharing.

## Prioritised studies

| ID | Small task and component | Main question | Useful result even if an LLM adds nothing |
| --- | --- | --- | --- |
| CS01 | Assertion and account attribution; CA01/CA02/CA09 | Can a method distinguish what is asserted, who supplied the account and what kind of evidence it is? | A fast, auditable extractor with measured limits and a documented HDC annotation layer |
| CS02 | Claim-to-evidence verification; CA02/CA11 | Does the cited evidence support the specific claim, including actor, time, negation and numbers? | A verifier that rejects material errors without suppressing too much supported information |
| CS03 | Temporal extraction and availability; CA03/CA04 | Can a method reconstruct partial chronology without inventing when information became available? | A reliable event representation for later decision analysis and process-mining experiments |

Run CS01 first, then CS02, then CS03. These are coherent components of one methods programme, not an assumption that each routine benchmark merits a separate paper.

## Common comparison and evaluation contract

| Arm | Implementation family | Role |
| --- | --- | --- |
| CS-RULES | Heading/quotation/date rules, clinical dictionaries and medspaCy ConText modules | Cheap, inspectable baseline; use a thin adapter and preserve raw text |
| CS-LINEAR | TF-IDF plus logistic regression or linear SVM for labels; CRF where sequence tagging is appropriate | Conventional supervised comparator |
| CS-ENCODER | A compact, non-generative contextual encoder suited to the task | Distinguish benefits of contextual representation from generation |
| CS-LLM | Untuned local model with constrained structured output | Generative comparator with the same admissible evidence |
| CS-CASCADE | Rules or encoder first, LLM only for defined difficult cases | Optional arm after a residual-error pattern justifies it |

A compact encoder is not conventional bag-of-words NLP, and schema constraints do not prove semantic correctness. Fine-tuning is optional under the existing [evaluation design](./evaluation-design.md); it is not an initial arm or a completion requirement.

- Freeze separate label-budget conditions: no task-specific labels, a small fixed labelled pool, and a larger admitted training pool where feasible. Include only methods that can operate in each condition; never compare an unfitted classifier with a pretrained LLM.
- Use the same training pool for rule refinement, supervised fitting and LLM demonstrations where applicable; report actual label exposure, prompt examples, manual rule effort, pretrained-data overlap, development trials and compute. Context limits may prevent identical presentation, so disclose that difference.
- Group report versions, linked cases, encounters and every derivative before train/development/test splitting. No test labels in prompts, retrieval, rule changes or selection. Freeze one primary contrast after development.
- Preserve numbers, units, punctuation, negation, quotations, paragraph coordinates and document boundaries. Store transformed features separately with reversible source-offset mappings.
- Match permitted evidence, output fields and applicable context envelope. Record exact model/runtime revisions and hardware; report quality at comparable budgets and the observed quality/resource trade-off.
- Use case-family clustered uncertainty. Report macro/per-class F1 and class prevalence, but retain the primary patient-relevant material-error outcome and minimum useful coverage. Count invalid outputs, timeouts and abstentions explicitly.
- Agent annotations and scores retain their reviewer-class label. A bounded random source audit supports prevalence estimates; separately selected disagreements do not provide an unbiased accuracy denominator. Human clinical or patient-participation claims require corresponding observations.
- Set sample size from pilot precision and eligible cases, not a fixed number of extracted sentences. Preserve existing synthetic results and use new CS study/run identifiers.

## CS01: Assertion and account attribution

The unit is a source-supported claim/account with context, not a whole report assigned one label. Extend the canonical evidence contract rather than create a second source store.

| Proposed field | Required behaviour |
| --- | --- |
| source_id, source_revision, span_start, span_end | Resolve to the immutable source and reproduce the exact cited text; offset convention is versioned |
| assertion_status | Distinguish affirmed, negated, possible, conditional/hypothetical and unknown; retain benchmark-specific label mappings |
| experiencer_or_subject | Preserve who the statement concerns; do not assume every finding concerns the patient |
| account_provider, attribution_span | Separate the speaker/account provider from the subject; unknown stays unknown |
| evidence_class | Distinguish contemporaneous record, retrospective account, expert interpretation and model hypothesis; retain ambiguous cases |
| rationale_present | Extract documented rationale when present; absence of a rationale is not absence of reasoning |
| contradiction_links | Preserve conflicting accounts without automatically choosing a winner |
| patient_concern_links | Link documented concerns or preferences and identify missing coverage without inventing a patient voice |

A model hypothesis may cite its premises but cannot become an observed fact through citation. Contemporaneous status needs documentary evidence; a confident past-tense sentence does not establish it.

Use i2b2 2010 for assertion machinery, with a separate HDC provenance annotation layer. PubMed-RCT sentence roles are an optional transfer experiment, not a reference for HDC evidence classes. SHAC can test extraction of explicitly documented social context; it does not label patient preferences or family concerns.

Acceptance measures: supported attribution precision/recall; rare assertion classes; unresolved-account coverage; patient-concern omissions; material false attribution. Include quotation nesting, conflicting accounts, negation scope and absent-rationale fixtures. Adopt the simplest arm that meets the frozen task requirements; a negative LLM comparison remains informative.

## CS02: Verify the claim, not just the citation

Split verification into deterministic source identity/span checks and semantic support assessment. Return support, contradiction or insufficient evidence for each scoped claim, plus the exact supporting spans and any failed checks. A source-supported statement is not automatically clinically true; an attributed account can be faithfully represented while its underlying assertion remains disputed.

Use NLI4CT for multi-evidence support, NLI4CT-P for paired perturbations, MedNLI for clinical inference and MEDEC-MS for medical-error detection. Preserve their different labels: NLI4CT's binary labels do not supply an insufficient-evidence class, and MEDEC's correct/one-error notes do not provide RCA causal ground truth. New HDC labels or independently checked variants are needed for those gaps.

Include hypothesis-only, evidence-only, shuffled-evidence and unrelated-case controls; correct quotations attached to unsupported claims; altered numbers/units; wrong actors; incorrect time scope; omitted contrary evidence; and sources that contain misleading instructions. [MedNLI artefacts](https://doi.org/10.18653/v1/2021.acl-short.129) show why a verifier must demonstrate use of evidence.

The [NLI4CT-P erratum](https://aclanthology.org/2024.semeval-1.271e1.pdf) corrects a consistency calculation that originally used gold-label accuracy instead of paired predictions. Pin a corrected evaluator and independently test prediction agreement and correctness as separate properties. An always-identical answer can be consistent and wrong.

Primary measures: material false-acceptance rate, false-rejection rate, retained supported-claim coverage and unresolved rate. Distinguish retrieval failure from verifier failure by testing both supplied-reference evidence and end-to-end retrieval. Calibrate thresholds on development data, then freeze them. Cross-model agreement is not a truth label.

## CS03: Separate chronology from information availability

Use [i2b2 2012](https://doi.org/10.1136/amiajnl-2013-001628) and [THYME](https://doi.org/10.1162/tacl_a_00172) for event/time spans and temporal relations. These labels do not establish which clinician saw information. Add an HDC-specific availability layer only when the record supports it.

Represent event, documentation and actor-specific availability times separately. Permit intervals, partial orders, conflicting assertions and unknowns; preserve stated timezone/granularity. Do not convert narrative order into event order or an event's existence into proof that a clinician knew it.

Compare exact-text extraction with event/time normalisation and downstream ordering separately. Score material ordering mistakes, unsupported precision, incorrect available/unavailable classifications, uncertainty coverage and later-information leakage. Test date-format ambiguity and contradictory timestamps with synthetic fixtures.

Export only the source-linked event representation to [process mining](./process-mining.md). Preserve uncertain or unobserved events; absence from an incomplete narrative is not proof of an omitted care action.

## Datasets, dependencies and delivery

[component-datasets.json](./component-datasets.json) is a candidate/source register, not a runtime allowlist or evidence of access. Admission must add exact releases, checksums, terms, permitted processing, annotation provenance, parent citations and grouped splits. Approved HDC research proceeds independently of unresolved external access. Restricted notes and derived case text stay out of public GitHub/Hugging Face; public metadata and adapters are separate artefacts.

Use maintained modules through the [verification and reuse plan](./verification-and-reuse.md). medspaCy already provides clinical section/context utilities ([Eyre et al.](https://pubmed.ncbi.nlm.nih.gov/35308962/)); inspect its current beta status and pin the tested revision. Disable destructive preprocessing for evidence records. Prefer existing linear-model, metrics and sequence-tagging implementations over project-owned equivalents.

Implement each study as five bounded agent tasks: (1) map existing input/output contracts; (2) add source-preserving fixtures and a candidate adapter; (3) implement the simplest comparator; (4) connect scoring and run receipts to the existing harness; (5) execute admitted development data, freeze the comparison, and evaluate held-out cases. Synthetic contract work can start before external-data access. Actual run duration depends on hardware and corpus availability.

Use [controlled experiments](./controlled-experiments.md) for bias/sensitivity manipulations and generated cases. Keep original HDC observations, altered derivatives and fully synthetic worlds separate in data lineage and denominators. The small studies measure extraction, support and temporal capability; they do not establish real clinician cognition, culpability, preventability or patient benefit.
