# Prospective protocol-candidate contract

Base: `370d0689aebc0d440da723a21e9a044d20b3f860`; existing PR #83.
This implements a read-only contract, not a frozen protocol or primary study.

## Implemented checks

`tools/prospective_protocol.py` reuses the existing safe JSON/artifact reader,
strict schema helpers and SHA-256 checks. It accepts only version 1.0.0 of the
declared two-public-synthetic-case, one-condition, one-repeat design. Case,
rubric, scoring-instruction and prompt-template paths are distinct and their
exact nonempty bounded UTF-8 bytes must match. Duplicate keys, extra fields,
symlinks, escaping paths, stale hashes, invalid identities and altered slot
denominators fail closed. Integer settings reject booleans and float lookalikes.
The model identifier permits underscores used by the admitted Qwen registry.

The contract fixes seed 42, temperature 0, 512 generated-token limit, 2,048
context tokens and a 120-second process timeout. One technical retry may be
declared; this validator does not execute or judge retries. Scoring declares
three agent roles, adjudication only after three sealed submissions, the
existing 0.80/0.67 conservative research thresholds and four safety hard gates.
Public exposed cases, metadata-only blinding and non-operational/no-comparative
claims are mandatory. These small-sample thresholds do not prove reliability.

The condition's model revision, model/runtime/profile/adapter/registry digests
are identity declarations only. This module does not open model files or
launch an executable. A declared normalisation method is not evidence that
its implementation exists. Candidate text marked synthetic is not proof that
arbitrary caller-supplied text is safe; reviewed source admission still applies.

## Invocation and result boundary

Supply a deliberately reviewed candidate path and pin:

```text
uv run python -m tools.prospective_protocol --protocol <candidate.json> --expected-sha256 <reviewed-sha256>
```

Exit 0 means `protocol_candidate_valid`. Results always carry
`study_unlocked: false` and `admitted: false`, with explicit unverified freeze,
runtime/adapter, normalisation and privacy boundaries. No actual prospective
candidate JSON was frozen or fabricated in this slice. The original v0.1
planning manifest, two pending slots and all historical evidence remain intact.

## Evidence and review

The initial fixture-first import failed before the new module existed.
Thirty-six synthetic tests then passed with 100% statement/branch coverage of
the module, plus Ruff, ty and basedpyright. `protocol_contract_review` implemented
only the two owned source/test files; the main agent reviewed the contract and
corrected compatibility with the actual admitted model ID. `runtime_profile_tests`
performed a separate read-only review and reran the focused suite, finding no
blocking defect. Exact agent model revisions were not exposed; correlated
errors remain possible. This is agent review, not independent human validation.

Whole-repository integration results belong to the runtime/protocol checkpoint
and exact PR head; this focused receipt is not a claim about hosted checks.

## Next and rollback

Implement and test the actual study execution/capture and deterministic
normalisation path. Then create and review the real protocol, pin all inputs
and adapter identities, commit its freeze before any study invocation, and
validate affirmative admission separately from blinding/scoring/analysis.
Do not use the non-study READY probe as the study runner or reuse its output.
No repeated owner approval is needed for this bounded work.

Rollback only this candidate validator/tests and receipt. Leave all existing
live preflights locked and preserve raw evidence, historical identities and
clinical/legal/policy/organisational authority boundaries.
