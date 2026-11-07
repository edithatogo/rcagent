# Recommendation incorporation and owner handoffs

Reconciled on 2026-11-08 after the owner requested incorporation into the relevant repositories. This is a navigation and ownership map for the existing programme, not a second task register. CAW01–CAW25 and CS01–CS08 remain the execution identifiers; implementation, study results and qualification remain pending.

## Recommendation coverage

| Accepted recommendation | Canonical plan | Existing execution owner |
| --- | --- | --- |
| Use the already authorised HDC corpus and preserve exact source lineage | [Source integration](../../research/cognitive-autopsy/integration-contract.md) | CAW01–03; corpus source track and nlp-policy-nz extraction track |
| Start with assertion/account attribution, verification and availability | [Component studies](../../research/cognitive-autopsy/component-studies.md) | CS01–03; CAW02–12 and CAW20–22 |
| Compare rules, classical NLP, optional encoders and untuned local LLMs fairly | [Work packages](./work-packages.md) | CAW03–07; research labels and splits in learningfromharm |
| Record external dataset citations, access, versions and limitations | [Candidate register](../../research/cognitive-autopsy/component-datasets.json), [bibliography](../../research/cognitive-autopsy/component-references.bib) | CAW01; supplementary access does not block the HDC/synthetic path |
| Test outcome, availability and equivalent framing with controlled variants | [Controlled experiments](../../research/cognitive-autopsy/controlled-experiments.md) | CAW10–13; CS03–04 |
| Use generated cases with a separate hidden reference and checked rendering | [Controlled experiments](../../research/cognitive-autopsy/controlled-experiments.md) | CAW14–15; CS05, optional |
| Reuse process mining and measure extraction/uncertainty propagation | [Process plan](../../research/cognitive-autopsy/process-mining.md) | CAW16–19; CS06, optional |
| Verify sources, semantic support, permitted evidence and omissions separately | [Verification and reuse](../../research/cognitive-autopsy/verification-and-reuse.md) | CAW08–10 and CAW20–21; generic owner handoffs below |
| Preserve patient/family concerns and evaluate quality before time/cost | [Evaluation design](../../research/cognitive-autopsy/evaluation-design.md) | CAW20–22; learningfromharm rubric and analysis |
| Keep sensitive execution local; test any optional cloud control plane | [Privacy architecture](../../research/cognitive-autopsy/hybrid-privacy.md) | Existing Phase 2 privacy gate and optional Phase 5 composition/broker |
| Fine-tune only for demonstrated incremental value | [Model selection](../../research/cognitive-autopsy/model-selection.md) | CAW23; CS07, conditional |
| Model the value of missing evidence only with explicit assumptions | [Controlled experiments](../../research/cognitive-autopsy/controlled-experiments.md) | CAW24; CS08, conditional; improvement at fixed evidence budget with burden separate |
| Use maintained dependencies and remove redundant generic code after parity | [Reuse decisions](../../research/cognitive-autopsy/verification-and-reuse.md) | Existing owning CAW adapter task; no new generic engine |
| Minimise human effort, preserve required observations and target one coherent paper | [Programme/publication plan](../../research/cognitive-autopsy/programme.md) | CAW22/25 and learningfromharm; coding-agent schedule is effort, not elapsed clinical-study time |

## Owner boundaries

- **archive-govt-nz:** authoritative public-source capture, fixity, source-version relations and replay receipts. Consume the existing owner contract; this programme adds no competing archive.
- **nlp-policy-nz:** neutral extraction, raw/normalised offset mappings, extraction uncertainty and reusable source records. Explicitly documented time and recipient statements may be extracted with source spans; whether a person knew something remains a downstream interpretation.
- **corpus-cases-medilegal-nz on GitHub:** source/distribution contracts, snapshot/release metadata and source-to-research lineage. The active GitHub repository does not acquire capture/extraction authority by being active. The existing Hugging Face dataset retains the canonical public normalised dataset identity.
- **learningfromharm:** reference labels, case-family partitions, controlled-experiment interpretation, patient-relevant outcome analysis and manuscripts.
- **rcagent:** permitted decision-time views, clinical/RCA semantics, source-to-process projection, local execution, semantic admission, component qualification and report composition.
- **SourceRight:** generic source identity, citation/claim/span linkage and evidence-observation transport. A linked citation or a consumer-supplied verifier observation cannot become source truth. Consumer view identifiers are opaque; rcagent determines their clinical meaning.
- **SearchRight:** public literature search and generic evidence-search provenance. A sensitive rcagent case view must not reach remote scholarly providers through queries, retry/fallback, logs or derived text. Existing local case retrieval remains SQLite FTS5; no mandatory retrieval migration is planned.

