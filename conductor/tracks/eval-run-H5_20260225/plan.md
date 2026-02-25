# H5 Run Plan: Qwen CLI (Injected Skill)

## Phase 1: Setup (OPERATOR)

- [ ] Task: Build skill injection file (/tmp/rcagent-system.md)
- [ ] Task: Identify Qwen CLI system prompt flag and verify context window
- [ ] Task: Verify Qwen CLI version and model

## Phase 2: Run All Cases (3 runs each) (OPERATOR)

- [ ] Task: case-01, run-1 — Qwen CLI, injected skill, Prompt S, temp=0, new session
    - [ ] Save raw-transcript.md with metadata
    - [ ] Normalize into normalized-output.md (8 sections)
- [ ] Task: case-01, run-2
- [ ] Task: case-01, run-3
- [ ] Task: case-02 through case-N, 3 runs each

## Phase 3: Quality Check

- [ ] Task: Verify injection confirmed in metadata headers
- [ ] Task: Verify all normalized-output.md have 8 sections
- [ ] Task: Document failure modes
