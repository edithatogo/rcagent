# Decision models implementation and verification plan

Status: **DM01 documentation and agent verification complete; exact-head hosted checks and the authorised merge are recorded separately in PR #147**. The earlier specification-only delivery is preserved in [planning-evidence.md](./planning-evidence.md). The 17 November 2026 bounded increment delivers the context, source-admission and frozen study-definition package; DM02–DM11 remain pending.

Continue automatically through DM01, review, bounded rework, exact-head checks and the authorised merge. Record the recommendation, supporting evidence and safe default. Retain owner decision gates for genuinely new data/rights, spend, egress, deployment and irreversible actions. Stop after DM01; the named increment does not start DM02 or execute a model.

## Execution and ownership contract

Use the [workflow](../../workflow.md), [constraints](../../../CONSTRAINTS.md), [specification](./spec.md) and [proposed contracts](./contracts.md). Track 12 owns scientific components, Track 13 owns shared assurance/integration, and Track 14 owns death-review applicability. Preserve AcciMap #141, HEAPS #142, recommendations #143 and coordinator `6af6164f-cf84-8321-9f96-8b7d685aabe5`. Reconcile fresh branch heads, receipts and file ownership before claiming any task. A production namespace in this plan is a proposal until the coordinator allocates it.

Each package follows fixture-first red–green–refactor: specify a discriminating failing case before implementation, add the smallest adapter/domain mapping, then run focused and applicable full checks. Tests do not replace source/rights admission, model measurement or accountable decisions. All future model/data work is public/synthetic or inside an already established exact approval; an unavailable dependency blocks only its consuming scope.

Do not duplicate generic engines. Reuse JSON Schema/typed ports/SQLite FTS5, optional maintained model/linker packages, scikit-learn/SciPy metrics and Inspect AI where appropriate. A project-owned shim needs a documented remaining gap, upstream reference, owner, compatibility window and removal test.

## Dependency order and parallel work

| Package | Depends on | May proceed independently | Existing receiving scope |
|---|---|---|---|
| DM01 Context, sources and study definition | User authority received 17 November 2026 | Source/rights inventory and protocol preparation | CAW01–03, CAW22 |
| DM02 Contract and file-allocation checkpoint | DM01 | Model-free schemas and independent fixture design | CAW02/08; Track 13 shared contracts |
| DM03 One admitted text decision adapter | DM02 | Parallel with DM04; no need for ontology/audio | CAW07/09; runtime measurement/isolation |
| DM04 References, baselines and benchmark plumbing | DM02 | Parallel with DM03, using synthetic/mock observations | CAW03–06/08/20–22 |
| DM05 Text workflows and triangulation | DM03, DM04; relevant D1–D3 contracts | Routing/completeness can precede extraction/timeline consumers | FAW08–14; CAW08–10/20–21 |
| DM06 Terminology retrieval/re-ranking | DM03, DM04; exact terminology rights | Optional lane after stable ports; not a blocker for text study | CAW06/09/21; retrieval contracts |
| DM07 Image/audio branches | DM03, DM04; modality admission | Each modality separate; omit from initial text study | FAW12; multimodal contracts |
| DM08 Calibration and frozen analysis | DM04; DM03/DM05 observations for fitting | Metric/report fixtures can precede model availability | CAW03/21/22; FAW18 |
| DM09 Holdout comparison and replication | DM05, DM08; DM06/DM07 only if included | No tuning after holdout access | FAW13/17–19/23; CAW22 |
| DM10 Optional service and consumer dry run | DM09 for its selected tuple, isolation evidence | Separate from pure offline research conclusion | FAW15; existing interface contracts |
| DM11 Reconciliation, qualification/rejection and handoff | DM09; DM10 only if service is claimed | Negative research results can close bounded packages | Track 12/13/14 owners |

The first useful sequence is **DM01 → DM02 → (DM03 and DM04) → DM05 → DM08 → DM09**. Calibration tooling in DM08 can begin during DM03/DM05 once its fixtures exist. DM06 and DM07 are conditional branches, not prerequisites for all work. Use at most one integrator and two non-overlapping implementation lanes; review agents do not acquire production ownership. No new chats or agents are scheduled by these documents.

