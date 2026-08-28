# Governance Ledger Receipt — 2026-08-29

Architecture and decision templates are complemented by dedicated risk, source, assumption, and evidence templates under `conductor/records/`. Each records stable identity, owner, scope, UTC time, freshness or wake condition, evidence, uncertainty, limitations, and safe continuation or rollback information.

The decision template contains every required option, recommendation, evidence, trade-off, reversibility, safe-default, paused-scope, continuing-work, dependency, schedule, and response field. `tools.autonomy_harness` validates those fields, deduplicates open decisions by stable ID, selects one deterministic engagement, and classifies authoritative context as current or stale from timezone-aware timestamps.

Focused validation: 19 tests passed; Ruff and ty passed. The contracts do not accept residual risk, choose a licence, contact an owner, or promote stale evidence automatically.
