# Phase 4 Slot Validator Receipt

Date: 2026-08-03
Validator: `tools/validate_phase4_slot.ps1`
Status: negative-path validation passed; positive primary fixture pending

The validator was run against `H8P-panel-2/nz-case-01/run-1`. It correctly
quarantined the slot because it lacks `attestation.md`, `slot-receipt.json`,
and required model, harness, operator, start, and end metadata. H8P remains
supplementary and was not admitted to the primary manifest.

The validator checks required files, non-empty evidence, expected condition/
case/run identity, eight normalized sections, required metadata, SHA-256
receipt entries, and actual hash matches. Exit 0 means eligible for admission
review only; the admission custodian must still issue the admission receipt.
