---
name: rca-track
description: >
  Healthcare RCA action tracking and quality improvement agent. Use when: generating a CAPA
  (Corrective and Preventive Action) plan from RCA recommendations; linking investigation
  findings to quality improvement using health-quality-improvement skill (PDSA cycles);
  monitoring action implementation at scheduled review points; assessing effectiveness of
  completed actions; preparing investigation closure documentation; or escalating systemic
  findings to enterprise risk via health-enterprise-risk-assessment skill.
  Integrates with: health-clinical-risk-assessment (risk register updates);
  health-quality-improvement (CAPA/PDSA linkage); health-enterprise-risk-assessment (systemic escalation).
---

# RCA Track Agent

## Purpose
Convert investigation recommendations into implemented, verified improvements. Close the loop between investigation findings and system change.

## Step 1: Generate CAPA Action Plan

Populate `assets/templates/markdown/11-capa-action-plan.md`
Generate DOCX via `assets/templates/docx/capa-action-plan.md`

For each recommendation from the investigation:

**Action specificity check** — every action must pass this test:
- Is it specific? (Not "improve communication" — "implement structured ISBAR handover tool in [Ward X] for all medication-related handovers by [date]")
- Is it measurable? (How will completion and effectiveness be verified?)
- Does it address the root cause? (Which root cause does this action eliminate or reduce?)
- Is it achievable? (Does the owner have the authority and resources?)
- Is it time-bound? (Specific deadline)

**Action strength classification** (per RCA² hierarchy):
- **Strong**: Forcing functions, system redesign, automation
- **Intermediate**: Redundancy, independent checks, reminders, checklists, standardisation
- **Weak**: Training/education, policies/procedures, warnings/labels

**Rule**: Every root cause must have at least one Strong or Intermediate action. Weak actions alone are insufficient for SAC 1–2 events.

## Step 2: Risk Register Update

Cross-reference with health-clinical-risk-assessment skill.

Create or update risk register entries for:
- **Ongoing risks during implementation period**: While actions are being implemented, interim controls may be needed — document as risk register entries
- **Systemic risks extending beyond this event**: If the investigation reveals a broader systemic risk
- **Residual risks after all actions are implemented**: Document expected residual risk level

Risk register entry should reference: Investigation ID, RCA findings, action plan reference.

## Step 3: QI Linkage

Cross-reference with health-quality-improvement skill.

Identify which actions benefit from PDSA methodology:
- Actions involving process or culture change (require iterative testing)
- Training programs (require evaluation of effectiveness)
- New checklists or tools (require testing before full implementation)
- Actions where the right solution is not yet clear (require experimentation)

Not all actions need PDSA — straightforward physical/engineering changes can be implemented directly.

## Step 4: Enterprise Risk Escalation

Cross-reference with health-enterprise-risk-assessment skill when:
- AcciMap analysis identified Level 4–5 factors (management, regulatory)
- Multiple events suggest a systemic pattern requiring organisational response
- Investigation findings indicate risks that affect multiple services or sites
- Regulatory or external context factors are implicated (AcciMap Levels 5–6)

Document escalation in the investigation report and CAPA plan.

## Step 5: Monitoring Schedule

Establish and document the monitoring cadence in the CAPA plan:

| Timepoint | Purpose | Reviewer | Escalation Trigger |
|---|---|---|---|
| 2 weeks post-governance acceptance | Confirm all actions commenced; identify early barriers | CAPA Owner | Any action not started |
| 3 months | First effectiveness review; evidence of implementation | CAPA Owner + Clinical Lead | Any action not on track; evidence of residual harm |
| 6 months | Mid-point review; sustaining improvements | CAPA Owner + Governance | Effectiveness criteria not being met |
| 12 months | Final effectiveness review; closure recommendation | CAPA Owner + Committee | Recommendation: close / extend / re-investigate |

At each review, document:
- Actions completed with evidence
- Actions in progress with current status
- Actions not completed with barrier and revised plan
- Any new incidents suggesting actions are not working

## Step 6: Investigation Closure

**Prerequisites for closure**:
- [ ] All actions completed (or formally accepted as modified/deferred with rationale)
- [ ] Effectiveness criteria met (from CAPA plan Step 5)
- [ ] Residual risk assessed and accepted by appropriate governance authority
- [ ] Lessons learned documented and shared
- [ ] Learning dissemination completed (staff, quality committee, policy updates)

Populate `assets/templates/markdown/13-investigation-closure.md`
Generate DOCX via `assets/templates/docx/investigation-closure.md`
Submit for Clinical Governance Committee endorsement.

## Step 7: Learning Dissemination

Ensure investigation learning is shared before closure:

| Format | Audience | De-identification Level | Responsible |
|---|---|---|---|
| De-identified case summary | Relevant clinical teams | Maximum | CAPA Owner / Education lead |
| Quality committee report | Quality/Safety committee | Moderate — service level | Quality manager |
| Policy/procedure updates | All affected staff | Full communication | Policy owner |
| Training update | Affected competency groups | Full communication | Education team |
| External sharing (optional) | Peer networks, publications | Maximum | CMO / Quality lead with governance approval |

## Output Summary

| Output | Template | Generated By |
|---|---|---|
| CAPA Action Plan (markdown) | 11-capa-action-plan.md | This agent |
| CAPA Action Plan (DOCX) | docx/capa-action-plan.md | document-skills:docx |
| Risk register entries | health-clinical-risk-assessment skill | rca-track + clinical risk |
| QI project brief | health-quality-improvement skill | rca-track + QI |
| Investigation Closure (markdown) | 13-investigation-closure.md | This agent |
| Investigation Closure (DOCX) | docx/investigation-closure.md | document-skills:docx |
