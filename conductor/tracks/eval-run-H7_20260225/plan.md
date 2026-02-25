# H7 Run Plan: GitHub Copilot (Injected Skill)

## Phase 1: Setup (OPERATOR)

- [ ] Task: Create .github/copilot-instructions.md from /tmp/rcagent-system.md
- [ ] Task: Verify Copilot picks up workspace instructions in a test session
- [ ] Task: Document Copilot version and underlying model

## Phase 2: Run All Cases (3 runs each) (OPERATOR)

- [ ] Task: case-01, run-1 — Copilot, injected skill, Prompt S, new session
    - [ ] Save raw-transcript.md with metadata (Copilot version, timestamp)
    - [ ] Normalize into normalized-output.md (8 sections)
- [ ] Task: case-01, run-2
- [ ] Task: case-01, run-3
- [ ] Task: case-02 through case-N, 3 runs each

## Phase 3: Quality Check

- [ ] Task: Verify injection method documented (workspace instructions vs chat context)
- [ ] Task: Verify all normalized-output.md have 8 sections
- [ ] Task: Document failure modes
