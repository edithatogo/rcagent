# Evaluation Scoring

## Current execution boundary (2026-08-30)

The specification below preserves the historical study design, not permission
to execute it. The owner has replaced external-human repository review with
[agent panels](../../decisions/20260830-001-legacy-agent-review.md). Human–AI
kappa and the fixed Claude Opus second-rater design below must not be claimed
for an agent panel. A prospective scoring protocol and condition manifest await
[decision 20260830-002](../../decisions/20260830-002-prospective-agent-study.md).
No scoring or blinding is unlocked by review substitution. Preserve original
scores; any rubric revision is prospective, with a new blinded run and an
unsupported outcome allowed. Do not optimise historical scores to pass kappa.

## Overview

Score all blinded normalized outputs using the 8-dimension evaluation rubric. Conduct inter-rater reliability assessment using Claude Opus as AI second rater on a 9-output subset. Refine rubric anchors if any dimension shows insufficient agreement.

## Functional Requirements

1. **Blinded scoring**: Score all normalized outputs using evaluation IDs (not condition names)
2. **8-dimension rubric**: Score D1-D8 (1–5 scale) per run with rationale per dimension
3. **Metrics capture**: Record composite score, structural completeness, time, tokens, cost, word count
4. **IRR subset**: Score 3 cases × 3 conditions = 9 outputs with Claude Opus as second rater
5. **Cohen's kappa**: Calculate per-dimension kappa between human and AI rater
6. **Anchor revision**: Revise any dimension anchors where kappa < 0.6
7. **Scores CSV**: Populate analysis/rubric-scores.csv with all scores

## Acceptance Criteria

- All normalized outputs scored (8 AI conditions × all cases × 3 runs + H8 × all cases × 1 run)
- Each scored output has D1-D8 scores with rationale
- IRR assessment complete (9-output subset, kappa per dimension)
- All dimensions achieve kappa ≥ 0.6 after any anchor revision
- rubric-scores.csv fully populated
- Blinding map remains sealed until all scoring is complete

## Dependencies

- eval-data-collection_20260225 (all normalized outputs needed)

## Out of Scope

- Statistical analysis and visualization (separate track)
