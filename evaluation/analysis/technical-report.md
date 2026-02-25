# Technical Report: Evaluation of AI-Assisted Root Cause Analysis in Healthcare

**A Multi-Agent Comparison Using AU/NZ Adverse Event Cases**

**Version**: Draft skeleton
**Date**: 2026-02-25
**Status**: Template — pending data collection and analysis

---

## Abstract

[To be written after analysis]

This study evaluates the rcagent skill suite — a structured AI-assisted Root Cause Analysis (RCA) framework — using [N] publicly available Australian and New Zealand adverse event cases across [N] AI agent conditions and a human expert benchmark. Using an 8-dimension evaluation rubric, we assess investigation quality across contributing factor completeness, root cause accuracy, action strength, Just Culture appropriateness, de-identification, method selection, chronology quality, and Safety-II/systems lens. Results show [key findings to be inserted].

---

## 1. Introduction

### 1.1 Background

Root Cause Analysis (RCA) remains the standard methodology for investigating serious adverse events in healthcare. In Australia and New Zealand, the Australian Commission on Safety and Quality in Health Care (ACSQHC) mandates formal investigation for SAC 1 events and recommends it for SAC 2. Despite decades of adoption, evidence suggests RCA quality varies significantly, with investigations frequently stopping at human error, producing weak recommendations, and failing to address systemic contributing factors (Peerally et al., 2017; Nicolini et al., 2011; Kellogg et al., 2017).

The emergence of Large Language Models (LLMs) with demonstrated clinical reasoning capabilities (Singhal et al., 2023; Nori et al., 2023) raises the question: can AI agents produce clinically acceptable RCA investigation outputs — and do structured skill frameworks improve investigation quality over raw model capability?

### 1.2 The rcagent Skill Suite

[Description of the skill suite — methods, templates, agents, design philosophy]

### 1.3 Research Questions

1. **Primary**: Does the rcagent skill suite produce investigation outputs of acceptable quality (mean score ≥ 3.0 on all 8 rubric dimensions)?
2. **Secondary**: How does investigation quality vary across models and harnesses? Does the skill suite improve output quality vs. raw model capability?
3. **Tertiary**: What are the common failure modes, and how do they correlate with case difficulty?

---

## 2. Methods

### 2.1 Study Design

Targeted factorial design: Model × Harness × Skill Condition × Data.

[Reference scientific-protocol.md for full design details]

### 2.2 Experimental Conditions

[Table of H0–H8 conditions]

### 2.3 Dataset

[N] publicly available AU/NZ adverse event cases sourced from [sources].

[Case characteristics table — event type, SAC, difficulty distribution]

### 2.4 Evaluation Rubric

8-dimension, 1–5 Likert scale rubric assessing:
D1: Contributing Factor Completeness
D2: Root Cause Accuracy
D3: Action Strength Quality
D4: Just Culture Appropriateness
D5: De-identification Compliance
D6: Method Selection Appropriateness
D7: Chronology/Timeline Quality
D8: Safety-II / Systems Lens

[Reference evaluation-rubric.md for full anchor descriptions]

### 2.5 Prompt Design

Two prompt variants: Prompt A (skill-aware, minimal task instruction) and Prompt B (naive control, generic investigation language).

[Reference agent-test-protocol.md for full prompt text]

### 2.6 Reproducibility

3 independent runs per condition per case. Temperature 0. Full metadata captured.

### 2.7 Blinding

Evaluator scored normalized outputs with random evaluation IDs. Condition mapping revealed post-scoring.

### 2.8 Inter-Rater Reliability

Claude Opus as AI second rater on 9-output subset. Cohen's kappa per dimension.

---

## 3. Results

### 3.1 Primary Outcome: Acceptable Quality Threshold

[Table: H1 mean scores per dimension vs ≥3.0 threshold]

### 3.2 Descriptive Statistics by Condition

[Heatmap: Condition × Dimension]
[Table: Means, SDs, ranges]

### 3.3 Skill Contribution (H1 vs H0)

[Per-dimension effect sizes]
[Radar chart comparison]

### 3.4 Model Quality Impact (H2 vs H1)

[Per-dimension comparison]

### 3.5 Cross-Model Transfer (H3, H4, H5 vs H1)

[Effect size table]

### 3.6 Alternative Harnesses (H6, H7)

[Results summary]

### 3.7 Human Gold Standard Comparison

[All conditions vs H8]

### 3.8 Additional Metrics

[Time, cost, token usage, word count comparisons]

### 3.9 Within-Condition Stability

[Cross-run variance analysis]

### 3.10 Inter-Rater Reliability

[Cohen's kappa per dimension]

---

## 4. Discussion

### 4.1 Can AI Produce Acceptable RCA Investigations?

[Discuss primary outcome relative to threshold]

### 4.2 The Value of Structured Skill Frameworks

[Discuss H1 vs H0 — what the skill adds]

### 4.3 Model vs Skill Contribution

[Discuss whether model quality or skill structure matters more]

### 4.4 Cross-Model Portability

[Discuss how well the skill transfers to non-Claude models]

### 4.5 Failure Mode Implications

[Discuss what AI gets wrong and what that means for clinical governance]

### 4.6 Difficulty Sensitivity

[Discuss whether skill benefit increases with case complexity]

### 4.7 Implications for Clinical Practice

[Discuss what this means for healthcare quality and safety teams]

---

## 5. Limitations

1. Information asymmetry (narrative only vs full clinical record)
2. Small N (pilot-scale, descriptive only)
3. Non-full-factorial design
4. Single primary human evaluator
5. AI knowledge cutoff and potential data leakage
6. AU/NZ specificity
7. Hindsight bias
8. Harness version sensitivity
9. LLM non-determinism

---

## 6. Conclusion

[To be written after analysis]

---

## 7. References

[Full reference list from literature-review.md]

---

## Appendices

### Appendix A: Full Evaluation Rubric

[Reference: evaluation/protocol/evaluation-rubric.md]

### Appendix B: Case Characteristics

[Full case metadata table]

### Appendix C: Per-Case Dimension Scores

[Full scoring data]

### Appendix D: Failure Mode Catalogue

[Reference: evaluation/analysis/failure-mode-analysis.md]

### Appendix E: Inter-Rater Reliability Details

[Reference: evaluation/analysis/inter-rater-reliability.md]
