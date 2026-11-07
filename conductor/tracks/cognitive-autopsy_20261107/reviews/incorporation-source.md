# Safety/privacy and source-ownership cross-review — 2026-11-08

## Reviewer and scope

- Reviewer role: `/root/source_owner`, agent safety/privacy and source-ownership cross-review. Exact serving model revision was not exposed.
- Context: the reviewer authored the adjacent nlp-policy-nz owner-local plan and proposed the shared source-ownership wording, but did not author these root rcagent/research/corpus edits. This was an existing-context cross-review, not fresh-context, blinded, independent-model, human or clinical validation.
- Instruction: read-only review of current rcagent documentation/catalogue deltas and learningfromharm/corpus documentation deltas against ca3-base, focusing on owner boundaries, recipient uncertainty, permitted views, existing HDC authority, release limits and accidental dependencies. Only this review receipt was written.
- Compared rcagent against HEAD `0c8607661e64a34b351b87ca1c6148d0e291fbed`; companions against the supplied local `ca3-base` snapshots. Read the unchanged verification/reuse contract for context. No remote calls, model execution or sensitive source reads were needed.
- A concurrent `tools/autonomy_state.py` change was visible in status but is outside this review. This receipt does not review or validate runtime code.

## Findings

No blocking safety/privacy or source-ownership finding in the reviewed planning delta.

1. **Minor — citation handoff points to an unmerged default-branch path.** `learningfromharm/docs/COGNITIVE_AUTOPSY_PROTOCOL.md:83` links dataset-citations.md and datasets.bib to rcagent/master. Both paths are absent at inspected default base `ae729dffd002c0a5b25fd3695b49378aff13e454`, confirmed with local `git cat-file -e`. Change those links to the coordinated branch or reviewed commit until merge. This is inherited prose adjacent to the revised source contract, rather than a new clinical/privacy error.
2. **Minor — pin the source-owner reference.** The existing NLP shared-core link in `rcagent/conductor/research/cognitive-autopsy/verification-and-reuse.md:63` uses `/main/`, although this audit inspected nlp-policy-nz/master at `e2940f045ad2e065ef2b406843db10c7e850f0f6`. Use that exact commit for the source reference. No claim is made here that a separate main branch cannot exist; the issue is matching the cited version to reviewed evidence.

## Confirmed boundaries

- Capture/fixity stays in archive-govt-nz; nlp-policy-nz owns neutral extraction/renditions/spans and uncertainty; the GitHub corpus owns source/distribution contracts and snapshot/release lineage; the existing HF identity remains the public normalised dataset surface.
- Research labels, grouped splits and analyses remain in learningfromharm. Decision-time views, clinical/RCA semantics, interpretation and qualification remain in rcagent. SourceRight transports evidence observations without converting them into truth; generic libraries receive opaque consumer view identifiers.
- Explicit recipient/time statements can be extracted without declaring a clinician knew the information. The retained verification contract binds all stages to the same permitted source spans, cutoff and recipient scope; unknown availability remains unknown.
- Source records, official findings, interpretations and altered/synthetic cases remain separate. A faithful account is not made true merely by source linkage.
- Existing HDC ethics is accepted. Exact payload/revision inventory remains a technical requirement, not a request to renew ethics or prove the corpus exists. External dataset access is optional.
- CAW09 now accepts source-linked HDC/synthetic labels; the first deterministic studies do not acquire a required NLI dataset, SourceRight/SearchRight migration, process engine, simulation framework, fine-tuning, VOI or Paignia dependency.
- The source/HF lifecycle permits only artefacts within existing authority and rights; the plans do not grant a new public-data/model release, clinical deployment, participant recruitment or sensitive cloud transfer.
- Training, development and calibration roles are separated in the research addendum; CS08 names improvement at a fixed evidence budget. These changes do not fabricate qualification or patient-benefit evidence.

## Disposition and limits

Recommended disposition: proceed with the planning integration after the two small citation-reference corrections. No new governance or permission checkpoint is needed for those fixes. Re-review materially changed ownership/privacy semantics; mechanical link/receipt updates can receive a bounded closure check.

This is a review of written requirements and task boundaries, not proof that an implementation enforces them. No runtime privacy, clinical validity, empirical model quality or production readiness conclusion is supported.

## Reviewed content hashes

