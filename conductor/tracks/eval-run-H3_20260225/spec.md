# H3 Run: Gemini CLI (Injected Skill)

## Overview

Run all cases through Gemini CLI with SKILL.md injected as system prompt, using Prompt S. Requires Gemini CLI installed and authenticated on the operator's machine.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H3 |
| Harness | Gemini CLI |
| Model | Gemini Pro (latest available) |
| Skill Condition | B — injected (SKILL.md as system prompt) |
| Prompt Variant | **Prompt S** (skill-aware) |
| Runs per case | 3 independent sessions |
| Temperature | 0 (or lowest available) |

## Skill Injection Method

Concatenate SKILL.md + key references into a system prompt file, then pass via `--system-prompt` flag or Gemini CLI config:

```bash
# Build injection file
cat skills/rca-investigation/SKILL.md > /tmp/rcagent-system.md
echo "" >> /tmp/rcagent-system.md
cat skills/rca-investigation/references/method-selection-matrix.md >> /tmp/rcagent-system.md
cat skills/rca-investigation/references/just-culture-guide.md >> /tmp/rcagent-system.md

# Verify token count fits context window before running
# Run with injection
gemini --system-prompt /tmp/rcagent-system.md
```

> **OPERATOR ACTION REQUIRED**: This track cannot be run by a Claude subagent. Must be executed by a human operator with Gemini CLI installed.

## Output Locations

```
evaluation/results/H3-gemini-cli/
└── case-XX/
    ├── run-1/
    │   ├── raw-transcript.md
    │   ├── normalized-output.md
    │   └── scores.md
    ├── run-2/
    └── run-3/
```

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
- Gemini CLI installed and authenticated
