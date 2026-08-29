# Quality frontier and architecture reconciliation

Date: 2026-08-29
Base revision: `69ca2d09278758fbed885104cf852b0fc74599cd`
Data boundary: repository metadata, public GitHub state, and synthetic tests only

## Issues #17 and #18

Repository-owned context gaps are addressed by the root `AGENTS.md`,
`CONTRIBUTING.md`, `SECURITY.md`, pull-request template, sanitised bug form,
private-vulnerability-report link, and `python -m tools.full_validation`. The
validator now fails when any canonical context surface is absent. The local
gate mirrors the hosted Quality workflow's lint, type, gremlin, governance,
deterministic benchmark, and test stages without model downloads or external
execution.

Dependency Review and Codecov have produced hosted results on current pull
requests. Renovate configuration now inherits `github>edithatogo/renovate-config`
while retaining the repository's justified update grouping and admission
rules. A local catch-all disables inherited automerge until the bounded master
ruleset is observed. No hosted Renovate Dependency Dashboard or pull request was observed,
so app installation/health remains an external prerequisite. Dependabot is
absent and is not reintroduced alongside an unverified Renovate installation.

No repository ruleset or legacy branch protection was observed through the
GitHub API. The stable required-check candidates are Dependency Review and the
Quality workflow's Ubuntu, macOS, and Windows validation jobs. Agent Skill
Conformance is path-conditional; Vale is advisory; Codecov patch arrival is
external-app dependent. A ruleset must preserve administrator recovery and
zero mandatory human approvals. Creating that hosted ruleset is a separate
settings mutation and is not claimed by this repository change. The ruleset
must be created and verified before Renovate is granted repository access.

## Issue #19

`architecture-issue-19-acceptance-map.json` maps all four issue criteria to
exact artefacts. `conductor/clinical-governance-architecture.json` validates
every layer and integration owner against `conductor/roadmap.json`. Track 02
plan lines covering the canonical lifecycle and its completion receipt, Track
04's policy-transition mapping and completion receipt, Track 07's federated
retrieval contract and completion receipt, and Track 09's end-to-end surface
and completion receipt directly evidence the first vertical slice. Their
metadata maps issues #7, #9, #12, and #14 and records completed or archived
repository state; those issues were observed closed. The architecture's five
extraction criteria and five shared contracts govern any specialist split.

This is repository architecture conformance, not clinical, policy, legal,
regulatory, employment, cultural-safety, organisational, or deployment
validation. No new specialist scope or accountable-authority decision is made.

## Validation and rollback

Focused tests cover canonical context presence, the one-command gate contract,
architecture owners, the first vertical slice, and split criteria. The complete
gate is `uv run python -m tools.full_validation`. Revert this focused change to
remove the new context surfaces and command; external settings are unchanged.
