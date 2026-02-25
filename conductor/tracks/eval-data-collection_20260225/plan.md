# Evaluation Data Collection — Plan

## Phase 1: Setup

- [ ] Task: Prepare skill injection files for Conditions B harnesses
    - [ ] Concatenate SKILL.md + key references into /tmp/rcagent-system.md
    - [ ] Verify total token count fits within each harness's context window
- [ ] Task: Verify harness versions and document
    - [ ] Claude Code version
    - [ ] Gemini CLI version
    - [ ] Codex CLI version
    - [ ] Qwen CLI version
    - [ ] Kilo Code version
    - [ ] Copilot version

## Phase 2: AI Condition Runs (H0-H7)

- [ ] Task: Run H0 (Raw API, no skill) — all cases, 3 runs each
- [ ] Task: Run H1 (Claude Code + Sonnet) — all cases, 3 runs each
- [ ] Task: Run H2 (Claude Code + Opus) — all cases, 3 runs each
- [ ] Task: Run H3 (Gemini CLI) — all cases, 3 runs each
- [ ] Task: Run H4 (Codex CLI) — all cases, 3 runs each
- [ ] Task: Run H5 (Qwen CLI) — all cases, 3 runs each
- [ ] Task: Run H6 (Kilo Code) — all cases, 3 runs each
- [ ] Task: Run H7 (Copilot) — all cases, 3 runs each

## Phase 3: Human Condition (H8)

- [ ] Task: Provide human expert with case narratives and instructions
- [ ] Task: Collect and save H8 outputs (1 per case)

## Phase 4: Normalization

- [ ] Task: Normalize all outputs into 8 standardized sections
    - [ ] For each raw transcript, extract sections 1-8
    - [ ] Mark ABSENT for any missing sections
    - [ ] Document failure modes encountered
- [ ] Task: Document all failure modes in analysis/failure-mode-analysis.md

## Phase 5: Blinding

- [ ] Task: Generate random evaluation IDs for all outputs
- [ ] Task: Create blinding-map.csv (condition → eval ID mapping)
- [ ] Task: Create scored copies with metadata stripped
- [ ] Task: Shuffle presentation order per case
