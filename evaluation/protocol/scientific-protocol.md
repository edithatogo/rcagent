# Evaluation of AI-Assisted Root Cause Analysis in Healthcare: A Multi-Agent Comparison Using AU/NZ Adverse Event Cases

**Version**: 1.0
**Date**: 2026-02-25
**Status**: Protocol — Pre-data-collection

---

## 1. Background

### 1.1 The Problem

Root Cause Analysis (RCA) is the primary investigative tool for serious adverse events (SAEs) in healthcare. In Australia and New Zealand, the Australian Commission on Safety and Quality in Health Care (ACSQHC) mandates RCA for Severity Assessment Code (SAC) 1 events and recommends it for SAC 2. Despite widespread adoption, RCA quality varies significantly — investigations frequently stop at human error, produce weak recommendations (training-only), and fail to address systemic contributing factors (Peerally et al., 2017; Nicolini et al., 2011).

### 1.2 AI-Assisted Investigation

Large Language Models (LLMs) have demonstrated capability in clinical reasoning (Singhal et al., 2023), structured analysis (Wei et al., 2022), and document generation. However, no published evaluation examines whether AI agents can produce clinically acceptable RCA investigations — or whether structured skill frameworks improve investigation quality over raw model capability.

### 1.3 The rcagent Skill Suite

The rcagent skill suite (v1.0) provides structured guidance for healthcare RCA investigations, including:

- **14 investigation methods** spanning core (RCA², 5 Whys, Fishbone, Timeline), systems (Yorkshire Framework, SEIPS 3.0, Swiss Cheese, London Protocol), structured (Bow-Tie, Barrier Analysis, FMEA, HFACS), and advanced (AcciMap, STAMP/STPA) approaches
- **Method selection matrix** — decision framework mapping SAC level and event characteristics to recommended methods
- **Just Culture framework** — structured individual accountability assessment
- **Safety-II/resilience engineering lens** — Work-as-Done vs Work-as-Imagined analysis
- **12 Mermaid diagram templates**, **14 markdown working document templates**, **7 DOCX templates**, **3 PPTX templates**
- **4 specialized agents** — Triage, Investigate, Report, Track

The skill suite is designed as a **harness configuration** — it instructs how an AI agent harness guides the underlying model. This evaluation tests whether this structured configuration improves investigation quality.

### 1.4 Gap in Literature

No published study:
1. Evaluates AI-generated RCA investigation quality using validated rubrics
2. Compares multiple AI agent harnesses on clinical investigation tasks
3. Isolates the contribution of structured skill frameworks from underlying model capability
4. Tests AI investigation against publicly available AU/NZ adverse event cases with known outcomes

---

## 2. Objectives

### 2.1 Primary

Does the rcagent skill suite produce investigation outputs of acceptable quality (mean score ≥ 3.0 on all 8 rubric dimensions)?

### 2.2 Secondary

1. How does investigation quality vary across models (Claude Sonnet, Claude Opus, Gemini Pro, GPT-4o, Qwen)?
2. How does investigation quality vary across harnesses (Claude Code, Gemini CLI, Codex CLI, Qwen CLI, Kilo Code, Copilot)?
3. Does the skill suite (harness configuration) improve output quality vs. raw model capability (Condition A/B vs. Condition C)?

### 2.3 Tertiary

1. What are the common failure modes across conditions?
2. How does performance correlate with case difficulty?
3. How stable are outputs across repeated runs (within-condition variance)?

---

## 3. Methods

### 3.1 Study Design

**Targeted factorial design**: Model × Harness × Skill Condition × Data

This is NOT a full factorial design (which would require hundreds of conditions). Instead, we test targeted combinations that isolate specific experimental questions.

**Factors:**

| Factor | Levels |
|---|---|
| **Model** | Claude Sonnet 4.6, Claude Opus 4.6, Gemini Pro, GPT-4o/Codex, Qwen, others as available |
| **Harness** | Claude Code, Gemini CLI, Codex CLI, Qwen CLI, Kilo Code, Copilot, Raw API |
| **Skill Condition** | (A) Skill-native, (B) Prompt-injected, (C) No skill (control) |
| **Data** | 5–10 AU/NZ public adverse event cases |