| Path | SHA-256 |
| --- | --- |
| `rcagent/conductor/context-packs/cognitive-autopsy.md` | `59bbd1f47444edc523209fd36f6ed1021e75670111a78ccd0f33d0497bd0b55c` |
| `rcagent/conductor/integration-map.json` | `991c237aac08121060faef0485548d9aa841369086a0b79513378ba7f47afcb1` |
| `rcagent/conductor/research/cognitive-autopsy/integration-contract.md` | `d3c1448d4a3afef333aa59905ddf4942c9241df7ce4f832cbb21cd04477d1d3f` |
| `rcagent/conductor/research/cognitive-autopsy/programme.md` | `745ace8f788c5eb69706376eec8f9471df1a7ae27f882206c3bb0912d60d8f51` |
| `rcagent/conductor/tracks/cognitive-autopsy_20261107/index.md` | `7304c9a4f71a5eb689bbbfd5a05ec428bf0a1ba1b393b4cc966736ef30d2ad37` |
| `rcagent/conductor/tracks/cognitive-autopsy_20261107/work-packages.md` | `12baa5ba77d9ec08e55316535cd4c49794058e46c8df6e0e2194c7f69735d3dc` |
| `rcagent/evaluation/cognitive-autopsy/experiment-catalogue.json` | `bb9530cb43b2ef5969f6e7ebfd8826e99cf77d6ceb2c247a5c34f322a4ccf4e4` |
| `rcagent/conductor/tracks/cognitive-autopsy_20261107/incorporation-map.md` | `7b169d3f450d0fdfd2f22431dd387faa185b6e9f64ed6b916d0a36e218f37df4` |
| `learningfromharm/conductor/index.md` | `332be8ad1e9d4e6fcea836e0b2c1ffeb7b78fadc0a880db45b43f6516bb86d69` |
| `learningfromharm/conductor/tracks/cognitive_autopsy_20261107/spec.md` | `a72076605d2319bfd8fefa5b58a5497dd32ed6cd619743c06efbabb6dfe9ecb2` |
| `learningfromharm/docs/COGNITIVE_AUTOPSY_COMPONENT_STUDIES.md` | `7a56a9817bdd3a2f86e8eabc1c7b1903044e44fd40d95e04d5e9a0c6c899f796` |
| `learningfromharm/docs/COGNITIVE_AUTOPSY_PROTOCOL.md` | `4f82cc508c3a3ee18bc9335435f91c52a076e98e59425006ddc9250559ed6ddd` |
| `corpus-cases-medilegal-nz/conductor/index.md` | `6ce9f90e80c2933ce08e2ca54fe6552f3a1ed10195acf2edb6b8c3e21e6d39b3` |
| `corpus-cases-medilegal-nz/conductor/tracks/cognitive_autopsy_source_integration_20261107/spec.md` | `a7a2087fe3861ae14126b763f80ea2ea47addb87576676b0c01f3526f89de93a` |
| `corpus-cases-medilegal-nz/docs/cognitive-autopsy-source-contract.md` | `31d144b25f8e56db6a2cd3d8f22f514c7c85af9ce966eb9c3af4c868fae852b7` |
| `rcagent/conductor/research/cognitive-autopsy/verification-and-reuse.md` | `65c89c241e6953fa997440377c15e2ad8c07acf9ab94fb8603194aedabc6f713` |

## Bounded closure and final-field check — 2026-11-08

- Finding 1 closed: both learningfromharm citation references now use the coordinated cognitive-autopsy branch. Exact link strings checked locally; no live-URL availability test is claimed.
- Finding 2 closed: the NLP README source reference now pins the inspected commit `e2940f045ad2e065ef2b406843db10c7e850f0f6`.
- Additional integration-map check: `selected_system` explicitly names existing rcagent contracts; the track remains `assess`, and external candidates remain unselected/unqualified. This selects an implementation starting point, not a clinical capability.
- Additional study-design check: `approval_reference` is JSON null with `pending_link_to_protected_study_register`; `hdc_ethics` remains `existing_approval_confirmed_by_owner`, `scope_extension_implied` remains false, and the study remains planning-only/non-executable. The edit distinguishes a missing protected record link from absent ethics and cannot be mistaken for a fabricated approval identifier.
- Additional workflow check: routine reversible repository/fixture/metadata work continues without repeated approval. Exact input scope and tested local privacy remain execution prerequisites. Missing inputs produce an unavailable run rather than a renewed ethics request. Reserved actions are considered only when needed and not already covered by existing authority; no blanket new human-approval gate was introduced.

**Closure disposition:** both minor findings are closed; no remaining blocking safety/privacy or ownership finding within this bounded documentation review. The additional fields preserve scope and existing authority. Prior independence and runtime/clinical-validation limitations still apply. Only the review receipt was edited.

| Closure-reviewed file | SHA-256 |
| --- | --- |
| `learningfromharm/docs/COGNITIVE_AUTOPSY_PROTOCOL.md` | `4f82cc508c3a3ee18bc9335435f91c52a076e98e59425006ddc9250559ed6ddd` |
| `rcagent/conductor/research/cognitive-autopsy/verification-and-reuse.md` | `65c89c241e6953fa997440377c15e2ad8c07acf9ab94fb8603194aedabc6f713` |
| `rcagent/conductor/integration-map.json` | `a41c20d44ea01852b49cd98c0af5e76877b2393997cdc2ac9b5ceb24eb3e047e` |
| `rcagent/evaluation/cognitive-autopsy/study-design.json` | `834f184b1df1ea20c38555d3f079f5a8638712a1138978cdd5807333e1a8250f` |
| `learningfromharm/conductor/workflow.md` | `23a81cfe8c8fc2c6f430b2872ff0de895d48c7482a25a20b77c117e9f89afe89` |
