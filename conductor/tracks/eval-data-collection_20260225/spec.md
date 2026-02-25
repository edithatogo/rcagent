# Evaluation Data Collection

## Overview

Execute all 8 AI experimental conditions (H0-H7) across all collected cases with 3 independent runs each. Capture full raw transcripts with metadata, normalize outputs into 8 standardized sections, and prepare for blinded scoring.

## Functional Requirements

1. **Condition execution**: Run all 8 AI conditions per the agent-test-protocol.md
2. **Per-run metadata**: Record model version, harness version, temperature, timestamps, token counts, cost
3. **Output capture**: Save full raw transcripts to results/{condition}/case-XX/run-N/raw-transcript.md
4. **Output normalization**: Extract 8 sections into normalized-output.md per run
5. **Human condition (H8)**: Obtain single human expert output per case
6. **Blinding preparation**: Generate random eval IDs, create blinding-map.csv, create scored copies

## Acceptance Criteria

- All 8 AI conditions run on all cases, 3 runs each
- H8 human expert run for all cases (1 run each)
- All raw transcripts saved with complete metadata
- All outputs normalized into 8 standardized sections
- Blinding map complete and sealed (not revealed until scoring complete)
- Failure modes documented during normalization

## Dependencies

- eval-case-collection_20260225 (cases needed)
- eval-pilot-calibration_20260225 (rubric finalized before running)

## Out of Scope

- Rubric scoring (separate track)
