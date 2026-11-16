# H3 — Frozen synthetic profile boundary

Status: implemented H3 contract/fixture checkpoint; see [the H3 receipt](./h3.md)
and [integrated review](./h2-h3-review.md). H3 does not implement H4 assembly or
establish H5 runtime acceptance. The user authorised
H2/H3 implementation; shared registry integration and unrelated owners' work
remain separate.

## Owned objects and interfaces

The schemas are [profile](../../../evaluation/heaps/heaps-profile.schema.json),
[manifest](../../../evaluation/heaps/packet-manifest.schema.json),
[decision](../../../evaluation/heaps/review-decision.schema.json) and
[status receipt](../../../evaluation/heaps/status-receipt.schema.json). Each is
standalone Draft 2020-12 with closed objects and local references only.

The canonical case remains safety-work 1.1. The profile stores process metadata,
mapping and typed references, not another copy of the case. A profile body has
no own hash and no future manifest, decision or status-receipt reference. Its
version is explicit; any material edit requires a new profile revision.

| Profile field | Frozen meaning |
| --- | --- |
| `case_binding` | Exact canonical schema, case ID, record version and evidence-core fingerprint. The consumer requires true positive integer versions, not Boolean or integral-float substitutes. |
| `applicability` | Queensland jurisdiction, purpose/scope, procedure and obligation snapshot IDs, commissioning role and explicit unverified authority/protection. |
| `selection` | HEAPS review process, selecting role and optional decision statement, with analytical tools and their questions separate. |
| `source_snapshots` | Snapshot/source/family IDs, nullable source version and locator, source kind, purposes, applicability, rights, availability and raw-byte digest. Null version/locator is an explicit gap. |
| `source_families` | Canonical source references, lineage family and derivation references. Different source IDs or equal text do not establish independent corroboration. |
| `roles` | Canonical role reference, incident involvement and review responsibilities as separate fields. Involvement does not itself establish competence, conflict resolution or approval authority. |
| `participation` | Role, account/response/disagreement references, needs, confirmation and explicit state rationale/evidence. `pending`, `unknown` and `not_requested` are distinct; silence is not agreement. |
| `chronology` | Statement references with event, document and information-availability time assertions and an ordering note. It does not use canonical workflow events as clinical events. |
| `clocks` / `deadlines` | Awareness, SAC1 reporting and review-submission clocks; separately sourced trigger, calendar, timezone, counting convention and unverified due-date assertions. |
| `factor_assignments` | Typed factor references, multiple categories or explicit unmapped status, taxonomy version and limited declared authority. Factor function stays in the core. |
| `finding_context` | Finding reference, supporting/contrary/alternative references and uncertainty. A syntactically valid finding reference is not an accepted finding. |
| `action_context` | Action/recommendation/finding or condition references plus mechanism, hazard, resources, dependencies, date basis, measures and residual risk absent from the small canonical action shape. |
| `template_mapping` | Original/unavailable/mapped-unverified/stale state, source/version/rights, field references and gaps. There is no official-conformity state. |
| `open_route_questions` | Concurrent death-review, reporting or other route questions with their own unresolved/referral states. HEAPS does not settle another route. |
| `optional_components` | Artifact references and questions only. D0 and AcciMap contracts are not duplicated or implicitly accepted. |

Typed references are exactly `{kind, id}`. `kind` identifies a canonical entity
collection or a statement's actual kind. For example, a `finding` reference must
resolve to a statement whose `kind` is `finding`, and a `reported_account`
reference must resolve to that statement kind. A factor used as an action's
condition is linked through its canonical statement ID; `condition_refs` are
statement references. All references must resolve in the exact bound case and
revision. Profile-local snapshot, deadline and artifact references have their
own typed positions and must resolve too.

The profile's bounds are a deliberately narrow synthetic contract, not a claim
about permissible real-world case size. Empty arrays can be structurally valid;
they do not prove a completed review. Unknown/missing data remain explicit.

