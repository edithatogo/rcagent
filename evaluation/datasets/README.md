# Evaluation Dataset — AU/NZ Adverse Event Cases

**Version**: 1.1
**Date**: 2026-02-25
**Status**: 5 NZ cases collected (HDC NZ)

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
| **HDC Decision Reports** | Health & Disability Commissioner | hdc.org.nz/decisions | Full range — **primary NZ source** | **5 cases collected** |
| Coroners Court NZ | NZ Coronial Services | coronialservices.justice.govt.nz | Deaths | Pending |
| HQSC Reports | Health Quality & Safety Commission | hqsc.govt.nz | Systemic quality issues | Pending |
| ACC Treatment Injury | ACC NZ | acc.co.nz | Clinical adverse events | Pending |

---

## Dataset Summary

| Metric | Target | Actual |
|---|---|---|
| Total cases | 5–10 | 5 |
| AU cases | ≥2 | 0 (pending) |
| NZ cases | ≥3 | 5 |
| SAC 1 equivalent | ≥2 | 2 (nz-case-01, nz-case-04) |
| SAC 2 equivalent | ≥3 | 3 (nz-case-02, nz-case-03, nz-case-05) |
| SAC 3/4 equivalent | Remainder | 0 |
| Difficulty 1 (simple) | 2–3 | 1 (nz-case-05) |
| Difficulty 2 (moderate) | 4–5 | 2 (nz-case-02, nz-case-04) |
| Difficulty 3 (complex) | 2–3 | 2 (nz-case-01, nz-case-03) |

### Event Type Coverage

| Event Type | Required | Case IDs |
|---|---|---|
| Medication error | ≥1 | nz-case-03 |
| Clinical deterioration | ≥1 | nz-case-02 |
| Falls / patient safety | ≥1 | nz-case-05 |
| Surgical/procedural / perinatal | ≥1 | nz-case-04 |
| Mental health | ≥1 | nz-case-01 |
| Other | Optional | — |

### SAC Level Coverage

| SAC Level | Case IDs |
|---|---|
| SAC 1 | nz-case-01, nz-case-04 |
| SAC 2 | nz-case-02, nz-case-03, nz-case-05 |
| SAC 3/4 | — (pending AU cases) |

### Jurisdiction Coverage

| Jurisdiction | Case IDs |
|---|---|
| NZ (HDC) | nz-case-01, nz-case-02, nz-case-03, nz-case-04, nz-case-05 |
| AU | — (pending) |

---

## Case Index

| Case ID | Title | Source | Jurisdiction | Event Type | SAC | Difficulty | File |
|---|---|---|---|---|---|---|---|
| nz-case-01 | Failures in Acute Mental Health Care Following Multiple Declined Referrals | HDC NZ Decision 21HDC00502 | NZ | Mental health | SAC 1 | 3 — Complex | hdc-nz/nz-case-01.md |
| nz-case-02 | Delayed Escalation of Care in Prison Health Leading to Emergency Surgery | HDC NZ Decision 22HDC02054 | NZ | Clinical deterioration | SAC 2 | 2 — Moderate | hdc-nz/nz-case-02.md |
| nz-case-03 | Multiple System Failures During Six-Week Inpatient Respiratory Admission | HDC NZ Decision 21HDC00718 | NZ | Medication error | SAC 2 | 3 — Complex | hdc-nz/nz-case-03.md |
| nz-case-04 | Neonatal Death Following Inadequate Monitoring During Nurse Break | HDC NZ Decision 20HDC01313 | NZ | Perinatal/neonatal | SAC 1 | 2 — Moderate | hdc-nz/nz-case-04.md |
| nz-case-05 | Failure to Protect Patient from Repeated Inappropriate Behaviour by Co-Patient | HDC NZ Decision 22HDC00290 | NZ | Patient safety (ward) | SAC 2 | 1 — Simple | hdc-nz/nz-case-05.md |

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
