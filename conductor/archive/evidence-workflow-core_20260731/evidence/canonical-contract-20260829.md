# Canonical safety-work contract receipt

- Track: `evidence-workflow-core_20260731`
- Functional commit: `cb9d9fc805c8ba09b79accefad232859fba0ee61`
- Scope: reversible, synthetic, jurisdiction-neutral foundation
- System-of-record boundary: ims+ or another approved organisational incident
  platform; this repository provides validation and interchange contracts only

## Delivered

- Draft 2020-12 JSON Schema with stable identifiers, authority, jurisdiction,
  privacy mode, typed statements, provenance, relationships, workflow events,
  actions, effectiveness state, and residual risk.
- Human-readable semantics and standards boundaries.
- Fail-closed semantic validation for duplicate identifiers, role references,
  relationship references, workflow transitions, and terminal case state.
- Deterministic validated JSON round trip and synthetic fixture coverage.

## Validation

Executed in the repository Python environment:

```text
python -m pytest tests/test_evidence_core.py -q
7 passed
python -m ruff check tools/evidence_core.py tests/test_evidence_core.py
All checks passed
python -m ty check tools/evidence_core.py tests/test_evidence_core.py
All checks passed
python -m basedpyright tools/evidence_core.py tests/test_evidence_core.py
0 errors, 0 warnings, 0 notes
```

The repository-wide gate also passed: Ruff, ty, basedpyright, gremlin scan,
governance validation, and pytest. The test suite reported 98 passed and 5
PowerShell-dependent tests skipped under the documented local compatibility
environment, with 83.55% total coverage against the 80% requirement.

## Limitations and negative findings

- This slice is not a complete case ontology and does not claim FHIR, PROV-O,
  CMMN, BPMN, or DMN conformance.
- It does not implement persistence, encryption, migrations, redaction,
  retention rules, adapters, or source verification.
- `source_id` is presently an external reference; a source/evidence collection
  and SourceRight adapter remain open work.
- No real patient, staff, or incident data was used.
- No clinical validity, legal status, deployment, or release claim is made.