**Skill Condition definitions:**
- **Condition A — Skill-native**: The harness loads SKILL.md through its native skill/instruction mechanism (e.g., Claude Code `/skill`). This is the designed usage path.
- **Condition B — Prompt-injected**: SKILL.md content is provided as system prompt / custom instructions. Tests cross-harness portability.
- **Condition C — No skill (control)**: No skill content provided. Tests raw model capability with generic investigation instructions.

### 3.2 Experimental Conditions

| ID | Model | Harness | Skill Condition | Purpose |
|---|---|---|---|---|
| H0 | Claude Sonnet 4.6 | Raw API | None (C) | Control — raw model capability |
| H1 | Claude Sonnet 4.6 | Claude Code | Native (A) | Baseline — skill as designed |
| H2 | Claude Opus 4.6 | Claude Code | Native (A) | Model quality impact |
| H3 | Gemini Pro | Gemini CLI | Injected (B) | Cross-model transfer |
| H4 | GPT-4o | Codex CLI | Injected (B) | Cross-model transfer |
| H5 | Qwen | Qwen CLI | Injected (B) | Cross-model transfer |
| H6 | Various | Kilo Code | Injected (B) | Alternative harness |
| H7 | Various | Copilot | Injected (B) | Alternative harness |
| H8 | Human Expert | — | Provided as ref | Gold standard |

**Key comparisons:**
- H1 vs H0: Skill contribution (same model, same base harness capability, skill vs no skill)
- H1 vs H2: Model quality impact (Sonnet vs Opus, same harness + skill)
- H1 vs H3/H4/H5: Cross-model transfer (skill injected into different models)
- H3/H4/H5 vs H0: Cross-model + skill vs Claude-only control
- H6/H7: Alternative harness compatibility
- H8: Human gold standard benchmark

### 3.3 Prompt Design

Two prompt variants are used to prevent confounding the control condition:

**Prompt S — Skill-Aware** (conditions A and B, where SKILL.md is loaded):

```
You are conducting a Root Cause Analysis investigation for the following
clinical adverse event.

## Case Narrative
[Standardized case text extracted from public source]

## Task
Follow the RCA investigation workflow: triage → investigate → report.
Produce all outputs in structured markdown format.
```

Rationale: Deliberately minimal task instruction. The SKILL.md guides method selection, Yorkshire Framework application, Just Culture assessment, action strength classification. This tests the skill suite's guidance value.

**Prompt N — Naive Control** (condition C, no skill):

```
You are a healthcare quality and safety expert conducting an investigation
into the following clinical adverse event.

## Case Narrative
[Standardized case text extracted from public source]

## Task
1. Assess the severity of this event
2. Build a chronology of events
3. Identify the factors that contributed to this event
4. Identify the root cause(s)
5. Assess accountability appropriately for individuals involved
6. Generate recommendations to prevent recurrence
7. Produce an action plan

Produce all outputs in structured markdown format.
```

Rationale: Generic investigation language without naming specific frameworks. Tests what the model produces from its training knowledge alone. The 7-step task list ensures baseline structural completeness without providing methodological guidance.

### 3.4 Dataset

**Sources**: Publicly available AU/NZ adverse event investigation reports and coroner findings.

| Source | Jurisdiction | Case Types |
|---|---|---|
| ACSQHC Sentinel Event Reports | AU (National) | Medication, surgical, deterioration, falls |
| NSW Clinical Excellence Commission | AU (State) | Various clinical incidents |
| Victorian CCOPMM Reports | AU (State) | Perinatal/maternal |
| Coroners Court of Victoria/NSW/QLD | AU (State) | Inpatient deaths |
| HDC NZ Decision Reports | NZ | Full range — **primary NZ source** |
| NZ Coroners Court | NZ | Deaths |
| HQSC NZ Reports | NZ | Systemic quality issues |
| ACC Treatment Injury | NZ | Clinical adverse events |

**Selection criteria:**
- Minimum 5, target 10 cases
- Event type coverage: ≥1 each of medication, clinical deterioration, falls, surgical, mental health
- SAC-equivalent coverage: ≥2 SAC 1, ≥3 SAC 2, remainder SAC 3/4
- Sufficient narrative detail (≥500 words in source)
- Published by issuing authority (public domain)
- Mix of AU (≥2) and NZ (≥3) sources

