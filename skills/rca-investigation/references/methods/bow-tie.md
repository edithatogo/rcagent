# Bow-Tie Analysis

Bow-Tie Analysis maps the relationship between threats (left side), a central hazardous event, and consequences (right side), with barriers on each side. It provides a visual, comprehensive picture of risk controls and their adequacy.

## Structure

```
THREATS          BARRIERS          EVENT          BARRIERS          CONSEQUENCES
(causes)        (preventive)    (top event)      (recovery)          (outcomes)

Threat 1 --[B1]--> ╮
Threat 2 --[B2]--> ╮--> EVENT -->[B4]--> Consequence 1
Threat 3 --[B3]--> ╯             [B5]--> Consequence 2
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
