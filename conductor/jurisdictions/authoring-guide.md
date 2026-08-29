# Jurisdiction Pack Authoring Guide

This guide defines the rights-safe process for adding or updating a jurisdiction profile without changing the jurisdiction-neutral core.

## Authority boundary

The issuing body and the organisation's approved incident, records and workflow systems remain authoritative. A pack is a versioned mapping and validation profile. It cannot lodge or close an incident, approve a review, interpret legislation, establish privilege, accept risk or certify compliance.

Every state profile inherits `jurisdiction-national`. State profiles add only state-specific sources and rules. Local procedures remain a separate `local` tier and require evidence of approval, applicability and rights before use.

## Source registration

For every source, record:

- issuer, exact title, identifier and version;
- jurisdiction, tier, authority level and current status;
- publication, review, retrieval and replacement dates where available;
- canonical HTTPS URL and a SHA-256 checksum of downloaded bytes where practical;
- rights status and whether the artefact is link-only;
- review cadence, limitations and unresolved interpretation.

Use `current`, `under_review`, `draft`, `consultation`, `superseded`, `local`, `advisory` or `unavailable` exactly. Draft, consultation, superseded and unavailable sources cannot drive rules. Link to restricted or unclear-rights content; do not copy it.

Rules sourced from an `under_review` authority must use
`activation_status: pending_owner_decision`, cite the corresponding
`decision_id`, disclose the uncertainty, and keep their jurisdiction pack and
capability profile blocked. Change those states to active/implemented only
after the decision record contains explicit approval evidence.

## Rule authoring

Each rule must cite at least one registered current, under-review, local or advisory source, state its authority and requirement level, and map to a valid canonical state transition. Preserve the external system-of-record boundary and require accountable human review.

Do not infer:

- clinical, legal, policy, employment, regulatory or privilege conclusions;
- that notification, disclosure, approval, submission, action or closure occurred externally;
- a mandatory requirement from guidance or a catalogue;
- state applicability from a national framework; or
- local applicability or approval from the presence of a document.

## Forms and templates

Inventory external forms as `linked_only` until rights permit a different treatment. Original or generated mappings may name canonical fields but must not reproduce branded layouts or restricted wording. Locally supplied templates stay in an authorised private compartment and are never committed by default.

## Drift workflow

1. Retrieve the source only in an authorised network environment.
2. Preserve the previous registry snapshot and create a candidate snapshot.
3. Run `python -m tools.jurisdiction_pack validate <candidate>`.
4. Run `python -m tools.jurisdiction_pack drift <baseline> <candidate>`.
5. Treat `guidance`, `normative` and `breaking` changes as material. The tool returns `review_required`, lists affected rules and invalidates affected compatibility receipts without changing behaviour.
6. An unavailable upstream is `unavailable_not_passed`; retain the last verified snapshot and retry at the declared cadence.
7. An accountable policy or clinical-governance reviewer must approve any interpretation that changes meaning before the candidate becomes current.

## Capability registration

Register a profile as `jurisdiction-<code>` in `conductor/capability-profiles.json`, inherit `jurisdiction-national`, add schema and negative fixtures, and document the system-of-record, safe fallback and replacement path in `conductor/integration-map.json`. A new connector, copied restricted template or organisation-specific localisation remains an owner gate.
