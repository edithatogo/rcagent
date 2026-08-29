# Tracks Registry

## Safety Systems Workbench Portfolio

- **Roadmap:** [conductor/roadmap.md](./roadmap.md)
- **GitHub roadmap:** [#1](https://github.com/edithatogo/rcagent/issues/1)
- **Execution policy:** [continuous autonomy](./autonomy.md) within declared
  owner decision gates; no routine stop between phases or tracks
- **Capability policy:** [portable core plus optional profiles](./capability-profiles.md)
  installed through verified scripts or an agent calling those same scripts

### Workstream A: Foundation and Governance

Parent: [GitHub #2](https://github.com/edithatogo/rcagent/issues/2)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [x] | [00 Agent Skills Living Conformance and Portable Architecture](./tracks/agent-skills-living-conformance_20260731/index.md) | [#5](https://github.com/edithatogo/rcagent/issues/5) | None |
| [x] | [01 Safety Systems Foundation and Solo-Developer Harness](./tracks/safety-systems-foundation_20260731/index.md) | [#6](https://github.com/edithatogo/rcagent/issues/6) | None; 00 remains a phase gate for licence/release scope |
| [x] | [02 Evidence Workflow Core](./archive/evidence-workflow-core_20260731/index.md) | [#7](https://github.com/edithatogo/rcagent/issues/7) | 01 |
| [x] | [03 Privacy, Security, and Assurance](./archive/privacy-security-assurance_20260731/index.md) | [#8](https://github.com/edithatogo/rcagent/issues/8) | 01 |
| [x] | [04 Jurisdiction Packs — National Baseline, NSW and Queensland](./archive/nsw-health-jurisdiction-pack_20260731/index.md) | [#9](https://github.com/edithatogo/rcagent/issues/9) | Completed; under-review NSW rules remain conditional |

### Workstream B: Data, Models, and Evaluation

Parent: [GitHub #3](https://github.com/edithatogo/rcagent/issues/3)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [x] | [05 Benchmark and Evaluation Harness](./archive/benchmark-evaluation-harness_20260731/index.md) | [#10](https://github.com/edithatogo/rcagent/issues/10) | Completed with negative comparator evidence |
| [x] | [06 Multimodal Capability Fabric](./archive/multimodal-capability-fabric_20260731/index.md) | [#11](https://github.com/edithatogo/rcagent/issues/11) | Completed with explicit negative-result support boundaries |
| [x] | [07 Retrieval and Knowledge System](./tracks/retrieval-knowledge-system_20260731/index.md) | [#12](https://github.com/edithatogo/rcagent/issues/12) | Completed with deterministic lexical support and explicit negative-result optional profiles |
| [ ] | [08 Local Runtime and Model Lab](./tracks/local-runtime-model-lab_20260731/index.md) | [#13](https://github.com/edithatogo/rcagent/issues/13) | 05, 06 |
| [ ] | [10 Domain Adaptation and Fine-Tuning](./tracks/domain-adaptation-finetuning_20260731/index.md) | [#15](https://github.com/edithatogo/rcagent/issues/15) | 05, 06, 07, 08 |

### Workstream C: Product, Interfaces, and Distribution

Parent: [GitHub #4](https://github.com/edithatogo/rcagent/issues/4)

| Status | Track | GitHub | Hard start blockers |
|---|---|---:|---|
| [ ] | [09 Interfaces, Templates, and Closed-Loop Actions](./tracks/interfaces-templates-action-loop_20260731/index.md) | [#14](https://github.com/edithatogo/rcagent/issues/14) | 02, 03, 04 |
| [!] | [11 Distribution, Registries, and Client Plugins](./tracks/distribution-registries-plugins_20260731/index.md) | [#16](https://github.com/edithatogo/rcagent/issues/16) | Release authorised; phase dependencies pending |

`metadata.json` records later phase dependencies that deliberately do not block independent foundation work.

### Cross-Cutting Quality Frontier

These issues refine existing tracks and must not become duplicate subsystems:

| Status | GitHub issue | Owning Conductor scope |
|---|---|---|
| [ ] | [#19 Clinical governance system-of-systems roadmap](https://github.com/edithatogo/rcagent/issues/19) | Track 01 architecture with first vertical slice across Tracks 02, 04, 07, and 09 |
| [ ] | [#17 Maximise security and solo-maintainer context](https://github.com/edithatogo/rcagent/issues/17) | Track 01 foundation harness, with Track 03 security assurance |
| [ ] | [#18 Complete evidence-based repository hardening](https://github.com/edithatogo/rcagent/issues/18) | Portfolio-level closeout; #17 is its tracked subissue |

Issue state is reconciled at every owning phase checkpoint. An issue is not
closed until its Conductor acceptance evidence and hosted repository state
both pass.

### Delivery Programme

- [~] [No-LLM Implementation Programme](./tracks/no-llm-implementation-programme_20260811/index.md) — sequential small PRs, one active branch, and no model-weight downloads

## Legacy Evaluation Study

These tracks remain preserved historical work. Track 05 will reconcile their schemas, cases, conditions, results, and limitations into the canonical benchmark harness without rewriting original artefacts.

### Completed and Pending Foundations

- [x] [Evaluation Protocol Development](./archive/eval-protocol_20260225/index.md)
- [ ] [Evaluation Case Collection](./tracks/eval-case-collection_20260225/index.md) — 7 NZ cases recorded; AU coverage and final QA remain pending

### Blocked

- [!] [Evaluation Pilot Calibration](./tracks/eval-pilot-calibration_20260225/index.md) — blocked by incomplete AU case coverage and unverified pilot evidence

### Historical Parallel Conditions

| Track | Condition | Recorded harness |
|---|---|---|
| [eval-run-H0_20260225](./tracks/eval-run-H0_20260225/index.md) | H0 control | Raw API |
| [eval-run-H1_20260225](./tracks/eval-run-H1_20260225/index.md) | H1 Claude Code Sonnet | Claude Code |
| [eval-run-H2_20260225](./tracks/eval-run-H2_20260225/index.md) | H2 Claude Code Opus | Claude Code |
| [eval-run-H3_20260225](./tracks/eval-run-H3_20260225/index.md) | H3 Gemini CLI | Gemini CLI |
| [eval-run-H4_20260225](./tracks/eval-run-H4_20260225/index.md) | H4 Codex CLI / GPT-4o | Codex CLI |
| [eval-run-H5_20260225](./tracks/eval-run-H5_20260225/index.md) | H5 Qwen CLI | Qwen CLI |
| [eval-run-H6_20260225](./tracks/eval-run-H6_20260225/index.md) | H6 Kilo Code | Kilo Code |
| [eval-run-H7_20260225](./tracks/eval-run-H7_20260225/index.md) | H7 Copilot | GitHub Copilot |
| [eval-run-H8_20260225](./tracks/eval-run-H8_20260225/index.md) | H8 Human Expert | Human |

### Later Historical Stages

- [ ] [Evaluation Scoring](./tracks/eval-scoring_20260225/index.md)
- [ ] [Evaluation Analysis and Reporting](./tracks/eval-analysis_20260225/index.md)

### Evidence Remediation

- [!] [Evaluation Blocker Remediation and Admission](./tracks/eval-blocker-remediation_20260803/index.md) — local controls complete; external Phase 4 execution evidence remains blocked

### Superseded

- **Superseded, not completed:** [Evaluation Data Collection](./tracks/eval-data-collection_20260225/index.md) — replaced by the per-condition historical run tracks; preserve its incomplete original artefacts.
