# Agent Test Protocol — AI-Assisted RCA Evaluation

**Version**: 1.0
**Date**: 2026-02-25

---

## 1. Overview

This document specifies the exact procedures for running each experimental condition, including prompt variants, per-harness skill injection methods, output capture, normalization, blinding, and reproducibility requirements.

---

## 2. Experimental Conditions

| ID | Model | Harness | Skill Condition | Prompt | Runs |
|---|---|---|---|---|---|
| H0 | Claude Sonnet 4.6 | Raw API | None (C) | Prompt N (Naive) | 3 per case |
| H1 | Claude Sonnet 4.6 | Claude Code | Native (A) | Prompt S (Skill-aware) | 3 per case |
| H2 | Claude Opus 4.6 | Claude Code | Native (A) | Prompt S (Skill-aware) | 3 per case |
| H3 | Gemini Pro | Gemini CLI | Injected (B) | Prompt S (Skill-aware) | 3 per case |
| H4 | GPT-4o | Codex CLI | Injected (B) | Prompt S (Skill-aware) | 3 per case |
| H5 | Qwen | Qwen CLI | Injected (B) | Prompt S (Skill-aware) | 3 per case |
| H6 | Various | Kilo Code | Injected (B) | Prompt S (Skill-aware) | 3 per case |
| H7 | Various | Copilot | Injected (B) | Prompt S (Skill-aware) | 3 per case |
| H8 | Human Expert | — | Provided as ref | N/A | 1 per case |

**Total AI runs**: 8 conditions × N cases × 3 runs = 24N transcripts (e.g., 240 for 10 cases).

---

## 3. Prompt Variants

### 3.1 Prompt S — Skill-Aware

Used for conditions A (skill-native) and B (prompt-injected), where SKILL.md content is available to the agent.

```
You are conducting a Root Cause Analysis investigation for the following
clinical adverse event.

## Case Narrative
{CASE_NARRATIVE}

## Task
Follow the RCA investigation workflow: triage → investigate → report.
Produce all outputs in structured markdown format.
```

**Rationale**: This prompt is deliberately minimal in task instruction. It relies on SKILL.md to guide:
- SAC classification and method selection (via method-selection-matrix)
- Contributing factor analysis (via Yorkshire Framework or selected method)
- Just Culture assessment (via just-culture-guide)
- Action strength classification (via RCA² methodology)
- Report structure (via templates)
- Safety-II lens (via safety-ii-principles)

The difference between this prompt + SKILL.md and Prompt N alone isolates the skill suite's contribution.

### 3.2 Prompt N — Naive Control

Used for condition C (no skill). No SKILL.md content is provided.

```
You are a healthcare quality and safety expert conducting an investigation
into the following clinical adverse event.

## Case Narrative
{CASE_NARRATIVE}

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

**Rationale**: Generic investigation language that:
- Does NOT name any specific framework (no Yorkshire, no RCA², no SEIPS)
- Does NOT reference method selection matrices or severity classification systems
- DOES provide a basic task structure (7 steps) to ensure some structural output
- Tests what the model produces from its training knowledge alone

The 7-step task list uses neutral language ("factors that contributed" not "contributing factors using the Yorkshire Framework") to avoid methodological cueing.

---

## 4. Per-Harness Skill Injection Methods

### 4.1 Condition A — Skill-Native (H1, H2)

**Harness**: Claude Code

**Setup**:
1. Ensure the `rca/` repo is the working directory
2. SKILL.md is in `skills/rca-investigation/SKILL.md`
3. Claude Code loads the skill natively through its skill discovery mechanism
4. The skill suite's references and templates are accessible via the file system

**Execution**:
```bash
# Start new Claude Code session
claude

