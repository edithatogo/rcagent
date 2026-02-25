# Failure Mode Analysis

**Date**: TBD (post-scoring)
**Status**: Template — pending data collection

---

## 1. Overview

This document catalogues common failure patterns observed across conditions and provides qualitative assessment of reasoning quality. Failure modes are identified during output normalization and scoring.

---

## 2. Failure Mode Taxonomy

### 2.1 Omission Failures

**Definition**: Critical content expected but absent from the output.

| Sub-type | Description | Example |
|---|---|---|
| Contributing factor omission | Major contributing factor from gold standard not identified | Environmental factors missed when focus is on individual error |
| Section omission | One of 8 expected sections entirely absent | No Just Culture assessment produced |
| Level omission | Contributing factors at only 1-2 levels, missing key levels | Only individual factors; no organisational analysis |
| Temporal omission | Critical time periods or events missing from chronology | Pre-event context absent; only immediate events described |

### 2.2 Commission Failures

**Definition**: Incorrect or fabricated content produced.

| Sub-type | Description | Example |
|---|---|---|
| Hallucinated framework | Model invents a non-existent investigation method | "Applied the Henderson Causal Model" (no such method) |
| Fabricated details | Clinical details added that are not in the case narrative | Specific lab values or medications not mentioned in source |
| Incorrect classification | Wrong SAC level, wrong Just Culture category, wrong action strength | SAC 3 for a death event; "reckless" for a system-induced error |
| Framework misapplication | Named method applied incorrectly | Fishbone categories don't match standard healthcare categories |

### 2.3 Structural Failures

**Definition**: Output poorly organized or sections conflated.

| Sub-type | Description | Example |
|---|---|---|
| Section conflation | Root causes mixed with contributing factors | "Root causes" section lists contributing factors |
| Disorganized output | Content scattered across sections without clear structure | Recommendations embedded in analysis, not in recommendations section |
| Incomplete structure | Section present but substantively empty | "Chronology: Events occurred over several days" (no actual timeline) |

### 2.4 Depth Failures

**Definition**: Analysis lacks sufficient depth to be clinically useful.

| Sub-type | Description | Example |
|---|---|---|
| Surface analysis | Factors identified but not explored in depth | "Communication was a factor" without specifying what, when, between whom |
| Stopped at human error | Root cause is individual action, not system condition | "Root cause: nurse did not check allergies" |
| No causal chain | Factors listed without causal reasoning | Bullet list of factors with no "because" relationships |
| Recommendation vagueness | Actions are generic, not specific to findings | "Improve communication" without specifying mechanism |

### 2.5 Specificity Failures

**Definition**: Content is too generic to be actionable.

| Sub-type | Description | Example |
|---|---|---|
| Generic recommendations | Recommendations not linked to specific root causes | "Provide education on medication safety" (for what specific gap?) |
| Template language | Output reads like a generic template, not case-specific | Same contributing factors listed regardless of case specifics |
| Missing SMART actions | Actions lack specificity, measurability, owners, timelines | "Review policy" (which policy? by whom? by when? measuring what?) |

### 2.6 Bias Failures

**Definition**: Output demonstrates inappropriate blame attribution or bias.

| Sub-type | Description | Example |
|---|---|---|
| Blame language | Individual-focused blame without system context | "The nurse should have known better" |
| Incorrect Just Culture | Wrong classification on the Just Culture spectrum | System-induced error classified as "at-risk behaviour" |
| Hindsight bias | Analysis assumes information was available that wasn't knowable at the time | "The team should have recognized the deterioration" when vital signs were ambiguous |
| Authority gradient bias | Disproportionate blame on junior staff without examining supervisory/system factors | Focus on nurse error without examining medical oversight |

### 2.7 Truncation/Technical Failures

**Definition**: Technical issues preventing complete output.

