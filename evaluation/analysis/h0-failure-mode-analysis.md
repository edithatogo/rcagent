# H0 Failure-Mode Analysis

Date: 2026-08-08
Scope: H0 raw and normalized evidence audit
Status: evidence classification only; no source files altered

| Failure mode | Observed scope | Disposition |
|---|---:|---|
| Metadata incomplete | 28 raw files | Quarantine; recover immutable execution metadata or rerun |
| H0 extra path `case-01/run-1` | 1 path | Quarantine pending case-manifest disposition |
| Normalized output has no detectable eight-section structure | 7 files | Quarantine; regenerate only from valid raw transcript |
| Authentication/API or scaffold/error material | See run manifest | Failed/unresolved; do not score |
| Complete eight-section normalized structure | 21 files | Still not admitted until raw, metadata, hashes, and receipts pass |

No timestamp, model, harness, temperature, endpoint, token, cost, case, or run
identity was inferred. No error or scaffold file was converted into a valid
evaluation run.

## Closure criteria

H0 can close only after every canonical slot has a complete atomic package,
the extra path has an explicit disposition, the manifest audit passes, and the
Track 5 preflight succeeds.
