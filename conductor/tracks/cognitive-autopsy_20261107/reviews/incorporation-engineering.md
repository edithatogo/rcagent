# Engineering and evidence-integrity cross-review — 2026-11-08

## Scope and reviewer limits

Reviewer: `/root/verification_owners`, reviewing the rcagent incorporation delta, learningfromharm/corpus coordination changes and nlp-policy-nz source-fidelity plan. The reviewer authored the separate SourceRight/SearchRight owner notes and has inherited programme context; this is a same-session cross-review, not a blinded/fresh-context, independent-model, human or clinical review. Exact serving model revision is not exposed. The SourceRight/SearchRight changes are outside this cross-review's acceptance scope.

Inspected diffs and current files against rcagent `0c8607661e64a34b351b87ca1c6148d0e291fbed`, learningfromharm `a9c5bdba7018ca5c71e460bbc2f6db9a43dfe71b`, corpus `06fcf44987a783a0883e1867da0c4231d2ad7f0d` and nlp-policy-nz `e2940f045ad2e065ef2b406843db10c7e850f0f6`. Exact reviewed file-byte hashes follow. No runtime tests, external literature search, model runs or data processing were repeated during this review.

## Findings and disposition

**No blocking design, ownership or false-completion finding in the reviewed delta.**

- Capture/fixity, neutral extraction, dataset identity/distribution, research labels and clinical interpretation are consistently assigned to their existing owners. Correcting the corpus repository's active status does not transfer processing authority or migrate its legacy runtime.
- Canonical source records remain separate from derived variants, attribution candidates, clinical hypotheses and research references. Raw capture and text-rendition digests/coordinate mappings are distinct. Delivery/receipt is not promoted into reading or knowledge.
- SourceRight/SearchRight, medspaCy, external datasets, process engines, simulation, tuning and VOI remain optional for the first rules/local-FTS5 HDC study. NLP-CA04 is not a hard dependency of later source-fidelity leaves.
- CAW09 permits source-linked HDC/synthetic labels before optional external NLI resources; CS08 now uses supported improvement at fixed evidence budget. The research split language separates training, development and calibration from a sealed holdout.
- Added planning markers are explicitly limited to planning/delivery. The experiment catalogue remains non-executable, implementation leaves remain open, and neither data admission nor qualification/release is inferred.
- The selected_system field names existing rcagent infrastructure without qualifying external candidates. A null unresolved approval_reference plus an explicit pending-link status avoids treating placeholder prose as evidence while preserving the owner's confirmed HDC ethics.
- `_locked` has a bare yield; `Generator[None, None, None]` is consistent with it and no locking, exception, state or filesystem behaviour was changed. No residual Iterator annotation remains in that file.
- Local relative links and existing dependency declarations were inspected alongside author receipts; primary external links are planning/source references, not new evidence of live compatibility. Journal scope links do not imply acceptance probabilities.

The review also caught a CAW10 dispatch mismatch in the reviewer's own separate owner notes; it was reported, corrected and handed to the other reviewer for closure. CAW10 is temporal entitlement, not contradictory retrieval. That correction is not self-issued independent acceptance of those notes.

## Delivery follow-through

The currently saved ca3 change/validation manifest predates these inspected additions: `conductor/research/cognitive-autopsy/verification-and-reuse.md`, `evaluation/cognitive-autopsy/study-design.json`. Root must regenerate the final manifest/validation at the final source freeze before comparing remote blobs; the old counts are not a complete delivery receipt. This is a delivery bookkeeping requirement, not a new research or approval gate.

Author command receipts were inspected, not represented as fresh executions by this reviewer. This review is bounded to the following source bytes and does not certify later source changes, runtime integration or clinical capability.

## Reviewed bytes

