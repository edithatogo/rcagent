# Bounded cognitive-autopsy work packages

These are future implementation leaves, not completed tasks or existing commands. The coordinating [plan](./plan.md) controls sequencing; the [experiment catalogue](../../../evaluation/cognitive-autopsy/experiment-catalogue.json) maps research questions to these leaves. Start with CAW01–05, 07–12 and 20–22. Optional encoder, rendering, process and VOI lanes must not delay the first component study.

## Execution contract

Each coding-agent task consumes the named inputs, changes only its declared adapter/fixture/analysis files, records exact versions, and stops after its acceptance evidence is met. Read the relevant component document instead of the whole repository. Reuse maintained dependencies; write only the domain mapping and invariants they lack. A task with unavailable controlled data can proceed on admitted HDC/synthetic or public alternatives while recording the missing comparator.

No task authorises private data in cloud coding contexts, arbitrary model-triggered tools, a dataset/model release, clinical deployment, or new paid compute. Existing HDC ethics is accepted; routine reversible implementation and agent review continue without repeated approval. Human effort is batched around study definitions, a bounded reference/rubric audit where claimed, and decisions requiring authority. Agents perform preparation, coding, runs, analysis and drafting.

## Leaves

| ID | Task | Depends on | Inputs | Deliverable | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| CAW01 | Source and dependency admission | none | Existing corpus/rights register and component datasets | Immutable candidate manifest, no implicit downloads/releases | Unknown revision/licence remains explicit; public and controlled subsets separate |
| CAW02 | Minimal source-linked record | CAW01 | Existing evidence schema and CA01–CA05 | Versioned assertion/account/time/span record and synthetic fixtures | Unknown availability and competing accounts survive round-trip; no duplicate generic validator |
| CAW03 | Grouped split and mutation lineage | CAW02 | Source family IDs and duplicate/version relationships | Frozen development/calibration/test grouping manifest | All linked reports, variants and renders stay in one family; fit vocabulary only on training |
| CAW04 | Rules baseline | CAW02, CAW03 | Admitted spaCy/medspaCy and documented labels | Thin rules/ConText/section adapter | Polarity, attribution and offset fixtures; measured per-label errors; raw text untouched |
| CAW05 | Classical statistical baseline | CAW03 | Same labelled examples and units | scikit-learn TF-IDF + regularised linear pipeline | Grouped validation, class/rare-label metrics and label-budget learning curves |
| CAW06 | Optional compact encoder baseline | CAW03 | Admitted local encoder and same labels | Non-generative encoder adapter | Separate category from classical NLP; same splits and documented compute/training budget |
| CAW07 | Untuned local LLM baseline | CAW02, CAW03 | Existing runtime/harness and admitted model tuple | Structured output adapter without weight changes | Exact prompt/template/context recorded; all failures counted; no cloud data flow |
| CAW08 | Exact source verifier | CAW02 | Immutable source bytes, quotes, IDs and offsets | Deterministic source/span/version/number checker | Reject injected wrong-ID/span/version/polarity fixtures where detectable; false rejection reported |
| CAW09 | Semantic support verifier | CAW03, CAW08 | Admitted NLI/error datasets and local model | Calibrated supported/contradicted/insufficient assessor | Hypothesis-only/shuffled-evidence controls; original and corrected items; no proof-of-truth claim |
| CAW10 | Availability and order verifier | CAW02, CAW08 | Event/document/recipient-availability intervals | Cutoff entitlement and graph consistency checks | Before/after/unknown cases distinguished; contradiction preserved; no invented point timestamps |
| CAW11 | Mutation manifest and operators | CAW03, CAW10 | Controlled-experiment definitions | One-factor edits, invariants and expected affected outputs | Every change traced; immutable originals; absence of evidence distinct from actual omission |
| CAW12 | Outcome × availability experiment | CAW07, CAW11 | Frozen development-selected method and paired families | Independent-session 2×3 outcome/availability run ledger | Outcome invariance and relevant-cue sensitivity scored separately, clustered by family |
| CAW13 | Equivalent risk-framing experiment | CAW07, CAW11 | Fixed risks/denominators/horizons/options/utilities | Equivalent percentages/frequencies/survival-mortality variants | Exact arithmetic oracle; representation invariance distinct from action optimality |
| CAW14 | Synthetic world and evidence projection | CAW02, CAW11 | Explicit events, actors, causal assumptions and seeded mechanism | Hidden world/oracle plus permitted observable packet | Oracle unavailable to RCA system; alternative compatible explanations accepted where non-identifiable |
| CAW15 | Renderer and round-trip controls | CAW14 | Observable packet, template renderer and optional local generator | Verified narrative variants and renderer metadata | No mechanism labels; render-to-world audit; held-out generator/style and template-only controls |
| CAW16 | Source-to-trace adapter | CAW02, CAW04, CAW07, CAW10 | Rules/LLM records and audited reference traces | Canonical uncertain trace and optional XES/OCEL2 export | Source spans and interval/partial-order information preserved; export loss explicit |
| CAW17 | Upstream process-engine fixture | CAW16 | Qualified upstream Rust4PM revision | Thin replay/conformance adapter and consumer fixtures | Use existing algorithms; reference-model provenance; deviation not labelled clinical error |
| CAW18 | Uncertain-conformance comparator spike | CAW17 | Published uncertainty method; optional qualified PROVED/PM4Py | Replication or explicit unsupported-capability report | Compatibility/licence recorded; no claim of uncertainty support from ordinary alignments |
| CAW19 | Extraction-to-judgment propagation | CAW07, CAW16, CAW17 | Reference, rules-derived and LLM-derived traces | Paired assessment comparison with fixed downstream model | Attribute changed judgments to trace differences; include matching-context raw-text comparator |
| CAW20 | Patient-concern and omission audit | CAW02, CAW04, CAW07 | Documented concern inventory and permitted context | Concern-to-response trace and material omission score | Missing voice stated; no inferred preferences; precision and useful coverage reported jointly |
| CAW21 | Generator-plus-verifier evaluation | CAW08, CAW09, CAW10, CAW20 | Natural model errors and separate injected-error set | End-to-end quality/coverage/resource report | Verifier gains, misses and false blocking measured; no all-abstain winner |
| CAW22 | Paired analysis and pilot precision | CAW03, CAW12, CAW21 | Frozen contrast, case-family run ledger and rubric | Cluster-aware estimates, uncertainty and cost-consequence table | Variants/repeats not independent cases; numerical margins set before test unblinding |
| CAW23 | Conditional adaptation decision | CAW05, CAW07, CAW21 | Repeated residual errors and authorised training labels | One bounded train/no-train decision and optional PEFT contrast | Beats strongest untuned comparator under predeclared gates or retains untuned model |
| CAW24 | Optional value-of-evidence model | CAW14, CAW22 | Explicit states, priors, likelihoods, utilities and acquisition cost | Voiage consumer experiment or empirical question-ranking study | Supported-accuracy or material-error/loss reduction at fixed evidence budget; report burden separately; formal VOI needs an admitted model |
| CAW25 | Coherent paper and handoff | CAW22 | Verified results, primary citations and negative findings | Research report in learningfromharm and reproducibility bundle | Claims match source/task/hardware evidence; clinical/education benefit unclaimed without observations |

