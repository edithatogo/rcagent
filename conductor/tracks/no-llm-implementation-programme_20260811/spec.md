# No-LLM Implementation Programme — Specification

## Overview

Coordinate the remaining repository work that can be completed without
downloading local LLM or embedding-model weights. Delivery proceeds through
small sequential pull requests, with evidence-backed checks and bounded local
Git state.

## Functional requirements

1. Reconcile Track 00 implementation evidence and pending Conductor tasks.
2. Implement Tracks 01-04 using deterministic fixtures, mocks, schemas, policy
   mappings, and fail-closed governance controls.
3. Implement the no-model portion of Tracks 05-08 and 10: harnesses, manifests,
   adapters, deterministic retrieval, runtime discovery, and dry-run pipelines.
4. Implement Tracks 09 and 11 interfaces, action tracking, packaging, adapters,
   and release-readiness controls.
5. Apply cross-cutting repository security and quality work from issues #17 and
   #18 throughout the programme.
6. Preserve external API, human-evaluator, licence, publication, and model-run
   gates as explicit blockers rather than simulated completion.

## Delivery requirements

- One implementation branch is active at a time.
- Use at most one disposable isolated checkout outside the mixed OneDrive
  worktree.
- Each PR addresses one coherent acceptance boundary and remains small enough
  for direct review.
- Make regular, coherent commits within a PR; do not combine unrelated tracks.
- Run relevant local checks before push.
- Wait for every required hosted check to complete successfully before merge.
- Do not merge queued, failing, cancelled, skipped-required, or unknown checks.
- Delete merged remote and local branches and remove the disposable checkout
  before beginning the next PR.
- Keep the preserved original worktree unchanged unless a later reconciliation
  task explicitly brings it into scope.

## Acceptance criteria

- The programme sequence and PR boundaries are recorded in Conductor.
- Every completed slice links its commits, PR, checks, and merge receipt.
- No slice downloads model weights or makes unsupported model-capability claims.
- Blocked work has an owner, prerequisite, contingency, and restart instruction.
- No more than one implementation branch and one disposable checkout remain
  active between slices.
- Parent roadmap issues close only after child-track acceptance evidence passes.

## Out of scope

- Downloading or running local LLM, multimodal, or embedding weights.
- Fine-tuning or producing model artefacts.
- Fabricating provider, operator, patient, clinical, or human-evaluator evidence.
- Selecting a project licence or making a public release without owner authority.
- Archiving the GitHub repository while open roadmap work remains.