**Difficulty rating**: Each case rated 1 (simple), 2 (moderate), or 3 (complex) based on number of contributing factors, individuals involved, timeframe span, and organisational complexity. See `case-selection-criteria.md` for full rating criteria.

### 3.5 Evaluation Rubric

**8 dimensions, 1–5 Likert scale** per case per condition per run. See `evaluation-rubric.md` for full anchor descriptions.

| Dim | Dimension | What It Assesses |
|---|---|---|
| D1 | Contributing Factor Completeness | Breadth and depth of factor identification |
| D2 | Root Cause Accuracy | Distinction between proximate and systemic causes |
| D3 | Action Strength Quality | Strength classification per RCA² hierarchy |
| D4 | Just Culture Appropriateness | Fair accountability without blame |
| D5 | De-identification Compliance | Privacy protection |
| D6 | Method Selection Appropriateness | Match between methods and event characteristics |
| D7 | Chronology/Timeline Quality | Accuracy, completeness, critical interval identification |
| D8 | Safety-II / Systems Lens | Resilience perspective, Work-as-Done vs Work-as-Imagined |

**Composite score**: Sum of D1–D8 (range 8–40). Per-dimension analysis is primary; composite is secondary.

**Additional metrics per run:**

| Metric | Measurement |
|---|---|
| Time to completion | Wall-clock seconds, start to final output |
| Token usage | Input + output tokens (API metadata or harness logs) |
| Cost per case | USD, calculated from token counts × model pricing |
| Output word count | Total words in raw output |
| Structural completeness | Binary checklist: which of 8 expected sections produced |

### 3.6 Gold Standard

The published investigation outcomes from HDC NZ / ACSQHC / coroner findings serve as the reference standard. These investigations were conducted by qualified human experts with access to the full clinical record, staff interviews, and site inspections.

The AI conditions receive only the published narrative — NOT the full source materials. This asymmetry is acknowledged as a limitation (see Section 8).

Evaluators score AI outputs against: "what did the source investigation find?" where the source findings are known.

### 3.7 Evaluator Blinding Protocol

To mitigate confirmation bias:

1. After all runs are complete, strip all harness metadata and condition identifiers from outputs
2. Assign random evaluation IDs (format: `eval-XXXX-case-NN`, where XXXX is random alphanumeric)
3. Shuffle presentation order within each case
4. Primary evaluator scores all outputs blind
5. Condition–ID mapping is stored in `results/blinding-map.csv` and revealed only after all scoring is complete

### 3.8 Output Normalization

Before scoring, each raw transcript is extracted into 8 standardized sections:

1. SAC Classification (with rationale)
2. Investigation Methods Selected (with rationale if provided)
3. Chronology/Timeline
4. Contributing Factors (categorized by level: individual, team, task, environment, organisation)
5. Root Causes (proximate and systemic, distinguished)
6. Just Culture Assessment
7. Recommendations (with strength classification if present)
8. CAPA Action Plan

Scoring is performed on the **normalized output**, not the raw transcript. Raw transcripts are preserved for qualitative analysis. See `agent-test-protocol.md` for extraction rules.

### 3.9 Reproducibility Protocol

- Temperature 0 (or lowest available setting) for all models
- **3 independent runs** per case per condition (separate sessions, no context carry-over)
- Single session per run (no multi-turn refinement)
- Full raw transcript preserved for every run
- Recorded per run: harness version, model version/ID, API endpoint, temperature setting
- Timestamp start/end for time-to-completion metric

**Stability metric**: Percentage of dimensions where all 3 runs for a condition score within ±1 point. Conditions with >2-point spread on any dimension flagged as unstable.

### 3.10 Pilot Calibration

Before full evaluation:

1. Select 2 pilot cases (1 AU, 1 NZ; 1 simple, 1 complex)
2. Run through 2 conditions only (H1 — skill baseline, H0 — control)
3. Score both outputs using the rubric with detailed scoring notes
4. Review: Were any dimensions difficult to score? Were anchors ambiguous?
5. Refine rubric wording if needed
6. Document all calibration decisions in `evaluation-rubric.md` appendix

### 3.11 Inter-Rater Reliability