## Hash domains and detached construction

| Domain | Exact input and encoding |
| --- | --- |
| `evidence-core-json-utf8-v1` | Admitted canonical record value serialized with sorted object keys, compact separators, `ensure_ascii=False`, UTF-8, no appended newline; SHA-256 with `sha256:` notation. This is the existing `tools.evidence_core.fingerprint` contract. |
| Shared interface source hash | The same admitted value serialized with sorted object keys, compact separators and `ensure_ascii=True`, UTF-8, no appended newline; bare SHA-256 hex. This is `tools.interface_actions.canonical_hash`. It is not the previous digest with a prefix removed. |
| `sha256-raw-bytes-v1` | Exact captured or emitted artifact bytes, without parsing, reformatting or newline normalization; bare SHA-256 hex. The manifest also records exact byte length and safe relative artifact path. |

The manifest binds the exact artifacts it inventories. Its case artifact's raw
digest is distinct from the canonical value fingerprint in `case_binding`.
Object-key reordering or a JSON whitespace change may preserve the canonical
fingerprint while changing raw input bytes. A consumer may produce a normalized
artifact, but must bind and inspect the bytes it actually emits. It must never
claim that unchanged canonical identity proves unchanged raw bytes. Arrays retain
their order; changed canonical array order changes the core fingerprint and
stales every dependent binding even if a particular semantic comparison is
order-insensitive.

Construction is acyclic:

1. Admit the canonical record and profile; capture and identify source,
   calendar, procedure, taxonomy, mapping, template and optional-component bytes.
2. Assemble a report from the fixed input identities. The report may cite those
   identities; it excludes its own digest and any later manifest, decision or
   status-receipt digest.
3. Hash the exact case, profile, sources, mapping, template and report artifacts.
   Put every additional consumed artifact in `supporting_artifacts`.
4. Construct the detached manifest, then hash its exact bytes externally.
5. Store a decision bound to that exact manifest. A later status receipt may bind
   the profile, manifest and decision. Neither object is inserted into earlier
   hashed artifacts.

Manifest component groups are fixed: `case`, `profile`, `sources`,
`supporting_artifacts`, `mapping`, `template`, `reports`. This is a fixed set of
named groups, not a second object-key order; generated object keys use the
serialization rule below. Within each array, paths
are strictly ascending by Unicode code-point comparison; paths and artifact IDs
are unique across the entire inventory. Every consumed input must appear exactly
once in its relevant group. The manifest cannot include itself or a later
decision/status receipt. H4 must enforce ordering, uniqueness, completeness and
byte/digest matching; JSON Schema does not perform those cross-object checks.

Source bytes are never normalized to manufacture a match. Mapping and template
digests identify their actual artifacts, not an inferred official instrument.
Source snapshot versions and family identity survive rendering and revisions.
Supplying changed template or source bytes under an old digest is tampering or
a stale binding and requires `reject_input`; merely labelling a mapping stale
does not admit the mismatched bytes. A legitimate revision requires explicit
new source/template and profile identities, correct raw bindings and a rebuilt
manifest. It may retain unresolved mapping/review status while preparation
continues, but cannot reuse the old packet decision.

### Generated output bytes and captured inputs

H4-generated JSON uses `json.dumps(value, sort_keys=True, indent=2,
ensure_ascii=False, allow_nan=False)`, encoded as UTF-8 without a byte-order mark,
followed by exactly one LF byte. Arrays retain their order and strings receive
no Unicode normalization. This output encoding is different from the compact
canonical fingerprint encoding. H4 reserializes the admitted case and profile
values into the packet's generated JSON artifacts using this convention.

Original consumed ingress bytes are retained separately and inventoried under
`supporting_artifacts`; their raw identity is not replaced by the normalized
case/profile identity. Accordingly, reordered ingress object keys may leave
canonical identity and generated case/profile bytes unchanged while changing
the ingress capture and detached manifest. All consumed calendar, procedure,
taxonomy, mapping and optional-component artifacts remain bound as well.

