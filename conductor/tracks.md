# Tracks Registry

## Safety Systems Workbench Portfolio

- **Roadmap:** [conductor/roadmap.md](./roadmap.md)
- **GitHub roadmap:** [#1](https://github.com/edithatogo/rcagent/issues/1)
- **Execution policy:** autonomous within declared owner decision gates

### Workstream A: Foundation and Governance

Parent: [GitHub #2](https://github.com/edithatogo/rcagent/issues/2)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [ ] | [00 Agent Skills Living Conformance and Portable Architecture](./tracks/agent-skills-living-conformance_20260731/index.md) | [#5](https://github.com/edithatogo/rcagent/issues/5) | None |
| [ ] | [01 Safety Systems Foundation and Solo-Developer Harness](./tracks/safety-systems-foundation_20260731/index.md) | [#6](https://github.com/edithatogo/rcagent/issues/6) | 00 |
| [ ] | [02 Evidence Workflow Core](./tracks/evidence-workflow-core_20260731/index.md) | [#7](https://github.com/edithatogo/rcagent/issues/7) | 01 |
| [ ] | [03 Privacy, Security, and Assurance](./tracks/privacy-security-assurance_20260731/index.md) | [#8](https://github.com/edithatogo/rcagent/issues/8) | 01 |
| [ ] | [04 NSW Health Jurisdiction Pack](./tracks/nsw-health-jurisdiction-pack_20260731/index.md) | [#9](https://github.com/edithatogo/rcagent/issues/9) | 01 |

### Workstream B: Data, Models, and Evaluation

Parent: [GitHub #3](https://github.com/edithatogo/rcagent/issues/3)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [ ] | [05 Benchmark and Evaluation Harness](./tracks/benchmark-evaluation-harness_20260731/index.md) | [#10](https://github.com/edithatogo/rcagent/issues/10) | 02, 03 |
| [ ] | [06 Multimodal Capability Fabric](./tracks/multimodal-capability-fabric_20260731/index.md) | [#11](https://github.com/edithatogo/rcagent/issues/11) | 02, 03 |
| [ ] | [07 Retrieval and Knowledge System](./tracks/retrieval-knowledge-system_20260731/index.md) | [#12](https://github.com/edithatogo/rcagent/issues/12) | 02, 03, 04 |
| [ ] | [08 Local Runtime and Model Lab](./tracks/local-runtime-model-lab_20260731/index.md) | [#13](https://github.com/edithatogo/rcagent/issues/13) | 05, 06 |
| [ ] | [10 Domain Adaptation and Fine-Tuning](./tracks/domain-adaptation-finetuning_20260731/index.md) | [#15](https://github.com/edithatogo/rcagent/issues/15) | 05, 06, 07, 08 |

### Workstream C: Product, Interfaces, and Distribution

Parent: [GitHub #4](https://github.com/edithatogo/rcagent/issues/4)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [ ] | [09 Interfaces, Templates, and Closed-Loop Actions](./tracks/interfaces-templates-action-loop_20260731/index.md) | [#14](https://github.com/edithatogo/rcagent/issues/14) | 02, 03, 04 |
| [ ] | [11 Distribution, Registries, and Client Plugins](./tracks/distribution-registries-plugins_20260731/index.md) | [#16](https://github.com/edithatogo/rcagent/issues/16) | 00 |

`metadata.json` records later phase dependencies that deliberately do not block independent foundation work.

## Legacy Evaluation Study

These tracks remain preserved historical work. Track 05 will reconcile their schemas, cases, conditions, results, and limitations into the canonical benchmark harness without rewriting original artefacts.

### Completed Foundations

- [x] [Evaluation Protocol Development](./tracks/eval-protocol_20260225/)
- [x] [Evaluation Case Collection](./tracks/eval-case-collection_20260225/) — 9 cases recorded

### In Progress

- [~] [Evaluation Pilot Calibration](./tracks/eval-pilot-calibration_20260225/) — H0 and H1 pilot runs recorded; scoring pending

### Historical Parallel Conditions

| Track | Condition | Recorded harness |
|---|---|---|
| [eval-run-H0_20260225](./tracks/eval-run-H0_20260225/) | H0 control | Raw API |
| [eval-run-H1_20260225](./tracks/eval-run-H1_20260225/) | H1 Claude Code Sonnet | Claude Code |
| [eval-run-H2_20260225](./tracks/eval-run-H2_20260225/) | H2 Claude Code Opus | Claude Code |
| [eval-run-H3_20260225](./tracks/eval-run-H3_20260225/) | H3 Gemini CLI | Gemini CLI |
| [eval-run-H4_20260225](./tracks/eval-run-H4_20260225/) | H4 Codex CLI / GPT-4o | Codex CLI |
| [eval-run-H5_20260225](./tracks/eval-run-H5_20260225/) | H5 Qwen CLI | Qwen CLI |
| [eval-run-H6_20260225](./tracks/eval-run-H6_20260225/) | H6 Kilo Code | Kilo Code |
| [eval-run-H7_20260225](./tracks/eval-run-H7_20260225/) | H7 Copilot | GitHub Copilot |
| [eval-run-H8_20260225](./tracks/eval-run-H8_20260225/) | H8 Human Expert | Human |

### Later Historical Stages

- [ ] [Evaluation Scoring](./tracks/eval-scoring_20260225/)
- [ ] [Evaluation Analysis and Reporting](./tracks/eval-analysis_20260225/)

### Superseded

- [x] `eval-data-collection_20260225` — replaced by the per-condition historical run tracks; preserve its original artefacts and status.