- Claude Opus serves as automated second rater on a subset
- Subset: 3 cases × 3 conditions = 9 outputs
- Human primary evaluator scores all 9 blind
- Claude Opus scores all 9 blind (using the rubric as system prompt)
- Calculate Cohen's kappa per dimension
- If kappa < 0.6 on any dimension: revise that dimension's anchor wording and re-score
- Full results documented in `analysis/inter-rater-reliability.md`

---

## 4. Analysis Plan

### 4.1 Descriptive Statistics (Primary)

Per dimension per condition:
- Mean, median, standard deviation, range across cases
- Mean, median, standard deviation, range across runs (within-condition stability)

Per condition (composite):
- Mean total score (D1–D8 sum)
- Profile: radar chart of 8-dimension means

### 4.2 Effect Sizes (Secondary — Descriptive Only)

Cohen's d between:
- H1 vs H0 (skill contribution)
- H2 vs H1 (model quality impact)
- H1 vs H3, H1 vs H4, H1 vs H5 (cross-model comparison)
- Each condition vs H8 (distance from human gold standard)

**No inferential statistical tests** — N is insufficient for meaningful p-values. Effect sizes are reported as descriptive measures only.

### 4.3 Visualizations

- **Heatmap**: Condition (rows) × Dimension (columns), cell = mean score
- **Radar charts**: One per condition showing 8-dimension profile
- **Box plots**: Per dimension, one box per condition, showing cross-case distribution
- **Scatter plot**: Case difficulty (x) vs composite score (y), one series per condition

### 4.4 Within-Condition Stability

For each condition:
- Cross-run variance per dimension per case
- Stability metric: % dimensions with all 3 runs within ±1 point
- Identify dimensions with highest cross-run variance

### 4.5 Difficulty Correlation

- Spearman rank correlation: case difficulty rating vs composite score per condition
- Qualitative analysis: do certain conditions degrade more on complex cases?

### 4.6 Failure Mode Taxonomy

Qualitative assessment across all conditions:
- **Omission failures**: Contributing factors missed, sections absent
- **Commission failures**: Incorrect classifications, hallucinated frameworks, fabricated details
- **Structural failures**: Output poorly organized, sections conflated
- **Depth failures**: Surface-level analysis, stopped at human error
- **Specificity failures**: Vague recommendations ("improve communication")
- **Bias failures**: Blame language, incorrect Just Culture classification
- **Truncation failures**: Output cut short, incomplete analysis

Document in `analysis/failure-mode-analysis.md`.

---

## 5. Literature Basis

See `literature-review.md` for full citation details. Key references:

### Investigation Methods (14)
- RCA² — Joint Commission (2015)
- 5 Whys — Ohno (1988), adapted by NHS Improvement
- Fishbone — Ishikawa (1968), adapted by IHI
- Yorkshire Framework — Lawton et al. (2012), BMJ Quality & Safety
- SEIPS 3.0 — Carayon et al. (2020), Applied Ergonomics
- Swiss Cheese — Reason (1990, 2000)
- London Protocol — Vincent et al. (2004), BMJ
- Bow-Tie — de Ruijter & Guldenmund (2016), Safety Science
- Barrier Analysis — Hollnagel (2004)
- FMEA — DeRosier et al. (2002), Joint Commission Journal
- HFACS — Shappell & Wiegmann (2000), FAA
- AcciMap — Rasmussen & Svedung (2000)
- STAMP/STPA — Leveson (2004), Safety Science
- Safety-II — Hollnagel et al. (2015), EUROCONTROL

### RCA Quality and Limitations
- Peerally et al. (2017). The failure of RCA. BMJ Quality & Safety
- Nicolini et al. (2011). When culture meets practice. Social Science & Medicine
- Wu et al. (2008). Effectiveness of root cause analysis. Journal of Patient Safety

### AI in Clinical Domains
- Singhal et al. (2023). Large language models encode clinical knowledge. Nature
- Nori et al. (2023). Capabilities of GPT-4 on medical competency examinations. arXiv

### Evaluation Methodology
- Cohen J (1960). A coefficient of agreement for nominal scales. Educational & Psychological Measurement
- Krippendorff K (2004). Content Analysis: An Introduction to Its Methodology

---

## 6. Datasets

See `datasets/README.md` for full provenance, licensing, and ethics documentation.

Each case is structured in standardized format:
- Source and URL
- Event type classification
- SAC-equivalent severity rating
- Difficulty rating (1–3)
- Standardized narrative (≥500 words)

