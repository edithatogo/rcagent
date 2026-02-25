# H8 Run: Human Expert (Gold Standard)

## Overview

Obtain a single human expert investigation output for each case. This serves as the gold standard reference condition. No blinding required for H8 outputs.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H8 |
| Harness | Human expert |
| Skill Condition | Skill suite provided as reference material |
| Prompt Variant | Prompt S provided as task framing |
| Runs per case | 1 (single run — no replication) |
| Output format | Structured markdown matching 8-section template |

## Expert Brief

Provide the human expert with:
1. The standardized case narrative for each case
2. Prompt S as the task framing
3. `evaluation/protocol/evaluation-rubric.md` as awareness context (not scoring guidance)
4. `skills/rca-investigation/SKILL.md` as optional reference material

The expert should produce investigation outputs matching the 8-section normalized format. Allow sufficient time (no time pressure that would degrade quality).

> **OPERATOR ACTION REQUIRED**: Coordinate with human expert. H8 is not automated.

## Output Locations

```
evaluation/results/H8-human-evaluator/
└── case-XX/
    ├── raw-transcript.md    (no run-N/ nesting — single run)
    └── normalized-output.md
```

Note: H8 has no `run-N/` subdirectory — single run per case only.

## Dependencies

- eval-case-collection_20260225 (cases needed)
- Human expert available and briefed
