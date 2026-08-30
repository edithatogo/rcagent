# Local execution provenance probe

## Scope and runtime drift

Base: `eada611`; branch: `codex/local-execution-provenance`. This is a fresh
non-study capability probe under the existing comparator decision, not a
primary observation, prospective protocol freeze, scoring run or admission.

The fresh full comparator admission check failed before model execution:
`/opt/homebrew/bin/llama-cli` now resolves to Homebrew 0.3.0, SHA-256
`dd6208ade8be12c77c3342ff09b2b0963515c5b9083753f46fecbed364754618`.
The unchanged registry admits 0.2.0, executable SHA-256
`456af2d481095b6a953b6ad21e9caa0411e5508955eb841f37574235da10a44e`.
The exact original binary remains at
`/opt/homebrew/Cellar/llama.cpp/0.2.0/bin/llama-cli`. The probe permits an
explicit alternate path only if the original admitted hash still matches.
No Homebrew symlink, historical registry, library, model or installation was
changed. Full admission still validates all three comparator size classes.

## Probe contract

```sh
uv run python -m tools.local_execution_probe --model-root /Volumes/PortableSSD/rcagent-model-cache --runtime-path /opt/homebrew/Cellar/llama.cpp/0.2.0/bin/llama-cli
```

The registry bytes are pinned in the adapter. It selects only the previously
admitted Qwen2.5 0.5B Instruct Q4_K_M revision, using a fixed synthetic software
prompt unrelated to the two planned study cases. Limits: 16 generated tokens,
seed 42, temperature 0, single turn, null stdin, 60-second timeout and a
minimal LANG/PATH environment. No inherited credentials, provider settings,
shell command or remote model argument is supplied.

The receipt retains exact raw stdout in base64 plus its hash, stderr hash and
byte count without publishing stderr contents, start/end UTC, monotonic elapsed
time, exit/timeout state, and registry/adapter/runtime/model/prompt pins.
Local paths are replaced by pinned identities in the published argument list.
Post-run hashes must still match. A nonzero exit, timeout, empty stdout,
oversized output or pin drift cannot report `process_completed`.
Exit 0 means process completion only; every receipt has `admitted: false` and
`study_unlocked: false`. Launch/admission failures do not claim execution.

Output retention is capped at 64 KiB per stream; oversized streams have no
partial-content hash masquerading as a full hash. Temporary files are not a
disk quota. The admitted executable is trusted; this is not a sandbox for an
arbitrary binary, adversarial filesystem or concurrent file replacement.
Network status means local-file invocation, not independently monitored or
enforced egress isolation. Dynamic libraries and the OS are not hash-attested;
the retained binary's loader-relative libraries do not establish complete
reproducibility. No new runtime version is admitted by this probe.

## Evidence and remaining boundary

The initial fixture-first test failed because the new module was absent.
Twenty focused tests passed with 100% statement/branch coverage of the probe.
`uv run python -m tools.full_validation` then passed 587 tests, 92.71% overall
coverage, lint, types, governance and benchmark checks on macOS/Python 3.14.5.

Agent reviewers `probe_scope_review` and `probe_security` reviewed authority,
code and provenance limitations; `probe_tests` implemented adversarial tests.
The security reviewer rechecked the final device/quantisation disclosures and
failure tests, reporting no blocking finding. Exact model revisions were not
exposed. These are agent engineering reviews, not independent human agreement;
correlated review errors remain possible.

After those gates, one live probe ran at 2026-08-30T05:40:17Z using the exact
retained 0.2.0 binary and admitted cached model. It exited 0 in approximately
29.95 seconds, with 1,141 stdout bytes, zero stderr bytes and unchanged checked
pins. Manual inspection found the generated response `READY`, as well as the
runtime banner and local model path. No study case or score was processed.

The [public receipt projection](../../../evaluation/prospective/probes/local-execution-20260830.json)
omits raw stdout because of the runtime's local path disclosure. The exact raw
JSON is retained outside Git at the operator's existing model cache under
`probe-evidence/probe-20260830T054017Z.json`, SHA-256
`8b19a909875439e1a259ced6a9aece8586eeb851cc6f439ab89cfe292672bb05`.
Its base64 stdout was decoded locally and verified against its length/hash.
The projection preserves all other fields and declares its omission; it is
not a substitute for the full local raw receipt. Future CLI output must also
be inspected before publication: redacted arguments do not redact raw stdout.

The existing prospective inventory remains unchanged: two pending slots and
zero admitted observations. Next: bind executable-condition provenance to a
frozen prospective protocol with verified runtime dependencies and affirmative
admission, then separate blinding/scoring/analysis checks. The parent track and
root #1 remain incomplete. No repeat approval is needed for bounded work.

No model weights, private clinical/employee data or credentials are distributed.
This probe makes no model recommendation, clinical, policy, legal, regulatory,
employment, cultural-safety, organisational or deployment validation claim.
Agent review is not independent human agreement. Retain the old preflight
locks if the new adapter or receipt is rolled back.
