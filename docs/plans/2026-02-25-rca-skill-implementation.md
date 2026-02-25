# RCA & SAE Investigation Skill Suite — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a comprehensive healthcare RCA & SAE investigation skill suite with 14 analysis methods, 12 Mermaid diagram templates, 14 markdown working templates, 7 DOCX templates, 3 PPTX templates, 4 specialized agents, and full integration with existing health skills.

**Architecture:** Single primary skill (`rca-investigation`) with progressive disclosure (SKILL.md -> references/ -> assets/), four specialized agents for the investigation lifecycle (triage, investigate, report, track), and Mermaid diagram templates for visual analysis. AU/NZ primary jurisdiction, integrates with health-incident-reporting, health-clinical-risk-assessment, health-quality-improvement, and health-enterprise-risk-assessment.

**Tech Stack:** Markdown (skill files, templates, references), Mermaid (diagram templates .mmd), YAML frontmatter (skill metadata), plain text agents

**Design doc:** `docs/plans/2026-02-25-rca-skill-design.md`

---

### Task 1: Repository Bootstrap

**Files:**
- Create: `CLAUDE.md`
- Create: `skills/rca-investigation/SKILL.md`

**Step 1: Initialize git and create CLAUDE.md**

```bash
git init
```

Create `CLAUDE.md`:

```markdown
# RCA & SAE Investigation Skill Suite

Healthcare root-cause analysis and serious adverse event investigation tools for AU/NZ clinical governance.

## Conventions

- Jurisdiction: AU/NZ default (NSQHS Standards, ACSQHC RCA guidelines, SAC 1-4 severity)
- All templates de-identify patients: use [Patient A], [Case ID], [Ward X]
- Mermaid diagrams use .mmd extension
- DOCX/PPTX files are generation-instruction markdown files (not binary files)
- Agent files live in agents/ at repo root
- Skill reference files live in skills/rca-investigation/references/
- Templates live in skills/rca-investigation/assets/templates/

## Integration

This skill integrates with:
- health-incident-reporting (SAC 1-2 triggers RCA triage)
- health-clinical-risk-assessment (RCA findings create risk register entries)
- health-quality-improvement (CAPA/PDSA flows from RCA recommendations)
- health-enterprise-risk-assessment (systemic findings escalate to enterprise risk)
```

**Step 2: Create directory structure**

```bash
mkdir -p skills/rca-investigation/references/methods
mkdir -p skills/rca-investigation/assets/templates/markdown
mkdir -p skills/rca-investigation/assets/templates/mermaid
mkdir -p skills/rca-investigation/assets/templates/docx
mkdir -p skills/rca-investigation/assets/templates/pptx
mkdir -p skills/rca-investigation/assets/styles
mkdir -p agents
```

**Step 3: Create SKILL.md**

Create `skills/rca-investigation/SKILL.md`:

```markdown
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
```

**Step 4: Commit**

```bash
git add CLAUDE.md skills/rca-investigation/SKILL.md
git commit -m "feat: bootstrap repo with CLAUDE.md and core SKILL.md"
```

---

### Task 2: Core RCA Methods (Part 1 — Linear/Traditional)

**Files:**
- Create: `skills/rca-investigation/references/methods/rca-squared.md`
- Create: `skills/rca-investigation/references/methods/five-whys.md`
- Create: `skills/rca-investigation/references/methods/fishbone.md`
- Create: `skills/rca-investigation/references/methods/timeline-analysis.md`

**Step 1: Create `rca-squared.md`**

```markdown
# RCA² — Root Cause Analysis and Action

RCA² (pronounced "RCA squared") is the Joint Commission's enhanced RCA methodology, designed to
address the weakness of traditional RCA: that it identifies causes but rarely produces effective,
sustainable actions.

## Key Difference from Traditional RCA

Traditional RCA asks "why did this happen?" and produces a list of causes.
RCA² adds: "what actions would reliably prevent recurrence?" and scores those actions
by strength — preferring system-level changes over administrative controls.

## Process

### Phase 1: Preparation (Day 1-3)
1. Confirm investigation team composition (team leader, clinical lead, quality/safety, frontline staff, patient/family representative for SAC 1)
2. Preserve evidence: medical records, equipment, incident reports, policies
3. Define scope with Terms of Reference (see template 01)
4. Brief team on RCA² methodology and Just Culture principles

### Phase 2: Data Collection (Week 1-2)
1. Build detailed timeline (see Timeline Analysis method)
2. Interview all involved staff using non-punitive, open questioning
3. Review relevant policies, procedures, training records
4. Inspect environment, equipment, and physical factors
5. Identify all contributing factors (use Yorkshire Framework as complement)

### Phase 3: Causal Analysis (Week 2-3)
1. Map the causal pathway from contributing factors to the adverse event
2. For each contributing factor, ask: "What was the direct cause? What was the indirect/system cause?"
3. Identify proximate cause(s): the most immediate factor(s) that led to harm
4. Identify root cause(s): the fundamental system failures that, if eliminated, would prevent recurrence
5. Avoid blaming individuals — trace back to system and organizational factors

### Phase 4: Action Development (Week 3-4)
Score proposed actions using the RCA² Action Strength Hierarchy:

| Strength | Action Type | Examples |
|---|---|---|
| **Strong** | Forcing functions, system redesign | Remove hazardous drug from ward stock; require two-person check with system lock |
| **Strong** | Automation and computerization | Clinical decision support alerts; automated dosing calculators |
| **Intermediate** | Redundancy and checks | Independent double-check protocols; read-back confirmation |
| **Intermediate** | Reminders and checklists | Pre-procedure safety checklists; medication reconciliation prompts |
| **Weak** | Training and education | Competency assessment; simulation training |
| **Weak** | Policies and procedures | Updated protocol; standing order revision |
| **Weak** | Warnings and labels | Warning stickers; visual cues |

**Rule:** At least one strong or intermediate action required for every identified root cause.
Weak actions alone are insufficient for SAC 1 and SAC 2 events.

### Phase 5: Report and Governance (Week 4-6)
1. Draft RCA² report (use template 08)
2. Present to Clinical Governance Committee
3. Submit to health department if SAC 1 or mandatory notification required
4. Implement CAPA action plan (use template 11)
5. Set effectiveness review timeline (typically 3, 6, and 12 months)

## Investigation Team Composition

| Role | SAC 1 | SAC 2 | SAC 3 |
|---|---|---|---|
| Team leader (not directly involved) | Mandatory | Mandatory | Mandatory |
| Clinical lead (relevant specialty) | Mandatory | Mandatory | Recommended |
| Quality/safety professional | Mandatory | Mandatory | Recommended |
| Frontline staff (direct care) | Mandatory | Mandatory | Recommended |
| Patient/family representative | Mandatory (offered) | Recommended | Optional |
| Human factors expert | Recommended | Optional | — |
| External investigator | For complex or high-profile | Optional | — |

## Common Pitfalls

- Stopping at "human error" — always ask what system factors enabled the error
- Generating only weak actions (training/policy) — these have the highest failure rate
- Over-scoping the investigation — focus on system factors, not exhaustive process mapping
- Excluding frontline staff — they have the richest knowledge of actual work vs. intended work
- Confusing proximate and root causes — proximate is what happened; root is why the system allowed it
```

**Step 2: Create `five-whys.md`**

```markdown
# 5 Whys

Iterative interrogative technique that drills from the symptom to the root cause by asking "why"
five times (or until no further cause can be identified). Best for SAC 3-4 events and as a
starting framework before escalating to deeper methods for complex events.

## Process

1. **State the problem clearly**: "Patient received wrong medication dose."
2. **Ask Why #1**: "Why did the patient receive the wrong dose?" → Answer: The nurse drew up 10mg instead of 1mg.
3. **Ask Why #2**: "Why did the nurse draw up the wrong dose?" → Answer: The ampoules for 1mg and 10mg look identical.
4. **Ask Why #3**: "Why do similar ampoules remain in the same location?" → Answer: Storage policy doesn't differentiate by concentration.
5. **Ask Why #4**: "Why doesn't the storage policy differentiate?" → Answer: The policy was written before the 10mg concentration was added to formulary.
6. **Ask Why #5**: "Why wasn't the policy updated when the new concentration was added?" → Answer: No process exists to review storage policies when new medications are added to formulary.
7. **Root cause**: No medication addition-to-formulary review process that triggers storage policy update.

## When to Stop

Stop when:
- The cause is outside your organization's control
- The answer is "no process exists" (you've found a system gap)
- Further drilling produces circular answers
- You've reached policy, culture, or resource decisions at organizational level

## Template

```
Problem statement: _______________________________________________

Why #1: ________________________________________________________
Because: _______________________________________________________

Why #2: ________________________________________________________
Because: _______________________________________________________

Why #3: ________________________________________________________
Because: _______________________________________________________

Why #4: ________________________________________________________
Because: _______________________________________________________

Why #5: ________________________________________________________
Because: _______________________________________________________

Root cause(s) identified: _________________________________________
```

## Limitations

- Works best for linear, single-cause chains — complex events have multiple parallel chains
- Risk of "tunnel vision" — stopping at a convenient answer rather than the true root
- Different people asking the same whys may reach different causes
- Does not surface contributing factors beyond the selected chain

**For complex events**: Use 5 Whys as initial exploration, then apply Yorkshire Framework or London
Protocol to capture the full contributing factor picture.

## Mermaid Diagram

Use template `assets/templates/mermaid/five-whys-chain.mmd`
```

**Step 3: Create `fishbone.md`**

```markdown
# Fishbone / Ishikawa Diagram

Cause-and-effect diagram that organizes contributing factors into categories around a central
problem (the "head" of the fish). Particularly effective for facilitating multidisciplinary
team discussions and ensuring systematic coverage of all factor categories.

## Healthcare Fishbone Categories (6Ms adapted for clinical)

| Category | Healthcare Adaptation | Examples |
|---|---|---|
| **Man (People)** | Staff, patients, family | Training gaps, fatigue, communication failures, patient complexity |
| **Machine (Equipment)** | Devices, technology, IT | Device failure, alarm fatigue, EMR design, missing equipment |
| **Method (Process)** | Procedures, protocols, pathways | Ambiguous policy, absent checklist, poor handover process |
| **Material (Medications/Supplies)** | Drugs, consumables, blood products | Lookalike/sound-alike drugs, supply shortage, labelling errors |
| **Environment** | Physical space, culture, workload | Noise, lighting, staffing ratios, organizational culture |
| **Management (Organization)** | Leadership, governance, resources | Budget constraints, governance gaps, conflicting priorities |

## Process

1. Define the problem statement (the "head") — be specific and factual
2. Draw the main "spine" with the problem at the right
3. Add the six category "bones" as diagonal branches
4. Brainstorm causes for each category in the team
5. Add sub-causes to each cause (smaller bones)
6. Identify the most likely root causes based on evidence
7. Prioritize for action

## Tips

- Use the fishbone as a team brainstorming tool, not a solo exercise
- Each branch can have multiple levels of sub-causes
- Not every category will have causes — that's normal
- Circle or highlight causes confirmed by evidence vs. hypothesised
- Combine with Timeline Analysis: causes on the fishbone should map to events in the timeline

## Text-Based Fishbone Format

```
                    PEOPLE          EQUIPMENT
                    /                 /
Training gap ---+  / EMR alert --+  /
Fatigue     ---+|/     failure   |/
                |
================|===============> PROBLEM: [State problem]
                |
Communication --|\  Policy -----+\
gap            |  \ absent      |  \
               +   \           +    \
                  PROCESS         ORGANIZATION
```

## Mermaid Diagram

Use template `assets/templates/mermaid/fishbone-ishikawa.mmd`

## Limitations

- Static snapshot — doesn't show temporal sequence
- Can generate long lists without identifying which causes are most significant
- Requires experienced facilitation to prevent blame culture emerging

**Complement with**: Timeline Analysis (temporal sequence), Yorkshire Framework (validated factor categories), 5 Whys (depth drilling on specific branches)
```

