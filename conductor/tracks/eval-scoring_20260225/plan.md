# Evaluation Scoring — Plan

## Current plan amendment

Repository reviews and prospective research scoring use the
[agent-panel decision](../../decisions/20260830-001-legacy-agent-review.md).
The historical condition counts below remain blocked until a versioned
protocol decision and canonical admission receipt exist. H8 is not an agent
reviewer and is not renamed. See
[pending protocol choice](../../decisions/20260830-002-prospective-agent-study.md).

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
- [ ] Task: Run three blind agent scorers and a separate post-submission
  adjudicator under the prospective approved protocol
    - [ ] Provide rubric as system prompt
    - [ ] Score each of 9 outputs blind (eval IDs only)
    - [ ] Record each agent's scores, revision, input/rubric hashes and abstentions
- [ ] Task: Calculate Cohen's kappa per dimension (D1-D8)
    - [ ] Use weighted kappa (ordinal scale)
    - [ ] Document agent agreement only, using the approved prospective metric;
      do not claim human–AI kappa or independent-human reliability

## Phase 4: Anchor Revision (if needed)

- [ ] Task: Review dimensions where kappa < 0.6
    - [ ] Identify ambiguous anchor wording
    - [ ] Draft revised anchor descriptions
    - [ ] Preserve original ratings; freeze a new rubric before a new blinded run
    - [ ] Report persistent low agreement as uncertain or unsupported; never
      revise thresholds or scores retrospectively to obtain a pass
    - [ ] Update evaluation-rubric.md with revised anchors
