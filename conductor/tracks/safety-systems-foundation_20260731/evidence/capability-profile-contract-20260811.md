# Capability Profile Contract Receipt — 2026-08-11

## Scope

This slice makes the existing capability registry structurally and semantically
executable. It does not claim that the complete installation lifecycle or any
planned profile is implemented.

## Contract

- JSON Schema draft 2020-12 validates the closed registry and installation
  contract, profile enums, required fields, and planned-profile default rule.
- Repository validation enforces unique IDs, exactly one matching default,
  implemented core invariants, valid owner tracks, fail-closed installation
  safeguards, and implementation contracts for implemented optional profiles.
- Planned profiles remain declarations and cannot be selected as defaults.
- The `validate` profile's current support scope is explicitly limited to
  installation and repository validation.

## Verification

- `python tools/validate_repository.py`: passed.
- `uv run --no-project --with pytest --with jsonschema pytest tests/test_validate_repository.py -q`:
  15 passed.
- Negative fixtures cover duplicate IDs, invalid default state, unknown owner
  tracks, missing implementation contracts, telemetry-on defaults, and planned
  profile installability.

## Limitations and next work

The existing PowerShell setup script still needs a separate fail-closed
lifecycle refactor. Its current contract does not yet provide safe independent
preflight, ownership receipts, update/rollback, or uninstall. It must also fix
separator-aware path containment, check native exit codes, and disclose or
prevent network egress. Those omissions remain pending and no lifecycle
completion claim is made.
