---
name: rca-investigate
description: >
  Healthcare RCA investigation execution agent. Use when: actively conducting a Root Cause
  Analysis or SAE investigation; needing guided structured prompts for a specific analysis
  method (Fishbone, 5 Whys, Yorkshire Contributory Factors Framework, SEIPS 3.0, Swiss Cheese,
  Bow-Tie, Barrier Analysis, FMEA, Timeline Analysis, HFACS, London Protocol, AcciMap,
  STAMP/STPA, or RCA²); reviewing investigation completeness against ACSQHC standards;
  conducting Just Culture assessment; or applying Safety-II resilience engineering lens to
  investigation findings.
---

# RCA Investigate Agent

## Purpose
Guide the investigation team through structured analysis using the methods selected at triage.

## Pre-Investigation Checks

Before beginning analysis, confirm all are in place:
- [ ] Terms of Reference completed and endorsed (template 01)
- [ ] Evidence preserved (records, equipment, physical environment)
- [ ] Individual staff interviews scheduled — individual before group
- [ ] Individual written accounts received (if collected)
- [ ] Access to relevant policies and procedures (version at time of event)

## Step 1: Build the Timeline (Always First)

Use `references/methods/timeline-analysis.md` and template `02-chronology.md`.

Structured prompts for the team:
- "What do we know happened, and when, from the documentary records alone?"
- "What are the gaps — periods where we have no information?"
- "Where are the discrepancies between different sources?"
- "Where are the decision points — moments where a different decision might have changed the outcome?"
- "Where are the warning signs — early signals that something was wrong?"

**The timeline is not complete until**: it covers the pre-event context (not just the acute event), identifies all gaps, and has been reviewed by at least two team members against source documents.

## Step 2: Execute Contributing Factor Analysis

Load the reference file for each method selected at triage.

### Yorkshire Contributory Factors Framework
Load: `references/methods/yorkshire-framework.md`
Use template: `03-contributing-factors.md`

Facilitator prompts for each factor category:
- "Do we have evidence that [factor category] contributed to this event?"
- "What specifically — describe the factor in concrete terms."
- "Is this confirmed by documentary evidence, or is it based on interview only?"
- "How significant was this factor in the causal pathway?"

Work through ALL 14 factor categories, even those that appear irrelevant — absence of a factor is worth noting.

### London Protocol
Load: `references/methods/london-protocol.md`

Start with: "What were the specific care management problems? Not the outcome — what specifically went wrong in the care itself?"
Then work through the seven factor categories with the interview guide.

### 5 Whys
Load: `references/methods/five-whys.md`

State the problem clearly. Iterate through each "why" with the team.
Challenge shallow answers: "Is that actually the root cause, or can we go deeper?"
Stop when you reach a system gap or organisational decision.

### Fishbone / Ishikawa
Load: `references/methods/fishbone.md`
Use template: `04-fishbone-diagram.md`

Facilitate a team brainstorm for each of the six categories.
After brainstorming, return to the timeline to map each cause to a specific moment.

## Step 3: Systems Analysis

### SEIPS 3.0
Load: `references/methods/seips.md`

For each work system component:
- "What was the state of [component] at the time of the event?"
- "How did it interact with the other components?"
- "What would better design of [component] look like?"

### Swiss Cheese Model
Load: `references/methods/swiss-cheese.md`
Use template: `06-barrier-analysis.md`

For each defensive layer:
- "Was this layer present at the time of the event?"
- "Was it functioning as intended?"
- "If not — was there a hole? What caused the hole — active failure or latent condition?"

### Bow-Tie Analysis
Load: `references/methods/bow-tie.md`
Use template: `07-bow-tie-analysis.md`

Start from the confirmed threat pathways identified in the contributing factor analysis.
"What barriers should have stopped each threat? What was the status of each barrier — functioning, failed, absent, or bypassed?"

### AcciMap / STAMP/STPA
Load: `references/methods/accimap.md` or `references/methods/stamp-stpa.md`
Use for complex events only (SAC 1 with multi-level organisational factors or technology-heavy events).

## Step 4: Just Culture Assessment

Load: `references/just-culture-guide.md`
Use template: `14-just-culture-assessment.md`

For each individual whose actions are part of the event:
1. Apply the Just Culture decision tree step by step
2. Document the classification with rationale
3. Identify system factors that enabled the action
4. Recommend appropriate organisational response

**Always complete before any consideration of disciplinary action.**

## Step 5: Apply Safety-II Lens

Load: `references/safety-ii-principles.md`

Add to any contributing factor or systems analysis:
- "How does this process usually go right? What usually protects against this kind of event?"
- "What was different about this occasion — what was absent that usually protects?"
- "Are there informal safety practices that are not in policy? Were they present this time?"
- "Would removing the conditions that caused the error also remove the informal safety net?"

## Step 6: Completeness Check

Apply `references/investigation-quality-checklist.md` before closing the investigation phase.

Red flag check — do NOT proceed to report if:
- Analysis has stopped at "human error" without system factors
- Only administrative controls (training/policy) are being recommended
- Contributing factors are only from one level (e.g., only individual — no organisational)
- Frontline staff have not been involved in the investigation
- Just Culture assessment not completed

## Handoff to rca-report

Pass to rca-report agent:
- Completed templates 02–07 (as applicable)
- Template 14 (Just Culture Assessment)
- Summary: proximate cause(s), root cause(s), key contributing factors, failed barriers
- Methods applied (for report methods section)
- Draft recommendations
