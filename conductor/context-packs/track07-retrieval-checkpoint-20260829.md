# Track 07 retrieval checkpoint

- Purpose: complete deterministic, synthetic-only retrieval contracts and
  record unsupported optional profiles honestly.
- Base: `b3537144e32be4c9741b04afa531615b85ec1ec9`.
- Authoritative inputs: Track 07 specification and plan; archived Tracks
  02–06; product guidelines; integration map; SourceRight adapter contract.
- Data boundary: generated synthetic public fixtures only. No private
  clinical, employee, incident or organisation data.
- Exclusions: external providers, model downloads, vector databases, remote
  embeddings, cross-compartment queries, clinical interpretation and
  operational promotion.
- Owned paths: retrieval schema, fixtures, evaluator, tests, Track 07 records
  and its integration-map entry.
- Commands: `uv run pytest -q tests/test_retrieval_system.py`, Ruff, ty,
  basedpyright, repository validation and the full test suite.
- Rollback: disable optional profiles, discard derived SQLite databases and
  rebuild from the validated manifest.
