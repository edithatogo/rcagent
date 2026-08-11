# Phase 4 H0–H1 Raw Metadata Remediation

**Audit scope:** `evaluation/results/H0-control-no-skill/**/raw-transcript.md` and `evaluation/results/H1-claude-code-sonnet/**/raw-transcript.md`

**Protocol checked:** `evaluation/protocol/agent-test-protocol.md`, sections 5.1 and 6.1.

**Audit rule:** This report records observed evidence and gaps only. Missing values are not reconstructed from directory names, neighbouring files, model defaults, or transcript content.

## Protocol requirements

Each raw transcript should record:

- Condition ID
- Case ID
- Run number
- Exact model ID
- Harness name and version
- Temperature
- Timestamp start
- Timestamp end
- API endpoint or `N/A`
- Exact prompt sent
- Complete raw output

The current files generally use `Start Time` rather than the protocol's `Timestamp Start` label. That is a schema inconsistency even where a start value is present.

## Inventory

| Condition | Raw-transcript files found | Expected case/run shape represented by directories | Inventory issue |
|---|---:|---|---|
| H0 | 28 | 9 case/run paths are not represented uniformly | Includes an extra `case-01/run-1` path and several scaffold/error-only files; the normalised H0 set is not metadata-complete |
| H1 | 27 | 9 cases × 3 runs | Several runs are scaffold/error-only or lack the required metadata fields |

The audit does not treat a file's presence as proof that a valid run completed.

## Observed metadata gaps

### H0 — control/no skill

- All audited H0 files lack a recorded temperature.
- All audited H0 files lack a completed end timestamp.
- All audited H0 files lack an API endpoint value.
- `au-01/run-1`, `au-01/run-2`, `au-01/run-3`, `au-02/run-1`, `au-02/run-2`, `au-02/run-3`, `nz-01/run-1`, and `nz-01/run-3` use `Start Time` but do not provide the protocol-required end/API/temperature fields.
- `nz-01/run-2` is not a protocol-shaped metadata record: its required condition, case, run, model, harness, start time, temperature, end time, and API endpoint fields were not observed in the metadata header.
- `case-01/run-1` is a short scaffold-only file with no observed start timestamp, end timestamp, temperature, or API endpoint; its directory identity must not be used to infer a completed run.
- `au-02/run-1` and `nz-01/run-1` contain authentication-error text rather than a completed raw model transcript.
- The H0 inventory also contains short metadata-only/scaffold files at `au-01/run-2`, `au-02/run-2`, and `nz-02`–`nz-07` `run-2` paths. These are not treated as completed runs without an explicit raw output and metadata receipt.

### H1 — Claude Code/Sonnet

- Temperature, completed end timestamp, and API endpoint were not observed in the files audited as having a normal metadata header.
- `au-01/run-1` has a partial metadata header but lacks temperature, end timestamp, and API endpoint.
- `au-01/run-2`, `au-01/run-3`, `au-02/run-1`, `au-02/run-2`, `au-02/run-3`, and `nz-01/run-1`–`run-3` do not expose a complete protocol-shaped metadata header in the inspected content; required identity/timing fields must not be inferred.
- `nz-02`–`nz-07` `run-1` files expose partial metadata but lack temperature, completed end timestamp, and API endpoint.
- H1 files contain error markers in multiple runs, including authentication/API-related errors. Those files require run-level disposition before they can be admitted as raw evidence.

## Integrity and admission findings

1. A raw-transcript filename and directory path establish only the repository path, not that the protocol run completed.
2. A transcript containing an error, a metadata scaffold, or an agent-output marker without completed output is not sufficient evidence of a valid evaluation run.
3. No missing metadata field is filled in here. In particular, model defaults, harness assumptions, timestamps from filesystem metadata, and API endpoint assumptions are not accepted as protocol evidence.
4. H0 has an inventory/path anomaly (`case-01/run-1`) requiring disposition against the authoritative case manifest.
5. H0 and H1 cannot be admitted to blinded scoring solely on the basis of the current raw files. Metadata remediation and run-level evidence classification are prerequisites.

## Remediation actions

### Repository-local actions

- Preserve all current raw files unchanged as the audit source.
- Create a separate run manifest that records, per path: metadata fields observed, output status, error status, and admission decision.
- Use explicit statuses such as `complete`, `error`, `scaffold-only`, `metadata-incomplete`, or `unresolved`; do not silently repair source files.
- Reconcile the extra H0 `case-01/run-1` path against the authoritative case list before counting H0 coverage.
- Keep incomplete/error/scaffold-only runs out of the sealed blinding map and final score dataset.

### Operator or human actions required

- For every candidate completed run, supply the missing protocol metadata from the execution record: exact model ID, harness/version, temperature, start/end timestamps, and API endpoint.
- Confirm whether each transcript is a complete single-prompt/single-response run and provide the exact prompt receipt where it is absent.
- Classify authentication/API-error files as failed runs unless an immutable execution receipt and complete raw output are supplied.
- Re-run failed or unverified cases into a canonical evidence tree if the study design still requires full H0/H1 coverage.
- Obtain an explicit disposition for the H0 `case-01/run-1` path.

## Gate decision

**H0–H1 raw metadata remediation: not complete.** The current evidence is insufficient for a provenance-complete Phase 4 admission or for Track 5 blinded scoring. This report does not alter, overwrite, normalize, score, or classify any source transcript as valid.

