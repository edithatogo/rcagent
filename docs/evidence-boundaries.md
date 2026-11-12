# Evidence References, Exports and Template Admission

## Typed References

`tools/evidence_core.py` first checks the safety-work JSON Schema, then resolves
semantic references within the correct entity collection. Globally unique IDs
are still required, but existence anywhere in the record is insufficient.

| Reference | Required target |
|---|---|
| Artefact/evidence `source_id` | Source |
| Evidence `artefact_id` | Artefact |
| Statement provenance author/reviewer | Role |
| Statement provenance source in schema 1.1 | Source |
| Statement `supersedes` | Another statement |
| Factor/outcome `statement_id`, review `statement_ids` | Statement |
| Event actor, action owner, review reviewers | Role |
| Event/outcome evidence, action implementation evidence | Evidence |
| Action `recommendation_id` | Statement whose kind is `recommendation` |

Schema 1.0 retains its legacy provenance-source migration path: migration to
1.1 creates explicitly unverified source records for unresolved source IDs.
An ID already registered as a different entity kind is rejected even in 1.0.
This compatibility behaviour does not establish source validity or evidence
support. Malformed collections and unhashable references return diagnostics
rather than interrupting validation with an exception.

Relationship direction and endpoint types are explicit:

| Relation | From | To |
|---|---|---|
| `supports`, `contradicts` | Source, artefact, evidence, statement or factor | Statement or factor |
| `derived_from` | Artefact, evidence, statement, factor or outcome | Source, artefact, evidence, statement or factor |
| `implements` | Action | Recommendation statement |
| `evaluates` | Review or outcome | Statement, factor or action |
| `supersedes` | A supported entity kind except roles/events | A different entity of the same kind |
| `relevant_to` | Any registered entity | Any registered entity |

`relevant_to` expresses association only. A valid reference or relationship
proves structural consistency; it does not prove the truth, sufficiency,
independence or causal force of the evidence.

## Export Compatibility and Privacy Boundary

`export_record(..., profile="governed")` preserves the existing governed view:
a validated deep copy of the canonical record with export profile and
fingerprint. It retains record content and the original privacy mode. It does
not transmit the result or establish permission to disclose it.

`profile="public"` now rejects `fully_local`, `governed_hybrid` and `air_gapped`
records. It never changes a private record into a public one. The caller must
already have a valid record classified `public_remote`; the helper cannot
verify the correctness of that upstream classification.

The public result is an explicit `public-summary-1.0` contract, not a canonical
case record. Consumers expecting the previous record-shaped public export
must update rather than treating the summary as an imported case. It contains
only these fields:

| Field | Content |
|---|---|
| `schema_version` | `public-summary-1.0` |
| `source_schema_version` | Validated source schema version |
| `privacy_mode` | `public_remote` |
| `state` | Validated lifecycle state enum |
| `record_counts` | Counts for fixed entity collections |
| `statement_kinds` | Counts for validated statement-kind enum values |
| `content_policy` | `metadata-only-no-record-text-or-identifiers` |
| `distribution_authority` | `not-established-by-export` |
| `export_profile` | `public` |
| `export_fingerprint` | Hash of the summary before this field is added |

No case/role/source identifiers, dates, jurisdiction, free text, raw source
fingerprints or evidence content enter this view. Changing arbitrary narrative
content cannot change the exported summary or its fingerprint. Both export
paths leave the caller's record unchanged.

This is data minimisation, not anonymisation. Even counts and state may reveal
information in context. Disclosure still requires the applicable purpose,
audience, data classification and authority. The helper supplies no claim of
de-identification, legal protection or permitted remote use.

## Revision-Bound Draft Templates

Both portable and client-plugin archive builders require
`skills/rca-investigation/assets/template-admission.json`. It inventories the
exact revised templates, style guides, use contract and supporting Just
Culture guide admitted for draft packaging. The gate validates the same
captured bytes written into the archive and records the manifest SHA-256 in
archive provenance. Missing assets, changed hashes, unlisted rendering assets,
duplicate entries, ambiguous JSON and non-admitted status fail before an
archive is written.

The revised content removes blanket quality-improvement protection claims,
universal timing and classification requirements, pre-filled closure approval,
and automated culpability trees. It records jurisdiction, current sources,
authority, uncertainty and accountable decisions as fields to verify. Styling
cannot silently restore the removed confidentiality markings.

The historical audit and SHA-256 inventory under `evaluation/interfaces/`
remain unchanged and quarantined. They describe different bytes. The current
admission is confined to draft packaging; it does not reclassify the old
revisions, certify a framework, grant rights to institutional content, or
establish clinical/legal approval. A changed manifest still requires content
review; hashes detect changes but cannot prove review quality. Release-source
checks separately bind the inventory and archive payload to the selected Git
revision.

## Verification

Regression tests replace references with existing IDs of the wrong kind,
exercise relationship endpoint semantics, preserve governed export behaviour,
and check that private modes cannot be reclassified by export. Hypothesis
generates cross-kind substitutions and arbitrary Unicode narrative changes
to test structural and disclosure invariants. Template tests exercise modified,
missing, unlisted, quarantined and malformed inventories for all archive
builders and simulate a filesystem change after validation to check that the
captured validated bytes are the bytes packaged.
