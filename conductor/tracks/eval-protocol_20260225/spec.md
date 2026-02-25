# Evaluation Protocol Development

## Overview

Create the complete scientific evaluation framework for validating the rcagent skill suite's investigation quality, including experimental design, evaluation rubric, literature basis, case selection criteria, and agent test protocol.

## Functional Requirements

1. **Scientific Protocol** (`evaluation/protocol/scientific-protocol.md`)
   - Targeted factorial design: Model x Harness x Skill Condition x Data
   - 9 experimental conditions (H0-H8)
   - Primary/secondary/tertiary objectives
   - Analysis plan with descriptive statistics and effect sizes
   - Limitations and ethics statement

2. **Evaluation Rubric** (`evaluation/protocol/evaluation-rubric.md`)
   - 8-dimension rubric (D1-D8) with 1-5 Likert scale
   - Detailed scoring anchors per level per dimension
   - Pilot calibration protocol
   - Inter-rater reliability subset plan

3. **Literature Review** (`evaluation/protocol/literature-review.md`)
   - Citations for all 14 investigation methods
   - RCA quality and limitations literature
   - AI in clinical domains references
   - Evaluation methodology citations

4. **Case Selection Criteria** (`evaluation/protocol/case-selection-criteria.md`)
   - Inclusion/exclusion criteria
   - Coverage requirements (event type, severity, jurisdiction, difficulty)
   - Difficulty rating system (1-3 scale)
   - Case standardization format

5. **Agent Test Protocol** (`evaluation/protocol/agent-test-protocol.md`)
   - Two prompt variants (Prompt S skill-aware, Prompt N naive control)
   - Per-harness injection instructions for 7 harnesses
   - Output capture, normalization (8 sections), blinding protocol
   - Reproducibility protocol (3 runs, temp=0)

6. **Infrastructure**
   - Dataset directory structure with source provenance
   - Results directory for 9 conditions x 3 runs
   - Analysis framework (CSV schema, 5 analysis templates)
   - Updated conductor context files

## Acceptance Criteria

- All 5 protocol documents present and internally consistent
- 8-dimension rubric with unambiguous anchors
- Two distinct prompt variants preventing control condition confound
- Blinding protocol documented
- Per-harness injection instructions for all 7 harnesses
- Output normalization rules for 8 sections
- Results infrastructure supporting all conditions
- Analysis templates ready for data population

## Out of Scope

- Actual case collection (separate track)
- Running experimental conditions (separate track)
- Scoring and analysis (separate tracks)
