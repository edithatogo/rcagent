# Dataset register and citations

Verified primary landing pages and author repositories were reviewed on 2026-11-07. This register identifies candidates and citations, not downloaded/admitted datasets. Freeze exact versions, checksums, access and split manifests before use. The [BibTeX file](./datasets.bib) supplies reusable citations.

## Primary HDC research material

**Health and Disability Commissioner, New Zealand. Decisions.** [Official search](https://www.hdc.org.nz/decisions/search-decisions/). Cite each used report by its actual case identifier, title, decision date and authoritative URL in the private/source manifest. Use an access date and preserved source digest where no DOI exists.

The project mirror is [edithatogo/corpus-cases-medilegal-nz](https://huggingface.co/datasets/edithatogo/corpus-cases-medilegal-nz), with [source repository](https://github.com/edithatogo/corpus-cases-medilegal-nz). Cite the exact selected release/commit and any verified DOI assigned to that release. No dataset DOI, case count or immutable HDC revision is fabricated here. A software repository's MIT licence does not automatically license the underlying reports or every derivative.

The owner confirms existing ethics approval for HDC corpus research. HDC is the main cohort; the following datasets are optional transfer/robustness experiments and do not block that work.

## Supplementary datasets

| Resource and exact citation | Proposed role | Access, limitations and use decision |
| --- | --- | --- |
| **MedCaseReasoning.** Wu K, Wu E, Thapa R, Wei K, Zhang A, Suresh A, Tao JJ, Sun MW, Lozano A, Zou J. MedCaseReasoning: Evaluating and learning diagnostic reasoning from clinical case reports. 2025. [arXiv:2505.11733v2](https://arxiv.org/abs/2505.11733v2), [DOI 10.48550/arXiv.2505.11733](https://doi.org/10.48550/arXiv.2505.11733). [Dataset](https://huggingface.co/datasets/zou-lab/MedCaseReasoning); [author code](https://github.com/kevinwu23/Stanford-MedCaseReasoning). | Secondary reasoning/extraction comparison or candidate training source; 14,489 cases in the paper | Retrospective published case reports, not contemporaneous thought traces. Author repository declares dataset CC BY 4.0 while Hub metadata says MIT; resolve the exact data licence and parent-article rights before use/distribution. Pin paper/data versions; use the verified arXiv citation rather than invent conference pages. |
| **DiReCT.** Wang B, Chang J, Qian Y. MIMIC-IV-Ext-DiReCT, version 1.0.0. PhysioNet; 2025. [DOI 10.13026/yf96-kc87](https://doi.org/10.13026/yf96-kc87). [Primary landing page](https://physionet.org/content/mimic-iv-ext-direct/1.0.0/). | Diagnostic entailment/source-grounding transfer test; 511 notes and 25 disease categories | Restricted/credentialed resource with applicable training and data-use agreement. Diagnostic entailment annotations do not establish actual clinician cognition or NZ safety practice. Keep records and derivatives within permitted access. |
| **MIMIC-IV-Ext-SDBench.** Nori H, Daswani M, Kelly C, Lundberg S, Correia Ribeiro MT, Wilson M, Liu X. MIMIC-IV-Ext-SDBench: Sequential Diagnosis Benchmark Cases Derived from MIMIC-IV, version 1.0.0. PhysioNet; 2026. [DOI 10.13026/xdmx-ty42](https://doi.org/10.13026/xdmx-ty42). [Primary landing page](https://physionet.org/content/mimic-iv-ext-sdbench/1.0.0/). | Sequential information-acquisition transfer experiment; 488 cases: 163 train, 254 validation, 71 clinician-reviewed test | Credentialed access and data-use agreement; not a public-Hub redistribution source. Published test and validation have different curation roles. The original [SDBench gatekeeper](https://microsoft.github.io/sdbench/) may synthesise missing test results. Historical cognitive autopsy must return “not documented” instead; that adapted experiment is not equivalent to the original benchmark. |
| **DDXPlus.** Fansi Tchango A, Goel R, Wen Z, Martel J, Ghosn J. DDXPlus: A New Dataset For Automatic Medical Diagnosis. Advances in Neural Information Processing Systems. 2022;35:31306–31318. [Paper](https://papers.neurips.cc/paper_files/paper/2022/hash/cae73a974390c0edd95ae7aeae09139c-Abstract-Datasets_and_Benchmarks.html), [DOI 10.52202/068431-2270](https://doi.org/10.52202/068431-2270). [Official project](https://mila-iqia.github.io/ddxplus/); [English release DOI 10.6084/m9.figshare.22687585](https://doi.org/10.6084/m9.figshare.22687585). | Optional controlled sequential-questioning and differential-diagnosis stress test | Approximately 1.3 million synthetic patients, 49 pathologies and 223 evidences; CC BY stated by authors. The English dataset DOI is linked by the official project; the Figshare page was unavailable during this review, so its exact version/receipt remains to verify. Synthetic simulator performance is not clinical validation. |

## SDBench paper and MIMIC parent citations

If SDBench is used, also cite **Nori H and colleagues. Sequential diagnosis with language models. Science. 2026. [DOI 10.1126/science.aeh7930](https://doi.org/10.1126/science.aeh7930)**, as requested by the dataset landing page. NEJM educational cases are a distinct source with distinct rights; access to the MIMIC extension does not confer rights to that edition.

Preserve parent provenance and cite the exact datasets actually consumed:

| Parent dataset | Citation |
| --- | --- |
| MIMIC-IV v3.1 | Johnson A, Bulgarelli L, Pollard T, Gow B, Moody B, Horng S, Celi LA, Mark R. MIMIC-IV. PhysioNet; 2024. [DOI 10.13026/kpb9-mt58](https://doi.org/10.13026/kpb9-mt58). [Landing page](https://physionet.org/content/mimiciv/3.1/). |
| MIMIC-IV-ED v2.2 | Johnson A, Bulgarelli L, Pollard T, Celi LA, Mark R, Horng S. MIMIC-IV-ED. PhysioNet; 2023. [DOI 10.13026/5ntk-km72](https://doi.org/10.13026/5ntk-km72). [Landing page](https://physionet.org/content/mimic-iv-ed/2.2/). |
| MIMIC-IV-Note v2.2 | Johnson A, Pollard T, Horng S, Celi LA, Mark R. MIMIC-IV-Note: Deidentified free-text clinical notes. PhysioNet; 2023. [DOI 10.13026/1n74-ne17](https://doi.org/10.13026/1n74-ne17). [Landing page](https://physionet.org/content/mimic-iv-note/2.2/). |

MIMIC primary paper: Johnson AEW, Bulgarelli L, Shen L, et al. MIMIC-IV, a freely accessible electronic health record dataset. Scientific Data. 2023;10:1. [DOI 10.1038/s41597-022-01899-x](https://doi.org/10.1038/s41597-022-01899-x).

Current PhysioNet landing pages request the platform citation: Pollard T, Moody BE, Lehman LH, Gow BJ, Fernandes C, Xie C, Johnson A, Mark RG, Heldt T. PhysioNet as a global platform for biomedical research. Nature Health. 2026;1:792–795. [DOI 10.1038/s44360-026-00096-z](https://doi.org/10.1038/s44360-026-00096-z).

MIMIC/PhysioNet authority is separate from HDC ethics. Follow the relevant agreement and current guidance for derived models/datasets; do not place restricted records or derived weights on public Hugging Face by default.

## Manifest fields required for any dataset

Record citation key, authoritative URL, dataset ID/version/commit, retrieval date, file checksums, parent sources, licence/access state, permitted purpose, transformations, annotation provenance, patient/case-family split group, train/development/test role, leakage risks, exclusions and release restrictions. Unknown fields remain unknown until verified.

Keep benchmark answers and expert appraisals separate from model-visible evidence. Never count duplicated source reports, synthetic variants or repeated inference as additional independent patients.

## Component validation supplements

The [candidate component dataset register](./component-datasets.json) and [component bibliography](./component-references.bib) extend this source list. See [component studies](./component-studies.md) for assertion, temporal, entailment and error-detection datasets, and [process mining](./process-mining.md) for Sepsis and Hospital Billing logs.

These sources test specified components, not real clinician cognition or the causes of harm. Some are controlled-access; others have unresolved redistribution terms. Do not copy third-party Hugging Face licence tags into the canonical register without the original source terms. The approved HDC study proceeds independently of these optional data-access arrangements. No supplemental payload was downloaded or admitted by this planning update.
