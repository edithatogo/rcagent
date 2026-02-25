# Evaluation Dataset — AU/NZ Adverse Event Cases

**Version**: 1.0
**Date**: 2026-02-25
**Status**: Case collection pending

---

## Overview

This dataset contains publicly available Australian and New Zealand adverse event cases used to evaluate the rcagent skill suite. Each case is extracted from official government or statutory body publications and formatted in a standardized structure.

---

## Sources

### Australian Sources

| Source | Organisation | URL | Case Types | Status |
|---|---|---|---|---|
| Sentinel Event Reports | ACSQHC | safetyandquality.gov.au | Medication, surgical, deterioration, falls | Pending |
| Clinical Excellence Commission | NSW Health | cec.health.nsw.gov.au | Various clinical incidents | Pending |
| CCOPMM Reports | Safer Care Victoria | safercare.vic.gov.au | Perinatal/maternal | Pending |
| Coroners Court Victoria | Coroners Court of Victoria | coronerscourt.vic.gov.au | Inpatient deaths | Pending |
| Coroners Court NSW | Coroners Court of NSW | coroners.nsw.gov.au | Inpatient deaths | Pending |
| Coroners Court QLD | Coroners Court of Queensland | courts.qld.gov.au/courts/coroners-court | Inpatient deaths | Pending |

### New Zealand Sources

| Source | Organisation | URL | Case Types | Status |
|---|---|---|---|---|
| **HDC Decision Reports** | Health & Disability Commissioner | hdc.org.nz/decisions | Full range — **primary NZ source** | Pending |
| Coroners Court NZ | NZ Coronial Services | coronialservices.justice.govt.nz | Deaths | Pending |
| HQSC Reports | Health Quality & Safety Commission | hqsc.govt.nz | Systemic quality issues | Pending |
| ACC Treatment Injury | ACC NZ | acc.co.nz | Clinical adverse events | Pending |

---

## Dataset Summary

| Metric | Target | Actual |
|---|---|---|
| Total cases | 5–10 | TBD |
| AU cases | ≥2 | TBD |
| NZ cases | ≥3 | TBD |
| SAC 1 equivalent | ≥2 | TBD |
| SAC 2 equivalent | ≥3 | TBD |
| SAC 3/4 equivalent | Remainder | TBD |
| Difficulty 1 (simple) | 2–3 | TBD |
| Difficulty 2 (moderate) | 4–5 | TBD |
| Difficulty 3 (complex) | 2–3 | TBD |

### Event Type Coverage

| Event Type | Required | Case IDs |
|---|---|---|
| Medication error | ≥1 | TBD |
| Clinical deterioration | ≥1 | TBD |
| Falls | ≥1 | TBD |
| Surgical/procedural | ≥1 | TBD |
| Mental health | ≥1 | TBD |
| Other | Optional | TBD |

---

## Case Index

| Case ID | Title | Source | Jurisdiction | Event Type | SAC | Difficulty | File |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

(To be populated during case collection phase.)

---

## Provenance and Licensing

### Data Provenance

All cases are sourced from publicly available documents published by official government or statutory bodies:

- **HDC NZ decisions**: Published under the Health and Disability Commissioner Act 1994. Decisions are published on the HDC website for public access as part of the Commissioner's transparency mandate.
- **ACSQHC reports**: Published by the Australian Commission on Safety and Quality in Health Care as part of national patient safety reporting. Available under Australian Government copyright (Creative Commons Attribution-NonCommercial-ShareAlike where specified, otherwise standard Crown copyright).
- **Coroner findings**: Published by state/territory Coroners Courts as a matter of public record. Coroner findings are public documents.
- **CEC/CCOPMM reports**: Published by state health agencies for public information and quality improvement.

### Licensing

- Source documents are published by government agencies for public access
- This dataset extracts and standardizes narratives from these public documents for research purposes
- Extracted narratives maintain the de-identification present in source documents
- No additional patient data is created, inferred, or supplemented
- Citation of source documents is provided for each case

### How Cases Were Extracted

1. Source document identified and URL recorded
2. Clinical narrative extracted verbatim or with minimal paraphrasing for clarity
3. De-identification from source document maintained (no names, MRN, or identifying details)
4. Source investigation findings (contributing factors, root causes, recommendations) extracted separately for use as gold standard
5. SAC-equivalent severity and difficulty rating assigned by the research team
6. Case formatted in standardized template (see `evaluation/protocol/case-selection-criteria.md`)

---

## Ethics Statement

- All case data is sourced from **publicly available** documents published by official government or statutory bodies
- No patient contact occurs during this study
- No ethics committee approval is required (secondary analysis of published, de-identified documents)
- All case narratives used in this study maintain the de-identification present in the source documents
- This study does not involve human subjects research
- AI-generated investigation outputs are for **evaluation purposes only** — they are NOT clinical investigation reports and must NOT be used for clinical governance decisions

---

## Difficulty Ratings

Cases are rated 1 (simple), 2 (moderate), or 3 (complex) based on:

| Criterion | Simple (1) | Moderate (2) | Complex (3) |
|---|---|---|---|
| Contributing factors | 1–2 clear | 3–5 across ≥2 levels | 6+ across ≥3 levels |
| Individuals involved | 1–2 staff | 3–5, possibly cross-discipline | Multiple teams, departments, shifts |
| Timeframe | Single encounter/shift | Multiple shifts/days | Weeks to months |
| Causal chain | Linear, clear | Branching, some ambiguity | Systemic, emergent, non-linear |
| Organisational factors | Minimal | Some | Significant |

Full criteria in `evaluation/protocol/case-selection-criteria.md`.

---

## Directory Structure

```
datasets/
├── README.md                  ← This file
├── acsqhc/
│   ├── au-case-01.md         ← ACSQHC sentinel event cases
│   └── ...
├── hdc-nz/
│   ├── nz-case-01.md         ← HDC NZ decision cases
│   └── ...
├── coroner-au/
│   ├── au-case-XX.md         ← Australian coroner cases
│   └── ...
└── coroner-nz/
    ├── nz-case-XX.md         ← NZ coroner cases
    └── ...
```
