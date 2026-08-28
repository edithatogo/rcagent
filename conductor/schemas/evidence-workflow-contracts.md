# Evidence workflow contracts

## Workflow profile

The core state machine covers intake, triage, review, investigation,
consultation, approval, action, effectiveness review, closure, reopen, appeal,
and withdrawal. Events distinguish submission, immediate response, huddle,
provisional assessment, review-path selection, team formation, evidence
acquisition, interviews, systems analysis, proposed findings, literature-
informed recommendations, decisions, learning, correction, and withdrawal.

Every transition names the actor role and authority. Optional preconditions,
deadline, and exception-path fields preserve orchestration context without
asserting jurisdiction-specific time limits. Correction and evidence-
withdrawal events may retain state; all other transitions must match the
declared transition table. Specialist pathways—lookback, cluster, individual-
worker, cultural, clinical-risk, enterprise-risk, quality-improvement,
medicolegal, and related-policy—are explicit referrals, never hidden
subprocesses.

CMMN is the semantic profile for adaptive investigation work, BPMN for
predictable integration processes, and DMN for transparent decision tables.
The project does not embed or claim conformance with an execution engine.

## Interchange boundaries

| Core concept | Candidate FHIR R5 boundary | Limitation |
|---|---|---|
| case and harm context | `AdverseEvent` | Exchange view only; not the investigation ontology |
| source attribution and derivation | `Provenance` | W3C PROV-aligned attribution is richer than a resource pointer |
| append-only access/change event | `AuditEvent` | Does not replace organisational audit infrastructure |
| governed action | `Task` | Local action/effectiveness semantics remain canonical |
| source or artefact reference | `DocumentReference` | Content and rights remain in the approved system |
| structured intake | `Questionnaire` / `QuestionnaireResponse` | Requires a separately versioned jurisdiction profile |

W3C PROV mappings use source/evidence as entities, workflow and transformation
events as activities, roles as agents, relationships as derivations, and
provenance author/reviewer fields as attribution. No RDF serialization claim
is made. ims+ or another approved platform remains authoritative; imports
must carry its identifier and version, and exports are reconciled rather than
treated as an independent shadow record.

## Persistence and compartments

The `EvidenceStore` port accepts and returns JSON-compatible values only. A
production adapter must provide encryption at rest, access control, atomic
version checks, idempotency, append-only audit receipts, backup and restore,
and organisation-approved deletion/retention behavior. The core deliberately
selects no database, key manager, or retention period.

Compartments are explicit capability profiles:

- `public_remote`: derived, reviewed, content-redacted material only;
- `governed_hybrid`: approved split processing with recorded transfers;
- `fully_local`: no external processing; and
- `air_gapped`: local dependencies and deterministic fixtures only.

Unavailable encryption, authority, or compartment capability is an error, not
a fallback to plaintext or remote execution.

## Serialization, migration, and views

Canonical JSON uses UTF-8, sorted keys, compact separators, stable identifiers,
and SHA-256 fingerprints. Imports validate before storage. Version 1.0 can be
migrated additively to 1.1; all other migrations fail closed. The source record
is retained for rollback and the migrated record receives a new version only
after an adapter commits it atomically.

Governed export preserves the canonical record. Public export removes evidence
content and confidentiality labels, records the export profile, and adds an
export fingerprint. Human-readable reports are derived views and must label
observations, accounts, inference, hypotheses, findings, recommendations, and
decisions separately.

## Adapter operations and failure semantics

`tools.evidence_ports` defines replaceable evidence-store, retrieval,
capability, workflow, and export ports. Each operation carries a bounded
timeout, idempotency key, privacy mode, and operation identifier. Results use
`succeeded`, `rejected`, `unavailable`, `timeout`, or `failed`, with retryability
declared explicitly. Cancellation is represented by the caller ceasing the
bounded operation; adapters must not commit after cancellation.

The SourceRight adapter owns only subprocess translation. It permits local or
air-gapped profiles, caps diagnostics, rejects malformed JSON, distinguishes
timeout from deterministic failure, and never invokes a write/apply command.
Its replacement condition is a maintained native project contract with equal
offline, provenance, and failure semantics; the upstream reference is
`edithatogo/sourceright`, pinned in `integration-map.json`.
