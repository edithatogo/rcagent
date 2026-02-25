# Tracks Registry

## Evaluation Study

---

### Phase 1: Foundation

- [x] **Track: Evaluation Protocol Development**
*Link: [./tracks/eval-protocol_20260225/](./tracks/eval-protocol_20260225/)*

---

### Phase 2: Case Collection

- [ ] **Track: Evaluation Case Collection**
*Link: [./tracks/eval-case-collection_20260225/](./tracks/eval-case-collection_20260225/)*

---

### Phase 3: Pilot Calibration

- [ ] **Track: Evaluation Pilot Calibration**
*Link: [./tracks/eval-pilot-calibration_20260225/](./tracks/eval-pilot-calibration_20260225/)*
*Depends on: eval-case-collection_20260225*

---

### Phase 4: Data Collection Runs (PARALLEL — all start after pilot calibration)

| Track | Condition | Harness | Agent |
|---|---|---|---|
| [eval-run-H0_20260225](./tracks/eval-run-H0_20260225/) | H0 — control | Raw API | Claude subagent |
| [eval-run-H1_20260225](./tracks/eval-run-H1_20260225/) | H1 — Claude Code Sonnet | Claude Code | Claude subagent |
| [eval-run-H2_20260225](./tracks/eval-run-H2_20260225/) | H2 — Claude Code Opus | Claude Code | Claude subagent |
| [eval-run-H3_20260225](./tracks/eval-run-H3_20260225/) | H3 — Gemini CLI | Gemini CLI | **Operator required** |
| [eval-run-H4_20260225](./tracks/eval-run-H4_20260225/) | H4 — Codex CLI / GPT-4o | Codex CLI | **Operator required** |
| [eval-run-H5_20260225](./tracks/eval-run-H5_20260225/) | H5 — Qwen CLI | Qwen CLI | **Operator required** |
| [eval-run-H6_20260225](./tracks/eval-run-H6_20260225/) | H6 — Kilo Code | Kilo Code | **Operator required** |
| [eval-run-H7_20260225](./tracks/eval-run-H7_20260225/) | H7 — Copilot | GitHub Copilot | **Operator required** |
| [eval-run-H8_20260225](./tracks/eval-run-H8_20260225/) | H8 — Human Expert | Human | **Human required** |

*All Phase 4 tracks depend on: eval-pilot-calibration_20260225*

- [ ] eval-run-H0_20260225
- [ ] eval-run-H1_20260225
- [ ] eval-run-H2_20260225
- [ ] eval-run-H3_20260225
- [ ] eval-run-H4_20260225
- [ ] eval-run-H5_20260225
- [ ] eval-run-H6_20260225
- [ ] eval-run-H7_20260225
- [ ] eval-run-H8_20260225

---

### Phase 5: Scoring

- [ ] **Track: Evaluation Scoring**
*Link: [./tracks/eval-scoring_20260225/](./tracks/eval-scoring_20260225/)*
*Depends on: ALL Phase 4 tracks complete*

---

### Phase 6: Analysis & Reporting

- [ ] **Track: Evaluation Analysis & Reporting**
*Link: [./tracks/eval-analysis_20260225/](./tracks/eval-analysis_20260225/)*
*Depends on: eval-scoring_20260225*

---

## Archived Tracks

- [x] **eval-data-collection_20260225** (superseded — replaced by 9 parallel per-harness run tracks in Phase 4)
  *Archived: [./archive/eval-data-collection_20260225/](./archive/eval-data-collection_20260225/)*
