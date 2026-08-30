# No-LLM Implementation Programme

- **Status:** Completed — repository-owned acceptance passed; legacy evaluation and root portfolio remain separate
- **Type:** Chore / delivery programme
- **Scope:** Remaining work that does not require downloading model weights

## Track artefacts

- [Specification](./spec.md)
- [Implementation plan](./plan.md)
- [Metadata](./metadata.json)

## Operating rule

Use one active implementation branch and at most one disposable isolated
checkout. Merge each small PR only after its required checks pass, then delete
the merged branch and clean the disposable checkout before starting the next
slice.

**Policy precedence:** while this programme is active, this one-branch baseline
preempts the lane limits in [autonomy.json](../../autonomy.json); parallel
lanes resume only after programme closure. Tracks additionally honour
single-active-phase-checkpoint WIP discipline per
[autonomy.md](../../autonomy.md).

## Acceptance Criteria

1. Every planned PR is merged to `master` with passing required checks and its receipt recorded per the Phase 1 template.
2. CI evidence across the merged history shows zero model-weight downloads and no network egress beyond disclosed dependencies.
3. Only `master` and intentionally retained branches remain; disposable checkouts and stale lock backups are removed.
4. Track 00 checklist reconciliation is evidence-backed and genuine decision gates are retained rather than closed silently.
5. The legacy evaluation estate is reconciled: completed records are archived,
   and incomplete or blocked tracks remain preserved outside this programme
   with their repository-owned and external restart work explicit.
6. Issues are closed only where acceptance evidence passes; the residual-blocker and restart manifest is produced even when no blockers remain.
