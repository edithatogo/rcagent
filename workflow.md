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

## Regulatory Currency

Review and update annually (or when ACSQHC/NSQHS standards change):
- SAC classification criteria
- Mandatory notification requirements
- Open disclosure framework references
- Method references (update when new evidence published)
