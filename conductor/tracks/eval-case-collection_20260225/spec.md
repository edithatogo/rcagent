# Evaluation Case Collection

## Overview

Research, select, and standardize 5-10 publicly available AU/NZ adverse event cases for the rcagent evaluation study. Cases serve as the input data for all experimental conditions and provide the gold standard for scoring.

## Functional Requirements

1. **Source research**: Search HDC NZ decisions, ACSQHC sentinel event reports, and AU/NZ coroner findings for eligible cases
2. **Case selection**: Apply inclusion/exclusion criteria from `evaluation/protocol/case-selection-criteria.md`
3. **Standardization**: Format each case using the template in case-selection-criteria.md Section 7
4. **Gold standard extraction**: Extract contributing factors, root causes, and recommendations from source investigations
5. **Difficulty rating**: Rate each case 1-3 using the criteria in case-selection-criteria.md Section 5
6. **Coverage verification**: Ensure the case set meets all coverage requirements (event type, severity, jurisdiction, difficulty)

## Acceptance Criteria

- Minimum 5, target 10 cases collected
- Event type coverage: >=1 each of medication, deterioration, falls, surgical, mental health
- Severity coverage: >=2 SAC 1, >=3 SAC 2
- Jurisdiction: >=2 AU, >=3 NZ
- Difficulty mix: 2-3 simple, 4-5 moderate, 2-3 complex
- Each case >=500 words narrative
- Gold standard findings extracted for each case
- All cases pass QA checklist (case-selection-criteria.md Section 8)
- datasets/README.md case index updated

## Out of Scope

- Running experimental conditions (separate track)
- Scoring (separate track)
