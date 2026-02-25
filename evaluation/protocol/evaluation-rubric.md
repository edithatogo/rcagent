# Evaluation Rubric — AI-Assisted RCA Investigation Quality

**Version**: 1.0
**Date**: 2026-02-25

---

## Overview

This rubric assesses the quality of Root Cause Analysis (RCA) investigation outputs across **8 dimensions** using a **1–5 Likert scale**. It is derived from the ACSQHC National RCA Guidelines, Joint Commission RCA² standards, and the rcagent skill suite's `investigation-quality-checklist.md`.

**Scoring**: Each dimension scored 1–5 per case per condition per run.
**Composite**: Sum of D1–D8 (range 8–40).
**Primary analysis**: Per-dimension. **Secondary**: Composite.

---

## Dimension D1: Contributing Factor Completeness

**What it assesses**: Breadth and depth of contributing factor identification across multiple levels (individual, team, task, environment, organisation).

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | All major factors identified; multi-level analysis (individual, team, task, environment, organisation); factors prioritized by influence | Factors span ≥4 Yorkshire categories; each factor has evidence cited; factor interactions described |
| **4** — Good | Most major factors identified; at least 3 levels addressed; minor gaps in depth | Factors span ≥3 categories; most have evidence; some interactions noted |
| **3** — Acceptable | Most major factors present; ≥2 levels addressed; some omissions but no critical gaps | Factors span ≥2 categories; some evidence cited; limited interaction analysis |
| **2** — Below acceptable | Significant gaps; factors predominantly at one level; critical contributing factors missed | Factors mostly individual-level; limited evidence; no interaction analysis |
| **1** — Inadequate | Surface-level; major gaps; factors are symptoms not causes | Single category or vague factors; no evidence; essentially a list of complaints |

**Reference standard**: Compare against contributing factors identified in the published source investigation. A score of 3 requires identification of ≥60% of major factors found in the source.

---

## Dimension D2: Root Cause Accuracy

**What it assesses**: Whether system root causes are distinguished from proximate/contributing factors; clarity of causal chain reasoning.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | System root causes clearly distinguished from proximate causes; causal chain explicitly traced from event → contributing factors → root causes; root causes are actionable system-level issues | Clear "because" chain; root causes are system conditions; proximate causes labeled as such |
| **4** — Good | Root causes identified at system level; some causal chain reasoning; minor conflation between contributing and root causes | Most root causes are systemic; reasoning present but not always explicit |
| **3** — Acceptable | Root causes identified but sometimes conflated with contributing factors; some system-level analysis | At least one true system root cause; some causal reasoning; distinction attempted |
| **2** — Below acceptable | Root causes are actually contributing factors relabeled; limited system thinking; stopped at individual/team level | "Root causes" are proximate causes; no system conditions identified |
| **1** — Inadequate | Stopped at human error; no system analysis; root cause is "staff didn't follow protocol" | Blame-attributing language; no causal chain; individual action treated as root cause |

**Reference standard**: Compare against root causes identified in the source investigation. Bonus points for identifying system root causes the source investigation missed.

---

## Dimension D3: Action Strength Quality

**What it assesses**: Whether recommendations use the RCA² action hierarchy; whether strong/intermediate actions dominate over weak actions; whether each root cause has at least one action.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Majority strong/intermediate actions; each root cause addressed; actions are specific, measurable, with named owners and timelines; strength explicitly classified | ≥70% strong/intermediate; all root causes covered; SMART format; explicit strength labels |
| **4** — Good | Mix favoring strong/intermediate; most root causes addressed; actions mostly specific | ≥50% strong/intermediate; most root causes covered; some specific detail |
| **3** — Acceptable | Mix of strong, intermediate, and weak; some root causes unaddressed; actions somewhat generic | Some strong actions present; some root causes covered; actions partially specific |
| **2** — Below acceptable | Predominantly weak actions (training, policy review); several root causes unaddressed | >70% weak actions; missing root cause coverage; generic actions |
| **1** — Inadequate | Training/education/reminders only; no system-level actions; no link to root causes | All actions are "re-educate staff" or "remind team"; no design changes |

**RCA² Action Strength Hierarchy** (reference):
- **Strong**: Architectural/physical changes, engineering controls, forcing functions, simplification, standardization
- **Intermediate**: Increased staffing, redundancy, software enhancements, checklists with independent verification
- **Weak**: Training/education, new policy/procedure, memos/reminders, additional study

---

## Dimension D4: Just Culture Appropriateness

