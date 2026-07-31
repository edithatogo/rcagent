# Agent Skills Standards Baseline

## Provenance

Captured `2026-07-31T17:51:19+10:00`.

| Source | Status | Revision evidence |
|---|---|---|
| `https://agentskills.io/specification` | authoritative specification | retrieved live |
| `https://agentskills.io/skill-creation/best-practices` | official guidance | retrieved live |
| `https://agentskills.io/skill-creation/optimizing-descriptions` | official guidance | retrieved live |
| `https://agentskills.io/skill-creation/evaluating-skills` | official guidance | retrieved live |
| `https://github.com/agentskills/agentskills` | upstream source | `38a2ff82958afee88dadf4831509e6f7e9d8ef4e` |
| `skills-ref/` in the upstream source | official reference validator | same commit |

## Normative Baseline

- A skill directory contains `SKILL.md` with YAML frontmatter and Markdown.
- `name` is required, 1-64 characters, lowercase ASCII alphanumeric plus
  hyphens, with no leading, trailing, or consecutive hyphen, and matches its
  parent directory.
- `description` is required, non-empty, at most 1,024 characters, and explains
  both capability and activation circumstances.
- Optional `license` is a short licence name or bundled-file reference.
- Optional `compatibility` is 1-500 characters and states genuine environment
  requirements.
- Optional `metadata` maps string keys to string values; unique keys are
  recommended.
- Optional `allowed-tools` is a space-separated string and remains
  experimental with client-dependent support.
- `scripts/`, `references/`, and `assets/` are standard optional directories.
- References use skill-root-relative paths and should avoid deep chains.

## Current Guidance Baseline

- Keep `SKILL.md` below 500 lines and approximately 5,000 tokens.
- Put activation information in the description.
- Use realistic positive and near-miss negative trigger queries, repeated
  trials, and held-out validation.
- Evaluate outputs with explicit assertions and preserve all execution
  evidence, not only failures.
- Prefer concise procedures, clear defaults, gotchas, templates, checklists,
  validation loops, and tested reusable scripts.

## Existing-Package Inventory

- Canonical skill: `skills/rca-investigation/`
- Files: 58
- Bytes: 134,103
- `SKILL.md`: 97 lines
- Standard resource directories present: `references/`, `assets/`
- Missing standard executable directory: `scripts/`
- External canonical dependencies: four files under repository-root `agents/`
- Current frontmatter: `name`, `description`
- Stable fields not yet declared: `license`, `compatibility`, `metadata`
- Experimental `allowed-tools`: absent

The current `SKILL.md` references repository-root agents, so it is not
self-contained. Its privacy section also implies that legal privilege may
apply without requiring jurisdiction-specific human review. Both are
conformance-quality defects to correct during migration.
