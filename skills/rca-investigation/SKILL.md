---
name: rca-investigation
description: >
  Healthcare Root Cause Analysis (RCA) and Serious Adverse Event (SAE) investigation skill for
  AU/NZ clinical governance. Use when: conducting an RCA or SAE review; classifying incident
  severity (SAC 1-4) and selecting investigation methods; executing structured analysis using
  Fishbone, 5 Whys, Yorkshire Framework, SEIPS, Swiss Cheese, Bow-Tie, Barrier Analysis, FMEA,
  Timeline, HFACS, London Protocol, AcciMap, STAMP/STPA, or RCA²; generating investigation
  reports, DOCX governance documents, PPTX presentations, or Mermaid diagrams; creating CAPA
  action plans; assessing Just Culture; or linking RCA findings to quality improvement.
  Integrates with health-incident-reporting, health-clinical-risk-assessment,
  health-quality-improvement, and health-enterprise-risk-assessment skills.
---

# RCA & SAE Investigation

## Operating Modes

| Mode | When | Agent |
|---|---|---|
| **Triage** | New incident — classify, prioritize, select methods | `agents/rca-triage.md` |
| **Investigate** | Active investigation — execute analysis method(s) | `agents/rca-investigate.md` |
| **Report** | Analysis complete — generate reports, diagrams, documents | `agents/rca-report.md` |
| **Track** | Report accepted — CAPA, QI linkage, effectiveness review | `agents/rca-track.md` |

## Quick Method Selection

Read `references/method-selection-matrix.md` for the full decision framework.

**By SAC level:**
- SAC 1 (catastrophic): Timeline + Yorkshire + Bow-Tie + SEIPS
- SAC 2 (major): Timeline + Yorkshire + Fishbone or London Protocol
- SAC 3 (moderate): 5 Whys + Contributing Factors
- SAC 4 (minor/near miss): 5 Whys
- Proactive: FMEA + Bow-Tie

## Methods Reference Index

| Method | File | Best For |
|---|---|---|
| RCA² | `references/methods/rca-squared.md` | Enhanced RCA with action focus |
| 5 Whys | `references/methods/five-whys.md` | Simple, rapid cause drilling |
| Fishbone/Ishikawa | `references/methods/fishbone.md` | Structured cause-effect categorization |
| Yorkshire Framework | `references/methods/yorkshire-framework.md` | Comprehensive contributing factors (SOTA) |
| SEIPS 3.0 | `references/methods/seips.md` | Work system model |
| Swiss Cheese | `references/methods/swiss-cheese.md` | Defence-in-depth failure analysis |
| Bow-Tie | `references/methods/bow-tie.md` | Threat-barrier-consequence mapping |
| Barrier Analysis | `references/methods/barrier-analysis.md` | Failed/missing barrier identification |
| FMEA | `references/methods/fmea.md` | Proactive failure mode analysis |
| Timeline Analysis | `references/methods/timeline-analysis.md` | Event sequencing, gap identification |
| HFACS | `references/methods/hfacs.md` | Human factors classification |
| London Protocol | `references/methods/london-protocol.md` | Systematic clinical investigation |
| AcciMap | `references/methods/accimap.md` | Multi-level systemic accident mapping |
| STAMP/STPA | `references/methods/stamp-stpa.md` | Systems-theoretic accident model |

## Template Index

### Mermaid Diagrams (`assets/templates/mermaid/`)
- `fishbone-ishikawa.mmd` — Cause-effect mindmap
- `swiss-cheese-model.mmd` — Defence layers
- `bow-tie-analysis.mmd` — Threat-barrier-consequence
- `timeline-chronology.mmd` — Event sequence
- `five-whys-chain.mmd` — Causal chain
- `seips-work-system.mmd` — Work system model
- `yorkshire-factors.mmd` — Contributing factor map
- `accimap-levels.mmd` — Multi-level systemic map
- `hfacs-layers.mmd` — Human factors pyramid
- `stamp-control-structure.mmd` — Control structure
- `investigation-workflow.mmd` — Investigation process
- `fmea-priority-quadrant.mmd` — Severity vs likelihood

### Working Document Templates (`assets/templates/markdown/`)
01 Investigation Terms of Reference | 02 Chronology | 03 Contributing Factors |
04 Fishbone Diagram | 05 FMEA Worksheet | 06 Barrier Analysis |
07 Bow-Tie Analysis | 08 RCA Investigation Report | 09 SAE Review Report |
10 Executive Summary | 11 CAPA Action Plan | 12 Open Disclosure Plan |
13 Investigation Closure | 14 Just Culture Assessment

### DOCX Templates (`assets/templates/docx/`)
RCA Investigation Report | SAE Review Report | Executive Briefing |
Terms of Reference | CAPA Action Plan | Open Disclosure Record | Investigation Closure

### PPTX Templates (`assets/templates/pptx/`)
Governance Committee Brief | Learning Presentation | Executive Summary Deck

## Key References

- `references/method-selection-matrix.md` — Which method(s) for which event
- `references/method-combination-guide.md` — How to combine methods
- `references/just-culture-guide.md` — Human error vs at-risk vs reckless
- `references/safety-ii-principles.md` — Resilience engineering lens
- `references/investigation-quality-checklist.md` — ACSQHC standards self-assessment

## Privacy

De-identify all patient data: use `[Patient A]`, `[Case ID]`, `[Ward X]`.
Investigation reports may be legally privileged — mark `CONFIDENTIAL: QUALITY IMPROVEMENT`.
