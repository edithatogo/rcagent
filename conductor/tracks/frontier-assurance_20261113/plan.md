# Frontier assurance implementation plan

Continue automatically through ready tasks, review and bounded rework. Do not ask for routine approval. Record the recommendation and supporting evidence; the safe default is a bounded synthetic/local result with unqualified capabilities withheld. No failure authorises relaxing a gate or reusing a contaminated holdout.

## Repository-review incorporation — 16 November 2026

The [recommendation map and implementation order](./recommendations-20261116.md)
and [machine-readable planning view](./execution-order-20261116.json) refine the
existing 24 work packages; they do not add a parallel queue. The
[incorporation receipt](./recommendations-evidence-20261116.md) distinguishes
documentation delivery from pending implementation. D0 ownership and acceptance
remain unchanged. AcciMap #139 and HEAPS #140 retain their separate owners and
track namespaces; the coordinator reconciles their shared registration.

- [ ] Follow-up to accepted FAW01 (R01): make `interface_actions.render_view` consume the canonical domain validator; reproduce and reject unknown-source, duplicate-ID and invalid-transition records at the rendering boundary. Preserve valid-record, hash, audience and privacy behaviour. This follow-up does not rewrite historical FAW01 acceptance and can run alongside D0 only in a separately assigned, non-overlapping scope.
- [ ] FAW06 maintenance / CAW02/08 (R02): measure validator construction and duplicate-ID checks; reuse cached immutable validators and `collections.Counter` where justified, preserve versioned hash contracts, and refactor only bounded responsibilities. The completed typing migration remains accepted.
- [ ] FAW18 / FA12–13 delivery metadata (R07): derive a capability/status view from existing registries and receipts, separating release, implementation, synthetic testing, benchmark, workflow and operational evidence. No duplicate manual registry or model qualification is introduced.

Priority: finish owned D0 and the renderer follow-up, then D1 → D2 → D3;
qualified component comparisons and final-output admission support selected D6
composition, then D7 evidence and conditional D8 extensions. Source/rights,
profile and dependency preparation may run in assigned parallel scopes. A
text-only deterministic D6 need not wait for every optional model, OCR or process
experiment. Later implementation remains pending coordinator file-scope
assignment under existing authority, rather than being claimed by this plan.

## Phase A: Repair and strict engineering