## Practical sequencing and estimates

- Days 1–2 of coding-agent work after input access: record/schema/splits and exact source-verification fixtures.
- Days 2–5: conventional baselines, untuned local adapter, availability checks and calibrated component scoring.
- Days 5–10: small development pilot, controlled outcome/availability comparison and case-level analysis, subject to hardware and necessary annotation.
- Later 2–5 day bounded spikes: process-engine adapter and uncertainty/error-propagation experiment; synthetic generation is optional.
- Conditional adaptation and VOI are separate, triggered experiments. Manuscript drafting can run alongside results assembly; elapsed research time depends on evidence and access, not coding speed alone.

Use the existing repository validator during planning: python tools/validate_repository.py and git diff --check. During implementation, add focused contract/property tests for each new behaviour; do not mark a task passed merely because a script exists. Every adapter exposes unavailable capability rather than routing to a cloud fallback.

## Study stopping rules

Freeze the principal contrast and acceptable uncertainty before opening the holdout. Keep conventional methods if LLMs add no useful gain. If a reference cannot establish availability, evaluate recognition of uncertainty. If synthetic renderings leak answers or fail fidelity checks, exclude them with counts and continue template-only. If uncertain process conformance is unsupported, retain intervals and label the result unavailable. Negative or inconclusive comparisons are valid results, not a reason to redefine success.

Repository agent review is engineering/research-plan assurance; it is not human clinical validation. Preserve run failures, reference disagreements, unknown source rights and the distinction between patient-relevant text outcomes and observed benefit.


Optional evidence does not create a mandatory prerequisite: CAW22 consumes CAW13/CAW19 only if those extensions ran; CAW23 uses CAW06 only if an encoder was admitted. CS03 starts with simple CAW02 interval/cutoff fixtures, without requiring the later CAW14 mechanistic-world lane. The initial CS04 question is equivalent framing only; base-rate updating needs a separately specified prior/likelihood experiment.
