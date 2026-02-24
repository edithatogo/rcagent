# Swiss Cheese Model (Reason's Model of Organisational Accidents)

James Reason's Swiss Cheese Model (1990, updated 2000) describes how adverse events occur when holes in multiple defensive layers align, allowing a hazard trajectory to reach and harm a patient.

## Core Concept

Each layer of defence (a "slice of cheese") has holes — gaps in protection caused by active failures and latent conditions. Normally, holes in different layers are misaligned and the hazard is stopped. An adverse event occurs when holes align across all layers simultaneously.

```
Hazard → [Layer 1] → [Layer 2] → [Layer 3] → [Layer 4] → HARM
         (policy)   (training)  (supervision) (checking)

When holes align:
Hazard → ○ hole → ○ hole → ○ hole → ○ hole → HARM
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
