# Safety-work record semantics (version 1.0)

The JSON Schema in `safety-work.schema.json` is the canonical machine-readable
contract. It is a client-neutral validation and interchange profile, not an
incident-management system, clinical ontology, retention schedule, or claim
of regulatory compliance.

## Authority boundaries

- `authority` records who authorises the case or transition; it does not grant
  authority by itself.
- `jurisdiction`, `confidentiality`, and `retention_rule` are descriptive
  values supplied by an approved jurisdiction pack or system of record. The
  core does not invent legal meanings or retention periods.
- `privacy_mode` records the permitted execution boundary. It does not prove
  that storage or transport controls were correctly implemented.
- ims+ or another approved organisational platform remains the system of
  record. Imports and exports must reconcile identifiers and versions rather
  than maintain an undisclosed shadow state.

## Statements and provenance

Every statement has a stable identifier, explicit semantic kind, text, and a
provenance block naming its source, author role, recording time, and review
state. A SHA-256 fingerprint, transformation description, and model
involvement disclosure are available when applicable.

`observed_fact` means a directly recorded observation, not an ultimate truth.
`reported_account` preserves an attributed account. `inference` and
`hypothesis` remain analytical and cannot be silently promoted to `finding` or
`decision`. `recommendation`, `problem`, `strength`, and `weakness` remain
distinct so that reports do not collapse intermediate reasoning.

Relationships explicitly represent support, contradiction, derivation,
supersession, relevance, implementation, and evaluation. Referenced local
identifiers must exist. Withdrawal is preserved rather than deleting the
statement.

The concepts align with W3C PROV entity, activity, agent, derivation, and
attribution, but version 1.0 is not a complete PROV-O serialization.

## Workflow

Events are append-oriented records of an authorised transition. The validator
fails closed for transitions outside the declared state machine, unknown actor
roles, duplicate identifiers, broken relationship references, and a case state
that disagrees with the final event.

The state machine is a jurisdiction-neutral constraint. CMMN is the candidate
profile for adaptive investigation work, BPMN for predictable processes, and
DMN for transparent decision tables. No engine is embedded in the core.

FHIR R5 `AdverseEvent`, `Provenance`, `AuditEvent`, `Task`, and
`DocumentReference` are candidate exchange boundaries. FHIR remains an
interchange format, not the investigation ontology; resource mappings and
version compatibility profiles require separate contract evidence.

## Versioning and serialization

Version 1.0 accepts only declared fields and canonical JSON-compatible values.
`canonical_round_trip` validates before producing a deterministic key-sorted
representation. Schema migrations, encrypted persistence, redaction profiles,
and external adapters are separate contracts and are not implied by this
foundation slice.
