# Context and Harness Receipt — 2026-08-29

The root `AGENTS.md` is a short client-neutral navigation and safety contract. Existing context-pack and decision templates define authority, freshness, privacy mode, bounded context, exclusions, owned files, commands, handoff, uncertainty, next action, and rollback.

`tools.workbench` implements machine-readable doctor, context, queue, validation, evaluation, receipt, and reconciliation entry points. Evaluation fails closed without executing a model. Reconciliation states that hosted and external state were not checked. The underlying autonomy module provides bounded recovery, circuit breaking, lease classification, and conflict-safe dispatch.

Focused validation: 17 tests passed; Ruff, ty, and basedpyright passed. No network, credential, private data, model, Git mutation, or external action is performed by the harness.
