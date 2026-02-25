# Markdown Style Guide

## File Structure

Every content file must open with a H1 title matching the filename intent, followed by a brief purpose statement if needed.

```markdown
# [Title]

[One-sentence purpose statement (optional for templates)]
```

## Headings

- H1 (`#`): Document title — one per file
- H2 (`##`): Major sections
- H3 (`###`): Subsections
- H4 (`####`): Use sparingly

Never skip heading levels (e.g., H2 → H4).

## Lists

Unordered lists: use `-` (not `*` or `+`)
Ordered lists: use `1.` for all items (renderer handles numbering)

```markdown
- First item
- Second item
  - Nested item (2-space indent)
```

## Tables

Use GFM pipe tables. Always include a header separator row.

```markdown
| Column A | Column B | Column C |
|---|---|---|
| Value | Value | Value |
```

Align columns consistently. For scoring tables, right-align numeric columns:

```markdown
| Dimension | Score |
|---|---:|
| D1 Contributing Factors | 4 |
```

## Code Blocks

Fenced with triple backticks. Always specify language:

```markdown
\`\`\`mermaid
flowchart TD
    A --> B
\`\`\`

\`\`\`yaml
---
name: skill-name
---
\`\`\`

\`\`\`bash
git commit -m "feat: add method"
\`\`\`
```

## Emphasis

- **Bold** (`**text**`): Key terms, important warnings, section labels
- *Italic* (`*text*`): Titles of publications, technical terms on first use
- `Code` (backtick): File paths, field names, CLI commands, placeholders like `[Patient A]`

## Placeholders

All de-identification placeholders use square brackets:
- `[Patient A]`, `[Patient B]`
- `[Case ID]`
- `[Ward X]`, `[Unit Y]`
- `[Clinician A]`, `[RN B]`
- `[Date]`, `[Time]`, `[DD/MM/YYYY HH:MM]`

## YAML Frontmatter

Required for SKILL.md and agent files. Optional for templates.

```yaml
---
name: short-kebab-case-name
description: >
  Multi-line description.
  Used for skill triggering.
---
```

## Line Length

No hard limit, but prefer wrapping prose at ~120 characters for readability in editors.
Tables and code blocks: do not wrap.

## Checkboxes (plan.md only)

```markdown
- [ ] Pending task
- [~] In-progress task
- [x] Completed task
```

Only use in `plan.md` files. Do not use in content/reference files.

## File Naming

- All lowercase
- Hyphens for word separation (not underscores, not spaces)
- Descriptive: `method-selection-matrix.md` not `matrix.md`
- Case files: `au-case-01.md`, `nz-case-01.md`
- Result files: follow prescribed naming (`raw-transcript.md`, `normalized-output.md`, `scores.md`)
