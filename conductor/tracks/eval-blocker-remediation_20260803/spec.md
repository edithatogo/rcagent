# Specification: Evaluation Blocker Remediation and Admission

Establish a fail-closed path from incomplete Phase 4 evidence to canonical
admission, then unlock Track 5 scoring/IRR and Track 6 analysis only after the
required evidence receipts and review gates pass.

The track must preserve historical evidence, quarantine invalid material, and
make no assumption about operator, human-evaluator, credential, protocol, or
licence decisions.

Repository review duties now use the approved agent-panel protocol in
[decision 20260830-001](../../decisions/20260830-001-legacy-agent-review.md).
This does not replace H8 observations, historical operator attestations or
missing execution. Changes to study conditions and research-scoring methodology
remain pending [decision 20260830-002](../../decisions/20260830-002-prospective-agent-study.md).

Acceptance requires:

1. Every expected Phase 4 slot is admitted, explicitly excluded by an approved
   protocol decision, or quarantined with a reason and owner.
2. Every admitted row has raw evidence, normalized output, complete metadata,
   hashes, and an attestation or approved equivalent receipt.
3. Track 5 preflight passes before blinding, and Track 5 closure is reviewed
   before Track 6 preflight passes.
4. Agent Skills structural, portability, archive, fixture, drift, and privacy
   receipts are retained; no unsupported conformance claim is made.