**Step 4: Create `timeline-analysis.md`**

```markdown
# Timeline / Chronology Analysis

Constructs a detailed, accurate sequence of events before, during, and after an adverse event.
The timeline is the foundation of almost every investigation — it provides the factual backbone
that all other analysis methods build upon.

## Process

### Phase 1: Evidence Gathering
Collect all sources of temporal data:
- Medical records (clinical notes, observation charts, medication records, imaging)
- Electronic systems (EMR timestamps, nursing call logs, alert systems, CCTV if available)
- Incident reports and near-miss reports
- Staff interviews (individual, before group discussions)
- Equipment logs and maintenance records
- Communications (handover notes, referral letters, phone logs)

### Phase 2: Build the Raw Timeline
1. List every event in chronological order with exact timestamp where known
2. Note the source of each event (whose record, which system)
3. Flag gaps where no information exists
4. Note discrepancies between sources (different accounts of the same event)

### Phase 3: Annotate the Timeline
For each entry, annotate:
- **What happened**: Factual description
- **Who was involved**: Staff, patient, family
- **What was known vs. unknown** at that point in time
- **Decision points**: Where a different decision could have changed the outcome
- **Warning signs**: Early signals that went unrecognized or unacted upon
- **Barriers**: Controls that were in place, bypassed, absent, or failed

### Phase 4: Identify Critical Intervals
- Time from first warning sign to recognition
- Time from recognition to escalation
- Time from escalation to response
- Any gaps in monitoring or observation
- Any periods of miscommunication or handover failure

## Timeline Template Format

```
PHASE 1: PRE-EVENT (background context)
[Date/Time] | [Event] | [Source] | [Notes/Significance]
...

PHASE 2: EARLY INCIDENT (warning signs)
[Date/Time] | [Event] | [Source] | [Warning sign? Y/N]
...

PHASE 3: INCIDENT / ACUTE PHASE
[Date/Time] | [Event] | [Source] | [Decision point? Y/N]
...

PHASE 4: RESPONSE AND ESCALATION
[Date/Time] | [Event] | [Source] | [Barrier present? Y/N]
...

PHASE 5: POST-EVENT (disclosure, investigation, actions)
[Date/Time] | [Event] | [Source]
...
```

## Mermaid Diagram

Use template `assets/templates/mermaid/timeline-chronology.mmd`

## Common Pitfalls

- Accepting a single source as definitive — cross-reference multiple records
- Assuming clocks are synchronized — EMR, nursing station, phone, and CCTV clocks may differ
- Focusing only on the acute event — the pre-event context often contains the most important findings
- Conflating what was known at the time with hindsight knowledge
- Omitting "nothing happened" intervals — these gaps are often as significant as events

## Integration

The timeline should be shared with the investigation team before applying any other analysis method.
It provides the shared factual foundation for Fishbone, Yorkshire Framework, Bow-Tie, and all other methods.
```

**Step 5: Commit**

```bash
git add skills/rca-investigation/references/methods/
git commit -m "feat: add core linear RCA methods (RCA², 5 Whys, Fishbone, Timeline)"
```

---

### Task 3: Systems-Thinking Methods

**Files:**
- Create: `skills/rca-investigation/references/methods/yorkshire-framework.md`
- Create: `skills/rca-investigation/references/methods/seips.md`
- Create: `skills/rca-investigation/references/methods/swiss-cheese.md`
- Create: `skills/rca-investigation/references/methods/london-protocol.md`

**Step 1: Create `yorkshire-framework.md`**

```markdown
# Yorkshire Contributory Factors Framework

The Yorkshire Contributory Factors Framework (YCFF) is a validated, evidence-based taxonomy of
contributing factors in healthcare adverse events. Developed from analysis of real incidents in the
UK NHS, it provides a comprehensive, structured vocabulary for describing why adverse events occur.

This is the **recommended primary contributing factor framework** for SAC 1-2 investigations.

## Factor Categories

### Level 1: Active Failures (at the point of care)

| Factor | Description | Investigation Questions |
|---|---|---|
| **Verification** | Failure to check, confirm, or verify | Was patient identity confirmed? Was the right drug/dose/patient verified? |
| **Monitoring** | Failure to observe, detect, or track | Was the patient being monitored at appropriate frequency? Were deterioration signs recognized? |
| **Communication** | Failure to convey critical information | Was the handover complete? Were concerns escalated? Were instructions unambiguous? |
| **Documentation** | Failure in records, noting, or information transfer | Were records contemporaneous? Were allergies/contraindications documented? |

### Level 2: Error-Producing Conditions (immediate work environment)

| Factor | Description | Investigation Questions |
|---|---|---|
| **Task factors** | Complexity, novelty, procedure design | Was the task well-designed? Were steps clear and unambiguous? |
| **Patient factors** | Complexity, acuity, communication ability | Was the patient's complexity recognized? Were communication needs addressed? |
| **Individual factors** | Skills, knowledge, competence, fatigue | Did staff have the training required? Were fatigue/workload factors present? |
| **Team factors** | Supervision, leadership, team dynamics | Was supervision adequate? Were concerns raised and acted upon? |
| **Physical environment** | Space, noise, lighting, interruptions | Did the environment support safe care? Were there distracting or competing demands? |
| **Equipment and supplies** | Availability, functionality, design | Was equipment available and working? Were supplies appropriate and correctly labelled? |

### Level 3: Latent Conditions (organizational)

| Factor | Description | Investigation Questions |
|---|---|---|
| **Management of staff** | Staffing levels, rostering, skill mix | Were staffing levels appropriate for workload and acuity? |
| **Training and education** | Induction, competency, simulation | Was training current and appropriate? Were competencies verified? |
| **Policy and procedures** | Clarity, currency, accessibility | Were policies clear, current, and accessible at the point of care? |
| **Barriers and defences** | Safety systems, checks, redundancies | What barriers existed? Which failed or were bypassed? |

### Level 4: Context Factors (external)

| Factor | Description |
|---|---|
| **Organizational culture** | Safety culture, reporting culture, openness to learning |
| **External context** | Regulatory, resource, workforce supply pressures |

## Process

1. Convene the investigation team after the timeline is complete
2. For each phase of the timeline, systematically work through each factor category
3. Ask the investigation questions for each category — even if the answer is "not a factor"
4. Document each confirmed contributing factor with supporting evidence
5. Distinguish between: Definitely contributed / Possibly contributed / Not a factor
6. Map contributing factors to specific points in the timeline

## Output Format

```
CONTRIBUTING FACTOR ANALYSIS — [Event ID]

ACTIVE FAILURES
[ ] Verification: ________________________________________________
[ ] Monitoring: _________________________________________________
[ ] Communication: ______________________________________________
[ ] Documentation: ______________________________________________

ERROR-PRODUCING CONDITIONS
[ ] Task factors: ________________________________________________
[ ] Patient factors: _____________________________________________
[ ] Individual factors: __________________________________________
[ ] Team factors: ________________________________________________
[ ] Physical environment: ________________________________________
[ ] Equipment and supplies: ______________________________________

LATENT CONDITIONS
[ ] Management of staff: _________________________________________
[ ] Training and education: ______________________________________
[ ] Policy and procedures: _______________________________________
[ ] Barriers and defences: _______________________________________

CONTEXT FACTORS
[ ] Organizational culture: ______________________________________
[ ] External context: ____________________________________________
```

## Mermaid Diagram

Use template `assets/templates/mermaid/yorkshire-factors.mmd`
```

**Step 2: Create `seips.md`**

```markdown
# SEIPS 3.0 — Systems Engineering Initiative for Patient Safety

SEIPS (Systems Engineering Initiative for Patient Safety) is a work system model that analyzes
healthcare as a system of interacting components. SEIPS 3.0 (2020) is the current version and the
most SOTA framework for understanding how work system design leads to (or prevents) adverse events.

## The SEIPS Work System Model

SEIPS frames adverse events as emerging from the interaction of five work system components during
processes of care, producing health outcomes for patients and workers.

```
WORK SYSTEM COMPONENTS
┌──────────────────────────────────────────────────────────────────┐
│  PERSON(S) ←→ TASKS ←→ TOOLS & TECHNOLOGY                       │
│                    ↕                                              │
│          ENVIRONMENT ←→ ORGANIZATION                             │
└──────────────────────────────────────────────────────────────────┘
                         ↓
              PROCESSES (care delivery)
                         ↓
              OUTCOMES (patient safety, quality, staff wellbeing)
```

## Work System Components

### Person(s)
Physical, cognitive, psychosocial attributes of all involved:
- Staff: Knowledge, skills, training, fatigue, workload, values
- Patient: Health status, cognitive ability, health literacy, language, cultural factors
- Family/carers: Role in care, communication, presence

### Tasks
Characteristics of the work being performed:
- Task complexity and cognitive demands
- Task clarity (clear steps, goals, criteria for success)
- Task sequencing and interdependencies
- Task demands vs. human capabilities

### Tools and Technology
Physical and information technology:
- Medical devices: Design, labelling, usability, alerts
- IT systems: EMR design, alert burden, interoperability
- Physical equipment: Availability, maintenance, ergonomics
- Medications: Packaging, naming, storage design

### Environment
Physical and social workspace:
- Physical: Space, layout, lighting, noise, temperature
- Social: Team culture, communication norms, psychological safety
- Temporal: Time pressure, shift patterns, interruptions

### Organization
Structural and governance factors:
- Staffing: Ratios, skill mix, rostering
- Culture: Safety culture, reporting culture, learning culture
- Leadership: Clinical governance, management support
- Policies: Currency, clarity, accessibility, compliance monitoring

## Investigation Process

For each work system component, ask:
1. **What was the state of this component at the time of the event?**
2. **How did it interact with other components?**
3. **What were the unintended consequences of these interactions?**
4. **What would better design of this component look like?**

## SEIPS Analysis Table

```
| Component | State at Time of Event | Interaction(s) | Redesign Opportunity |
|---|---|---|---|
| Person(s) — Staff | | | |
| Person(s) — Patient | | | |
| Tasks | | | |
| Tools & Technology | | | |
| Environment | | | |
| Organization | | | |
```

## When to Use SEIPS

SEIPS is particularly powerful for:
- Technology-related adverse events (EMR, device failures, alarm fatigue)
- Events involving complex patient populations (elderly, ICU, mental health)
- Events where the work system design enabled rather than prevented harm
- New service design and risk assessment (proactive SEIPS analysis)

## Mermaid Diagram

Use template `assets/templates/mermaid/seips-work-system.mmd`
```

**Step 3: Create `swiss-cheese.md`**

```markdown
# Swiss Cheese Model (Reason's Model of Organisational Accidents)

James Reason's Swiss Cheese Model (1990, updated 2000) describes how adverse events occur when
holes in multiple defensive layers align, allowing a hazard trajectory to reach and harm a patient.

## Core Concept

Each layer of defence (a "slice of cheese") has holes — gaps in protection caused by active
failures and latent conditions. Normally, holes in different layers are misaligned and the hazard
is stopped. An adverse event occurs when holes align across all layers simultaneously.

```
Hazard ──→ [Layer 1] ──→ [Layer 2] ──→ [Layer 3] ──→ [Layer 4] ──→ HARM
          (policy)    (training)   (supervision) (checking)

