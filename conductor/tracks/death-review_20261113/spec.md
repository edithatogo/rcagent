# Death review and mortality learning specification

## Purpose and present boundary

Add a source-grounded death-review pathway to rcagent, beginning with a small, inspectable chronology and evidence packet. Expand only after each component demonstrates its limits. The initial delivery is a plan, original workflow guidance, a source register and synthetic acceptance cases. It does not implement an automated mortality review service, admit patient records or establish clinical validity.

Users are the developer, authorised clinical reviewers, mortality/M&M coordinators and quality-improvement staff. Patient and family perspectives are evidence in their own right; consultation, consent, cultural wishes or agreement must never be invented.

The pathways below can coexist for one death. Selecting one must not suppress another.

| Pathway | Purpose and bounded assistant output | Decision authority / policy anchor |
|---|---|---|
| Routine mortality screening | Record scope, completeness, review questions and candidate routes; retain expected as well as unexpected deaths | Applicable service process; NSW CEC death-screening overview [NSW-DS](../../research/death-review/source-map.md#nsw-ds) |
| Structured case review and M&M | Present evidence, disagreements, system context and learning for a multidisciplinary discussion | Authorised meeting/review process; NSW CEC M&M guidance [NSW-MM](../../research/death-review/source-map.md#nsw-mm); QLD local instrument remains to be verified |
| Clinical incident management | Flag a potential need to use the applicable incident pathway; preserve parallel deadlines/questions | Local authorised officers; current NSW transition [NSW-IM](../../research/death-review/source-map.md#nsw-im); QLD [QLD-PS](../../research/death-review/source-map.md#qld-ps), [QLD-CIM](../../research/death-review/source-map.md#qld-cim) |
| Death verification/certification | Index existing documents, authors and unresolved status; never certify or supply a definitive cause of death | Authorised practitioner and jurisdiction process; [NSW-VD](../../research/death-review/source-map.md#nsw-vd); QLD local process and [QLD-COR](../../research/death-review/source-map.md#qld-cor) |
| Coronial reporting/investigation | Surface a question for immediate responsible human assessment where appropriate; preserve evidence and current authority | Statutory decision-makers; [NSW-COR](../../research/death-review/source-map.md#nsw-cor), [QLD-COR](../../research/death-review/source-map.md#qld-cor) |
| Specialty review | Suggest relevant maternal, perinatal, child, anaesthetic, surgical, mental-health or other pathway for applicability review | Verified specialty process; [NSW-MAT](../../research/death-review/source-map.md#nsw-mat), [NSW-PERI](../../research/death-review/source-map.md#nsw-peri), [NSW-CHASM](../../research/death-review/source-map.md#nsw-chasm), [QLD-MP](../../research/death-review/source-map.md#qld-mp), [QLD-ANA](../../research/death-review/source-map.md#qld-ana) |

## Requirements — MoSCoW

The following are proposed **rcagent engineering requirements**, not a claim that either jurisdiction mandates this software or its schema. Policy-derived requirements and limitations are linked separately in the source crosswalk.

### Must

- **DR-M01 — Scope and routing:** record jurisdiction, organisation, care setting, review purpose, death date/precision, expectedness as an attributed account, policy version, applicability uncertainty and responsible human. Support concurrent routes; an expected death remains eligible for learning. Do not infer that every death is a serious incident or that every serious incident requires RCA. QLD expressly permits more than one analysis method [QLD-CIM](../../research/death-review/source-map.md#qld-cim).
- **DR-M02 — Evidence integrity:** every factual assertion has a source identifier and inspectable location; distinguish recorded facts, accounts, inference, proposals and accepted decisions. Conflicts, missing pages and uncertain extraction remain visible. A record's omission does not establish that care did not occur.
- **DR-M03 — Time:** preserve event time, document time and information-availability time, their precision and timezone. A partial order is allowed. Later autopsy, genetic, laboratory or coronial findings cannot leak into an earlier decision packet. Unknown availability must stay unknown.
- **DR-M04 — Authority:** no automated cause-of-death certificate, coronial reportability determination, statutory submission, preventability verdict, negligence/blame judgement or declaration of privilege. Preserve a route-specific `requires_authorised_review` state and unresolved obligations. An output label cannot confer legal protection [NSW-COR](../../research/death-review/source-map.md#nsw-cor), [QLD-CIM](../../research/death-review/source-map.md#qld-cim).
- **DR-M05 — Person and context:** represent patient/family concerns and desired questions; documented goals, escalation/resuscitation decisions, deterioration, symptom relief, transfers and follow-up; cultural/communication needs; staff accounts and system constraints. Show whether each item is documented, absent from available material or not applicable. Use safe, compassionate learning language, with patient/family and cultural context informed by [NSW-MM](../../research/death-review/source-map.md#nsw-mm), [NSW-IM](../../research/death-review/source-map.md#nsw-im), [QLD-CIM](../../research/death-review/source-map.md#qld-cim).
- **DR-M06 — Causality and uncertainty:** keep care quality, causal contribution and preventability as separate fields. Record alternative explanations and evidence that could change the assessment. No numeric probability of preventability from model confidence. QMPQC explicitly distinguishes potential improvement from proof that a death was preventable [QLD-MP](../../research/death-review/source-map.md#qld-mp).
- **DR-M07 — Actions and outcomes:** trace each proposed action to a supported hazard or unresolved question, with an owner role, mechanism, feasible next step, due-date basis, intended outcome and balancing measure. Implementation is not evidence of benefit. Only an authorised person accepts an action or a final finding.
- **DR-M08 — Source freshness:** version jurisdiction sources; preserve observed status, retrieval date, access/rights and conflicts. Withhold rules whose source/applicability is unresolved. In particular, do not carry PD2020_047 deadlines forward into PD2026_036 or use superseded PD2021_006 for current maternal reporting [source transition findings](../../research/death-review/source-map.md).
- **DR-M09 — Privacy and security:** synthetic-only public examples and CI; minimum necessary identifiers; case-local access, retention and deletion manifest; no case text in CI, issue bodies, ordinary logs or outbound telemetry. Untrusted records are data, never tool instructions. Follow Track 13 isolation, leakage, provenance and fail-safe gates.
- **DR-M10 — Honest qualification:** demonstrate and qualify components separately. Record run attempts, failures, exclusions, uncertainty, labelled agent review and model/runtime versions. Planning checks or a green pipeline do not qualify clinical decisions.

### Should

- **DR-S01 — Programmatic baseline:** regex plus conventional NLP should expose dates, units, medications, negation, uncertainty, entity references and escalation/goals terms, with rules and source spans. Evaluate ambiguity and false positives rather than equating a keyword with a finding.
- **DR-S02 — Selective triangulation:** compare deterministic extraction, a capable single model and an independent verifier against the same frozen evidence. Add a different model family or modality only for a measured failure mode; preserve shared-source and shared-model error dependence.
- **DR-S03 — Inclusive review:** include paediatric/developmental, disability, Aboriginal and Torres Strait Islander, language/access and care-transition contexts when documented. Ask a relevant human to resolve missing context; do not impute cultural identity or stereotyped explanations.
- **DR-S04 — Useful workload:** report correction time, missed concerns, review burden, cost and latency alongside quality. Prioritise a clear evidence packet over an elaborate unsupported narrative.
- **DR-S05 — Reusable contracts:** reuse CA01–CA06 and CA09–CA12 from Track 12, existing provenance and action records, and Track 13 component receipts. Avoid a separate death-specific reasoning engine.

### Could

- **DR-C01:** add OCR/table/audio alignment when the text-only pathway is qualified and the specific modality improves source fidelity on a paired benchmark.
- **DR-C02:** compare blinded independent models and disagreement-based routing if the added cost produces a predeclared material-error or abstention benefit.
- **DR-C03:** explore temporal graphs, process conformance and prospective action-effectiveness studies after component qualification. These are research hypotheses, not frontier capability claims.

### Will not in this track

- Perform clinical examination, verify life extinct, diagnose from images/waveforms, infer an unrecorded cause of death, file statutory reports or contact patients/families.
- Treat agent consensus as clinical validation, substitute NSW rules for QLD rules, copy copyrighted branded templates, or establish legal privilege by filename.
- Require independent human engineering reviewers or repeated approval of already authorised research/repository work. Operational clinical decisions retain their existing human authority.
- Migrate the repository to Rust as a prerequisite. Track 13 owns the evidence-led language decision; this track uses stable contracts independent of implementation language.

## Interfaces and dependencies

The [workflow contract](../../research/death-review/workflow-contract.md) specifies an original review packet and testable invariants; it is a proposed interface, not an implemented public API. Track 12 supplies CA01 source fidelity, CA02 provenance, CA03 time/availability, CA04/05 decision context, CA06 historical policy retrieval, CA09 family voice, CA10 actions and CA11/12 synthesis/follow-up. CA07 cognitive hypotheses remain explicitly research-only. Track 13 supplies strict CI, deterministic timeline demonstration, source verification, isolated execution and material-error measurements. No entire-track completion barrier is required to deliver an independently qualified component.

## Acceptance and evidence

| ID | Measurable acceptance | Claim permitted by success |
|---|---|---|
| A0 | Required track files parse/link; every policy anchor resolves to a register entry; observed source conflicts are retained; synthetic catalogue has no real case | Planning incorporated only |
| A1 | On the frozen synthetic catalogue: 100% sources resolve; 0 fabricated material events, hidden contradictions, case cross-links, source instructions executed or unlabelled unknown times | Deterministic contract demonstration on that catalogue |
| A2 | Temporal permutation, timezone, interval, duplicate and late-information tests pass; mutation tests exercise policy-version/availability/provenance guards | Invariants verified within stated test scope |
| A3 | Frozen component evaluation reports precision/recall and case-clustered intervals; all attempts counted; material invented facts, leakage or unauthorised final decisions block qualification; coverage/abstention measured | Bounded capability only if the predeclared risk/coverage target is met |
| A4 | Every explicit family concern in synthetic fixtures is retained or explicitly unresolved; quality and preventability never collapse into one field; every accepted action has human authority and evidence | Packet fidelity on the evaluated scope |
| A5 | Each optional NLP/model/modality comparison uses paired cases, equal available evidence and recorded cost; benefit and error correlation are reported; no improvement means retain the simpler qualified method | Comparative result, including a negative result |
| A6 | Applicable local pathway and exact policy versions verified before use; appropriate existing clinical/organisational authority and observed performance recorded | Only the explicitly authorised deployment scope |

Zero observed severe errors in a finite fixture set does not establish zero clinical risk. Select numerical real-case precision/coverage thresholds and sample sizes before opening a holdout, based on the intended bounded use and pilot uncertainty. Do not choose thresholds retrospectively to pass a model.

## Risks, assumptions and rollback

Source staleness is already observed, not hypothetical: NSW policy changes and QLD metadata conflicts need reconciliation. Source extraction can fail, death records can omit care, reviewers can suffer hindsight bias, and models can repeat correlated errors. The proposed controls are source snapshots, explicit unknowns, decision-time packets, independent extraction checks and human decision ownership. Where evidence is inadequate, retain the chronology and unresolved-question list and withhold the stronger claim. Disable a failing optional component without deleting historical receipts or changing a completed study's denominators.
