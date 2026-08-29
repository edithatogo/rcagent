# Track 05 benchmark implementation context

- Purpose: implement the canonical synthetic benchmark contracts and deterministic baseline.
- Base revision: `ac8f283` plus Track 05 activation `2795da1`.
- Authoritative inputs: Track 05 specification and plan; archived Tracks 02 and 03 contracts; Track 04 jurisdiction registry and pending NSW decision.
- Included data: repository-owned synthetic fixtures and metadata-only legacy H0-H8 mappings.
- Excluded data: real/private incidents, restricted benchmark content, credentials, provider runs, clinical gold judgements, operational thresholds, and publication.
- Owned paths: `evaluation/benchmark/`, `tools/benchmark_harness.py`, `tests/test_benchmark_harness.py`, benchmark schema, Track 05 records, and Track 05 integration-map entry.
- Validation: benchmark validate/run/report, focused tests, repository governance, Ruff, ty/basedpyright, gremlin, and full pytest coverage.
- Rollback: revert focused Track 05 commits; no external data, model, service, or migration is created.
- Handoff: framework adapters and generative comparators remain unadmitted until exact execution and owner gates are available.