When holes align:
Hazard ──→ ○ hole ──→ ○ hole ──→ ○ hole ──→ ○ hole ──→ HARM
```

## Defensive Layers in Healthcare

| Layer | Examples | Common Failure Modes |
|---|---|---|
| **Design** | Safe system design, forcing functions, human factors | Poor interface design, ambiguous labelling, similar packaging |
| **Policy and procedure** | Clinical protocols, standing orders, guidelines | Absent, outdated, unclear, or inaccessible policies |
| **Training and competency** | Orientation, simulation, competency assessment | Training not current, competency not verified, high staff turnover |
| **Supervision** | Senior oversight, clinical review, escalation | Inadequate supervision, escalation barriers, after-hours gaps |
| **Independent checks** | Double-checks, sign-off requirements, peer review | Checks bypassed, rubber-stamping, check fatigue |
| **Technology** | Decision support, alerts, automated verification | Alert fatigue, technology failure, workarounds |
| **Patient and family** | Patient involvement, open disclosure, speaking up | Disempowerment, health literacy barriers, cultural factors |

## Investigation Process

1. List all defensive layers relevant to this type of event
2. For each layer, determine: Was it present? Was it functioning? Was it bypassed?
3. Identify the specific "holes" in each layer that allowed the harm trajectory to pass through
4. Classify each hole as: Active failure (human action/inaction) or Latent condition (system design flaw)
5. Map holes across layers to understand the alignment that allowed the event

## Analysis Table

```
| Defensive Layer | Present? | Functioning? | Nature of Hole | Active/Latent |
|---|---|---|---|---|
| Design | Y/N | Y/N | | |
| Policy/Procedure | Y/N | Y/N | | |
| Training/Competency | Y/N | Y/N | | |
| Supervision | Y/N | Y/N | | |
| Independent Checks | Y/N | Y/N | | |
| Technology | Y/N | Y/N | | |
| Patient/Family | Y/N | Y/N | | |
```

## Key Insight for Action Planning

Weak defences: Training, policy, supervision (human-dependent, fail under pressure)
Strong defences: Design, forcing functions, automation (system-level, fail-safe)

Actions should strengthen the weakest layers AND introduce new layers where gaps exist.

## Mermaid Diagram

Use template `assets/templates/mermaid/swiss-cheese-model.mmd`
```

**Step 4: Create `london-protocol.md`**

```markdown
# London Protocol

The London Protocol (Vincent, Taylor-Adams & Stanhope, 1998; updated 2004) is a systematic
clinical investigation framework structured around seven contributing factor categories. It provides
a comprehensive interview and investigation guide for structured clinical incident analysis.

## Contributing Factor Categories

| Category | Key Questions |
|---|---|
| **Patient factors** | Patient complexity, communication, contribution to the event |
| **Task and technology** | Task design, guideline quality, decision support availability |
| **Individual factors** | Knowledge/skills, competence assessment, physical and mental state |
| **Team factors** | Communication, supervision, team structure and leadership |
| **Work environment** | Staffing, workload, physical environment, equipment |
| **Organisational factors** | Financial, safety culture, priorities and constraints |
| **Institutional context** | Regulatory, economic, policy environment |

## Process

### Step 1: Identify the Care Management Problems
What specifically went wrong in the care? (Not the outcome — the specific care problems)
Example: "Deteriorating patient not escalated for 4 hours despite documented vital sign changes"

### Step 2: Identify Contributing Factors
For each care management problem, work through all seven factor categories.
Use the interview guide (below) with each staff member individually.

### Step 3: Build the Causal Tree
Map from the adverse outcome back through care management problems to contributing factors.

### Step 4: Develop Recommendations
For each contributing factor, identify: What would prevent this from occurring again?

## Interview Guide

Use these questions in individual staff interviews. The goal is understanding, not blame.

**Opening**: "I want to understand what happened and why, so we can learn and improve. There are no
right or wrong answers — your perspective is essential."

**Timeline**: "Can you walk me through your shift/involvement from [time] to [time]?"

**Decision making**: "At the point where [specific action], what were you thinking? What information did you have?"

**Conditions**: "What was the unit/ward like at that time? Staffing? Workload?"

**Knowledge/training**: "Had you encountered this situation before? What training had you had?"

**System factors**: "Was there anything about the policy, equipment, or system that made this harder than it needed to be?"

**Hindsight**: "What, if anything, would you do differently? What would help you in the future?"

**Closing**: "Is there anything else you think I should know to understand what happened?"

## Causal Tree Format

```
ADVERSE OUTCOME
        ↑
CARE MANAGEMENT PROBLEM 1    CARE MANAGEMENT PROBLEM 2
        ↑                              ↑
Contributing Factor A    Contributing Factor B    Contributing Factor C
        ↑                              ↑
System Factor X               System Factor Y
```
```

**Step 5: Commit**

```bash
git add skills/rca-investigation/references/methods/
git commit -m "feat: add systems-thinking methods (Yorkshire, SEIPS, Swiss Cheese, London Protocol)"
```

---

### Task 4: Structured Analysis Methods

**Files:**
- Create: `skills/rca-investigation/references/methods/bow-tie.md`
- Create: `skills/rca-investigation/references/methods/barrier-analysis.md`
- Create: `skills/rca-investigation/references/methods/fmea.md`
- Create: `skills/rca-investigation/references/methods/hfacs.md`

**Step 1: Create `bow-tie.md`**

```markdown
# Bow-Tie Analysis

Bow-Tie Analysis maps the relationship between threats (left side), a central hazardous event,
and consequences (right side), with barriers on each side. It provides a visual, comprehensive
picture of risk controls and their adequacy.

## Structure

```
THREATS          BARRIERS          EVENT          BARRIERS          CONSEQUENCES
(causes)         (preventive)      (top event)    (recovery)        (outcomes)

Threat 1 ──[B1]──→╮
Threat 2 ──[B2]──→╮──→ EVENT ──→[B4]──→ Consequence 1
Threat 3 ──[B3]──→╯              [B5]──→ Consequence 2
```

Left side: Prevention (stop the event occurring)
Right side: Mitigation (reduce harm once the event occurs)

## Components

**Hazardous Event (Top Event)**: The central failure or hazardous state
Example: "Patient receives incorrect medication"

**Threats (left)**: All plausible causes that could lead to the top event
- Communication breakdown during handover
- Look-alike/sound-alike drug names
- EMR prescribing error

**Preventive Barriers (left)**: Controls that interrupt the threat-to-event pathway
- Pharmacist verification
- Two-nurse check before administration
- Clinical decision support alert

**Consequences (right)**: Potential harms if the event occurs
- Adverse drug reaction
- Therapeutic failure
- Patient death

**Recovery Barriers (right)**: Controls that reduce consequences once the event has occurred
- Rapid response team activation
- Antidote availability
- Incident reporting and escalation

## For Adverse Event Investigation

When investigating a past event:
1. Map the actual threat pathway that led to the event (the one that penetrated all left barriers)
2. Identify which preventive barriers failed or were absent
3. Map the consequences that resulted
4. Identify which recovery barriers worked, failed, or were absent
5. Identify both missing barriers and failed barriers

## Annotation for Investigation

Mark each barrier with status:
- ✓ Functioned correctly
- ✗ Failed
- ∅ Absent/not in place
- → Bypassed/circumvented

## Mermaid Diagram

Use template `assets/templates/mermaid/bow-tie-analysis.mmd`

## When to Use

Bow-Tie is most powerful for:
- Events with multiple possible causes (threats) and multiple possible consequences
- Risk communication to non-technical audiences
- Demonstrating the adequacy of current controls
- Identifying gaps in barrier systems
- Proactive analysis of new services or high-risk processes
```

**Step 2: Create `barrier-analysis.md`**

```markdown
# Barrier Analysis

Barrier Analysis identifies what physical, procedural, or cognitive barriers exist to prevent
harm, which of those barriers failed in the event under investigation, and what additional barriers
should be created. Closely related to Bow-Tie but focused specifically on the barrier inventory.

## Barrier Types (Hierarchy of Effectiveness)

| Type | Description | Effectiveness | Examples |
|---|---|---|---|
| **Physical/Engineering** | Physical constraint preventing harm | Highest | Drug storage lock, needle-free connector, forced function in EMR |
| **Natural** | Distance, time, or natural separation | High | Separate storage for high-risk medications |
| **Human action** | Procedural checks requiring human action | Moderate | Independent double-check, sign-off |
| **Administrative** | Policy, procedure, training | Lower | Protocol, standing order, competency |
| **Warning/symbolic** | Alerts, labels, colour-coding | Lowest | Warning sticker, alert pop-up, tall-man lettering |

## Analysis Process

For the adverse event being investigated:

### Step 1: Barrier Inventory
List all barriers that should have prevented or mitigated this event.
For each barrier, document:
- Barrier type (physical/natural/human/administrative/warning)
- Was it present? (Y/N)
- Did it function? (Y/N)
- If it failed, why? (Active failure / Latent condition / Not applicable)

### Step 2: Barrier Gap Analysis
Identify barriers that:
- Were present but failed
- Were present but bypassed
- Should have existed but were absent

### Step 3: Barrier Strengthening Recommendations
For each gap, recommend:
- Strengthen the existing barrier
- Add a new, stronger barrier
- Add a redundant barrier (defence in depth)

## Analysis Table

```
| Barrier | Type | Present? | Functioned? | Failure Mode | Recommendation |
|---|---|---|---|---|---|
| | | Y/N | Y/N | | |
```

## Integration

Barrier Analysis is a natural complement to:
- **Swiss Cheese Model**: Each cheese layer is a barrier — analyse the holes in each
- **Bow-Tie Analysis**: Barriers on both the prevention and recovery sides
- **RCA²**: Action strength hierarchy aligns with barrier type hierarchy
```

**Step 3: Create `fmea.md`**

```markdown
# Failure Mode and Effects Analysis (FMEA)

FMEA is a proactive risk assessment tool that identifies potential failure modes in a process
BEFORE they cause harm. In healthcare, FMEA is used to analyze new services, high-risk
processes, and proposed changes to clinical pathways.

## FMEA vs. RCA

| | FMEA | RCA |
|---|---|---|
| Timing | Proactive — before harm occurs | Reactive — after harm occurs |
| Purpose | Prevent failures before they happen | Understand and prevent recurrence |
| Starting point | Process steps | Adverse event |
| Output | Risk priority scores + prevention actions | Root causes + corrective actions |

## Process Steps

### Step 1: Define the Process
Map every step in the process being analyzed.
Example process: "Administration of high-alert medication"
Steps: Prescribe → Verify → Dispense → Prepare → Administer → Monitor

### Step 2: Identify Failure Modes
For each step, ask: "In what ways could this step fail?"
List every possible failure mode.

### Step 3: Identify Effects
For each failure mode: "What is the effect on the patient if this failure occurs?"

### Step 4: Score Each Failure Mode
Score three dimensions on 1-10 scale:

**Severity (S)**: How serious is the effect on the patient?
1-2 = Negligible | 3-4 = Minor | 5-6 = Moderate | 7-8 = Major | 9-10 = Catastrophic

**Occurrence (O)**: How often does this failure mode occur?
1-2 = Almost never | 3-4 = Rare | 5-6 = Occasional | 7-8 = Frequent | 9-10 = Almost certain

**Detectability (D)**: How likely is detection before harm reaches the patient?
1-2 = Almost certain to detect | ... | 9-10 = Almost impossible to detect

**Risk Priority Number (RPN) = S × O × D**

### Step 5: Prioritize
- RPN > 200: Critical — immediate action required
- RPN 100-200: High — urgent action required
- RPN 50-99: Medium — action plan required
- RPN < 50: Low — monitor

Note: Any failure mode with Severity ≥ 9 requires action regardless of RPN.

### Step 6: Develop Actions
For each high/critical failure mode:
- What control prevents the failure from occurring? (reduce O)
- What detection mechanism catches the failure before harm? (reduce D)
- If neither, is the process step necessary? Can it be eliminated or redesigned? (reduce S)

## FMEA Worksheet Format

```
| Process Step | Failure Mode | Effect | S | O | D | RPN | Action | Owner | Target Date |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |
```

## Mermaid Diagram

Use template `assets/templates/mermaid/fmea-priority-quadrant.mmd` (Severity vs Occurrence)
```

**Step 4: Create `hfacs.md`**

