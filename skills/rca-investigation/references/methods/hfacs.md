# HFACS — Human Factors Analysis and Classification System

HFACS was developed from James Reason's Swiss Cheese Model and originally applied in aviation accident investigation (US military). It provides a structured taxonomy of human error and organisational factors across four levels.

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

### Level 4: Organisational Influences

- **Resource management**: Human resources (staffing, selection, training), monetary resources, equipment resources
- **Organisational climate**: Culture, policies, command structure, values
- **Organisational process**: Operations, procedures, oversight, incentives

## HFACS Classification Process

1. Review the timeline and contributing factor analysis
2. For each identified human action (or inaction), classify using the Level 1 taxonomy
3. For each Level 1 classification, trace back through Levels 2, 3, and 4 to identify enabling factors
4. This creates a structured causal chain from organisational influences down to the unsafe act

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
- You want to trace individual actions back to organisational system failures

**Important**: HFACS classifies errors for analysis — it does not assign blame. Use alongside Just Culture framework to ensure fair treatment of individuals.
