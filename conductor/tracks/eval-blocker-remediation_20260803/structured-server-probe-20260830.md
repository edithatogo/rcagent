# Structured non-study server observation

## Scope and execution identity

One fixed synthetic probe ran on 2026-08-30 UTC under
[committed context](../../context-packs/structured-server-probe-20260830.md)
`6bfd1a1`. Source/test bytes were unchanged from merged `64810aa` (PR #92),
whose seven exact-head checks and both post-merge workflows passed. No source
was patched for the observation. Fresh per-artefact eligibility checked the
existing canonical local cache, all original model classes/licences and the
separate pinned server profile before launch; postflight checks agreed.

Model: Qwen2.5-0.5B-Instruct GGUF Q4_K_M, immutable revision
`9217f5db79a29953eb74d5343926648285ec7e67`, model SHA-256
`74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
The existing Apache-2.0 model licence and separate runtime/component rights
controls remain unchanged. No download, credential, paid provider, private data,
remote code, new network route or redistribution was introduced.

The unchanged fixed READY request used the admitted server, private Unix socket,
explicit offline/no-agent/no-UI/no-MCP-proxy options and cleared profile
environment. These controls are not OS-wide egress or peer authentication.

## Observed result and negative finding

The session returned `session_captured`, error `none`, with admission and study
unlock both false. Five bounded HTTP 503 loading observations preceded exact
status-ok health and one HTTP 200 completion. The complete native response was
1,748 bytes and passed strict settings/EOS decoding. It contained 32 decoded
UTF-8 content bytes, nine predicted tokens and fourteen evaluated tokens.

**Exact decoded content equality with `READY` was false.** No stripping,
case-folding, extraction, prompt tuning or retry was used to manufacture a pass.
This is structured capability evidence, not instruction-following success or
model-quality evidence. The native completion prompt is not automatically a
chat-message contract; a study runner must explicitly freeze its serialization.

All 15 non-system loader images matched the pinned profile, with loader PID
matching the captured direct child. Complete stdout was empty; complete stderr
was 102,450 bytes. Neither stream was truncated. Graceful TERM was sent, no
KILL was required, return code was zero, and capture elapsed 1.4718 seconds
(excluding eligibility hashing). Worker join, child reaping and owned socket
directory removal were confirmed; no cleanup errors were reported. Main also
checked that the recorded directory no longer existed.

## Local custody and reviewed projection

The exclusive `0600`, 151,533-byte raw receipt remains in the existing governed
local cache's evidence folder as `structured-server-v030-20260830.json`.
It was read back after successful return. Public source records contain only
this reviewed summary, not raw logs, response content or model bytes.

| Artefact | SHA-256 |
| --- | --- |
| Complete local receipt | `c4e6104bfd08f97d0b36ca5b7b42e2665593668c002eee3d3ad21de724e9ea5e` |
| Request bytes | `8a88c2cc67b2b67e24643edd623abe84b8c83845bf6f2ce14c1f911de85c8e8c` |
| Native response body | `26242cc2f30c25802259259d5c545be077e143bed387b1f9e328c8601cd9ab16` |
| Decoded content | `c435df96bc9500ef09454e4dae19c6c91adfb9fb79bb752e6d03561f4488b63c` |
| Complete stderr | `edd9e3c4d5eef421428ed41a8521278b0186f3aca6d5c5bd6fbb8f00964dcacf` |
| Eligibility envelope | `ff36594d9259cf136cd738342c4c5734ebd4619d8394fee0c5dc979da90f5b31` |
| Server profile | `c5bdd37eb8391baedd191c482996210ebdfbd43888ab8afb578092fafd8896c1` |
| Fixed session source | `8c7353942a3c3c1bab492f70a8a892ea0b4d92eef80783c9778205a4dca17fc7` |

The raw receipt retains the complete thirteen-module source inventory, actual
invocation, environment digest and model/registry identities. Source observations
are not a frozen study protocol or immutable loaded-code attestation.

## Review and next work

Both reviewing agents recommended the bounded attempt before execution. Main
owns execution and custody inspection; acceptance agent independently checks
the local receipt without launching anything. Independent-context agent receipt
review passed the hashes/counts, strict native re-decode, settings/EOS, fifteen
images and matching child PID, all thirteen source pins against both committed
revisions, fixed invocation/environment, health sequence and cleanup. It did
not repeat the model run or all-model cache hashing.
The implementation agent separately reviewed this public projection and found
no raw-log/content disclosure or unsupported admission/accuracy claim. Stale
plan wording was identified and reconciled; the negative READY finding remains.
After the observation and record updates, `uv run python -m tools.full_validation`
passed 1,106 tests in 85.03 seconds at 93.91% coverage, including all preceding
lint, native types, governance and deterministic benchmark gates. This test run
did not repeat the model observation. Hosted evidence delivery is pending.
Exact agent model revisions are not exposed; correlated errors remain possible.
This is agent engineering review, not human agreement or clinical, legal,
policy, regulatory, employment, cultural-safety, organisational or deployment
validation.

Preserve this single observation and the negative READY finding. Do not repeat
it without a distinct evidentiary purpose. Next implement the primary runner and
explicit prompt/normalization contract, full-component freeze and affirmative
admission-before-blinding transitions using synthetic fixtures. Historical
H0–H8/H8P, unavailable client observations and root issue #1 remain unchanged.
No study slot or score was generated. Rollback retains this raw observation and
reverts only successor repository records or code, not historical evidence.
