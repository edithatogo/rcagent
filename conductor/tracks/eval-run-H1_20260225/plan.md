# H1 Run Plan: Claude Code + Sonnet (Native Skill)

## Phase 1: Setup

- [ ] Task: Confirm all cases available in evaluation/datasets/
- [ ] Task: Confirm rubric finalized (eval-pilot-calibration complete)
- [ ] Task: Verify SKILL.md loads correctly in Claude Code (check skills/rca-investigation/SKILL.md)

## Phase 2: Run All Cases (3 runs each)

- [ ] Task: case-01, run-1 — Claude Code + Sonnet, SKILL.md loaded natively, Prompt S, temp=0, new session
    - [ ] Save raw-transcript.md with metadata (model version, harness version, timestamp, tokens)
    - [ ] Normalize into normalized-output.md (8 sections)
- [ ] Task: case-01, run-2
- [ ] Task: case-01, run-3
- [ ] Task: case-02, run-1 through run-3
- [ ] Task: case-03, run-1 through run-3
- [ ] Task: case-04, run-1 through run-3
- [ ] Task: case-05, run-1 through run-3
- [ ] Task: (additional cases as collected)

## Phase 3: Quality Check

- [ ] Task: Verify all raw-transcript.md files have complete metadata headers
- [ ] Task: Verify all normalized-output.md files have all 8 sections
- [ ] Task: Document any failure modes in evaluation/analysis/failure-mode-analysis.md
