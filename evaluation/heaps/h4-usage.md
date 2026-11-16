# HEAPS synthetic packet consumer

H4 prepares a deterministic review packet from a prestructured safety-work 1.1
case and its HEAPS profile. It retains accounts, evidence, alternative
explanations, proposed findings, participation concerns and unresolved questions
in their recorded roles. It does not infer clinical truth or actual authority.

## Run the supplied synthetic example

From the repository root, install the committed validation environment:

```sh
uv sync --locked --extra validate --extra test --extra lint --extra assurance
```

Then run the public entry point with an explicit fictional evaluation clock and
a new output directory:

```sh
uv run --no-sync python -m tools.heaps \
  --case tests/fixtures/heaps/canonical/base-case.json \
  --profile tests/fixtures/heaps/packet/base-profile.json \
  --artifacts tests/fixtures/heaps \
  --template packet/template-v1.md \
  --evaluated-at 2030-01-07T00:00:00Z \
  --output heaps-example
```

The date belongs to the fictional fixture; it is not the current date or a
policy deadline. Repeating the command with the same input bytes, evaluation
time and component revision in another new directory must produce identical
packet bytes.

| Exit code | Disposition |
| --- | --- |
| `0` | A synthetic draft was prepared. |
| `2` | Input or output-boundary admission failed. |
| `3` | The admitted case was empty or all statements were excluded from draft representation. |

The Python entry point is
`tools.heaps.assemble_packet(case_bytes, profile_bytes, artifacts, *, evaluated_at, ...)`.
It accepts captured bytes and returns separate preparation and review
dispositions, errors, generated files and a status observation. It performs no
network calls, model calls or external submission.

The base example emits `report.md`, `chronology.md` and `actions.md`, normalised
`case.json` and `profile.json`, an original mapping and template, unchanged source
files, the original JSON ingress captures, and detached manifest/status/
verification records. A supplied synthetic decision is preserved separately.

## Input and identity rules

Supply generated-synthetic, fully local case and profile records. A declaration
of synthetic origin is not proof of provenance; this interface is not a
de-identification service or an authorised path for clinical records.

JSON admission rejects malformed UTF-8, a byte-order mark, duplicate keys,
nonfinite numbers and unpaired surrogates. Schema and semantic checks then
validate the case, exact versions, typed references, source families, dates and
artifact bindings. The shared canonical schema remains unchanged.

Direct canonical `supports` relationships and supplementary profile support
references use the same eligibility rule for findings marked accepted. A
withdrawn or rejected factor or statement, a factor backed by such a statement,
or withdrawn evidence cannot supply that positive support. Other relationship
types and unreviewed draft findings retain their recorded roles; this check does
not infer transitive support or establish the finding's truth.

Captured source and template bytes are preserved exactly. Generated JSON uses
sorted keys, two-space indentation, unescaped Unicode and one terminal LF.
Original case and profile ingress bytes are retained separately from normalised
JSON. Reordering object keys can preserve the canonical case identity while
changing its raw capture and the packet manifest. Changing array order changes
the canonical identity.

The detached manifest inventories the exact bytes consumed or emitted before
review. A decision and later status observation remain outside that inventory,
so neither can change the artifact it claims to describe. Material changes
invalidate a prior packet decision. A simulated draft decision does not approve
findings, actions, effectiveness, closure or disclosure.

### Detached verification inputs

Optional `--manifest`, `--decision` and `--status` arguments are verification
inputs. Every artifact named in a supplied manifest is checked and must be
represented in the new construction inventory or rejected. Historical artifacts
are never skipped merely because their filenames resemble generated outputs.

The supplied manifest itself is a detached verification object. Its original
bytes are retained as `verification-input-manifest.json`; a supplied status claim
is retained as `verification-input-status.json`. The later `verification.json`
receipt binds those exact inputs and the generated manifest and status, records
the explicit evaluation time and fixes authority/clinical/submission claims at
unverified, not-established and not-submitted. These verification files sit
outside the decision-covered construction inventory.
This preserves an acyclic construction: verifying an unchanged current manifest
does not repeatedly insert another copy of itself into the packet it describes.

The verification receipt's schema identifier is `heaps-verification-1.0`; it is
an H4 execution observation, separate from the four frozen H3 input contracts.
A changed verification input cannot silently retain the same verification
receipt even when the report material is unchanged.

## Supported input subset

H4 supports bounded, safe synthetic text artifacts: at most 4 MiB per artifact,
32 MiB of consumed/generated material and 64 levels of JSON nesting. Artifact
paths must be safe relative paths without case-insensitive collisions, traversal
or reserved platform names. The CLI rejects symlinks and existing output paths.
It stages output before making the packet available.

The existing shared export restrictions remain in force for all rendered
content. Active links, values caught by the shared sensitive-content checks and
HTTPS locators inside the runtime profile are rejected. H3 permits metadata shapes that this narrower H4
consumer does not yet support; schema validity alone does not guarantee runtime
admission. This limitation does not change H3 or qualify a local instrument.

Specified synthetic calendar assertions currently support explicit UTC only.
The consumer does not depend on the host's installed timezone database. Other
zones remain unsupported in this version, and the underlying obligation and
calendar must still have exact, available, versioned source bindings.

A mapped taxonomy declaration requires an available captured snapshot with
`taxonomy` purpose. Its `taxonomy_id` must match the snapshot ID or source ID and
its version must match exactly. Categories remain declared mappings; this check
does not establish category fit or clinical validity. Unmapped factors remain
explicitly unmapped.

HEAPS manifest, decision, status and verification objects are admitted through
their detached verification channels. This consumer rejects those objects when
disguised as source, report or supporting artifacts inside the construction
inventory, regardless of the filename extension.
The six detached root filenames are reserved case-insensitively, including
`manifest.json`, `decision.json`, `status.json`, `verification.json` and the two
`verification-input-*.json` captures. This keeps admitted output portable across
case-sensitive and case-insensitive filesystems.

## Interpretation boundaries

Preparation, structural checks, source checks, template mapping, review and
submission are separate observations. The count unit is one canonical
statement. Withdrawn or rejected statements remain in history but do not count
as usable draft items. Empty and all-abstain inputs cannot become a completed
review.

The chronology preserves supplied event, document and availability times and
their unknowns. It does not invent a total order. Deadlines remain unresolved or
specified-unverified; the consumer does not create an authoritative Queensland
deadline or reset a clock after a method change.

Source checking is limited to record/reference integrity and raw artifact
bindings. H4 does not compose accepted D0 byte-span verification, D1 extraction,
D2 chronology or an AcciMap graph. Each optional composition needs its own
HEAPS-specific evidence. The basic packet remains available without them.

The report is an original draft. Current local HEAPS instrument conformity,
actual reviewer authority, clinical review and operational suitability remain
unverified. Action implementation does not establish effectiveness. Creating a
packet never establishes external submission.

See [the frozen H3 contract](../../conductor/tracks/qld-heaps-review_20261116/h3-contract.md)
for normative schema and identity semantics, and
[the implementation plan](../../conductor/tracks/qld-heaps-review_20261116/plan.md)
for the separate H5 qualification and H6 local alignment stages.
