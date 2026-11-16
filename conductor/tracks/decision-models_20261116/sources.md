# Decision-model primary-source register

Source check: **16 November 2026**, using the requested client date. This is a documentation/model-card review, not installation, executable-code review, licence advice, model measurement or clinical validation. Mutable URLs below are discovery references. DM01 must pin the exact artefact/revision, source snapshot and applicable rights before execution; no immutable model revision is invented in this plan.

## Model and runtime evidence

| ID | Primary source | Bounded finding used in the proposal |
|---|---|---|
| S01 | Liquid AI, [d1-2B model card](https://huggingface.co/LiquidAI/d1-2B) | Native decision/typed API; local Score median; extraction `found` boundary; custom implementation. Read the authored card rather than generic automatically generated chat snippets. |
| S02 | Liquid AI, [d1-Omni-2B model card](https://huggingface.co/LiquidAI/d1-Omni-2B) | Distinct audio-capable candidate; decision output is not transcription. The exact repository spelling matters. |
| S03 | Liquid AI, [d1-omni-600M model card](https://huggingface.co/LiquidAI/d1-omni-600M) | Smaller, earlier decision family with different limits. Do not infer newer typed-head support from its name. |
| S04 | Liquid AI, [hosted d1 documentation](https://docs.liquid.ai/lfm/models/d1) | d1.1/d1-ultra, hosted endpoint and provider links. Scope and billing are provider-specific; typed/local capabilities are not automatically portable. |
| S05 | Liquid AI, [d1-2B GGUF](https://huggingface.co/LiquidAI/d1-2B-GGUF) and [d1-Omni-2B GGUF](https://huggingface.co/LiquidAI/d1-Omni-2B-GGUF) | Authored cards document a restricted llama.cpp primitive set. Unsupported multi-label/extraction/box requests must remain unavailable. |
| S06 | Liquid AI, [MLX deployment guide](https://docs.liquid.ai/deployment/on-device/mlx) | MLX-VLM decision path and version floor; ordinary generation/chat path is not a decision adapter. |
| S07 | Ollama, [System One endpoint](https://docs.ollama.com/api/systemone) | Separate version/payload/modality limits; no video/streaming/tool controls. Usage varies by model/server, so zero output tokens is not protocol-wide. |
| S08 | Liquid AI, [ONNX deployment guide](https://docs.liquid.ai/deployment/on-device/onnx) | Reviewed material does not establish the requested d1 typed-head parity. Treat export as an unqualified spike. |
| S09 | Liquid AI, [d1-2B MLX 4-bit card](https://huggingface.co/LiquidAI/d1-2B-MLX-4bit) | Author-reported quantisation comparison shows changed answers/probabilities; motivates separate exact-tuple calibration, not a measured rcagent result. |
| S10 | TypeSafe, [confidence](https://docs.typesafe.ai/confidence) and [model jaggedness](https://docs.typesafe.ai/model-jaggedness) | Provider confidence semantics and documented failure modes are not a universal probability of correctness. |
| S11 | Liquid AI, [LFM Open License v1.0](https://www.liquid.ai/lfm-license) | A distinct licence with conditions, not the repository's Apache-2.0 licence. Pin actual terms and applicability; this proposal makes no organisational/commercial-use determination. |
| S12 | TypeSafe, [models](https://docs.typesafe.ai/models) | Current Jev variants and capabilities are version-specific. Use an exact model ID rather than a floating alias. |
| S13 | Cloudflare, [Clef release](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/) | Distinct decision-model family and hosted/open-weight options; optional comparative candidate only. |

The claimed latency advantage, cost reduction, empirical calibration, extraction fidelity and operational suitability remain hypotheses. No vendor leaderboard, warm-call table or source description is used as acceptance evidence for rcagent. Current documentation is rechecked when an implementation tuple is chosen.

## Encoder, linker and terminology evidence

| ID | Primary source | Bounded finding used in the proposal |
|---|---|---|
| S16 | GLiNER authors, [official repository](https://github.com/urchade/GLiNER) | Label-conditioned NER candidate. Code and selected checkpoint rights/architecture require separate admission. |
| S17 | Answer.AI, [ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base) | Encoder/masked-language backbone; task-specific head or checkpoint needed. |
| S18 | Microsoft, [DeBERTa-v3-base](https://huggingface.co/microsoft/deberta-v3-base) | Encoder backbone; not a complete clinical NER/linker by default. |
| S19 | Original authors, [Bio_ClinicalBERT](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT) | Clinical pretraining does not itself supply a task head or grant access to its training notes. |
| S20 | Cambridge authors, [SapBERT](https://huggingface.co/cambridgeltl/SapBERT-from-PubMedBERT-fulltext) | Biomedical-name embedding/retrieval candidate. Similarity does not establish assertion status or calibrated coding correctness. |
| S21 | Microsoft, [KRISSBERT](https://huggingface.co/microsoft/BiomedNLP-KRISSBERT-PubMed-UMLS-EL) | Contextual entity-linking approach; described mention-example distribution has UMLS/PubMed rights constraints. |
| S22 | CogStack, [current NLP repository](https://github.com/CogStack/cogstack-nlp) and [MedCAT entry point](https://github.com/CogStack/MedCAT) | Toolkit/modelpack reuse candidate. Current and historical licence descriptions differ; inspect the actual selected revision/LICENSE, modelpack and terminology independently. |
| S23 | WHO, [ICPS conceptual framework](https://www.who.int/publications-detail-redirect/WHO-IER-PSP-2010.2) | WHO describes the framework as an information model rather than a classification. A local code profile needs its own explicit mapping/version. |
| S26 | Australian Digital Health Agency, [NCTS licensing](https://implementer.digitalhealth.gov.au/ncts/licensing) | Record selected SNOMED CT-AU/terminology access and redistribution terms; do not assume unrestricted distribution from local access. |
| S27 | IHACPA, [ICD-10-AM/ACHI/ACS](https://www.ihacpa.gov.au/health-care/classification/icd-10-amachiacs) and [products and licences](https://www.ihacpa.gov.au/health-care/products-and-licenses) | Distinct Australian classification/edition and licence choices; no automatic equivalence with ICD-10 or SNOMED CT. |
| S28 | US National Library of Medicine, [UMLS licence](https://www.nlm.nih.gov/research/umls/license.html) | UMLS/source-vocabulary conditions are admitted separately from a model/code licence. |
| S29 | FAA, [original HFACS report record](https://www.faa.gov/data_research/research/med_humanfacs/oamtechreports/2000s/2000/0007) | Source for the framework, not evidence that a local healthcare adaptation or automated causal/culpability tag is validated. |

## Evaluation and dependency reuse evidence

| ID | Primary source | Bounded use and limit |
|---|---|---|
| S14 | NVIDIA, [When2Call](https://github.com/NVIDIA/When2Call); authors' [NAACL paper](https://aclanthology.org/2025.naacl-long.174/) | Tool/clarification decision benchmark inspiration; not an installed agent controller or an incident-safety benchmark. |
| S15 | Artificial Analysis, [Decision Index methodology](https://artificialanalysis.ai/methodology/decision-index) and [AA-Symmetry](https://artificialanalysis.ai/evaluations/aa-symmetry) | Probability-sensitive and invariance methodology. AA-Symmetry is private: author original equivalents, do not claim official reproduction. |
| S24 | scikit-learn, [calibration](https://scikit-learn.org/stable/modules/calibration.html) and [GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) | Maintained metrics/calibration/group splitting. Brier is not solely a calibration measure; preserve group isolation and calibration-data separation. |
| S25 | UK AI Security Institute, [Inspect custom scorers](https://inspect.aisi.org.uk/custom-scorers.html) and [scoring policy](https://inspect.aisi.org.uk/scoring-policy.html) | Reuse task/solver/scorer orchestration where appropriate; preserve model versus grader/infrastructure failures and original structured probabilities. |
| S30 | Guo et al., [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html), ICML 2017 | Calibration/temperature-scaling methodology; no assertion that one method fits every multi-label or shifted clinical task. |
| S31 | Geifman and El-Yaniv, [SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html), ICML 2019 | Risk/coverage methodology; adoption of this particular architecture is not required. |
| S32 | SciPy, [binomial proportion intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) | Maintained exact/Wilson interval machinery. Case clustering and sample design still determine appropriate inference. |
| S33 | Original authors, [MedMentions](https://github.com/chanzuckerberg/MedMentions) | Optional public biomedical-linking comparator; pin dataset/terminology versions and rights. It does not validate Australian incident coding. |
| S34 | Haas et al., [Ranked Probability Score for ordinal classification](https://proceedings.mlr.press/v337/haas26a.html), UAI 2026 | Primary methodological discussion of cumulative ordinal scoring; this plan does not adopt its conformal method or claim its guarantees for incident tasks. |

## Repository evidence and freshness

Repository observations are pinned to `37ca41fa2e7eeee8cc79e24efd5d7c0f915269f3`; see [the baseline tree](https://github.com/edithatogo/rcagent/tree/37ca41fa2e7eeee8cc79e24efd5d7c0f915269f3). The specification gives exact inspected paths and symbols. Preflight observed these open owner branches:

| Work | Observed head | Meaning |
|---|---|---|
| AcciMap PR #141 | `dc42b2e5660c5070db0b1b48b5a83fd17f54425e` | Separate owned implementation; not imported into this proposal. |
| HEAPS PR #142 | `58fb0b15171322f70ee070cea6756f32fe792f50` | Separate owned interface checkpoint; no duplicate code or approval contract. |
| Shared recommendations PR #143 | `ff82e1a41283a500e579f5ef83e96b2802dd3e2e` | Shared roadmap/registry proposal; coordinator reconciles the additive entry here. |

No open issue matching the exact phrase “decision models” was returned in the preflight search. Existing local-model planning already mentions d1: this track expands that candidate/contract analysis while preserving Track 12's scientific ownership. It does not infer absence of all relevant work from the search result alone.

At DM01, recheck source availability and current owner state. Record changed/unavailable sources and do not reuse stale evidence as if newly verified. Sensitive source material, model weights, training corpora and restricted terminology were not downloaded for this plan.