**What it assesses**: Whether individual accountability is assessed fairly using a Just Culture framework (human error vs at-risk behaviour vs reckless behaviour); whether system context is provided.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Correct classification with full system context; distinguishes human error, at-risk, and reckless behaviour; avoids blame; considers substitution test | Explicit Just Culture framework applied; system conditions that shaped behaviour identified; substitution test referenced |
| **4** — Good | Correct classification; system context provided; avoids blame | Just Culture categories referenced; some system context; no blame language |
| **3** — Acceptable | Classification broadly correct; limited system context; no overt blame | Accountability mentioned; system factors acknowledged; neutral tone |
| **2** — Below acceptable | Classification unclear or oversimplified; limited system context; some blame undertones | Vague accountability statements; individual focus without system context |
| **1** — Inadequate | Incorrect classification or overtly blame-focused; no Just Culture lens | Individuals named as causes; punitive tone; "should have known better" language |

**N/A**: Score N/A if the case narrative does not contain sufficient information for accountability assessment. Replace with mean of other dimensions for composite calculation.

---

## Dimension D5: De-identification Compliance

**What it assesses**: Whether all patient, staff, and location identifiers are properly removed or replaced with placeholders.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Fully compliant; consistent use of de-identification placeholders; no identifiable information; CONFIDENTIAL marking applied | [Patient A], [Case ID], [Ward X] used consistently; no names, dates of birth, MRN, or specific locations that could re-identify |
| **4** — Good | Compliant; minor inconsistency in placeholder usage but no real re-identification risk | Mostly consistent placeholders; occasional specific but non-identifying detail |
| **3** — Acceptable | Minor lapses in de-identification; no real re-identification risk in context | Some specific details retained but not individually identifying |
| **2** — Below acceptable | Notable lapses; potential re-identification risk from combination of details | Specific dates, locations, or role descriptions that could narrow identification |
| **1** — Inadequate | Identifiable information present; names, MRN, or specific locations included | Direct identifiers present; clear re-identification possible |

