# Evaluation Case Collection — Plan

## Current reconciliation (2026-08-31)

The [bounded structural audit](../eval-blocker-remediation_20260803/historical-readiness-20260831.md)
found seven existing NZ files and their index under `evaluation/datasets/`.
Narrative sections exceed 500 whitespace-delimited words, with recorded ratings
and findings; source fidelity, privacy, rights and QA are not established.
The former Phase 2 checked state recorded a historical collection judgement,
not demonstrated final acceptance: AU coverage is zero, difficulty targets are
unmet and two event-type mappings remain unresolved. The dated original note
below is retained. No historical case bytes or classifications were changed.

Agent panels perform repository reviews under
[decision 001](../../decisions/20260830-001-legacy-agent-review.md). Missing
rights, source evidence and applicable authority are not reviewer recruitment
tasks; no repeat approval is needed for routine reconciliation.

## Phase 1: Source Research

- [x] Task: Search HDC NZ decisions for eligible cases
    - [x] Search by category (public hospital, aged care)
    - [x] Filter for clinical adverse events (not pure complaints)
    - [x] Identify 5-7 candidate cases meeting inclusion criteria
- [ ] Task: Search ACSQHC sentinel event reports
    - [ ] Review recent annual reports for individual case vignettes
    - [ ] Identify 3-5 candidate cases meeting inclusion criteria
- [ ] Task: Search AU/NZ coroner findings (if needed for coverage)
    - [ ] Search Victoria, NSW, QLD coroner findings for healthcare deaths
    - [ ] Search NZ coronial services
    - [ ] Identify 2-3 candidate cases

## Phase 2: Case Selection and Coverage Check

- [!] Task: Establish inclusion/exclusion acceptance for all candidates
    - [!] Verify I1-I7 and per-artefact rights/privacy/authority evidence
    - [ ] Check E1-E6 exclusions against source evidence
    - [ ] Reconcile retained inclusion decisions with current admission evidence
- [!] Task: Select final case set meeting coverage requirements
    - [!] Event type coverage: unresolved falls/patient-safety and surgical/perinatal mappings
    - [ ] Verify recorded SAC-equivalent coverage and rationales
    - [!] Jurisdiction coverage: zero AU cases against at least two required
    - [!] Difficulty distribution: simple 1 and moderate 3 below targets

> **Note (2026-02-25)**: 7 cases collected — all NZ (HDC decisions). AU cases pending: ACSQHC and coroner sites timed out during collection. NZ cases cover mental health x2, deterioration x2, medication, neonatal, patient safety, aged care.

## Phase 3: Case Standardization

- [!] Task: Verify standardised cases against source and admission evidence
    - [ ] Verify existing narrative extraction and eligible clinical word count
    - [ ] Verify recorded SAC-equivalent and rationale
    - [ ] Verify recorded difficulty rating and rationale
    - [ ] Verify source findings extraction (factors, root causes, recommendations)
- [ ] Task: Run QA checklist on each case
    - [ ] All items in case-selection-criteria.md Section 8 checked
- [ ] Task: Save cases to datasets directories
    - [x] Seven historical HDC NZ files exist in `evaluation/datasets/hdc-nz/`;
      [structural receipt](../eval-blocker-remediation_20260803/historical-readiness-20260831.md),
      not a source-rights or QA pass
    - [ ] ACSQHC cases to datasets/acsqhc/
    - [ ] Coroner cases to datasets/coroner-au/ or coroner-nz/
- [x] Existing seven-case index verified at `evaluation/datasets/README.md` and
  current rights/privacy/coverage qualifications added; see the
  [receipt](../eval-blocker-remediation_20260803/historical-readiness-20260831.md).
  Future admitted cases still require index updates.