## Phase A: Admit the question and freeze contracts

- [x] **DM01.1 — Reconcile current context.** Refresh master, open PRs, Track 12/13/14 state, the renderer/domain-validation repair and D1–D3 receiving contracts. Reserve only owned files; record base/tree and the current user's explicit DM01/merge authority. Shared production-contract allocation still requires its receiving agreement in DM02; no coordinator acknowledgement is inferred. Accept when the bounded context pack and dependency map distinguish ready from blocked leaves.
- [x] **DM01.2 — Admit candidate sources and rights.** Pin current model/code/tokenizer/processor/licence/runtime/API documentation and exact terminology/data releases. Record remote-code and hosted-boundary conflicts. Use the source register as discovery input, not an immutable model manifest. Accept when unavailable or rights-uncertain candidates are explicitly excluded from execution rather than silently substituted.
- [x] **DM01.3 — Freeze the first research task.** Select a bounded public/synthetic text task, intended user, target hardware, primary material-error contrast, useful-coverage floor, severe-event endpoint and annotation protocol. Fix numerical margins, precision/sample-size plan, threshold selection, split lineage and stopping rules before holdout access; label pilot estimates as exploratory. Preserve existing HDC authority only within its established scope.
- [x] **Checkpoint A1.** Agent reviewers examine acceptance, evidence integrity and safety/privacy. Publish a source/fit-gap receipt, decision log and ready/blocked map. Do not mark model/runtime or clinical capability supported.

DM01 acceptance: [context and receiving map](./dm01/context-pack.md), [source admission](./dm01/source-admission.md), [frozen study](./dm01/study-protocol.md) and [verification/review receipt](./dm01/verification.md). The original and integrated local full gates retain their environment failures; final-head hosted checks are required before merge. DM02 has not started.

- [ ] **DM02.1 — Complete request/output schemas.** Convert the documented primitive/envelope design into versioned JSON Schema and checked Python types in coordinator-allocated files. Freeze provider-native versus canonical semantics, status/error precedence, source/view/hash domains, limits, calibration and thresholds. Keep Pydantic optional and avoid changing canonical safety-work records without receiving agreement.
- [ ] **DM02.2 — Write independent contract fixtures first.** Cover C01–C42 in the contract appendix, including missing versus null, `found` just below/equal/above 0.5, exclusive/multi-label probabilities, score direction, unit/date/box validation, unsupported runtime features, timeouts and privacy/authority vetoes. Add Hypothesis combinations that exercise real boundary risks.
- [ ] **DM02.3 — Agree shared mappings and rollback.** Obtain coordinator acceptance of ports, statuses, registry mapping, paths and exact existing validators to consume; supply proposed changes through that owner. Define backwards compatibility, invalidation and adapter-disable behaviour. Do not treat document existence as interface acceptance.
- [ ] **Checkpoint A2.** Validate schemas against independent valid/invalid examples, JSON/links and the dependency graph; review complete error and missing-value behaviour. Run affected existing evidence/port/privacy tests and the applicable full gate. Record exact source bytes, commands, failures and acceptance before parallel implementation.

## Phase B: Build the smallest measurable text comparison

