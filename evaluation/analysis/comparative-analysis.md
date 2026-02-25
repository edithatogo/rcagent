# Comparative Analysis — Model × Harness × Skill Condition

**Date**: TBD (post-scoring)
**Status**: Template — pending data collection

---

## 1. Primary Analysis: Descriptive Statistics

### 1.1 Per-Dimension Means by Condition

| Condition | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | Composite |
|---|---|---|---|---|---|---|---|---|---|
| H0 (Control) | | | | | | | | | |
| H1 (CC Sonnet) | | | | | | | | | |
| H2 (CC Opus) | | | | | | | | | |
| H3 (Gemini) | | | | | | | | | |
| H4 (Codex) | | | | | | | | | |
| H5 (Qwen) | | | | | | | | | |
| H6 (Kilo Code) | | | | | | | | | |
| H7 (Copilot) | | | | | | | | | |
| H8 (Human) | | | | | | | | | |

### 1.2 Per-Dimension Standard Deviations by Condition

| Condition | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | Composite |
|---|---|---|---|---|---|---|---|---|---|
| H0 | | | | | | | | | |
| H1 | | | | | | | | | |
| ... | | | | | | | | | |

### 1.3 Per-Dimension Ranges by Condition

| Condition | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|---|---|---|---|---|---|---|
| H0 | | | | | | | | |
| ... | | | | | | | | |

---

## 2. Secondary Analysis: Effect Sizes

### 2.1 Skill Contribution (H1 vs H0)

| Dimension | H1 Mean | H0 Mean | Difference | Cohen's d | Interpretation |
|---|---|---|---|---|---|
| D1 | | | | | |
| D2 | | | | | |
| D3 | | | | | |
| D4 | | | | | |
| D5 | | | | | |
| D6 | | | | | |
| D7 | | | | | |
| D8 | | | | | |
| **Composite** | | | | | |

### 2.2 Model Quality Impact (H2 vs H1)

| Dimension | H2 Mean | H1 Mean | Difference | Cohen's d |
|---|---|---|---|---|
| D1 | | | | |
| ... | | | | |

### 2.3 Cross-Model Transfer (H1 vs H3, H4, H5)

| Comparison | D1 d | D2 d | D3 d | D4 d | D5 d | D6 d | D7 d | D8 d | Composite d |
|---|---|---|---|---|---|---|---|---|---|
| H1 vs H3 | | | | | | | | | |
| H1 vs H4 | | | | | | | | | |
| H1 vs H5 | | | | | | | | | |

### 2.4 Distance from Human Gold Standard

| Condition | Composite Mean | H8 Composite | Gap | Cohen's d |
|---|---|---|---|---|
| H0 | | | | |
| H1 | | | | |
| H2 | | | | |
| H3 | | | | |
| H4 | | | | |
| H5 | | | | |
| H6 | | | | |
| H7 | | | | |

**Note**: Effect sizes are descriptive only. N is insufficient for inferential testing.

---

## 3. Additional Metrics Comparison

| Condition | Mean Time (s) | Mean Input Tokens | Mean Output Tokens | Mean Cost (USD) | Mean Output Words |
|---|---|---|---|---|---|
| H0 | | | | | |
| H1 | | | | | |
| H2 | | | | | |
| H3 | | | | | |
| H4 | | | | | |
| H5 | | | | | |
| H6 | | | | | |
| H7 | | | | | |
| H8 | | | | | |

---

## 4. Within-Condition Stability

### 4.1 Cross-Run Variance by Condition

| Condition | Mean Cross-Run SD | Max Cross-Run SD | Stability % |
|---|---|---|---|
| H0 | | | |
| H1 | | | |
| ... | | | |

**Stability %**: Percentage of (case × dimension) pairs where all 3 runs score within ±1 point.

### 4.2 Unstable Dimensions

| Condition | Case | Dimension | Run 1 | Run 2 | Run 3 | Range |
|---|---|---|---|---|---|---|
| (Rows where range > 2) | | | | | | |

---

## 5. Structural Completeness

| Condition | Mean Sections Present | % with All 8 | Most Frequently Missing |
|---|---|---|---|
| H0 | | | |
| H1 | | | |
| ... | | | |

---

## 6. Visualizations

(To be generated during analysis phase)

- [ ] Heatmap: Condition × Dimension (mean scores)
- [ ] Radar charts: One per condition (8-dimension profile)
- [ ] Box plots: Per dimension, one box per condition
- [ ] Bar chart: Composite scores with error bars

---

## 7. Key Findings

[To be completed after analysis]

### 7.1 Primary: Does rcagent meet acceptable quality?
[H1 scores vs ≥3.0 threshold on all 8 dimensions]

### 7.2 Secondary: Skill contribution
[H1 vs H0 — which dimensions show largest improvement?]

### 7.3 Secondary: Model impact
[H2 vs H1 — does Opus improve on Sonnet with same skill?]

### 7.4 Secondary: Cross-model transfer
[H3/H4/H5 vs H1 — does the skill transfer across models?]

### 7.5 Tertiary: Harness impact
[H6/H7 vs H3/H4/H5 — do alternative harnesses perform differently?]
