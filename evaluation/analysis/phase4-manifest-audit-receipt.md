# Phase 4 Manifest Audit Receipt

**Audit date:** 2026-08-01  
**Auditor role:** P4-M manifest auditor  
**Scope:** Canonical Phase 4 conditions H0–H8 in `evaluation/results/`  
**Method:** Read-only recursive inventory of raw transcripts, normalized outputs, metadata, and score artefacts; path and file-size comparison against `phase4-canonical-run-manifest.md`. No source evidence was edited, moved, deleted, or synthesized.

## Expected inventory

The manifest specifies 225 slots:

- H0–H7: 8 conditions × 9 cases × 3 runs = 216 slots.
- H8 Human Expert: 9 cases × 1 run = 9 slots.
- Total: 225 slots.

Expected case/run keys are `nz-01`–`nz-07` and `au-01`–`au-02`, with runs `run-1`–`run-3` for H0–H7 and `run-1` for H8.

## Observed condition inventory

| Condition tree(s) | Raw transcripts | Normalized outputs | Empty normalized | Metadata JSON | Manifest assessment |
|---|---:|---:|---:|---:|---|
| H0 `H0-control-no-skill` | 28 | 28 | 0 | 0 | **Quarantine pending remediation:** one extra raw/output path is present relative to 27 expected slots; metadata is not in standalone JSON files and protocol fields remain incomplete. |
| H1 `H1-claude-code-sonnet` | 27 | 27 | 0 | 0 | **Quarantine pending remediation:** counts match, but standalone metadata and complete timing/token/cost evidence were not found. |
| H2 `H2-claude-code-opus` | 0 | 27 | 0 | 0 | **Quarantine:** all normalized outputs lack raw transcripts. |
| H3 `H3-gemini-cli` | 0 | 27 | 0 | 0 | **Quarantine:** all normalized outputs lack raw transcripts. |
| H4 `H4` + `H4-codex-cli` | 29 combined | 27 | 0 | 0 | **Quarantine pending attestation:** 27 raw files are in `H4`, 2 additional raw files are in `H4-codex-cli`; normalized files are in `H4-codex-cli`; joins are not proven. |
| H5 `H5` + `H5-qwen` | 29 combined | 27 | 0 | 0 | **Quarantine pending attestation:** 27 raw files are in `H5`, 2 additional raw files are in `H5-qwen`; normalized files are in `H5-qwen`; joins are not proven. |
| H6 `H6-opencode` + `H6-kilo-code` | 2 combined | 54 combined | 25 empty in `H6-opencode` | 0 | **Quarantine:** raw and normalized trees are split; all 27 `H6-kilo-code` normalized files lack same-tree raw; 25 `H6-opencode` normalized files are empty. |
| H7 `H7-amp` + `H7-copilot` | 2 combined | 54 combined | 27 empty in `H7-amp` | 0 | **Quarantine:** raw and normalized trees are split; all 27 `H7-copilot` normalized files lack same-tree raw; all 27 `H7-amp` normalized files are empty. |
| H8 `H8-human-evaluator` | 1 | 27 | 0 | 0 | **Quarantine:** only one raw receipt exists for 27 normalized paths; the manifest expects 9 human runs, not 27. |

The H0–H8 condition trees contain 149 raw transcripts and 325 normalized-output files in total, including duplicate/alternate trees and the H8 overrun. These totals are not eligible-slot totals.

Out-of-scope trees observed and excluded from the 225-slot reconciliation:

- `H8P-panel-1`, `H8P-panel-2`, `H8P-panel-3`: 27 raw and 27 normalized outputs in a separate subagent-panel condition; not H8 Human Expert and not in the current manifest.
- `H9` and `H10`: 4 raw transcripts combined; not in the current manifest.

## Slot reconciliation

| Reconciliation class | Count | Basis |
|---|---:|---|
| Expected Phase 4 slots | 225 | Canonical manifest. |
| Exact-count raw/normalized condition sets | 27 | H1 only; still not eligible because metadata is incomplete. |
| H0 raw/normalized paths observed | 28 | One extra path relative to the 27-slot condition design; requires case/run/path review. |
| H2/H3 normalized without raw | 54 | 27 each. |
| H4/H5 candidate raw-to-normalized joins | 54 | 27 each, but cross-tree provenance is unverified; 4 additional raw files are unmatched/extra relative to the 27 normalized paths. |
| H6/H7 normalized without same-tree raw | 54 | 27 each in the canonical normalized trees. |
| Empty normalized outputs | 52 | 25 in `H6-opencode`; 27 in `H7-amp`. |
| H8 normalized paths lacking raw | 26 | 27 normalized, 1 raw. |
| Slots eligible for blinding | 0 | No condition currently satisfies the full raw + metadata + normalized + receipt/attestation gate. |
| Slots explicitly quarantined by this audit | 225 pending admission decision | All expected slots remain non-eligible; reasons are recorded above. This receipt does not alter source files or manifest status. |

