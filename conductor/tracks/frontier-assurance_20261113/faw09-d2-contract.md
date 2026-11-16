# FAW09 / D2: source-bound partial chronology contract

## Authority, ownership and reuse

On 17 November 2026 (Australia/Brisbane), Dylan instructed this conversation to
implement D2, open a PR, check Actions and merge. The reconciled base is
`6f9cd9627adc52782a67fa6693f1cdb90c3c84a7`, containing accepted D0 and D1.
FAW09 contributes a finite synthetic demonstration to CAW10 / CS03. D3,
Checkpoint B, wider component studies, models and clinical qualification remain
open. The active AcciMap, HEAPS, planning, security and dependency PRs keep their
existing owners.

The integration owner owns `tools/faw09_d2_timeline.py`,
`tools/faw09_d2_clock.py`, the narrow workbench dispatcher,
`tests/test_faw09_d2_timeline.py` and D2 Conductor records. The independent
verifier owns `tests/fixtures/faw09_independent/**` and
`tests/test_faw09_independent_timeline.py`. Two other agents review semantics,
reuse, admission and resources without editing production.

Reuse D0's public `inspect_case`, `json_shapes`, `evidence_core` canonical
serialization/fingerprints, standard-library `datetime` and
`graphlib.TopologicalSorter`, and the existing pytest/Hypothesis environment.
No dependency or global safety-work schema changes are needed. D1's atomic
mentions remain unchanged: lexical co-occurrence does not establish event or
clock linkage. The remaining project-owned gap is a bounded mapping of
explicit synthetic annotations to clock windows and a partial order. A future
qualified linkage adapter can replace those annotations after parity testing.

## Input and admission

`assemble_timeline(case: object)` accepts a case object with these exact keys:
`case_id`, `permitted_view=synthetic-d2-timeline-only`, `sources`, `recipients`,
`events`, `clocks`, `relations`, and `amendments`. Arrays are required even when
empty. The linkage basis is **caller-declared synthetic annotations**, not
automatically extracted or semantically verified event/clock associations.
Changing a declared association changes the binding and replay result.

- Sources use D0's `id`, positive integer `version`, `case_id`, `state=present`,
  nonempty exact `content` and `fingerprint`. At most 32 sources, each at most
  65,536 UTF-8 bytes. Wrong case/digest/version, duplicates, withdrawn or unknown
  sources and malformed data fail with `ValueError` before assembly.
- Identifiers are nonempty UTF-8 strings of at most 128 characters. There are at
  most 16 distinct recipients, 16 events, 32 clocks, 32 relations and 16
  amendments. The total number of event, clock, relation and amendment spans
  is at most 64. Limits are checked before parsing nested rows.
- Each event has `id` and `evidence`. Each clock has `id`, `event_id`, `kind`
  (`event`, `recording`, `availability`), `recipient_id` and `evidence`.
  Availability requires a listed recipient; the other kinds require null.
- Each relation has `id`, `before_event_id`, `after_event_id` and `evidence`.
  It declares strict precedence between known events. Self-relations are
  retained as inconsistent evidence, not silently discarded.
- Each amendment has `id`, `earlier_clock_id`, `later_clock_id` and `evidence`.
  Endpoints must have the same event/kind/recipient and source ID, and the later
  clock must use a strictly higher source version. Amendment evidence must be
  in that later source version. Explicit amendments deactivate earlier clock
  assertions for current ordering, while retaining both originals and the
  amendment. Higher source versions alone never deactivate an assertion.
- Every `evidence` contains `case_id`, `source_id`, `source_version`,
  `source_sha256`, `coordinate_system=utf8-byte`, `start_byte`, `end_byte` and
  `text`. D0 validates exact zero-based, half-open UTF-8 spans. Full-source
  admission witnesses are checked separately and never counted as events.
  Domain IDs are unique within their array; all endpoints are checked before
  graph construction. Unknown fields fail rather than disappear.

Events carry the original assertion text and provenance. Actor, subject and
assertion polarity are explicitly uninterpreted; neither a negated mention nor
an event annotation is promoted to proof that an action occurred. Recording
and availability clocks are independently supported annotations. Availability
does not prove that a recipient read or understood information. Every listed
recipient has an explicit summary for every event, including missing values.

## Clock grammar and uncertainty

Only the selected clock span is parsed. It is at most 512 UTF-8 bytes. The
fixed grammar supports full ISO dates and date-times with minute or second
precision, `T` or one space between date and time, and an optional `Z` or
`+/-HH:MM` offset. Explicit offsets are bounded to 14 hours. The special
`-00:00` offset remains unknown. No host timezone, file time, incidental
timezone database or default anchor is used.

A date is a possible-time window from `00:00:00` through `23:59:59`; a minute
from second `00` through `59`; a second denotes that reported second. This is
a discrete one-second representation with inclusive endpoints, not a claim
about physical subsecond precision. Windows describe uncertainty about a
single occurrence, not the duration of an activity. Date-only expressions
without offsets remain local windows with unknown absolute time.

`A to B` gives one uncertainty window using A's lower and B's upper bound.
Reversed windows are invalid. Endpoints must both resolve to UTC or share the
same unresolved literal timezone. Up to four alternatives separated by ` or `
retain distinct windows. Every alternative must be valid before UTC comparison
is available; a malformed or unresolved alternative cannot be dropped.

Missing offsets retain local values with `timezone_unknown`. Named IANA zones
retain local values with `named_timezone_unresolved`; this baseline deliberately
does not consult host `zoneinfo` data. Thus a DST fold or gap written with only
a named zone stays unresolved, without choosing a fold or rolling a gap
forward. Explicit offset alternatives can represent a fold. This is not a
named-zone validity classifier. A future named-zone adapter must pin its data
and prove fold/gap parity before adoption. Calendar/offset/UTC overflow remains
invalid. Unsupported formats, fractional seconds, relative or bare clock
expressions remain visible as unsupported; there is no fuzzy parsing or
invented anchor. The literal `unknown` records an explicit unknown clock.

