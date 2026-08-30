# Evaluation Analysis — Plan

Repository reproducibility, failure-mode and claims reviews use the
[approved agent-panel protocol](../../decisions/20260830-001-legacy-agent-review.md).
Actual analysis remains blocked on admitted scoring evidence and implementation
of the [approved prospective protocol](../../decisions/20260830-002-prospective-agent-study.md),
not on another owner approval.
The historical denominators below are not automatically applicable to a new
agent-scored cohort. No human comparison or clinical validity is inferred.

## Phase 1: Data Preparation

- [ ] Task: Reveal blinding map and annotate rubric-scores.csv
    - [ ] Add condition column (from blinding-map.csv)
    - [ ] Verify all rows present (8 AI conditions × N cases × 3 runs + H8 × N cases)
    - [ ] Check for missing values

## Phase 2: Descriptive Statistics

- [ ] Task: Compute per-condition summary statistics
    - [ ] Mean, median, SD, range for composite score
    - [ ] Mean per dimension (D1-D8) per condition
    - [ ] Document in comparative-analysis.md
- [ ] Task: Compute stability metrics
    - [ ] Cross-run variance per condition per dimension
    - [ ] % of dimensions scoring within ±1 across 3 runs
    - [ ] Document in comparative-analysis.md

## Phase 3: Effect Sizes and Comparisons

- [ ] Task: Calculate Cohen's d (descriptive)
    - [ ] H1 vs H0 (skill effect)
    - [ ] H2 vs H1 (model quality effect)
    - [ ] H3-H7 vs H1 (cross-harness comparisons)
    - [ ] Document with explicit caveat: descriptive only, not hypothesis testing
- [ ] Task: Difficulty × performance correlation
    - [ ] Correlate case difficulty rating (1–3) with composite score per condition
    - [ ] Document in case-level-analysis.md

## Phase 4: Visualizations

- [ ] Task: Create condition × dimension heatmap
    - [ ] Rows: 9 conditions, Columns: D1-D8 + composite
    - [ ] Color scale: 1 (red) → 5 (green)
    - [ ] Save as evaluation/analysis/heatmap.md (Mermaid or ASCII)
- [ ] Task: Create per-condition radar charts
    - [ ] 8 axes (D1-D8), overlaid or faceted
    - [ ] Save as evaluation/analysis/radar-charts.md

## Phase 5: Failure Mode Analysis

- [ ] Task: Review normalization notes and failure mode log
    - [ ] Categorize all observed failures into taxonomy
    - [ ] Calculate frequency per category per condition
    - [ ] Document in failure-mode-analysis.md

## Phase 6: Technical Report

- [ ] Task: Write technical-report.md — all sections
    - [ ] Abstract (250 words)
    - [ ] Introduction (background, objectives)
    - [ ] Methods (design, conditions, rubric, analysis)
    - [ ] Results (descriptive stats, effect sizes, stability, failure modes)
    - [ ] Discussion (skill contribution, cross-model, limitations)
    - [ ] Conclusions
    - [ ] References (from literature-review.md)
- [ ] Task: Obtain agent-panel reproducibility and claims review of exact
  admitted inputs, analysis outputs, exclusions and unsupported conclusions