All cases are sourced from publicly available documents published by official government or statutory bodies. No patient contact, no ethics committee approval required (secondary analysis of published documents).

---

## 7. Deliverables

| Deliverable | Location |
|---|---|
| Master protocol | `evaluation/protocol/scientific-protocol.md` (this document) |
| Literature review | `evaluation/protocol/literature-review.md` |
| Evaluation rubric | `evaluation/protocol/evaluation-rubric.md` |
| Case selection criteria | `evaluation/protocol/case-selection-criteria.md` |
| Agent test protocol | `evaluation/protocol/agent-test-protocol.md` |
| Dataset documentation | `evaluation/datasets/README.md` |
| Standardized cases | `evaluation/datasets/{source}/xx-case-XX.md` |
| Raw transcripts | `evaluation/results/{condition}/case-XX/run-N/raw-transcript.md` (H8: no run-N/ nesting) |
| Normalized outputs | `evaluation/results/{condition}/case-XX/run-N/normalized-output.md` (H8: no run-N/ nesting) |
| Rubric scores | `evaluation/results/{condition}/case-XX/run-N/scores.md` (H8: no run-N/ nesting) |
| Blinding map | `evaluation/results/blinding-map.csv` |
| Score database | `evaluation/analysis/rubric-scores.csv` |
| Inter-rater reliability | `evaluation/analysis/inter-rater-reliability.md` |
| Comparative analysis | `evaluation/analysis/comparative-analysis.md` |
| Case-level analysis | `evaluation/analysis/case-level-analysis.md` |
| Failure mode analysis | `evaluation/analysis/failure-mode-analysis.md` |
| Technical report | `evaluation/analysis/technical-report.md` |

---

## 8. Limitations

1. **Information asymmetry**: AI conditions receive published narratives only; human investigators had access to full clinical records, staff interviews, and site inspections. AI outputs are expected to be less complete — the question is whether they are structurally sound and identify the major contributing factors present in the narrative.

2. **Small N**: 5–10 cases is a pilot-scale evaluation. Results are descriptive and hypothesis-generating, not confirmatory. Effect sizes are reported as descriptive measures only.

3. **Non-full-factorial design**: Not all model × harness × condition combinations are tested. Conclusions about interaction effects are limited.

4. **Single primary human evaluator**: Mitigated by AI second rater and inter-rater reliability assessment, but generalizability of scoring is limited.

5. **AI knowledge cutoff**: Models may have been trained on some of the source investigation reports, potentially inflating performance on cases from widely cited sources.

6. **AU/NZ specificity**: The skill suite is designed for AU/NZ regulatory context. Results may not generalize to other jurisdictions.

7. **Hindsight bias**: All investigations (human and AI) are conducted after the outcome is known. The AI has no ability to assess "what was knowable at the time" without explicit narrative cues.

8. **Harness version sensitivity**: Agent harnesses are rapidly evolving. Results are specific to the versions tested and may not replicate with future versions.

9. **Temperature and non-determinism**: Even at temperature 0, LLM outputs are non-deterministic due to implementation details (floating-point arithmetic, batching). The 3-run protocol mitigates but does not eliminate this.

---

## 9. Ethics

- All case data is sourced from publicly available documents published by official government or statutory bodies
- No patient contact occurs during this study
- No ethics committee approval is required (secondary analysis of published, de-identified documents)
- AI-generated investigation outputs are for evaluation purposes only — they are NOT clinical investigation reports and must NOT be used for clinical governance decisions
- All case narratives used in this study maintain the de-identification present in the source documents
- This study does not involve human subjects research

---

## 10. Timeline

| Phase | Description | Status |
|---|---|---|
| Protocol development | This document + supporting protocols | Complete |
| Case collection | Identify and standardize 5–10 AU/NZ cases | Pending |
| Pilot calibration | 2 cases × 2 conditions, rubric refinement | Pending |
| Data collection | All conditions × all cases × 3 runs | Pending |
| Scoring | Blind evaluation of normalized outputs | Pending |
| Inter-rater reliability | AI second rater on 9-output subset | Pending |
| Analysis | Descriptive statistics, visualizations, failure modes | Pending |
| Technical report | Final publishable report | Pending |

---

## References

See `evaluation/protocol/literature-review.md` for complete reference list.
