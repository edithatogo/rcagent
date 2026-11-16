# H4 independent engineering review

The production author, independent test author and read-only reviewer used
disjoint ownership. The integration agent reconciled contracts, performed
additional code/output review, ran the full gate and reproduced the actual CLI.
These are agent engineering reviews with shared-model/shared-context correlation
limits; they are not independent human or clinical validation.

## Original checkpoint source

| File | Original checkpoint SHA-256 |
| --- | --- |
| `tools/heaps.py` | `ea9fe374ae7f387d92d11ab7800bd2c636d947f5e62a03e88d5ed75c504dd55b` |
| `tools/heaps_validation.py` | `d3bbcffdcfc88f5e453ea6863e22ae5f40727b0425bb3da4be8226ef4ea9a7ae` |
| `tests/test_heaps.py` | `5b794df73241730efca79cc3d5863b7fd765969e2955dfa2fd7c1081da36ffcb` |

The read-only reviewer independently computed raw hashes/canonical bindings and
called the public byte API without production fixture-oracle helpers. Its final
inline verifier exited 0 with 24 behavioural assertions and four start/end
source-hash assertions. The same behaviours have persistent regressions in the
220-test module. Both source hashes remained unchanged during reproduction.
The reviewer reported no remaining material finding within the declared H4
subset and recommended integration subject to repository/hosted gates.

## Findings and repairs

| Finding | Repair and discriminating check |
| --- | --- |
| High: changed historical `report.md` bytes could disappear from the generated inventory, allowing an old synthetic decision to remain reviewed | Capture every distinct consumed historical artifact or reject it. A correctly rebound changed historical report changes the construction hash and stales the old decision; old decision bytes are preserved. |
| Generated manifest could not reenter because source paths were rewritten | Preserve coherent source paths and verify exact current-manifest reentry without changing construction identity. |
| Semantically equal historical case/profile bytes and extra historical sources could be ignored | Retain different raw case/profile bytes; reject source inventory entries outside the declared canonical source set. |
| Manifest/status verification input bytes lacked a durable identity | Retain their raw captures and bind them in a later, explicitly scoped verification receipt outside construction. Raw-presentation changes alter that observation without inventing a new report. |
| Impossible canonical `reviewed_at` and event `deadline` were admitted | Cover both canonical timestamp fields with strict parsing; independently rebound adversarial cases reject. |
| Missing source availability and contradictory local locators could look complete | Require explicit canonical-source coverage, consistent family/locator bindings and exact available bytes. |
| Nested object-key order changed report bytes | Sort object fields while preserving meaningful array order; normalised profile/report remain stable while raw ingress changes the manifest. |
| Mapped taxonomy lacked an admitted basis | Require matching available captured taxonomy identity/version/purpose; retain category-fit limitations. |
| Path collisions, receipt-shaped construction inputs and output failure could undermine packet integrity | Enforce portable paths/reserved channels, reject disguised receipt payloads, stage output before publication, and test failure cleanup without overwriting existing work. |
| Returned status mutation could affect later runs | Copy mutable limitation data and verify independent subsequent observations. |

The initial red test established the absent consumer. Subsequent failing
regressions were retained while the implementation was repaired. Literal H3
expectations and frozen source bytes were not changed to manufacture passes.

One test assumption was corrected after contract review: H3 does not require an
old decision's evaluation timestamp to equal a later explicit observation clock.
A valid historical annotation remains intact; current validity is checked
against the caller's time. Rendering tests were also corrected to inspect the
literal visible text after Markdown escaping, and a manifest-binding test used
valid JSON for its JSON mapping artifact so that it isolated the intended
binding defect.

An early module-only coverage diagnostic failed its inherited 90% floor at
74.66%; actual CLI subprocess lines were outside that parent-process
measurement. It is not recorded as a passing gate. The complete final repository
run reached 92.94% but retained 52 environment-denied socket failures, as detailed
in [the H4 receipt](./h4.md). No gate was weakened.

## Final evidence and limits

- [Frozen-oracle execution](./h4-execution.json): 38/38 matching dispositions
  across 25 cases, with errors, counts and input identities.
- [Two clean CLI runs](./h4-replay.json): 16 files / 94,722 bytes, exact equality,
  commands and output/component hashes.
- [Conformance](./h4-conformance.json): pinned official validator and current
  upstream drift assessment passed.
- Full strict gate and subsequent hosted results remain separate observations;
  source-bound local evidence is not a hosted pass.

The narrower runtime subset is documented in
[the usage guide](../../../evaluation/heaps/h4-usage.md): safe synthetic text,
UTC calendar assertions, bound taxonomy declarations, detached verification
channels and unchanged export restrictions. D0/AcciMap composition, current
local instrument conformity, actual identity/authority and clinical performance
remain unqualified. This closes the H4 implementation review, not H5 or H6.

## Hosted portability follow-up

The first publication exposed a Windows static-type error in the Unix FIFO test. A separate read-only review accepted the minimal capability-guard repair; production bytes and POSIX rejection assertions are unchanged. The failed job, exact old/new test identities and independent checks are retained in [h4-hosted-repair.md](./h4-hosted-repair.md). This does not replace the requirement for a fresh hosted Windows pass.

## Subsequent hosted review findings

Hosted review subsequently found two boundary defects missed by the original
checkpoint: canonical support edges could bypass withdrawn-factor eligibility,
and uppercase detached filenames could collide with generated outputs. The
earlier no-material-findings recommendation is preserved as that checkpoint's
observation; it was superseded until the new findings were repaired and checked.
The [follow-up receipt](./h4-hosted-review-repair.md) records the reproduced
failures, bounded repairs, independent review and new source-bound verification.
The original execution and replay records above retain their original hashes.
