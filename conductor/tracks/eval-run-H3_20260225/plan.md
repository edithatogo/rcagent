# H3 Run Plan: Gemini CLI (Injected Skill)

## Phase 1: Setup (OPERATOR)

- [ ] Task: Build skill injection file
    - [ ] Concatenate SKILL.md + method-selection-matrix.md + just-culture-guide.md into /tmp/rcagent-system.md
    - [ ] Verify token count fits Gemini context window
- [ ] Task: Verify Gemini CLI version and document
- [ ] Task: Test injection on a dummy prompt to confirm SKILL.md is loaded

## Phase 2: Run All Cases (3 runs each) (OPERATOR)

- [ ] Task: case-01, run-1 — Gemini CLI, injected skill, Prompt S, temp=0, new session
    - [ ] Save raw-transcript.md with metadata (model version, CLI version, timestamp)
    - [ ] Normalize into normalized-output.md (8 sections)
- [ ] Task: case-01, run-2
- [ ] Task: case-01, run-3
- [ ] Task: case-02 through case-N, 3 runs each

## Phase 3: Quality Check

- [ ] Task: Verify injection method documented in all raw-transcript.md metadata headers
- [ ] Task: Verify all normalized-output.md files have all 8 sections
- [ ] Task: Document failure modes
