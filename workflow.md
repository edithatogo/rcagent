# Development Workflow

## Philosophy

This repo follows a content-first approach. All files are Markdown or Mermaid — there is no code to compile or test in the traditional sense. Quality is assessed by:
1. Completeness (all required files exist)
2. Accuracy (method content is clinically correct and evidence-based)
3. Usability (templates are actionable, not vague)
4. Integration (cross-references between files are accurate)

## Adding a New Investigation Method

1. Create reference file: `skills/rca-investigation/references/methods/<method-name>.md`
2. Add entry to `skills/rca-investigation/SKILL.md` Methods Reference Index table
3. Add entry to `skills/rca-investigation/references/method-selection-matrix.md`
4. Add entry to `skills/rca-investigation/references/method-combination-guide.md` if it combines with other methods
5. Create Mermaid diagram template in `skills/rca-investigation/assets/templates/mermaid/` if visual representation useful
6. Commit with: `git commit -m "feat: add [method-name] investigation method"`

## Adding a New Template

1. Create template file in appropriate subdirectory:
   - Working documents: `assets/templates/markdown/`
   - Diagrams: `assets/templates/mermaid/`
   - Word documents: `assets/templates/docx/`
   - Presentations: `assets/templates/pptx/`
2. Add entry to SKILL.md Template Index
3. Update relevant agent files to reference new template
4. Commit with: `git commit -m "feat: add [template-name] template"`

## Updating an Agent

1. Edit the relevant file in `agents/`
2. Verify all template references match actual template files
3. Verify all reference file paths match actual reference files
4. Commit with: `git commit -m "feat: update [agent-name] agent"`

## Commit Convention

```
feat: add [description]       — new content
fix: correct [description]    — fixing errors in existing content
update: revise [description]  — updating existing content
docs: [description]           — documentation changes
```

## Privacy in Templates

All templates must de-identify patient data:
- Use `[Patient A]`, `[Patient B]` — never real names
- Use `[Case ID]` — never real MRN or URN
- Use `[Ward X]`, `[Unit Y]` — de-identified locations
- Use `[Date/Time]` placeholders — never real patient dates unless anonymized

## Evaluation Study Workflow

### Adding a New Case
1. Verify case meets all inclusion criteria in `evaluation/protocol/case-selection-criteria.md`
2. Format case using the standardized template
3. Assign SAC-equivalent and difficulty rating with documented rationale
4. Save to `evaluation/datasets/{source}/xx-case-XX.md`
5. Update `evaluation/datasets/README.md` case index
6. Verify coverage requirements still met

### Running an Experimental Condition
1. Follow exact setup in `evaluation/protocol/agent-test-protocol.md` (Section 4 for injection)
2. Record all metadata per run (model version, timestamp, tokens)
3. Save raw transcript to `evaluation/results/{condition}/case-XX/run-N/raw-transcript.md`
4. Normalize output into 8 sections → `normalized-output.md`
5. Repeat for 3 independent runs per case per condition

### Scoring
1. Complete ALL runs before scoring begins
2. Generate blinding map (Section 8 of agent-test-protocol)
3. Score normalized outputs blind using rubric in `evaluation/protocol/evaluation-rubric.md`
4. Record scores to `evaluation/results/{condition}/case-XX/run-N/scores.md` (H8: omit run-N/, single run)
5. After all scoring: unblind, populate `evaluation/analysis/rubric-scores.csv`

## Regulatory Currency

Review and update annually (or when ACSQHC/NSQHS standards change):
- SAC classification criteria
- Mandatory notification requirements
- Open disclosure framework references
- Method references (update when new evidence published)
