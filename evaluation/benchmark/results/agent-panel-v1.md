# Agent-panel comparator review

- Review mode: three blind agent raters plus separate post-submission agent adjudication
- Panel receipt: `ab1fd836bdaeb047cd5be674f50997f3c159ef5c9898d53f553094b14f34b7fd`
- Rated items: 27
- Unanimous items: 19
- Majority decisions: 27
- Raw exact agreement: 0.703704
- Ordinal Krippendorff alpha: 0.575597
- Submitted hard-gate conflicts: 0
- Conservative research threshold: failed
- Comparator disposition: all unsupported

All three blind reviewers independently recommended `unsupported`. The agreement failure is preserved as negative evidence. The adjudicator identified eight disagreements involving rubric ambiguity and candidate weakness; no score was changed and no threshold was lowered.

The frozen version 1 panel directly scored privacy, clinical safety, cultural
safety, and authority boundaries, but did not separately score security or
harmful output. The deterministic harness enforced all five hard gates and
observed zero violations in the synthetic cases. This incomplete qualitative
gate coverage independently prohibits a positive panel recommendation; see
`hard-gate-evidence-v1.json`. Neither zero observed violations nor absence of
panel flags proves domain safety.

Track completion, if otherwise evidenced, attests the benchmark harness and its ability to preserve a reproducible negative result. It does not promote a comparator or establish clinical, legal, policy, regulatory, employment, cultural-safety, organisational, deployment, or operational validation.