| Sub-type | Description | Example |
|---|---|---|
| Output truncation | Analysis cut short by token limit | Output ends mid-sentence in contributing factors section |
| Repetition loop | Model repeats content sections | Same contributing factors listed twice |
| Format failure | Output is not structured markdown | Plain text blob without headers or sections |
| Refusal | Model declines to perform the investigation | "I cannot conduct medical investigations" |

---

## 3. Failure Mode Frequency by Condition

| Failure Mode | H0 | H1 | H2 | H3 | H4 | H5 | H6 | H7 |
|---|---|---|---|---|---|---|---|---|
| Contributing factor omission | | | | | | | | |
| Section omission | | | | | | | | |
| Level omission | | | | | | | | |
| Temporal omission | | | | | | | | |
| Hallucinated framework | | | | | | | | |
| Fabricated details | | | | | | | | |
| Incorrect classification | | | | | | | | |
| Framework misapplication | | | | | | | | |
| Section conflation | | | | | | | | |
| Disorganized output | | | | | | | | |
| Surface analysis | | | | | | | | |
| Stopped at human error | | | | | | | | |
| No causal chain | | | | | | | | |
| Generic recommendations | | | | | | | | |
| Blame language | | | | | | | | |
| Incorrect Just Culture | | | | | | | | |
| Output truncation | | | | | | | | |
| Refusal | | | | | | | | |

(Cells contain count of occurrences across all cases × 3 runs)

---

## 4. Failure Mode Frequency by Difficulty

| Failure Mode | Simple (1) | Moderate (2) | Complex (3) |
|---|---|---|---|
| Contributing factor omission | | | |
| Surface analysis | | | |
| Stopped at human error | | | |
| Generic recommendations | | | |
| ... | | | |

---

## 5. Qualitative Assessment of Reasoning Quality

### 5.1 Causal Reasoning Depth

For each condition, assess the depth of causal reasoning observed:

| Condition | Typical Causal Depth | Example |
|---|---|---|
| H0 | | |
| H1 | | |
| H2 | | |
| H3 | | |
| H4 | | |
| H5 | | |

**Depth levels**:
1. **Descriptive**: Lists what happened (no causation)
2. **Proximate**: Identifies immediate causes ("drug administered because...")
3. **Contributing**: Identifies factors that enabled the error
4. **Systemic**: Traces to system conditions (policies, resources, culture)
5. **Multi-level**: Connects across individual → team → organisation → system

### 5.2 Use of Investigation Frameworks

For conditions with SKILL.md access, assess how the skill's methods were used:

| Condition | Methods Referenced | Methods Applied Correctly | Methods Applied Partially | Methods Misapplied |
|---|---|---|---|---|
| H1 | | | | |
| H2 | | | | |
| H3 | | | | |
| H4 | | | | |
| H5 | | | | |

### 5.3 Notable Examples

**Strongest investigation output** (across all conditions):
- Case: TBD
- Condition: TBD
- What made it strong: TBD

**Weakest investigation output**:
- Case: TBD
- Condition: TBD
- What made it weak: TBD

**Most improved by skill** (largest H1 - H0 gap):
- Case: TBD
- Key dimensions: TBD
- What the skill added: TBD

---

## 6. Condition-Specific Failure Patterns

### H0 — Control (No Skill)
[Common failure patterns specific to the no-skill condition]

### H1 — Claude Code + Sonnet + Skill
[Common failure patterns specific to the baseline skill condition]

### H2 — Claude Code + Opus + Skill
[Common failure patterns — does Opus avoid H1's failures?]

### H3–H5 — Cross-Model Injected
[Common failure patterns in cross-model transfer]

### H6–H7 — Alternative Harnesses
[Common failure patterns in alternative harnesses]

---

## 7. Key Findings

[To be completed after analysis]

1. What are the most common failure modes across all conditions?
2. Which failure modes does the skill suite prevent vs not prevent?
3. Are there failure modes unique to specific models or harnesses?
4. Do failure modes correlate with case difficulty?
5. What are the implications for skill suite improvement?
