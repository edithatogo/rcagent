# Phase 4 Canonical Run Manifest

**Status:** Awaiting operator execution  
**Cases:** 9 total (7 NZ, 2 AU)

## Expected run inventory

| Conditions | Runs per case | Expected runs |
|---|---:|---:|
| H0–H7 | 3 | 216 |
| H8 | 1 | 9 |
| **Total** |  | **225** |

## Required manifest fields

Each row must contain:

```text
eval_id,condition,case_id,run,raw_path,normalized_path,receipt_path,
model,harness,temperature,timestamp_start,timestamp_end,
input_tokens,output_tokens,cost_usd,operator,status,failure_mode
```

## Admission statuses

- `pending` — row reserved but no valid evidence yet.
- `raw-captured` — raw transcript and metadata validated.
- `normalized` — eight-section normalized output derived from the raw transcript.
- `attested` — operator or human attestation retained.
- `eligible-for-blinding` — all required evidence and metadata pass validation.
- `quarantined` — empty, placeholder, mismatched, or otherwise invalid evidence.

## Acceptance gate

The manifest is complete only when all 225 expected rows are either `eligible-for-blinding` or explicitly `quarantined` with a documented reason. Only eligible rows may enter the sealed blinding map; quarantined rows remain excluded from Track 5 scoring.