- [x] FAW01: repair typed entity/relationship references and add adversarial regression tests (FA01; evidence core and its tests; PR127 merged, hosted Quality43400688051 passed).
- [x] FAW02: replace unsafe public relabelling with an explicit public-view boundary; document compatibility and canary tests (FA02; accepted with PR127).
- [x] FAW03: correct portable templates, hash-bind current admission and enforce selection/package invariants; preserve historical quarantine (FA03; accepted with PR127).
- [x] FAW04: lock CI installation; broad Ruff plus format; strict basedpyright and measured legacy baseline with no growth (FA04; accepted with PR127, remaining debt belongs to FAW06).
- [x] FAW05: add Hypothesis, pytest-gremlins, Scalene, Bandit and Vulture with real invocations and meaningful failure behaviour (FA05; accepted with PR127).
- [x] FAW06: complete active source/test typing migration. All 3,198 remaining diagnostics are removed across 153 Python files; the baseline and allowances are empty, and explicit Any is an error. Checked raw boundaries, typed receipts and reviewed package/lifecycle APIs preserve rejection ordering and single-use witnesses. Source `c3d26b0c70a65f06dcab9f878db99d351de7b758` passed all nine Quality jobs in [run43553845148](https://github.com/edithatogo/rcagent/actions/runs/43553845148), plus dependency/privacy/conformance. Current runtime identities are distinct from unchanged consumed research source/protocol/review/results. See [completion evidence](./typing-completion-evidence.md); final documented-head checks and protected delivery remain required and will be recorded on [PR #131](https://github.com/edithatogo/rcagent/pull/131).
- [x] Checkpoint A: source engineering acceptance verified by local/hosted gates and three-role agent review, with rollback notes and immutable receipts. Final publication requires the exact documented-head gates and protected merge on [PR #131](https://github.com/edithatogo/rcagent/pull/131); the receipt distinguishes that delivery step from observed source acceptance.

## Phase B: Incremental component demonstrations

- [~] FAW07 / D0: publish one deterministic demonstration command and receipt format over generated synthetic cases; inspect actual output, not status text (CAW02/08, FA06). The [bounded acceptance and ownership contract](./faw07-d0-contract.md) assigns the existing implementation PR #132 and independent verification PR #133; the coordinator alone owns shared contracts, CI and merges. [Reconciliation](./faw07-d0-coordination.json) records exact observed heads and outstanding gates. D0 is not yet accepted.
- [ ] FAW08 / D1: demonstrate bounded dates/times/units/negation and exact source-span extraction, including invalid/ambiguous expressions (CAW02/04/08).
- [ ] FAW09 / D2: demonstrate timeline/partial-order assembly with event, recording and recipient-availability clocks; preserve disagreement and unknown order (CAW10, CS03).
- [ ] FAW10 / D3: demonstrate decision-time packets and patient/family concern traceability; hide future outcome/appraisal through every retrieval/verification/rendering path (CAW10/20).
- [ ] Checkpoint B: pass the finite oracle suite and property/metamorphic tests; publish precision/recall and abstention on held-out component examples without calling them clinical validation.

## Phase C: Measured triangulation and hallucination reduction

- [ ] FAW11 / D4: compare regex, token/section/ConText NLP, conventional classifiers and structured local generation with the same case-family split and labelled resources (CAW04–09/21).
- [ ] FAW12 / D5: conditionally test document text/layout/OCR and structured event-log agreement; differentiate duplicated source representations from independent evidence. CAW15 applies only to the optional synthetic-world rendering experiment, CAW16 to source-to-trace work; neither is a universal prerequisite for a source-native text packet. Admit Docling or another maintained parser only for a measured ingestion need (R04).
- [ ] FAW13: compare single model, same-model critic, diverse-model verifier and independent rule/NLP checks; score joint failures and useful disagreement (CAW21/22).
- [ ] FAW14: freeze and test claim admission, opposing-evidence retrieval, critical-omission audit, calibrated abstention and bounded repair; reverify final prose. Test correction/withdrawal propagation to dependent claims, views, exports and action justifications while retaining unaffected outputs and immutable history (R05/R08; CAW08/10/20, with CAW09/21 for included generative arms). Controlled experiments CAW11/12 are research comparisons, not prerequisites for every deterministic renderer.
- [ ] FAW15: validate actual local data/egress/log/cache isolation with canaries and adversarial traffic; isolated-host tests remain external-environment work, not paper evidence.
- [ ] Checkpoint C: retain a simpler arm if additional models/modalities fail the predeclared error/coverage/burden contrast. No majority vote overrides a failed deterministic boundary.

## Phase D: Frontier evidence and death-review composition

- [ ] FAW16 / D6: compose individually qualified components into a reproducible investigation/death-review packet; test propagated errors, source corrections/withdrawals and reviewer corrections (R06/R08; Track 14 DR-04–12 and CA08–CA12). Prepare packet fixtures after D3; acceptance requires the renderer follow-up, FAW14 final-output checks and qualification of every included component. CAW19 applies only to included process studies and CAW21 to included generative arms; optional D4/D5/process experiments do not block a qualified text-only packet. Consume AcciMap/HEAPS handoffs through their existing owners.
- [ ] FAW17 / D7: execute a frozen external/temporal holdout against a competent same-model prompt, portable skill, strongest conventional baseline and staged system (CAW22).
- [ ] FAW18: report case-clustered uncertainty, material-error/omission/coverage metrics, severe errors, concern fidelity, false blocking, model costs, hardware resources, correlated judges and failure denominators; refresh comparator literature at freeze. Admit applicable LRRT/IGZ rubric items with source/version/rights and rating-reliability evidence; derive capability cards from existing receipts (R07/R09).
- [ ] FAW19: observe appropriate users/reviewers only for claims requiring workflow, judgement or patient-benefit evidence; agent engineering review continues independently. Consider ordinary review versus a deterministic viewer versus viewer plus generated assistance, with randomised/counterbalanced allocation, unsupported-claim detection, correction time and reliance measured where feasible (R10).
- [ ] Checkpoint D: publish a research qualification or rejection card for an exact task/configuration. A frontier claim requires useful improvement over current relevant baselines, not just a new architecture.

## Phase E: Beyond-frontier hypotheses and selective Rust

- [ ] FAW20: run the ADR's bounded Rust spike for streaming evidence/span/temporal validation or a local worker boundary; compare parity, memory, p95 latency, packaging and maintainability.
- [ ] FAW21 / D8: evaluate uncertainty-aware temporal/process reconstruction and active evidence questions at fixed evidence budget (CAW17–19/24); use Voiage/Rust4PM only through admitted interfaces.
- [ ] FAW22: evaluate action mechanism and recurrence/effectiveness monitoring; measure workflow effects separately from text quality and causal patient benefit (CA12).
- [ ] FAW23: replicate promising effects across a new source/jurisdiction/hardware condition and assess drift, distribution shift and calibration failure.
- [ ] FAW24: attempt adaptation only after error analysis justifies it; compare against the strongest untuned arm, with frozen family splits and rejection criteria (CAW23).
- [ ] Checkpoint E: retain negative findings; revise scientific hypotheses prospectively. 'Beyond frontier' is a research aim until evidence supports a bounded claim.

## Execution, dependencies and rollback

Phase A may run in parallel with public-source planning and fixture design. B consumes repaired source/provenance boundaries. C consumes qualified extraction/view contracts; D consumes its qualified components and Track 14 applicability. E experiments are conditional and never block a useful deterministic timeline product.

FAW01–05 are accepted in merged PR127 after complete hosted Quality, dependency,
privacy/secrets and official conformance success. FAW06 was delivered through
PR #131 at `419c04d7e1c0a16e924e0b7058604671855625a2`; final-head Quality43555675618
and merged-master Quality43556852077 both passed all nine jobs, with
privacy/secrets and official conformance success. This updates the Phase A
publication-time statements above without rewriting their source receipts.
The current bounded D0 implementation increment remains FAW07 / D0 only, using
the two named ordinary ChatGPT workers and the sole integration coordinator.
The separately authorised 16 November planning refinement and AcciMap/HEAPS
owner lanes do not expand those workers' file scopes. The implementation has distinct CLI/server admission and
phase-dependent probe receipts, checked optional/native output, typed autonomy,
evidence, retrieval, benchmark, privacy, panel and evaluator contracts, and
reviewed package/test APIs. Preserve early rejection, oversized-stream hash
withholding, timeout/launch-failure states, repeated pin checks and single-use
observation witnesses. Checked container shapes alone do not validate domain
values. Current engineering source revalidation does not revise historical
study declarations or revive consumed protocols. The next
staged capability programme maps into existing CAW02/04/08/10/20 rather than
creating duplicate implementation counters. FAW08–10, model/modality work and
Rust remain outside the current D0 increment. Model/hardware/data-dependent
leaves may wait while software work continues. No elapsed research-time promise
is inferred from coding-agent speed.

Revert individual implementation commits or disable an optional adapter; preserve original datasets, receipts, negative results and prior release artifacts. Tightened disclosure behaviour must never be rolled back merely to make an unauthorised export succeed.
