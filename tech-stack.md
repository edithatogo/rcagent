# Tech Stack

## Core Format: Markdown

All skill files, reference documents, templates, and agent definitions are written in Markdown.
- YAML frontmatter for skill metadata (name, description)
- CommonMark-compatible syntax
- GitHub Flavored Markdown tables

## Diagram Format: Mermaid

Diagram templates use `.mmd` extension (Mermaid diagram files).
Supported diagram types used in this suite:
- `mindmap` — Fishbone/Ishikawa, Yorkshire Factors
- `flowchart TD/LR` — 5 Whys chain, Bow-Tie, AcciMap, STAMP, Investigation Workflow
- `timeline` — Chronology/Event sequence
- `block-beta` — Swiss Cheese, SEIPS, HFACS layers
- `quadrantChart` — FMEA Priority matrix

## Document Generation: document-skills

DOCX and PPTX templates are Markdown instruction files that describe document structure
for generation using the `document-skills:docx` and `document-skills:pptx` Claude Code skills.
They are not binary Office files — they are generation instructions.

## Skill Metadata: YAML Frontmatter

Each SKILL.md and agent file uses YAML frontmatter:
```yaml
---
name: skill-name
description: >
  Comprehensive description used for skill triggering.
  Includes when to use and key triggers.
---
```

## Directory Structure

```
rca/
├── CLAUDE.md               # Project conventions
├── product.md              # Conductor: product context
├── tech-stack.md           # Conductor: tech stack context
├── workflow.md             # Conductor: development workflow
├── skills/
│   └── rca-investigation/
│       ├── SKILL.md                    # Core skill entry point
│       ├── references/
│       │   ├── methods/                # 14 method reference files
│       │   ├── method-selection-matrix.md
│       │   ├── method-combination-guide.md
│       │   ├── just-culture-guide.md
│       │   ├── safety-ii-principles.md
│       │   └── investigation-quality-checklist.md
│       └── assets/
│           ├── templates/
│           │   ├── markdown/           # 14 working document templates
│           │   ├── mermaid/            # 12 .mmd diagram templates
│           │   ├── docx/               # 7 DOCX generation instructions
│           │   └── pptx/              # 3 PPTX generation instructions
│           └── styles/
│               ├── docx-style-guide.md
│               └── pptx-style-guide.md
├── agents/
│   ├── rca-triage.md
│   ├── rca-investigate.md
│   ├── rca-report.md
│   └── rca-track.md
└── docs/
    └── plans/
        ├── 2026-02-25-rca-skill-design.md
        └── 2026-02-25-rca-skill-implementation.md
```

## No Build Step

This is a pure content/configuration repository. No build tools, package managers, or compilation required.
