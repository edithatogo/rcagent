# Claim admission and hallucination reduction

Status: normative design for new component implementation. The existing identifier/schema checks do not implement the complete contract. No layer guarantees truth or zero hallucinations.

## Failure taxonomy

Record invented evidence; wrong source or version; corrupted extraction; wrong actor/experiencer; altered number/unit/negation; chronology error; later knowledge presented as contemporaneous; unsupported semantic inference; unsupported cognition/causality; inappropriate authority/jurisdiction; omitted material fact or family concern; misleading synthesis; and an action unsupported by its claimed mechanism. A source may contain a mistaken account even when extraction is perfect.

## Admission sequence

| Layer | Required check | Failure behaviour |
| --- | --- | --- |
| Source and scope | Immutable permitted source/version, correct case and recipient/cutoff view, rights/privacy class | Reject unauthorised input; retain a bounded missing-evidence record |
| Extraction | Source span resolves; original bytes and coordinate mapping agree; OCR/layout confidence and missing pages explicit | Retain uncertain extraction, seek an alternative representation, do not fill missing text |
| Structure and identity | Typed relationships, required fields, no duplicate/cross-case IDs, allowed state transitions | Reject invalid record |
| Exact content | Quote, number, unit, negation, actor and temporal fields match available evidence where deterministically testable | Reject or flag the specific mismatch with source evidence |
| Availability | All generation, retrieval, verifier, cache and renderer access remains inside the same time/view boundary | Reject future/other-case access; unknown availability stays unknown |
| Semantic support | Calibrated supported/contradicted/insufficient decision with complete relevant context | Withhold an unsupported conclusion; preserve the competing accounts |
| Completeness | Compare against an independently prepared, view-bound critical-fact and concern inventory | Expose omissions and unanswered concerns; do not infer absent care |
| Interpretation | Facts, accounts, hypotheses, findings and decisions stay typed; alternatives and causal assumptions visible | No inferred cognition, preventability or culpability promoted by model confidence |
| Rendering | Deterministic templates from admitted records first; re-extract and verify any free-form rewrite | Block invented prose additions or return a labelled draft with unresolved items |
| Acceptance | Exact qualification receipt and accountable review required for the claimed use | Research-only output or explicit abstention when evidence is insufficient |

Grounded generation should prefer extractive records and constrained field values before prose. Allowed evidence IDs or schema-constrained decoding reduce certain errors but do not establish entailment. Retrieval must include opposing evidence and correct policy versions, with separate public/private and time-scoped indexes. Truncation, token limits and unavailable tools produce incomplete status, never implied success.

## Repair, uncertainty and review

Permit a small preregistered repair budget (initial engineering default: at most two attempts per failed candidate), each retaining the original failure and revised evidence. Stop if the required evidence is absent. The repair model receives the verifier's concrete error, not an instruction to keep trying until it passes. No critic can rewrite a source or erase a disagreement. Surface calibrated uncertainty and the reason for abstention; self-reported model confidence is not a calibrated probability.

Human corrections create a new version with source and authority provenance; they do not silently alter historical model outputs or test labels. Agent panels provide software and research-method review. Observed investigator/patient benefit requires the appropriate separate study observations and cannot be inferred from agent agreement.

## Evaluation contract

Use naturally occurring model errors as well as a separately labelled injected-error suite. Evaluate each layer and the composed system. Report unsupported assertions per admitted claim, severe error per case, material omissions, contradictory-evidence retention, family-concern coverage, useful output coverage, false blocking, calibration and resource cost. Include truthful-but-incomplete, correct refusal, no incident, insufficient evidence and multiple equally compatible causal explanations.

Freeze the primary risk/coverage contrast before the final holdout. Compare improvements against the same generator without the verifier and against a competent non-generative baseline. An all-abstain system cannot satisfy useful coverage; a fluent report cannot compensate for a failed integrity/privacy check. Report failures and missing runs in the denominator. Case variants and repeated seeds remain clustered, not counted as independent patients.

## Security and privacy engineering

Treat source documents, policy pages, OCR, retrieved text and model outputs as untrusted data. Separate instructions from quoted content; disable arbitrary tools; use explicit argument schemas, a local broker and least authority. Test prompt injection in documents/metadata/images, path traversal, archive expansion, unsafe serialisation, malformed schemas, regex denial-of-service, resource exhaustion and tool-result spoofing. Filesystem, egress, logs, crash reports, caches and exports require observed boundary tests. A language migration or an identifier scanner does not establish that boundary.

Record only synthetic case text in public CI. Local/private validation receipts contain opaque IDs, hashes, aggregate errors and bounded metadata; no raw source fragments in public artifacts. Existing retention, source rights and clinical authority remain applicable without repeated routine implementation approvals.

## Primary evidence informing the design

- Wang et al., Augmenting patient safety surveillance in radiation oncology with large language model-based root cause analysis, PLOS Digital Health, 25 September 2026: https://doi.org/10.1371/journal.pdig.0001740. A 19-case proof-of-concept with expert assessment and observed hallucinations, not an rcagent benchmark result.
- Anthropic, Demystifying evals for AI agents, 9 January 2026: https://www.anthropic.com/research/demystifying-evals-for-ai-agents. Distinguishes outcomes, trials, graders and model-plus-harness evaluation; engineering guidance, not clinical validation.
- Existing [verification and reuse contract](../cognitive-autopsy/verification-and-reuse.md) supplies the source/view and semantic boundaries; this document adds the delivery-level admission sequence.
