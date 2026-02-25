# H7 Run: GitHub Copilot (Injected Skill)

## Overview

Run all cases through GitHub Copilot with SKILL.md injected via `.github/copilot-instructions.md`, using Prompt S.

## Condition Details

| Field | Value |
|---|---|
| Condition ID | H7 |
| Harness | GitHub Copilot (VS Code) |
| Model | Copilot default model |
| Skill Condition | B — injected via workspace instructions |
| Prompt Variant | **Prompt S** |
| Runs per case | 3 independent sessions |
| Temperature | not configurable — document default |

## Skill Injection Method

```bash
# Create Copilot workspace instructions
mkdir -p .github
cp /tmp/rcagent-system.md .github/copilot-instructions.md
```

Verify Copilot picks up the instructions by checking the system context in a test session before running cases. Also test chat context injection as an alternative if workspace instructions don't load correctly.

> **OPERATOR ACTION REQUIRED**: Requires GitHub Copilot subscription and VS Code extension. Document exact injection method used.

## Output Locations

```
evaluation/results/H7-copilot/
└── case-XX/run-N/{raw-transcript.md, normalized-output.md, scores.md}
```

## Dependencies

- eval-pilot-calibration_20260225
- eval-case-collection_20260225
- GitHub Copilot subscription + VS Code
