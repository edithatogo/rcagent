# Product Guidelines

## Writing Style

### Tone
- **Clinical and professional**: This is a governance tool used in serious adverse event investigations. Language must reflect that gravity.
- **Evidence-based**: All method descriptions and recommendations must reference published literature or established frameworks (ACSQHC, Joint Commission, NHS Improvement).
- **Systems-focused**: Avoid individual blame language. Frame findings at system, team, and organisational levels before individual.
- **Precise**: Use exact regulatory terminology (SAC not "severity", NSQHS not "standards", "contributing factors" not "causes" unless at root cause level).

### Voice
- Active voice preferred for recommendations and action items
- Passive voice acceptable for event descriptions and investigation findings
- Second person ("you") for workflow instructions and agent prompts
- Third person for formal reports and templates

### AU/NZ Spellings
Use Australian/New Zealand English throughout:
- organisation (not organization)
- recognise, analyse, categorise (not -ize)
- programme (not program, except computer program)
- colour, honour, behaviour

## De-identification (Mandatory)

All templates and examples must use placeholder identifiers:
- Patients: `[Patient A]`, `[Patient B]` — never real names or initials
- Case identifiers: `[Case ID]` — never real MRN, URN, or NHI
- Locations: `[Ward X]`, `[Unit Y]`, `[Hospital Z]` — never real ward names
- Dates: `[Date]`, `[Time]`, `[DD/MM/YYYY HH:MM]` — never real patient dates
- Staff: `[Clinician A]`, `[RN B]` — never real names or employee IDs

**All investigation reports must include the header:**
```
CONFIDENTIAL: QUALITY IMPROVEMENT DOCUMENT
Protected under [relevant state/territory Health Act] quality improvement provisions
```

## Regulatory Language

### SAC Classification
Always use the full term on first reference: "Severity Assessment Code (SAC)"
Use SAC 1, SAC 2, SAC 3, SAC 4 (not SAC1, sac1, or other variants)

### Framework References
- Full name first use: "National Safety and Quality Health Service (NSQHS) Standards"
- "Australian Commission on Safety and Quality in Health Care (ACSQHC)"
- "Health and Disability Commissioner (HDC)" for NZ cases
- "Health Quality & Safety Commission New Zealand (HQSC)"

### Investigation Method Names
Always capitalise formal method names:
- Root Cause Analysis (RCA)
- Yorkshire Contributory Factors Framework
- Systems Engineering Initiative for Patient Safety (SEIPS)
- Human Factors Analysis and Classification System (HFACS)

## Template Formatting

### Headers
- H1 (`#`): Document title only
- H2 (`##`): Major sections
- H3 (`###`): Subsections
- H4 (`####`): Use sparingly, only where needed

### Tables
Use GFM tables for structured data (scoring rubrics, method matrices, case metadata).
Include a header row. Align columns for readability.

### Callouts / Notes
Use blockquotes for important notes:
> **Note**: This template requires completion within 72 hours of SAC 1 event notification.

### Code blocks
Use fenced code blocks (triple backtick) for:
- Mermaid diagram source
- YAML frontmatter examples
- Command-line instructions

## Content Accuracy Standards

- All 14 investigation method descriptions must cite their primary literature source
- SAC classification criteria must match current ACSQHC RCA guidelines
- Just Culture classifications must align with Marx (2001) framework
- Action strength classifications (Strong/Intermediate/Weak) must follow IHI/ACSQHC hierarchy
- Any regulatory reference must include the issuing body and version/year