Generated Markdown uses UTF-8 without a byte-order mark, LF line endings and
exactly one final LF. The generator converts CRLF or bare CR line separators to
LF and replaces only the terminal run of LF bytes with one LF. It performs no
implicit Unicode normalization. Captured source/template bytes remain unchanged;
this generated-output convention does not rewrite them.

Before schema admission, the future consumer must reject malformed UTF-8,
byte-order marks in JSON ingress, duplicate JSON object keys even when the
values agree, nonfinite numeric values and unpaired surrogate string values.
Unknown fields, wrong types and bounds then fail schema admission. No parser
repair, key overwriting or nonfinite-to-null substitution is allowed.

The H3 positive documents are immutable hand-authored structural specimens.
Their captured raw hashes are not claimed to be H4-generated output vectors.
The independent oracle separately pins canonical value, raw ingress and
normalized JSON identities. H4/H5 must verify actual generated report and packet
bytes after the consumer exists.

## Synthetic draft decision and actual authority

The decision scope is exactly `heaps-synthetic-draft-packet`. This is a distinct
HEAPS contract, not an accepted scope of
`tools.interface_actions.validate_approval`. Do not pass it directly to that
shared API or silently map it to `communication`. No shared API is changed.

`approved_synthetic_draft` means the declared synthetic draft review decision
only. `authority_status` remains `unverified` and `substantive_approval` remains
`not_established`. It cannot approve findings, actions, effectiveness, closure,
legal protection, clinical use or external disclosure. A future operational
mapping requires its own authorised scope and qualified interface.

H4 must recompute the manifest's raw digest, resolve author/reviewer roles in the
bound canonical case, reject the same author/reviewer role for draft approval,
require the declared conflict state, and strictly parse and compare
`issued_at <= evaluated_at < expires_at`. The evaluation time is supplied
explicitly; no historical helper default supplies the current clock. The schema
does not authenticate a real person or organisation. Identical role labels do
not prove different people, and distinct role IDs do not establish independence.

Decisions are retained as historical records. A material case/profile/source/
mapping/template/report change creates a new manifest and makes the old decision
inapplicable to the changed packet. The new status receipt records `review=stale`
until a decision for the new manifest exists; do not rewrite the old decision.

## Independent status and transition rules

The receipt records `preparation`, `structural_check`, `source_check`,
`source_check_scope`, `template_mapping`, `review` and `submission` separately.
`clinical_review=not_established`, `actual_authority=unverified` and
`submission=not_submitted` are fixed in v1.

- Preparation can be `not_started`, `prepared`, `empty`, `all_abstain` or
  `failed`. Empty and all-abstain outcomes cannot become a reviewed draft or a
  completed clinical review. The counting unit is one canonical statement in
  the exact bound case. `input_items` is that statement count, not the number of
  profile references or rendered rows. `usable_items` counts statements eligible
  for draft representation in their recorded epistemic kind; it does not count
  accepted clinical facts. Statements with `withdrawn=true` or a
  `provenance.review_state` of `withdrawn` or `rejected` are excluded from usable
  draft items and counted as abstentions, with the reason and history retained.
  Input validation and other
  rule-specific admission conditions still apply. A supplied status receipt is
  not evidence that any item was processed or abstained from. H4 derives counts
  and reasons from inputs and executed checks, verifies
  `usable_items + abstained_items <= input_items`, and requires equality for
  finished preparation dispositions (`prepared`, `empty`, `all_abstain`).
- Structure is `not_checked`, `passed` or `failed`. A pass requires actual
  schema and semantic admission of all consumed objects, not the presence of
  this string or a successful render.
- Source checking has separate result and scope. `record_reference_integrity`
  does not claim exact bytes. `accepted_d0_byte_spans` requires a matching
  accepted D0 contract and verified relevant receipt/input/span bindings.
  Neither proves source truth, causal support or independent corroboration.
  A result cannot advertise a broader scope than the checks actually executed;
  a supplied positive label without matching check evidence is rejected.
