# Product Guidelines

## Voice and Writing

- Use Australian English: organisation, recognise, analyse, categorise, programme, colour, behaviour.
- Be clinical, calm, precise, respectful, systems-focused, and accessible.
- Prefer active voice for actions and ownership. Use neutral factual language for event descriptions.
- State the issuing body, exact title, version or date, jurisdiction, authority level, and source for policy or regulatory claims.
- Distinguish observed fact, reported account, evidence-supported inference, hypothesis, finding, recommendation, decision, and unresolved uncertainty.
- Avoid blame, hindsight, certainty inflation, euphemism, and causal language that exceeds the evidence.
- Explain specialist terminology on first use and provide a plain-language view where consumers or non-specialists may read the output.

## Safety and Human Authority

- Never present model or tool output as a clinical, legal, employment, disciplinary, policy, disclosure, or regulatory decision.
- Identify the accountable human reviewer and the evidence they must inspect.
- Surface missing, conflicting, late, low-quality, or potentially biased evidence.
- Use abstention and escalation when the evidence, capability, authority, privacy mode, or jurisdiction is inadequate.
- Do not let a confident style, numeric score, or workflow completion imply correctness.
- Treat radiology, pathology, ECG, diagnosis, treatment, and other clinical interpretations as research-disabled unless a separately approved governed pathway exists.

## Privacy and De-identification

Use synthetic placeholders in templates, examples, fixtures, screenshots, prompts, tests, and documentation:

- Patients or consumers: `[Patient A]`, `[Consumer B]`
- Cases: `[Case ID]`; never a medical record, unit record, NHI, or incident-system identifier
- Locations: `[Ward X]`, `[Unit Y]`, `[Facility Z]`
- Dates and times: `[Date]`, `[Time]`, `[DD/MM/YYYY HH:MM]`
- Staff: `[Clinician A]`, `[RN B]`; never names, initials, employee IDs, or rosters
- Contact details, credentials, network paths, and internal identifiers: synthetic values only

De-identification is a risk-reduction process, not a guarantee of anonymity. Preserve the minimum necessary detail, record transformations, test re-identification risk, and keep private data out of remote services unless an explicit governed decision permits it.

## Confidentiality and Legal Privilege

Do not add a blanket `CONFIDENTIAL`, `QUALITY IMPROVEMENT`, statutory-protection, legal-privilege, or similar header by default.

Such a label may be used only when:

1. the applicable jurisdiction, process, document class, purpose, and authority have been verified;
2. an authorised human has directed its use;
3. the exact approved wording and source are recorded; and
4. the label does not imply that the tool created or guaranteed the protection.

When status is unknown, state that confidentiality and privilege must be determined through the applicable authorised process. A label alone does not establish protection.

## Evidence and Citation

- Link every policy, framework, clinical, legal, model, benchmark, and compatibility claim to an authoritative or primary source where one exists.
- Record exact revisions, retrieval dates, hashes or checksums where practical, and whether a source was available online or from an approved local copy.
- Distinguish current, under review, consultation draft, superseded, local, advisory, and binding material.
- Quote minimally and respect copyright, licence, template, and database rights.
- Preserve contradictory evidence and explain how it affected the analysis.
- Never invent a citation, policy number, model revision, benchmark result, or source status.

## Jurisdictional Language

- Use the current terminology defined by the applicable jurisdiction pack.
- On first use, spell out formal names such as Severity Assessment Code (SAC), National Safety and Quality Health Service (NSQHS) Standards, and Clinical Excellence Commission (CEC).
- Do not assume an Australian national framework, NSW policy, New Zealand framework, or local procedure applies outside its recorded scope.
- Do not convert guidance, examples, consultation material, or common practice into a mandatory requirement.
- Preserve unresolved interpretation as a decision with sources and recommended options.

## Systems, Culture, and Participation

- Examine task, technology, team, environment, organisation, policy, resource, demand, control, and adaptation factors.
- Use Just Culture principles without converting them into an automated culpability classification.
- Include Safety-II and work-as-done perspectives where they help explain normal adaptation and resilience.
- Design for open disclosure, consumer and family participation, staff support, procedural fairness, accessibility, language needs, and trauma-informed practice.
- Embed Aboriginal cultural safety and appropriate consultation; do not treat a generic acknowledgement or checkbox as evidence of culturally safe practice.

## Recommendations and Actions

- Tie every recommendation to evidence, a system hazard or contributing condition, intended mechanism, and foreseeable unintended consequences.
- Prefer stronger system controls where feasible, while acknowledging context, resources, and new risks.
- Assign action owners, dependencies, due dates, implementation evidence, assurance, and escalation.
- Define process, outcome, and balancing measures plus an effectiveness review date.
- Do not mark an action effective merely because it was completed or a document was published.

## Model, Retrieval, and Tool Disclosures

Before a non-deterministic or external run, disclose:

- task, modality, model or tool, exact revision, runtime, quantisation, and device;
- execution mode, data boundary, network and telemetry status;
- input and context limits, knowledge limitations, intended and out-of-scope uses;
- retrieval corpus, source freshness, index or embedding revision where applicable;
- known failure modes, calibration evidence, and required human review; and
- whether the capability is supported, conditional, experimental, research-only, or unavailable.

Never describe a candidate model as recommended until the exact tested revision has a current receipt for the target device and task.

## Templates and Generated Documents

- Use one H1 document title, H2 major sections, and H3 subsections.
- Use GitHub-flavoured Markdown tables for structured data and Mermaid for source-controlled diagrams.
- Map template fields to canonical schemas and provenance requirements.
- Identify original, adapted, linked-only, locally supplied, restricted, and generated templates.
- Keep branded, organisation-specific, or mandated templates behind an owner and rights review.
- Generated outputs must expose evidence, uncertainty, model involvement, approvals, privacy mode, and limitations appropriate to their audience.

## Content Quality Gate

Before a deliverable can pass:

- [ ] Facts, accounts, analysis, findings, recommendations, and decisions are distinguishable.
- [ ] Sensitive data is absent from fixtures and unauthorised compartments.
- [ ] Sources, versions, authority, jurisdiction, rights, and freshness are recorded.
- [ ] Cross-references and citations resolve.
- [ ] Model, retrieval, framework, and device claims have exact evidence.
- [ ] Clinical, legal, privacy, cultural-safety, and human-review boundaries are explicit.
- [ ] Known limitations, negative results, and unresolved decisions remain visible.
- [ ] Completion is supported by a durable receipt, not only a checklist.
