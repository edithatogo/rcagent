# Verification, dependency reuse and repository boundaries

Status: proposed research/engineering design, 2026-11-07. No new verifier, dependency, model qualification or sensitive-data run is implemented by this document. The current evidence core, JSON Schema validation, SQLite FTS5 retrieval and SourceRight adapter remain the starting points.

## Verification is a set of bounded claims

A valid schema, genuine reference, matching quotation, supported paraphrase, sound interpretation and causal conclusion are different properties. Record each separately. A citation on the same line as a sentence does not establish that the source supports it. A source-grounded account can still be mistaken about the underlying event. Verification cannot guarantee zero hallucinations.

| Layer | Reuse and small project-specific extension | What a pass establishes; residual limitation |
| --- | --- | --- |
| Source identity | Existing corpus capture receipts, immutable source hashes and versioned extraction; source coordinates from nlp-policy-nz where admitted | The cited version and bytes exist; not that the source account is true |
| Output structure | Existing Draft 2020-12 JSON Schema validator, enums, local references and cross-ID checks | Required fields/types/references are valid; not semantic correctness |
| Exact evidence | UTF-8 source-byte slices or explicitly mapped normalized spans; deterministic quote, number/unit, actor-ID and date checks | Exact correspondence for the specified fields; normalization and context can still alter meaning |
| Temporal entitlement | Event/document/availability intervals, recipient and decision cutoff; maintained graph routines for precedence consistency | A claim uses permitted evidence if availability is established; unknown availability stays unknown |
| Semantic support | Calibrated local entailment/contradiction model or bounded critic over the claim AND complete relevant evidence | A measured, fallible support judgment; not proof or a substitute for source adjudication |
| Completeness and alternatives | Compare output to a source-derived critical-fact/concern inventory; retrieve opposing passages; retain conflicting accounts | Measured coverage and contradiction handling; precision alone can hide omissions |
| Report admission | Domain policy distinguishes documented fact, account, interpretation, hypothesis and unresolved issue; deterministic templates first | No unverified claim is silently promoted to a finding; source error and clinical interpretation remain possible |
| Privacy and execution | Existing local runtime/privacy ports; no-egress worker, offline schemas/models, data-independent scheduling | Tested technical boundary for a named configuration; no implicit permission for other configurations |

Offsets must declare their coordinate system and source revision. Do not compare character indexes to UTF-8 byte offsets. Preserve original bytes; any OCR/normalization mapping has a version and diagnostic. A failed or ambiguous match is unresolved, not automatically false.

Semantic inference uses three outcomes: supported, contradicted and insufficient/uncertain. Do not coerce every absent statement into contradiction or equate missing narrative evidence with omitted care. Scores from an NLI4CT binary task cannot be adopted as a calibrated three-way clinical verifier without separate evaluation.

## Proposed local flow

1. Admit immutable source and allowed packet view.
2. Run rules/statistical or local LLM extraction into typed candidate records with source spans.
3. Apply deterministic source, numeric, identity, compartment and temporal checks.
4. Apply a separately evaluated semantic verifier only to eligible candidates; it may abstain.
5. Retrieve contradictory evidence and check critical information/concern coverage.
6. Render admitted records, retaining visibly distinct accounts, hypotheses and unresolved issues.
7. Re-run claim extraction/verification after any free-form synthesis or style transformation.

Every stage is bound to the same immutable authorised packet/view: packet ID and hash, permitted source-span set, decision cutoff and recipient scope. Apply that binding to exact checks, semantic verification, contradictory retrieval, critical-inventory comparison, rendering and post-render checks as well as generation. Reject a valid source ID whose span is outside the view. A verifier must not fetch later outcome/appraisal evidence through a global source store, shared cache or unconstrained retrieval index. Other task views are separate executions with explicit scope, not silent evidence upgrades.

The critical-fact/concern inventory has a frozen version, source spans, permitted view, creator/reviewer class and adjudication status. Candidate-system output alone cannot be its sole performance reference. A reference constructed with later knowledge must not be used as decision-time truth without a separately justified, source-limited reference procedure.

