# H4 Run Plan: Codex CLI / GPT-4o (Injected Skill)

## Phase 1: Setup (OPERATOR)

- [ ] Task: Build skill injection file (/tmp/rcagent-system.md)
- [ ] Task: Test both injection methods (--system-prompt flag vs .codex/instructions.md)
    - [ ] Document which method works and use consistently
- [ ] Task: Verify Codex CLI version and GPT-4o model endpoint

## Phase 2: Run All Cases (3 runs each) (OPERATOR)

- [ ] Task: case-01, run-1 — Codex CLI, GPT-4o, injected skill, Prompt S, temp=0, new session
    - [ ] Save raw-transcript.md with metadata
    - [ ] Normalize into normalized-output.md (8 sections)
- [ ] Task: case-01, run-2
- [ ] Task: case-01, run-3
- [ ] Task: case-02 through case-N, 3 runs each

## Phase 3: Quality Check

- [ ] Task: Verify injection method documented consistently
- [ ] Task: Verify all normalized-output.md have 8 sections
- [ ] Task: Document failure modes