| Repository | Path | SHA-256 |
| --- | --- | --- |
| rcagent | `conductor/context-packs/cognitive-autopsy.md` | `59bbd1f47444edc523209fd36f6ed1021e75670111a78ccd0f33d0497bd0b55c` |
| rcagent | `conductor/integration-map.json` | `a41c20d44ea01852b49cd98c0af5e76877b2393997cdc2ac9b5ceb24eb3e047e` |
| rcagent | `conductor/research/cognitive-autopsy/integration-contract.md` | `d3c1448d4a3afef333aa59905ddf4942c9241df7ce4f832cbb21cd04477d1d3f` |
| rcagent | `conductor/research/cognitive-autopsy/programme.md` | `745ace8f788c5eb69706376eec8f9471df1a7ae27f882206c3bb0912d60d8f51` |
| rcagent | `conductor/research/cognitive-autopsy/verification-and-reuse.md` | `65c89c241e6953fa997440377c15e2ad8c07acf9ab94fb8603194aedabc6f713` |
| rcagent | `conductor/tracks/cognitive-autopsy_20261107/incorporation-map.md` | `7b169d3f450d0fdfd2f22431dd387faa185b6e9f64ed6b916d0a36e218f37df4` |
| rcagent | `conductor/tracks/cognitive-autopsy_20261107/index.md` | `7304c9a4f71a5eb689bbbfd5a05ec428bf0a1ba1b393b4cc966736ef30d2ad37` |
| rcagent | `conductor/tracks/cognitive-autopsy_20261107/plan.md` | `ddc66dbfe3f4b50e6918be304e8af9105ab85bcf773dbd285a1a7b4c47dd637e` |
| rcagent | `conductor/tracks/cognitive-autopsy_20261107/work-packages.md` | `12baa5ba77d9ec08e55316535cd4c49794058e46c8df6e0e2194c7f69735d3dc` |
| rcagent | `evaluation/cognitive-autopsy/experiment-catalogue.json` | `bb9530cb43b2ef5969f6e7ebfd8826e99cf77d6ceb2c247a5c34f322a4ccf4e4` |
| rcagent | `evaluation/cognitive-autopsy/study-design.json` | `834f184b1df1ea20c38555d3f079f5a8638712a1138978cdd5807333e1a8250f` |
| rcagent | `tools/autonomy_state.py` | `17888356468ee202d34f0b54283f2e0af3e0e4c3d2f88b5f225465c93a9627d3` |
| learningfromharm | `conductor/index.md` | `332be8ad1e9d4e6fcea836e0b2c1ffeb7b78fadc0a880db45b43f6516bb86d69` |
| learningfromharm | `conductor/tracks/cognitive_autopsy_20261107/plan.md` | `2672f57675f8a821b400b013a08d8a74d0bfd60020ad50a000cdac9b0c645cdd` |
| learningfromharm | `conductor/tracks/cognitive_autopsy_20261107/spec.md` | `a72076605d2319bfd8fefa5b58a5497dd32ed6cd619743c06efbabb6dfe9ecb2` |
| learningfromharm | `docs/COGNITIVE_AUTOPSY_COMPONENT_STUDIES.md` | `7a56a9817bdd3a2f86e8eabc1c7b1903044e44fd40d95e04d5e9a0c6c899f796` |
| learningfromharm | `docs/COGNITIVE_AUTOPSY_PROTOCOL.md` | `4f82cc508c3a3ee18bc9335435f91c52a076e98e59425006ddc9250559ed6ddd` |
| corpus-cases-medilegal-nz | `conductor/index.md` | `6ce9f90e80c2933ce08e2ca54fe6552f3a1ed10195acf2edb6b8c3e21e6d39b3` |
| corpus-cases-medilegal-nz | `conductor/tracks/cognitive_autopsy_source_integration_20261107/plan.md` | `d66cda9c2cccfe4103e1e485d197a121dbdf693ef265ce93854455a80ed5c104` |
| corpus-cases-medilegal-nz | `conductor/tracks/cognitive_autopsy_source_integration_20261107/spec.md` | `a7a2087fe3861ae14126b763f80ea2ea47addb87576676b0c01f3526f89de93a` |
| corpus-cases-medilegal-nz | `docs/cognitive-autopsy-source-contract.md` | `31d144b25f8e56db6a2cd3d8f22f514c7c85af9ce966eb9c3af4c868fae852b7` |
| nlp-policy-nz | `conductor/design.md` | `6f931321423844c2ff6e1ab5d5424959c6829a8b77da802aab457396a105d03e` |
| nlp-policy-nz | `conductor/index.md` | `cf36055ba51d5902f2576f97da3cb9cd21ae87c0d9b973c532b49036a430517d` |
| nlp-policy-nz | `conductor/product.md` | `afbd66c7bd84a9c7066a70a5ed7c9e2d382b0b12898d063e141b256f5b43a04a` |
| nlp-policy-nz | `conductor/requirements.md` | `4578a799cf841b6b65ca984837e43ccc03153aea25131b0f60365cd845db5f3c` |
| nlp-policy-nz | `conductor/tech-stack.md` | `835553931d2309f0fe91c56520000732a1a1bb1f8e8785d59d161dc2727d0cee` |
| nlp-policy-nz | `conductor/tracks.md` | `b9d7ff93ad5d4b7c293938f491369725f93271b6b315c0909151770990aed75c` |
| nlp-policy-nz | `conductor/tracks/cognitive_autopsy_source_fidelity_20261108/index.md` | `798a802fe90fa5b67465d040f5848d03d2a5b5b1c29cb8161f56109785a303b6` |
| nlp-policy-nz | `conductor/tracks/cognitive_autopsy_source_fidelity_20261108/metadata.json` | `e7d01fac78fac8ebdc098e620701ca852247e0592f5bc3de1358090eea704920` |
| nlp-policy-nz | `conductor/tracks/cognitive_autopsy_source_fidelity_20261108/plan.md` | `e03fca8cfa31ed9e559ad3dd772dff13ac15f01f18dde4e0db46d3bf6cd3728d` |
| nlp-policy-nz | `conductor/tracks/cognitive_autopsy_source_fidelity_20261108/planning-evidence.md` | `2da094bf4d0175535a654d484f7bfb42f48141cd9b3b1921940a29048ca955ec` |
| nlp-policy-nz | `conductor/tracks/cognitive_autopsy_source_fidelity_20261108/spec.md` | `0f3358f0e930310f653a3630c43fcc1b7789c3eb69538c5d10337d941f81b1dc` |
| nlp-policy-nz | `docs/source-profiles/hdc-medico-legal-profile.md` | `6692711803dbd2d62f3f4b42be44d244a5588c1d2a20dbda80c29237602b0847` |
| nlp-policy-nz | `task_plan.md` | `85871013de1c281264bb10b091a611ea7efb0632fb91bdd6cf94de88c63cd544` |
