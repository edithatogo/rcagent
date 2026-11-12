# RCA & SAE Investigation Skill Suite

Healthcare root-cause analysis and serious adverse event investigation tools for AU/NZ clinical governance.

Start with `AGENTS.md`, `CONSTRAINTS.md` and `conductor/index.md`; they hold the
current navigation, quality and authority contracts. Load the selected track
and bounded context pack rather than treating this summary as complete context.

## Conventions

- Jurisdiction: verify the actual AU/NZ jurisdiction, current policy and local applicability; severity scales and review/reporting obligations are not universal.
- All templates de-identify patients: use [Patient A], [Case ID], [Ward X]
- Mermaid diagrams use .mmd extension
- DOCX/PPTX files are generation-instruction markdown files (not binary files)
- Agent files live in agents/ at repo root
- Skill reference files live in skills/rca-investigation/references/
- Templates live in skills/rca-investigation/assets/templates/

## Evaluation

- Evaluation protocol and framework live in evaluation/
- Protocol documents: evaluation/protocol/ (scientific protocol, rubric, test protocol)
- Datasets: evaluation/datasets/ (AU/NZ public adverse event cases)
- Results: evaluation/results/H{0-8}-{condition}/ (raw transcripts, normalized outputs, scores)
- Analysis: evaluation/analysis/ (scores CSV, reports)
- 8-dimension rubric (D1-D8): see evaluation/protocol/evaluation-rubric.md
- 9 experimental conditions (H0-H8): see evaluation/protocol/scientific-protocol.md

## Integration

This skill integrates with:
- health-incident-reporting (verified local incident criteria prompt review-path triage; no universal severity-to-RCA rule)
- health-clinical-risk-assessment (RCA findings create risk register entries)
- health-quality-improvement (CAPA/PDSA flows from RCA recommendations)
- health-enterprise-risk-assessment (systemic findings escalate to enterprise risk)
