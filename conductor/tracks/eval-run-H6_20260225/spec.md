# H6 Run: Kilo Code (Injected Skill)

## Overview

Run all cases through Kilo Code IDE extension with SKILL.md injected via custom instructions, using Prompt S.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H6 |
| Harness | Kilo Code (VS Code extension) |
| Model | Model configured in Kilo Code settings |
| Skill Condition | B — injected via custom instructions |
| Prompt Variant | **Prompt S** |
| Runs per case | 3 independent sessions |
| Temperature | 0 (set in Kilo Code settings) |

## Skill Injection Method

In Kilo Code settings, paste SKILL.md content into the "Custom Instructions" / "System Prompt" field before each session. Verify the skill content appears in the system context before running cases.

> **OPERATOR ACTION REQUIRED**: Requires Kilo Code VS Code extension installed and configured. UI-based injection — document exact steps taken for reproducibility.

## Output Locations

```
evaluation/results/H6-kilo-code/
└── case-XX/run-N/{raw-transcript.md, normalized-output.md, scores.md}
```

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
- Kilo Code installed in VS Code with model API access
