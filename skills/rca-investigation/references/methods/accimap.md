# AcciMap — Accident Mapping

AcciMap (Rasmussen & Svedung, 2000) is a systems-thinking accident analysis method that maps causal factors across multiple levels of a sociotechnical system. Unlike linear methods that trace a single causal chain, AcciMap reveals the network of decisions and conditions at every level that contributed to the accident.

## Levels of Analysis

AcciMap organises factors into six levels:

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
LEVEL 6 (Government/Policy): [Factor A] --> [Factor B]
                                   ↓              ↓
LEVEL 5 (Regulators):        [Factor C] <-- [Factor D]
                                   ↓
LEVEL 4 (Management):        [Factor E] --> [Factor F]
                                                  ↓
LEVEL 3 (Technical/Environment): [Factor G]
                                          ↓
LEVEL 2 (Staff):              [Action H] --> [Action I]
                                                  ↓
LEVEL 1 (Patient/Event):           [ADVERSE EVENT]
```

## When to Use AcciMap

AcciMap is most powerful for:
- Complex, multi-factorial events with organisational and regulatory contributing factors
- Events that reveal systemic issues requiring change at multiple levels
- Situations where traditional RCA would focus only on the "sharp end" (staff) and miss the blunt end (organisation, policy)
- Healthcare system redesign and policy development

## Key Output for Governance

AcciMap explicitly shows governance bodies which level they are responsible for:
- Clinical Governance Committee: Level 3–4 factors
- Executive/CEO: Level 4–5 factors
- Regulatory reporting: Level 5–6 factors

## Mermaid Diagram

Use template `assets/templates/mermaid/accimap-levels.mmd`
