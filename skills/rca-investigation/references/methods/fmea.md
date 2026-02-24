# Failure Mode and Effects Analysis (FMEA)

FMEA is a proactive risk assessment tool that identifies potential failure modes in a process BEFORE they cause harm. In healthcare, FMEA is used to analyse new services, high-risk processes, and proposed changes to clinical pathways.

## FMEA vs. RCA

| | FMEA | RCA |
|---|---|---|
| Timing | Proactive — before harm occurs | Reactive — after harm occurs |
| Purpose | Prevent failures before they happen | Understand and prevent recurrence |
| Starting point | Process steps | Adverse event |
| Output | Risk priority scores + prevention actions | Root causes + corrective actions |

## Process Steps

### Step 1: Define the Process
Map every step in the process being analysed.
Example process: "Administration of high-alert medication"
Steps: Prescribe → Verify → Dispense → Prepare → Administer → Monitor

### Step 2: Identify Failure Modes
For each step, ask: "In what ways could this step fail?"
List every possible failure mode.

### Step 3: Identify Effects
For each failure mode: "What is the effect on the patient if this failure occurs?"

### Step 4: Score Each Failure Mode
Score three dimensions on 1–10 scale:

**Severity (S)**: How serious is the effect on the patient?
1–2 = Negligible | 3–4 = Minor | 5–6 = Moderate | 7–8 = Major | 9–10 = Catastrophic

**Occurrence (O)**: How often does this failure mode occur?
1–2 = Almost never | 3–4 = Rare | 5–6 = Occasional | 7–8 = Frequent | 9–10 = Almost certain

**Detectability (D)**: How likely is detection before harm reaches the patient?
1–2 = Almost certain to detect | 5–6 = Moderate | 9–10 = Almost impossible to detect

**Risk Priority Number (RPN) = S × O × D**

### Step 5: Prioritise
- RPN > 200: Critical — immediate action required
- RPN 100–200: High — urgent action required
- RPN 50–99: Medium — action plan required
- RPN < 50: Low — monitor

Note: Any failure mode with Severity ≥ 9 requires action regardless of RPN.

### Step 6: Develop Actions
For each high/critical failure mode:
- What control prevents the failure from occurring? (reduce O)
- What detection mechanism catches the failure before harm? (reduce D)
- If neither, can the process step be eliminated or redesigned? (reduce S)

## FMEA Worksheet Format

Use template `assets/templates/markdown/05-fmea-worksheet.md`

```
| Process Step | Failure Mode | Effect | S | O | D | RPN | Action | Owner | Target Date |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |
```

## Mermaid Diagram

Use template `assets/templates/mermaid/fmea-priority-quadrant.mmd` (Severity vs Occurrence)
