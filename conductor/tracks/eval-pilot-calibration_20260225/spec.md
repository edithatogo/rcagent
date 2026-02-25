# Evaluation Pilot Calibration

## Overview

Run a pilot calibration phase using 2 cases and 2 conditions (H0 control, H1 baseline) to validate that the 8-dimension rubric anchors are unambiguous and produce consistent scoring. Refine anchor wording before full evaluation.

## Functional Requirements

1. **Case selection**: Select 2 pilot cases (1 AU moderate, 1 NZ complex) from collected dataset
2. **Condition execution**: Run H0 (Raw API, Prompt N) and H1 (Claude Code + skill, Prompt S) on both cases
3. **Scoring**: Score all 4 outputs using the evaluation rubric with detailed notes
4. **Rubric review**: Assess each dimension for scoring difficulty, ambiguity, and needed refinements
5. **Anchor revision**: Revise any dimension anchors scoring "Hard" to apply
6. **Documentation**: Record all calibration decisions in evaluation-rubric.md Appendix A

## Acceptance Criteria

- 2 pilot cases selected and documented
- 4 outputs generated (2 cases x 2 conditions)
- All 4 outputs scored with detailed rationale per dimension
- Each dimension assessed for scoring difficulty (Easy/Moderate/Hard)
- No dimension requires >30 seconds of deliberation after refinement
- Calibration log completed in evaluation-rubric.md Appendix A
- Rubric anchor revisions documented (if any)

## Dependencies

- eval-case-collection_20260225 (must be completed first — need cases)

## Out of Scope

- Full data collection across all conditions
- Inter-rater reliability assessment (done during scoring track)