Clock interpretations retain `status`, `reason`, and `windows`, each with
`local_start`, `local_end`, `utc_start`, `utc_end`, `precision` and `timezone`.
UTC values are canonical second-resolution strings ending in `Z`, or null.
Precision is `day`, `minute`, `second` or `range`. Status is `resolved`,
`ambiguous`, `unknown`, `invalid` or `unsupported`.

## Clock summaries and partial order

Each event has `event_time`, `recording_time` and recipient-specific
`availability`. A summary lists all and active clock assertion IDs, its status,
reasons, disagreement and UTC `windows` (`start`, `end`) or null. Missing
assertions have status `unknown`, reason `no_assertion` and null windows.
Any unresolved active assertion makes the summary `unresolved` with null
windows; known assertions remain inspectable in the assertion list. Distinct
resolved active accounts are alternatives, never averaged or selected by file
order. Their disagreement remains explicit. Summary status otherwise is
`known`, `ambiguous` or `conflicting`.

Only event-time summaries supply interval-derived edges. A is definitely
before B when the latest possible A is strictly earlier than the earliest
possible B. Overlapping or touching windows preserve unknown order. Two point
windows at the same reported second are labelled `same_reported_time`, which
does not prove physical simultaneity. Recording and recipient clocks never
substitute for event time, and no universal event/recording/availability
inequality is assumed.

The result preserves asserted and interval-derived edges separately and emits
all unordered event-ID pairs in a canonical pair table. `interval_relation`
is `before`, `after`, `same_reported_time`, `overlap_or_touch` or `unknown`.
`order` is `before`, `after`, `same_reported_time`, `unknown` or `inconsistent`;
`basis` distinguishes asserted, interval and transitive support. Evaluation
scores the full transitive closure of asserted and interval-derived edges,
not just directly supplied edges. The feasibility check does not claim to
discover additional relations obtainable by pruning time alternatives.

Validate graph endpoints before `TopologicalSorter`; never accept its implicit
creation of unknown nodes. Detect cycles without dropping their evidence.
For an acyclic graph, test the feasibility of strict one-second precedence
against the union of admitted windows by propagating earliest feasible bounds.
Unknown clocks are unbounded. This internal check must not publish a chosen
point time as an observation. An infeasible graph has no accepted display
order. All pairs have `order=inconsistent` when the case is inconsistent;
their original interval relations remain visible for diagnosis.

`consistency` reports status, all cyclic event IDs and infeasible event IDs.
`display_order` is one deterministic topological presentation, or null for an
inconsistent case. It never proves additional ordering or simultaneity.
No total-order enumeration is performed. Source/event/clock array permutations
preserve the canonical case result. Source revisions, amendments and binding
changes remain visible and cannot reuse a stale replay result.

## Public result, receipt and delivery

The case result has schema version `faw09-d2-case-1.0`, case/view/linkage/rule
identity, sorted D0 source summaries, sorted recipients/events/clock assertions,
relations/amendments, edges/pairs, consistency, display order, event count and
`display_order_is_temporal_evidence=false`. Each event, clock, relation and
amendment has a content-bound `binding_id`. Event assertion fields are `text`,
`actor=null`, `subject=null`, `polarity=not_interpreted`. Clock assertions carry
their interpretation, `active` flag and `superseded_by` clock IDs. All asserted
and derived output retains its source-bound input rather than replacing it.

`verify_timeline(case, result)` checks canonical deterministic replay equality.
It is not an independent semantic oracle. Malformed/cyclic/unencodable result
objects return false; invalid cases may raise `ValueError`.
`uv run --no-sync python -m tools.workbench d2-demo` and
`python -m tools.faw09_d2_timeline` emit the same fixed synthetic inputs and
outputs as canonical UTF-8 JSON plus one LF. The CLI accepts no external input,
URL or model. The receipt binds input/output, view/schema/rule/generator,
implementation and lock hashes, counts and limitations. The producer contains
no expected labels or precision claims. Two clean processes must agree at
identical code/lock versions. Runtime measurements are recorded separately.

Freeze independent literal expectations before running production. Include
useful positive controls and adverse controls for shuffled order, all three
clocks, recipients, unknown availability, explicit offsets, DST uncertainty,
equal/coarse/overlapping windows, conflicting accounts, cycles, infeasible
precedence, amendments, withdrawal, Unicode and provenance/resource limits.
Report event/clock retention, normalization/unresolved counts, strict-order
TP/FP/FN, precision/recall, unknown/conflict preservation, false blocking and
execution failures with exact denominators. All-unknown cannot pass useful
positive controls. Visible development fixtures are not a held-out assessment.

Require unchanged strict gates, zero typing allowances, independent agent
review, all nine exact-head Quality jobs, dependency/privacy checks, normal
protected merge and observed automatic master conformance. Keep failures and
unavailable local socket tests distinct from hosted results. Queued offline
security is not a completed scan. Mark FAW09 accepted only after observed
delivery. Preserve all historical D0/D1 receipts and other owners' work.

## Standard-library references

- [Python datetime](https://docs.python.org/3/library/datetime.html): bounded
  calendar arithmetic and explicit-offset conversion.
- [Python graphlib](https://docs.python.org/3/library/graphlib.html): cycle
  detection and topological presentation; endpoint validation remains local.
- [Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html): explains
  host/database dependence; named-zone conversion is outside this baseline.