- [ ] **DM03.1 — Select one compatible execution path.** Compare maintained reference/local runtimes on the task's actual primitive needs. Reject an inadmissible remote-code path under current policy; if a reviewed packaged implementation is proposed, qualify its full boundary before use. Do not enable a forbidden path by changing a flag or moving it into a sidecar.
- [ ] **DM03.2 — Implement the thin wire adapter against fixtures.** Add capability negotiation, request/result parsing, duplicate/non-finite rejection, deadlines/cancellation, bounded transient retry, idempotency and unavailable-state handling. Keep raw provider values and exact model/transport identities. Reuse the existing operation and privacy concepts; do not reinterpret `/completion` as System One.
- [ ] **DM03.3 — Execute a separately admitted synthetic measurement probe.** Pin model assets and run the minimum exact-tuple local inference outside any operational workflow, under the existing measurement protocol. Record actual primitives/modalities, cold/warm latency, resources, errors and egress observations. Only a measured receipt can support later runtime registry admission; mocked passes never create one.
- [ ] **Checkpoint B1.** Independently reproduce wire negatives, fallback/cancellation and at least the admitted local task. Verify local-only behaviour, no implicit download/telemetry and source hash/candidate preservation. Run focused tests then full applicable validation and exact-head hosted checks. An unavailable runtime is a recorded unsupported result, not a fabricated pass.
- [ ] **DM04.1 — Build a source-bound reference set.** Reuse existing fixture conventions and CAW02/03 grouping. Create independently authored synthetic missing/contradictory/high-severity/negative cases and original invariance variants. Record source lineage, labels, adjudication, reviewer class and rights; freeze family assignments before fitting anything.
- [ ] **DM04.2 — Establish suitable baselines.** Reuse deterministic rules/FTS5; add maintained classical/encoder conditions only if admitted. Define a competent task-matched generative comparator with immutable prompts and constraints. Keep mandatory privacy/provenance checks in every arm; preserve historical comparator receipts separately.
- [ ] **DM04.3 — Extend the benchmark through an adapter.** Reuse existing manifests/receipts and optional Inspect AI solver/scorer integration; preserve native decision probabilities without pretending they are generated text. Account for malformed/unavailable/error/abstention outcomes and infrastructure failures separately, with complete attempt/resource denominators.
- [ ] **Checkpoint B2.** Test the harness on independently calculated metric fixtures, all-abstain and malformed-output controls, a missing true retrieval candidate and grouped leakage probes. Confirm replayability and no holdout/reference answer leakage. Run affected benchmark/retrieval/native-completion regressions, full applicable validation and review.

## Phase C: Apply text decisions with explicit triangulation

- [ ] **DM05.1 — Intake and eligible routing.** Map Noul/Choice to completeness, privacy suspicion and permitted skill/team/tool candidates. Preserve urgent escalation for incomplete reports, NIL/insufficient outcomes, deterministic permissions and ownership. Tests must show that high confidence cannot execute an unauthorised tool or clear detected PII.
- [ ] **DM05.2 — Source-linked extraction and ordinal review.** Consume accepted D1–D3 source/span/time-view interfaces. Map text/number/date candidates with original-byte provenance; preserve units, temporal uncertainty and availability. Add separate severity/harm/reportability rubrics only with source-qualified semantics. Test tail risk, reversed label directions and `found` boundaries.
- [ ] **DM05.3 — Implement the comparison/abstention policy.** Bind all methods to the same permitted view; retain source-family/method/model/modality lineage. Apply the specified hard vetoes, sensitive review thresholds, conflict handling and bounded local escalation. Test duplicate evidence, correlated critics, high-entropy and confidently wrong outputs.
- [ ] **DM05.4 — Add bounded QA and optional loop/RAG advice.** Score concern coverage and corrective-action criteria separately. Compare risk statements using the same rubric. Preserve critical/opposing evidence in context selection; budgets and terminal evidence remain deterministic. Do not make action effectiveness, approval or blame labels from scores.
- [ ] **Checkpoint C.** Execute C01–C42 controls relevant to the admitted text path plus existing evidence/privacy/interface/autonomy regressions. Independently inspect natural and injected failures and false blocking. Record exact contracts and eligible scopes; unresolved rendering/approval defects stay with the shared owner and block only consumers that need them.

## Phase D: Conditional terminology and modality branches

