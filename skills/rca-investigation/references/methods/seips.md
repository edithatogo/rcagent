# SEIPS 3.0 — Systems Engineering Initiative for Patient Safety

SEIPS (Systems Engineering Initiative for Patient Safety) is a work system model that analyses healthcare as a system of interacting components. SEIPS 3.0 (2020) is the current version and the most SOTA framework for understanding how work system design leads to (or prevents) adverse events.

## The SEIPS Work System Model

SEIPS frames adverse events as emerging from the interaction of five work system components during processes of care, producing health outcomes for patients and workers.

```
WORK SYSTEM COMPONENTS
┌──────────────────────────────────────────────────────────────────┐
│  PERSON(S) ←→ TASKS ←→ TOOLS & TECHNOLOGY                       │
│                    ↕                                              │
│          ENVIRONMENT ←→ ORGANISATION                             │
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

### Organisation
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
| Organisation | | | |
```

## When to Use SEIPS

SEIPS is particularly powerful for:
- Technology-related adverse events (EMR, device failures, alarm fatigue)
- Events involving complex patient populations (elderly, ICU, mental health)
- Events where the work system design enabled rather than prevented harm
- New service design and risk assessment (proactive SEIPS analysis)

## Mermaid Diagram

Use template `assets/templates/mermaid/seips-work-system.mmd`