- Template mapping has the same four v1 states as the profile. A stale or
  unavailable mapping is never promoted to official conformity.
- Review can be `not_requested`, `pending`, `returned`, `rejected`,
  `synthetic_draft_reviewed` or `stale`. A reviewed draft requires a prepared,
  structurally admitted packet and a matching synthetic-draft decision. Missing
  or mismatched bindings cannot inherit a preceding revision's review.

Status receipts are observations about exact bound revisions. Moving from
unverified/failed/stale to a positive result requires a new observation with
the corresponding evidence. A schema-valid transition label alone proves
nothing. Reject forged positive receipt claims at the H4 consumer. Report
generation, review of a synthetic draft and submission remain different actions.

## Time, calendars and policy applicability

Time assertions retain `known`/`unknown`, day/minute/second precision, basis
references and uncertainty. Regex patterns check lexical form only. H4 must use
a strict parser that rejects impossible dates/times and unsupported zones; it
must not silently coerce dates or supply missing precision. The pattern-only
limit is deliberate and is exercised as a limit in structural tests.

A deadline is `unresolved` or `specified_unverified`; v1 never claims an
authoritative computed deadline. A specified candidate requires a source
snapshot, counting rule, calendar snapshot, timezone, counting convention,
positive offset and known due assertion. The consumer also requires the named
trigger clock to be known and its basis resolvable. The calendar must resolve
to an available snapshot with `calendar` purpose, an explicit version and exact
raw-byte digest. The obligation snapshot must resolve with the relevant purpose,
applicability and source revision. The declared convention must explain trigger
inclusion, non-working days and cutoff treatment where relevant.

Missing source, source version, trigger, calendar, timezone or counting
convention leaves the deadline unresolved. H4 must reject a fabricated
`specified_unverified` assertion whose referenced basis is missing. No business
calendar or statutory trigger is inferred from a generic weekday calculation.
Method changes do not reset awareness or SAC1 reporting clocks. Event-time
standards, current incident-management duties and local targets remain distinct.

## Accepted master and remaining shared limitations

Inspected master is `d11548357baba6a1e20163139a366c6367a05432`. D0 was accepted
through PR #144 (source `29d099b6e8d8507250c360481adba0fef63f91bf`, merge
`d3c10d607470c9a50c5410030b80aeab2cfa5430`), recorded in the
[D0 acceptance receipt](../frontier-assurance_20261113/faw07-d0-acceptance-20261116.md).
D0 remains optional for HEAPS; acceptance of D0 does not qualify a HEAPS
composition. Its input and source versions are distinct from a canonical case
record's version. Its fixed CLI is not a general HEAPS ingestion command.

`inspect_case` raises `ValueError` for malformed input and returns a rejected
case with no admitted spans for well-shaped invalid evidence. A consumer must
preserve both failure channels. D0's public Python seam does not itself prove
synthetic provenance. Every consumed D0 artifact must be bound in the manifest.
The merged lint dependency update changes the lock digest in newly generated D0
receipts; preserve historical receipts and record new execution identities.

The canonical schema, evidence core and interface actions are unchanged from
H1's inspected baseline. The renderer still admits an unknown source, duplicate
ID or invalid transition that canonical validation rejects. The locked
environment still lacks the date-time checker. H4 must apply canonical domain
admission before rendering and an explicit strict time guard or accepted shared
repair. Existing sanitizer restrictions remain in force; a source locator in
metadata is not permission to bypass sanitization in a rendered view.

Recommendation/action enrichment also remains explicit: the shared recommendation
API requires more than canonical `actions[]`, and its evaluation time must be
supplied. H3 does not claim that the profile's fields are already an accepted
lossless mapping to every shared action/effectiveness interface.

## Verification and rollback boundary