# In session, provide Prompt S with case narrative
# The skill is available through the working directory
```

**Verification**: Confirm the agent references skill content (method names, templates) in its output. If the output shows no evidence of skill loading, note in run metadata and investigate.

### 4.2 Condition B — Prompt-Injected (H3, H4, H5, H6, H7)

The full content of SKILL.md (plus key referenced files) is provided as system-level instructions. Due to context window limitations, provide a condensed version including:

1. SKILL.md (full content)
2. `references/method-selection-matrix.md` (full)
3. `references/just-culture-guide.md` (full)
4. `references/safety-ii-principles.md` (key sections)
5. `references/investigation-quality-checklist.md` (full)

**Total injected content target**: <15,000 tokens (verify per model context window).

If the full injection exceeds the model's system prompt limit, prioritize in order: SKILL.md > method-selection-matrix > just-culture-guide > quality-checklist > safety-ii-principles.

#### H3 — Gemini CLI

**Setup**:
```bash
# Create system instruction file
cat skills/rca-investigation/SKILL.md > /tmp/rcagent-system.md
cat skills/rca-investigation/references/method-selection-matrix.md >> /tmp/rcagent-system.md
cat skills/rca-investigation/references/just-culture-guide.md >> /tmp/rcagent-system.md
cat skills/rca-investigation/references/safety-ii-principles.md >> /tmp/rcagent-system.md
cat skills/rca-investigation/references/investigation-quality-checklist.md >> /tmp/rcagent-system.md
```

**Execution**:
```bash
# Use Gemini CLI with system prompt
gemini --system-prompt-file /tmp/rcagent-system.md
# Then provide Prompt S with case narrative
```

**Notes**: Verify Gemini CLI version supports `--system-prompt-file` flag. Alternative: use config file approach. Document actual flag used.

#### H4 — Codex CLI

**Setup**:
```bash
# Option 1: System prompt flag
# Option 2: .codex/instructions.md in working directory
mkdir -p .codex
cat skills/rca-investigation/SKILL.md > .codex/instructions.md
cat skills/rca-investigation/references/method-selection-matrix.md >> .codex/instructions.md
# ... (append other references)
```

**Execution**:
```bash
codex
# Provide Prompt S with case narrative
```

**Notes**: Test both injection methods. Document which is used. Remove `.codex/instructions.md` after testing to avoid contaminating other conditions.

#### H5 — Qwen CLI

**Setup**:
```bash
# Use system prompt parameter (verify exact syntax for current version)
# Prepare system prompt file as per H3
```

**Execution**:
```bash
qwen --system-prompt-file /tmp/rcagent-system.md
# Provide Prompt S with case narrative
```

**Notes**: Check token limits. Qwen models may have smaller context windows — may need to further condense injected content. Document actual content injected.

#### H6 — Kilo Code (IDE-based)

**Setup**:
1. Open the `rca/` repo in VS Code
2. Install Kilo Code extension (document version)
3. Navigate to Kilo Code settings → Custom Instructions
4. Paste the condensed SKILL.md + references content into the custom instructions field

**Execution**:
1. Open new Kilo Code chat session
2. Paste Prompt S with case narrative
3. Capture full output

**Notes**: IDE-based harness — document exact UI steps taken. Screenshot settings if possible for reproducibility.

#### H7 — GitHub Copilot

**Setup**:
1. Open the `rca/` repo in VS Code
2. Create/update `.github/copilot-instructions.md` with condensed SKILL.md + references

**Alternative**: Use Copilot Chat with workspace context:
1. Ensure SKILL.md is in the workspace
2. Use `@workspace` context in Copilot Chat

**Execution**:
```
# In Copilot Chat
@workspace [Prompt S with case narrative]
```

**Notes**: Test both approaches (copilot-instructions.md and @workspace). Document which method produces better skill utilization. Remove `.github/copilot-instructions.md` after testing.

### 4.3 Condition C — No Skill (H0)

**Harness**: Raw API call (Anthropic API)

**Setup**: Direct API call with no system prompt (or minimal system prompt: "You are a helpful assistant.").

**Execution**:
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6-20250514",  # Verify current model ID
    max_tokens=8192,
    temperature=0,
    messages=[
        {"role": "user", "content": PROMPT_B_WITH_CASE_NARRATIVE}
    ]
)
```

