# Bounded context: frontier assurance

- Purpose: prioritise Track 13 FAW06 typing repairs under the user's latest direction; retain the Track 14 death-review plan for later implementation.
- Initial integration revision: 50c8a81; assessment reference: a895d42a8738d2937f849b65e3b892042f64b979.
- Current typing base: PR #130 merged at e6d95394241661db117dc429976aaa6204a1128b after exact-head Quality43529164806, dependency/privacy/conformance success. FAW06 has removed all 3,198 remaining diagnostics across 153 active files; the baseline and caps are empty, and explicit Any is an error. Local verification preserves the base's 52 socket-denied failures and adds 177 passing cases. Require exact final-head hosted acceptance before closure.
- Authority: user request of 13 November 2026; existing autonomous workflow and agent-panel decisions.
- Start: AGENTS.md, CONSTRAINTS.md, conductor/index.md, selected spec/plan/metadata, and the exact capability/claim/triangulation document needed by that task.
- Budget: prefer 20,000 input tokens; fetch only relevant source/schema/tests and receipts. This is a planning budget, not permission to omit a material safety dependency.
- Exclude: private cases, model weights, generated coverage/profile reports, historical raw transcripts and unrelated repositories unless the selected task needs their exact evidence.
- Ownership: root integration owns shared indexes/contracts, baseline/caps, source fixity and CI; at most two implementation lanes own declared non-overlapping batches. Read-only review continues across lane and root changes. Do not edit another lane's files without handing off ownership.
- Historical/current source: preserve consumed source S e6c1453d68b562829b99f40b925de6d287496601 and historical protocols/reviews/negative results. Active typed implementations use the new typing-20261114 engineering identities, reviewed current source inventories and the narrow hash-bound Bandit revalidation. Historical consistency is tested against S, never rewritten to current hashes. Current engineering closure updates do not requalify consumed studies.
- Worktree runtime: use the selected worktree's interpreter with `python -m pytest` and verify imported module origins; a reused editable environment's pytest console script can import a different checkout.
- Checks: locked environment; relevant tests first, then tools.full_validation and hosted required checks. Socket-denied environments must record unavailable integration evidence; never skip it silently in CI.
- Safety: generated synthetic fixtures; preserve source/view hashes; no cloud fallback or new publication. Agent agreement is labelled and does not supply clinical authority.
- Handoff: selected FAW/CAW ID, exact commit/worktree, dirty files, tests and failures, baseline/debt delta, unresolved source questions, next command and rollback path.
- Freshness: refresh GitHub head, policy/source versions and applicable tool APIs before acting on a new session; do not re-request standing approvals.

Canonical task records: [Track 13](../tracks/frontier-assurance_20261113/index.md), [Track 12](../tracks/cognitive-autopsy_20261107/index.md), [Track 14](../tracks/death-review_20261113/index.md).
