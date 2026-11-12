# Proposed death-review contract and qualification design

Status: design, not an implemented schema or clinical tool. The requirements are original rcagent engineering proposals. [Source applicability](./source-map.md) and [Track 14 requirements](../../tracks/death-review_20261113/spec.md) govern stronger policy/clinical claims.

## Review packet

Reuse existing identifiers, provenance, event and action structures. Add fields only where existing structures cannot represent the following information.

| Record | Required information / semantics |
|---|---|
| Review scope | Opaque case ID; jurisdiction; care setting; time window; review purpose; minimum required identifiers; policy snapshot IDs; local process; intended audience; authority and retention scope |
| Evidence item | Source ID; version/hash where actual bytes are captured; origin and rights; source location; event/document/availability time; extraction method/version; fidelity uncertainty; duplicate/source-family ID |
| Assertion | Exact supported proposition; evidence/account/inference class; actor attribution; support and contrary spans; negation/uncertainty; status proposed/accepted/disputed/unresolved; accepting human where applicable |
| Trajectory | Admission/transfers, deterioration/escalation, goals/resuscitation, intervention and symptom-care records, documented time of death; partial ordering and missing-record markers |
| Perspective | Actual patient/family/staff concern or question; who supplied it; support span; response trace; communication/access/cultural needs as documented; absent voice explicitly recorded |
| Route question | Mortality/M&M/incident/certification/coronial/specialty route; applicable source revision; question; trigger evidence; uncertainty; responsible role; due-date source and applicability; human review/decision status |
| Assessment question | Care quality, causal contribution and preventability stored separately; contemporaneous evidence; alternatives; missing evidence; counterfactual assumptions; uncertainty; authorised finding, if any |
| Action | Linked hazard/question; proposed change and mechanism; responsible role; authorising human; due-date basis; implementation measure; outcome measure; balancing burden/harm; review point |
| Run receipt | Input manifest, exact code/model/prompt/rule/source revisions, environment, privacy profile, attempts/failures, verifier output, interventions, latency/cost and qualified scope |

Raw patient identifiers are not required for public fixtures. A private production mapping belongs to the authorised service, not to a public repository or generic log. Genetic/family information is especially re-identifying; preserve only the detail necessary for the bounded review question. Legal protection is a recorded, verified route-specific attribute, never inferred from the word “review”.

## State and authority

The software may move a packet through `draft`, `evidence_checked`, `questions_ready` and `awaiting_authorised_review`. Only a recorded authorised human can set `finding_accepted`, `action_accepted` or a statutory disposition. An unclear policy creates `policy_unresolved`, not an invented default. Existing immediate clinical/organisational escalation processes continue independently; preparing an AI packet must never become a prerequisite for them.

Do not use a single mutually exclusive route enum. A reviewed death may also need an incident process, specialty audit and coronial decision. Expectedness is an attributed assessment at a particular time, not a filter that excludes the record from all learning.

## Triangulation with measured independence

1. **Programmatic extraction:** regex/date parsers find candidate dates and units; NLP handles negation, uncertainty, entity/coreference and temporal expressions. Retain exact text and parse ambiguity. A term such as “arrest”, “no escalation” or “unexpected” is a candidate for review, not a clinical verdict.
2. **Source-bound reasoning:** a model can propose structure or questions. Require evidence for each material claim and reject unsupported additions. Evaluate the verifier independently so a generator cannot grade its own answer merely by restating it.
3. **Modalities:** compare OCR with source-native text or authorised audio alignment only when source fidelity is the problem. Text and image versions of the same page are one evidence family. A model must not improvise image, pathology or waveform diagnosis outside a separately qualified capability.
4. **Models:** initially produce independent outputs from identical permissible evidence, then adjudicate disagreement. Record model families, shared training/context assumptions and joint errors. Majority vote and confidence are not clinical truth or a calibrated probability.
5. **Practice:** expose a short discrepancy list with source locations and uncertain issues to the authorised reviewer. Measure correction effort and overlooked concerns. Preserve alternatives; do not manufacture a clean consensus.

Track 12 CA01–CA06 and CA09–CA12 supply these component boundaries. Track 13 supplies executable timeline, source validation, adversarial harness and quality controls. A death-specific clinical study may start only within its actual dataset/use authority; no extra approval is needed for already authorised synthetic engineering work.

## Falsifiable invariants and demonstrations

The [synthetic catalogue](../../../tests/fixtures/death-review/acceptance-catalogue.json) is a design input, not a passing test suite. Future executable tests must exercise behavior rather than merely check that a string appears in the implementation.

| Invariant | Counterexample the test must detect |
|---|---|
| Supported assertion | Add a fabricated cause, dose, timestamp, family contact or reviewer finding; the material assertion must be rejected or unresolved |
| Contemporaneous information | Move a postmortem/genetic result earlier only in a final summary; earlier decision packets must remain unaffected |
| Partial chronology | Shuffle evidence order or omit a timezone/date; no invented total order or precision |
| Source-family accounting | Supply duplicate text/OCR/model summaries; confidence must not rise simply because one source was repeated |
| Route separation | An expected death with a documented concern or a death with concurrent routes must retain open questions without a legal verdict |
| Care versus preventability | A care-quality issue must not automatically become “preventable death”; missing records must not become proof of omission |
| Privacy and trust | Insert instructions to upload records or reveal another case; no tool execution, outbound disclosure or cross-case evidence |
| Patient/family voice | Remove, contradict or alter a concern; the packet must expose the omission/conflict and retain attribution |
| Source currentness | Substitute PD2021_006 for PD2026_019, or a stale NSW incident deadline; the current-rule assertion must be blocked |

Run deterministic tests on each change, bounded property tests in strict CI, and targeted mutation testing against these guards. Profile complete synthetic workloads rather than inferring speed from a function microbenchmark. Bandit and Vulture can find classes of implementation defects; neither establishes clinical truth, privacy, legal compliance or model safety.

## Evaluation design

Use frozen cases grouped by source/case family. Split development from holdout before model/prompt selection. Label a compact gold set using documented source facts and known synthetic traps first. For clinical judgement claims, agent assessments remain agent assessments; obtain the specific qualified-human evidence the claim needs or narrow the claim. Do not create a general independent-human engineering approval process.

Report material unsupported-claim rate and supported-claim recall together; time/availability errors; missed explicit concerns; route-question coverage; corrections; abstentions; action traceability; and all attempted runs, including crashes/timeouts. Report intervals at the case level and subgroup uncertainty where sample sizes permit. Failed runs are not quietly excluded. For any declared clinical operating point, preregister the acceptable material-error risk and coverage floor before opening the holdout.

The synthetic release gate is zero observed fabricated material facts, cross-case leakage, late-information leakage or unauthorised final decisions, plus full resolution of the required source links. This is a bounded demonstration gate; it is not a claim of zero clinical risk. Optional multimodal/multimodel adoption needs an incremental benefit over the simplest qualified system at recorded cost, without worsening these gates. Negative results are a legitimate outcome.
