# FAW12 / D5 — representation and provenance comparison (initial synthetic contract)

## Authority and predecessor

D5 begins only after D3 source and Conductor acceptance and the bounded D4
comparison infrastructure have protected-merged. The accepted D3 source
filters an actor/cutoff evidence view; D4 retains reference-label and
case-family separation. Track 13 owns this narrow D5 implementation, while
Track 12 owns scientific modality and process studies. Do not duplicate an
OCR framework, XES/OCEL engine or general document parser.

The first increment is a deterministic **simulation of representation outputs**,
not a new OCR, speech, clinical, process or model execution. Reuse the D3
`assemble_decision_packet` boundary and D0 source/span validation. Existing
`tools.docling_synthetic_evaluation` and the public Docling test receipt
are inputs for later adapter assessment; the measured born-digital conversion
does not qualify scanned/rotated/handwritten or other OCR classes. Reuse
maintained optional adapters only after explicit version/license/egress and
synthetic/real-data permission review.

## Proposed public seam

`compare_representations(d3_case: object, rows: object)` accepts a bounded list
of at most 64 objects with exactly:

- `id`: unique, nonempty bounded identity
- `event_id`: D3-visible source-verified event ID; an excluded future event
  must not appear in output, retrieval or exception text
- `comparison_key`: a **caller-declared** synthetic alignment key for
  potentially related observations, not a semantic entailment
- `origin_family_id`: **caller-declared** upstream family identity, common
  across native extraction and OCR of one artefact and any known copied
  upstream records
- `representation_kind`: `native_text`, `layout_ocr` or
  `structured_log`
- `status`: `simulated_annotation` or `unsupported`
- `value`: a bounded literal transcription for simulated records, or null
  when unsupported

All annotations point to the **same immutable D3 packet replay**, with
case/recipient/cutoff and source-span evidence. Source SHA-256 must not be
split into different origin families; source-family declared independence is
not proof of independent systems of record. Every public error is generic.
Input and output size limits apply before source/projected-data processing.
No dynamic regex, file read, arbitrary remote access or model call is allowed.

## Outputs and invariants

The result binds the D3 view fingerprint, visible source IDs/versions/digests
and exact span anchors; includes all admitted annotations, including
disagreements, null/unsupported outcomes and explicit origin groups; and emits
a deterministic comparison summary per alignment key.

- Native text and OCR of the **same source** count as *one* origin, never
  independent corroboration, even when they agree.
- Conflicting renderings within the same origin remain a
  `representation_disagreement`; do not select or average a value.
- A separately sourced log can add a second *declared* origin, but its
  independence is not externally verified. No consensus is promoted as a
  clinical finding.
- Unsupported/unexecuted modalities contribute no observed value and do not
  become failures/successes counted as measurements of OCR quality.
- Retain negative results, source provenance and abstention. Reordering input
  rows does not change byte-identical canonical output.

The initial result always declares `synthetic_contract_only`,
`ocr_executed=false`, `model_executed=false`,
`independence_qualified=false`, `clinical_qualification=none`.
Actual native/layout/OCR conversion, reading-order and table/unit loss,
structured-log exchange (XES/OCEL), real provenance independence and measured
model/adapter performance remain future D5 gates. The existing optional
Docling evaluation and upstream process connectors are not silently
relabelled as completed D5 experiments.

## Test-first acceptance

Freeze synthetic positive/negative examples for shared-source duplicate
representations, within-source text/OCR disagreement, distinct log origin,
unknown/unsupported adapter, late recipient/cutoff exclusion, forged source
SHA/span, duplicated IDs, mismatched origin declarations and deterministic
input permutations. Require locked lint/format/ty/strict basedpyright,
repository governance tests, full hosted Quality matrix, dependency review
and privacy/secrets before any later protected merge.

This file records **D5 implementation started**. It is not a claim of D5
acceptance or completed multimodal scientific evaluation.
