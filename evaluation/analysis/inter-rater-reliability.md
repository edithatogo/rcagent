# Inter-Rater Reliability Analysis

**Date**: TBD (post-scoring)
**Status**: Template — pending data collection

---

## 1. Overview

This document reports the agreement between the primary human evaluator and the AI second rater (Claude Opus) on a subset of evaluation outputs.

---

## 2. Subset Selection

| # | Case | Difficulty | Condition | Evaluation ID |
|---|---|---|---|---|
| 1 | TBD | Simple (1) | H0 (control) | |
| 2 | TBD | Simple (1) | H1 (baseline) | |
| 3 | TBD | Simple (1) | H3 (cross-model) | |
| 4 | TBD | Moderate (2) | H0 (control) | |
| 5 | TBD | Moderate (2) | H1 (baseline) | |
| 6 | TBD | Moderate (2) | H3 (cross-model) | |
| 7 | TBD | Complex (3) | H0 (control) | |
| 8 | TBD | Complex (3) | H1 (baseline) | |
| 9 | TBD | Complex (3) | H3 (cross-model) | |

**Selection rationale**: 3 cases spanning difficulty levels × 3 conditions spanning skill conditions (control, native, injected) = 9 outputs. This provides diversity across both axes.

---

## 3. Scoring Protocol

### Human Evaluator
- Scores all 9 outputs blind using the evaluation rubric
- Provides written rationale per dimension per output
- Scoring conditions identical to main evaluation

### AI Second Rater (Claude Opus)
- Receives the evaluation rubric as system prompt
- Scores each output independently per dimension
- Provides written rationale per dimension per output
- Temperature: 0
- Single run per output (no repeated scoring)

### AI Rater Prompt Template

```
You are evaluating the quality of a Root Cause Analysis investigation output.

## Source Investigation Findings (Gold Standard)
{SOURCE_FINDINGS}

## Output to Evaluate
{NORMALIZED_OUTPUT}

## Rubric — Dimension {N}: {DIMENSION_NAME}
{FULL_RUBRIC_TEXT_FOR_DIMENSION}

## Task
Score this output on the dimension described above using a 1-5 scale.
Provide:
1. Score (integer 1-5)
2. Rationale (2-3 sentences referencing specific elements of the output
   and the rubric anchors)
```

---

## 4. Results

### 4.1 Raw Scores

| Output | Dim | Human Score | AI Score | Difference |
|---|---|---|---|---|
| | D1 | | | |
| | D2 | | | |
| | D3 | | | |
| | D4 | | | |
| | D5 | | | |
| | D6 | | | |
| | D7 | | | |
| | D8 | | | |

(72 rows total: 9 outputs × 8 dimensions)

### 4.2 Cohen's Kappa per Dimension

| Dimension | Kappa | Interpretation | Threshold Met (≥0.6)? |
|---|---|---|---|
| D1: Contributing Factor Completeness | | | |
| D2: Root Cause Accuracy | | | |
| D3: Action Strength Quality | | | |
| D4: Just Culture Appropriateness | | | |
| D5: De-identification Compliance | | | |
| D6: Method Selection Appropriateness | | | |
| D7: Chronology/Timeline Quality | | | |
| D8: Safety-II / Systems Lens | | | |

**Interpretation scale** (Landis & Koch, 1977):
- < 0.00: Poor
- 0.00–0.20: Slight
- 0.21–0.40: Fair
- 0.41–0.60: Moderate
- 0.61–0.80: Substantial
- 0.81–1.00: Almost perfect

### 4.3 Agreement Summary

- **Overall weighted kappa**: TBD
- **Dimensions meeting threshold (≥0.6)**: TBD / 8
- **Dimensions requiring anchor revision**: TBD

---

## 5. Anchor Revisions (if needed)

| Dimension | Issue Identified | Original Anchor | Revised Anchor | Rationale |
|---|---|---|---|---|
| | | | | |

---

## 6. Discussion

[To be completed after analysis]

Key questions to address:
1. Which dimensions showed highest/lowest agreement?
2. Were there systematic biases (AI consistently higher/lower than human)?
3. Did disagreements cluster on specific conditions or difficulty levels?
4. Were anchor revisions sufficient to improve agreement?