**Notes**: No system prompt containing skill content. The model receives only Prompt N (naive control) as a user message. Document exact model ID, API version, and all parameters.

---

## 5. Reproducibility Protocol

### 5.1 Per-Run Requirements

For EVERY run, record:

| Metadata | Where to Record |
|---|---|
| Condition ID (H0–H8) | Run folder name |
| Case ID | Run folder path |
| Run number (1–3) | Run folder name |
| Model ID (exact version string) | `raw-transcript.md` header |
| Harness name and version | `raw-transcript.md` header |
| Temperature setting | `raw-transcript.md` header |
| API endpoint / region | `raw-transcript.md` header |
| Timestamp start (ISO 8601) | `raw-transcript.md` header |
| Timestamp end (ISO 8601) | `raw-transcript.md` header |
| Input token count | `scores.md` metrics section |
| Output token count | `scores.md` metrics section |
| Total cost (USD) | `scores.md` metrics section |

### 5.2 Session Isolation

- Each run is a **fresh session** — no context carry-over from previous runs
- For CLI-based harnesses: start a new session/process for each run
- For API-based harnesses (H0): each run is an independent API call
- No multi-turn interaction — single prompt, single response
- If the harness requires clarification or asks a follow-up question, provide only: "Please proceed with the investigation based on the information provided."

### 5.3 Temperature and Sampling

- Temperature: 0 for all models (or lowest available setting if 0 is not supported)
- If the model does not support temperature=0, document the minimum available setting
- Do NOT use top-k or top-p sampling modifications unless the harness requires it (document if used)

### 5.4 Output Length

- Set max tokens to 8192 (or equivalent) for all conditions
- If output is truncated, note in run metadata and increase limit for subsequent runs
- If a harness does not support max token setting, document the default

---

## 6. Output Capture

### 6.1 Raw Transcript Format

Each run produces a `raw-transcript.md` with the following structure:

```markdown
# Raw Transcript

## Run Metadata

| Field | Value |
|---|---|
| Condition | [H0–H8] |
| Case | [case-id] |
| Run | [1/2/3] |
| Model | [exact model ID] |
| Harness | [name and version] |
| Temperature | [0 or actual setting] |
| Timestamp Start | [ISO 8601] |
| Timestamp End | [ISO 8601] |
| API Endpoint | [endpoint or N/A] |

## Prompt Sent

[Exact prompt text sent to the model, including case narrative]

## Raw Output

[Complete, unedited model output]
```

### 6.2 Output Word Count

Automated count of words in the "Raw Output" section. Record in `scores.md`.

---

## 7. Output Normalization

### 7.1 Purpose

Different models and harnesses produce different output formats and structures. To enable fair comparison, each raw output is normalized into 8 standardized sections before scoring.

Scoring is performed on the **normalized output**, not the raw transcript.

### 7.2 Normalization Procedure

From each raw transcript, extract the following 8 sections. If a section is not present in the output, mark as "ABSENT" in the normalized document.

#### Section 1: SAC Classification

Extract:
- SAC level assigned (1–4) or equivalent severity classification
- Rationale for classification
- If no explicit classification: note "No explicit SAC classification" and extract any severity language

#### Section 2: Investigation Methods Selected

Extract:
- Named methods (e.g., "Yorkshire Framework", "5 Whys", "Fishbone")
- Rationale for selection (if provided)
- If no explicit methods named: describe the approach used (e.g., "unstructured factor listing", "implicit fishbone categories")

#### Section 3: Chronology/Timeline

Extract:
- Chronological sequence of events
- Timestamps or relative timing
- Identified gaps, critical intervals, decision points
- If no timeline section: extract any temporal information from the narrative

#### Section 4: Contributing Factors