- [ ] **DM06.1 — Admit a terminology task.** Choose the specific SNOMED CT/ICD-10/ICD-10-AM/local ICPS/HFACS use case and exact edition/rights. Define mention, assertion, NIL, granularity and mapping rules; do not combine non-equivalent classifications. Keep restricted terminology and vectors out of public artefacts.
- [ ] **DM06.2 — Benchmark retrieval before adding complexity.** Measure FTS5 recall@K; test an admitted SapBERT/KRISSBERT/MedCAT route only when it addresses an observed gap. Use FAISS/Qdrant or another maintained optional index only where justified. Preserve candidate IDs, rank, source and edition hash.
- [ ] **DM06.3 — Add capability-matched re-ranking.** Use single Choice for disambiguation or multi-label Choice for independent factors. Include missing-gold, NIL, ambiguity, inactive-code, negation/uncertainty/experiencer and option-order cases. Report candidate-conditioned and full-pipeline errors separately.
- [ ] **Checkpoint D1.** Compare lexical, encoder/linker-only and re-ranked conditions on identical family splits. Verify source/code membership and rights; preserve negative results. Run retrieval/adapter integration checks, independent review and full applicable gate before supplying an optional condition to DM09.
- [ ] **DM07.1 — Qualify image inputs separately.** Admit synthetic/public screenshots/document regions; verify media limits, hashes/transforms, coordinates, prompt injection and privacy metadata. Compare direct decisions with text/OCR and separate representation agreement from independent-source corroboration.
- [ ] **DM07.2 — Qualify audio only if warranted.** Verify exact audio-capable tuple, duration/language envelope, recording rights and timecode binding. Compare direct decisions with an admitted transcript path; include number/negation, noise, accent, missing audio and uncertain-speaker cases. No transcript or diagnosis claim from a decision-only output.
- [ ] **Checkpoint D2.** Record modality-specific errors, missingness, resource use and impact over text-only at the same evidence budget. Reject unsupported modalities and all silent truncation. Do not block or enlarge the first text study solely to include an optional modality.

## Phase E: Calibrate and evaluate without holdout tuning

- [ ] **DM08.1 — Add maintained metrics and independent numerical controls.** Implement thin wrappers for binary/multiclass/multi-label Brier, prespecified-bin ECE/reliability, log loss where applicable, severe-tail/ordinal scores, recall@K and selective risk/coverage. Check known values, class ordering, empty/missing denominators and all-abstain behaviour; state Brier scaling and undefined outcomes explicitly.
- [ ] **DM08.2 — Fit calibration and thresholds on reserved data.** Compare simple suitable calibration methods with grouped/nested handling if required. Bind every calibrator and policy to the full task/model/runtime/precision/rubric/candidate procedure/population identity. Freeze the operating point and coverage/safety margins before the holdout; report insufficient positive cases honestly.
- [ ] **DM08.3 — Freeze the paired analysis and cost ledger.** Register R/C/G/D/H arms, limited ablations, case-family uncertainty, subgroup scope, multiplicity, stopping/exclusion rules and primary versus exploratory metrics. Include cold/warm p50/p95/p99, queues/preprocessing, errors/retries/fallbacks, RAM/VRAM and human review burden; no vendor benchmark substituted for measurement.
- [ ] **Checkpoint E1.** Acceptance/evidence/safety reviewers audit split isolation, reference independence, candidate-set conditioning, probability semantics and numerical controls. Confirm adequate precision or explicitly exploratory status; seal the final-test manifest and protocol before execution.
- [ ] **DM09.1 — Execute the frozen comparison.** Run the same authorised evidence/task for standalone generative, decision-only and triangulated hybrid arms plus rules/classical baselines. Attribute fallback successes to the cascade. Preserve all eligible attempts, raw results, errors and unmodified protocol/source identities.
- [ ] **DM09.2 — Analyse and replicate the claim.** Report case-family paired material-error differences, severe-event sensitivity/FNR with intervals, calibration, useful coverage, joint errors and resources. Add original symmetry-inspired and genuinely changed-evidence controls; replicate promising findings on the declared temporal/source/runtime holdout. Do not claim to reproduce private AA-Symmetry.
- [ ] **DM09.3 — Make a bounded qualification decision.** Apply the prospectively frozen margins; retain the simplest satisfactory arm. Publish a task/configuration qualification, rejection or inconclusive card with uncertainty and remaining limitations. A small pilot, agent panel or green software gate cannot establish clinical effectiveness.
- [ ] **Checkpoint E2.** Independently reproduce analysis from immutable receipts; reconcile source/model/data rights, all failures and denominators. Require the exact applicable software gates and study criteria. Preserve negative evidence and never retune/relabel a consumed holdout to obtain a pass.

