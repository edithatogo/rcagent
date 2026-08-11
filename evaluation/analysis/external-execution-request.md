# External Execution Request — Phase 4 and Track 5

## Required operator actions

1. **H2 Claude Code + Opus:** execute 27 runs; retain raw transcripts, complete metadata, normalized outputs, and receipts.
2. **H3 Gemini CLI:** execute 27 runs; retain raw transcripts, complete metadata, normalized outputs, and receipts.
3. **H4 Codex:** attest or rerun the 27 candidate raw-to-normalized joins in `phase4-h4-h5-mapping.md`.
4. **H5 Qwen:** attest or rerun the 27 candidate raw-to-normalized joins in `phase4-h4-h5-mapping.md`.
5. **H6 Kilo Code:** confirm the actual harness for the alternate raw evidence or rerun 27 canonical cases; quarantine empty outputs.
6. **H7 Copilot:** confirm the actual harness for the alternate raw evidence or rerun 27 canonical cases; quarantine empty outputs.
7. **H8 Human Expert:** provide the remaining raw receipts for 9 cases, one run per case.

## Required submission per run

- Raw transcript, unedited.
- Complete metadata: condition, case, run, model, harness, temperature, start/end timestamps, endpoint, token/cost metrics or explicit unavailable reason.
- Eight-section normalized output derived from that raw transcript.
- Run receipt and completed operator/evaluator attestation.

## Acceptance gate

## Current access-resolution guidance (2026-08-10)

Before any run, the operator should use the vendor's current authentication
documentation and record the exact client/version and authentication mode in the
slot metadata. Current official references include:

- Claude Code authentication: https://code.claude.com/docs/en/authentication
- Gemini CLI authentication: https://google-gemini.github.io/gemini-cli/docs/cli/authentication.html
- GitHub Copilot CLI authentication: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli

Authentication success alone is not execution evidence. The operator must still
capture the complete raw transcript, prompt, model/harness configuration,
timestamps, usage or an explicit unavailable reason, hashes, and attestation in
the atomic slot package. If access cannot be established, the slot remains
quarantined and the failure is recorded rather than replaced with a synthetic
run.

Submit evidence only into the canonical manifest workflow. Unjoined, empty, inferred, or placeholder files remain quarantined. After all eligible rows are admitted, the scoring custodian may populate and seal the blinding map. Do not modify `rubric-scores.csv` until that gate passes.
