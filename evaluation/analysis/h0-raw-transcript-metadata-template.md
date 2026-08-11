# H0 Raw Transcript Metadata Template

Use one copy per canonical H0 case/run. This template is for future or
operator-supplied evidence; it must not be backfilled from directory names or
filesystem timestamps.

```yaml
condition: H0
case_id:
run_id:
model_id:
harness:
harness_version:
temperature:
started_at:
ended_at:
endpoint: N/A
prompt_sha256:
operator:
token_count: unavailable
token_count_reason:
cost: unavailable
cost_reason:
```

The raw transcript below the metadata must be unedited. A complete slot also
requires `normalized-output.md`, `attestation.md`, and `slot-receipt.json`.
