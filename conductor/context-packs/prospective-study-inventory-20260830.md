# Context Pack: Prospective study inventory

Base: 5de27309df69f8f59eda3f1125bac8b1b81d7285; track:
eval-blocker-remediation_20260803; issue #1. Standing decision 20260830-002.

## Scope and fit

Own a new planning manifest under evaluation/prospective, a read-only Python
inventory adapter, synthetic tests and selected track records. Reuse existing
JSON, SHA-256 and bounded file helpers; no new dependency, runtime or provider.
The legacy protocol and observations are excluded. Existing preflights remain
locked. Context budget: selected track, decision, existing fixture validator,
agent rubric and these new files. No remote execution or sensitive inputs.

## Acceptance

Pin the manifest and input/rubric bytes, use a new study namespace and verify
the exact case-by-condition-by-repeat denominator. Enumerate expected slots
and unexpected submissions without following symlinks or leaking contents.
Distinguish missing submissions from invalid and structurally consistent but
unverified submissions. No receipt can produce admission: execution provenance
verification and study freeze are not implemented in this planning slice.

## Validation and handoff

Fixture-first tests, adversarial tests, full_validation and agent-panel review.
No fresh historical inventory or completed readiness fallback is claimed.
Next: assign an executable condition and capture/verify provenance, finalise
the study protocol and implement affirmative admission, then blinding/scoring.
Rollback only these new files; retain existing preflight locks. Fresh until
manifest/schema/provenance design changes; local branch owns the new files.