```markdown
# HFACS — Human Factors Analysis and Classification System

HFACS was developed from James Reason's Swiss Cheese Model and originally applied in aviation
accident investigation (US military). It provides a structured taxonomy of human error and
organizational factors across four levels.

## The Four HFACS Levels

### Level 1: Unsafe Acts (at the point of care)

**Errors** (unintentional actions):
- **Skill-based errors**: Errors in the execution of a routine task (attention failures, memory lapses)
- **Decision errors**: Wrong choice based on insufficient information or incorrect knowledge
- **Perceptual errors**: Misjudgement of sensory information (distance, speed, ambiguous cues)

**Violations** (intentional deviations from procedures):
- **Routine violations**: Habitual deviation that is tacitly accepted ("we always do it this way")
- **Exceptional violations**: Unique deviation in response to unusual circumstances

### Level 2: Preconditions for Unsafe Acts

**Environmental factors**:
- Physical environment (noise, lighting, space, equipment)
- Technological environment (interface design, automation, alert systems)

**Condition of operators**:
- Adverse mental states (fatigue, distraction, stress, complacency)
- Adverse physiological states (illness, medication, physical limitation)
- Physical/mental limitations (lack of skill, inadequate knowledge)

**Personnel factors**:
- Crew/team resource management failures (communication, coordination)
- Personal readiness failures (pre-duty preparation, fitness for duty)

### Level 3: Unsafe Supervision

- **Inadequate supervision**: Failure to provide appropriate oversight
- **Planned inappropriate operations**: Inadequate briefings, overtime, heavy workload
- **Failed to correct known problem**: Ignoring safety deficiencies, ineffective training
- **Supervisory violations**: Knowingly allowing unsafe acts or conditions

### Level 4: Organizational Influences

- **Resource management**: Human resources (staffing, selection, training), monetary resources, equipment resources
- **Organizational climate**: Culture, policies, command structure, values
- **Organizational process**: Operations, procedures, oversight, incentives

## HFACS Classification Process

1. Review the timeline and contributing factor analysis
2. For each identified human action (or inaction), classify using the Level 1 taxonomy
3. For each Level 1 classification, trace back through Levels 2, 3, and 4 to identify enabling factors
4. This creates a structured causal chain from organizational influences down to the unsafe act

## HFACS Table

```
| Event/Action | Level 1 Category | Level 2 Factor | Level 3 Factor | Level 4 Factor |
|---|---|---|---|---|
| | | | | |
```

## Mermaid Diagram

Use template `assets/templates/mermaid/hfacs-layers.mmd`

## When to Use

HFACS is most useful when:
- Human error is a prominent feature of the event
- You need structured language for the "why" behind human actions
- The event involves complex team dynamics, fatigue, or high-stress environments
- You want to trace individual actions back to organizational system failures

**Important**: HFACS classifies errors for analysis — it does not assign blame. Use alongside
Just Culture framework to ensure fair treatment of individuals.
```

**Step 5: Commit**

```bash
git add skills/rca-investigation/references/methods/
git commit -m "feat: add structured analysis methods (Bow-Tie, Barrier Analysis, FMEA, HFACS)"
```

---

### Task 5: Advanced / SOTA Methods

**Files:**
- Create: `skills/rca-investigation/references/methods/accimap.md`
- Create: `skills/rca-investigation/references/methods/stamp-stpa.md`

**Step 1: Create `accimap.md`**

```markdown
# AcciMap — Accident Mapping

AcciMap (Rasmussen & Svedung, 2000) is a systems-thinking accident analysis method that maps
causal factors across multiple levels of a sociotechnical system. Unlike linear methods that trace
a single causal chain, AcciMap reveals the network of decisions and conditions at every level that
contributed to the accident.

## Levels of Analysis

AcciMap organizes factors into six levels:

| Level | Description | Examples in Healthcare |
|---|---|---|
| 6 | **Government and regulators** | Health legislation, funding policy, accreditation standards |
| 5 | **Regulatory bodies and associations** | ACSQHC, AMC, AHPRA, health department policy |
| 4 | **Local area / hospital management** | Executive decisions, resource allocation, culture |
| 3 | **Physical environment and technical** | Ward design, equipment, IT systems |
| 2 | **Staff / operators** | Clinical staff actions, decisions, communications |
| 1 | **Patient and activity** | Patient factors, the adverse event itself |

## Process

1. Build the timeline and contributing factor analysis first
2. Assign each identified contributing factor to one of the six levels
3. Map causal connections between factors across levels (arrows show influence)
4. Identify what decisions or conditions at each level contributed to, enabled, or failed to prevent the adverse event
5. Look for patterns: which levels have the most contributing factors? Where are the systemic gaps?

## AcciMap Diagram Format

```
LEVEL 6 (Government/Policy): [Factor A] ──→ [Factor B]
                                   ↓              ↓
LEVEL 5 (Regulators): [Factor C] ←── [Factor D]
                            ↓
LEVEL 4 (Management): [Factor E] ──→ [Factor F]
                                          ↓
LEVEL 3 (Technical/Environment): [Factor G]
                                          ↓
LEVEL 2 (Staff): [Action H] ──→ [Action I]
                                     ↓
LEVEL 1 (Patient/Event): [ADVERSE EVENT]
```

## When to Use AcciMap

AcciMap is most powerful for:
- Complex, multi-factorial events with organizational and regulatory contributing factors
- Events that reveal systemic issues requiring change at multiple levels
- Situations where traditional RCA would focus only on the "sharp end" (staff) and miss the blunt end (organization, policy)
- Healthcare system redesign and policy development

## Key Output for Governance

AcciMap explicitly shows governance bodies which level they are responsible for.
When presenting to the Clinical Governance Committee, highlight Level 3-4 factors.
When escalating to executive, highlight Level 4-5 factors.
For regulatory reporting, include Level 5-6 factors.

## Mermaid Diagram

Use template `assets/templates/mermaid/accimap-levels.mmd`
```

**Step 2: Create `stamp-stpa.md`**

```markdown
# STAMP/STPA — Systems-Theoretic Accident Model and Processes

STAMP (Leveson, 2004) is a causality model based on systems theory and control theory.
STPA (System-Theoretic Process Analysis) is the analysis technique derived from STAMP.

STAMP views accidents not as chains of events but as failures of control — where a controller
(person, system, or organization) fails to enforce constraints needed to prevent harm.

## Core Concepts

**Safety Constraints**: Conditions that must hold for the system to remain safe
Example: "Blood type must be verified before transfusion"

**Control Structure**: The hierarchy of controllers and controlled processes
- Controllers: Staff, systems, protocols, management
- Control actions: Orders, decisions, automated commands, policies
- Feedback: Vital signs, alerts, audit results, incident reports
- Controlled processes: Clinical care delivery

**Unsafe Control Actions (UCAs)**: When a controller provides the wrong action:
- Action not provided when needed
- Unsafe action provided
- Action provided too early, too late, or for too long
- Action stopped too soon

## STAMP Accident Causation

An accident occurs when:
1. Safety constraints are violated
2. Control actions fail to maintain those constraints
3. Inadequate feedback prevents controllers from knowing the system is out of safe state

## STPA Process

### Step 1: Define the accident and hazards
- Accident: Patient harmed (final outcome to prevent)
- Hazard: System state that leads to accident under certain conditions
Example hazard: "Patient receives incorrect blood product"

### Step 2: Map the control structure
Draw the hierarchy of controllers relevant to this process:
- Hospital policy/management → Department protocols → Clinical supervisor → Bedside nurse → Patient

### Step 3: Identify unsafe control actions
For each control link, identify UCAs across all four types (not provided, unsafe when provided, timing, duration)

### Step 4: Identify loss scenarios
For each UCA, identify the causal scenarios that could produce it:
- Controller had inadequate process model (wrong belief about system state)
- Controller received inadequate feedback
- Control algorithm was flawed (wrong protocol)
- Physical control failure (equipment malfunction)

### Step 5: Generate safety constraints and requirements
For each UCA, define the control constraint that would prevent it.
These become the system requirements for safe design.

## When to Use STAMP/STPA

STAMP/STPA is most powerful for:
- Complex sociotechnical systems with multiple interacting controllers
- Technology-heavy processes (EMR, automated systems, robotics)
- Proactive analysis of new systems or pathways before implementation
- Events where multiple controllers contributed and the interaction pattern is the problem
- Healthcare system redesign and safety architecture

## Mermaid Diagram

Use template `assets/templates/mermaid/stamp-control-structure.mmd`

## Note on Complexity

STAMP/STPA is the most technically sophisticated method in this suite. Use it for SAC 1 events
with complex technology or system interactions, or for major system redesign projects.
For most clinical adverse events, Yorkshire Framework + London Protocol + Swiss Cheese will be
sufficient and more accessible for clinical teams.
```

**Step 3: Commit**

```bash
git add skills/rca-investigation/references/methods/
git commit -m "feat: add advanced systems methods (AcciMap, STAMP/STPA)"
```

---

### Task 6: Supporting Reference Files

**Files:**
- Create: `skills/rca-investigation/references/method-selection-matrix.md`
- Create: `skills/rca-investigation/references/method-combination-guide.md`
- Create: `skills/rca-investigation/references/just-culture-guide.md`
- Create: `skills/rca-investigation/references/safety-ii-principles.md`
- Create: `skills/rca-investigation/references/investigation-quality-checklist.md`

**Step 1: Create `method-selection-matrix.md`**

```markdown
# Method Selection Matrix

## Primary Selection: By SAC Level

| SAC Level | Event Type | Recommended Methods | Timeframe |
|---|---|---|---|
| **SAC 1** | Death or serious harm; sentinel event | Timeline + Yorkshire Framework + Bow-Tie + SEIPS 3.0 ± London Protocol | 8-12 weeks |
| **SAC 2** | Moderate harm; temporary significant harm | Timeline + Yorkshire Framework + Fishbone OR London Protocol | 4-6 weeks |
| **SAC 3** | Minor harm; additional treatment required | 5 Whys + Yorkshire Framework (abbreviated) | 1-2 weeks |
| **SAC 4** | Near miss; no harm | 5 Whys | 48h-1 week |
| **Proactive** | New service, pathway, or high-risk process | FMEA + Bow-Tie | 2-4 weeks |

## Secondary Selection: By Event Characteristic

| Event Characteristic | Add This Method |
|---|---|
| Technology/device/EMR prominent | + SEIPS 3.0 |
| Human error prominent | + HFACS |
| Multiple organisational levels involved | + AcciMap |
| Complex sociotechnical system | + STAMP/STPA |
| Complex defence failures | + Swiss Cheese / Barrier Analysis |
| Patient safety culture concern | + Safety-II principles lens |

## Decision Questions

**Q1: What is the SAC level?** → Use SAC table above for baseline method set

**Q2: Is technology a major factor?** → Add SEIPS 3.0

**Q3: Are there significant human factors (fatigue, communication, decision-making)?** → Add HFACS

**Q4: Does the event reflect organisational or policy failures beyond the ward?** → Add AcciMap

**Q5: Are there multiple barrier failures?** → Add Swiss Cheese / Barrier Analysis

**Q6: Is this a proactive review of a new or high-risk process?** → Switch to FMEA + Bow-Tie

## Minimum Viable Investigation by SAC Level

**SAC 1 minimum**: Timeline + Yorkshire Framework + at least one systems-thinking method (SEIPS or London Protocol) + Bow-Tie for recommendations

**SAC 2 minimum**: Timeline + Yorkshire Framework

**SAC 3 minimum**: 5 Whys

**SAC 4 minimum**: 5 Whys or local team discussion with documented outcome
```

**Step 2: Create `method-combination-guide.md`**

