# Cognitive autopsy agent context pack

- Purpose: implement Track 12 in bounded, independently verifiable components.
- Base inspected: ae729dffd002c0a5b25fd3695b49378aff13e454 on master.
- Freshness: 2026-11-08; refresh exact sources and current branch before implementation.
- Start: [track index](../tracks/cognitive-autopsy_20261107/index.md), then only the specification, plan and relevant component document.
- Authority: [scope record](../decisions/20261107-001-cognitive-autopsy-programme.md), existing product/privacy rules and approved agent-review decisions.
- Owned scope: cognitive-autopsy contracts, decision-time interpretation and evaluation adapter; public-source capture/fixity stays with archive-govt-nz, neutral extraction with nlp-policy-nz, source/distribution contracts and snapshot/release lineage with the corpus GitHub repository, and study methods with learningfromharm. The existing Hugging Face corpus retains its canonical public dataset identity.
- Exclusions: no patient data in cloud coding context; no fabricated human scores; no rewriting historical results; no operational promotion, training job or public data release implied by this plan.
- Context budget: load one component, its exact dependencies and a bounded non-sensitive fixture; do not load the entire corpus or repository.
- Validation for this planning change: repository governance validator, JSON parsing, changed-document links, diff/whitespace and source checks. Future implementation adds behaviour-based tests for the actual risk.
- Resume point: Phase 1 exact HDC snapshot and three-clock decision contract; preserve unresolved approval identifiers in the protected register without re-requesting existing ethics.
- Rollback: revert the planning commit; future component versions must be independently disableable.

## Small-component refinement

Load only the relevant leaf from [work packages](../tracks/cognitive-autopsy_20261107/work-packages.md) and its linked component/controlled/process/verification document. First priorities are source/account attribution, verification and availability sensitivity. The [experiment catalogue](../../evaluation/cognitive-autopsy/experiment-catalogue.json) is planning-only; no run or clinical qualification exists. Use admitted HDC/synthetic/public inputs while optional external agreements remain unresolved.
