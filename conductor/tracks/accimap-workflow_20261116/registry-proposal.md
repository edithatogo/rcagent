# Shared integration proposal

The existing coordinator owns the shared Conductor index, registry, roadmap,
integration map and merges. This increment supplies a dedicated track and a
reviewable additive proposal without editing those shared files.

## Proposed registry entry

Add under current implementation/research in `conductor/tracks.md` after
coordinator reconciliation; assign a portfolio number only if needed:

| Status | Track | GitHub | Scope |
|---|---|---:|---|
| [~] | [AcciMap workflow](./tracks/accimap-workflow_20261116/index.md) | [#139](https://github.com/edithatogo/rcagent/issues/139) | Named profiles, evidence-bound synthetic companion graph and guided analysis; integration and operational qualification separate |

Add a discoverability link in `conductor/index.md` to this track, without
changing FAW07/D0 or Track 12–14 states. Record the fit-gap in the shared
integration map using [the local decision](./context.md). If a numbered roadmap
entry is required, use the coordinator's current inventory and do not copy a
stale roadmap wholesale.

## Shared changes requiring their existing owner

1. Reconcile method-selection heuristics in the matrix/agent dispatch. The method
   guide clarifies that severity alone is not a methodological requirement for
   AcciMap. Existing defaults should be reviewed alongside applicable local policy.
2. Keep the legacy template source and its admission hashes unchanged in this
   increment. A later template/header change must update the admission manifest
   and run the existing package gates on its actual bytes.
3. Decide whether and when to expose the standalone adapter through
   `tools/workbench.py`, currently part of the D0 implementation boundary.
4. Requalify any future integration with extracted evidence and model-generated
   hypotheses. Synthetic graph validation cannot transfer D0 or scientific passes.

## Integration order

Review the scoped source, fixtures and method independently; inspect the actual
tested tree and hosted checks. Reconcile the additive registry proposal and any
new master changes in the coordinator's integration candidate. Preserve D0
ownership and all failures. Merge only through the existing protected process.
Build and verify a new release separately if distribution is later authorised.
