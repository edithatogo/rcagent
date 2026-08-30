# Prospective planning inventory checkpoint

## Scope and evidence

Base: `5de2730`; branch: `codex/prospective-study-inventory`. This implements
only the new planning manifest and read-only inventory portion of decision
20260830-002. See the [study README](../../../evaluation/prospective/prospective-agent-text-20260830/README.md)
and [scoped receipt](../../../evaluation/prospective/prospective-agent-text-20260830/inventory-20260830.json).

Two generated synthetic inputs, one unassigned local-text candidate and one
planned repeat yield two expected slots. The observed directory inventory
found both pending, zero supplied/quarantined/unexpected and zero admitted.
No execution, scoring, blinding, historical audit or readiness-only closeout
is claimed. Hashes establish byte consistency, not truthful provenance.
The schema cannot represent a frozen protocol or an admitted executable
condition; those require the next implementation slice.

## Review and validation

The fixture-first test initially failed because the module did not exist.
The focused suite subsequently passed 51 tests, with 100% statement and
branch coverage of the new adapter. Tests cover denominator mismatch,
cross-study identities, fixture relabelling, pins, normalization, invalid
JSON, path escapes, symlinks, entry limits, inventory CLI and checked-in pins.

Agent reviewers `inventory_contract_review` and `inventory_security` reviewed
the new code, manifest/artifacts, context and plan, using the pinned base diff.
`inventory_tests` implemented and ran the adversarial tests. Model revisions
were not exposed. Security review reproduced float-valued repeat and trailing
newline identity defects; both were fixed and regression-tested. Reviewers
rechecked and found no remaining blocker for planning-only scope. Agent
agreement is not independent human agreement; correlated errors remain possible.
`uv run python -m tools.full_validation` passed on macOS/Python 3.14.5:
567 tests, 92.64% overall coverage, plus Ruff, ty, basedpyright, gremlins,
governance and deterministic benchmark checks. A schema-boundary typing error
was corrected before this final run. Hosted checks are separate evidence.

The implementation uses the repository's existing jsonschema dependency and
bounded JSON/file helpers. No new dependency, model, provider or client adapter
was installed. No private or third-party-controlled data was introduced.
Clinical, legal, policy, regulatory, employment, cultural-safety, organisational
and deployment authority remains external.

## Remaining work

Keep the historical inventory and parent semantic-admission tasks incomplete.
Assign an executable condition, verify captured execution provenance, finalise
and freeze the protocol, and implement affirmative admission before any
blinding, scoring or analysis. No repeated approval is needed for bounded
implementation. Roll back only the new planning artefacts and adapter if
necessary; retain the legacy fail-closed gates from PR #80.
