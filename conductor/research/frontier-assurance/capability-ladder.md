# Incremental capability demonstrations

This is an executable delivery design, not a record of completed demonstrations. Track 12 owns the corresponding CA/CAW components. Each demo is useful on its own and has a finite, source-controlled synthetic oracle before model evaluation.

## Demonstration contract

Each demo records input/source hashes, schema and extractor/rule versions, permitted packet/view, command, runtime/dependency lock, expected outputs, actual outputs, failures, resource measurements and limitations. Repeat the demo in a clean checkout. A UI screenshot or successful exit alone is insufficient. Fixture generation must not leak expected labels into model inputs or retrieval.

| Demo | Increment | Initial finite oracle | Promotion question |
| --- | --- | --- | --- |
| D0 | Preserve and inspect evidence | Bytes/hashes/spans, typed ID relations, duplicates, revisions and unknown source states | Does accepted output point to exactly the admitted source? |
| D1 | Extract explicit observations | At least 12 independent synthetic case families covering numeric dates, missing year, midnight, locale ambiguity, ranges, units, negation, attribution, relative time, conflicting notes, OCR corruption and no event | Are matched spans faithful; what explicit events are missed or falsely extracted? |
| D2 | Build a timeline/partial order | Events in shuffled source order; three clocks; timezone/DST uncertainty; simultaneous/overlapping intervals; impossible cycles and amended records | Does chronology preserve uncertainty and contradiction without inventing point times? |
| D3 | Reconstruct a decision-time view | Later test result, delayed note, different recipient knowledge, explicit unknown availability, changed outcome with unchanged prior evidence, family concern | Is every fact entitled to this actor/cutoff/view, including verification and retrieval? |
| D4 | Extract and verify claims | Correct claims plus one-factor edits of source/version/span/number/unit/negation/subject, unsupported rationale and omitted concern | Does verification improve supported content and material coverage together? |
| D5 | Triangulate representations/sources | Native PDF text vs layout/OCR; narrative vs synthetic orders/observations log; noisy audio transcript vs source recording where admitted | Does a new modality add information or expose errors, and at what burden? |
| D6 | Compose an investigation/death-review packet | Complete and incomplete case packets, patient voice, conflicting accounts, proportionate methods, actions and unresolved issues | Do local gains survive composition and final rendering? |
| D7 | Compare on a frozen held-out corpus | Same admissible evidence, family/temporal split and matched budgets; real failures retained | Is there a clinically meaningful material-error/coverage advantage with uncertainty? |
| D8 | Test new research contributions | Evidence acquisition, uncertain conformance, action effectiveness, transportability and drift | Does a new mechanism add benefit over the strongest existing qualified system? |

## Timeline record and invariants

Extend the existing evidence contracts rather than replace them. A timeline event contains case/event/source/artefact IDs; immutable source digest; exact span with explicit byte/character/page coordinate system; raw expression; normalised event-time interval and precision; recording-time interval; recipient-specific availability interval; timezone and uncertainty; actor/subject; action/observation; assertion/negation/experiencer; extraction method/version; conflicts and provenance. Unknown times are null with reason, not midnight or file order.

Store an interval or a partial-order relation when an exact timestamp is unsupported. Relative time requires an explicit source anchor and recorded derivation. Different clocks are never silently substituted. Document order is not event order; note creation is not necessarily first clinical availability; a discharge summary may describe earlier events using later knowledge. A missing account of an action is not proof the action did not occur.

A chronology renderer displays source identifiers and uncertainty, supports review/correction without overwriting original extraction, and can show alternative orderings where required. Exports describe any loss of intervals/partial orders. Calendar arithmetic and timezone conversion use maintained standard libraries; untrusted regular expressions are prohibited and text/pattern work is bounded.

## Verification examples

- Reordering files or irrelevant paragraphs preserves source-linked event identity and all justified temporal relations.
- Uniformly shifting anchored dates shifts the timeline by the same amount while retaining durations; changing a genuine new cue may change the decision packet.
- Changing only a later outcome does not insert that outcome into earlier knowledge.
- Removing an availability anchor makes availability unknown, rather than inferred from an outcome.
- Unicode or whitespace normalisation requires an explicit reversible span mapping; a character offset is never treated as a UTF-8 byte offset.
- Duplicate renderings of the same source do not count as independent corroboration.
- Known-invalid references, forged digests and forbidden future-view access have zero accepted cases in the finite oracle. Report the denominator; this is not a zero-risk population claim.

Property-based tests generate valid/invalid relations and event intervals. Stateful tests exercise ingestion, correction, supersession, withdrawal, export and rebuild. Metamorphic tests exercise the invariants above. Mutation testing must kill changes that remove entity checks, cutoff checks or exclusion of non-public fields. Natural extraction errors and deliberately injected errors are reported separately.

## Empirical thresholds

Before the final holdout, freeze component-specific numerical margins, coverage floors and severe-error limits using the development pilot, intended task and available sample size. Report precision/recall, unsupported assertions, material omissions, abstention risk/coverage and case-clustered 95% intervals. All-abstention cannot win; neither can high coverage obtained by inventing events. Preserve a wholly deterministic timeline capability when no model earns promotion.
