# External Evidence Dispatch Ledger

Current review override: use
[agent panels](../../decisions/20260830-001-legacy-agent-review.md) for
repository review appointments. This ledger preserves historical execution
requests; no request has been sent by this amendment. H8 remains a human data
condition, not a review role. Its disposition awaits the
[prospective protocol decision](../../decisions/20260830-002-prospective-agent-study.md).

Updated: 2026-08-03
Admission status: blocked; zero eligible Phase 4 slots

Mandatory execution controls are defined in
`option-a-execution-control.md`. Owner names, appointment receipts, T0, and
deadlines are intentionally blank until authorised appointments are supplied.

| Condition | Owner/harness | Current state | Required unblock evidence |
|---|---|---|---|
| H0 | Internal custodian | In progress | Resolve extra path and complete metadata/receipt fields |
| H1 | Internal custodian | In progress | Complete metadata, timing, token/cost, and receipt fields |
| H2 | Claude Code operator | Blocked | 27 Claude Code/Opus raw transcripts, normalized outputs, metadata, hashes, receipts |
| H3 | Gemini operator | Blocked | 27 Gemini raw transcripts, normalized outputs, metadata, hashes, receipts |
| H4 | Codex operator | Blocked | Attested raw-to-normalized joins or 27 canonical reruns |
| H5 | Qwen operator | Blocked | Attested raw-to-normalized joins or 27 canonical reruns |
| H6 | Kilo Code operator | Blocked | Harness identity, non-empty normalized outputs, raw evidence, receipts |
| H7 | Copilot operator | Blocked | Harness identity, non-empty normalized outputs, raw evidence, receipts |
| H8 | Human Expert | Blocked | Nine raw case receipts, normalized outputs, metadata, evaluator attestations |

## Operational blockers still requiring assignment

| Control | Current state | Required next evidence |
|---|---|---|
| Role appointments | Unassigned | Named appointment/authority receipts |
| H2-H7 credentials and trust | Unverified | Harness preflight receipts without secrets |
| H8 evaluator authority/conflicts | Unverified | Appointment, confidentiality, and conflict receipt |
| Submission schedule | Not started | Study-owner T0 declaration and dated deadlines |
| Automated slot admission | Validator implemented; full positive primary-slot fixture pending | Passing validator and synthetic fixture receipt; fixture is not an admitted study observation |
| Irrecoverability review | Not scheduled | T0+22 owner decision receipt |

## Admission procedure

1. Submit evidence through `evaluation/analysis/external-execution-request.md`.
2. Preserve originals and quarantine unjoined, empty, inferred, or placeholder files.
3. Re-run the canonical manifest audit.
4. Admit only rows satisfying raw, normalized, metadata, hash, and attestation requirements.
5. Run `tools/track5_preflight.ps1`; do not proceed if it fails.

H8P remains supplementary and is excluded from the H8 Human Expert row set.
