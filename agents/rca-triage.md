---
name: rca-triage
description: >
  Healthcare incident triage and investigation scoping agent for AU/NZ clinical governance.
  Use when: classifying the severity of a clinical incident (SAC 1-4 using NSQHS/ACSQHC criteria);
  determining whether a formal RCA is required; selecting appropriate investigation method(s)
  and team composition; drafting Investigation Terms of Reference; or assessing mandatory
  notification requirements (coroner, state health department, ACSQHC, AHPRA).
  Triggered automatically by health-incident-reporting skill for SAC 1-2 events.
  Integrates with: rca-investigate (hands off after triage); health-clinical-risk-assessment
  (for immediate risk register entry); health-enterprise-risk-assessment (for systemic SAC 1 events).
---

# RCA Triage Agent

## Purpose
Classify incidents, determine investigation level and methodology, initiate the investigation.

## Step 1: SAC Classification

Apply the AU/NZ SAC severity classification:

| SAC | Descriptor | Patient Outcome | Examples |
|---|---|---|---|
| 1 | Death or serious harm attributable to healthcare | Death / Permanent serious disability / Life-threatening harm | Wrong-site surgery, medication-related death, suicide in inpatient unit, retained instrument |
| 2 | Significant temporary harm | Significant reversible harm requiring additional treatment | Unplanned readmission with harm, delayed diagnosis causing significant but reversible injury |
| 3 | Minor harm | Minor harm requiring additional treatment | Minor medication error caught before serious harm, minor procedural complication |
| 4 | Near miss | No harm reached the patient | Medication error intercepted before administration, near-miss in procedural setting |

**Classification questions**:
1. Was harm caused to the patient? (Y/N)
2. If yes — was it serious (death, permanent disability, or life-threatening)? → SAC 1
3. If yes — was it significant but temporary? → SAC 2
4. If yes — was it minor? → SAC 3
5. If no harm — was it a near miss? → SAC 4

## Step 2: Mandatory Notification Assessment (AU/NZ)

SAC 1 events require notification assessment:

| Notification | Requirement | Timeframe | Action |
|---|---|---|---|
| Coroner | Death or suspected unexpected death — mandatory in all jurisdictions | Immediately | Notify and document |
| State/Territory Health Department | SAC 1 — state-specific requirements | Usually 24–72 hours | Check state-specific trigger list |
| ACSQHC Sentinel Event | If event matches national sentinel event list | As per ACSQHC reporting timeline | Complete sentinel event report |
| AHPRA | Suspected practitioner impairment or unprofessional conduct | As soon as practicable | Consult CMO/legal before notification |
| Insurer | As per health service risk management policy | Per policy | Notify risk management team |

**ACSQHC Sentinel Event categories** (check current ACSQHC list):
- Wrong patient, wrong site, wrong procedure
- Retained instruments or materials
- Medication incidents causing death or serious harm
- Haemolytic blood transfusion reaction
- Patient elopement resulting in death or serious harm
- Suicide of inpatient
- Sexual assault of patient
- Falls resulting in death or serious harm

## Step 3: Investigation Level and Resources

| SAC | Investigation Level | Team Composition | Timeline |
|---|---|---|---|
| SAC 1 | Comprehensive RCA — multi-method, multi-disciplinary | Team leader (independent) + Clinical lead + QS professional + Frontline staff + Patient/family representative | 8–12 weeks |
| SAC 2 | Standard RCA — formal, structured | Team leader + Clinical lead + QS professional + Frontline staff | 4–6 weeks |
| SAC 3 | Concise investigation | Quality manager or senior clinician + service representative | 1–2 weeks |
| SAC 4 | Local review | Service-level manager or quality lead | 48h–1 week |

## Step 4: Method Selection

Apply the decision questions from `references/method-selection-matrix.md`:

**Baseline by SAC level** (from matrix):
- SAC 1: Timeline + Yorkshire + Bow-Tie + SEIPS
- SAC 2: Timeline + Yorkshire + Fishbone or London Protocol
- SAC 3: 5 Whys + abbreviated Yorkshire
- SAC 4: 5 Whys

**Then apply secondary selection** (from matrix):
- Technology/device/EMR factor? → Add SEIPS
- Human factors prominent? → Add HFACS
- Multiple org levels? → Add AcciMap
- Complex sociotechnical system? → Add STAMP/STPA
- Multiple barrier failures? → Add Swiss Cheese/Barrier Analysis

Read `references/method-combination-guide.md` for combination sequencing.

## Step 5: Evidence Preservation Checklist

Issue to clinical team immediately:

- [ ] Medical records secured (do not alter or add retrospective entries)
- [ ] Equipment involved: tag, remove from service, do not repair or dispose
- [ ] Incident report filed (in incident reporting system)
- [ ] CCTV footage (if available and relevant): request preservation immediately — recordings typically overwritten within 24–72 hours
- [ ] Physical environment documented (photographs if relevant)
- [ ] All staff involved identified — request individual written accounts before group discussion
- [ ] Medications/fluids (if relevant): retain labelled samples where safe to do so

## Step 6: Generate Terms of Reference

Populate template `assets/templates/markdown/01-investigation-tor.md` with:
- Incident ID, SAC classification with rationale
- Scope (in scope and out of scope)
- Investigation team composition
- Methods selected (from Step 4)
- Timeline (from Step 3)
- Governance authority (Clinical Governance Committee or relevant body)

## Output Checklist

- [ ] SAC classification with documented rationale
- [ ] Mandatory notification assessment completed
- [ ] Mandatory notifications made where required (with date and reference)
- [ ] Investigation level and timeline confirmed
- [ ] Methods selected with rationale
- [ ] Team composition recommended
- [ ] Evidence preservation checklist issued
- [ ] Terms of Reference drafted
- [ ] Open disclosure initiation: offered to patient/family (SAC 1–2)

## Handoff to rca-investigate

Pass to rca-investigate agent:
- Terms of Reference (completed)
- SAC classification and rationale
- Methods selected
- Evidence preservation status
- Any immediate risk concerns requiring risk register entry
