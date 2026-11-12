# Frontier assurance specification

## Problem and starting evidence

The 13 November 2026 assessment identified three reproducible defects: wrong-entity provenance references passed validation; a public export could retain private free text while changing its privacy label; portable instructions selected legacy templates with unconditional confidentiality/protection claims. The assessed commit was a895d42a8738d2937f849b65e3b892042f64b979. Integration starts from 50c8a81, which also contains the subsequently merged local-model planning note.

The assessed revision's [hosted Quality run 43292641115](https://github.com/edithatogo/rcagent/actions/runs/43292641115) passed the Linux, macOS and Windows jobs; the Linux job reported 1,786 tests and 95.29% coverage. This later receipt is separate from Track 12's older incorporation run, whose Windows job stopped at typing. None establishes semantic correctness, investigation quality, local model qualification or clinical effectiveness. Preserve seven-case deterministic fixture results, the negative Qwen comparator pilot and the separate zero-of-two admitted prospective run as distinct evidence.

## Goals and ownership

Repair the defects; enforce strict, reproducible and proportionate engineering; demonstrate useful components incrementally; assess triangulation by measured error reduction; qualify claims about frontier performance through matched comparisons; extend the existing death-review and clinical-governance learning loop without duplicating a system of record.

Track 12 retains scientific component/work-package ownership. Track 13 owns assurance, demonstration evidence and cross-component promotion. Track 14 owns NSW/Queensland death-review mappings. Corpus capture/extraction, research labels and downstream operational workflow remain with the existing named owners in Track 12's integration contract.

## Requirements

| ID | Priority | Requirement | Acceptance evidence |
| --- | --- | --- | --- |
| FA01 | Must | References resolve to the intended entity and statement kind, with valid relationship endpoints | Wrong-kind, unknown, duplicate, withdrawn and cross-case adversarial fixtures are rejected or explicitly represented |
| FA02 | Must | Public disclosure is an explicit allowlisted view; sensitive records cannot be relabelled public | Synthetic free-text canaries in every supported input text field fail or disappear from public views; governed export remains faithful |
| FA03 | Must | Portable workflows and package payloads use admitted, revision-bound templates | Corrected content, tamper/missing/unlisted-template failures, package-member checks; historical quarantine retained |
| FA04 | Must | Locked dependencies, broad lint/format, strict typing, security/dead-code checks and coverage are enforced | Local and hosted commands; justified legacy strict debt is measured and non-growing; new modules have zero baseline entries |
| FA05 | Must | Hypothesis and real mutation testing cover integrity boundaries; Scalene measures a representative synthetic workload | Actual property and mutant outcomes, fail-on-survivor threshold, profiling artifact with environment and workload size |
| FA06 | Must | Demonstrate source capture, typed claims and chronology before higher-order inference | D0–D3 demonstrations in the capability ladder; exact inputs, outputs, errors, versions and reproducible command |
| FA07 | Must | Every assertion remains bound to immutable source and permitted decision-time view | Exact span/number/negation/actor checks and time-entitlement tests; unsupported claims cannot become accepted findings |
| FA08 | Must | Compare rules/regex, NLP, encoders and generative systems under the same evidence and split | Per-task precision/recall, material omissions, failure severity, useful coverage, latency and memory |
| FA09 | Must | Separate method, model, modality and source independence | Origin graph and shared-error measurements; agreement does not manufacture evidence or authority |
| FA10 | Must | Missing/contradictory evidence, late information and absent family voice survive processing | Negative controls, contradictory accounts, outcome masking, no-harm and insufficient-evidence cases |
| FA11 | Must | Death reviews inherit the same provenance and authority constraints | Track 14 original workflow, official source matrix, jurisdiction-specific applicability, synthetic acceptance cases |
| FA12 | Must | Engineering completion and scientific/clinical capability claims remain distinct | Capability cards expose status, task, model/runtime/hardware/view, evidence date and exclusions |
| FA13 | Must | Solo-maintainer context and governance remain bounded and autonomous | One integration plus two implementation lanes; no routine approval prompts; three-role agent review with precise evidence |
| FA14 | Must | Evaluate selective Rust adoption against measured defects/resources and maintenance | ADR, fixed workload, Python/Rust parity and malformed-input results before an implementation decision |
| FA15 | Should | Demonstrate document layout/OCR and structured event-source triangulation before expensive clinical modalities | Modality-specific error/omission analyses and propagation study; no diagnostic inference from ingestion tests |
| FA16 | Should | Reuse Inspect AI, maintained NLP/ML and the existing Rust ecosystem through thin adapters | Fit-gap and exact-version tests; no duplicate general evaluation/process engine |
| FA17 | Should | Evaluate staged critics or diverse models only where they add value | Ablations against the best single model under matched total budgets, correlated-error and false-blocking analysis |
| FA18 | Should | Measure investigation-to-action learning and reviewer effort | Traceable mechanisms, action/outcome/balancing evidence and appropriate workflow observations |
| FA19 | Could | Evaluate active evidence acquisition, uncertainty-aware process conformance and causal simulation | Identifiability assumptions, predeclared loss/utility, held-out mechanisms and negative controls |
| FA20 | Won't now | Promise zero hallucinations, infer culpability/preventability, perform blanket Rust rewrite or promote an untested model | Explicit limitations and no capability promotion without evidence |

## Non-functional requirements

Every execution records source revision, package lock, model/tokenizer/quantisation/runtime/hardware, input/view/rubric/renderer versions, budgets, failures and exclusions. Input size, archive expansion, regex work, tool time, memory, retries and log retention are bounded. Sensitive case text stays outside repository fixtures and public CI artifacts. Schema validation uses offline local schemas. Only authorised tools and view-scoped retrieval are exposed to a model.

Full engineering checks are blocking where the tools can execute. Environment-unavailable checks remain unavailable, never converted into passes. Experimental clinical/model claims require their own qualification receipt. Existing legacy typing debt is frozen with an explicit migration queue; new code cannot expand it.

## Delivery and compatibility

Keep changes independently revertible. Preserve old source/study receipts; introduce new versions for changed output contracts and study definitions. Public export changes are intentionally fail-closed and require migration notes. Optional dependencies remain outside the portable Markdown package. No clinical source-of-record migration, hosted service, new private-data access or model download is implied by this specification.

## Completion standard

Initial delivery completes planning and the applicable FA01–FA05/FA13 engineering work only when implementation and review receipts support it. D1–D8 and empirical qualification remain open until actually executed. Complete the track only after every Must requirement has linked evidence, deferred Should work is explicit, and Conductor/Git/GitHub agree.
