# Available-client synthetic trials — 2026-09-01

## Scope

The owner approved one bounded, synthetic-only trial per available authenticated
client. No private data, publication, release, clinical use, deployment approval
or universal compatibility claim was in scope. A command-line rejection before a
provider request did not consume a trial; a provider request did. Provider
failures were not retried.

The common prompt is retained at
`evaluations/skills/rca-investigation/available-client-synthetic-prompt.md`.

## Inventory and observations

| Client | Installed/auth state | Discovery/path evidence | Single provider trial | Result |
|---|---|---|---|---|
| Codex 0.144.1 | authenticated with ChatGPT | adapter installed at `.codex/skills/rca-investigation`; the run named and discovered `rca-investigation` | one model turn, read-only sandbox | **Fail.** Codex identified the skill but declined to read `SKILL.md` because the prompt prohibited every shell command. It therefore did not produce the representative investigation opening. |
| AGY 1.1.22 | authenticated; model catalogue available | adapter installed at `.agents/skills/rca-investigation` | one successful `gemini-3.7-flash-low` turn in plan+sandbox mode | **Pass.** The response explicitly named `rca-investigation`, selected an investigation-opening mode, defined placeholders, separated facts and unknowns, listed safeguards, non-causal system questions and evidence, and reserved clinical, notification, severity, policy, legal, employment and final decisions for authorised humans. |
| OpenCode 1.18.21 | client credentials existed, but the selected Google provider was not authenticated | `opencode debug skill` discovered `rca-investigation` under `.opencode/skills/` | one provider request | **Unverified/fail.** The provider rejected the request before generation because its API key was absent. No retry was made. |
| Kilo 7.5.6 | Kilo Gateway OAuth present | `kilo debug skill` discovered `rca-investigation` under `.kilo/skills/` | one provider request | **Unverified/fail.** The gateway returned HTTP 402 and required credits or a free model. No retry was made. |
| Cursor 3.17.6 | installed; `cursor-agent status` reported not logged in | contract adapter only | not attempted | **Unverified.** Authentication prerequisite absent. |
| Cline 3.0.60 | installed; authentication could not be established non-interactively | contract adapter only | not attempted | **Unverified.** Authentication prerequisite unverified. |
| Claude Code 2.1.126 | installed; authentication false | contract adapter only | not attempted | **Unverified.** Authentication prerequisite absent. |

## Acceptance conclusion

AGY supplies one passing non-Codex actual-client observation. Codex does not yet
supply a passing representative execution observation, so `RCA-ADAPTER-001`
remains pending. Deterministic adapter tests and successful discovery do not
replace the missing execution evidence. Track 00 is not archive-eligible.

The smallest technical correction is to use a prompt that prohibits arbitrary
shell work but explicitly permits the client's read-only skill-loading mechanism.
Because the approved trial was one attempt without retries, that corrected Codex
trial requires a fresh owner authorisation rather than being run implicitly.
