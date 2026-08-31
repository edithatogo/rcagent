# Evaluation Dataset — AU/NZ Adverse Event Cases

**Version**: 1.2
**Date**: 2026-02-25
**Status**: 7 historical NZ case files retained (HDC NZ); current study admission not established

**Readiness qualification (2026-08-31):** The historical inventory below is not
proof of source rights, anonymity, ethics status, coverage or study admission.
See the [bounded readiness audit](../../conductor/tracks/eval-blocker-remediation_20260803/historical-readiness-20260831.md).
Case bytes and historical classifications are preserved; unresolved category
mappings must not count as verified coverage.

---

## Overview

This directory retains seven NZ case files attributed to public HDC publications
and formatted for a historical evaluation. Australian cases remain absent.
File presence and formatting do not establish permission for reuse or admission
to a new study. These are historical real-case derivatives, not synthetic data.

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
| **HDC Decision Reports** | Health & Disability Commissioner | hdc.org.nz/decisions | Full range — **primary NZ source** | **7 cases collected** |
| Coroners Court NZ | NZ Coronial Services | coronialservices.justice.govt.nz | Deaths | Pending |
| HQSC Reports | Health Quality & Safety Commission | hqsc.govt.nz | Systemic quality issues | Pending |
| ACC Treatment Injury | ACC NZ | acc.co.nz | Clinical adverse events | Pending |

---

## Dataset Summary

| Metric | Target | Actual |
|---|---|---|
| Total cases | 5–10 | 7 |
| AU cases | ≥2 | 0 (pending) |
| NZ cases | ≥3 | 7 |
| SAC 1 equivalent | ≥2 | 3 (nz-case-01, nz-case-04, nz-case-07) |
| SAC 2 equivalent | ≥3 | 4 (nz-case-02, nz-case-03, nz-case-05, nz-case-06) |
| SAC 3/4 equivalent | Remainder | 0 |
| Difficulty 1 (simple) | 2–3 | 1 (nz-case-05) |
| Difficulty 2 (moderate) | 4–5 | 3 (nz-case-02, nz-case-04, nz-case-06) |
| Difficulty 3 (complex) | 2–3 | 3 (nz-case-01, nz-case-03, nz-case-07) |

### Event Type Coverage

| Event Type | Required | Case IDs |
|---|---|---|
| Medication error | ≥1 | nz-case-03 |
| Clinical deterioration | ≥1 | nz-case-02 |
| Falls / patient safety | ≥1 | nz-case-05 |
| Surgical/procedural / perinatal | ≥1 | nz-case-04 |
| Mental health | ≥1 | nz-case-01 |
| Other (aged care) | Optional | nz-case-06 |

### SAC Level Coverage

| SAC Level | Case IDs |
|---|---|
| SAC 1 | nz-case-01, nz-case-04, nz-case-07 |
| SAC 2 | nz-case-02, nz-case-03, nz-case-05, nz-case-06 |
| SAC 3/4 | — (pending AU cases) |

### Jurisdiction Coverage

| Jurisdiction | Case IDs |
|---|---|
| NZ (HDC) | nz-case-01, nz-case-02, nz-case-03, nz-case-04, nz-case-05, nz-case-06, nz-case-07 |
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
| nz-case-06 | Multiple Clinical Failures in Dementia Aged Care — Pressure Injuries, Nutrition, Falls | HDC NZ Decision 24HDC00630 | NZ | Other (aged care) | SAC 2 | 2 — Moderate | hdc-nz/nz-case-06.md |
| nz-case-07 | Delayed Colorectal Cancer Diagnosis Due to Multi-Service Pathway Failures | HDC NZ Decision 25HDC00796 | NZ | Clinical deterioration | SAC 1 | 3 — Complex | hdc-nz/nz-case-07.md |

---

## Provenance and Licensing

### Data Provenance

Existing case metadata attributes seven files to HDC NZ decisions and records
source URLs. Other source families above are candidates, not acquired cases.
The current bounded audit did not verify source availability, extraction parity
or per-artefact terms. No licence is inferred from a publisher's government or
statutory status.

### Licensing

- Public access and citation do not establish permission to copy, adapt,
  redistribute or submit source-derived material to a provider.
- Repository Apache-2.0 licensing does not grant rights in third-party material.
- Before further use, record the exact source, applicable terms and permitted
  action for each artefact; preserve unresolved rights as an admission blocker.
- Source de-identification is not a guarantee of anonymity. Privacy assessment,
  minimum-necessary content and any required authority remain separate gates.
- No further acquisition, redistribution or study use is authorised by this
  inventory. Historical files remain unchanged pending evidence reconciliation.

### How Cases Were Extracted

The retained historical record describes the following extraction method;
the current audit has not verified its fidelity or privacy assurances:

1. Source document identified and URL recorded
2. Clinical narrative extracted verbatim or with minimal paraphrasing for clarity
3. Source de-identification reportedly maintained; absence of identifying or
   re-identifying detail is not established by that report
4. Source investigation findings (contributing factors, root causes, recommendations) extracted separately for use as gold standard
5. SAC-equivalent severity and difficulty rating assigned by the research team
6. Case formatted in standardized template (see `evaluation/protocol/case-selection-criteria.md`)

---

## Ethics Statement

- Public availability does not determine ethics-review requirements, human
  research status, privacy acceptability or organisational permission.
- The earlier blanket statements that no ethics approval was required and that
  the study did not involve human subjects research are not established and
  must not be relied upon. Applicable authority must determine any such status
  for a proposed use; this repository does not make that determination.
- Repository engineering and research-method reviews use agent panels under
  the [standing decision](../../conductor/decisions/20260830-001-legacy-agent-review.md),
  not independent human reviewer recruitment. Agent agreement cannot replace
  missing rights, private-data admission, historical human observations or
  clinical, legal, regulatory, cultural-safety or organisational authority.
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

Historical illustrative layout, not an inventory: only the README and seven
`hdc-nz/` files currently exist. Australian and coroner paths below are planned.
The repository prefix is `evaluation/datasets/`.

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