H3 verifies that all four schemas are valid, closed and structurally
discriminating against independent examples. The independent fixture lane owns
source bytes, canonical cases, revisions and expected outcomes. Neither the
schemas nor producer helpers generate its semantic oracle.

Structural tests are not HP01–HP25 runtime acceptance. Unknown/cross-case or
wrong-kind targets, stale digests, raw-byte tampering, impossible dates, calendar
resolution, role identity, receipt claims, support/contrary-evidence fidelity,
source-family independence and safe report assembly require the H4/H5 public
consumer and independent execution. Those expectations remain visible in the
fixture catalogue instead of being reported as executed passes.

### Frozen future consumer dispositions

[The independent oracle](../../../tests/fixtures/heaps/oracle.json) freezes 25
acceptance cases with 38 variants: four positive controls and 34 boundary or
adversarial arrangements. Their literal expected preparation dispositions are
22 `prepare_draft`, 14 `reject_input` and two `abstain`; review dispositions are
31 `not_established`, five `stale` and two `withheld`. These are fixture design
denominators, not observed H4/H5 results or test-pass counts.

| Expected field/value | Meaning required of the future consumer |
| --- | --- |
| `preparation_disposition=prepare_draft` | Admit preparation in synthetic scope, retaining all specified conflicts, uncertainty, missingness and prohibited-claim limits. Unresolved content is not silently filled. |
| `preparation_disposition=reject_input` | Reject the invalid binding, structure or boundary with its applicable rule evidence. Do not repair it or emit an apparently accepted packet. |
| `preparation_disposition=abstain` | Retain an explicit empty/all-abstain observation; do not claim a completed draft or review. |
| `review_disposition=not_established` | No substantive or actual approval is established by preparation. |
| `review_disposition=stale` | A prior decision cannot authorise changed bound bytes or revisions. Preserve that historical decision and the stale condition. |
| `review_disposition=withheld` | The specified review/conformity claim is withheld while the otherwise admissible preparation and its unresolved basis may remain. |

These are expected consumer disposition fields, distinct from individual status
receipt enums. They do not rename a receipt's `pending` or `not_requested` state
to `withheld`. The oracle's `required_states`, `retained_ids`, `prohibited_claims`
and `input_identity` fields add exact variant-specific requirements.

The following 34 rule IDs name the frozen semantic obligations. They are stable
fixture identifiers, not a claim that a current CLI returns those error codes:

| Rule family | Exact IDs |
| --- | --- |
| Case and references | `case_binding.case_id`, `case_binding.version`, `case_binding.fingerprint`, `reference.kind`, `reference.unresolved` |
| Evidence and reasoning | `account.conflict`, `recommendation.support`, `factor.promotion`, `source.family_identity`, `documentation.gap_only` |
| Participation and authority | `participation.no_inferred_agreement`, `authority.no_inferred_protection`, `scope.synthetic_draft`, `boundary.synthetic_only` |
| Artifacts and revisions | `artifact.raw_byte_identity`, `packet.approval_stale`, `revision.source`, `revision.template`, `template.conformity_withheld` |
| Time, routes and actions | `deadline.calendar`, `deadline.trigger`, `clock.method_independence`, `action.effectiveness`, `submission.receipt_required`, `route.concurrent`, `component.optional` |
| Completeness and representation | `completion.nonempty`, `canonical.array_identity`, `canonical.content_identity`, `canonical.object_key_order`, `canonical.replay`, `canonical.round_trip`, `schema.closed`, `schema.malformed` |

An H3 test may establish that a specimen has the intended structural validity
or immutable identity. It must not report a future semantic disposition as an
executed pass. Parser failures described above and broader H4/H5 checks remain
explicit requirements even where they are outside this 38-variant denominator.

Rollback reverts only these dedicated schema/contract/test artifacts. No shared
canonical schema, registry, dependency, dispatcher, D0 or AcciMap implementation
is changed. A future incompatible contract uses a new schema version and explicit
migration; existing source records and failed receipts remain intact.