## Phase F: Optional deployment design, integration and closure

- [ ] **DM10.1 — Establish the need for a service.** Prefer the existing worker/CLI boundary. If a local service is justified, specify an optional FastAPI/Pydantic adapter with schema parity, authentication, caller scope, backpressure, health/capability negotiation, cancellation, safe logging and retained local-only data boundaries. ONNX conversion remains a separately measured parity experiment.
- [ ] **DM10.2 — Test the actual service boundary.** Run admitted synthetic requests under load and failure injection; test attempted egress, cache/log/temp leakage, request/media limits, replay and remote-code restrictions. Verify actual isolation rather than declarations. Operational/private use remains gated by applicable authority.
- [ ] **DM10.3 — Prepare an enterprise consumer dry run only if requested.** Reuse the existing dry-run contract. Document Power Automate/gateway/cloud-history data flow and minimum metadata; no new connector, credential, external message or records update without its established authority.
- [ ] **Checkpoint F1.** Independently compare in-process and service semantics, latency/resources and privacy evidence for the selected tuple. Demonstrate disable/uninstall rollback and exact hash/calibration invalidation. If no service is needed, record the justified deferral; it is not a blocker for a completed offline study.
- [ ] **DM11.1 — Reconcile with existing owners.** Supply accepted component receipts and concrete shared-registry/schema proposals to the integrator; update only allocated files. Track 12 receives scientific results, Track 13 assurance/promotion, and Track 14/AcciMap/HEAPS only their actually qualified consumption contracts.
- [ ] **DM11.2 — Verify and close the bounded result.** Run full applicable validation, exact-head CI and fresh-context review; record commands, failures, immutable revisions, limitations, review disagreements and rollback. Mark tasks complete only with evidence; map omitted optional branches explicitly. Keep deployment and unsupported capabilities visible.
- [ ] **Checkpoint F2.** Verify that specification acceptance, plan, metadata, GitHub, source state and receipts agree. Preserve archived studies and all negative findings; leave merge/release decisions with the existing authorised owner. Stop at the currently authorised boundary.

## Verification commands and receipts

The original planning change used the repository validator, JSON/schema-fragment and link/path checks, source/ownership review and `git diff --check`. DM01 additionally verifies immutable source identifiers, protocol arithmetic and cross-file consistency, uses the locked repository checks, and requires exact-head hosted checks before the authorised merge. No model call or empirical performance result is part of DM01 verification.

For DM01 and future implementation, use the repository's locked commands:

```bash
uv sync --locked --extra validate --extra test --extra lint --extra assurance
uv run --no-sync python -m tools.full_validation
```

Run meaningful focused tests during development, then the applicable phase gate. Preserve zero typing allowances, 90% branch coverage, mutation/security/quality gates and full supported-platform tests. Record unavailable local environments as unavailable, not passed; exact-head hosted evidence remains separate. A new optional model profile requires its own lock/compatibility/actual-runtime evidence without bloating the portable core.

Each receipt records task, base/head/tree, environment, privacy mode, actual commands, dependency/model/runtime/device/data/ontology versions and hashes, observed results, uncertainty, raw-evidence location, deviations, reviewer class, authority limits and rollback. Use synthetic/public-safe material in public receipts; private source content and low-entropy sensitive hashes must not be exposed through logs or external artefacts.

## Rollback

This proposal can be withdrawn by reverting only its documentation/registry commit. Future changes must allow disabling an optional adapter and restoring the authorised rules/manual path while retaining source records and historical receipts. Do not delete evidence or revert safeguards to make a failed model, export or connector appear usable.
