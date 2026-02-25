# H1 Run: Claude Code + Sonnet (Native Skill)

## Overview

Run all collected cases through Claude Code with Sonnet and native SKILL.md loaded, using Prompt S (skill-aware, minimal). 3 independent runs per case.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H1 |
| Harness | Claude Code (claude-sonnet-4-6) |
| Skill Condition | A — native (SKILL.md loaded from working directory) |
| Prompt Variant | **Prompt S** (skill-aware — minimal, relies on SKILL.md) |
| Runs per case | 3 independent sessions |
| Temperature | 0 |

## Skill Injection

SKILL.md is loaded natively by Claude Code from `skills/rca-investigation/SKILL.md`. No additional injection needed — this is the designed operating path.

## Prompt S (exact text — do not modify)

```
You are conducting a Root Cause Analysis investigation for the following
clinical adverse event.

## Case Narrative
[paste standardized case narrative here]

## Task
Follow the RCA investigation workflow: triage → investigate → report.
Produce all outputs in structured markdown format.
```

## Output Locations

```
evaluation/results/H1-claude-code-sonnet/
└── case-XX/
    ├── run-1/
    │   ├── raw-transcript.md
    │   ├── normalized-output.md
    │   └── scores.md
    ├── run-2/
    └── run-3/
```

## Acceptance Criteria

- All cases run × 3 independent sessions
- SKILL.md confirmed loaded at start of each session
- Each run: raw-transcript.md with full metadata
- Each run: normalized-output.md with 8 sections

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
