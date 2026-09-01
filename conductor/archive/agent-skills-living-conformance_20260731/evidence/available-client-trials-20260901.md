# Available-client synthetic trials — 2026-09-01

## Scope

The owner approved one bounded, synthetic-only trial per available authenticated
client. No private data, publication, release, clinical use, deployment approval
or universal compatibility claim was in scope. A command-line rejection before a
provider request did not consume a trial; a provider request did. Provider
failures were not retried.

The initial common prompt is retained at
`evaluations/skills/rca-investigation/available-client-synthetic-prompt.md`.
After explicit owner approval, the fresh Codex-only prompt permitting the
minimum read-only skill-loading operation is retained at
`evaluations/skills/rca-investigation/codex-readonly-synthetic-prompt.md`.

## Inventory and observations

| Client | Installed/auth state | Discovery/path evidence | Single provider trial | Result |
|---|---|---|---|---|
| Codex 0.144.1 | authenticated with ChatGPT | adapter installed at `.codex/skills/rca-investigation`; both runs named and discovered `rca-investigation` | initial bounded run failed because the prompt prohibited skill loading; one separately authorised fresh run used a corrected prompt in a read-only sandbox | **Pass on the fresh authorised run.** Codex read `SKILL.md`, the Triage workflow and investigation checklist, selected Triage, defined placeholders, separated facts and unknowns, listed safeguards, non-causal questions and evidence, and reserved the required decisions for authorised humans. The initial failed observation remains retained. |
| AGY 1.1.22 | authenticated; model catalogue available | adapter installed at `.agents/skills/rca-investigation` | one successful `gemini-3.7-flash-low` turn in plan+sandbox mode | **Pass.** The response explicitly named `rca-investigation`, selected an investigation-opening mode, defined placeholders, separated facts and unknowns, listed safeguards, non-causal system questions and evidence, and reserved clinical, notification, severity, policy, legal, employment and final decisions for authorised humans. |
| OpenCode 1.18.21 | client credentials existed, but the selected Google provider was not authenticated | `opencode debug skill` discovered `rca-investigation` under `.opencode/skills/` | one provider request | **Unverified/fail.** The provider rejected the request before generation because its API key was absent. No retry was made. |
| Kilo 7.5.6 | Kilo Gateway OAuth present | `kilo debug skill` discovered `rca-investigation` under `.kilo/skills/` | one provider request | **Unverified/fail.** The gateway returned HTTP 402 and required credits or a free model. No retry was made. |
| Cursor 3.17.6 | installed; `cursor-agent status` reported not logged in | contract adapter only | not attempted | **Unverified.** Authentication prerequisite absent. |
| Cline 3.0.60 | installed; authentication could not be established non-interactively | contract adapter only | not attempted | **Unverified.** Authentication prerequisite unverified. |
| Claude Code 2.1.126 | installed; authentication false | contract adapter only | not attempted | **Unverified.** Authentication prerequisite absent. |

## Acceptance conclusion

Codex and AGY supply the two required passing actual-client observations, so
`RCA-ADAPTER-001` passes at the recorded client versions, prompts, modes and
synthetic case. OpenCode, Kilo, Cursor, Cline and Claude remain explicitly
unverified for actual execution. This bounded evidence does not establish
universal compatibility, operational safety, deployment approval or any
external authority decision.
