# Track 02 Fit-Gap: Citation and Source Verification — 2026-08-29

Phase 0 existing-system fit for citation integrity and source verification
within the evidence workflow.

## Candidate evaluated

**SourceRight** (vendored at `.agents/plugins/sourceright`, pin `c5fa583`,
crate version 0.1.20, licence MIT OR Apache-2.0).

Source-verified capabilities (from `README.md`, `Cargo.toml`, `src/`):

- `validate-csl`, `report`, `export`, `init` — reference verification and
  degraded-coverage diagnostics with repair-action errors
- `citation-sync` — fail-safe by default (preview mode; explicit `--apply`
  required before writing audit logs or remote snapshots)
- `bench` — deterministic checked-in fixture suite **without live providers**
- `mcp` — MCP server surface for agent integration
- `src/citeweft_adapter.rs` — dedicated citation-weft adapter module
- Audit logs, malformed-sidecar failures include path + repair action

## Selection

**Thin SourceRight adapter** is the selected smallest adequate intervention
for citation verification. No project-owned reference verifier will be built.
No ADR required: this is an adapter against a maintained system, not a new
subsystem or fork (per `integration-strategy.md`).

## Constraints recorded

- Rust workspace (202 upstream commits, solo maintainer, active hardening
  programme in its own conductor records, tracks 36–40 examiner-grade audit)
- Offline-safe by design: `bench` fixture suite runs without live providers;
  `citation-sync` requires explicit `--apply` for any write
- No telemetry found in vendored source
- Upstream findings already filed: sourceright#100 (backup artefacts)
- Registry: `vendored_plugins` in `conductor/integration-map.json`

## Execution boundary (honest limitation)

A live CLI trial (`cargo build --locked` + `bench --json`) was attempted and
**deferred**: the local execution shell caps commands at 30 seconds, which
killed the toolchain build mid-fetch three times (build, offline-cache miss,
timed-out index fetch). The live fixture run is carried forward as an entry
condition of Phase 6 (adapter API implementation), where it belongs with the
contract fixtures. Static/source-level evaluation above is complete.

## Decisions

1. Citation verification ownership: SourceRight (maintained) — project owns
   only the adapter and evidence-schema mapping.
2. Live `bench` fixture trial: Phase 6 entry condition (this receipt is the
   handoff context).
3. Generic gaps → upstream: sourceright#100 already filed; no additional gap
   identified at source level.
