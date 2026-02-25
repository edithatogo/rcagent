# H4 Run: Codex CLI / GPT-4o (Injected Skill)

## Overview

Run all cases through Codex CLI (GPT-4o) with SKILL.md injected, using Prompt S.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H4 |
| Harness | Codex CLI |
| Model | GPT-4o |
| Skill Condition | B — injected |
| Prompt Variant | **Prompt S** |
| Runs per case | 3 independent sessions |
| Temperature | 0 |

## Skill Injection Method

Use `--system-prompt` flag or place in `.codex/instructions.md`:

```bash
# Option A: system prompt flag
codex --system-prompt /tmp/rcagent-system.md

# Option B: instructions file
cp /tmp/rcagent-system.md .codex/instructions.md
codex
```

Test both injection methods on pilot case to confirm SKILL.md is loaded before full runs.

> **OPERATOR ACTION REQUIRED**: Requires Codex CLI + OpenAI API key.

## Output Locations

```
evaluation/results/H4-codex-cli/
└── case-XX/run-N/{raw-transcript.md, normalized-output.md, scores.md}
```

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
- Codex CLI installed, OpenAI API key configured
