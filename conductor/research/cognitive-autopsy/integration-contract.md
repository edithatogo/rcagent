# Repository and dataset integration contract

## Ownership and fit-gap decision

| Repository or service | System of record | Small extension proposed |
| --- | --- | --- |
| rcagent | Component contracts, local inference/evaluation adapters, qualification and privacy evidence | Cognitive decision records, temporal packet controls, component scorer/admission adapter and optional scheduling broker |
| learningfromharm | HDC research protocol, sampling, analytic methods, interpretation and manuscripts | Cognitive-autopsy protocol addendum, patient-centred outcomes, grouped splits, analysis/reproducibility |
| corpus-cases-medilegal-nz | Canonical source documents, source metadata and publication receipts | Exact HDC snapshot inventory, source/appraisal span contracts and downstream lineage manifest |
| nlp-policy-nz | Shared extraction/normalisation library | Reusable preservation of spans, event/document times and document sections when a generic gap is demonstrated |
| archive-govt-nz | Source preservation and capture receipts | Reuse authoritative capture provenance; do not build a second archive |
| atlas-health-policy-anz / SourceRight | Policy/source provenance candidates | Time- and jurisdiction-bound reference lookup; applicability remains explicit |
| Hugging Face source corpus | Versioned distribution surface for permitted source artefacts | Pin commit/config/split/files and checksums; no mutable-main benchmark |
| Proposed Hugging Face derived dataset | Research annotations and split/packet metadata, if released | Candidate name edithatogo/hdc-cognitive-autopsy; creation and payload release are not performed by this plan |

Reuse existing maintained runtimes, JSON Schema, lexical retrieval, provenance and benchmark machinery. Assess Inspect AI as a thin local evaluation adapter; keep canonical receipts independent of it. No new framework, trainer or cloud service is installed by the planning change. A replacement must preserve receipts and exact input/output semantics.

## Source and derived records

The source layer records case/report ID, source URL, source authority, decision/publication date, retrieval timestamp, document hash, source revision, extraction version, rights/access state, text coordinates and uncertainty. Keep actual source decisions unchanged.

The derived layer records parent source revision/hash, source-span IDs, decision episode, event/document/availability times, rationale provenance, packet tier, split group, transformation/prompt/model version, annotator class, adjudication status and uncertainty. It must be possible to reconstruct each derived field's provenance or mark it unsupported.

The existing nlp-policy-nz HDC source profile separates official findings from project classifications and prohibits autopsy scores or clinical-truth claims as source outputs. Cognitive-autopsy annotations belong in the research layer; renaming a prohibited source field does not remove that boundary.

No patient-level case content is required in Conductor, GitHub issues, cloud agents or hosted CI. Public code uses synthetic placeholders. Private study stores hold mappings, approval details and sensitive receipts.

## HDC snapshot reconciliation

The owner confirms the HDC corpus and ethics approval are available. The exact approved snapshot, including any private/gated Hugging Face revision, still needs a machine-verifiable inventory. The public release tree inspected during planning was insufficient to establish the full HDC case payload. This is a technical location/version task, not evidence that the corpus or ethics approval is absent.

Verify actual files and records, not README examples, source counts or aggregate tables. Existing HDC text in learningfromharm and seven historical HDC-derived cases in rcagent are useful orientation, but their mere presence does not establish the size or quality of the new study. Source-specific coronial fixture corrections do not invalidate HDC as a whole.

## Hugging Face research lifecycle

1. Pin the source dataset's immutable revision and manifest; retain authorised local copies.
2. Build derived records locally and version the schema. Separate source evidence, model outputs and adjudicated annotations.
3. Publish only code/schema/citation metadata by default. Any case text, excerpts, embeddings, annotations or weights must meet its specific existing authority and rights scope.
4. Keep test answer material sealed or access-controlled during evaluation. A public A/B/C dataset may support reproduction after release, but publication makes future contamination more likely.
5. Record dataset card, collection purpose, selection/annotation methods, split definitions, provenance, known bias, licences, permitted use, change history and takedown/version replacement path. Register a released derivative through dataset-estate-registry.
6. Pin model cards and training lineage if an adapter is eventually released; a GitHub commit is not a model-release receipt.

Restricted PhysioNet records cannot be copied to a public Hugging Face dataset. Other data supplements are optional transfers, not hard dependencies for the approved HDC study. Their primary citations and licence caveats are in [dataset citations](./dataset-citations.md).

## Version negotiation and failure behaviour

Contracts start at cognitive-autopsy study schema 0.1.0, explicitly planning-only. An implementation must validate a declared supported version; unknown versions fail closed. A missing source span, unavailable packet, unsupported runtime or stale qualification yields a typed unavailable/abstain result, never a fabricated value.

Integration order is source snapshot contract, research sampling/packet contract, local component execution, then composition. The three repository tracks can prepare independently against these contracts; none may claim end-to-end validation before consuming actual receipts from the others.

## Additional consumer boundaries

The [verification/reuse map](./verification-and-reuse.md) records inspected sibling repositories and their current limits. Prefer upstream Rust4PM with an optional Propel inspection surface, existing spaCy/medspaCy and scikit-learn baselines, existing JSON Schema/SQLite contracts, and SourceRight/Searchright through their published boundaries. Keep policy interchange, evidence acquisition, simulation and clinical decision interpretation separate.

Derived event logs preserve source spans, object relationships and temporal uncertainty; XES/OCEL2 exports declare any representational loss. Mutation and synthetic-case ledgers record parent family/hash, allowed edits, invariants, oracle access and generator identity. The canonical corpus never overwrites original reports with a variant. External dataset cards retain source-specific citation, access, licence, version and redistribution state.

No new shared library is needed for the initial programme. Generic gaps should be implemented in their existing owner after a demonstrated consumer fixture; clinical-specific invariants remain in rcagent. An archived careops-process repository or a process-mappings scaffold is not a production dependency.
