# Evaluation Scoring — Plan

## Phase 1: Pre-Scoring Setup

- [ ] Task: Confirm blinding is complete
    - [ ] Verify blinding-map.csv is sealed (condition → eval ID mapping)
    - [ ] Confirm all normalized outputs use eval IDs only
    - [ ] Prepare scoring workspace (eval IDs visible, conditions hidden)

## Phase 2: Primary Scoring

- [ ] Task: Score H0 outputs — all cases, all runs
    - [ ] Score each normalized-output.md: D1-D8 (1–5) with rationale
    - [ ] Record structural completeness checklist
    - [ ] Enter scores into rubric-scores.csv
- [ ] Task: Score H1 outputs — all cases, all runs
- [ ] Task: Score H2 outputs — all cases, all runs
- [ ] Task: Score H3 outputs — all cases, all runs
- [ ] Task: Score H4 outputs — all cases, all runs
- [ ] Task: Score H5 outputs — all cases, all runs
- [ ] Task: Score H6 outputs — all cases, all runs
- [ ] Task: Score H7 outputs — all cases, all runs
- [ ] Task: Score H8 outputs — all cases (1 run each)

## Phase 3: Inter-Rater Reliability

- [ ] Task: Select 9-output IRR subset
    - [ ] 3 cases × 3 conditions (H0, H1, H2)
    - [ ] Document selection in inter-rater-reliability.md
- [ ] Task: Run Claude Opus second-rater scoring
    - [ ] Provide rubric as system prompt
    - [ ] Score each of 9 outputs blind (eval IDs only)
    - [ ] Record Opus scores in inter-rater-reliability.md
- [ ] Task: Calculate Cohen's kappa per dimension (D1-D8)
    - [ ] Use weighted kappa (ordinal scale)
    - [ ] Document in inter-rater-reliability.md

## Phase 4: Anchor Revision (if needed)

- [ ] Task: Review dimensions where kappa < 0.6
    - [ ] Identify ambiguous anchor wording
    - [ ] Draft revised anchor descriptions
    - [ ] Re-score affected dimensions with revised anchors
    - [ ] Verify kappa improves to ≥ 0.6
    - [ ] Update evaluation-rubric.md with revised anchors
