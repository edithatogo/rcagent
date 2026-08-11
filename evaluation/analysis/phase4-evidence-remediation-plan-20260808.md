# Phase 4 Evidence Remediation Plan

Date: 2026-08-08
Status: active; external execution gate remains blocked

## Objective

Produce a provenance-complete Phase 4 evidence set without altering or
backfilling historical records, then admit only slot packages that pass the
canonical validator.

## Path A — recover historical evidence

For each affected H0-H2 slot and each alternate-path H3-H8 candidate:

1. Search the original execution environment, provider/client logs, durable
   exports, and operator-held receipts.
2. Preserve the source artefact unchanged and calculate its hash.
3. Reconcile it to condition, case, run, prompt, harness, model, timestamps,
   configuration, raw output, normalized output, and operator/evaluator
   attestation.
4. Reject any field inferred from filenames, directory names, or normalized
   output alone.
5. Package the evidence using the atomic Phase 4 slot template.

## Path B — canonical rerun

Use when Path A cannot supply an immutable field or complete raw transcript.
The operator must perform the run with the approved prompt, condition,
harness, model, and configuration, then capture the raw transcript, metadata,
hashes, normalization, attestation, and slot receipt before submission.

## Order of operations

1. H0/H1: resolve metadata gaps and the H0 extra path, or rerun affected slots.
2. H2: rerun or recover raw transcripts for normalized-only slots.
3. H3-H7: execute operator-controlled harness packets and collect receipts.
4. H8: obtain nine human-expert outputs and evaluator attestations.
5. Run the manifest audit and slot validator after every evidence batch.
6. Admit only complete packages; retain all others in quarantine.
7. Run Track 5 only after Phase 4 admission passes.

## Stop conditions

- Missing raw transcript, prompt, model/harness identity, timestamps, or
  attestation: quarantine the slot.
- Unresolved raw-to-normalized join: quarantine the slot.
- Any request to infer or fabricate historical metadata: stop and record a
  blocked receipt.
- Zero eligible slots after audit: keep blinding sealed and Track 5/6 locked.

## Acceptance gate

Phase 4 is complete only when every required canonical slot has a valid atomic
package, every quarantine disposition is resolved or explicitly excluded by an
authorised protocol amendment, the final manifest receipt passes, and Track 5
preflight returns PASS.
