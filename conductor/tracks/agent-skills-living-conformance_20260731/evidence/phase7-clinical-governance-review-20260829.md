# Phase 7 Clinical-Governance Review — 2026-08-29

Fresh-context clinical-governance review of the Phase 7 triggering and
output-quality evidence, assessed against
`conductor/clinical-governance-architecture.md` principles (human
accountability, evidence primacy, jurisdiction visibility, privacy-first
de-identification).

## Evidence reviewed

- Trigger held-out partition: `runs/codex-0.145.0-20260731-v4-heldout/summary.json`
- Regression negatives: `runs/codex-0.145.0-20260731-v4-regression/summary.json`
- Positive training control: `runs/codex-0.145.0-20260731-v4-positive-training/summary.json`
- Output-quality composite: `output-quality-result.md` (v2–v5 assertion results)
- Immutable failed-run history: `runs/codex-0.145.0-20260731{,-v2,-v3}/`

## Findings

1. **Activation boundary.** Held-out negative cases for adjacent clinical,
   liability, employment, and policy-summary requests record 0.0 activation
   (3 trials each); positive systems and closure cases record 1.0. The skill
   therefore does not conduct investigations outside its declared trigger —
   the correct clinical-governance posture for an unauthorised actor.
2. **Human-authority gates in output assertions.** The composite suite
   includes human-review and jurisdictional-uncertainty assertions, and all
   applicable hard assertions pass; outputs must defer severity, disclosure,
   and approval decisions to authorised humans.
3. **Privacy and de-identification.** The de-identification assertion passes
   in the current composite; placeholder schemes remain mandatory in the
   skill body (reconfirmed in the Phase 4 editorial review).
4. **Evidence integrity.** Failed v1–v3 runs remain preserved and are not
   reclassified; the v2 adapter-boundary failure was corrected in v4 and both
   generations stay visible. No regression is hidden by the composite gate.
5. **Monitored residual risk.** The adapter boundary required one correction
   cycle (v2 fail → v4 pass). This is recorded as a standing watch item for
   Phase 8 living-conformance monitoring rather than a defect.

## Governance status

This review records project clinical-governance *conformance* evidence. It
does not assert organisational approval, clinical sign-off, or privilege
determination — those remain reserved to authorised humans per Track 00
metadata `decision_gates` and the skill's own body text. No owner-authority
claim is made or discharged by this receipt.

No clinical-governance defects found; one standing watch item recorded.