Extract all identified contributing factors, categorized by level:
- **Individual**: Knowledge, skill, physical/mental state, fatigue
- **Team**: Communication, supervision, handover, team dynamics
- **Task**: Complexity, clarity of procedures, protocol availability
- **Environment**: Equipment, staffing levels, workload, physical environment
- **Organisation**: Culture, policies, training systems, resourcing, governance

If the output uses different categories, map to the nearest level. If factors are not categorized, categorize them during normalization.

#### Section 5: Root Causes

Extract:
- Root causes explicitly labeled as such
- Distinction between proximate and systemic causes (if made)
- Causal chain reasoning (if present)
- If no explicit root causes: extract the deepest causal analysis present

#### Section 6: Just Culture Assessment

Extract:
- Classification of individual actions (human error, at-risk, reckless)
- System context provided for individual actions
- Substitution test (if applied)
- Tone assessment: blame-attributing vs system-focused
- If no explicit Just Culture section: extract any accountability language

#### Section 7: Recommendations

Extract all recommendations, classified by strength:
- **Strong**: Engineering controls, forcing functions, simplification, design changes
- **Intermediate**: Checklists, redundancy, software changes, staffing
- **Weak**: Training, education, policy, reminders
- If no strength classification in output: classify during normalization

#### Section 8: CAPA Action Plan

Extract:
- Specific actions with owners, timelines, and measures of success
- Link between actions and root causes
- Effectiveness review plan
- If no CAPA section: extract any action-oriented content

### 7.3 Normalized Output Format

```markdown
# Normalized Output

## Normalization Metadata

| Field | Value |
|---|---|
| Source | [raw-transcript.md path] |
| Normalized by | [name] |
| Date | [ISO 8601] |
| Notes | [any issues encountered during normalization] |

## Section 1: SAC Classification
[Extracted content or "ABSENT"]

## Section 2: Investigation Methods Selected
[Extracted content or "ABSENT"]

## Section 3: Chronology/Timeline
[Extracted content or "ABSENT"]

## Section 4: Contributing Factors
[Extracted and categorized content or "ABSENT"]

## Section 5: Root Causes
[Extracted content or "ABSENT"]

## Section 6: Just Culture Assessment
[Extracted content or "ABSENT"]

## Section 7: Recommendations
[Extracted and strength-classified content or "ABSENT"]

## Section 8: CAPA Action Plan
[Extracted content or "ABSENT"]
```

### 7.4 Normalization Rules

1. **Preserve content**: Extract verbatim where possible. Add categorization labels but do not rewrite content.
2. **Do not add content**: If the output does not address a topic, mark as ABSENT. Do not infer or supplement.
3. **Categorization only**: When categorizing factors or classifying recommendation strength, use the standardized categories above. Note in metadata if categorization was ambiguous.
4. **Cross-section duplication**: If the same content appears in multiple sections of the raw output, include it in the most appropriate normalized section. Do not duplicate across sections.
5. **Preserving structure**: Maintain bullet points, numbering, and sub-sections from the raw output where they map to a normalized section.

---

## 8. Blinding Protocol

### 8.1 Purpose

Prevent evaluator knowledge of which condition produced which output from biasing rubric scores.

### 8.2 Procedure

**After all runs are complete and normalized (before scoring begins):**

1. **Generate random IDs**: For each normalized output, generate a random evaluation ID:
   - Format: `eval-XXXX-case-NN` where XXXX is 4 random alphanumeric characters
   - Example: `eval-K7F2-case-03`

2. **Strip condition metadata**: Create scoring copies of normalized outputs with:
   - Run metadata section removed
   - File renamed to evaluation ID
   - No folder structure that reveals condition

3. **Shuffle order**: For each case, randomize the order in which outputs are presented for scoring

4. **Record mapping**: Store the condition → evaluation ID mapping in `results/blinding-map.csv`:
   ```csv
   eval_id,condition,case,run,original_path
   eval-K7F2-case-03,H1,case-03,run-1,results/H1-claude-code-sonnet/case-03/run-1/normalized-output.md
   ```

