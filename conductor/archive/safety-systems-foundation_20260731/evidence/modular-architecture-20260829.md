# Modular Architecture Receipt — 2026-08-29

## Implemented boundary

The product, clinical-governance architecture, integration map, capability registry, architecture and decision templates, and track specifications define the portable core, domain packs, capability adapters, interfaces, evaluation, and distribution layers. They preserve organisational incident, identity, content, records, clinical, and workflow systems as external authorities.

FHIR R5, W3C PROV, CMMN, BPMN, and DMN are profiled as interchange or workflow boundaries rather than replacement ontologies. GitHub, Conductor, JSON Schema, Python, pytest, client adapters, and SourceRight are used behind replaceable contracts with explicit fallbacks and exit paths.

Capability installation is fail-closed: preflight and verification are implemented; update, executable rollback, and destructive uninstall are explicitly unavailable until safe generation and quarantine contracts exist. Defining those operations as unavailable satisfies the contract without inventing unsafe behaviour.

## Evidence

- `conductor/integration-map.json`
- `conductor/clinical-governance-architecture.json`
- `conductor/capability-profiles.json`
- `conductor/architecture/template.md`
- `conductor/decisions/template.md`
- `evidence/fit-gap-20260811.md`
- `evidence/installer-preflight-20260811.md`
- `evidence/installer-lifecycle-20260811.md`

No new enterprise connector, credential, production system, permanent fork, or release was created.