The accompanying owner-local plans must preserve these boundaries and use synthetic consumer fixtures. HDC clinical labels do not become canonical extraction fields. Generic libraries must return unsupported/unavailable capability explicitly; their new plans are not evidence of implementation.

| Owner-local planning delivery | Existing or new owning track | Consumer dependency |
| --- | --- | --- |
| [SourceRight PR 133](https://github.com/edithatogo/sourceright/pull/133) | 110-scoped-evidence-consumers; completed Track 14 linkage baseline retained | Optional identity/span/observation adapter; CAW08/09/10/21 retain their distinct meanings |
| [SearchRight PR 759](https://github.com/edithatogo/searchright/pull/759) | Existing Track 13 Phase 3 consumer-contract work | Public-literature handoff and optional local evidence-view adapter; existing FTS5 path independent |
| [nlp-policy-nz PR 358](https://github.com/edithatogo/nlp-policy-nz/pull/358) | cognitive_autopsy_source_fidelity_20261108 | Neutral fidelity/export requirements consumed by CAW01–04/08/10; optional clinical adapter does not block required source work |

The local source-library seven-leaf plan refines its implementation ownership; it does not add seven duplicate completion counters to rcagent. PR state proves delivery state only. Runtime adoption still requires the exact consumer fixtures and receipts in the owning plan.

## Optional dependencies and parallel programmes

Rust4PM/Propel remain optional engine/inspection candidates behind CAW16–19. Use upstream algorithms after consumer fixtures, revision and licence checks; personal forks do not need new feature tracks merely because they are available. Uncertain-input conformance is separately qualified.

Voiage remains an optional numerical consumer for CAW24. The inspected main at `862d510f1cd0420d32c7b84734066ee6d6f291bb` already defines an [optional outcome boundary](https://github.com/edithatogo/voiage/blob/862d510f1cd0420d32c7b84734066ee6d6f291bb/conductor/tracks/simulation_outcome_boundary_20261107/spec.md): explicit alternatives, draw identity/coupling, value convention, units, perspective and provenance. rcagent/research supplies states, likelihoods, utilities and evidence-acquisition costs. Do not infer these from prose or turn agreement scores into utility. No duplicate VOI implementation or requirement for Paignia/strategic-information work enters CS01–03. Recheck the exact qualified Voiage method/profile when this optional experiment begins.

Kairos/careops-sim, policy interchange and Authentext stay behind their existing boundaries. Synthetic template worlds can be built without a simulation-engine dependency. No new upstream track or runtime migration is required until a concrete consumer fixture demonstrates a missing generic capability.

## Dispatch and evidence

Start the existing CAW01–03 contract/fixture lane and CAW08 exact-check preparation. Real HDC execution still requires its exact admitted snapshot and privacy evidence. SourceRight/SearchRight additions, external datasets, process engines, synthetic-world extensions, fine-tuning and VOI must not become accidental hard prerequisites for a useful deterministic HDC study.

Use the task graph for sequencing; study membership is not automatically a hard dependency. If the currently non-executable catalogue becomes a scheduler, encode optional tasks explicitly before dispatch rather than inferring them from titles. Preserve failures and abstentions in all denominators.

The incorporation review corrected four ambiguities: CS08 now names its fixed-budget endpoint; CAW09 has source-linked HDC/synthetic labels as an initial route; training vocabulary, development tuning and calibration partitions are distinct; and PLOS Digital Health is included in the coordinating publication table. These corrections do not change the eight-study/25-package scope or mark empirical work complete.
