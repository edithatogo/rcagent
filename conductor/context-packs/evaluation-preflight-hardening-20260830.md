# Context Pack: Evaluation preflight hardening

Base: 7ba8b1c5163d4d92743430d0514ee94ef763f378
Track: eval-blocker-remediation_20260803; root issue #1
Scope: legacy preflight scripts, shared receipt-envelope validator, generated
synthetic tests and this track's evidence. Read-only local execution; no raw
historical case processing, credentials, model acquisition or provider calls.

## Acceptance and boundary

Remove unsafe acceptance based on absence of negative words or a nonempty CSV.
Validate a versioned, stage-specific fixture envelope with pinned input digest,
artifact hashes, bounded local paths and strict field validation. Fixtures may
prove contract behaviour but can never unlock a study. Live study admission
remains disabled until the separately versioned protocol and semantic slot,
blinding and scoring-completion validators exist. Do not claim this envelope
alone proves provenance, blinding, review or clinical validity.

## Inputs, fit and gap

Use the existing three PowerShell entry points and Python tools package; add no
dependency or subsystem. Existing slot validation does not prove full cohort
admission. Reuse SHA-256 and JSON parsing from the standard library; receipt
structure is project-specific. Standing decisions 20260830-001 and -002 apply.
Historical execution dependencies remain blocked; this security repair does not
consume or alter their raw evidence. Fresh until preflight/protocol change.
Context budget: selected plan/spec/metadata, three wrappers and validator tests.

## Verification and handoff

Run focused tests, all three read-only preflights, lint/types, governance and
full_validation. Three-agent review checks false acceptance and scope claims.
Next: implement protocol-bound semantic admission before enabling study passes.
Rollback through a reviewed fix; reverting alone would restore the known
permissive gates and is not a safe operational fallback.