**Note**: Since input case narratives are already publicly available de-identified documents, this dimension primarily tests whether the AI maintains de-identification (doesn't fabricate identifying details) and applies the rcagent de-identification convention.

---

## Dimension D6: Method Selection Appropriateness

**What it assesses**: Whether investigation methods were explicitly selected and whether the selection matches the event's SAC level and characteristics.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Methods explicitly selected with rationale; match SAC level per selection matrix; method combination appropriate for event complexity; selection considers event characteristics (latent vs active, single vs multi-cause) | Named methods with "because" rationale; matches rcagent matrix; appropriate combination |
| **4** — Good | Methods selected and named; reasonable match to event; minor deviation from optimal selection | Methods named; generally appropriate; rationale present but brief |
| **3** — Acceptable | Reasonable method choice; minor mismatch with SAC level or event characteristics; implicit rather than explicit selection | Method recognizable from output structure; somewhat appropriate; selection not explicitly discussed |
| **2** — Below acceptable | Methods poorly matched to event; over- or under-investigation for SAC level; no explicit selection rationale | Wrong complexity level for the event; no rationale; method applied mechanically |
| **1** — Inadequate | No explicit method selection; inappropriate methods; or no recognizable methodology at all | Free-form analysis with no methodological structure; or completely wrong method for event type |

**Reference**: rcagent method selection matrix — SAC 1: Timeline + Yorkshire + Bow-Tie + SEIPS; SAC 2: Timeline + Yorkshire + Fishbone or London Protocol; SAC 3: 5 Whys + Contributing Factors; SAC 4: 5 Whys.

---

## Dimension D7: Chronology/Timeline Quality

**What it assesses**: Accuracy, completeness, and utility of the event chronology/timeline.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Complete, accurate chronology; multiple evidence sources cross-referenced; critical intervals and gaps identified; includes pre-event context and systemic timeline | All key events present; times/sequence correct; gaps explicitly noted; "what else was happening" context; critical decision points marked |
| **4** — Good | Mostly complete chronology; accurate sequence; some critical intervals identified | Most key events; correct sequence; some gaps noted; decision points partially identified |
| **3** — Acceptable | Mostly accurate chronology; minor gaps or missing intervals; key events present | Major events included; generally correct sequence; limited gap analysis |
| **2** — Below acceptable | Incomplete chronology; some inaccuracies; missing critical events | Notable gaps; some sequence errors; critical events omitted; no interval analysis |
| **1** — Inadequate | Major inaccuracies; grossly incomplete; or no chronology produced | Wrong sequence; major events missing; or chronology section absent |

**Reference standard**: Compare against the timeline in the published source investigation (where available).

---

## Dimension D8: Safety-II / Systems Lens

**What it assesses**: Whether the investigation considers Work-as-Done vs Work-as-Imagined; whether it explores what usually goes right (resilience); whether it takes a systems perspective beyond individual blame.

| Score | Anchor | Indicators |
|---|---|---|
| **5** — Excellent | Explicit Work-as-Done vs Work-as-Imagined comparison; considers what usually goes right and why this time was different; identifies system conditions that normally support safe performance; resilience perspective | WAD/WAI explicitly discussed; "why does this usually go well?" answered; system resilience factors identified; Safety-II language |
| **4** — Good | Some WAD/WAI comparison; systems perspective present; limited but genuine resilience thinking | WAD/WAI touched on; system conditions discussed; some "what usually goes right" content |
| **3** — Acceptable | Some systems thinking present; limited Safety-II; focuses on what went wrong but acknowledges system context | System factors mentioned; no explicit WAD/WAI; brief acknowledgment of normal variation |
| **2** — Below acceptable | Minimal systems thinking; almost entirely Safety-I (what went wrong); individuals as primary unit of analysis | Some system mention but individual focus dominates; no resilience perspective |
| **1** — Inadequate | Purely Safety-I; no systems perspective; individuals blamed; no consideration of normal work variation | Linear cause-effect; "if only X had done Y"; no system conditions; no resilience |

---

## Scoring Procedure

### Per-Run Scoring

For each case × condition × run:

1. Read the **normalized output** (not raw transcript)
2. Read the **source investigation findings** (gold standard)
3. Score each dimension D1–D8 using the anchors above
4. Record score and brief scoring rationale (1–2 sentences per dimension)
5. Record additional metrics: time to completion, token usage, cost, word count, structural completeness

### Structural Completeness Checklist

For each output, record presence (1) or absence (0) of:

| Section | Present? |
|---|---|
| SAC Classification | |
| Investigation Methods Selected | |
| Chronology/Timeline | |
| Contributing Factors | |
| Root Causes | |
| Just Culture Assessment | |
| Recommendations | |
| CAPA Action Plan | |

**Structural completeness score**: Count of present sections (0–8).

### Score Aggregation

1. **Per condition per case**: Mean of 3 runs per dimension
2. **Per condition**: Mean across all cases per dimension
3. **Composite**: Sum of 8 dimension means per condition (range 8–40)

---

## Pilot Calibration Protocol

### Purpose

Ensure rubric anchors are unambiguous and produce consistent scoring before full evaluation.

### Procedure

1. **Select 2 pilot cases**: 1 AU case (moderate difficulty), 1 NZ case (complex difficulty)
2. **Run 2 conditions**: H1 (Claude Code + skill, baseline) and H0 (Raw API, control)
3. **Score all 4 outputs** (2 cases × 2 conditions) using this rubric
4. **Document**: For each dimension, record:
   - Score given
   - Scoring rationale (detailed, 3–5 sentences)
   - Difficulty of scoring (Easy / Moderate / Hard)
   - Suggested anchor refinement (if Hard)
5. **Review**: If any dimension scored "Hard" to apply:
   - Revise anchor wording
   - Add concrete examples
   - Re-score and verify improved clarity
6. **Document all changes** in Appendix A below

### Acceptance Criteria

- All 8 dimensions scorable without ambiguity on both pilot outputs
- No dimension requires >30 seconds of deliberation
- Scoring rationale for each dimension is expressible in ≤3 sentences

### Appendix A: Pilot Calibration Log

| Date | Case | Condition | Dimension | Original Score | Revised Score | Anchor Change | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

(To be completed during pilot calibration phase.)

---

## Inter-Rater Reliability Subset

### Selection

From the full evaluation, select:
- 3 cases (1 simple, 1 moderate, 1 complex)
- 3 conditions (H0, H1, H3)
- = 9 outputs total

### Procedure

1. Human evaluator scores all 9 blind
2. Claude Opus scores all 9 blind (rubric provided as system prompt with instructions to score the normalized output against the source investigation findings)
3. Calculate Cohen's kappa per dimension
4. Threshold: kappa ≥ 0.6 (moderate agreement) required for each dimension
5. If kappa < 0.6: revise dimension anchors and repeat

### AI Rater Prompt

```
You are evaluating the quality of a Root Cause Analysis investigation output.

## Source Investigation Findings
[Published source investigation summary]

## Output to Evaluate
[Normalized output]

## Rubric
[Full rubric text for the dimension being scored]

## Task
Score this output on the dimension described above using a 1-5 scale.
Provide: (1) the score, (2) a 2-3 sentence rationale referencing specific
elements of the output and the rubric anchors.
```