```markdown
# Method Combination Guide

Most SAC 1-2 investigations use 3-4 methods together. Each method captures a different dimension
of the event. This guide shows which combinations are most effective.

## Recommended Combinations

### Combination 1: Standard SAC 1-2 (Most Common)
**Timeline + Yorkshire Framework + Bow-Tie**

- Timeline establishes factual sequence
- Yorkshire Framework maps all contributing factors systematically
- Bow-Tie maps the specific barriers that failed and guides action strength decisions

*Best for*: Clinical events with multiple contributing factors and identifiable barrier failures

### Combination 2: Technology-Heavy Events
**Timeline + SEIPS 3.0 + Swiss Cheese**

- Timeline establishes factual sequence
- SEIPS maps the work system components and their interactions
- Swiss Cheese identifies which defensive layers failed and why

*Best for*: EMR-related events, device failures, alarm fatigue, automation errors

### Combination 3: Human Factors Focus
**Timeline + London Protocol + HFACS**

- Timeline establishes factual sequence
- London Protocol provides structured interview and factor classification
- HFACS traces human actions back through levels to organizational influences

*Best for*: Events where communication, decision-making, fatigue, or team dynamics are prominent

### Combination 4: Systemic / Organisational Events
**Timeline + Yorkshire Framework + AcciMap**

- Timeline establishes factual sequence
- Yorkshire Framework maps ward-level contributing factors
- AcciMap maps factors at all levels from staff to government policy

*Best for*: Events revealing systemic issues requiring change at multiple organizational levels

### Combination 5: Proactive Risk Analysis
**FMEA + Bow-Tie**

- FMEA systematically identifies all failure modes in a process before implementation
- Bow-Tie maps the specific barriers and their adequacy for each high-risk failure mode

*Best for*: New services, new high-risk medications, pathway redesign, post-RCA process changes

### Combination 6: Comprehensive SAC 1 (Complex Events)
**Timeline + Yorkshire Framework + London Protocol + SEIPS + Bow-Tie**

Full systems-thinking investigation. Use when the event is highly complex, involves multiple
services, or has significant governance, media, or regulatory attention.

## Sequencing Methods

Always apply methods in this order:

1. **Timeline first** — establishes the shared factual foundation for the whole team
2. **Contributing factor analysis** (Yorkshire / London Protocol / HFACS) — identifies what was present
3. **Systems analysis** (SEIPS / Swiss Cheese / AcciMap) — explains how those factors interacted
4. **Barrier/action analysis** (Bow-Tie / Barrier Analysis) — guides what changes to make

Never start with Bow-Tie before the timeline and contributing factor analysis.
Never start contributing factor analysis without a shared timeline.
```

**Step 3: Create `just-culture-guide.md`**

```markdown
# Just Culture Guide

Just Culture is a framework for making fair, consistent decisions about individual accountability
in healthcare adverse events. It distinguishes between:
- **Human error**: Unintentional mistakes
- **At-risk behaviour**: Choices that increase risk, often without recognition
- **Reckless behaviour**: Conscious disregard for substantial and unjustifiable risk

Just Culture does NOT mean no accountability — it means the right type of accountability for the
right type of behaviour.

## The Just Culture Decision Tree

### Step 1: Was the act intentional?

- **No** → Go to Step 2
- **Yes** → This may be reckless behaviour or a violation. Go to Step 4.

### Step 2: Were there any substance issues or medical conditions?

- **Yes** → Manage through human resources and occupational health processes
- **No** → Go to Step 3

### Step 3: Would a competent, equally trained peer act the same way given the same circumstances?

- **Yes** → Likely **human error** → Console and support; examine system factors
- **No** → Go to Step 4

### Step 4: Was the risk of the behaviour recognized?

- **No** → Likely **at-risk behaviour** → Coach; manage through system and incentives
- **Yes** → Go to Step 5

### Step 5: Did the person have an expectation that this was acceptable?

- **Yes, created by management action/inaction** → At-risk behaviour created by organizational culture → Address at organizational level
- **No** → **Reckless behaviour** → May require disciplinary process

## Responses by Category

| Category | Response | Purpose |
|---|---|---|
| **Human Error** | Console; support; investigate system factors | Reduce future error opportunity; support the staff member |
| **At-Risk Behaviour** | Coach; remove incentives for at-risk choices; redesign system | Change behaviour pattern; address why risk-taking seemed reasonable |
| **Reckless Behaviour** | Consider disciplinary action | Deter intentional unsafe acts |

## Key Principle for RCA

**Human error is a symptom, not a cause.** When the Just Culture analysis identifies human error,
the RCA must go deeper: what were the system conditions that made the error likely or inevitable?

Common system conditions enabling human error:
- Poorly designed equipment or interfaces
- Inadequate training or competency verification
- Excessive workload or fatigue
- Ambiguous policies or procedures
- Absent or ineffective checking systems
- Organizational culture that discourages speaking up

## For SAC 1 Investigations

The Just Culture assessment should be completed **before** any consideration of disciplinary action.
Individual clinicians should not be disciplined for human error in a broken system.
All Just Culture findings should be documented in the investigation report.
```

**Step 4: Create `safety-ii-principles.md`**

```markdown
# Safety-II Principles — Resilience Engineering Lens

Safety-II is a complementary perspective to traditional Safety-I (prevent things from going wrong).

**Safety-I**: Study failures to prevent recurrence. Assumes safety = absence of accidents.
**Safety-II**: Study successes to understand how things usually go right, and strengthen those conditions.

## Core Insight

In healthcare, the vast majority of clinical encounters go well — despite the complexity, variability,
and imperfect systems. Safety-II asks: *how*? What are clinicians doing (individually and collectively)
to compensate for system weaknesses and produce safe outcomes most of the time?

Understanding this "performance adjustment" is essential for:
1. Not inadvertently removing the informal safety net when redesigning processes
2. Finding what we should protect and strengthen, not just what we should fix
3. Understanding the gap between "work as imagined" (policies/protocols) and "work as done" (actual practice)

## Work as Imagined vs. Work as Done

**Work as imagined**: How policy writers and management believe work is performed.
**Work as done**: How work is actually performed to get things done safely in real conditions.

The gap between these is filled by:
- Informal knowledge sharing
- Peer checking and mutual monitoring
- Ad hoc adaptations to unexpected conditions
- Tacit expertise developed through experience

In an adverse event investigation, ask: "What was different this time? What adaptations usually
present were absent or failed?"

## Applying Safety-II in an Investigation

Add these questions to any investigation:

1. **"How does this usually go right?"** — Before analysing the failure, understand the normal process
2. **"What was different about this occasion?"** — Not just what went wrong, but what was absent that usually protects
3. **"What informal safety checks exist that aren't in the policy?"** — Surface the invisible safety net
4. **"What was the staff trying to achieve?"** — Understand intent and adaptive behaviour
5. **"Would removing the conditions that caused the error also remove conditions that usually enable safety?"** — Prevent unintended harm from fixes

## Learning from Excellence

As a complement to adverse event investigation, consider "Learning from Excellence" (LfE):
structured analysis of clinical encounters that went exceptionally well. What conditions, behaviours,
and system factors enabled excellent care? These become candidates for strengthening and spreading.

## Practical Integration

When conducting a Yorkshire Framework or SEIPS analysis, add a Safety-II row/column:
- "What was the safety net that usually catches this? Why wasn't it present or effective this time?"
- This surfaces the invisible barriers that the Swiss Cheese model often misses because they aren't
  formally documented in policy.
```

**Step 5: Create `investigation-quality-checklist.md`**

```markdown
# Investigation Quality Checklist

Use this checklist to self-assess the quality of an RCA or SAE investigation before governance submission.
Adapted from ACSQHC National RCA Guidelines and Joint Commission RCA² standards.

## 1. Scope and Context

- [ ] Incident clearly described with SAC classification rationale
- [ ] Investigation scope defined (what is included, what is excluded)
- [ ] Terms of Reference completed and endorsed
- [ ] Investigation team documented with roles
- [ ] Patient/family involvement offered and decision documented

## 2. Data Collection

- [ ] Timeline completed with multiple evidence sources cross-referenced
- [ ] All relevant clinical records reviewed
- [ ] All involved staff interviewed (individually, before group sessions)
- [ ] Relevant policies and procedures reviewed (version current at time of event)
- [ ] Equipment and environment inspected (where relevant)
- [ ] Previous incidents reviewed for patterns

## 3. Analysis Quality

- [ ] Analysis extends beyond "human error" to system factors
- [ ] All major contributing factor categories addressed (not just ones with obvious findings)
- [ ] Proximate and root causes distinguished
- [ ] Root causes identified (not just contributing factors)
- [ ] Just Culture assessment completed for individual actions
- [ ] Analysis is evidence-based (not speculative without caveat)

## 4. Action Plan Quality (RCA²)

- [ ] Every root cause has at least one action
- [ ] At least one strong or intermediate action per root cause
- [ ] Actions are specific and measurable (not "improve communication")
- [ ] Named owner and realistic timeline for each action
- [ ] Effectiveness review date specified for each action
- [ ] Risk register updated where relevant
- [ ] Clinical risk assessment skill cross-referenced for HIGH/EXTREME residual risks

## 5. Report Quality

- [ ] Report is clear and factual; avoids blame language
- [ ] Conclusions supported by evidence cited in the report
- [ ] Patient/family perspective included where obtained
- [ ] Confidentiality marking applied (CONFIDENTIAL: QUALITY IMPROVEMENT)
- [ ] Report de-identified appropriately
- [ ] Executive summary suitable for governance committee

## 6. Process Compliance (AU/NZ)

- [ ] Mandatory external notification assessed (ACSQHC/state health department for SAC 1)
- [ ] Open disclosure initiated and documented
- [ ] Timeframes met (SAC 1: investigation commenced within 5 business days)
- [ ] Clinical Governance Committee submission prepared
- [ ] Learning shared with relevant teams (de-identified)

## Red Flags — Do Not Submit if Any Apply

- [ ] Investigation stopped at "human error" without system analysis
- [ ] All recommendations are training/education only (no system-level actions)
- [ ] Contributing factors from only one level (e.g., only individual, no organizational)
- [ ] No involvement of frontline staff in investigation
- [ ] Investigation led by direct supervisor of involved staff without independent oversight
- [ ] No patient/family contact offered for SAC 1
```

**Step 6: Commit**

```bash
git add skills/rca-investigation/references/
git commit -m "feat: add supporting references (method selection, just culture, safety-ii, quality checklist)"
```

---

### Task 7: Mermaid Diagram Templates

**Files (12 .mmd files in `skills/rca-investigation/assets/templates/mermaid/`):**

**Step 1: Create all 12 Mermaid templates**

Create `fishbone-ishikawa.mmd`:
```
mindmap
  root((PROBLEM<br/>[State the adverse event]))
    PEOPLE
      Staff factors
        Training gap
        Fatigue/workload
        Knowledge deficit
      Patient factors
        Complexity
        Communication barrier
    EQUIPMENT
      Device failure
      Poor interface design
      Lookalike packaging
      Alarm fatigue
    PROCESS
      Policy absent or unclear
      Checklist not used
      Handover failure
      Escalation pathway unclear
    MATERIALS
      Medication similarity
      Labelling error
      Supply unavailability
    ENVIRONMENT
      Noise/distractions
      Lighting inadequate
      Staffing ratio
      Physical layout
    ORGANIZATION
      Culture
      Resources
      Governance gap
      Training system
```

Create `swiss-cheese-model.mmd`:
```
block-beta
  columns 6
  space H["HAZARD"]:1
  space:4
  space
  space L1["Layer 1\nDesign\n\n[Status: FAILED]\nGap: [describe]"]:1
  space:4
  space
  space L2["Layer 2\nPolicy &\nProcedure\n\n[Status: BYPASSED]\nGap: [describe]"]:1
  space:4
  space
  space L3["Layer 3\nTraining &\nCompetency\n\n[Status: ABSENT]\nGap: [describe]"]:1
  space:4
  space
  space L4["Layer 4\nSupervision\n\n[Status: FAILED]\nGap: [describe]"]:1
  space:4
  space
  space L5["Layer 5\nIndependent\nCheck\n\n[Status: BYPASSED]\nGap: [describe]"]:1
  space:4
  space
  space HARM["HARM\n[Patient outcome]"]:1

  H --> L1
  L1 --> L2
  L2 --> L3
  L3 --> L4
  L4 --> L5
  L5 --> HARM
```

