# Case Selection Criteria — AI-Assisted RCA Evaluation

**Version**: 1.0
**Date**: 2026-02-25

**Safety qualification (2026-08-31):** These historical selection criteria do
not establish source rights, anonymity, ethics status or permission for study
use. Each artefact and proposed action still needs applicable rights/privacy
admission evidence. Public access or source de-identification alone is
insufficient. Repository reviews use agent panels; applicable external
authority is not delegated to those panels. See the
[current dataset qualification](../datasets/README.md#provenance-and-licensing).

---

## 1. Overview

This document defines the inclusion/exclusion criteria, difficulty rating system, and case standardization format for selecting publicly available AU/NZ adverse event cases for the evaluation study.

**Target**: Minimum 5, target 10 cases.

---

## 2. Inclusion Criteria

A case meets historical selection eligibility if ALL of the following are met.
This does not establish study admission; rights, privacy and applicable
authority must also be established for the proposed use.

| # | Criterion | Rationale |
|---|---|---|
| I1 | Published by an official government or statutory body | Ensures authority and reliability of source |
| I2 | Publicly accessible (no paywall, login, or restricted access) | Reproducibility and transparency |
| I3 | Sufficient narrative detail (≥500 words of clinical narrative) | AI needs substantive input to generate meaningful investigation |
| I4 | Occurred in AU or NZ healthcare setting | Jurisdictional relevance to rcagent skill suite |
| I5 | Involves a patient safety event (harm or near-miss) | Core scope of RCA investigation |
| I6 | Source includes identified contributing factors or findings | Enables gold-standard comparison |
| I7 | Already de-identified in source document | Historical selection condition only; further privacy assessment and any necessary transformations or authority remain required before admission |

---

## 3. Exclusion Criteria

A case is excluded if ANY of the following apply:

| # | Criterion | Rationale |
|---|---|---|
| E1 | Case involves only consent/communication complaints without clinical harm | Outside RCA scope |
| E2 | Source document is primarily legal/liability-focused without clinical analysis | Different analytical framework |
| E3 | Insufficient clinical detail to conduct meaningful investigation (narrative <500 words) | AI cannot generate useful output from minimal input |
| E4 | Case involves ongoing legal proceedings where use could be inappropriate | Ethical caution |
| E5 | Source findings are ambiguous or disputed | Undermines gold standard comparison |
| E6 | Case so widely publicized that LLMs likely memorized the specific findings | Confound — tests recall, not investigation capability |

---

## 4. Coverage Requirements

The selected case set must collectively satisfy:

### 4.1 Event Type Coverage

| Event Type | Minimum Count | Rationale |
|---|---|---|
| Medication error | ≥1 | Common, well-understood event type |
| Clinical deterioration / failure to rescue | ≥1 | Tests recognition of escalation failures |
| Falls (with significant harm) | ≥1 | Common, often has systems factors |
| Surgical / procedural | ≥1 | Tests understanding of procedural safety |
| Mental health | ≥1 | Tests understanding of mental health-specific factors |

Additional event types (diagnostic error, infection, maternity, etc.) are desirable but not required.

### 4.2 Severity Coverage

| SAC-Equivalent | Minimum Count | Rationale |
|---|---|---|
| SAC 1 (death / permanent severe harm) | ≥2 | Tests skill on highest-severity events requiring comprehensive investigation |
| SAC 2 (major / temporary severe harm) | ≥3 | Most common RCA trigger level |
| SAC 3/4 (moderate / minor / near-miss) | Remainder | Tests proportionality of investigation response |

**SAC-equivalent assignment**: Since source documents may not use SAC classification, assign SAC-equivalent based on:
- SAC 1: Death, permanent loss of function, or sentinel event
- SAC 2: Temporary severe harm requiring intervention, or significant near-miss
- SAC 3: Moderate harm, minor procedure, or short-term temporary harm
- SAC 4: Minor harm or near-miss with no patient harm

### 4.3 Jurisdictional Coverage

| Jurisdiction | Minimum Count | Rationale |
|---|---|---|
| Australia (any state/territory) | ≥2 | Primary jurisdiction |
| New Zealand | ≥3 | HDC decisions are richest source |

### 4.4 Difficulty Coverage

| Difficulty | Target Count | Rationale |
|---|---|---|
| Simple (1) | 2–3 | Baseline — do all conditions perform well on easy cases? |
| Moderate (2) | 4–5 | Core comparison range |
| Complex (3) | 2–3 | Stress test — where does performance degrade? |

---

## 5. Difficulty Rating System

Each case is rated for investigation difficulty on a 1–3 scale. Rating is assigned BEFORE any AI conditions are run, based on the source investigation's characteristics.

### 5.1 Rating Criteria

| Criterion | Simple (1) | Moderate (2) | Complex (3) |
|---|---|---|---|
| **Contributing factors** | 1–2 clear factors | 3–5 factors across ≥2 levels | 6+ factors across ≥3 levels |
| **Individuals involved** | 1–2 staff | 3–5 staff, possibly cross-discipline | Multiple teams, departments, shifts |
| **Timeframe** | Single encounter / shift | Multiple shifts / days | Weeks to months; chronic system issues |
| **Causal chain** | Linear, clear | Branching, some ambiguity | Systemic, emergent, non-linear |
| **Organisational factors** | Minimal | Some (staffing, policy) | Significant (culture, governance, resourcing) |
| **Information in narrative** | Mostly complete | Some gaps, requires inference | Significant gaps, complex inferences needed |

### 5.2 Rating Procedure

1. Read the full source document
2. Score each criterion as 1, 2, or 3
3. Overall difficulty = mode of criterion scores (if tied, round up)
4. Document the rating rationale

### 5.3 Rating Examples

**Simple (1)**: A single medication error where a nurse administered the wrong dose due to a look-alike/sound-alike drug name, resulting in temporary harm. One staff member, one shift, clear contributing factor (LASA naming), clear root cause (no LASA alert in dispensing system).

**Moderate (2)**: A patient fall resulting in hip fracture where multiple contributing factors include: incomplete falls risk assessment, understaffing on night shift, environmental hazard (wet floor), and inadequate post-operative mobilization protocol. Multiple staff across 2 shifts, 3–4 contributing factors, some organisational factors.

**Complex (3)**: A patient death following failure to escalate clinical deterioration over 48 hours, involving multiple handovers across 3 shifts, communication failures between medical and nursing teams, inadequate observation protocols, MET call criteria not met despite vital sign abnormalities, training gaps, and organisational culture issues around escalation. 6+ contributing factors, multiple teams, systemic issues.

---

## 6. Case Sources — Priority Order

### 6.1 Primary Sources

**HDC NZ Decision Reports** (hdc.org.nz/decisions)
- **Priority**: Highest for NZ cases
- **Strengths**: Full investigation reports with detailed findings, contributing factors identified, recommendations made, de-identified, publicly available
- **Case types**: Full range of healthcare complaints and adverse events
- **Selection approach**: Search by category (e.g., "public hospital"), filter by year (recent preferred), select cases with clinical adverse events (not pure communication/consent complaints)

**ACSQHC Sentinel Event Reports**
- **Priority**: Highest for AU cases
- **Strengths**: National-level analysis, standardized format, de-identified vignettes
- **Limitation**: Vignettes may be brief — verify ≥500 words of narrative
- **Selection approach**: Annual sentinel event reports, select individual case vignettes

### 6.2 Secondary Sources

**Coroners Court** (Victoria, NSW, QLD)
- **Strengths**: Detailed clinical narratives, investigation findings, recommendations
- **Limitation**: Only death cases (SAC 1 equivalent only); may be more widely publicized (E6 risk)
- **Selection approach**: Search health/medical findings, select inpatient/healthcare-related deaths

**NSW Clinical Excellence Commission** (cec.health.nsw.gov.au)
- **Strengths**: State-level published incident analyses, clinical focus
- **Selection approach**: Published reports and case studies

**Victorian CCOPMM Reports** (safercare.vic.gov.au)
- **Strengths**: Detailed perinatal/maternal case reviews
- **Limitation**: Specialized event type only (maternity)
- **Selection approach**: Annual reports with individual case reviews

### 6.3 Tertiary Sources

**HQSC NZ Reports** (hqsc.govt.nz)
- **Strengths**: National quality improvement reports
- **Limitation**: Often aggregate/thematic rather than individual case
- **Selection approach**: Look for individual case studies within thematic reports

**NZ Coroners Court** (coronialservices.justice.govt.nz)
- **Strengths**: Detailed death investigation findings
- **Limitation**: Only death cases; NZ coronial findings may be lengthy legal documents
- **Selection approach**: Search healthcare-related findings

**ACC Treatment Injury** (acc.co.nz)
- **Strengths**: NZ-specific treatment injury data
- **Limitation**: Aggregate data; individual case details rare
- **Selection approach**: Published case studies if available

---

## 7. Case Standardization Format

Each selected case is documented in a standardized markdown file with the following structure:

```markdown
# [Case ID]: [Brief Title]

## Metadata

| Field | Value |
|---|---|
| **Source** | [Full source name and document title] |
| **URL** | [Direct URL to source document] |
| **Jurisdiction** | AU / NZ |
| **Event Type** | [e.g., Medication error, Clinical deterioration, Fall, Surgical, Mental health] |
| **SAC-Equivalent** | [1 / 2 / 3 / 4] |
| **Difficulty Rating** | [1 (Simple) / 2 (Moderate) / 3 (Complex)] |
| **Year of Event** | [Year, if known] |
| **Setting** | [e.g., Public hospital, Private hospital, Community health] |
| **Word Count** | [Narrative word count] |

## Difficulty Rating Rationale

[2–3 sentences explaining the difficulty rating based on the criteria in Section 5]

## Case Narrative

[Standardized narrative extracted from the source document.
- Maintains de-identification from source
- Written in clinical neutral language
- Includes relevant clinical details, timeline elements, and contextual information
- Minimum 500 words]

## Source Investigation Findings (Gold Standard)

### Contributing Factors Identified
[Bulleted list of contributing factors as identified by the source investigation]

### Root Causes Identified
[Bulleted list of root causes / key findings from the source investigation]

### Recommendations Made
[Bulleted list of recommendations from the source investigation]

### Outcome / Actions Taken
[Summary of any reported outcomes or actions taken, if available in source]
```

---

## 8. Quality Assurance Checklist

Before including a case in the evaluation dataset:

- [ ] Per-artefact rights, privacy and applicable authority evidence supports
  the proposed use; public access and source de-identification alone do not pass
- [ ] Meets ALL inclusion criteria (I1–I7)
- [ ] Does not meet ANY exclusion criteria (E1–E6)
- [ ] Narrative is ≥500 words
- [ ] Difficulty rating assigned with documented rationale
- [ ] SAC-equivalent assigned with documented rationale
- [ ] Source investigation findings extracted accurately
- [ ] Case formatted in standardized template
- [ ] De-identification maintained (no real names, MRN, specific dates of birth)
- [ ] Case does not duplicate another case in the dataset (different event, not different reports of same event)

After full case set is assembled:

- [ ] Coverage requirements met (event types, severity, jurisdiction, difficulty)
- [ ] Minimum 5 cases, target 10
- [ ] Mix of sources (not all from single source)
