# H0 Public-Evidence Boundary Receipt

Date: 2026-08-08
Track: `eval-run-H0_20260225`
Purpose: record what authoritative public documentation can and cannot remediate
for the H0 evidence gap.

## Public documentation reviewed

- OpenAI documents describe request identifiers, response identifiers, model,
  creation time, and usage fields in API responses, and recommend retaining
  request IDs for support and troubleshooting.
- Google Gemini API documentation describes the public API surface and response
  usage metadata.
- These sources establish capture requirements for a future controlled rerun;
  they are not evidence that any historical H0 request occurred with those
  fields.

## Boundary

Public internet sources can supply current provider field definitions,
versioned API semantics, and a schema/runbook for future collection. They cannot
reconstruct H0-specific execution facts that are absent from the repository:

- the exact prompt and request payload for each affected slot;
- provider request/response IDs and timestamps;
- model, client, harness, configuration, and environment versions;
- token usage, cost, operator identity, attestations, or chain-of-custody;
- the missing raw completion or an authoritative disposition for the extra path.

Those facts are private execution evidence. Substituting public examples would
be fabrication and would invalidate Phase 4 admission.

## Action taken

- No historical H0 metadata was invented or backfilled from public sources.
- Existing raw and normalized evidence remains preserved and `not-admitted`.
- The future rerun requirement is confirmed: capture provider-native IDs,
  timestamps, model/configuration, usage, client/harness versions, prompt,
  raw output, hashes, operator attestation, and a slot receipt atomically.
- H0 remains blocked pending immutable execution metadata/dispositions or a
  canonical rerun.

## Result

Internet research addressed the specification-side gap only. It did not and
cannot close the historical-evidence gap. The admission state is unchanged:
zero H0 slots are eligible for archival.
