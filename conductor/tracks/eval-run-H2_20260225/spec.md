# H2 Run: Claude Code + Opus (Native Skill)

## Overview

Identical to H1 but using Claude Opus instead of Sonnet. Tests the impact of model quality when the skill suite is held constant.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H2 |
| Harness | Claude Code (claude-opus-4-6) |
| Skill Condition | A — native (SKILL.md loaded from working directory) |
| Prompt Variant | **Prompt S** (skill-aware — minimal) |
| Runs per case | 3 independent sessions |
| Temperature | 0 |

## Skill Injection

Native — SKILL.md loaded from `skills/rca-investigation/SKILL.md`. Switch model to claude-opus-4-6 via Claude Code model setting.

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
evaluation/results/H2-claude-code-opus/
└── case-XX/
    ├── run-1/
    │   ├── raw-transcript.md
    │   ├── normalized-output.md
    │   └── scores.md
    ├── run-2/
    └── run-3/
```

## Acceptance Criteria

- All cases run × 3 independent sessions using Opus model
- Model version recorded in each raw-transcript.md metadata
- Each run: normalized-output.md with 8 sections

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
