# Bounded cross-review: cognitive-autopsy methods

Date: 2026-11-07. Reviewer: /root/nlp_datasets.

This is an existing-context cross-review, not a fresh, blinded or independent-model review. I authored the separate component-study/dataset documents and did not review those as independent work. Scope: root-authored verification-and-reuse.md, work-packages.md, experiment-catalogue.json, and learningfromharm/docs/COGNITIVE_AUTOPSY_COMPONENT_STUDIES.md. No model runs, clinical validation or repository mutations were performed.

## Findings

### P2 — Base-rate response is promised without a corresponding executable contrast

In experiment-catalogue.json, studies[id=CS04].question includes appropriate response to base rates. Its linked CAW13 task holds risks fixed and changes equivalent representations; its primary outcome measures framing inconsistency and numerical error. Those tests cannot establish appropriate updating when a prior/base rate changes. The learningfromharm document correctly describes base-rate updating as a later extension.

Fix: narrow CS04's present question to equivalent representations, or add a distinct controlled-prior/likelihood contrast with a specified posterior reference, output and scoring rule. Do not infer base-rate competence from representation invariance.

### P2 — Evidence-acquisition outcome needs a direction of benefit

In experiment-catalogue.json, studies[id=CS08].primary is change_in_supported_assessment_per_evidence_acquisition_cost. An assessment changing is not necessarily improving; the metric could reward disruptive or incorrect changes. A cost ratio can also be unstable at zero or very small acquisition cost.

Fix: define a predeclared improvement in reference-supported assessment accuracy, material-error reduction or decision loss at a fixed evidence budget, with burden/cost reported separately. Use utilities only where the explicit decision model supports them. Retain the current formal-VOI claim boundary.

### P3 — Core-study dependencies conflict with the stated optional sequence

work-packages.md instructs agents to start with CAW01–05, 07–12 and 20–22, but CAW22 requires CAW13. Separately, CS03 lists synthetic_worlds as a non-optional dataset profile sourced from CAW14, while CS03's listed tasks omit that later world-generation task. This can accidentally make optional behavioural or synthetic-world work a prerequisite for the first component paper.

Fix: add a study-specific/conditional analysis dependency or explicitly include CAW13 in the initial sequence. Distinguish simple HDC mutation fixtures from mechanistic synthetic worlds, or include CAW14 when those worlds are actually required.

## Positive findings and limits

No P0/P1 scientific-claim issue identified in the reviewed scope. The verification document correctly distinguishes schema validity, source existence, semantic support, completeness and causal truth; separates injected from natural errors; preserves insufficient evidence; and requires the corrected NLI4CT-P consistency calculation. The research addendum keeps case families as the independent unit and does not claim clinician psychology or patient benefit from text metrics.

This bounded review does not independently verify the underlying repository implementations, dependency licences or external citations afresh.


## Closure check — evidence integrity, 2026-11-07

Existing-context follow-up only; not a fresh, blinded or independent-model review. I checked the specified corrections in the current experiment catalogue and work-package plan. No clinical validation or new broad review was performed.

All three prior findings are resolved for these checked planning versions:

- CS04 now tests equivalent fixed-risk representations and does not claim base-rate updating.
- CS08 measures supported accuracy or material-error reduction at a fixed evidence budget, reporting burden separately.
- CAW22 no longer requires framing; CAW23 no longer requires the optional encoder; CAW09 now depends on the frozen split task.
- CS03 uses CAW02 availability fixtures; CS04 uses CAW13 numerical-risk fixtures. Neither requires mechanistic world generation.
- Source-register paths explicitly use the repository root and resolve to existing files.

Checked SHA-256 values:

| File | SHA-256 |
| --- | --- |
| rcagent/evaluation/cognitive-autopsy/experiment-catalogue.json | 589dd68b37327acab6a76f3c1b74b87a9d20ef07e08582eb3237f3921ce3f832 |
| rcagent/conductor/tracks/cognitive-autopsy_20261107/work-packages.md | 59a2377ed326ea08cea96b8d2d37afae71cb7e38c61d31ce9e0259ba914df582 |

No unresolved finding remains within this closure scope. These hashes identify reviewed documentation, not executed experiments or qualified capabilities.
