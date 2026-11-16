# HEAPS bounded continuation context

## Goal and current authority

The user instructed: **Implement H4, open a PR, check actions pass, then merge.**
The instruction was received on 17 November 2026 (Australia/Brisbane). Implement
and independently review the deterministic synthetic consumer, reconcile and
publish the complete HEAPS prerequisite chain through PR #142, verify the actual
required hosted checks, then merge with the expected-head guard. This authority
supersedes the earlier merge reservation for this PR only. It does not authorise
release, clinical use, local instrument copying or another owner's work.

## Reconciled baseline and ownership

H2/H3 source is `8adcff03d7f33baf0110fbb198661b01db0754b0`. The H4 starting master
is `6f9cd9627adc52782a67fa6693f1cdb90c3c84a7`, including accepted D0/D1. A normal
merge reconciles those histories; no history rewrite is needed. Core validators,
canonical schema, shared interface, dependency lock and D0 implementation bytes
remain unchanged from the H3 inspection. H1's renderer/date-time findings still
apply to other callers. The H4 boundary must enforce canonical and strict-time
admission itself.

One integration lane owns this track and PR. Two disjoint lanes own production
`tools/heaps*.py` and independent `tests/test_heaps*.py` consumer checks; a separate
agent performs read-only contract/security review. Preserve the frozen H3
schemas, oracle and fixtures. Preserve D0/D1/D2/AcciMap/death-review ownership,
shared workbench dispatch, jurisdiction registry, CI, dependencies and zero
quality allowances. Portfolio numbering remains with the shared coordinator;
its absence is not a new permission gate for this explicitly authorised PR.

## H4 contract and limitations

Use [h3-contract.md](./h3-contract.md) and the immutable independent 38-variant
oracle. Production code must not branch on fixture IDs or manufacture expected
results. The consumer accepts prestructured, declared synthetic, fully local
records. It cannot prove synthetic provenance or de-identify clinical data.

- Resolve typed references in the bound canonical case and revision.
- Strictly parse JSON and all consumed timestamps; reject malformed input.
- Preserve raw ingress separately from normalised artifacts and bind exact bytes.
- Keep the detached manifest, decision and status construction acyclic.
- Derive counts and statuses from executed checks, never supplied positive labels.
- Preserve contrary accounts, alternative explanations, source families,
  participation concerns, separate clocks and unresolved questions.
- Keep preparation, source-check scope, template mapping, review, submission,
  implementation and effectiveness distinct.
- Leave D0 byte spans and AcciMap composition explicitly unimplemented; accepted
  upstream D0/D1 does not qualify their HEAPS composition.
- Current local form/taxonomy/roles/rights and actual authority remain unverified.

## Verification and next steps

Run focused consumer/contract checks and the locked strict repository gate.
Independently reproduce two clean CLI runs and inspect exact output hashes.
Preserve failed development observations and the local Unix-socket restriction;
hosted matrix results must be observed at the actual source head. The active
master ruleset requires dependency review and Linux/macOS/Windows validation;
the Ubuntu aggregate also requires the complete validation matrix, mutation,
profiling and combined coverage. Preserve privacy/secrets and conformance checks.
The separately configured offline AI security workflow currently awaits its
self-hosted runner and is not a completed scan or a required merge check.

Do not mark H5 or H6 complete merely because H4 implementation checks pass. H5
remains the independent qualification/handoff stage; H6 requires current
local instrument evidence and applicable operational authority. The observed publication, checks and merge are recorded in [H4 acceptance](./h4-acceptance-20261117.md).

## Current execution checkpoint

PR #142 is merged. Source `05975675467684f033e5d4df7320984a4c9eb3a1` and tree `5c55fde1cbe324973b71413f63367c773391d523` passed the
required hosted checks, complete Quality aggregation, Codecov, privacy/secrets
and conformance. Merge `006d98cb60c72143b0517f0e7a446641642ddd5a` has the same tree. [The acceptance receipt](./h4-acceptance-20261117.md)
records actual job identities, times, ruleset and expected-head merge evidence.
The separate offline security scan remains queued, not passed. Original failed
and later repaired local/hosted observations remain distinct.

H4's 304 tests, frozen 38-variant execution and identical 16-file replay are
development-visible engineering evidence. H5 qualification and handoff is next;
do not mark its tasks complete from this H4 receipt. H6 still needs current local
instrument evidence and applicable authority. Shared registration remains with
the coordinator, with no portfolio number assigned here.