5. **Seal mapping**: The blinding map is not opened until ALL scoring is complete

### 8.3 Unblinding

After all rubric scores are recorded:
1. Open `blinding-map.csv`
2. Merge scores with condition identifiers
3. Populate `analysis/rubric-scores.csv`
4. Begin analysis

---

## 9. Scoring Procedure

### 9.1 Scoring Template

Each run produces a `scores.md`:

```markdown
# Rubric Scores

## Identification

| Field | Value |
|---|---|
| Evaluation ID | [eval-XXXX-case-NN or condition/case/run if pre-blinding] |
| Scorer | [name] |
| Date | [ISO 8601] |

## Dimension Scores

| Dimension | Score (1-5) | Rationale |
|---|---|---|
| D1: Contributing Factor Completeness | | |
| D2: Root Cause Accuracy | | |
| D3: Action Strength Quality | | |
| D4: Just Culture Appropriateness | | |
| D5: De-identification Compliance | | |
| D6: Method Selection Appropriateness | | |
| D7: Chronology/Timeline Quality | | |
| D8: Safety-II / Systems Lens | | |

**Composite Score**: [sum of D1-D8, range 8-40]

## Structural Completeness

| Section | Present (1/0) |
|---|---|
| SAC Classification | |
| Investigation Methods Selected | |
| Chronology/Timeline | |
| Contributing Factors | |
| Root Causes | |
| Just Culture Assessment | |
| Recommendations | |
| CAPA Action Plan | |

**Structural Completeness**: [count] / 8

## Additional Metrics

| Metric | Value |
|---|---|
| Time to completion (seconds) | |
| Input tokens | |
| Output tokens | |
| Cost (USD) | |
| Output word count | |
```

### 9.2 Scoring Order

1. Score ALL outputs for one case before moving to the next case
2. Within a case, score in the randomized (blinded) order
3. Score all dimensions for one output before moving to the next output
4. Take a break between cases to prevent fatigue effects

---

## 10. Human Expert Condition (H8)

### 10.1 Setup

The human expert receives:
- The standardized case narrative (identical to AI conditions)
- Access to the rcagent skill suite documentation (as reference, not directive)
- Unlimited time

### 10.2 Instructions

```
You are conducting a Root Cause Analysis investigation for the following
clinical adverse event, using the information provided in the case narrative.

Produce a complete investigation including:
- Severity classification
- Investigation method selection
- Event chronology
- Contributing factor analysis
- Root cause identification
- Accountability/Just Culture assessment
- Recommendations with strength classification
- Action plan

Use any investigation methods and frameworks you consider appropriate.
You may reference the rcagent skill suite documentation as a resource.

Produce all outputs in structured markdown format.
```

### 10.3 Notes

- Human expert has the same information asymmetry as AI conditions (narrative only, not full clinical record)
- Human expert's output is NOT blinded during scoring (evaluator knows it is the human condition)
- Human expert produces a single output per case (not 3 runs) — no reproducibility analysis for H8
- The human condition serves as a benchmark, not a competitor — the question is "how close do AI conditions come?" not "does AI beat humans?"

---

## 11. Failure Mode Documentation

During output capture and normalization, document any of the following failure modes if they occur:

| Failure Mode | Description | Record In |
|---|---|---|
| **Refusal** | Model refuses to conduct the investigation | Run metadata |
| **Truncation** | Output is cut short mid-analysis | Run metadata |
| **Hallucinated framework** | Model invents a non-existent investigation method | Normalization notes |
| **Fabricated details** | Model adds clinical details not in the case narrative | Normalization notes |
| **Framework confusion** | Model conflates or misapplies a named method | Normalization notes |
| **Repetition/loop** | Model repeats sections or enters a loop | Run metadata |
| **Format failure** | Output is not structured markdown | Run metadata |
| **Off-topic** | Model produces content unrelated to RCA investigation | Run metadata |

These failure modes are catalogued in `analysis/failure-mode-analysis.md` after scoring.
