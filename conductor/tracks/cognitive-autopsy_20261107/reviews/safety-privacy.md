# Cognitive-autopsy cross-review: bounded adversarial assessment

Reviewer: existing-context behavioural-controls agent, 2026-11-07. This is a cross-review of four other documents, not a fresh-context/blinded review, independent-model validation, clinical validation or review of my own `controlled-experiments.md`. No experiment was run.

## Findings

**P2 — Work-package dependencies conflict with the declared initial/optional sequence.** `work-packages.md` line 3 selects CAW22 but omits CAW13, although CAW22 requires CAW13 (line 36). CAW23 also requires CAW06 (line 37), although the encoder is explicitly optional (lines 3 and 20). An agent following the dependency graph could stall or unnecessarily implement an optional comparison. Add CAW13 to the initial set if intended, or make CAW22 depend on the prespecified selected experiment set. Make the encoder dependency conditional on its inclusion. This is an execution-plan defect, not evidence that experiments failed.

**P2 — Bind every verification stage explicitly to the same authorised evidence view.** `verification-and-reuse.md` says semantic support consumes “complete relevant evidence” (line 15), then retrieves contradictory passages and checks completeness after the initial deterministic checks (lines 28–32). The allowed packet is admitted at the start, but the later stages do not explicitly restate the view binding. An implementation could inadvertently retrieve later appraisal/outcome evidence or use a full-report concern inventory to judge an earlier packet. Specify one immutable packet/view identifier across generation, semantic verification, contradictory retrieval, completeness checks and final rendering; reject out-of-view material after retrieval. Keep any fuller retrospective assessment in a separate labelled condition. This clarification preserves the intended design rather than adding a new approval gate.

**P3 — Make the critical-fact/concern reference provenance explicit.** The critical inventory in `verification-and-reuse.md` line 16 and CAW20's inventory input should have its own frozen version, creator/reviewer class, source spans and uncertainty. The existing instructions correctly preserve model-rating labels and freeze references; explicitly add that the candidate generator/verifier's own uncorroborated inventory cannot be its sole performance reference. This closes a remaining route to circular completeness scoring without mandating a large human annotation exercise.

## Checks with no further blocking findings

The documents require material error and useful coverage jointly and explicitly reject an all-abstaining winner. Binary NLI labels are not silently converted into a three-way reference. Injected errors and naturally occurring generator errors have separate interpretations. Source support is distinguished from clinical truth. Hidden/missing documentation is not treated as proof of omitted care. The synthetic protocol withholds oracle/manifest/answer labels and includes template-only and held-out generator/style controls. Behavioural effects concern the reviewer model; clinician psychological parameters, culpability, prevented harm and observed patient benefit remain unclaimed. No contradiction on these points was found across the four reviewed documents.

## Reviewed snapshots

All paths below are relative to `/workspace/scratch/81269358b64d/cognitive-autopsy-work/`.

- `rcagent/conductor/research/cognitive-autopsy/component-studies.md`: `a4f794bd48a6f69bef7e70901e889aeab5b4251c1bfe64a75d646d1631bb4247`
- `rcagent/conductor/research/cognitive-autopsy/verification-and-reuse.md`: `b67262bb04d69db6ffef269f308f02ebb489383a92d975f97b17394a1f7c903c`
- `rcagent/conductor/tracks/cognitive-autopsy_20261107/work-packages.md`: `1841f9ef08b87510b457171e29b6f6f0a928e13fde62f19701d099d582439386`
- `learningfromharm/docs/COGNITIVE_AUTOPSY_COMPONENT_STUDIES.md`: `5ad566a6082390301fd9f8c53dcb0c151dca0800db59e7b49a6b3e530258b3b9`

Disposition: no high-severity finding; resolve the two P2 documentation issues before treating the work-package plan as execution-ready. This review does not establish implementation correctness or dataset/model admission.

## Closure check — safety/privacy role

Existing-context follow-up, 2026-11-07; not fresh/blinded review or independent-model validation. Reviewed only the specified changes in the three snapshots below.

**The two P2 findings and P3 clarification are resolved at the planning-document level.** Every generation, verification, contradictory retrieval, inventory, rendering and post-render stage now shares an immutable packet/hash, permitted span set, cutoff and recipient scope. Out-of-view spans are rejected even when the source ID is valid; global stores, caches and indexes cannot restore later evidence. The frozen reference inventory records source spans, view, creator/reviewer class and adjudication status; candidate output alone cannot be its sole reference.

CAW13 and CAW06 are optional evidence for CAW22 and CAW23, respectively, rather than hard dependencies. CAW09 now depends on grouped splits. Targeted checks confirmed these relationships and packet-binding fields agree with the catalogue.

SHA-256 snapshots:

- `verification-and-reuse.md`: `41a7d8a01b9c94fb475163acfee1c6e96f15e39da27780ec256977e473705fcf`
- `work-packages.md`: `59a2377ed326ea08cea96b8d2d37afae71cb7e38c61d31ce9e0259ba914df582`
- `experiment-catalogue.json`: `589dd68b37327acab6a76f3c1b74b87a9d20ef07e08582eb3237f3921ce3f832`

No remaining blocking finding within this closure scope. These checks establish documented requirements and consistency, not runtime non-egress, enforced information isolation, clinical correctness or model qualification. No repository files were edited.
