# Frozen prospective capture: retained negative outcome

Owning track: `eval-blocker-remediation_20260803`; root issue #1 remains open.
This is operational evidence, not scoring, study completion or validation for
clinical, legal, policy, regulatory, employment, cultural-safety, organisational
or deployment use. Apache-2.0 and per-artefact rights boundaries are unchanged.

## Invocation and frozen scope

Main invoked `tools.prospective_study_controller.run_study` exactly once in an
isolated `.venv/bin/python -I` interpreter with the explicit repository import
path, after baseline full validation passed (1,536 tests, 94.56% coverage).
Activation `3d1693a` and in-progress checkpoint `1243914` preserve the cursor.
The invocation ran from `2026-08-30T21:26:59.929521+00:00` to
`2026-08-30T21:37:06.337046+00:00`; terminal session 14492 finished with exit 0.
That exit means the controller returned, not that capture succeeded.

- Source S: `e6c1453d68b562829b99f40b925de6d287496601`.
- Review R: `cd09dba47704f3c87b95975a216a9a5be98158bd`.
- Protocol SHA-256: `650186fd54dd832532ea995c954862026203b848bb520e8e0cae7a4af8c80628`.
- Run ID: `71ac409cab4b35f9ab28af73ef56612457b3a53779a675d545fa4ac91aee65da`.
- Model: pinned Qwen2.5 0.5B Instruct Q4_K_M, native completion, seed 42,
  temperature 0, output cap 512, context 2048, session deadline 120 seconds.
- Runtime: frozen llama.cpp server 0.3.0 Darwin/arm64 profile, private Unix
  socket; no OS/egress-isolation attestation.

The canonical private root is
`/Volumes/PortableSSD/rcagent-model-cache/study-evidence`, created once with
mode 0700 after its absence was checked. Return and stderr were exclusively
created with no-clobber and umask 077. No retry, alternate root, acquisition,
provider call, scoring, or source modification was performed.

## Exact outcome and denominator

Controller status: `controller_failed`, error `capture_or_admission_failed`,
stage `readback`. The retained first receipt says `session_failed`, error
`incomplete_generation`, stage `completion_failed`. Controller `readback` is
where that negative primary return was classified; it is not evidence of
corrupt storage. Admission, admission-before-blinding, unlock and scoring are
all false. No positive custody record or scorer packet may be produced.

| Frozen slot | Recorded disposition |
| --- | --- |
| `case-missing__condition-local-text__r1` | `failed-receipt-retained` |
| `case-conflict__condition-local-text__r1` | `not-attempted` |

The journal contains run-start, first-slot-start, first-slot-failed, and
capture-failed events. A start alone is not execution evidence; the retained
process receipt separately records execution observed, child reaped, return
code 0, worker joined, resources removed and no cleanup errors. Transport
capture success is not complete-generation success.

## Private evidence identity

Root-relative locators below are private custody references, not public raw
attachments. `run/` denotes the exact `run-<run ID>` directory above.

| File | SHA-256 |
| --- | --- |
| `controller-return-20260831.json` | `0a81090203058e67aaeeb68b11830549fe0f650f3b09cdfeef7b811c3fed9121` |
| `controller-stderr-20260831.txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `run/journal.jsonl` | `bcf77db7a62c0265e3216ff9e87703acd6ec3e62646da1ea9f55cb1cc246cd2a` |
| `run/slot-1.json` | `7daf4faef631650a8f081a5a87450dea5efb7d071fa8d187fd0dd228d22d478b` |

Raw responses, request bodies, process streams and local diagnostics are not
included in this public projection. Preserve the exact failed receipt and
missing second-slot disposition, rather than creating replacement evidence.

## Review and next route

Three read-only agent roles passed retained-negative-evidence review:
`root_acceptance_map` (acceptance), `runtime_profile_tests` (evidence consistency)
and `runtime_security_review` (safety). All independently found HTTP 200 with a
complete body but native `stop_type=limit`, 512 predicted tokens, 242 evaluated
tokens and `truncated=false`. The frozen EOS-only decoder correctly returns
`incomplete_generation`. This is not a timeout or context truncation.

Panel checks confirmed the journal chain, exact request reconstruction,
receipt/body/stream hashes and byte counts, two-slot denominator, private
ownership/modes and single-link files. Socket and temporary session directory
are absent. The response body hash is
`f9478baa377e605c048bd1702c7dac8be2245eb1fb2db198d9559e5cd3ac755d`.
Retrospective loader inventory is not successful session postflight: the
failure occurred before that block, and runtime verification remains false.
The original in-memory primary return cannot be reconstructed independently;
the controller's comparison is implementation evidence, not a new witness.
Agent review establishes neither blinded scoring nor human agreement.
PR #103 passed all seven checks at `31cc89ed1350ef54513b22a26d7af33e8e161c4f`
and merged normally as `25f7f3ae0ac349b8dfd336ce3dff399c5e11a9d1` at
2026-08-30T21:49:51Z. Exact tree parity
`7610d691358c450c05ff8931157c7eba9a27d4e1` and S/R ancestry were verified.
Final local full validation passed 1,536 tests in 413.96 seconds at 94.56%.
Post-merge Quality `33337488195` and conformance `33337488240` both passed,
freshly verified on the 23:00 UTC continuation. Local master was fast-forwarded;
completed local/remote-tracking branch cleanup followed verified remote absence.

Use Branch B of the [post-capture context](../../context-packs/prospective-postcapture-20260831.md):
bounded diagnosis from retained bytes and frozen source, then scope-correct
readiness-only evidence. This run has no admitted cohort; that does not prove
all other models or runtimes unavailable. Do not retry this consumed run or
alter generation settings retrospectively. Historical H0–H8/H8P, the owning
track's broader acceptance map and root #1 remain separate and unresolved.
