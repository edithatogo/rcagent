# Component qualification for cognitive autopsy and RCA

## Existing structure and actual evidence

The portable RCA skill has four workflow stages: triage, investigate, report and track. The broader workbench adds evidence/provenance, retrieval, systems methods, jurisdiction profiles, privacy routing, local runtime admission, interfaces and action follow-up. These are workflow and software capabilities, not a demonstrated general RCA model.

Relevant implementation includes [workbench](../../../tools/workbench.py), [retrieval](../../../tools/retrieval_system.py), [privacy assurance](../../../tools/privacy_assurance.py), [benchmark harness](../../../tools/benchmark_harness.py), [local comparator](../../../tools/local_model_comparator.py) and [runtime lab](../../../tools/runtime_lab.py). The [existing comparator pilot](../../../evaluation/benchmark/results/local-comparators-v1.md) obtained schema-valid output in all 63 observations but only 3 strict passes, across seven synthetic cases and repeated fixed-seed runs. The repeats were identical within case/model. These results neither qualify a model nor establish 63 independent cases. The [runtime matrix](../../../evaluation/runtime-lab/recommendation-matrix-20260829.json) contains no supported model/device profile.

## Proposed component contracts

| ID | Component and existing home | Required input → output | Evaluation before promotion |
| --- | --- | --- | --- |
| CA01 | Source capture and text fidelity; evidence core / corpus adapter | Immutable source and page/paragraph coordinates → faithful text with extraction uncertainty | Character/span fidelity; critical doses, units, negation and tables; duplicate/version linkage; no silent missing text |
| CA02 | Claims, accounts and provenance; evidence core | Source spans → typed fact/account/inference, actor role, contradiction and citations | Supported-claim precision/recall, assertion status, provenance coverage and unsupported attribution |
| CA03 | Temporal and epistemic reconstruction; new extension | Evidence plus event/document/availability times → decision-time information state | Temporal relation accuracy; uncertain availability; clinically material late-information leakage |
| CA04 | Decision opportunities; new extension | Timeline and contemporaneous evidence → decisions, omissions, deferrals, escalation opportunities | Recall and precision against documented opportunities; reasonable choices retained; no event invented as a decision |
| CA05 | Decision context and alternatives; new extension | Decision-time state → documented goals, cues, constraints, options and missing information | Source-grounded coverage; unsupported rationale rate; feasible alternatives; separation of observed and hypothetical cognition |
| CA06 | Retrieval and historical standards; retrieval / jurisdiction tracks | Scoped question, permitted compartment, time and jurisdiction → cited evidence packet | Evidence recall/ranking, correct policy version, no outcome leakage, no NZ-to-Qld authority substitution |
| CA07 | Cognitive hypotheses and uncertainty; new extension | CA02–CA06 → qualified hypotheses, competing accounts and abstention | Unsupported bias/blame, calibration, selective risk/coverage, negative controls and response to relevant evidence |
| CA08 | Systems contributors and barriers; existing investigation methods | Grounded decisions plus context → SEIPS/AcciMap/other method-specific relationships | Traceable links, preservation of system conditions, contradictions; causal claims no stronger than evidence |
| CA09 | Patient/family perspective and equitable learning; participation/action tracks | Documented concerns, goals, communication/access needs → concern-to-response trace | Material concern omission, distortion, accessibility and documented equity context; missing voice explicitly acknowledged |
| CA10 | Recommendations and learning; action-loop track | Supported hazards and alternatives → mechanism, owner, intended benefit, burden and balancing measures | Actionability, evidence link, strength/feasibility, patient relevance and foreseeable unintended effects |
| CA11 | Report synthesis and verification; report/interface tracks | Qualified component outputs → auditable narrative with unresolved issues | Cross-component consistency, material omission, citation support, readable uncertainty, no promotion of hypothesis into finding |
| CA12 | Closed-loop learning; track/action-effectiveness track | Authorised action and observed follow-up → implementation and effectiveness records | Completion distinct from effectiveness; actual outcome and balancing measures; no inferred patient benefit |

Privacy, access control, source rights and audit are cross-cutting hard constraints, not optional components that can be averaged against quality.

## First experimental slice

Begin with CA01–CA05 and CA09, using bounded text passages and then full decision episodes. Evaluate CA06 for the retrieval arm. CA07 is research-only hypothesis generation; CA08–CA12 require additional task-specific evaluation. A component can be useful for extracting documented options while unsuitable for judging decision quality.

The decision record contains source IDs/spans; decision time and uncertainty; actor role; information known/unknown/uncertain at that time; goal; documented options; action or deferral; resource/team constraints; patient/family preferences if documented; rationale provenance class; competing explanations; missing evidence; and separate later outcome/appraisal links. Hypothetical alternatives are visibly labelled and never inserted into the original chronology.

## Qualification ladder

1. Contract-valid: schema and deterministic behaviour only.
2. Benchmark-measured: results on a specified held-out source/task, including negative results.
3. Research-qualified: predeclared task gates passed within a bounded context.
4. Workflow-evaluated: actual intended users and workflow observed where those claims are made.
5. Operationally authorised: accountable organisational decision and monitoring for the exact setting.

The promotion key is the tuple of component, task, source/domain, jurisdiction, model and tokenizer revision, quantisation, runtime revision, hardware, context envelope, prompt/retrieval revision and privacy mode. A new tuple starts unqualified. Drift invalidates affected receipts.

## Advanced additions with a purpose

Use a provenance-linked decision graph with three clocks; calibrated abstention and risk/coverage curves; contradictory-evidence retrieval; controlled changes to outcomes versus genuinely available cues; contamination probes and recent-case holdouts; an error-driven local model cascade; and composition testing. Add counterfactual simulations only after a validated mechanism exists. More agents, longer reasoning or a larger context window are experimental conditions, not evidence of better clinical reasoning.

## Small-study entry points

CS01 tests CA01/CA02/CA09 assertion, account and concern fidelity; CS02 tests CA01/CA02/CA06/CA11 verification; CS03 tests CA03–CA05 availability and outcome sensitivity. CS04 risk framing and CS05 synthetic mechanism recovery are controlled research conditions. CS06 tests CA03/CA08/CA11 process reconstruction and propagated errors. CS07 adaptation and CS08 value-of-evidence are conditional extensions. See the [unexecuted catalogue](../../../evaluation/cognitive-autopsy/experiment-catalogue.json).

Rule-based NLP, classical supervised ML and compact encoders are independently measured comparators. A semantic verifier or process engine is never a blanket admission of clinical causality or complete RCA.
