# Phase 4 Atomic Slot Package Template

Each canonical slot directory must contain exactly the required evidence files:

- `raw-transcript.md`
- `normalized-output.md`
- `metadata.json`
- `attestation.md`
- `slot-receipt.json`

`metadata.json` must identify condition, case, run, model, harness, start/end
timestamps, and operator. Token/cost fields must be recorded or explicitly
marked unavailable with a reason under the approved metadata policy.

`slot-receipt.json` must contain a `files` array with `path` and SHA-256 for
each of the other four files. Run:

`powershell -File tools/validate_phase4_slot.ps1 -SlotRoot <path> -ExpectedCondition <Hn> -ExpectedCase <case> -ExpectedRun <run>`

Exit 0 means eligible for admission review, not automatic admission. Exit 1
means quarantine with the emitted diagnostics.
