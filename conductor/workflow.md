# Development Workflow

## Philosophy

This is a **content-first repository** — all files are Markdown or Mermaid with no code to compile or test. Quality is assessed by:
1. **Completeness** — all required files exist and are cross-referenced correctly
2. **Accuracy** — method content is clinically correct and evidence-based
3. **Usability** — templates are actionable, not vague
4. **Integration** — cross-references between files are accurate

Traditional TDD and code coverage metrics do not apply. Quality gates are content-specific (see below).

---

## Task Workflow

All tasks follow this lifecycle, tracked in `plan.md`:

### 1. Select Task
Choose the next `[ ]` task from `plan.md` in sequential order within the current phase.

### 2. Mark In Progress
Edit `plan.md` and change `[ ]` to `[~]` before beginning work.

### 3. Do the Work
Create or edit content files as specified by the task. Follow:
- `conductor/product-guidelines.md` for writing style and de-identification rules
- `conductor/tech-stack.md` for file format and directory conventions
- `CLAUDE.md` for project-wide conventions

### 4. Quality Check
Before marking complete, verify against the content quality gates:
- [ ] Content is factually accurate (method descriptions cite sources)
- [ ] All placeholder identifiers used (no real patient/staff data)
- [ ] Cross-references to other files are accurate (paths exist)
- [ ] AU/NZ regulatory terminology correct
- [ ] Formatting follows product-guidelines.md

### 5. Commit
```
feat: add [description]       — new content added
fix: correct [description]    — correcting errors in existing content
update: revise [description]  — updating existing content
docs: [description]           — documentation changes
```

### 6. Update Plan
Change `[~]` to `[x]` in `plan.md` and commit:
```
conductor(plan): Mark task '[task name]' as complete
```

---

## Phase Completion

When all tasks in a phase are `[x]`:
1. Announce the phase is complete
2. Summarise what was produced
3. Check all deliverables match the phase's acceptance criteria in `spec.md`
4. Ask the user: "Phase [N] complete. All deliverables checked. Shall I proceed to Phase [N+1]?"
5. Await explicit confirmation before starting the next phase

---

## Track Dependency Order

The evaluation tracks must be executed in this order (each depends on the previous):

```
eval-case-collection_20260225
    ↓
eval-pilot-calibration_20260225
    ↓
eval-data-collection_20260225
    ↓
eval-scoring_20260225
    ↓
eval-analysis_20260225
```

Do not start a track until its dependency is complete.

---

## Evaluation-Specific Workflows

### Adding a New Case
1. Verify case meets all inclusion criteria in `evaluation/protocol/case-selection-criteria.md`
2. Format using standardized template (Section 7 of case-selection-criteria.md)
3. Assign SAC-equivalent and difficulty rating (1–3) with documented rationale
4. Save to `evaluation/datasets/{source}/xx-case-XX.md`
5. Update `evaluation/datasets/README.md` case index
6. Verify coverage requirements (event types, jurisdictions, difficulty distribution)

### Running an Experimental Condition
1. Follow exact setup in `evaluation/protocol/agent-test-protocol.md` (Section 4 for skill injection per harness)
2. Use Prompt S for conditions H1–H7 (skill-aware), Prompt N for H0 (naive control)
3. Record all metadata per run (model version, harness version, timestamp, tokens, cost)
4. Save raw transcript to `evaluation/results/{condition}/case-XX/run-N/raw-transcript.md`
5. Normalize output into 8 sections → `normalized-output.md` in same directory
6. Repeat for 3 independent runs per case per condition (H8: 1 run only, no run-N/ nesting)

### Scoring (Blinded)
1. Complete ALL runs across ALL conditions before scoring begins
2. Generate blinding map: assign random eval IDs, strip metadata, shuffle order
3. Score normalized outputs blind using `evaluation/protocol/evaluation-rubric.md`
4. Record per-dimension scores (D1–D8) and composite to `scores.md`
5. After all scoring complete: unblind, populate `evaluation/analysis/rubric-scores.csv`

---

## Commit Convention

```
feat: add [description]       — new content
fix: correct [description]    — fixing errors
update: revise [description]  — updating existing content
docs: [description]           — documentation changes
conductor(plan): [description] — plan.md updates
conductor(checkpoint): [description] — phase checkpoint commits
```
