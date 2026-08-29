# Track 09 review fixes

The three-role agent panel initially returned rework. The implementation was changed to:

- minimise audience views and recursively reject active, path, credential and identifier content;
- bind dry-run receipts to request, registry and immutable source revision;
- parse and evaluate approval timestamps, require accountable-human role separation, and bind action/effectiveness decisions to exact hashes and scopes;
- bind synthetic participation hashes and reject nested sensitive content;
- replace fabricated external specialist states with local/unverified states;
- replace hard-coded scenario passes with executable fixtures and record unmeasured metrics as null;
- make method guidance signal-driven with abstention, budget, rationale and stop rules;
- validate canonical paths against safety-work, strengthen the JSON Schema, verify audit chains, and enforce registry uniqueness;
- bind the checked synthetic receipt to actual output and verify every preserved legacy-template path and hash.

No agent review is represented as accountable human approval or as clinical, legal, policy, cultural-safety, organisational, accessibility, usability or deployment validation.
