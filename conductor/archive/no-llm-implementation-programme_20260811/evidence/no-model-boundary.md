# No-Model Execution Boundary

This programme may implement deterministic contracts, schemas, adapters, fixtures, mocks, dry-run paths, validators, packaging, and resource discovery without downloading or executing model weights.

## Permitted

- Synthetic, public, or already-authorised fixtures.
- Deterministic unit, property, schema, contract, integration, privacy, security, and provenance tests.
- Mock model descriptors and recorded capability metadata that cannot initiate inference.
- Runtime discovery and preflight that perform no installation, download, authentication, paid call, or model execution.
- Hosted repository checks already configured for source validation.

## Prohibited without a new gate

- Model-weight, dataset, or opaque binary downloads.
- Hosted inference, paid API use, credential entry, or new network-egress paths.
- Training, fine-tuning, benchmark execution, or human evaluation represented as completed from mocks.
- Real clinical, employee, consumer, or other private data.

Every test double must identify itself as synthetic or mocked, reject production credentials and private inputs, and avoid producing performance, clinical-validity, or release claims.
