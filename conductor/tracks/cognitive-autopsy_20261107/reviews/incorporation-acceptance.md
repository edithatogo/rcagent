# Cognitive-autopsy incorporation: acceptance and evidence cross-review

Date: 2026-11-08 (Australia/Brisbane). Reviewer: `/root/reconcile_core`.

## Scope and reviewer class

This is an existing-context agent acceptance/evidence cross-review, not blinded, fresh-context, independent-model or human clinical validation. The serving model revision is not exposed. The reviewer authored no planning changes under review. It separately authored the two-line `tools/autonomy_state.py` typing repair; that repair is excluded from any independent-review claim here and was accepted by the coordinating agent after its recorded tests.

The first audit covered the existing rcagent programme at `0c8607661e64a34b351b87ca1c6148d0e291fbed`, the learningfromharm files from `a9c5bdba7018ca5c71e460bbc2f6db9a43dfe71b`, and the corpus files from `06fcf44987a783a0883e1867da0c4231d2ad7f0d`. This follow-up checks closure of its four findings, the central incorporation map, and owner-local plans against these bases:

- nlp-policy-nz: `e2940f045ad2e065ef2b406843db10c7e850f0f6`.
- SourceRight: `3a603ec8344e9865c68998d48eca573499d3fb5d`.
- SearchRight: `4bfffc43e25641962fca394d43446888376156b4`.

The final review is bound to the file blobs listed below rather than an assumption that an uncommitted working tree or current branch head cannot change.

## Findings and closure

| ID | Finding | Closure evidence | Status |
| --- | --- | --- | --- |
| AC01 | CS08 question still suggested improvement per unit burden, inconsistent with its fixed-budget primary endpoint. | Catalogue question now names supported-accuracy improvement or material-error reduction at a fixed evidence budget; CAW24 retains separate burden reporting and explicit assumptions for formal VOI. | Closed |
| AC02 | CAW09 inputs could be read as requiring external NLI/error datasets despite the optional-access policy. | Work-package table and catalogue now permit source-linked HDC or synthetic support labels, with external NLI/error datasets optional. Reference quality and calibration requirements remain. | Closed |
| AC03 | Research prose conflated vocabulary fitting, development tuning and calibration. | learningfromharm addendum now assigns vocabulary/supervised fitting to training families, prompt/rule refinement to designated non-test development data and threshold calibration to its designated partition; final holdout stays sealed. | Closed |
| AC04 | Coordinating publication table omitted PLOS Digital Health despite the research addendum and recommendation. | Programme now includes a conditional PLOS Digital Health option and official journal-information link, without an acceptance probability or validation claim. | Closed |
| AC05 | Owner notes grouped CAW10 with contrary-evidence retrieval, creating a dispatch ambiguity. The owner identified this during cross-review and this reviewer concurred. | Revised SourceRight spec/plan and SearchRight consumer table distinguish CAW08 exact-source checks, CAW09 semantic support, CAW10 temporal entitlement and CAW21 combined evaluation. Contrary retrieval is explicitly a broader consumer requirement. Refreshed owner blob manifest and SearchRight source hashes match. | Closed |

No remaining blocking finding was identified in the reviewed planning scope.

## Acceptance observations

- The incorporation map preserves CS01–CS08 and CAW01–CAW25 as the existing execution identifiers. It is navigation/ownership context, not another task register. Optional SourceRight/SearchRight integrations, process engines, external datasets, synthetic-world extensions, fine-tuning and VOI do not block the initial HDC/synthetic path.
- nlp-policy-nz supplies neutral extraction, immutable text renditions, coordinate mappings, uncertainty and consumer-scoped export. Source capture remains with archive-govt-nz; corpus source/distribution metadata remains with corpus-cases-medilegal-nz; research labels/splits stay with learningfromharm; clinical information-state interpretation and qualification stay with rcagent. The correction of the older archived-corpus description does not authorise a second capture pipeline.
- All seven NLP runtime leaves remain pending. The optional clinical-adapter comparison is not a hard prerequisite for other leaves. The existing HDC YAML is unchanged. Runtime, lockfile, schema and source-payload changes are not claimed.
- SourceRight Track 110 carries neutral identity/span/binding checks and attributed optional support observations. It preserves canonical CSL, keeps observation verdicts distinct from execution state and factual truth, and leaves temporal/clinical meaning with the consumer. All seven implementation tasks remain unchecked.
- SearchRight extends the existing Track 13 consumer-contract work rather than creating a second hierarchy or changing its 200-assertion ledger. It separates public literature search from optional local case retrieval; default-deny, cache/view isolation and error/log/packaging boundaries remain explicit. No passport, dependency pin, executable schema, runtime support or compatibility promotion is asserted.
- Patient/family concerns, material errors and useful coverage remain primary; model runtime is not presented as observed clinician review time. Synthetic recovery, process conformance and agent ratings retain their stated evidence limits.

## Checks performed by this reviewer