Keep final prose factual to the admitted record. An optional LLM critic may flag issues or propose repairs; it cannot silently change source facts. Allow at most a predeclared bounded repair budget, retain every attempt, and send unresolved items to the research review queue. All-abstention is not a successful system.

## A small verifier experiment

Build a controlled challenge set from authorised source-linked items plus entirely synthetic fixtures. Preserve unmodified positive controls. Inject exactly specified errors: invented source ID; wrong source version; altered quotation; changed dose/unit or denominator; reversed polarity; wrong speaker/subject; later information presented as available; quoted text with contradictory surrounding context; invented rationale; or omitted patient concern.

Measure error-type recall, false rejection of valid items, positive predictive value, abstention, coverage, verifier latency and downstream material-error change. Keep verifier development, calibration and final test families separate. Evaluate the whole generator-plus-verifier system, not only detection accuracy. Test the generator's naturally occurring errors separately from injected errors; the latter distribution does not estimate real-world hallucination prevalence.

Use MEDEC-MS for additional error-detection stress tests and MedNLI/NLI4CT-P where admitted for semantic-support components; these are not RCA ground truth. Pin the corrected NLI4CT-P consistency evaluator and add independent tests that distinguish accuracy from paired invariance. See [component studies](./component-studies.md) and [controlled experiments](./controlled-experiments.md).

## Existing repository fit, observed 2026-11-07

| Repository | Observed useful surface | Proposed integration and boundary |
| --- | --- | --- |
| rcagent | evidence_core.py uses JSON Schema; retrieval_system.py uses SQLite FTS5 and explicitly labels claim-link-only grounding; SourceRight is behind a port | Own medical-safety decision semantics, packet access, component evaluation and report admission. Preserve the deliberate refusal to treat retrieval IDs as semantic proof. |
| nlp-policy-nz | Shared Rust-accelerated/Python NLP, spaCy, source profiles, Polars and versioned corpus output | Reuse source extraction/normalization and offsets. Decision scores and model hypotheses belong downstream, outside canonical HDC source records. |
| sourceright | CSL/reference integrity and claim/citation linkage; src/provenance.rs links citation occurrences to claim spans | Reuse source identity and bibliographic evidence. Current linkage is not quote/paraphrase entailment verification. Add a thin consumer contract before depending on new semantic capability. |
| searchright | Search/review orchestration, evidence-search-contracts/core, audit receipts and optional extraction adapters; technical alpha | Public literature search/update and reproducibility, with approved offline results imported locally. Never pass sensitive case text through scholarly provider queries. No immediate migration of local case retrieval is needed. |
| citeweft | Searchright documents a backend-neutral scholarly extraction boundary | Evaluate a source-span adapter only for supported document types; do not assume clinical PDF/OCR accuracy or replace existing ingestion without fixtures. |
| rust4pm / propel | Personal forks of upstream Rust4PM/Propel; upstream engine and local inspection components are documented | Prefer a qualified upstream release through a small adapter; compare fork divergence before pinning. Do not duplicate discovery/alignment algorithms. Hosted demos are not an admitted sensitive-data runtime. |
| process-mappings / rac-conformance | Process profiles remain an incubator/scaffold; policy interchange and rules/process contracts exist separately | Reuse applicable contracts when implemented and tested. Do not present a scaffold as a clinical pathway or automatic standard-of-care oracle. |
| voiage | VOI methods with method-specific capability limits and Rust-owned kernels | Optional value-of-evidence experiments once states, utilities, likelihoods and costs are explicit. RCA supplies the decision model; Voiage does not infer it from narratives. |
| careops-sim / Kairos | Separate simulation programme and generic kernel; clinical model qualification remains distinct | Optional future mechanism-based synthetic worlds or intervention scenarios. Keep clinical pathways outside the generic kernel; a simulator result depends on its validated assumptions. |
| authentext | Existing optional writing skill integration | If used, transform only admitted report content and recheck factual invariants. Prose quality cannot certify clinical validity. |

