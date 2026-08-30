# Prospective protocol preparation and execution freeze evidence

## Scope and activation

Activated `4cab688` from clean checkpoint `95b418f` after rechecking merged
PR #101 (`4d621e6`) and both successful post-merge workflows. Main used the
Conductor implementation workflow; no overlapping writer or lease was present.
This slice prepares exact public synthetic inputs, then requires a separate
source S / review R binding. Preparation is not execution or study admission.
The owning track and root issue #1 remain incomplete. Historical H0–H8/H8P,
planning manifest/rubric/inventory, negative READY evidence and licences remain
unchanged. No new download, global runtime change or provider execution occurs.

## Baseline and local eligibility

`uv run python -m tools.full_validation` passed 1,532 tests in 207.84 seconds,
94.56% coverage plus lint, types, governance and benchmark checks. Log:
`/tmp/rcagent-freeze-baseline.log`. The baseline started before the four new
protocol files and four input-consistency tests existed; it is not their
validation. No fixture-first RED is claimed for these declarative inputs.

For the distinct purpose of an actual prospective freeze, main called existing
`prospective_server_model.admit_model` against the approved canonical local
cache. It returned local artefact eligibility true, admission/unlock false.
All original model classes and licence checks were retained; no model launched.
The historical probe was not repeated. Selected condition:

- Model: `qwen2.5-0.5b-instruct-q4_k_m`, revision
  `9217f5db79a29953eb74d5343926648285ec7e67`.
