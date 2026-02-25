# RCA & SAE Investigation Skill Suite — Design Document

**Date**: 2026-02-25
**Status**: Approved
**Jurisdiction**: Australia / New Zealand (primary default)
**Integration**: Cross-references existing health skills (incident-reporting, quality-improvement, clinical-risk-assessment, enterprise-risk-assessment)

---

## 1. Purpose

Create a comprehensive, state-of-the-art Root Cause Analysis (RCA) and Serious Adverse Event (SAE) investigation skill suite for healthcare organizations. The suite moves beyond traditional single-cause linear RCA toward modern systems-thinking approaches, recognizing that serious adverse events emerge from interactions between people, processes, technology, and organizational culture.

## 2. Architecture

### 2.1 Multi-Agent Design

Four specialized agents, one primary skill, integrated with the existing healthcare skill ecosystem.

**Primary Skill**: `rca-investigation` — Core workflow, method selection, operating modes, reference materials, and templates.

**Agents**:

| Agent | Role | Triggers |
|---|---|---|
| `rca-triage` | Classify incident severity (SAC 1-4), recommend investigation level and method(s), assign investigation team structure | SAC 1-2 incidents from incident-reporting; manual invocation |
| `rca-investigate` | Guide analysis execution using selected method(s), structured prompts for each method, combining multiple methods for complex events | After triage; method selection confirmed |
| `rca-report` | Generate investigation reports (full, executive, governance), populate DOCX/PPTX templates, create Mermaid diagrams | After investigation analysis complete |
| `rca-track` | Generate CAPA/action plans, link to QI skill (PDSA cycles), monitor action completion, trigger effectiveness reviews | After report accepted by governance |

### 2.2 Integration Flow

```
Incident Reporting (SAC 1-2) --> RCA Triage Agent --> RCA Investigate Agent
                                       |                       |
                                       v                       v
                              Clinical Risk Assessment    RCA Report Agent
                                                               |
                                                               v
                                                      RCA Track Agent --> Quality Improvement
                                                               |            (CAPA/PDSA)
                                                               v
                                                      Enterprise Risk
                                                      (systemic findings)
```

### 2.3 Integration Points

- `health-incident-reporting` -> triggers RCA triage for SAC 1-2 events
- `health-clinical-risk-assessment` -> risk scoring feeds into RCA prioritization; RCA findings create risk register entries
- `health-quality-improvement` -> CAPA/PDSA actions flow from RCA recommendations
- `health-enterprise-risk-assessment` -> systemic findings escalate to enterprise risk

## 3. Investigation Methods

### 3.1 Method Inventory

