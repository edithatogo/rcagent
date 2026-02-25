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
├── conductor/              # Conductor CDD framework context
│   ├── product.md
│   ├── product-guidelines.md
│   ├── tech-stack.md
│   ├── workflow.md
│   ├── tracks.md
│   ├── code_styleguides/
│   ├── tracks/             # Active tracks (6 evaluation tracks)
│   └── archive/            # Completed tracks
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
├── evaluation/
│   ├── protocol/
│   │   ├── scientific-protocol.md
│   │   ├── literature-review.md
│   │   ├── evaluation-rubric.md
│   │   ├── case-selection-criteria.md
│   │   └── agent-test-protocol.md
│   ├── datasets/
│   │   ├── README.md
│   │   ├── acsqhc/
│   │   ├── hdc-nz/
│   │   ├── coroner-au/
│   │   └── coroner-nz/
│   ├── results/            # H0-H8 condition directories
│   └── analysis/
└── docs/
```

## Evaluation Data Format: CSV

The evaluation uses CSV for structured scoring data (`rubric-scores.csv`), with columns for condition, case, run, 8 dimension scores, composite, and metrics (time, tokens, cost, words).

## No Build Step

This is a pure content/configuration repository. No build tools, package managers, or compilation required. No tests, no linting, no CI pipeline. Quality is assessed through human and AI review of content accuracy and completeness.
