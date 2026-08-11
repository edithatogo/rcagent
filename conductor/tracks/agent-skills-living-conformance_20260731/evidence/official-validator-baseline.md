# Official Validator Baseline Receipt

- Checked: `2026-07-31`
- Upstream: `agentskills/agentskills`
- Commit: `38a2ff82958afee88dadf4831509e6f7e9d8ef4e`
- Command: `uv run --directory skills-ref skills-ref validate <skill-root>`
- Result before migration: `Valid skill`
- Properties command: passed

The validator accepted the existing frontmatter. It did not detect that
`SKILL.md` depended on four files outside the skill root, did not assess the
legal-privilege wording, and emitted `RCA²` as `RCAÂ²` in JSON property output.
These are recorded fit gaps, not reasons to fork the validator.
