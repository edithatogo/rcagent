# Cognitive autopsy specification

## Problem and purpose

The workbench separates evidence, analysis and decisions but has no demonstrated model qualification for reconstructing an individual healthcare decision in its information context. A fluent retrospective account may import later knowledge, invent a clinician's reasoning, or convert an adverse outcome into presumed decision error.

Develop a research capability that reconstructs the documented decision opportunity, information available at that time, options, constraints, uncertainty and subsequent learning, with source-level provenance. The primary research material is the New Zealand Health and Disability Commissioner (HDC) corpus for which the owner confirms existing ethics approval. Cognitive autopsy complements the systems analysis in RCA; it does not infer private mental states or assign culpability.

## Scope and stakeholders

The programme supports researchers, safety investigators and clinical educators, with patient and family interests represented explicitly in the outcome framework. The owner and clinical collaborators retain governance and interpretation. Repository construction, literature maintenance, data preparation, model runs within admitted local environments, analysis and repository review are agent tasks. A person's participation or a patient's benefit cannot be manufactured by an agent.

The first release target is a reproducible research pipeline and capability report, not an operational RCA service. Text evidence is first; clinical image, waveform and treatment interpretation are separate future studies.

## Requirements

1. Add the component contracts CA01–CA12 in the component matrix, each with an independent status, evidence receipt and permitted context. Reuse the existing evidence, retrieval, benchmark, runtime, privacy and adaptation contracts.
2. Retain immutable source records and exact spans. Preserve event time, documentation time and information availability separately, including unknown values.
3. Construct isolated A/B/C packets: decision-time evidence; later outcomes; official or expert retrospective appraisal. Findings must not enter a masked condition via titles, filenames, frontmatter, prompts, indexes, caches or a previous conversational turn.
4. Classify rationale as contemporaneous documentation, retrospective reported account, expert interpretation, or model hypothesis. Missing rationale remains missing. Keep reasonable actions and successful adaptations alongside possible failures.
5. Compare deterministic extraction, untuned structured generation, local retrieval, a staged local system, and conditional adaptation. Use a new study ID and preserve historical H0–H8/H8P and synthetic results.
6. Evaluate patient-relevant material omissions, unsupported attributions and misleading learning, with grounded evidence coverage, uncertainty, patient/family concerns, equity and recommendation quality. Time and resource use are secondary.
7. Require exact model, tokenizer, prompt, runtime, quantisation, hardware, retrieval snapshot, input envelope and dataset revisions for each result. No receipt means no qualified capability.
8. Keep the default sensitive-data execution fully local. A cloud scheduler is an optional control-plane experiment under the hybrid privacy contract; it receives no sensitive payload, intermediate text or result.
9. Gate fine-tuning on a reproducible residual error pattern and matched held-out improvement over the best untuned configuration. Archive a negative result when adaptation does not earn its cost.
10. Integrate source snapshots from corpus-cases-medilegal-nz and study design/analysis from learningfromharm. Store derived annotations separately from the source corpus. Record citations and permitted uses for every additional dataset.

## Acceptance and evidence

- Each component has a specified input, output, benchmark, failure response and promotion envelope; the planning manifest starts with an empty qualified set.
- A packet builder demonstrates positive and adversarial fixtures for time, negation, doses, uncertain availability, document conflicts and outcome leakage before admitted HDC execution.
- Split manifests group related reports, versions, encounters and derived variants. Retrieval and fine-tuning never expose held-out answer material.
- The evaluation reports failures, exclusions, timeouts and abstentions, case-clustered uncertainty, subgroup limitations and model-judge limitations. Schema validity alone cannot pass it.
- Local-network tests, including actual packet capture and failure injection, precede any claim that the hybrid boundary is enforced.
- Fine-tuning has a prespecified decision rule, paired comparator results and rollback. It is optional, not a completion prerequisite.
- An integrated RCA pilot begins only after relevant component evidence and separate composition checks exist. Component results never automatically become a whole-RCA or patient-benefit claim.
- Governance, source access, exact revisions and publication decisions are recorded without credentials or patient content in GitHub.

## Dependencies and constraints

Planning can proceed now. Execution consumes the existing benchmark, evidence, privacy, retrieval, runtime and adaptation contracts, but their archived status is not proof that an intended model or HDC snapshot is admitted. The owner-confirmed HDC ethics approval is not reopened by this plan; capture the existing approval reference and scope in the protected study record. Additional datasets have their own access conditions.

Use maintained runtimes and thin adapters. Do not alter old results, lower gates to pass, create a second ingestion framework, or make sensitive data accessible to a cloud coding agent. The [integration contract](../../research/cognitive-autopsy/integration-contract.md) identifies the small remaining project-owned gaps.

## Risks, contingencies and open facts

Main risks are hindsight, outcome-shaped source narratives, memorised public cases, invented rationale, selection bias, correlated model errors, small subgroup samples, and hidden data egress. Mitigations and failure contingencies are specified in the evaluation and privacy documents.

Still to measure: exact eligible HDC snapshot and case count; hardware and run throughput; model compatibility; uncertainty and error prevalence; whether adaptation helps. These are executable tasks, not reasons to request the same research permission again.
