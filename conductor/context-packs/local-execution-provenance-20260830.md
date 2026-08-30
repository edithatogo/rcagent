# Context Pack: Local execution provenance probe

Base: eada61125e5f099d945a04a38219a59f3a26bc88; owning track:
eval-blocker-remediation_20260803; issue #1. Existing comparator admission and
decisions 20260829-002/20260830-002 bound this work.

## Scope and fit

Reuse the admitted llama-cli runtime and cached Qwen comparator artefacts.
Add a thin fixed-prompt capability probe and tests, without changing historical
results, prospective study inputs, existing preflights or scoring. No model
download, new provider, credential, paid compute or rights expansion.

The gap is retained execution evidence: current comparator results record
response hashes but not exact raw output and invocation timing. Capture a
small fresh non-study probe with pinned registry/runtime/model/adapter/prompt,
raw stdout, stderr digest/size, timestamps, exit state and timeout. This is
process observation, not a tamper-proof attestation or study admission.

## Acceptance and validation

Fail before execution for changed pins or unavailable admission. Fixed token,
seed, prompt and timeout settings; minimal environment, no shell or provider
arguments. Bound retained output; do not publish stderr bytes or local cache
paths. Report the runtime's local-file execution design, not an enforced
network sandbox. Failed/empty/oversized probes cannot imply readiness.

Fixture-first tests, full_validation and agent-panel review precede the live
probe. Inspect generated stdout before committing a synthetic-only receipt.
No primary study execution or protocol freeze; all admission gates stay locked.
Next: connect observed execution provenance to the separate frozen study
protocol. Rollback only new probe code/records, retaining historical evidence.
Context budget: selected track, standing decisions, comparator adapter/registry,
new probe and tests. Fresh until registry/runtime/model/prompt changes.
