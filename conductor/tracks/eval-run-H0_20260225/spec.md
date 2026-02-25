# H0 Run: Raw API Control (No Skill)

## Overview

Run all collected cases through the Raw API (Claude Sonnet, no SKILL.md, Prompt N) with 3 independent runs each. Capture full metadata and normalize outputs into 8 standardized sections.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H0 |
| Harness | Raw API (direct claude-sonnet-4-6 call, no system prompt) |
| Skill Condition | C — no skill |
| Prompt Variant | **Prompt N** (naive control — generic 7-step investigation) |
| Runs per case | 3 independent sessions |
| Temperature | 0 |

## Prompt N (exact text — do not modify)

```
You are a healthcare quality and safety expert conducting an investigation
into the following clinical adverse event.

## Case Narrative
[paste standardized case narrative here]

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

## Output Locations

```
evaluation/results/H0-control-no-skill/
└── case-XX/
    ├── run-1/
    │   ├── raw-transcript.md
    │   ├── normalized-output.md
    │   └── scores.md (populated during scoring track)
    ├── run-2/
    └── run-3/
```

## Acceptance Criteria

- All cases run × 3 independent runs
- Each run: raw-transcript.md saved with full metadata header
- Each run: normalized-output.md with all 8 sections extracted
- Temperature=0, separate sessions, no cross-run context

## Dependencies

- eval-pilot-calibration_20260225 (rubric finalized before running)
- eval-case-collection_20260225 (cases must exist)
