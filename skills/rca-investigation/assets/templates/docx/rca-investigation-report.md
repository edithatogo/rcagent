# DOCX Generation: Full RCA Investigation Report

Use the document-skills:docx skill to generate this document.
Apply styles from: assets/styles/docx-style-guide.md
Source content from: assets/templates/markdown/08-rca-investigation-report.md (populated)

## Document Properties
- Title: Root Cause Analysis — Investigation Report
- Confidentiality: CONFIDENTIAL: QUALITY IMPROVEMENT
- Template version: 1.0

## Cover Page
Generate a cover page with:
- Organisation name and logo (top right)
- Document title: "Root Cause Analysis — Investigation Report" (Heading 1 style, 28pt)
- SAC badge: coloured badge showing SAC level (red for SAC 1, orange for SAC 2)
- Metadata box:
  - Incident ID: [INC-YYYY-XXX]
  - Service: [De-identified]
  - Investigation Period: [Start date] to [End date]
  - Report Date: [DD/MM/YYYY]
  - Version: [X.X]
  - Approved by: [Governance committee name and date]
- "CONFIDENTIAL: QUALITY IMPROVEMENT" footer

## Section Structure (Heading 1 for each)

### 1. Executive Summary
- Maximum 1 page
- What happened: 3-bullet factual summary box (coloured background)
- Key findings: numbered list
- Recommendations: numbered list with action strength label (Strong/Intermediate/Weak)

### 2. Background and Context
- Subsections (Heading 2): Incident Description | Immediate Actions | Mandatory Notification Assessment

### 3. Investigation Process
- Team table (Heading 2: Investigation Team)
- Methods used (Heading 2: Methods Used)
- Evidence table (Heading 2: Evidence Reviewed)

### 4. Chronology of Events
- Five-phase narrative with timeline table (from template 02)
- Mermaid timeline diagram: insert PNG from timeline-chronology.mmd

### 5. Contributing Factor Analysis
- Four subsections per Yorkshire Framework level
- Contributing factors table for each level
- Mermaid Yorkshire factors diagram: insert PNG from yorkshire-factors.mmd

### 6. Root Cause Analysis
- Proximate cause: highlighted box (light orange background)
- Root cause(s): highlighted box (light red background)
- Systems analysis summary
- Bow-Tie diagram: insert PNG from bow-tie-analysis.mmd

### 7. Just Culture Assessment
- Table: Individual (role) | Classification | Rationale | Response

### 8. Findings and Recommendations
- Numbered findings table with recommendation strength indicator

### 9. Action Plan Summary
- CAPA table with RAG status colour coding
- Link to full CAPA (Appendix B)

### 10. Monitoring Plan
- Review schedule table

## Appendices
- Appendix A: Full Chronology (insert populated template 02)
- Appendix B: CAPA Action Plan (insert populated template 11)
- Appendix C: Contributing Factor Detail (insert populated template 03)
- Appendix D: Just Culture Assessment (insert populated template 14)
- Appendix E: Mermaid Diagrams (insert all populated .mmd renders)
