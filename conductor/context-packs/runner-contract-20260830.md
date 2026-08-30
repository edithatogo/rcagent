# Context Pack: Fixture-only prospective runner contract

Track `eval-blocker-remediation_20260803`, issue #1. Base `5b194a8` (PR #95),
tree `e5996b18b35d7e279d7f4872971cdc1248d6c61c` equals reviewed head `4973f9b`.
Branch `codex/prospective-runner-contract`; no lease enabled. This context is
activated for fixture-only implementation. No further model run is scoped.

## Smallest remaining gap and reuse

The fixed server session and one actual structured observation are complete.
Preserve the 32-byte non-READY finding and all raw local evidence. Acceptance
agent recommends a pure deterministic contract before any execution runner:
exact prompt/request construction, byte-preserving normalization and slot-keyed
candidate records. Main concurs; no new owner approval is needed for fixtures.

Read the selected spec/plan/metadata, workflow/guidelines, continuation cursor,
structured observation and `prospective_protocol`, `prospective_freeze` and
`native_completion` contracts. Do not import unrelated historical outputs or
private material. Reuse `GENERATION` values and the existing strict native
decoder. Later integration must reuse protocol denominator/reference checks;
do not duplicate or weaken those validators here.

## Owned paths and acceptance

Own only new `tools/prospective_runner_contract.py`, its matching tests and
linked Conductor records. Main integrates and owns records; assign bounded
implementation and independent acceptance/privacy roles before starting.
Assigned: `runtime_profile_tests` owns both new files, `root_acceptance_map`
owns read-only acceptance/privacy review, main owns integration, safety and records.

API boundary agreed by the panel: pure `build_request(template, input_bytes)`
and `normalize_candidate(request, raw_body, slot_id, expected_slot_id,
expected_model)` only. Do not read or claim compatibility with a legacy protocol.
Literal slot equality is caller-label consistency, not denominator membership
or input provenance. Reconstruct the full canonical request package from retained
template/input bytes, checking its exact fields, types, hashes and bytes before
normalizing. Leave protocol compatibility, denominator/slot provenance, request/
response binding, model identity and execution unverified.

Construct prompts from exact valid UTF-8 template/input bytes using one fixed
`{{INPUT}}` insertion marker. Reject absent/duplicate markers; preserve whitespace, Unicode
and input markers literally, without trimming or recursive substitution.
Construct canonical non-stream native request bytes using existing fixed
generation values. Retain template, input, prompt and request hashes.

Normalize solely through `native_completion.decode_completion`, preserving
decoded content bytes and every incomplete-generation/settings rejection.
Bind exact slot identity into candidate records and reject slot mismatches.
Every execution/admission/study flag stays false: consistent fixtures are not
observed primary evidence. Test deterministic bytes/hashes, malformed inputs,
byte preservation, marker handling, slot mismatch and decoder failures.

No subprocess, transport call, model run, arbitrary callback, provider access,
download, credentials, protocol freeze, scoring or admission in this slice.
The fixed READY session remains unchanged. Do not tune prompt text or filter
outputs to turn the prior READY mismatch into a pass.

## Separate later integration gates

The current protocol enum does not yet enable `llama-native-json-v1`. Introduce
its versioned declaration separately before execution integration. A complete
freeze must bind the actual server session/profile/model helper, process,
transport, decoder, prospective model helper and new runner contract, plus
registry, protocol artefacts and transitive dependency identities. Existing
disk-source hashes are not loaded-code attestation or study admission.

## Validation and handoff

Use fixture-first tests, meaningful adversarial coverage, Ruff, native/Windows
types, full validation and agent-panel review. Keep hosted patch coverage above
the existing gate without weakening it. Record exact failures and bounded fixes.
Deliver the reviewed green exact head, verify tree parity and save the cursor.
Rollback only this new contract and records; preserve parent code and evidence.
