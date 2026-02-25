# Evaluation Analysis

## Overview

Perform all statistical analysis, generate visualizations, compile the failure mode taxonomy, and write the final publishable technical report.

## Functional Requirements

1. **Descriptive statistics**: Mean, median, range per dimension per condition
2. **Effect sizes**: Cohen's d (H1 vs H0, cross-model comparisons) as descriptive measures
3. **Stability analysis**: Cross-run variance per dimension per condition
4. **Difficulty correlation**: Case difficulty (1–3) vs composite score correlation
5. **Heatmap**: Condition × dimension score heatmap
6. **Radar charts**: Per-condition radar chart across 8 dimensions
7. **Failure mode taxonomy**: Categorize observed failure patterns from normalization notes
8. **Technical report**: Complete publishable report (introduction through discussion)

## Acceptance Criteria

- rubric-scores.csv used as primary data source (not re-extracted)
- All descriptive statistics computed and documented
- Effect sizes reported as descriptive only (no hypothesis testing given small N)
- Failure modes classified into taxonomy categories
- technical-report.md complete with all sections filled
- Blinding map revealed and condition labels added to final report

## Dependencies

- eval-scoring_20260225 (rubric-scores.csv must be populated)

## Out of Scope

- Inferential hypothesis testing (insufficient N — acknowledged in limitations)
- Inter-rater reliability (completed in scoring track)
