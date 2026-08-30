# Context Pack: Legacy review substitution and protocol decision

- **Track:** eval-blocker-remediation_20260803
- **GitHub issue:** https://github.com/edithatogo/rcagent/issues/1
- **Base revision:** 9fcfab4e37d85aa1dffc1457ca605f24c558f21b
- **Created:** 2026-08-30T04:40:11Z
- **Fresh until:** Source, protocol or owner-decision change
- **Privacy mode:** Repository metadata only; no case narrative processing
- **Context budget:** Selected remediation, scoring and analysis plans/specs;
  standing governance decision and preflight source; no raw study outputs
- **Owned files:** Review amendments in those tracks, decision records, this
  context pack and the panel recommendation receipt

## Objective and acceptance

Replace external-human repository reviews with agent panels, preserve genuine
condition/provenance/authority gates, and present one protocol choice. Do not
execute, score, admit, unblind or complete the historical study.

## Inputs and dependencies

Use conductor/index.md, product-guidelines.md, workflow.md, tech-stack.md,
the selected track specification/plan/metadata and its Option A controls;
eval-scoring and eval-analysis specifications/plans; standing decision
20260829-004-agent-panel-research-governance. Historical execution dependencies
remain blocked and are not prerequisites for this planning-only amendment.

## Validation and handoff

Run uv run python -m tools.full_validation, repository governance validation,
JSON and diff checks. Panel reviews acceptance, provenance and authority.
Rollback is a scoped revert of this amendment, preserving historical evidence.
Next work: structured preflight hardening and synthetic fixtures; study
execution awaits decision 20260830-002-prospective-agent-study and admission.
