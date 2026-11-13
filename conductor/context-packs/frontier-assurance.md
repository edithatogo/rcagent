# Bounded context: frontier assurance

- Purpose: prioritise Track 13 FAW06 typing repairs under the user's latest direction; retain the Track 14 death-review plan for later implementation.
- Initial integration revision: 50c8a81; assessment reference: a895d42a8738d2937f849b65e3b892042f64b979.
- Current typing base: PR #129 merged at 388a4c6 after exact-head hosted acceptance. PR #130 records the next 4,431-to-3,198 reduction through inventory/execution/admission producer contracts and twelve regressions. Read the [current receipt](../tracks/frontier-assurance_20261113/typing-producers-evidence.md) and final-head hosted results before claiming acceptance.
- Authority: user request of 13 November 2026; existing autonomous workflow and agent-panel decisions.
- Start: AGENTS.md, CONSTRAINTS.md, conductor/index.md, selected spec/plan/metadata, and the exact capability/claim/triangulation document needed by that task.
- Budget: prefer 20,000 input tokens; fetch only relevant source/schema/tests and receipts. This is a planning budget, not permission to omit a material safety dependency.
- Exclude: private cases, model weights, generated coverage/profile reports, historical raw transcripts and unrelated repositories unless the selected task needs their exact evidence.
- Ownership: root integration owns shared indexes/contracts, the typing baseline/caps and CI; at most two implementation lanes own declared non-overlapping source/test batches. The completed lanes handled inventory/freeze and execution producers; the first then handled admission fixtures. Next lanes: distinct CLI admission plus output-probe contracts, and capability-probe admission/capture contracts, each with its tests. Review remains read-only. Do not edit another lane's files without handing off ownership.
- Frozen source: preserve darwin_runtime_profile.py, local_model_comparator.py, darwin_server_v030.py and darwin_runtime_v030.py, historical protocols/reviews and negative outcomes. Current engineering closure updates do not requalify consumed studies.
- Worktree runtime: use the selected worktree's interpreter with `python -m pytest` and verify imported module origins; a reused editable environment's pytest console script can import a different checkout.
- Checks: locked environment; relevant tests first, then tools.full_validation and hosted required checks. Socket-denied environments must record unavailable integration evidence; never skip it silently in CI.
- Safety: generated synthetic fixtures; preserve source/view hashes; no cloud fallback or new publication. Agent agreement is labelled and does not supply clinical authority.
- Handoff: selected FAW/CAW ID, exact commit/worktree, dirty files, tests and failures, baseline/debt delta, unresolved source questions, next command and rollback path.
- Freshness: refresh GitHub head, policy/source versions and applicable tool APIs before acting on a new session; do not re-request standing approvals.

Canonical task records: [Track 13](../tracks/frontier-assurance_20261113/index.md), [Track 12](../tracks/cognitive-autopsy_20261107/index.md), [Track 14](../tracks/death-review_20261113/index.md).
