# FAW07 / D0 acceptance and ownership contract

Contract: `faw07-d0-contract-1.0`. Owner: the existing ordinary ChatGPT integration
coordinator. Authority: Dylan's 14 November 2026 instruction to coordinate the
two named ordinary ChatGPT workers in the GitHub project. This contract is ready
for implementation and review; it is not a D0 completion receipt.

## Baseline and scope

Start from master `419c04d7e1c0a16e924e0b7058604671855625a2`, tree
`c0ff3fa9ce5cc78232d3987431ff857c43d1aa68`, the protected merge of
[PR #131](https://github.com/edithatogo/rcagent/pull/131). Its exact final head
`d974f78700e75ce9b266dbdf1cb1a435b03d036a` passed all nine Quality jobs in
[43555675618](https://github.com/edithatogo/rcagent/actions/runs/43555675618).
The merged master itself subsequently passed all nine jobs in
[43556852077](https://github.com/edithatogo/rcagent/actions/runs/43556852077),
privacy/secrets and official conformance. Offline AI security remains queued;
it is not a completed scan.

FAW06 established zero diagnostics across 153 active Python files, an empty
basedpyright baseline, zero policy allowances and rejection of explicit `Any`.
Every new D0 source and test file inherits that zero allowance. Preserve all
existing required checks, branch coverage, mutation and profiling gates.

D0 demonstrates **preservation and inspection of synthetic evidence**: exact
bytes, hashes, explicit byte spans, typed identities, source revisions, duplicate
rejection and unknown/withdrawn source states. Its question is whether accepted
output points to exactly the admitted synthetic source. Reuse the existing
canonical serialization and fingerprint primitives. This is a bounded adapter
and demonstration, not a replacement evidence engine or safety-work schema.

Only generated synthetic inputs are in scope. No AGY credits, Work/Codex chats,
new worker chats, model calls, model downloads, private cases, network source
acquisition, D1 extraction, D2 chronology, D3 decision-time expansion, clinical
qualification or Rust work. Existing later-stage plans remain pending.

## Exclusive ownership

| Lane | Actual worker | Owned files or edit region |
| --- | --- | --- |
| Integration | This coordinator | This contract; `faw07-d0-coordination.json`; shared Conductor index, plan, metadata, context and evidence; CI, locks, baselines, shared schemas; integration branch and all merges |
| Implementation | rcagent — FAW07 demo and receipts | `tools/faw07_d0_demo.py`; `tests/test_faw07_d0_demo.py`; only the D0 import, parser and output hook in `tools/workbench.py` |
| Independent verification | rcagent — Independent verification and synthetic cases | `tests/fixtures/faw07_independent/**` including its existing `verification-receipt.md`; `tests/test_faw07_independent_oracle.py`; `tests/test_faw07_d0_independent.py` if separate production integration tests are needed |

The workers are running according to the owner's report. Their existing GitHub
branches have been observed independently. A branch is not a completed handoff.
Names, exact observed heads, acknowledgement state and findings are recorded in
[the coordination record](./faw07-d0-coordination.json). No extra local agent is
standing in for either ordinary chat.

[PR #132](https://github.com/edithatogo/rcagent/pull/132) is the implementation
handoff and [PR #133](https://github.com/edithatogo/rcagent/pull/133) is the
verifier handoff. Both are drafts. The verifier's existing oracle test and
receipt paths are retained; this supersedes the initially suggested extra
`quality/` receipt path in the coordinator's first issue comment. Do not create
a duplicate receipt merely to match that initial suggestion.

Both workers keep their existing branches. Each posts a draft PR and a handoff
with exact base/head, paths, commands, outcomes and unresolved findings. The
implementation handoff belongs in its PR body. The verifier owns its separate
receipt and must identify the implementation revision actually exercised.
Neither worker edits the other's files, shared contracts, quality configuration
or historical evidence, and neither merges. Report a needed ownership change
on [issue #125](https://github.com/edithatogo/rcagent/issues/125); the coordinator
records the transfer before the new owner edits. Read-only cross-review is
allowed and required where it exposes an interface mismatch.

The coordinator's available browser reaches a sign-in page for the private chat
links. Issue #125 and the worker PRs are therefore the observed coordination
channel. Publication does not imply that a worker has read or acknowledged it.
No new login, chat type or execution service is required to proceed via GitHub.

## Entry points and input contract

The canonical demonstration command is:

```sh
uv run --no-sync python -m tools.workbench d0-demo
```

It emits the complete JSON receipt on stdout, followed by one LF. It accepts no
case-file path, URL, private input, model argument or hidden network fallback.
A zero exit means the finite demonstration ran and emitted a receipt; expected
negative cases remain visible as rejections. It does not mean clinical success.
Optional module output-file support must produce the same bytes and must not
silently overwrite an existing file. A write failure is nonzero, not a pass.

The Python inspection seam is `inspect_case(case)` in `tools.faw07_d0_demo`.
It validates raw values before issuing typed observations. The following is the
coordinator's input contract, `faw07-d0-input-1.0`, retaining the implementation's
existing field names where possible:

| Object | Required fields and meaning |
| --- | --- |
| Case | Nonempty `case_id`; nonempty `sources` and `evidence` arrays of objects |
| Source | Nonempty `id`; positive integer `version`; nonempty `case_id`; `state` equal to `present`, `unknown` or `withdrawn` |
| Present source | `content` is exact UTF-8-encodable text and `fingerprint` is its declared `sha256:<hex>` byte digest; no normalization or newline conversion |
| Unknown source | `content` is absent; bytes and digest remain unknown, never fabricated |
| Withdrawn source | May retain exact synthetic `content` for inspection; it cannot support an accepted span |
| Evidence | Nonempty `id`, `case_id`, `source_id`, `text`; positive integer `source_version`; `source_sha256`; `coordinate_system`; integer `start_byte` and `end_byte` |
| Digest | `source_sha256` is `sha256:` followed by exactly 64 lowercase hexadecimal characters; it must equal SHA-256 of the selected source version's raw UTF-8 bytes |
| Coordinates | `coordinate_system` is exactly `utf8-byte`; zero-based half-open interval `[start_byte, end_byte)`; integer values exclude booleans |

Case binding is explicit: source and evidence `case_id` must equal the containing
case. A source identity is `(case_id, id, version)` and an evidence identity is
`(case_id, id)`. Evidence `source_id` resolves only against sources, never another
entity kind. Different versions of one source are retained separately. Duplicate
source identity or duplicate evidence identity rejects the case even if the
duplicates have identical bytes. Equal text from distinct sources is not
independent corroboration.

For acceptance, the source must be present; its declared `fingerprint`, the
actual bytes and the evidence's `source_sha256` must agree; the claimed version
must match; `0 <= start_byte < end_byte <= len(raw_bytes)`; the slice must decode as
UTF-8 at both boundaries; and its decoded text must equal the submitted `text`
exactly. Unicode code-point positions are not byte positions. Neither source
hashes nor quotes establish that the underlying account is true.

Malformed shapes or field types raise a documented `ValueError` before receipt
publication. Structurally valid but invalid evidence returns `status=rejected`
with a nonempty, stable error list. Every rejection path must be observable;
uncaught `KeyError`, `AttributeError` or encoding failure is not the intended
rejection contract. Unknown optional fields must not silently stand in for any
required field. Enforce finite input limits for this seam: at most 32 sources,
64 evidence entries and 65,536 UTF-8 bytes per present source per case. Exceeding
a limit raises `ValueError`; no schema allowance or implicit truncation is added.

A case with any error has **no admitted spans** (`spans=[]`). Diagnostic source
observations may remain inspectable. This prevents a consumer from promoting a
valid-looking prefix of a rejected case. An accepted case must have at least one
fully checked span; an empty input cannot pass through all-abstention.

## Deterministic receipt

`generate_receipt()` runs a fixed, versioned synthetic corpus. It includes at
least two accepted and three rejected examples; the independent verifier freezes
their exact expected results separately. Production inputs contain no oracle
expected labels. Add examples only with an explicit generator version change.

The receipt retains `schema_version=faw07-d0-receipt-1.0`, `task=FAW07/D0`,
`dataset=generated-synthetic-only`, the canonical command, explicit coordinate
and source-hash algorithms, per-case observations, counts, limitations and
`output_fingerprint`. It additionally exposes:

- `input_schema_version`, `rule_version`, `generator_version` and the permitted
  view `synthetic-d0-evidence-only`;
- the actual synthetic `inputs` and `input_fingerprint` over their canonical
  JSON, so every source byte and accepted slice can be inspected independently;
- `dependency_lock_sha256`, computed from the actual `uv.lock` bytes;
- `implementation_files`, a relative-path-to-SHA-256 mapping of the demo,
  workbench entry point and reused evidence-core serialization source.

Source and file digests use the same `sha256:<hex>` notation. The exact field
names above are shared; workers may request a justified amendment before
changing them. Source/lock identity is content-bound, so the producer does not
need to invoke Git or hard-code a self-referential commit hash.

Canonical JSON uses UTF-8, sorted object keys, compact separators and no ASCII
escaping; stdout adds exactly one LF. `output_fingerprint` is SHA-256 of the
canonical receipt **with the fingerprint field omitted**, excluding the stdout
LF. Counts reconcile exactly with the emitted cases and accepted/rejected states.
No NaN, Infinity, wall-clock timestamp, random identifier, absolute path or
environment-dependent field enters that deterministic payload.

Run time, Python/platform versions, process exit status, command, source commit,
implementation-file hashes, lock hash, artifact byte hash and measured resource
observations belong in the verifier's execution receipt. It binds those
observations to the deterministic artifact without changing its content digest.
Runtime observations are not p95 latency, resident-memory or performance claims.

Every receipt explicitly limits its conclusion to synthetic source identity and
byte-span inspection. No accepted finding, chronology, clinical/model validity,
independent corroboration, legal protection or public-disclosure authority is
implied. Historical negative studies are not rerun, relabelled or superseded.

## Independent verification and translation

The verifier's existing `d0_oracle.json` remains a separate representation. Its
expected labels must be checked against literal source bytes and hand-specified
cases before production is called. Do not generate expected results with
`inspect_case`, the demo generator or a production fingerprint helper.

Only a transparent representation adapter is needed:

| Independent fixture field | Production field |
| --- | --- |
| Source `revision`, `text`, `sha256`, `state=admitted` | `version`, `content`, `fingerprint` (add the notation prefix only), `state=present` |
| Source `id`, `case_id`; withdrawn state | Same identity/case; `state=withdrawn` |
| Claim `revision`, `digest`, `unit` | `source_version`, `source_sha256` (add the notation prefix only), `coordinate_system` |
| Claim `start`, `end`, `span_text` | `start_byte`, `end_byte`, `text` |
| Claim `case_id`, `source_id` | Same fields; synthetic evidence `id` is the fixed case identifier |

The adapter preserves incorrect/missing values. It must not repair forged
digests, infer missing hashes, change byte coordinates, remove duplicate sources
or discard cross-case sources to obtain a pass. For an isolated claim case,
retain the requested source ID's available revisions and original `case_id`.
For an unknown source ID, include an explicit known control source in the case
so rejection tests the unresolved reference rather than an empty source array.
Collection checks preserve all declared duplicates and revisions within each
case. Partition a legitimate multi-case collection by its literal source
`case_id` for the per-case entry point; never relabel or move an individual
cross-case claim to make it valid. Wrong-kind references and missing identities
remain negative cases. Error labels may be mapped to the documented production error
category, but a generic exception is not equivalent to the intended rejection.

Acceptance exercises the actual production seam **and** the workbench subprocess
command. It requires all positive controls to pass and every known-invalid case
to reject, with denominators and reason categories. Cover forged/stale digests,
cross-case and wrong-kind links, absent versions, duplicate identities, unknown
and withdrawn sources, malformed/missing fields, invalid bounds, split UTF-8,
wrong coordinate units and byte/quote mismatches. Include bounded generated
properties and metamorphic checks for repeatability, harmless collection
reordering and one-byte tampering. Reordering compares source/evidence identities
and verdicts rather than assuming identical presentation-array order.

Two clean-process command runs must have identical output bytes for identical
source/lock/input versions. Recompute input and output fingerprints, raw source
hashes, accepted slices and count totals using standard library operations in
the verification lane. A changed byte must change its digest and invalidate any
stale binding. An oracle self-test without running production is recorded as
oracle preparation only, never as D0 acceptance.

## Acceptance gates and integration order

| Gate | Required evidence | Owner |
| --- | --- | --- |
| A0: ownership | This versioned contract; non-overlapping path lists; actual worker branch/head and acknowledgement or explicitly missing acknowledgement | Coordinator |
| A1: implementation | Real command and inspectable artifact; validated identities/digests/spans; deterministic failure behaviour; narrow unit tests | Implementation |
| A2: independent verification | Positive and negative oracle denominators; independent byte/hash calculations; actual production and subprocess execution; exact tested implementation SHA/tree or file hashes; honest failure receipt | Verifier |
| A3: strict engineering | Empty baseline/caps; zero basedpyright diagnostics; ty, Ruff lint/format, Bandit, Vulture, repository validation, benchmark and full branch-covered test suite | Coordinator checks worker evidence and integrated head |
| A4: hosted delivery | Exact integrated head passes dependency review, every Quality job, privacy/secrets and official conformance; normal protected merge against current master | Coordinator only |
| A5: acceptance record | Reconciled worker receipts, integrated diff, final-head CI and merge SHA; unchanged negative evidence; FAW07 completion recorded only then | Coordinator only |

The active master ruleset requires `dependency-review`,
`validate (ubuntu-latest)`, `validate (macos-latest)` and
`validate (windows-latest)`, with an up-to-date base. The Linux aggregate requires
both Python jobs, all platforms, mutation, profiling and combined coverage.
Linux/macOS and the validated four-input combined branch database retain the
90% floor. The release boundary retains all 24 real mutation kills and the
profiling workload retains 300 completed synthetic iterations. Existing scope
is preserved; these gates do not become D0-specific mutation or performance
qualification by association. No bypass, reduced coverage, new skip, allowance,
disabled rule or additional routine human approval is introduced.

First merge the coordinator's contract-only PR after its required checks.
Workers then reconcile their branches with that master. The verifier exercises
the implementation's exact candidate revision in an isolated checkout without
copying production code into its owned changes. The coordinator combines the
implementation and verifier changes into one D0 integration candidate, resolves
only integration-owned conflicts, and runs the full gates. Worker PRs remain
traceable and are closed with the integration reference when superseded. Do not
merge a failing verification branch by changing expected results or omitting it.

Keep FAW07 `[~]`, Track 13 open and qualified clinical/model capabilities at zero
until A1–A5 have direct evidence. A0 alone is contract publication. Later-stage
work is not implied by D0 acceptance. If a worker handoff is unavailable, record
the exact missing receipt/commit and resume cursor; do not duplicate its scope.

## Historical evidence and rollback

Preserve consumed source `e6c1453d68b562829b99f40b925de6d287496601`, review
`cd09dba47704f3c87b95975a216a9a5be98158bd`, protocol SHA-256
`650186fd54dd832532ea995c954862026203b848bb520e8e0cae7a4af8c80628`,
historical profile SHA-256
`c5bdd37eb8391baedd191c482996210ebdfbd43888ab8afb578092fafd8896c1`
and the **0/2 admitted observations** outcome. Current `typing-20261114`
engineering identities remain distinct. The two source-bound Bandit findings
and their baseline are outside the D0 edit set.

Rollback is a normal revert of the new D0 integration commit, leaving FAW06,
the historical receipts and prior negative evidence intact. Record failed
attempts and superseding receipts; do not rewrite old observations into passes.