## Duplicate and alternate-path findings

Every standard case/run key (`nz-01`–`nz-07`, `au-01`–`au-02`, runs 1–3) appears as a normalized path in multiple condition trees, as expected for repeated evaluation conditions. Those same relative keys do not establish equivalence: condition, harness, model, raw transcript, normalized derivation, and receipt must be joined by evidence.

Observed alternate trees requiring explicit provenance decisions:

- H4 raw in `H4` versus normalized in `H4-codex-cli`.
- H5 raw in `H5` versus normalized in `H5-qwen`.
- H6 raw in `H6-opencode` versus normalized in `H6-kilo-code`; `H6-opencode` also contains 25 empty normalized files.
- H7 raw in `H7-amp` versus normalized in `H7-copilot`; every `H7-amp` normalized file is empty.
- H0 has 28 observed paths against a 27-slot design and requires anomaly resolution.
- H8 has 27 normalized paths against a 9-slot design and only one raw transcript.

No duplicate was collapsed, selected, or deleted by this audit.

## Quarantines and blockers

The following evidence is non-admissible until remediated:

1. H2 and H3 normalized outputs without raw transcripts.
2. H4/H5 cross-tree joins without operator attestation confirming condition, harness, case, run, model, and derivation.
3. H6/H7 split-tree material and all empty normalized outputs.
4. H8 human outputs without corresponding raw receipts, including the mismatch between 27 normalized paths and 9 expected slots.
5. H0 extra path and H0/H1 incomplete protocol metadata.
6. All rows lacking complete receipt fields required by the manifest, including timestamps, token counts, cost, operator, and failure mode where applicable.

Because no slot passes the complete admission gate, the sealed blinding map must remain unpopulated and Track 5 must not score or unseal these records. H8P is a separate supplementary condition and cannot substitute for H8 Human Expert without an explicit manifest/protocol decision.

## Hashes recorded safely

SHA-256 hashes were calculated only for existing files; no file contents were changed. Representative normalized-output hashes are included as audit anchors, not as eligibility evidence:

| Tree | Representative file | SHA-256 |
|---|---|---|
| H0-control-no-skill | first recursive normalized output encountered | `CABC5D0AFC3FDB129C042F80B02CD0C1FB7CE4AD8C4AEB2D7695D1A7FC39A180` |
| H1-claude-code-sonnet | first recursive normalized output encountered | `CB80F51C33FF4D2732CF1875B535C52802BC7283FD0FBF7779AA78FF2330D3FE` |
| H2-claude-code-opus | first recursive normalized output encountered | `1C9F38EB7824AC9C87147721AB3CEA965A13A7BAFB4305083EA65308386B41F5` |
| H3-gemini-cli | first recursive normalized output encountered | `AB10B6185A687FA813580CAD811AEE28C2EFFA64EBC977EA2C5D336FA0169BB2` |
| H4-codex-cli | first recursive normalized output encountered | `26F434DBC3BB74DDB51D821178B1C355F233AB562F8C239E1119CFD69F68C895` |
| H5-qwen | first recursive normalized output encountered | `3DBBBB00480629DBD4ED0E125023EA313DF148E58107F7A6DFD37E1A69615BE6` |
| H6-opencode | first recursive normalized output; empty file | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| H7-amp | first recursive normalized output; empty file | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| H7-copilot | first recursive normalized output encountered | `E1043BBD9D604A52CF3E3DD4746A1DBAD9187E347B47240E91FCAA6486410DA7` |
| H8-human-evaluator | first recursive normalized output encountered | `34F3706A016C7B1960AA324F044B11D62F80CFCD5FF954B50BC4784B781E5096` |

The empty-file hash is the standard SHA-256 for a zero-byte file; it confirms emptiness, not validity.

## Audit conclusion

The Phase 4 manifest is **not complete and has zero eligible-for-blinding slots**. The current evidence supports only a documented quarantine and remediation queue. The next safe actions are operator attestations for H4/H5, canonical reruns or raw recovery for H2/H3/H6/H7/H8, H0/H1 metadata remediation, and an explicit protocol decision for the separate H8P panel condition. No source evidence was altered by this audit.