| Category | Method | Primary Use |
|---|---|---|
| **Core RCA** | RCA-squared (RCA²) | Enhanced RCA with stronger action focus (Joint Commission) |
| | 5 Whys | Rapid iterative cause drilling for simpler events |
| | Fishbone / Ishikawa | Structured cause-effect categorization |
| **Systems-Thinking** | Yorkshire Contributory Factors Framework | Comprehensive contributing factor analysis (SOTA) |
| | SEIPS 3.0 | Work system model: person, tasks, tools, environment, organization |
| | Swiss Cheese (Reason's Model) | Defence-in-depth failure analysis |
| **Structured Analysis** | Bow-Tie Analysis | Threat-barrier-consequence mapping |
| | Barrier Analysis | What barriers existed, failed, or were missing |
| | FMEA | Proactive failure mode identification and prioritization |
| | Timeline / Chronology Analysis | Event sequencing and gap identification |
| **Human Factors** | HFACS | Human factors classification (aviation-derived) |
| | London Protocol | Systematic clinical investigation framework |
| **Advanced / SOTA** | AcciMap | Multi-level systemic accident mapping |
| | STAMP/STPA | Systems-theoretic accident model with control structures |

### 3.2 Method Selection Matrix

Selection based on four dimensions:

| Dimension | Options |
|---|---|
| **Severity** | SAC 1 (catastrophic), SAC 2 (major), SAC 3 (moderate), SAC 4 (minor) |
| **Complexity** | Single event, multi-factorial, systemic |
| **Timeframe** | Rapid (48h), Standard (4-6 weeks), Comprehensive (8-12 weeks) |
| **Purpose** | Learning, Compliance, Both |

**Recommended combinations by SAC level:**

- **SAC 1**: Timeline + Yorkshire Framework + Bow-Tie + SEIPS (comprehensive, 8-12 weeks)
- **SAC 2**: Timeline + Yorkshire Framework + Fishbone or London Protocol (standard, 4-6 weeks)
- **SAC 3**: 5 Whys + Contributing Factors summary (rapid, 1-2 weeks)
- **SAC 4**: 5 Whys or single-method review (48h-1 week)
- **Proactive/FMEA**: For new services, pathways, or standing orders before implementation

### 3.3 Method Combination Guide

Most SAC 1 investigations need 3-4 methods combined:

| Combination | When to Use |
|---|---|
| Timeline + Yorkshire + Bow-Tie | Complex clinical events with multiple contributing factors |
| Timeline + SEIPS + Swiss Cheese | System design failures, technology-related events |
| Timeline + London Protocol + HFACS | Events with significant human factors component |
| Timeline + AcciMap + Yorkshire | Events revealing organizational/regulatory system gaps |
| FMEA + Bow-Tie | Proactive risk analysis for new services/pathways |

## 4. Visual & Diagram Templates (Mermaid)

| RCA Method | Mermaid Type | Purpose |
|---|---|---|
| Fishbone/Ishikawa | `mindmap` | Cause-effect branching by category |
| Swiss Cheese | `block-beta` | Layered defence barriers with holes |
| Bow-Tie Analysis | `flowchart LR` | Threats -> event -> consequences with barriers |
| Timeline/Chronology | `timeline` | Sequenced event chronology with phases |
| 5 Whys | `flowchart TD` | Iterative causal chain |
| SEIPS 3.0 | `block-beta` | Work system -> process -> outcomes |
| Yorkshire Framework | `mindmap` | Contributing factor categories |
| AcciMap | `flowchart TD` | Multi-level systemic factors |
| HFACS | `block-beta` | Four-layer human factors pyramid |
| STAMP/STPA | `flowchart TD` | Control structure with feedback loops |
| Investigation Workflow | `flowchart TD` | End-to-end investigation process |
| FMEA Priority | `quadrantChart` | Severity vs likelihood plotting |

## 5. Document Templates

### 5.1 Markdown Templates (Working Documents)

1. Investigation Terms of Reference
2. Chronology / Timeline
3. Contributing Factors Analysis
4. Fishbone Diagram (text-based)
5. FMEA Worksheet
6. Barrier Analysis Matrix
7. Bow-Tie Analysis
8. Full RCA Investigation Report
9. SAE Review Report
10. Executive Summary
11. CAPA Action Plan
12. Open Disclosure Planning
13. Investigation Closure Report
14. Just Culture Assessment

### 5.2 DOCX Templates (Governance-Ready)

| Template | Purpose |
|---|---|
| RCA Investigation Report | Full investigation for governance submission |
| SAE Review Report | SAC-classified serious adverse event format |
| Executive Briefing | 2-page summary for executives/board |
| Terms of Reference | Investigation team mandate and scope |
| CAPA Action Plan | Corrective & Preventive Actions with tracking |
| Open Disclosure Record | Patient/family disclosure documentation |
| Investigation Closure | Formal closure and governance sign-off |

### 5.3 PPTX Templates (Presentation-Ready)

| Template | Slide Structure |
|---|---|
| Governance Committee Brief | Title -> Key facts -> Timeline -> Analysis -> Findings -> Recommendations -> Actions |
| Learning Presentation | What happened -> What we found -> Systems issues -> What changed -> Discussion |
| Executive Summary Deck | Key message -> Risk level -> Critical findings -> Actions -> Monitoring |

### 5.4 Style Guides

- DOCX style guide: professional healthcare corporate styling, accessibility compliant, consistent headers/footers, governance watermarks
- PPTX style guide: clean presentation styling, consistent colour palette, appropriate for clinical governance audiences

## 6. Reference Materials

| Reference | Content |
|---|---|
| Method Selection Matrix | Decision framework for choosing investigation methods |
| Method Combination Guide | Which methods complement each other for complex events |
| Safety-II Principles | Resilience engineering lens — what usually goes right and why it didn't |
| Just Culture Guide | Structured framework for human error vs at-risk behaviour vs reckless conduct |
| Investigation Quality Checklist | Self-assessment against ACSQHC standards before governance submission |

## 7. Regulatory Context

**Primary**: Australia / New Zealand
- NSQHS Standards (Standard 1: Clinical Governance)
- ACSQHC National RCA Guidelines
- AS/NZS ISO 31000:2018
- State/Territory WHS Acts
- SAC severity classification (SAC 1-4)
- Open Disclosure Framework (ACSQHC)

**SAC Severity Classification**:

| SAC Level | Description | Investigation Required |
|---|---|---|
| SAC 1 | Death or serious harm; sentinel event | Comprehensive RCA (mandatory) |
| SAC 2 | Moderate harm; temporary but significant | Formal investigation (standard RCA) |
| SAC 3 | Minor harm; additional treatment required | Concise investigation or rapid review |
| SAC 4 | Near miss; no harm | Local review; trend monitoring |

## 8. Privacy & Security

- De-identify all patient data: use [Patient A], [Case ID], [Ward X]
- No PHI/PII in templates, diagrams, or working documents
- Risk register entries are governance documents — controlled access
- Open disclosure records require secure storage per jurisdiction requirements
- Investigation reports may be legally privileged — mark appropriately

## 9. File Structure

```
rca/
├── CLAUDE.md
├── skills/
│   └── rca-investigation/
│       ├── SKILL.md
│       ├── references/
│       │   ├── methods/
│       │   │   ├── rca-squared.md
│       │   │   ├── five-whys.md
│       │   │   ├── fishbone.md
│       │   │   ├── yorkshire-framework.md
│       │   │   ├── seips.md
│       │   │   ├── swiss-cheese.md
│       │   │   ├── bow-tie.md
│       │   │   ├── barrier-analysis.md
│       │   │   ├── fmea.md
│       │   │   ├── timeline-analysis.md
│       │   │   ├── hfacs.md
│       │   │   ├── london-protocol.md
│       │   │   ├── accimap.md
│       │   │   └── stamp-stpa.md
│       │   ├── method-selection-matrix.md
│       │   ├── method-combination-guide.md
│       │   ├── safety-ii-principles.md
│       │   ├── just-culture-guide.md
│       │   └── investigation-quality-checklist.md
│       └── assets/
│           ├── templates/
│           │   ├── markdown/
│           │   │   ├── 01-investigation-tor.md
│           │   │   ├── 02-chronology.md
│           │   │   ├── 03-contributing-factors.md
│           │   │   ├── 04-fishbone-diagram.md
│           │   │   ├── 05-fmea-worksheet.md
│           │   │   ├── 06-barrier-analysis.md
│           │   │   ├── 07-bow-tie-analysis.md
│           │   │   ├── 08-rca-investigation-report.md
│           │   │   ├── 09-sae-review-report.md
│           │   │   ├── 10-executive-summary.md
│           │   │   ├── 11-capa-action-plan.md
│           │   │   ├── 12-open-disclosure-plan.md
│           │   │   ├── 13-investigation-closure.md
│           │   │   └── 14-just-culture-assessment.md
│           │   ├── mermaid/
│           │   │   ├── fishbone-ishikawa.mmd
│           │   │   ├── swiss-cheese-model.mmd
│           │   │   ├── bow-tie-analysis.mmd
│           │   │   ├── timeline-chronology.mmd
│           │   │   ├── five-whys-chain.mmd
│           │   │   ├── seips-work-system.mmd
│           │   │   ├── yorkshire-factors.mmd
│           │   │   ├── accimap-levels.mmd
│           │   │   ├── hfacs-layers.mmd
│           │   │   ├── stamp-control-structure.mmd
│           │   │   ├── investigation-workflow.mmd
│           │   │   └── fmea-priority-quadrant.mmd
│           │   ├── docx/
│           │   │   ├── rca-investigation-report.md
│           │   │   ├── sae-review-report.md
│           │   │   ├── executive-briefing.md
│           │   │   ├── terms-of-reference.md
│           │   │   ├── capa-action-plan.md
│           │   │   ├── open-disclosure-record.md
│           │   │   └── investigation-closure.md
│           │   └── pptx/
│           │       ├── governance-committee-brief.md
│           │       ├── learning-presentation.md
│           │       └── executive-summary-deck.md
│           └── styles/
│               ├── docx-style-guide.md
│               └── pptx-style-guide.md
├── agents/
│   ├── rca-triage.md
│   ├── rca-investigate.md
│   ├── rca-report.md
│   └── rca-track.md
└── docs/
    └── plans/
        └── 2026-02-25-rca-skill-design.md
```
