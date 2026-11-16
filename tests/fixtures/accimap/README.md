# Synthetic AcciMap example

These repository-authored records were constructed on 16 November 2026 from
literal invented statements. They contain no real incident, patient, staff or
organisation data. The case uses a simulated alert exercise solely to test
graph structure and evidence references.

- `record.json` uses the unchanged canonical safety-work 1.1 schema.
- `graph.json` is the versioned AcciMap companion.
- `expected.json` records hand-specified topology expectations. Expected paths
  were not calculated with the production traversal. SHA-256 bindings were
  independently calculated using standard-library canonical JSON serialization.

Policy and queue factors have supported-declared paths to the incident outcome.
An additional direct policy pathway is hypothetical and has no evidence. Queue
availability is contested by two generated accounts. A context factor remains
unassigned and disconnected. The single proposed action has not been implemented
or evaluated; no map review is declared.

The example demonstrates preservation of uncertainty and incomplete drafts.
Its source/evidence content fingerprints identify invented bytes, not verified
clinical facts. The word `supported` is an analyst declaration checked for
references; neither this fixture nor its tests proves a causal interpretation.