Create `bow-tie-analysis.mmd`:
```
flowchart LR
  T1["Threat 1\n[e.g. Lookalike ampoules]"]
  T2["Threat 2\n[e.g. Distraction]"]
  T3["Threat 3\n[e.g. Policy gap]"]

  B1{{"Barrier 1\n[Double-check]\n✗ FAILED"}}
  B2{{"Barrier 2\n[Pharmacist verify]\n∅ ABSENT"}}
  B3{{"Barrier 3\n[CDS alert]\n✓ In place"}}

  EVENT(["TOP EVENT\n[e.g. Wrong medication administered]"])

  B4{{"Recovery Barrier 1\n[Rapid response]\n✓ In place"}}
  B5{{"Recovery Barrier 2\n[Antidote available]\n✗ FAILED"}}

  C1["Consequence 1\n[Adverse drug reaction]"]
  C2["Consequence 2\n[Therapeutic failure]"]

  T1 -->|prevented by| B1 --> EVENT
  T2 -->|prevented by| B2 --> EVENT
  T3 -->|stopped by| B3
  T3 --> EVENT

  EVENT -->|mitigated by| B4 --> C1
  EVENT -->|mitigated by| B5 --> C2

  style EVENT fill:#ff6b6b,color:#fff
  style B1 fill:#ffd93d
  style B2 fill:#ff6b6b,color:#fff
  style B5 fill:#ffd93d
```

Create `timeline-chronology.mmd`:
```
timeline
  title Investigation Timeline — [Event ID]
  section Pre-Event Context
    [Date -7d] : Background factor 1
               : Background factor 2
    [Date -1d] : Preceding event
  section Early Incident (Warning Signs)
    [Date T-4h] : First warning sign
                : Action taken or not taken
    [Date T-2h] : Second warning sign
                : Escalation attempt
  section Acute Phase
    [Date T-0] : Adverse event occurs
               : Immediate response
    [Date T+30m] : Escalation to senior
                 : Emergency intervention
  section Response and Recovery
    [Date T+2h] : Patient stable
               : Incident report filed
    [Date T+4h] : Family notified
               : Open disclosure initiated
  section Investigation
    [Date +1d] : Investigation team formed
    [Date +5d] : Evidence preserved, interviews begin
    [Date +4wk] : Investigation report drafted
```

Create `five-whys-chain.mmd`:
```
flowchart TD
  E["PROBLEM\n[State the adverse event or problem clearly]"]
  W1["WHY #1\n[Answer: immediate cause]"]
  W2["WHY #2\n[Answer: cause of cause]"]
  W3["WHY #3\n[Answer: deeper cause]"]
  W4["WHY #4\n[Answer: systemic factor]"]
  W5["WHY #5\n[Answer: root cause]"]
  RC(["ROOT CAUSE\n[System gap or failure]"])

  E -->|"Why did this happen?"| W1
  W1 -->|"Why?"| W2
  W2 -->|"Why?"| W3
  W3 -->|"Why?"| W4
  W4 -->|"Why?"| W5
  W5 --> RC

  style E fill:#ff6b6b,color:#fff
  style RC fill:#51cf66,color:#fff
```

Create `seips-work-system.mmd`:
```
block-beta
  columns 3

  block:ws["WORK SYSTEM"]:3
    P["PERSON(S)\n\nStaff:\n[Assessment]\n\nPatient:\n[Assessment]"]
    T["TASKS\n\n[Complexity]\n[Clarity]\n[Sequencing]\n[Demands]"]
    TT["TOOLS &\nTECHNOLOGY\n\n[Devices]\n[IT systems]\n[Medications]"]
    E["ENVIRONMENT\n\n[Physical]\n[Social]\n[Temporal]"]
    O["ORGANIZATION\n\n[Staffing]\n[Culture]\n[Governance]\n[Policies]"]
  end

  space:3

  PROC["PROCESSES\n(Care Delivery at Time of Event)\n[What was happening]"]

  space:3

  block:OUT["OUTCOMES"]:3
    PS["Patient Safety\nOutcome:\n[What happened]"]
    QO["Quality of Care\nOutcome:\n[Assessment]"]
    SW["Staff\nWellbeing:\n[Assessment]"]
  end

  ws --> PROC
  PROC --> OUT
```

Create `yorkshire-factors.mmd`:
```
mindmap
  root((ADVERSE EVENT\n[ID]))
    ACTIVE FAILURES
      Verification failure
        [Specific finding]
      Monitoring failure
        [Specific finding]
      Communication failure
        [Specific finding]
      Documentation failure
        [Specific finding]
    ERROR-PRODUCING CONDITIONS
      Task factors
        [Specific finding]
      Patient factors
        [Specific finding]
      Individual factors
        [Specific finding]
      Team factors
        [Specific finding]
      Physical environment
        [Specific finding]
      Equipment/supplies
        [Specific finding]
    LATENT CONDITIONS
      Staff management
        [Specific finding]
      Training/education
        [Specific finding]
      Policy/procedures
        [Specific finding]
      Barriers/defences
        [Specific finding]
    CONTEXT FACTORS
      Organizational culture
        [Specific finding]
      External context
        [Specific finding]
```

Create `accimap-levels.mmd`:
```
flowchart TD
  subgraph L6["Level 6: Government & Policy"]
    G1["[Government/regulatory factor 1]"]
    G2["[Funding/policy factor 2]"]
  end

  subgraph L5["Level 5: Regulatory Bodies"]
    R1["[Standards/accreditation factor]"]
    R2["[Professional body factor]"]
  end

  subgraph L4["Level 4: Hospital Management"]
    M1["[Executive decision/resource factor]"]
    M2["[Organizational culture factor]"]
  end

  subgraph L3["Level 3: Physical/Technical Environment"]
    T1["[Equipment/system factor]"]
    T2["[Physical environment factor]"]
  end

  subgraph L2["Level 2: Staff / Operators"]
    S1["[Staff action/decision 1]"]
    S2["[Staff action/decision 2]"]
  end

  subgraph L1["Level 1: Patient / Activity"]
    E["ADVERSE EVENT\n[Description]"]
  end

  G1 --> R1
  G2 --> M1
  R1 --> M1
  R2 --> M2
  M1 --> T1
  M2 --> S1
  T1 --> S1
  T2 --> S2
  S1 --> E
  S2 --> E
```

Create `hfacs-layers.mmd`:
```
block-beta
  columns 1

  block:L4["Level 4: Organizational Influences"]
    columns 3
    RM["Resource Management\n\n[Staffing, equipment,\nfinancial]"]
    OC["Organizational\nClimate\n\n[Culture, command\nstructure]"]
    OP["Organizational\nProcess\n\n[Operations, oversight,\nincentives]"]
  end

  block:L3["Level 3: Unsafe Supervision"]
    columns 4
    IS["Inadequate\nSupervisor\n\n[Finding]"]
    PIO["Planned\nInappropriate Ops\n\n[Finding]"]
    FCP["Failed to Correct\nKnown Problem\n\n[Finding]"]
    SV["Supervisory\nViolation\n\n[Finding]"]
  end

  block:L2["Level 2: Preconditions"]
    columns 3
    EF["Environmental\nFactors\n\n[Physical/tech\nenvironment finding]"]
    CO["Condition of\nOperators\n\n[Mental/physical\nstate finding]"]
    PF["Personnel\nFactors\n\n[CRM / readiness\nfinding]"]
  end

  block:L1["Level 1: Unsafe Acts"]
    columns 2
    ER["Errors\n\nSkill-based: [finding]\nDecision: [finding]\nPerceptual: [finding]"]
    VIO["Violations\n\nRoutine: [finding]\nExceptional: [finding]"]
  end

  L4 --> L3 --> L2 --> L1
```

Create `stamp-control-structure.mmd`:
```
flowchart TD
  GOV["Government / Regulators\nSafety constraints: [list]"]
  EXEC["Hospital Executive\nControl actions: [policies, resources]\nFeedback: [audit, incident reports]"]
  MGR["Department Management\nControl actions: [staffing, protocols]\nFeedback: [ward reports, incidents]"]
  SUPER["Clinical Supervisor\nControl actions: [direction, oversight]\nFeedback: [observation, rounds]"]
  STAFF["Clinical Staff\nControl actions: [care delivery decisions]\nFeedback: [patient signs, monitoring]"]
  PATIENT["Patient Care Process\n[The controlled process]"]

  GOV -->|"Legislation, funding"| EXEC
  EXEC -->|"Policy, resources"| MGR
  MGR -->|"Protocols, staffing"| SUPER
  SUPER -->|"Supervision, guidance"| STAFF
  STAFF -->|"Clinical interventions"| PATIENT

  PATIENT -->|"Patient outcomes (feedback)"| STAFF
  STAFF -->|"Escalation, handover (feedback)"| SUPER
  SUPER -->|"Reports, incidents (feedback)"| MGR
  MGR -->|"Performance data (feedback)"| EXEC

  style PATIENT fill:#ff6b6b,color:#fff

  note1["UNSAFE CONTROL ACTIONS IDENTIFIED:\n1. [UCA description]\n2. [UCA description]"]
```

Create `investigation-workflow.mmd`:
```
flowchart TD
  INC["Incident Occurs\nor is Reported"]
  SAC{"SAC\nClassification"}

  SAC -->|"SAC 1-2"| TRIAGE["RCA Triage Agent\nClassify, scope, method selection,\nTeam composition, ToR"]
  SAC -->|"SAC 3-4"| RAPID["Rapid Review\n5 Whys + Contributing Factors\n48h - 2 weeks"]

  TRIAGE --> PRESERVE["Preserve Evidence\nRecords, equipment, CCTV"]
  PRESERVE --> TIMELINE["Build Timeline\nMulti-source chronology"]
  TIMELINE --> CF["Contributing Factor Analysis\nYorkshire / London Protocol / HFACS"]
  CF --> SYSTEMS["Systems Analysis\nSEIPS / Swiss Cheese / AcciMap"]
  SYSTEMS --> BOWTIE["Barrier Analysis\nBow-Tie / Barrier Analysis"]
  BOWTIE --> JUST["Just Culture Assessment\nHuman error / At-risk / Reckless"]

  JUST --> REPORT["RCA Report Agent\nDraft investigation report\nMermaid diagrams, DOCX, PPTX"]

  REPORT --> REVIEW{"Governance\nReview"}
  REVIEW -->|"Revise"| REPORT
  REVIEW -->|"Accepted"| TRACK["RCA Track Agent\nCAPA Action Plan\nQI linkage, monitoring"]

  TRACK --> EFFECT["Effectiveness Review\n3, 6, 12 months"]
  EFFECT -->|"Actions effective"| CLOSE["Investigation Closure"]
  EFFECT -->|"Further action needed"| TRACK

  RAPID --> CLOSE

  style INC fill:#ff6b6b,color:#fff
  style CLOSE fill:#51cf66,color:#fff
```

Create `fmea-priority-quadrant.mmd`:
```
quadrantChart
  title FMEA Risk Priority — Severity vs Occurrence
  x-axis Low Severity --> High Severity
  y-axis Low Occurrence --> High Occurrence
  quadrant-1 High Priority — Redesign Required
  quadrant-2 Monitor — Frequency Reduction Needed
  quadrant-3 Low Priority — Accept and Monitor
  quadrant-4 Critical — Immediate Action if Undetectable
  [Failure Mode 1]: [0.8, 0.9]
  [Failure Mode 2]: [0.5, 0.6]
  [Failure Mode 3]: [0.3, 0.2]
  [Failure Mode 4]: [0.7, 0.3]
```

