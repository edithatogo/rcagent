# Track 04 Jurisdiction Implementation Context

## Purpose and base

- Purpose: reproduce and review the national, NSW and Queensland jurisdiction profiles.
- Base revision: `d61dbc9cd002effdba4555988ee62248bc4725ff`
- Privacy mode: public remote for official-source verification; synthetic local fixtures for tests.
- Freshness: source retrieval `2026-08-29T00:54:13Z`.

## Authoritative inputs

- Track 04 specification, plan and metadata.
- `conductor/jurisdictions/registry.json` and its JSON Schema.
- Archived Track 02 evidence/workflow and Track 03 privacy/assurance contracts.
- Issuing-body URLs, versions and checksums recorded in the Track 04 fit-gap receipt.

## Owned files

- `conductor/jurisdictions/`
- `conductor/schemas/jurisdiction-pack.schema.json`
- `tools/jurisdiction_pack.py`
- `tests/test_jurisdiction_pack.py`
- Track 04 Conductor records and capability/integration registrations.

## Exclusions and assumptions

- No real or private data, credentials, enterprise connector or external write-back.
- No copied external template, local procedure, legal advice, privilege claim or organisational approval.
- Current official publication state is evidence, not a guarantee that every local organisation has implemented the source.

## Commands and acceptance

```bash
uv run python -m tools.jurisdiction_pack validate
uv run python -m pytest tests/test_jurisdiction_pack.py -q
uv run python -m ruff check tools tests
uv run python -m ty check tools tests
uv run python -m basedpyright
uv run python -m tools.check_gremlins .
uv run python -m tools.validate_repository
uv run python -m pytest --cov=tools --cov-report=term-missing
```

Acceptance requires schema and semantic validity, valid canonical transitions, no rule driven by draft/consultation/superseded/unavailable authority, state-pack inheritance, visible safeguards, review-required material drift and a clean full gate.

## Handoff and rollback

The implementation is a data-only optional profile. Roll back the functional commit to remove it without changing the generic evidence core. Retain prior registry snapshots when reviewing drift; never overwrite current behaviour from an unreviewed candidate.