Source inspection: [SourceRight provenance implementation](https://github.com/edithatogo/sourceright/blob/3a603ec8344e9865c68998d48eca573499d3fb5d/src/provenance.rs), [Searchright boundary](https://github.com/edithatogo/searchright/blob/main/README.md), [NLP shared core](https://github.com/edithatogo/nlp-policy-nz/blob/e2940f045ad2e065ef2b406843db10c7e850f0f6/README.md), [Rust4PM fork](https://github.com/edithatogo/rust4pm), [Propel fork](https://github.com/edithatogo/propel), [process profiles status](https://github.com/edithatogo/process-mappings/blob/main/README.md), [RaC contract](https://github.com/edithatogo/rac-conformance/blob/main/README.md), [Voiage capability matrix](https://github.com/edithatogo/voiage/blob/main/README.md), [CareOps Sim status](https://github.com/edithatogo/careops-sim/blob/main/README.md). Default-branch documentation can change; implementation must record exact candidate revisions and execute consumer fixtures. No downstream runtime acceptance was performed during this inspection.

## Dependency replacement decisions

| Need | Preferred reuse | Custom work retained / removal condition |
| --- | --- | --- |
| Negation, assertion, sections, lexical patterns | spaCy matchers and medspaCy ConText/section components (MIT), behind a local adapter | Domain rules and provenance mapping only; replace duplicate generic rule engines after matched-fixture parity |
| Classical classification and retrieval evaluation | scikit-learn pipelines, TF-IDF, regularised linear classifiers, grouped splits and calibration (BSD-3-Clause); existing SQLite FTS5 BM25 | HDC label mapping, source grouping and outcome definitions; avoid writing generic training/splitting/ranking engines |
| Structured contracts | Existing jsonschema dependency; local/vendored schema resolution | Cross-field clinical evidence invariants only; no second general-purpose schema validator |
| Process discovery / conformance | Upstream Rust4PM process_mining (MIT OR Apache-2.0), optional existing Propel components | Evidence-to-log mapping and clinical interpretation only; preserve unknown times outside algorithms requiring point timestamps |
| Comparator algorithms | Optional PM4Py (AGPL-3.0-or-later or commercial terms); PROVED replication comparator (GPL-3.0, older research software) | No default bundling or claim that subprocess isolation resolves licensing; use only a compatible, explicitly admitted profile |
| Graph consistency | Existing graph facilities or maintained petgraph in a Rust adapter | Domain-specific precedence/availability rules; no bespoke traversal/shortest-path library |
| Experiment/property checks | Existing benchmark ledger and test stack; Hypothesis/proptest where useful | Clinical mutation definitions and expected invariants, not a new evaluation platform |

These are reuse decisions for implementation, not package installation or licence selection for an incompatible distribution. Pin a compatible release at execution, record transitive licences/offline capability, test against the existing contract, then remove duplicated code. Keep a safe deterministic fallback. Do not replace working domain safeguards just because an upstream library has a similarly named feature.

Official documentation: [spaCy matching](https://spacy.io/usage/rule-based-matching), [medspaCy](https://github.com/medspacy/medspacy), [scikit-learn text pipelines](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html), [Rust4PM](https://rust4pm.aarkue.eu/docs/rust/), [PM4Py licence](https://github.com/process-intelligence-solutions/pm4py/blob/release/README.md), [PROVED](https://github.com/proved-py/proved-core), [petgraph cycle detection](https://docs.rs/petgraph/latest/petgraph/algo/fn.is_cyclic_directed.html).

## Rollout

First implement exact source/span and availability checks plus conventional baselines. Then measure semantic verification and its false-negative/false-positive trade-off. Add process adapters and active evidence acquisition only after their prerequisites pass. Keep shared dependencies optional until they demonstrate a needed capability. Apply the [bounded work packages](../../tracks/cognitive-autopsy_20261107/work-packages.md); document failures as results, without creating recurring human approval steps.