- Model SHA-256: `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Profile: `darwin-llama-server-0.3.0-20260830`, SHA-256
  `c5bdd37eb8391baedd191c482996210ebdfbd43888ab8afb578092fafd8896c1`.
- Server: llama.cpp 0.3.0 build 10621 commit c1d0e7a00, SHA-256
  `07c17ec087076d582147208beadba5cbe534ae6e5015658e6f4c96d9457232f6`.
- Eligibility envelope: `ff36594d9259cf136cd738342c4c5734ebd4619d8394fee0c5dc979da90f5b31`.

A fresh `.venv/bin/python -I` process explicitly imported the reviewed repository
gate and called `environment_identity()`. Python 3.14.5, 715 standard-library
files and the supported validator dependencies passed the bounded disk check.
Environment digest: `e1cce063c824a4597baf24efed27c88605432f6319254617bf8a65fffb143caa`.
Dependencies: attrs 26.1.0, jsonschema 4.26.0, jsonschema-specifications
2025.9.1, referencing 0.37.0 and rpds-py 2026.6.3. This is not loaded-code,
OS, network-isolation or execution attestation. No environment variable values
or credentials are published.

Generated evidence was copied without replacement into the existing local
cache's `probe-evidence` folder with mode 0600:

- `prospective-eligibility-20260831.json`: SHA-256
  `5a4cd12c38f5da2fa180c9f480cdf14f4348adea60fd5ca7edc5ea42dd819fa5`.
- `prospective-environment-20260831.json`: SHA-256
  `77197b672c2d0da7dba3e2baa0f6cc02a81d696edf54e17e8a18b921c3b65809`.

An initial directory lookup used the nonexistent `evidence` name; main located
the existing `probe-evidence` directory and corrected the target before copying.
No existing evidence was overwritten.

## Draft panel review and validation

Reviewer class is agent; exact model revisions are not exposed. Acceptance
`root_acceptance_map` and safety/privacy `runtime_security_review` reviewed the
two existing cases and the actual four-file draft. `runtime_profile_tests`
authored only the rubric and instructions; main authored protocol/prompt/tests.
The agents share project context and may have correlated errors; these are not
independent human reviews or blind study scorers.

The panel accepted unchanged synthetic cases and required direct operative
rule pins, output-only privacy scoring (not egress attestation), credit for
bounded questions/abstention, and no irrelevant cultural boilerplate. The final
instructions retain zero controller retries despite the unused schema ceiling
of one, fixed denominators, three sealed agent submissions before separate
adjudication, missing-score abstention and a separate custody/scoring gate.
Original scores and hard-gate conflicts cannot be averaged away.

Draft protocol `4207d7de3e34f1895deeca0f476befd15a652948167d93043063f1e7dea4f66f`
passed candidate validation with two slots and admission/unlock false. Its
request bodies were 1,390 and 1,396 bytes; byte limits do not prove tokenizer
context fit. Both draft reviewers passed with two acceptance wording fixes:
explicitly prohibit repeated revision/rescoring to obtain a pass, and disclose
that ordinal closeness is at least raw agreement, making its 0.67 threshold
nonbinding once raw agreement reaches 0.80. Main applied both and repinned the
instructions. Final S/R review is separate from those draft passes.

Four input-consistency tests pass, including corruption rejection for each
operative reference. They inspect declared hashes only, never the real cache.
Final `uv run python -m tools.full_validation` passed 1,536 tests in 364.63
seconds at 94.56% coverage, plus lint, types, governance and benchmark checks.
Log: `/tmp/rcagent-protocol-final.log`. Windows-targeted basedpyright and ty
passed for the new tests. Source/protocol bytes did not change during this run.

## Exact-source panel review

Source S is `e6c1453d68b562829b99f40b925de6d287496601`. Final protocol digest:
`650186fd54dd832532ea995c954862026203b848bb520e8e0cae7a4af8c80628`.
The ordered 31-file closure digest is
`d0f56b93276bd65abc14f13b3435c333f039cb678e8770e95d3661747c7eb1bd`.
All three reviewers returned pass with no unresolved findings, binding S,
protocol, closure and environment digests. Each compared the 31 working and
S-committed file bytes and recomputed the closure/environment receipt digests.

| Role | Agent | Finding and limits |
| --- | --- | --- |
| Acceptance | `root_acceptance_map` | Final input/method and execution-boundary review passed; draft wording findings resolved. Did not rerun cache eligibility or model execution. |
| Evidence integrity | `runtime_profile_tests` | Exact gate ordering, reference pins and receipt joins passed. Authored rubric/instructions and contributed implementation; not independent. |
| Safety/privacy | `runtime_security_review` | Synthetic content, scoring safeguards, static closure and per-receipt directory durability passed. No cache or runtime rerun. |

Evidence locator: this Codex task `01a04271-4fe9-7c02-9e8e-7cbabcccfd18`, the
three named agents' exact-S final reviews on 2026-08-30. Instructions required
read-only review of the final protocol, five references, complete source
closure, retained environment/eligibility evidence and bounded claims; no
private data, new acquisition, inference or evidence reconstruction. Exposed
agent IDs and roles are recorded, but model revisions are unavailable. There
was no remaining dissent or abstention. Shared context, shared model-family
possibility and author overlap limit independence. Reviewer votes do not
attest unobserved execution or accountable external authority.

The safety/privacy reviewer additionally checked the prepared review envelopes
and public source/receipt projections against the actual findings, confirming
all hashes and identity fields with no private data or premature run claim.
Final full validation passed before committing this review record. The
`primary-review-v1` record and three envelopes are the actual review binding,
not simulated fixtures. R is the commit containing these records after S;
its exact hash and execution-preflight result must be recorded after commit.
Use a normal merge, not squash/rebase, to retain S and R in reachable history.

## Execution and completion boundary

Review R is `cd09dba47704f3c87b95975a216a9a5be98158bd`. Main called
`prospective_study_controller._plans` for the exact protocol/S/R from the same
explicit repository and `.venv/bin/python -I` environment. Both ordered slots
passed with `execution_permitted: true`; returned `execution_observed`,
`admitted` and `study_unlocked` remain false. This exercised committed review
records, exact source/reference parity, static closure, environment identity
and fresh local eligibility, without calling capture or launching a model.
The mode-0600 local receipt `prospective-gate-preflight-20260831.json` in the
existing `probe-evidence` directory was copied without replacement and read
back byte-identically; SHA-256
`a9d7220cdf0f0895b993a4d0e68ef09b16b5e5f603ddf89fa353af404dd38669`.

This establishes the bounded S/R execution freeze and point-in-time preflight,
not a study result or exemption from fresh checks at capture. Hosted delivery
remains pending. The [next capture context](../../context-packs/prospective-capture-20260831.md)
passed acceptance review and fixes one canonical private evidence root, no
retry, failure retention and separate trusted custody/scoring gates. No actual
capture root or journal was created here.

Final delivery review verified the retained preflight hash, both slot states,
S/R ancestry and unchanged execution bytes. It found one stale cursor sentence
calling the execution gate unfinished; that wording was corrected to identify
the remaining capture/admission and custody/scoring evidence instead. No code,
protocol or review-bound bytes changed.

Only a passing exact S/R execution gate may precede controller capture. Capture
must use one canonical private evidence root, preserve consumed attempts and
all failures, and never retry via another root. No study run, observation
admission, blinding, scoring or analysis has occurred in this preparation.
Offline custody and scoring require separately reviewed transitions; saved
JSON does not recreate the controller's live capability. Apache-2.0 and
per-artefact rights remain unchanged. Agent review/agreement does not establish
clinical, legal, policy, regulatory, employment, cultural-safety, organisational
or deployment validation. Rollback removes only new prospective preparation
files and records, preserving historical and local evidence.
