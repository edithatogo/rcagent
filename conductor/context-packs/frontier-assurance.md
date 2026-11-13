# Bounded context: frontier assurance

- Purpose: prioritise Track 13 FAW06 typing repairs under the user's latest direction; retain the Track 14 death-review plan for later implementation.
- Initial integration revision: 50c8a81; assessment reference: a895d42a8738d2937f849b65e3b892042f64b979.
- Authority: user request of 13 November 2026; existing autonomous workflow and agent-panel decisions.
- Start: AGENTS.md, CONSTRAINTS.md, conductor/index.md, selected spec/plan/metadata, and the exact capability/claim/triangulation document needed by that task.
- Budget: prefer 20,000 input tokens; fetch only relevant source/schema/tests and receipts. This is a planning budget, not permission to omit a material safety dependency.
- Exclude: private cases, model weights, generated coverage/profile reports, historical raw transcripts and unrelated repositories unless the selected task needs their exact evidence.
- Ownership: root integration owns shared indexes/contracts, the typing baseline/caps and CI; one implementation lane owns declared production-validator/conformance files, one owns declared prospective test files. Review remains read-only. Do not edit another lane's files without handing off ownership.
- Checks: locked environment; relevant tests first, then tools.full_validation and hosted required checks. Socket-denied environments must record unavailable integration evidence; never skip it silently in CI.
- Safety: generated synthetic fixtures; preserve source/view hashes; no cloud fallback or new publication. Agent agreement is labelled and does not supply clinical authority.
- Handoff: selected FAW/CAW ID, exact commit/worktree, dirty files, tests and failures, baseline/debt delta, unresolved source questions, next command and rollback path.
- Freshness: refresh GitHub head, policy/source versions and applicable tool APIs before acting on a new session; do not re-request standing approvals.

Canonical task records: [Track 13](../tracks/frontier-assurance_20261113/index.md), [Track 12](../tracks/cognitive-autopsy_20261107/index.md), [Track 14](../tracks/death-review_20261113/index.md).
