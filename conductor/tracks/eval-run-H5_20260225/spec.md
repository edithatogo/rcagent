# H5 Run: Qwen CLI (Injected Skill)

## Overview

Run all cases through Qwen CLI with SKILL.md injected as system prompt, using Prompt S.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H5 |
| Harness | Qwen CLI |
| Model | Qwen (latest available) |
| Skill Condition | B — injected |
| Prompt Variant | **Prompt S** |
| Runs per case | 3 independent sessions |
| Temperature | 0 |

## Skill Injection Method

Pass SKILL.md content via system prompt parameter. Check Qwen CLI documentation for exact flag. Verify SKILL.md fits within Qwen context window before running.

> **OPERATOR ACTION REQUIRED**: Requires Qwen CLI installed and API access configured.

## Output Locations

```
evaluation/results/H5-qwen/
└── case-XX/run-N/{raw-transcript.md, normalized-output.md, scores.md}
```

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
- Qwen CLI installed and authenticated
