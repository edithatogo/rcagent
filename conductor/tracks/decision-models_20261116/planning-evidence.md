# Decision-model planning evidence and integration handoff

## Scope and identity

This receipt concerns the **planning-only** Decision Models proposal dated 16 November 2026 (requested client date). It does not report model evaluation, installed dependencies, feature implementation, real-case processing or deployment. Baseline: `37ca41fa2e7eeee8cc79e24efd5d7c0f915269f3`, tree `038115c101c98efc9438589d9ed1a0efaf294cb8` on `master`.

The new track is `decision-models_20261116`. The branch is `docs/decision-models-spec-plan-20261116`. The supplied repository spelling returned 404; the accessible `edithatogo/rcagent` matches the existing project context and inspected Conductor artefacts. The worktree was clean before this change.

Before publication, master advanced to `d11548357baba6a1e20163139a366c6367a05432`, tree `387522947a4162f2e28241971fcd5620c2fadefd`. The complete intervening diff was the ty dependency/lock update from PR #138; inspected application interfaces were unchanged. This isolated branch was fast-forwarded to that base without altering the proposed documents or another owner's work.

## Preflight and design evidence

- Read root instructions/constraints and Conductor index, product, guidelines, stack, workflow, registry and existing track formats before drafting.
- Inspected current evidence/ports, runtime/privacy, completion, retrieval/encoder, benchmark, action and orchestration boundaries. The specification records exact paths and current limitations.
- Inspected open PR ownership, including AcciMap #141, HEAPS #142 and recommendations #143. The latter also changes `conductor/tracks.md`; the single additive row here is a reviewable registration proposal for the existing shared coordinator.
- Verified current primary model/runtime, encoder/linker and evaluation sources through two read-only research agents and root source checks. The source register distinguishes documentation from executable measurement.
- Preserved current model/runtime unsupported state, existing Track 12/13/14 ownership and all historical results. Every future implementation task remains pending.

## Planning verification

| Check | Observed result and limit |
|---|---|
| `python -m tools.validate_repository` | Passed: repository governance validation. This does not prove model behaviour. |
| Metadata, task state and dependency graph | JSON parsed; 11 unique planned packages; full declared dependency graph acyclic; 43 task/checkpoint markers all pending. No implementation package is marked completed. |
| Local links and source references | 71 local Markdown links resolved across the track documents and registry; every explicit source ID referenced in the specification exists in the register. External documentation was assessed separately, not by this path check. |
| Documented schema fragments | Both JSON Schema 2020-12 fragments passed metaschema checks. Eight shape-positive and six shape-negative examples behaved as specified. These check documented shapes, not the unimplemented semantic validators, runtime or C01–C42 acceptance suite. |
| Mathematical illustration | Independently calculated `0.05 ** (1 / 59) = 0.950492`; valid only for the explicitly stated independent-positive, one-sided exact illustration. No clinical operating threshold adopted. |
| Diff and ownership | New track documents plus one additive registry row only; `git diff --check` passed. No source/tests/shared schemas/CI/manifests/locks or existing track records changed by this proposal. |
| Full application/model validation | Not run for this documentation-only change. Zero model runs, dependency installations, real cases and empirical/clinical qualifications. Hosted results are separately observed after publication; no earlier green run is inherited. |

The initial direct-script invocation `python tools/validate_repository.py` failed with `ModuleNotFoundError: No module named 'tools'` because the repository package root was not on that invocation's import path. The supported module invocation above passed without editing source or changing any gate. The failed invocation is retained as an observation, not misreported as a completed validation.

## Agent panel and resolved findings

Three separate read-only agent roles reviewed the proposal: acceptance/architecture, evidence integrity/source semantics, and safety/privacy/evaluation. The two source researchers also reviewed their subject areas; this was not a blinded independent clinical review. Their initial reviews inspected all seven documents and the registry row; final delta reviews checked the corrected specification/source register. Root checks cover final factual receipt/metadata updates.

| Finding | Resolution and recheck |
|---|---|
| A1: optional ontology/media/service branches conflicted with unconditional empirical acceptance | DM-A03/05/07 now require all requested design mappings but condition empirical claims on the frozen study's included capabilities. Deferred branches stay unsupported; bounded completion cannot imply all workflows qualified. Acceptance reviewer rechecked and closed the finding. |
| E1: changing case-specific Top-K candidates/source views could be misread as forcing per-case recalibration | Qualified candidate-generation procedures can cover varying lists; each list/view stays hash-bound. Source changes invalidate the cached case result, while tuple/procedure/population changes trigger calibration/threshold revalidation. Source and safety reviewers rechecked. |
| S1: ordinal metric needed a direct methodological citation | Added primary RPS source S34 and a bounded citation; no conformal guarantees imported. Root and source reviewer opened the primary source; safety reviewer rechecked the text. |

All three final scoped reviews reported **no blocking finding**. Reviewed content hashes:

| File | SHA-256 |
|---|---|
| `spec.md` | `cb96b968ee428f78d1982cda295ee178522c6d69a62ec2daded3d1527c3c9539` |
| `contracts.md` | `4a32dbfff3cc3499023f60544ea5b1e8e404fd71a8ae39c014300ad158807be2` |
| `plan.md` | `8de989681a7c23e92326415d6055d883cb9e64e22dc8c2551e70bf0aa127fad3` |
| `index.md` | `3904982d95fb7f81db5cf1f0c193b5c0915b9bb8308d1a78c282583073ebf7d9` |
| `sources.md` | `81cee97bab8814211231939d5a8d7491ef9952525b2c99e54fa9b0a6a151a81e` |
| `conductor/tracks.md` | `99aa0196dba321aa3226d24c26ffb3ef3a9fce8178f7b1da4763609f54b3935d` |

Metadata and this receipt were then updated with observed planning results and publication-base reconciliation. Those factual updates do not change the reviewed scope, contracts, sequence or acceptance criteria. Review establishes planning assurance only; it is not formal GitHub approval, executable-schema acceptance, model performance, organisational authority or permission to begin implementation.

## Integration handoff

The explicit user request authorises creation of this track and an entry in `conductor/tracks.md`. Only that additive shared-registry proposal and this new track directory are in scope. The existing coordinator retains portfolio number/roadmap reconciliation, shared-contract/path allocation and merge authority. No runtime registry, canonical schema, dependency manifest, lock, CI, source module, test or another owner's track is changed.

The proposed execution sequence is DM01 → DM02 → parallel DM03/DM04 → DM05 → DM08/DM09, with independent metric-fixture work possible earlier. Ontology and modalities are conditional branches; service deployment is separate. No implementation starts under the present instruction.

A new dedicated operational issue and native dependency registration may be created by the existing coordinator when this proposal is accepted into the execution queue; the draft PR and registry row carry this planning handoff. No new issue is used to claim a second scientific or integration owner.

## Rollback and limitations

Revert only the documentation/registry commit to withdraw this proposal. Retain all earlier repository evidence. Current source URLs are mutable and no weight/runtime revision is qualified. Full empirical acceptance, operational thresholds, future model licences/data rights and target-device compatibility remain as specified future work. Agent review is not human clinical validation.
