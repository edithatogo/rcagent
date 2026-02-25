# Evaluation Protocol Development — Plan

## Phase 1: Protocol Documents

- [x] Task: Write master scientific protocol
    - [x] Factorial design with 9 conditions
    - [x] Primary/secondary/tertiary objectives
    - [x] Dataset sources and selection criteria
    - [x] Analysis plan
    - [x] Limitations and ethics
- [x] Task: Write 8-dimension evaluation rubric
    - [x] Scoring anchors for D1-D8 (1-5 scale)
    - [x] Pilot calibration protocol
    - [x] Inter-rater reliability subset plan
    - [x] AI rater prompt template
- [x] Task: Write literature review
    - [x] 14 investigation method citations
    - [x] RCA quality literature
    - [x] AI in clinical domains
    - [x] Evaluation methodology
- [x] Task: Write case selection criteria
    - [x] Inclusion/exclusion criteria
    - [x] Coverage requirements
    - [x] Difficulty rating system
    - [x] Case standardization format
- [x] Task: Write agent test protocol
    - [x] Prompt S (skill-aware) and Prompt N (naive control)
    - [x] Per-harness injection for 7 harnesses
    - [x] Output normalization (8 sections)
    - [x] Blinding protocol
    - [x] Reproducibility protocol

## Phase 2: Infrastructure

- [x] Task: Create dataset directory structure
    - [x] README with provenance and ethics
    - [x] Source directories (acsqhc, hdc-nz, coroner-au, coroner-nz)
- [x] Task: Create results directory structure
    - [x] 9 condition directories (H0-H8)
    - [x] case-01 scaffolds with run-1/2/3
    - [x] Template files (raw-transcript, normalized-output, scores)
    - [x] Blinding map CSV
- [x] Task: Create analysis framework
    - [x] rubric-scores.csv with schema
    - [x] Inter-rater reliability template
    - [x] Comparative analysis template
    - [x] Case-level analysis template
    - [x] Failure mode analysis template
    - [x] Technical report skeleton

## Phase 3: Integration

- [x] Task: Update conductor context files
    - [x] product.md — evaluation study section
    - [x] tech-stack.md — evaluation directory tree + CSV format
    - [x] workflow.md — evaluation study workflow procedures
    - [x] CLAUDE.md — evaluation reference section
- [x] Task: Consistency review and fixes
    - [x] Fix composite score formula (Issue 4 — critical)
    - [x] Fix H8 path structure (Issue 1)
    - [x] Rename Prompt A/B to S/N (Issue 3)
    - [x] Add ACC NZ to scientific protocol (Issue 5)
    - [x] Add H6/H7 to case-level analysis (Issue 2)

## Phase 4: Publication

- [x] Task: Commit and push to GitHub
    - [x] Stage all new and modified files
    - [x] Commit with descriptive message
    - [x] Create public repo `rcagent` via gh CLI
    - [x] Push to origin
