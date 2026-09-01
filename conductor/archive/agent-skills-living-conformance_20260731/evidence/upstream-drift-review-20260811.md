# Agent Skills Normative Drift Review

Date: 2026-08-11

## Revisions

- Previous reviewed baseline: `38a2ff82958afee88dadf4831509e6f7e9d8ef4e`
- Reviewed upstream revision: `69ef37e9424c0a7ea9dd2293b559e43ec8176379`

## Normative change

The upstream comparison changed `docs/specification.mdx` in two places:

1. The optional `metadata` field is explicitly a map from string keys to
   string values.
2. A skill may contain files and directories beyond `SKILL.md`; `scripts/`,
   `references/`, and `assets/` are recommended organisational conventions.

No `skills-ref` source or dependency file changed between these revisions.

## Compatibility assessment

- `skills/rca-investigation/SKILL.md` uses string metadata keys and values.
- The package does not treat the conventional optional directories as an
  exclusive allow-list.
- The compliance matrix already states and tests the string metadata rule.
- No portable-package or adapter change is required.

## Decision

Advance the reviewed baseline and CI pin to
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`. Retain earlier dated receipts as
historical evidence of the prior baseline.
