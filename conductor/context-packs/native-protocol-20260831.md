# Context Pack: Native protocol candidate declaration

Track `eval-blocker-remediation_20260803`, issue #1. Activated on
`codex/prospective-native-protocol` at parent PR #96 head `427ce4d` while its
hosted checks run. Reconcile the merged parent before successor delivery.
No model or study execution is scoped.

## Purpose and bounded inputs

Introduce a separately versioned native protocol candidate. Read the selected
specification, plan, metadata, continuation cursor, workflow and guidelines,
then `prospective_protocol.py`, `prospective_inventory.py`,
`prospective_runner_contract.py`, `prospective_freeze.py` and matching tests.
Limit context to these contracts and their directly referenced validators.
Reuse existing reference, identity, generation, scoring and two-slot denominator
checks. Do not duplicate them, rewrite temporary protocol files, mutate a global
schema or widen the legacy normalization enum in place.

## Ownership and acceptance

Main owns integration and records. `runtime_profile_tests` owns implementation
and fixtures; `root_acceptance_map` owns read-only acceptance review. Owned paths are new
`tools/prospective_native_protocol.py`, matching tests, a narrow shared-validation
extraction in `prospective_protocol.py`, legacy compatibility tests and these
linked records. Confirm the final file scope during activation.

Extract one shared candidate validator returning the legacy result, parsed
declaration and validated reference bytes. Native construction uses those retained
bytes, with no second reads. The legacy module must not import the runner.
The native schema is separately copied/versioned; no global schema mutation.

Require a distinct protocol version, exact `llama-native-json-v1` normalization
and an explicit runner-contract version. Validate prompt construction through
the pure contract using pinned reference bytes. Retain false execution/admission
flags. Legacy validation must reject native declarations, and native validation
must reject legacy modes. Exercise duplicate slots/paths, altered references,
malformed markers and generation mismatches. Preserve legacy API and behavior.

Leave `prospective_freeze.py` unchanged: its component closure is incomplete for
the native path and must not implicitly accept it. Historical source-pin receipts
remain immutable snapshots. Do not refresh installed server-profile static pins
unnecessarily. Later full-component freeze must explicitly include the native
validator and runner contract, plus the actual execution dependency closure.

## Boundaries, validation and handoff

Standing synthetic implementation and agent-panel review authority applies;
no new approval is required. This is not model execution, response provenance,
privacy validation, protocol freeze, scoring or study admission. Preserve the
prior negative READY finding without rerunning or tuning it. No private data,
credentials, acquisition, historical evidence alteration or authority attestation.

Use fixture-first tests, focused coverage, native/Windows type checks, full
repository validation and agent-panel review. Record failures and fixes, deliver
only a green exact head and verify merge tree parity. Roll back only this native
candidate integration; retain legacy contracts and historical evidence. Next
gates remain the actual runner, transitive freeze and admission-before-blinding.
