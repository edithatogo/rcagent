# Coordinator handoff

- Issue: [#139](https://github.com/edithatogo/rcagent/issues/139)
- Draft PR: [#141](https://github.com/edithatogo/rcagent/pull/141)
- Branch: `feat/accimap-workflow-20261116`
- Implementation commit: `3f1d143c8ecaba0aad13365dd35afc3701992dd8`
- Implementation tree: `20cf409a8c424f61da4edba2c0c9b682524fb99d`
- Existing coordinator: conversation `6af6164f-cf84-8321-9f96-8b7d685aabe5`

## Delivered

A dedicated Conductor specification/contract/plan, expanded portable AcciMap
facilitation guide, two named hierarchy profiles, a typed synthetic companion
schema and validator, deterministic Mermaid generation, independently specified
fixture, 80 tests and review/parser/verification receipts. Source identities and
actual limitations are in [verification.md](./verification.md).

The changes use only the paths in [spec.md](./spec.md). The shared schema,
evidence core, workbench/D0 dispatch, CI, dependencies, baselines and legacy
template/admission hashes remain unchanged. D0 PR #132 head
`4746027c7de6cd4e0ed1518241f847146d79faef` and verifier PR #133 head
`4057512f23a2301d6ffe4649e42fb055eeb83937` were rechecked before publication and
retain their owners and draft status.

## Remaining integration work

1. Reconcile the current master, PR head and hosted checks. Local source checks
   passed, but the local full suite records 52 failures in existing Unix-socket
   tests because this executor denies AF_UNIX creation. Keep the required hosted
   Quality, mutation, profiling and conformance gates intact.
2. Apply the additive [registry proposal](./registry-proposal.md) to the shared
   Conductor registry/index and integration map. Assign a portfolio number if
   needed, without changing D0 or other workstream acceptance states.
3. Inspect actual Mermaid rendering on a permitted client, including uncertain
   links, all note text, hierarchy/readability and hostile-label handling.
   Ten parser cases passed; browser SVG/layout qualification remains open.
4. Review the scoped diff and retain this draft until integration acceptance.
   The existing coordinator owns merging through the protected process.

Later AM06 work remains explicit in the plan: reconcile shared method-selection
heuristics and dispatch, qualify extraction/model integration and other profiles,
evaluate facilitator agreement/usability, and build/verify any new portable
release. None is inferred from this synthetic structural increment.

Rollback is a scoped revert. There is no canonical migration, system-of-record
change, real-case processing, model evaluation or release to undo.
