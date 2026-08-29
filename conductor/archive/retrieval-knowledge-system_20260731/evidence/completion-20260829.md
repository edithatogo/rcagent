# Track 07 completion evidence

Completed: 2026-08-29

## Supported result

The repository supports a deterministic SQLite FTS5 lexical retrieval profile
over schema-validated, repository-generated synthetic public content. Every
index is durably bound to exactly one compartment. Search defaults to current
records before limiting results and emits source, location, transformation,
rights-basis, checksum, safety, filter and query receipts.

Lifecycle operations cover incremental ingest, correction, supersession,
deletion, rebuild, backup, restore, deterministic export and compartment-bound
audit receipts. Corpus validation defines chunk, page, section, table,
transcript, image-region and signal-window provenance and rejects unadmitted
rights, cross-compartment units, checksum drift and instruction-like source or
metadata unless quarantined.

Grounding is deliberately claim-link-only and always abstains from synthesis;
it does not treat caller assertions or a copied checksum as semantic support.
Literature and SourceRight contracts preserve exact negative states. No
Track 07 SourceRight success, external provider result, study appraisal,
clinical interpretation or recommendation is claimed.

## Negative-result closures

- Vector retrieval, embeddings, hybrid retrieval and model reranking remain
  unsupported because no model, weights licence, device profile or measured
  gain was admitted.
- External literature providers and approved-public corpus admission remain
  fail closed because no exact provider or public-rights receipt registry was
  admitted.
- Federation remains a public synthetic contract only. Governed-private and
  cross-compartment use is rejected.
- Latency and allocation observations are descriptive, separately hashed and
  non-operational. No threshold, deployment or organisational policy is set.

## Verification

- Archive-candidate code and specification revision:
  `bcad1071bdee3481dbaf4574ec73bce4814f8213`.
- Environment: macOS 26.6.2 arm64; Python 3.14.5; SQLite 3.50.4;
  network-disabled deterministic retrieval fixtures.
- `uv run ruff check tools tests`: passed.
- `uv run ty check tools tests`: passed.
- `uv run basedpyright`: zero errors.
- `uv run python -m tools.check_gremlins .`: no gremlins found.
- `uv run python -m tools.validate_repository`: passed.
- `uv run python -m tools.benchmark_harness validate`: passed.
- `uv run python -m tools.benchmark_harness run --suite regression`: seven of
  seven deterministic cases passed; no model or external execution.
- `uv run pytest --cov=tools --cov-report=term-missing`: final archive replay
  passed 302 tests in 55.53 seconds; 90.90% total tools coverage; retrieval
  module coverage 93%.
- `uv run pytest -q tests/test_retrieval_system.py --cov=tools.retrieval_system
  --cov-report=term-missing`: 18 passed; 92.59% focused module coverage.
- PR #54 merged as `c8d0ea3`; its late 80.77% Codecov patch result exposed a
  hosted evidence gap after merge. PR #55 added negative-path tests, merged as
  `a7f2787`, and passed Codecov patch plus Agent Skill Conformance, dependency
  review, Vale, Linux, macOS and Windows quality checks.
- Fresh archive review panel evidence is recorded in
  [review-panel-20260829.md](./review-panel-20260829.md). This is agent
  agreement only, not clinical, legal, policy, regulatory, employment,
  cultural-safety, organisational or deployment approval.

## Acceptance evidence mapping

| Criterion | Direct evidence |
|---|---|
| AC1 source and provenance metadata | `conductor/schemas/retrieval-corpus.schema.json`, `evaluation/retrieval/synthetic-public-corpus.json`, `test_manifest_admits_only_generated_public_units` |
| AC2 deterministic full-text baseline | `LexicalIndex` in `tools/retrieval_system.py`, `test_lexical_baseline_filters_citations_and_current_status` |
| AC3 optional stages only after measured benefit | `evaluation/retrieval/profiles.json`, `evidence/fit-gap-20260829.md`, `test_profiles_reject_missing_lifecycle_and_enabled_optional_capability` |
| AC4 citations, conflict visibility and abstention | `grounded_answer`, `test_grounding_conflicts_poisoning_and_abstention` |
| AC5 public/private non-join | persistent `index_metadata` compartment binding, `test_lifecycle_delete_export_backup_and_restore` |
| AC6 lifecycle, injection and drift tests | `test_lifecycle_delete_export_backup_and_restore`, `test_raw_mixed_compartment_and_rights_manifest_fails_closed`, `test_source_drift_marks_retrieval_receipts_for_rebuild` |
| AC7 literature receipt fidelity | `evaluation/retrieval/literature-contract-receipt-20260829.json`, `validate_literature_receipt`, literature and malformed-receipt regression tests |
| AC8 governed retrieval controls | `validate_federated_request`, `test_federated_controls_reject_cross_case_causal_or_cross_compartment_use` |
| AC9 no causal finding from prior retrieval | causal-finding rejection in `validate_federated_request` and the same federation regression test |

## Boundaries

The artefacts contain generated synthetic descriptors only and are licensed
under the repository's Apache-2.0 licence. They contain no private clinical or
employee data and claim no third-party rights. Clinical, policy, legal,
regulatory, employment, cultural-safety, organisational, deployment, public
release and marketplace validation remain outside repository completion unless
separately exercised by the applicable authority.