**Step 2: Commit**

```bash
git add skills/rca-investigation/assets/templates/mermaid/
git commit -m "feat: add all 12 Mermaid diagram templates"
```

---

### Task 8: Markdown Working Document Templates

**Files (14 in `skills/rca-investigation/assets/templates/markdown/`):**

**Step 1: Create templates 01-07 (investigation working documents)**

These templates are working documents for the investigation team. Each uses `[PLACEHOLDER]` for values to be populated. See the design doc for full content structure. Key templates:

`01-investigation-tor.md` — Terms of Reference with: Incident ID, SAC level, scope, out-of-scope, team composition table, methodology, timeline, reporting requirements, governance authority, confidentiality statement.

`02-chronology.md` — Chronology table with five phases (Pre-event, Early incident, Acute phase, Response/escalation, Post-event), columns for datetime, event, source, significance, and annotation flags for warning signs, decision points, and barrier failures.

`03-contributing-factors.md` — Yorkshire Framework analysis table with all 14 factor categories, columns for finding, evidence source, confirmed/possible, and significance.

`04-fishbone-diagram.md` — Structured fishbone with all six categories (People, Equipment, Process, Materials, Environment, Organization), each with sub-cause bullets and evidence column.

`05-fmea-worksheet.md` — FMEA table with process steps, failure modes, effects, S/O/D scores, RPN, action, owner, and target date.

`06-barrier-analysis.md` — Barrier inventory table with type, present/absent, functioning, failure mode, and recommendation.

`07-bow-tie-analysis.md` — Bow-tie with threats/preventive barriers/event/recovery barriers/consequences in structured table format.

**Step 2: Create templates 08-14 (reports and governance documents)**

`08-rca-investigation-report.md` — Full investigation report with 10 sections: Cover page, Executive summary, Background/context, Investigation process, Chronology, Contributing factor analysis, Root cause analysis, Recommendations, Action plan summary, Appendices.

`09-sae-review-report.md` — SAE-specific format including SAC classification rationale, immediate actions taken, mandatory notification assessment, open disclosure record.

`10-executive-summary.md` — 2-page maximum with: What happened (3 bullets), What we found (3 bullets), Risk level, Key recommendations (3 bullets), Immediate actions taken, Monitoring plan.

`11-capa-action-plan.md` — CAPA table with: Action, Root cause addressed, Action type (strong/intermediate/weak), Owner, Deadline, Progress status, Effectiveness measure, Review date.

`12-open-disclosure-plan.md` — Open disclosure with: Patient/family contact record, What was disclosed, Questions raised, Support offered, Follow-up plan, Translator requirements.

`13-investigation-closure.md` — Closure report with: Summary, Actions completed evidence, Residual risk assessment, Lessons learned, Learning dissemination record, Governance endorsement.

`14-just-culture-assessment.md` — Just Culture decision tree applied to each involved individual, with classification (human error/at-risk/reckless) and recommended response.

**Step 3: Commit**

```bash
git add skills/rca-investigation/assets/templates/markdown/
git commit -m "feat: add all 14 markdown working document templates"
```

---

### Task 9: DOCX Template Generation Instructions

**Files (7 in `skills/rca-investigation/assets/templates/docx/`):**

Each DOCX template file is a markdown document that tells Claude how to generate a properly formatted Word document using the document-skills:docx skill.

**Step 1: Create style guide `skills/rca-investigation/assets/styles/docx-style-guide.md`**

```markdown
# DOCX Style Guide — Healthcare RCA Documents

## Document Identity
- Organization name: [Health Service Name] — replace all instances
- Logo: Insert at top right of cover page
- Confidentiality: All documents marked "CONFIDENTIAL: QUALITY IMPROVEMENT" in header/footer
- Version control: Version number and date in footer

## Typography
- Body text: Calibri 11pt
- Heading 1: Calibri Bold 16pt, Dark Blue (#1F3864)
- Heading 2: Calibri Bold 13pt, Medium Blue (#2E75B6)
- Heading 3: Calibri Bold 11pt, Light Blue (#5A96D2)
- Table headers: Calibri Bold 10pt, White text on Dark Blue (#1F3864) background
- Table body: Calibri 10pt

## Layout
- Margins: 2.5cm all sides
- Page size: A4
- Header: Document title left, Organization right
- Footer: "CONFIDENTIAL: QUALITY IMPROVEMENT" left, Page number right, Date center

## Tables
- All tables use "Table Grid" style with header row shading
- Alternating row shading: Light Blue (#DEEAF1) every second row
- Column widths specified per template

## Status Indicators (for CAPA tables)
- Not started: Grey background
- In progress: Yellow (#FFF2CC) background
- Complete: Green (#E2EFDA) background
- Overdue: Red (#FCE4D6) background

## Risk Level Colours (for risk matrices)
- LOW: Green (#70AD47)
- MEDIUM: Yellow (#FFD966)
- HIGH: Orange (#ED7D31)
- EXTREME: Red (#FF0000)
```

**Step 2: Create each DOCX template instruction file**

Each file specifies the document structure for generation via `document-skills:docx`. Example structure for `rca-investigation-report.md`:

```markdown
# DOCX Generation: RCA Investigation Report

Use document-skills:docx skill to generate this document.
Apply styles from assets/styles/docx-style-guide.md.

## Cover Page
- Title: "Root Cause Analysis Investigation Report"
- Subtitle: "[Event description — de-identified]"
- Incident ID: [ID]
- Investigation Period: [Start] to [End]
- Classification: CONFIDENTIAL: QUALITY IMPROVEMENT
- Version: [X.X]
- Date: [Date]
- Approved by: [Clinical Governance Committee]

## Sections (Heading 1 for each)
1. Executive Summary (max 1 page)
2. Background and Context
3. Investigation Process
4. Chronology of Events
5. Contributing Factor Analysis
6. Root Cause Analysis
7. Findings and Recommendations
8. Action Plan
9. Monitoring and Effectiveness Review
10. Appendices

## Tables Required
- Investigation team composition (Section 3)
- Contributing factors (Section 5) — Yorkshire Framework format
- Root causes (Section 6)
- Recommendations (Section 7)
- CAPA Action Plan (Section 8) — with status colours

## Special Formatting
- SAC level displayed as coloured badge (RED for SAC 1, ORANGE for SAC 2)
- Risk ratings in cells with appropriate colour fill
- Mermaid diagrams: insert as PNG exports from .mmd templates
```

**Step 3: Commit**

```bash
git add skills/rca-investigation/assets/templates/docx/
git add skills/rca-investigation/assets/styles/docx-style-guide.md
git commit -m "feat: add DOCX template generation instructions and style guide"
```

---

### Task 10: PPTX Template Generation Instructions

**Files (3 in `skills/rca-investigation/assets/templates/pptx/` + style guide):**

**Step 1: Create `skills/rca-investigation/assets/styles/pptx-style-guide.md`**

```markdown
# PPTX Style Guide — Healthcare RCA Presentations

## Theme
- Background: White (#FFFFFF)
- Primary: Dark Blue (#1F3864)
- Accent 1: Medium Blue (#2E75B6)
- Accent 2: Teal (#008B8B)
- Warning: Orange (#ED7D31)
- Critical: Red (#C00000)
- Success: Green (#70AD47)

## Title Slide
- Full-width dark blue bar at top (40% of slide height)
- White title text: Calibri Bold 40pt
- Subtitle: Calibri 24pt, white
- Confidentiality badge: "CONFIDENTIAL" in red rounded rectangle

## Section Slides (Divider)
- Dark blue background, white text
- Section number left, section title right

## Content Slides
- Heading: Calibri Bold 28pt, dark blue
- Body text: Calibri 18pt (max 5 bullet points per slide)
- Footer: Organization name left, date right, slide number right

## Special Slide Types
- Timeline: Horizontal arrow with milestone markers
- Risk matrix: Colour-coded 5x5 grid
- Findings: Card-style layout (3 cards per slide)
- Recommendations: Numbered list with action strength indicator
- Action plan: Summary table with RAG status colours

## Confidentiality
Every slide footer includes "CONFIDENTIAL: QUALITY IMPROVEMENT"
```

**Step 2: Create the three PPTX template files**

`governance-committee-brief.md`:
```
Slide structure (12-15 slides):
1. Title slide: "RCA Investigation — [Event ID] — Governance Committee Brief"
2. Agenda (4 items)
3. What happened — 3 bullet facts, SAC badge
4. Investigation process overview — Mermaid workflow diagram
5. Timeline — Mermaid timeline diagram
6. Contributing factors — Yorkshire Framework summary (top 5)
7. Systems analysis — SEIPS or Swiss Cheese diagram
8. Root causes identified (max 3 per slide)
9. Barrier failures — Bow-Tie diagram
10. Just Culture findings
11. Recommendations — with action strength indicators
12. Action plan summary — RAG table
13. Monitoring plan
14. Questions
```

`learning-presentation.md`:
```
Slide structure (8-10 slides):
1. Title: "Learning from [de-identified event description]"
2. Our patient — de-identified case summary
3. What happened — factual timeline (simplified)
4. What we found — top 3 contributing factors
5. The system picture — simplified Fishbone or Yorkshire
6. What we're changing — specific actions (strong/intermediate)
7. How this affects your practice
8. Questions and discussion
```

`executive-summary-deck.md`:
```
Slide structure (6 slides):
1. Title + SAC badge
2. Key message (single slide, large font): what happened and why it matters
3. Risk level: 5x5 matrix with position marked
4. Critical findings (3 max, card layout)
5. Actions: what we're doing and by when
6. Monitoring: how we'll know it's working
```

**Step 3: Commit**

```bash
git add skills/rca-investigation/assets/templates/pptx/
git add skills/rca-investigation/assets/styles/pptx-style-guide.md
git commit -m "feat: add PPTX template generation instructions and style guide"
```

---

### Task 11: Four Specialized Agents

**Files:**
- Create: `agents/rca-triage.md`
- Create: `agents/rca-investigate.md`
- Create: `agents/rca-report.md`
- Create: `agents/rca-track.md`

**Step 1: Create `agents/rca-triage.md`**

```markdown
---
name: rca-triage
description: >
  Healthcare incident triage and investigation scoping agent. Use when: classifying the severity
  of a clinical incident (SAC 1-4); determining whether a formal RCA is required; selecting the
  appropriate investigation method(s) and team composition; drafting Terms of Reference; or
  assessing mandatory notification requirements under AU/NZ health legislation.
  Triggers automatically from health-incident-reporting for SAC 1-2 events.
---

# RCA Triage Agent

## Purpose
Classify incidents, determine investigation level and methodology, initiate the investigation.

## Step 1: SAC Classification

Apply the AU/NZ SAC severity classification:

| SAC | Descriptor | Examples |
|---|---|---|
| 1 | Death or serious harm attributable to healthcare | Surgical wrong-site, medication-related death, suicide in inpatient unit |
| 2 | Moderate harm; significant temporary harm | Unplanned readmission with harm, delayed diagnosis causing harm |
| 3 | Minor harm; additional treatment required | Minor medication error caught before significant harm |
| 4 | Near miss; no harm | Medication error caught before administration |

Ask: What was the actual or potential patient outcome? Was harm caused? Was it serious?

## Step 2: Mandatory Notification Check (AU/NZ)

SAC 1 events may require notification to:
- State/Territory health department (usually within 24-48 hours)
- ACSQHC (for sentinel events matching the national sentinel event list)
- AHPRA (if practitioner impairment or misconduct suspected)
- Coroner (if death — mandatory in most jurisdictions)
- Police (if suspected criminal act)

Check state-specific requirements. Generate notification checklist as part of triage output.

## Step 3: Investigation Level Decision

| SAC | Required Response | Timeline |
|---|---|---|
| 1 | Comprehensive RCA — full investigation team, multi-method | 8-12 weeks |
| 2 | Standard RCA — formal investigation team, structured methods | 4-6 weeks |
| 3 | Concise investigation — small team or quality manager | 1-2 weeks |
| 4 | Local review — service-level manager or quality lead | 48h-1 week |

## Step 4: Method Selection

Use `references/method-selection-matrix.md` and `references/method-combination-guide.md`.
Apply the decision questions from the matrix to the specific event.
Output: Recommended primary methods + secondary methods based on event characteristics.

## Step 5: Team Composition

Recommend team composition based on SAC level:

SAC 1: Team leader (independent) + Clinical lead (relevant specialty) + Quality/Safety professional + Frontline staff (involved service) + Patient/family representative (offered) + Human factors expert (optional) + External investigator (complex events)

SAC 2: Team leader + Clinical lead + Quality/Safety professional + Frontline staff

SAC 3: Quality manager or senior clinician + relevant service representative

## Step 6: Generate Terms of Reference

Use template `assets/templates/markdown/01-investigation-tor.md`
Populate: Incident ID, SAC level, scope, team, methodology, timeline, governance authority.

## Output Checklist
- [ ] SAC classification with rationale
- [ ] Mandatory notification assessment
- [ ] Investigation level and timeline
- [ ] Recommended methods
- [ ] Recommended team composition
- [ ] Terms of Reference (draft)
- [ ] Evidence preservation checklist
- [ ] Open disclosure initiation prompt (SAC 1-2)
```

