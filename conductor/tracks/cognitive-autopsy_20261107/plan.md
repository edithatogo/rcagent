# Cognitive autopsy implementation plan

The owner requested these repository and research updates on 2026-11-07 and confirmed existing HDC ethics approval. This plan schedules future implementation; unchecked items are not completed work.

Continue automatically through ready tasks, agent review and bounded rework. Do not ask for routine approval. Record each recommendation with evidence; the safe default is a local research-only result with unsupported capabilities withheld. Escalate only a genuinely new reserved action, not an already authorised corpus study or reversible repository change.

## Phase 1: Snapshot, contracts and frozen design — target days 1–2

- [ ] Resolve the exact HDC source/Hugging Face revision through the corpus subtrack; inventory actual case payloads, duplicates, completeness and source spans.
- [ ] Link the existing ethics record in the protected study register; carry the already confirmed approval forward without inventing its identifier or extending its scope.
- [ ] Map existing contracts to CA01–CA12; implement versioned decision records and A/B/C packet manifests as small extensions.
- [ ] Separate original text from topic-model preprocessing; preserve negation, units, doses, time and uncertainty.
- [ ] Freeze eligibility, split groups, initial component tasks, outcome definitions and comparison hierarchy before evaluating the holdout.
- [ ] Checkpoint: validate contracts and lineage on synthetic fixtures; report unresolved data inventory facts without claiming case admission.

## Phase 2: Local harness and patient-relevant scoring — target days 2–5

- [ ] Add a cognitive-autopsy study adapter to the existing harness; preserve the synthetic v1 comparator and its negative evidence.
- [ ] Admit exact local model/runtime artefacts with model-specific licence metadata; do not reuse the old Apache-only comparator gate for differently licensed models.
- [ ] Build deterministic extraction and untuned structured baselines; add compartment- and time-filtered lexical retrieval before optional local embeddings/reranking.
- [ ] Implement material-error, evidence, abstention, patient/family concern and action-quality scoring with source adjudication records and reviewer-class labels.
- [ ] Test prohibited information in filenames, metadata, retrieval, tool outputs, cache reuse, truncation and documents that contain instructions.
- [ ] Checkpoint: verify failed-run denominators, reproducible receipts, network denial and local-only storage. No sensitive run while these controls are unproved.

## Phase 3: Pilot and component comparison — target days 5–10

- [ ] Run a 20–30-case development pilot if the eligible snapshot supports it; estimate runtime, error prevalence, annotation effort and score reliability.
- [ ] Preselect at most two general local contenders and the medical/base-model pair for the main study; add a small extraction model only where its role is distinct.
- [ ] Refine only on development data, version changes, then freeze all prompts, budgets, scoring and primary contrast.
- [ ] Execute the held-out HDC evaluation; provisional planning range 80–120 independent cases, final size based on pilot precision and availability.
- [ ] Compare masked and outcome-exposed runs independently; assess both resistance to hindsight and appropriate response to genuinely decision-relevant new evidence.
- [ ] Checkpoint: three-role agent repository review; agent scoring remains labelled. Obtain only the targeted human observations necessary for any claim requiring them, or narrow the claim.

## Phase 4: Optional adaptation — trigger-based, not on the critical path

- [ ] Diagnose a persistent, learnable error pattern after prompting, retrieval, context allocation and decoding fixes.
- [ ] Admit training data and freeze case-family splits, training budget, comparison and stopping rule before adaptation.
- [ ] Run one bounded PEFT/LoRA experiment using the most promising base model; compare base, base+retrieval, adapted, and adapted+retrieval under matched settings.
- [ ] Apply the predeclared quality, safety, privacy, robustness and resource gates; retain the untuned system if results are inconclusive or worse.
- [ ] Checkpoint: publish an internal adoption/rejection receipt, including failures, training cost and reproducibility. Weight release is a separate exact-artefact decision.

## Phase 5: Composition and optional hybrid orchestration

- [ ] Compose only individually qualified components, testing propagated errors, shared-context leakage, correlated critics and useful abstention.
- [ ] Implement the optional cloud control-plane adapter only after the fully local path works; cloud inputs are allowlisted public templates and opaque scheduling metadata.
- [ ] Verify local broker policy, signatures, replay protection, deny-by-default networking, constant/coarse scheduling metadata and safe failure paths with actual adversarial traffic tests.
- [ ] Checkpoint: compare the staged system against the best single model and deterministic baseline. A successful component does not qualify complete RCA or cloud orchestration.

## Phase 6: Analysis, manuscript and governed handoff — target weeks 3–6

- [ ] Generate reproducible tables, case-clustered intervals, failure taxonomy, evidence cards and cost-consequence analysis.
- [ ] Draft the HDC methods/evaluation paper in learningfromharm, with complete dataset and model citations.
- [ ] Prepare a release manifest and dataset/model cards; expose only artefacts whose exact publication scope is already authorised.
- [ ] Record patient benefit as unmeasured unless observed; reserve educational effectiveness or prospective clinical benefit for an appropriate separate study.
- [ ] Checkpoint: reconcile exact commits, CI, agent reviews, exclusions, governance decisions and remaining limitations before claiming track completion.

## Delivery assumptions and rollback

Days are coding-agent work packages after corpus and hardware access, not promised elapsed clinical-study time. Parallelise one integration lane and two non-overlapping lanes. Corpus/model availability and necessary adjudication determine elapsed time.

If no local model passes, retain the deterministic evidence/chronology product and publish the negative comparison. If source evidence is insufficient, reduce the question to documented information rather than infer cognition. If the hybrid boundary fails, disable the cloud adapter and continue fully local. Revert this documentation commit to remove the plan; implementation must preserve versioned snapshots and allow per-component rollback without deleting historical receipts.
