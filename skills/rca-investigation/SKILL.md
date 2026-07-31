---
name: rca-investigation
description: Conduct evidence-grounded systems analysis for an established healthcare safety investigation. Use only when asked to investigate a past incident or serious adverse event, build its evidence chronology, analyse contributing conditions and barriers, draft findings from completed analysis, or govern accepted review actions and effectiveness checks in an AU/NZ RCA or SAE workflow.
compatibility: Requires an Agent Skills client that can read bundled Markdown files.
metadata:
  rca-workbench-profile: portable-core
  rca-workbench-version: "0.1"
---

# Healthcare Incident Investigation

Assist an accountable human investigation team. Do not act as the investigator,
clinician, legal adviser, regulator, decision-maker, or system of record.

## Select the operating mode

Choose the first mode matching the user's current outcome:

1. **Triage** — scope a new review, assess immediate safeguards, or select
   methods. Read `references/workflows/triage.md`.
2. **Investigate** — organise evidence, build a chronology, or analyse system
   conditions. Read `references/workflows/investigate.md`.
3. **Report** — convert reviewed analysis into a report, briefing, or diagram.
   Read `references/workflows/report.md`.
4. **Track** — translate accepted recommendations into actions and verify
   effectiveness. Read `references/workflows/track.md`.

If the request spans modes, complete them in that order. Never infer that a
later mode's human approvals have occurred.

## Apply gates before analysis

1. Establish the jurisdiction, organisation, investigation authority, intended
   audience, and governing policy version. If unknown, label jurisdictional
   requirements unverified.
2. Ask for or derive the permitted data boundary. Default to placeholders such
   as `[Patient A]`, `[Staff member B]`, `[Ward X]`, and `[Case ID]`.
3. Separate source evidence, participant accounts, analysis, findings,
   decisions, and unresolved questions.
4. Record missing, conflicting, late, transformed, or unverified evidence.
   Never invent a fact to complete a chronology or template.
5. Identify immediate safety actions without treating them as proof of cause.
6. Reserve clinical, legal, regulatory, employment, disclosure, notification,
   severity, and final approval decisions for authorised humans.

Do not state that material is legally privileged merely because it concerns
quality improvement. Ask an authorised person to determine confidentiality,
records, disclosure, and privilege markings under applicable law and policy.

## Select methods

Read `references/method-selection-matrix.md` when choosing methods and
`references/method-combination-guide.md` when combining them. Treat any
severity examples as prompts rather than jurisdiction-independent rules.

Default sequence:

1. Build and source a timeline.
2. Identify work-as-done, expected work, changes, adaptations, and context.
3. Analyse contributing system conditions and barriers.
4. Test candidate findings against supporting and conflicting evidence.
5. Develop recommendations that address evidenced system conditions.
6. Define implementation, effectiveness, balancing, and residual-risk checks.

Load only the relevant method file under `references/methods/`. For complex
events, prefer a complementary set rather than forcing every method.

## Produce bounded outputs

Use the smallest suitable template under `assets/templates/`. Preserve
placeholders until an authorised local workflow replaces them. Clearly label:

- known facts and their sources;
- accounts and their provenance;
- analysis and alternative explanations;
- findings and confidence or uncertainty;
- decisions requiring human authority;
- actions, owners, dates, measures, and review points; and
- limitations, missing evidence, and residual risk.

When producing a DOCX or presentation, also apply the relevant guidance under
`assets/styles/`.

Read `references/just-culture-guide.md` only when authorised reviewers need a
behavioural decision aid. Do not convert it into an automated blame or
disciplinary determination. Read `references/safety-ii-principles.md` when
ordinary work, adaptations, or resilience are material.

## Validate before handoff

Read `references/investigation-quality-checklist.md`, then check:

- every material claim traces to evidence or is labelled as analysis;
- missing and conflicting evidence remains visible;
- language examines systems and does not imply individual blame;
- direct identifiers and unnecessary sensitive detail are absent;
- jurisdictional and policy claims are verified or qualified;
- recommendations connect to findings and favour stronger system controls;
- implementation is not confused with effectiveness;
- required human review and approval gates are explicit; and
- all referenced files and templates exist inside this skill directory.

Correct failures before presenting the output. If evidence is insufficient,
return a bounded gap list and safe next steps instead of a completed finding.

## Gotchas

- A report is not evidence that an investigation, action, or external
  notification was completed.
- A plausible causal story is not a finding without evidence and alternatives.
- Training and policy reminders are usually weak controls when used alone.
- Severity and notification rules vary by jurisdiction and policy revision.
- De-identification reduces risk but does not automatically make data safe.
- Never place client-specific tool permissions in this portable core.
