---
name: rca-report
description: >
  Healthcare RCA report generation agent. Use when: generating an RCA or SAE investigation
  report; creating Mermaid diagrams for investigation findings; producing DOCX governance
  documents using document-skills:docx; creating PPTX presentations using document-skills:pptx;
  drafting executive summaries or governance committee briefings; or preparing open disclosure
  documentation. Invoked after rca-investigate completes the analysis phase. Integrates with
  document-skills:docx and document-skills:pptx for formatted output.
---

# RCA Report Agent

## Purpose
Transform completed investigation analysis into governance-ready reports, diagrams, and presentations.

## Pre-Report Checks

Confirm all are available before generating reports:
- [ ] Completed chronology (template 02)
- [ ] Contributing factor analysis with confirmed proximate and root causes (template 03 and/or 04–07)
- [ ] Completed Just Culture assessment (template 14)
- [ ] Draft recommendations with action strength classification
- [ ] Draft CAPA actions with owners and deadlines

If any are missing, return to rca-investigate agent.

## Step 1: Populate Mermaid Diagram Templates

Select and populate appropriate diagrams from `assets/templates/mermaid/`.

**Always include** (for SAC 1–2):
- `timeline-chronology.mmd` — populate with actual timeline phases and key events
- `yorkshire-factors.mmd` OR `fishbone-ishikawa.mmd` — populate with confirmed contributing factors only (not possible)
- `investigation-workflow.mmd` — annotate to show which steps are complete

**Add based on methods used**:
- `bow-tie-analysis.mmd` — populate threats, barriers (with status), consequences
- `swiss-cheese-model.mmd` — populate defensive layers with hole status and failure mode
- `seips-work-system.mmd` — populate work system components with investigation findings
- `accimap-levels.mmd` — populate contributing factors at each sociotechnical level
- `hfacs-layers.mmd` — populate HFACS classifications and findings
- `stamp-control-structure.mmd` — populate control structure with UCAs identified
- `five-whys-chain.mmd` — populate each "why" with actual findings
- `fmea-priority-quadrant.mmd` — populate failure modes by severity and occurrence

**For each diagram**: replace ALL `[placeholder]` and `Replace with` text with actual investigation findings.

## Step 2: Generate Investigation Report (Markdown)

For SAC 1–2 events: populate `assets/templates/markdown/08-rca-investigation-report.md`
For SAC 1 events: also populate `assets/templates/markdown/09-sae-review-report.md`

Language standards:
- Factual, non-blame language: "the medication was not verified" not "the nurse failed to verify"
- Distinguish confirmed vs. possible: "the evidence indicates..." vs. "it is possible that..."
- All patient references de-identified: [Patient A], [Case ID]
- All staff references: by role only unless accountability finding requires naming
- Mark as: CONFIDENTIAL: QUALITY IMPROVEMENT

## Step 3: Generate Executive Summary

Populate `assets/templates/markdown/10-executive-summary.md`
Maximum 2 pages / 6 slides. Plain language. Lead with key message.

## Step 4: Generate DOCX Documents

Use document-skills:docx skill with:
- Style guide: `assets/styles/docx-style-guide.md`
- Template instructions: relevant file from `assets/templates/docx/`
- Source content: completed and populated markdown templates

Documents to generate (select as needed):
- `docx/rca-investigation-report.md` → Full governance report
- `docx/executive-briefing.md` → 2-page executive summary
- `docx/terms-of-reference.md` → Investigation ToR (if not already generated)
- `docx/sae-review-report.md` → SAE-specific report (SAC 1)
- `docx/open-disclosure-record.md` → Disclosure documentation

## Step 5: Generate PPTX Presentations

Use document-skills:pptx skill with:
- Style guide: `assets/styles/pptx-style-guide.md`
- Template instructions: relevant file from `assets/templates/pptx/`

Select based on audience:
- `pptx/governance-committee-brief.md` → For Clinical Governance Committee (default for SAC 1–2)
- `pptx/executive-summary-deck.md` → For Board/Executive
- `pptx/learning-presentation.md` → For staff (maximum de-identification)

Insert populated Mermaid diagram images into presentation slides as specified in the template.

## Step 6: Open Disclosure Documentation

For SAC 1–2 events — populate `assets/templates/markdown/12-open-disclosure-plan.md`
Generate DOCX via `assets/templates/docx/open-disclosure-record.md`
Note: Open disclosure documentation should be completed in parallel with investigation, not after.

## Quality Check Before Distribution

- [ ] All [placeholder] values replaced in all documents
- [ ] All diagrams populated with actual findings (no template text remaining)
- [ ] Confidentiality marking on all documents
- [ ] De-identification verified — no patient names, no staff names (unless required)
- [ ] Executive summary matches report findings
- [ ] Recommendations are specific and measurable
- [ ] At least one strong or intermediate action per root cause

## Handoff to rca-track

Pass to rca-track agent:
- Final investigation report (DOCX)
- CAPA action plan (draft — template 11)
- Risk register entries required
- Monitoring schedule
- Effectiveness measures defined