**Step 2: Create `agents/rca-investigate.md`**

```markdown
---
name: rca-investigate
description: >
  Healthcare RCA investigation execution agent. Use when: actively conducting an RCA or SAE
  investigation; needing guided prompts for a specific analysis method (Fishbone, 5 Whys,
  Yorkshire Framework, SEIPS, Swiss Cheese, Bow-Tie, Barrier Analysis, FMEA, Timeline, HFACS,
  London Protocol, AcciMap, STAMP/STPA); reviewing investigation completeness; or facilitating
  a multidisciplinary investigation team meeting.
---

# RCA Investigate Agent

## Purpose
Guide the investigation team through structured analysis using the methods selected at triage.

## Step 1: Confirm Investigation Foundations

Before beginning analysis, confirm:
- [ ] Terms of Reference completed (template 01)
- [ ] Evidence preserved (records, equipment, environment)
- [ ] Individual staff interviews scheduled (before group sessions)
- [ ] Timeline started with factual events from records

## Step 2: Build the Timeline

Always start here. Use `references/methods/timeline-analysis.md` and template 02.
Ask the team:
- "What do we know happened, and when, from the records alone?"
- "What are the gaps or discrepancies between sources?"
- "Where are the decision points and warning signs?"

## Step 3: Execute Primary Analysis Method(s)

Load the reference file for each method selected at triage.
For each method, provide structured prompts:

**If Yorkshire Framework (template 03)**:
Work through each of the 14 factor categories with the team.
For each: "Do we have evidence this was a contributing factor? What specifically?"

**If SEIPS (no dedicated template — use guided questions)**:
For each work system component, ask the analysis questions from `references/methods/seips.md`.

**If London Protocol**:
Start with: "What were the specific care management problems — not the outcome, but what went wrong in the care itself?"
Then work through each of the seven factor categories.

**If 5 Whys (template — use fishbone as complement)**:
State the problem clearly, then iterate through each "why" with the team.
Challenge shallow answers: "Is that actually the root cause, or can we go deeper?"

**If Bow-Tie (template 07)**:
Start from the confirmed timeline and contributing factors.
"What were the threats that led to this event? Which barriers should have stopped each threat? Which failed or were absent?"

## Step 4: Completeness Check

Before closing the analysis phase, apply the Investigation Quality Checklist:
`references/investigation-quality-checklist.md`

Check specifically:
- Does the analysis go beyond individual human error to system factors?
- Are all major contributing factor categories addressed?
- Have both proximate and root causes been identified?

## Step 5: Just Culture Assessment

For each individual whose actions are part of the event, apply the Just Culture decision tree:
`references/just-culture-guide.md`
Document findings in template 14.

## Step 6: Apply Safety-II Lens (recommended for SAC 1-2)

Use `references/safety-ii-principles.md` questions:
- "How does this process usually go right? What's different about this occasion?"
- "What informal safety practices usually protect against this? Were they absent or overwhelmed?"

## Output
- Completed working templates (02-07, 14 as applicable)
- Summary of: proximate cause(s), root cause(s), contributing factors, barrier failures
- Ready to hand to rca-report agent
```

**Step 3: Create `agents/rca-report.md`**

```markdown
---
name: rca-report
description: >
  Healthcare RCA report generation agent. Use when: generating an RCA or SAE investigation
  report; creating Mermaid diagrams for investigation findings; producing DOCX governance
  documents; creating PPTX presentations for governance committees or staff learning;
  drafting executive summaries; or preparing open disclosure documentation.
---

# RCA Report Agent

## Purpose
Transform completed investigation analysis into governance-ready reports, diagrams, and presentations.

## Step 1: Verify Analysis Completeness

Confirm you have:
- [ ] Completed chronology (template 02)
- [ ] Contributing factor analysis (template 03 and/or applicable templates)
- [ ] Root causes identified
- [ ] Just Culture findings (template 14)
- [ ] Recommendations drafted
- [ ] CAPA actions drafted

If any are missing, route back to rca-investigate agent.

## Step 2: Generate Mermaid Diagrams

Select and populate the appropriate diagram templates from `assets/templates/mermaid/`:

Always for SAC 1-2:
- `timeline-chronology.mmd` — populate with actual timeline data
- `yorkshire-factors.mmd` or `fishbone-ishikawa.mmd` — populate with confirmed contributing factors

Additional based on methods used:
- `bow-tie-analysis.mmd` — if Bow-Tie analysis performed
- `swiss-cheese-model.mmd` — if Swiss Cheese analysis performed
- `seips-work-system.mmd` — if SEIPS analysis performed
- `accimap-levels.mmd` — if AcciMap analysis performed
- `hfacs-layers.mmd` — if HFACS analysis performed
- `investigation-workflow.mmd` — always include in report appendix

For each diagram: replace all `[placeholder]` values with actual findings.

## Step 3: Generate Investigation Report

Use template `assets/templates/markdown/08-rca-investigation-report.md` (or 09 for SAE).
Populate all sections with investigation findings.
Apply DOCX instructions from `assets/templates/docx/rca-investigation-report.md`
using document-skills:docx skill.

Language guidance:
- Use factual, non-blame language ("the medication was not verified" not "the nurse failed to verify")
- Distinguish confirmed findings from hypotheses ("the evidence indicates..." vs. "it is possible that...")
- All patient references de-identified
- All staff references de-identified or by role only unless individual accountability finding requires naming

## Step 4: Generate Executive Summary

Use template `assets/templates/markdown/10-executive-summary.md`
Maximum 2 pages / 6 slides. Key messages: what, why it matters, what we're doing.

## Step 5: Generate Governance Presentation (if required)

Use `assets/templates/pptx/governance-committee-brief.md` with document-skills:pptx skill.
Insert populated Mermaid diagram images.

## Step 6: Generate Learning Presentation (if required)

Use `assets/templates/pptx/learning-presentation.md`
De-identify to maximum extent — this will be shared with staff.

## Step 7: Open Disclosure Documentation (SAC 1-2)

Use template `assets/templates/markdown/12-open-disclosure-plan.md`
Ensure this is completed before or in parallel with the investigation report.

## Output
- Populated Mermaid diagram files
- Markdown investigation report (populated template)
- DOCX governance report
- PPTX governance presentation (if requested)
- PPTX learning presentation (if requested)
- Executive summary
```

**Step 4: Create `agents/rca-track.md`**

```markdown
---
name: rca-track
description: >
  Healthcare RCA action tracking and quality improvement agent. Use when: generating a CAPA
  (Corrective and Preventive Action) plan from RCA recommendations; linking investigation
  findings to quality improvement (PDSA cycles); monitoring action implementation; scheduling
  effectiveness reviews; closing a completed investigation; or escalating systemic findings to
  enterprise risk or health-enterprise-risk-assessment skill.
---

# RCA Track Agent

## Purpose
Convert investigation recommendations into implemented, verified improvements.

## Step 1: CAPA Action Plan Generation

Use template `assets/templates/markdown/11-capa-action-plan.md`.

For each recommendation from the investigation:
1. State the action specifically and measurably (not "improve communication" — "implement structured ISBAR handover tool in [ward] by [date]")
2. Classify action strength (Strong/Intermediate/Weak per RCA² hierarchy)
3. Assign named owner and realistic deadline
4. Define the effectiveness measure: "How will we know this action has worked?"
5. Schedule effectiveness review date (typically 3, 6, 12 months post-implementation)

**Rule**: Every root cause must have at least one action. Every action must have an owner and deadline.

## Step 2: Risk Register Update

For any finding that represents an ongoing risk:
Cross-reference with health-clinical-risk-assessment skill.
Create or update risk register entry for:
- Risks that persist during the action implementation period
- Systemic risks identified that extend beyond this single event
- Residual risks that remain after all actions are implemented

## Step 3: QI Linkage

For actions requiring sustained improvement:
Cross-reference with health-quality-improvement skill.
Identify whether PDSA cycles are appropriate for:
- Process changes requiring testing and refinement
- Culture change initiatives requiring iterative improvement
- Training programs requiring evaluation

## Step 4: Enterprise Risk Escalation

Escalate to health-enterprise-risk-assessment skill when findings indicate:
- Systemic risk affecting multiple services or sites
- Organizational or governance failures at executive level
- Regulatory or external context factors at AcciMap Levels 5-6
- Events revealing a pattern across multiple incidents

## Step 5: Monitoring Schedule

Establish regular review cadence:
| Timeline | Action |
|---|---|
| 2 weeks post-acceptance | Confirm all actions commenced; early barriers identified |
| 3 months | First effectiveness review; evidence of implementation |
| 6 months | Mid-point review; assess whether improvements are sustained |
| 12 months | Final effectiveness review; investigation closure recommendation |

## Step 6: Investigation Closure

When all actions are implemented and effectiveness verified:
Use template `assets/templates/markdown/13-investigation-closure.md`
Populate: actions completed with evidence, residual risk level, lessons learned, learning dissemination record.
Submit for Clinical Governance Committee endorsement.

## Step 7: Learning Dissemination

Ensure investigation learning is shared:
- De-identified case summary to relevant clinical teams
- Learning themes to quality committee for pattern analysis
- Policy/procedure updates communicated to all affected staff
- Training updates with competency verification scheduled

## Output
- CAPA Action Plan (populated template 11)
- Risk register updates (cross-reference health-clinical-risk-assessment)
- QI project brief (if PDSA indicated)
- Monitoring schedule
- Investigation Closure report (when complete)
```

**Step 5: Commit**

```bash
git add agents/
git commit -m "feat: add four specialized agents (triage, investigate, report, track)"
```

---

### Task 12: Final Review and Polish

**Step 1: Verify all files exist**

```bash
find . -name "*.md" -o -name "*.mmd" | sort
```

Expected: ~60 files total.

**Step 2: Read SKILL.md and verify the template index is accurate**

Check that every file referenced in the SKILL.md template index actually exists.

**Step 3: Run a final quality pass**

Check:
- All `[PLACEHOLDER]` values in templates use consistent bracketing
- All Mermaid templates have valid syntax (no unclosed brackets, valid diagram types)
- All agent files have valid YAML frontmatter with name and description
- SKILL.md frontmatter description is comprehensive enough to trigger reliably

**Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete RCA & SAE Investigation Skill Suite v1.0"
```

---

## Execution Options

Plan complete and saved to `docs/plans/2026-02-25-rca-skill-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (this session)** — Dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** — Open a new session with executing-plans skill, batch execution with checkpoints

Which approach would you prefer?
