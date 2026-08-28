# Track 02 phase completion receipt

- Track: `evidence-workflow-core_20260731`
- Functional commit: `4a976e02e61733f47446b6b50ad3d575275a53ed`
- Review-fix commit: `14316744c1d0b42eb3765f12013689f90d2ef97a`
- Data boundary: synthetic fixtures only; no patient, staff, credential, or
  organisation record data

## Phase reconciliation

| Phase | Evidence-backed result |
|---|---|
| 0 — fit and gap | ims+ or an approved incident platform remains authoritative; SourceRight 0.1.20 is the optional citation-verification dependency; project code is limited to schemas, workflow rules, and thin ports |
| 1 — canonical model | schema 1.1 represents roles, sources, artefacts, evidence, typed statements, factors, reviews, actions, outcomes, referrals, authority, privacy, jurisdiction, and system-of-record reconciliation |
| 2 — provenance | deterministic SHA-256 fingerprints, transformation/model disclosure, author/reviewer state, support/contradiction/supersession, lawful redacted views, and hash-linked receipts are implemented |
| 3 — workflow | explicit states, event vocabulary, governed referrals, preconditions, deadlines, exception paths, correction, withdrawal, reopen, and appeal semantics are validated |
| 4 — persistence/interchange | vendor-neutral ports, canonical JSON, additive migration, compartments, bounded exports, FHIR R5 exchange boundaries, W3C PROV alignment, and CMMN/BPMN/DMN profiles are documented |
| 5 — fixtures | complete, conflicting, late, literature, invalid provenance, invalid transition, duplicate, supersession, redaction, audit-tampering, migration, and round-trip behaviors use synthetic values |
| 6 — adapters | primitive-only ports cover storage, retrieval, capabilities, workflow, and export; the SourceRight subprocess adapter enforces local privacy profiles, read-only commands, timeouts, diagnostics, and fail-closed JSON |
| 7 — completeness | exports retain statement kinds, invalid references fail, audit tampering is detected, unsupported migrations fail, and framework types do not enter the core port contracts |

## SourceRight live fixture gate

The previously deferred local gate was rerun from the pinned vendored plugin:

```text
cargo build --locked --bin bench
Finished dev profile; sourceright 0.1.20
./target/debug/bench --json
task_count=13, passed_count=13, failed_count=0
```

The benchmark uses checked-in fixtures without live providers. It does not
prove production, publisher, legal, or network-provider suitability.

## Validation and hashes

Before review fixes, repository-wide Ruff, ty, basedpyright, gremlin scan, and
governance validation passed; pytest reported 105 passed and 5 documented
PowerShell-dependent skips with 83.47% coverage. After review fixes, 15 focused
evidence tests and all focused lint/type checks passed. The final gate ran from
a clean detached worktree at `acca833`: all quality and governance checks
passed, with 106 tests passed, 5 documented PowerShell-dependent skips, and
83.58% coverage against the 80% requirement.

- schema: `ccf454138863d98af6337703a874f8e8a90f819e1fbdeb1f4f97c684d36f53d5`
- contracts: `2a0927b822639a45859eeaa121ad30e890d53864c87047ce4e10648226b25bd4`
- valid fixture: `3a39c9137e69a9d563f6289aeacec5e5980a879498e40433eaa1c2343c3e3fce`
- invalid catalogue: `0d01b22da1cec99f465cfa3821b29564260dc94f6a59714396efd4723bd30a3b`

## Fresh-context review

Review found and fixed two gaps: arbitrary SourceRight commands could bypass
the claimed read-only profile, and malformed relationship entries could raise
after schema diagnostics. The adapter now uses an executable/read-only
allowlist and rejects `--apply`; semantic validation skips malformed values
after recording schema errors. Redaction also records `custody_state=redacted`.

After PR #41 merged, Codecov reported 85.20% patch coverage against its 90%
target even though all required workflows and the repository-wide coverage
gate passed. A focused follow-up added tests for every previously uncovered
statement in the new evidence modules; the focused evidence-module suite now
reports 20 passed and 99.06% coverage. Track closure waits for the follow-up
hosted patch check rather than downgrading that negative result.

## Limitations and external gates

- No production persistence adapter, encryption product, enterprise connector,
  jurisdiction rule pack, or UI is selected or claimed.
- No retention period, privilege, legal status, clinical conclusion, or
  organisational authority is inferred.
- FHIR, PROV, CMMN, BPMN, and DMN are bounded mappings/profiles, not certified
  conformance claims.
- Release, deployment, real-data use, credentials, paid services, and external
  submissions remain separately gated.