- Original audit: 10 candidate datasets with none admitted; 43 unique bibliography keys; every candidate citation key resolved; eight unexecuted studies; 25 acyclic work packages with no missing hard-dependency IDs; empty qualified profiles.
- Closure inspection: exact corrected question/input/prose/publication fields and the final CAW08/09/10/21 owner mapping.
- nlp-policy-nz: independently checked all 13 changed planning files, parsed the metadata JSON, resolved 22 added/new relative Markdown links, verified seven acyclic leaves and no hard dependency on optional NLP-CA04, and compared the HDC YAML bytes with the base unchanged.
- SourceRight: all seven final file blobs match the author's refreshed freeze manifest; ten relative document links resolve; metadata status/evidence level remain planned; seven future tasks unchecked and none checked.
- SearchRight: all four final file blobs match the refreshed freeze manifest; five relative document links resolve; updated source-manifest entries match the changed source bytes.

The owner-agent reports and root delivery checks remain separately attributed. This review did not rerun full native suites, the strict clean-tree package gate, hosted CI, local model experiments or sensitive-data boundary tests. Those unrun gates are not converted into passes by document acceptance. No new research, model inference, data access, publication, commit or push was performed by this review.

## Reviewed content binding

The following map uses Git blob SHA-1 identity (`blob <length>\0<bytes>`). Its canonical JSON SHA-256 is `20db44f8b06a1a00d084d51821adb355f5422c25fc1d4bb869daf022f7c1df3b`.

```json
{
  "learningfromharm": {
    "docs/COGNITIVE_AUTOPSY_COMPONENT_STUDIES.md": "b4014467844ca5b93b1987d2dea6e13bc57a5f24"
  },
  "nlp-policy-nz": {
    "conductor/design.md": "e549a27d0de85d84f85845f09f46b45ecd4aa180",
    "conductor/index.md": "ae3ec958814237162db57ce5b964c3159d053089",
    "conductor/product.md": "a9f741d7fafe9f4256f231118907374b16bdad1b",
    "conductor/requirements.md": "2ddec5d9a58f2d924bbbb49aa4881c6fddb080e9",
    "conductor/tech-stack.md": "44f84c87fffd3be162d4b8cf1d629f7aa43210cb",
    "conductor/tracks.md": "619b70ed3cf18a3c6a5581b90b5662c5e221d643",
    "conductor/tracks/cognitive_autopsy_source_fidelity_20261108/index.md": "83be2615b101fb5b1b594cc0741f9baf4fe78856",
    "conductor/tracks/cognitive_autopsy_source_fidelity_20261108/metadata.json": "d872934f61acbedb4100406f701ecaa5cc1f7836",
    "conductor/tracks/cognitive_autopsy_source_fidelity_20261108/plan.md": "002e242f229585f8acb7efb6264250d4ce3c6b15",
    "conductor/tracks/cognitive_autopsy_source_fidelity_20261108/planning-evidence.md": "57a0dfbce12c3f33e6170577a9d00042469cb07f",
    "conductor/tracks/cognitive_autopsy_source_fidelity_20261108/spec.md": "418d574d2949e4157bb4e152fc8c8c75d4182cda",
    "docs/source-profiles/hdc-medico-legal-profile.md": "539cc831d6b539f96759d2013da78f0b6e2e09a8",
    "task_plan.md": "b27a147a3955a13b1e4e7673e423d65c5261a70e"
  },
  "rcagent": {
    "conductor/research/cognitive-autopsy/programme.md": "823cec99a869164e21e750affc4cda3a77b60387",
    "conductor/tracks/cognitive-autopsy_20261107/incorporation-map.md": "4e4ebb4f0f9bd178a1991caa4d71cf59d9e454a6",
    "conductor/tracks/cognitive-autopsy_20261107/work-packages.md": "aa981b409afdcab4e00ca73e8520571703e5c709",
    "evaluation/cognitive-autopsy/experiment-catalogue.json": "ebfc4a60f28ea528b1eeca25733cabc478b460c5"
  },
  "searchright": {
    "conductor/tracks/13-integration-passports-github-context/spec.md": "b78abb96600f2790fe1042348fb7f3b5508ba206",
    "docs/integration/rcagent-evidence-view.md": "c3d0a12cdfd3d2ec520d749aff13a5df06a6126b",
    "docs/research/portfolio-reuse.md": "17d572ff0452f2d242aa368dda811f46924a9eea",
    "verification/receipts/source-manifest.sha256": "850430a01d14101515a8c04db5459fb1b45cf837"
  },
  "sourceright": {
    "conductor/implementation-order.md": "6df77a0f6e23f3a4e7f847798a0a7b4553db6a3e",
    "conductor/tracks.md": "341634b919525de7c335b6d2cbf86bdc2c52908b",
    "conductor/tracks/110-scoped-evidence-consumers/metadata.json": "011d0db6c4e5c123faa278f3132e89537e1ac951",
    "conductor/tracks/110-scoped-evidence-consumers/plan.md": "50b2ae8f7ceb165e5bfe5b5785e71ad323bc5f0c",
    "conductor/tracks/110-scoped-evidence-consumers/spec.md": "f022f535e0e89552d82a3059afc0166f869f859e",
    "conductor/tracks/110-scoped-evidence-consumers/test-matrix.md": "f1e2c2c9914cb513e049660176e4285e6d8212e4",
    "conductor/tracks/14-claim-source-provenance/spec.md": "25eef619c3706c08d6e3e73e5f9fc40c40828dc1"
  }
}
```
