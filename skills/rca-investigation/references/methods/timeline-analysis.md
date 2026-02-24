# Timeline / Chronology Analysis

Constructs a detailed, accurate sequence of events before, during, and after an adverse event. The timeline is the foundation of almost every investigation — it provides the factual backbone that all other analysis methods build upon.

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
- **Warning signs**: Early signals that went unrecognised or unacted upon
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

PHASE 2: EARLY INCIDENT (warning signs)
[Date/Time] | [Event] | [Source] | [Warning sign? Y/N]

PHASE 3: INCIDENT / ACUTE PHASE
[Date/Time] | [Event] | [Source] | [Decision point? Y/N]

PHASE 4: RESPONSE AND ESCALATION
[Date/Time] | [Event] | [Source] | [Barrier present? Y/N]

PHASE 5: POST-EVENT (disclosure, investigation, actions)
[Date/Time] | [Event] | [Source]
```

## Mermaid Diagram

Use template `assets/templates/mermaid/timeline-chronology.mmd`

## Common Pitfalls

- Accepting a single source as definitive — cross-reference multiple records
- Assuming clocks are synchronised — EMR, nursing station, phone, and CCTV clocks may differ
- Focusing only on the acute event — the pre-event context often contains the most important findings
- Conflating what was known at the time with hindsight knowledge
- Omitting "nothing happened" intervals — these gaps are often as significant as events

## Integration

The timeline should be shared with the investigation team before applying any other analysis method. It provides the shared factual foundation for Fishbone, Yorkshire Framework, Bow-Tie, and all other methods.
