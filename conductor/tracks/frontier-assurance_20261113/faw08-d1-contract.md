# FAW08 / D1 bounded extraction contract

Contract: `faw08-d1-contract-1.0`. This is the implementation and verification
contract, not an acceptance receipt. On 16 November 2026 Dylan explicitly
instructed this conversation: **"Implement D1, open a PR, check actions pass,
then merge."** This authorises this bounded increment and its protected merge.
The earlier D0-only restriction is superseded for D1; other owners and D2–D8
remain separate. Base: `d11548357baba6a1e20163139a366c6367a05432`, including the
already merged D0 delivery and the subsequently accepted ty/lock update.

## Scope, ownership and reuse

FAW08 contributes to CAW02/04/08. It demonstrates deterministic lexical
observations over at least twelve independently specified synthetic families:
numeric dates, missing year, midnight, locale ambiguity, ranges, units,
negation, attribution, relative time, conflicting notes, OCR corruption and
no supported observation. It does not complete those scientific work packages,
Checkpoint B, a general clinical NLP baseline, chronology or decision-time
entitlement. Model and clinical qualification remain zero.

The completion owner owns `tools/faw08_d1_extraction.py`, its narrow
`tools/workbench.py` dispatcher, `tests/test_faw08_d1_extraction.py` and the D1
Conductor records. The independent verifier owns only
`tests/fixtures/faw08_independent/**` and
`tests/test_faw08_independent_extraction.py`. Two other existing agents review
the contract, source, reuse and delivery read-only. This does not create another
external worker chat or transfer the AcciMap, HEAPS, broader planning, security
or dependency-update PRs. No active D1 PR or conflicting owner was present in
the initial live reconciliation.

Reuse `evidence_core.canonical_bytes/fingerprint`, checked `json_shapes`, D0's
public `inspect_case`, Python `re`, `datetime` and `Decimal`, and existing
pytest/Hypothesis. The remaining project-owned gap is this bounded extraction
grammar and its source-bound admission rules. No new dependency, generic NLP
engine, canonical safety-work schema, model, private data or network ingestion
is needed. `python-dateutil` is only transitive in the lock and is not adopted
as an implicit runtime dependency. A later admitted NLP adapter may replace
these rules after parity against independent fixtures; FAW11 owns comparison.

## Public boundaries and admission

`extract_case(case: object)` returns a versioned D1 case observation.
`verify_extraction(case, result)` checks canonical equality with deterministic
re-execution. That is a replay-consistency check, not an independent semantic
judge; independent labels and calculations remain in the verifier lane.

The case contains nonempty `case_id`, exact
`permitted_view=synthetic-d1-extraction-only`, `sources`, optional `date_order`
(`unknown`, `DMY` or `MDY`, default `unknown`) and optional `anchors` (default
empty). Source fields retain D0 names and meanings: `id`, positive integer
`version`, `case_id`, `state=present`, nonempty exact `content` and declared
`fingerprint`. Identifiers are at most 128 characters, sources at most 32, and
each source at most 65,536 UTF-8 bytes. Booleans are not versions. Unknown or
withdrawn sources, forged bindings, wrong case, duplicates, malformed input,
wrong view and exceeded limits fail with `ValueError` before extraction.

Actual full-source spans are checked through D0 before extraction. These are
**source-admission witnesses**, not extracted observations, and are excluded
from extraction counts and metrics. Therefore a nonempty administrative source
can be admitted while yielding zero observations. Empty extraction says only
that the supported grammar found no observation; it does not establish absence
of an incident, clinical action or omitted care.

An optional anchor has the D0 evidence fields `case_id`, `source_id`,
`source_version`, `source_sha256`, `coordinate_system=utf8-byte`, `start_byte`,
`end_byte` and `text`. The caller explicitly selects at most one anchor per
source/version. It must resolve to an exact, valid local ISO date-time
`YYYY-MM-DD HH:MM[:SS]` or its `T` form in that same admitted source. It does not
declare recording or recipient-availability time. Missing, conflicting,
malformed, cross-source or forged anchors cannot silently become defaults.
No source's first timestamp, system clock or file order is an implicit anchor.
Anchor arrays are limited to 32 entries before any row parsing. Relative
integers are unsigned and at most six digits; longer matching expressions stay
visible with `unsupported/relative_offset_limit`. Calendar arithmetic overflow
stays visible with `invalid/relative_time_out_of_range`.

## Bounded grammar and interpretation

Patterns are fixed, source text is bounded before matching, and original text
is never normalised or OCR-corrected. Longer range/relative expressions take
precedence over contained scalar matches. Malformed date/time/number tokens
must not produce a valid-looking suffix.

| Kind | Supported form and result | Uncertainty or failure |
| --- | --- | --- |
| Date | ISO `YYYY-MM-DD`; numeric `D/M/YYYY` or `M/D/YYYY`; English `D Month [YYYY]` | Calendar validation; unknown numeric order retains alternatives; absent year remains null |
| Date range | Two full ISO dates joined by `to`, an en dash or spaced hyphen | Preserve endpoints; reversed range invalid; no midpoint |
| Clock | 24-hour `H:MM[:SS]`, including `00:00` | `24:00`, impossible minutes/seconds invalid; no date or timezone inferred |
| Clock range | Two supported clocks joined by hyphen, en dash or `to` | Preserve endpoints; an end before its start needs an explicit date/rollover and remains ambiguous |
| Quantity | Signed decimal and a unit; decimal range with one trailing unit | Exact decimal strings; no unit conversion, dose inference or denominator substitution; unknown unit/number format remains visible |
| Relative time | Integer minutes/hours/days `later` or `earlier`; `yesterday`, `today`, `tomorrow` | Preserve offset when unanchored; resolve only against the explicitly selected same-source anchor; day words give a date, not an invented clock time |
| Assertion | Bounded mentions of `pain`, `fever`, `cough`, `rash`, `nausea`, `dizziness` | Preserve supported immediate positive/negative cues; unsupported or hypothetical scope remains uncertain |

Units initially admitted as literal spellings are `mg`, `g`, `mcg`, `µg`, `μg`,
`kg`, `mL`, `L`, `mL/h`, `mg/kg`, `mg/kg/h`, `mmol/L`, `bpm`, `mmHg`, `%` and
`°C`. Their spelling is preserved, not converted. Decimal tokens have at most
32 characters; scientific notation and comma forms are retained as unsupported
or ambiguous rather than partially parsed. Quantities are mentions, not proof
that a treatment was administered.

Context is the source clause bounded by a sentence, semicolon, newline or
explicit `but`/`however` boundary; decimal points are not sentence boundaries.
Supported immediate cues include `received`, `was`, `is`, `has`, `had`,
`given`, `administered`, `reports`, `denies`, `denied`, `no`, `not received`,
`did not receive`, `not given`, `not administered` and `does not have`.
Unsupported compound negation, `not only`, conditional or hypothetical cues
produce uncertain polarity. Cues and attribution never carry across clauses.

Supported explicit entities are synthetic bracketed roles (`[Patient A]`,
`[Consumer B]`, `[Clinician A]`, `[RN B]`) and the literal role words `patient`,
`child`, `mother`, `father`, `nurse`, `clinician`. A direct subject followed by
the supported predicate supplies the subject; `reporter reports [that] subject
predicate` distinguishes reporter from subject. Missing or complex attribution
remains unknown. Recognised words alone do not justify an inferred experiencer.

Date, clock, quantity and relative mentions remain separate observations.
Their co-occurrence does not assemble an event or timeline. Conflicting sources
and source revisions remain separate; no winner or independent corroboration
is inferred. Recording time, availability time, timezone and event linkage
remain explicitly unknown unless a field's declared grammar directly supplies
its local lexical value. D2/D3 own subsequent clock and entitlement work.

## Output and deterministic receipt

Each observation includes a stable content-bound ID, case/source/version/hash,
exact UTF-8 half-open span and raw text, kind, lexical interpretation status
(`resolved`, `partial`, `ambiguous`, `invalid`, `unsupported`), normalised fields
where supported, a specific reason where unresolved, polarity, subject,
reporter, exact clause context, any explicitly selected anchor, method/rule
version and the permitted view. Unknown fields survive JSON round trips.
Normalised numeric values are decimal strings, never binary floats.

The concrete case result fields are `schema_version=faw08-d1-case-1.0`,
`case_id`, `permitted_view`, `date_order`, `source_admission` (the explicit
non-observation witness label), D0-style `sources`, `observations`,
`observation_count` and `no_supported_observation`. Observation fields are
`observation_id`, `case_id`, `source_id`, `source_version`, `source_sha256`,
`coordinate_system`, `start_byte`, `end_byte`, `text`, `kind`, `status`,
`normalized`, `reason`, `polarity`, `subject`, `reporter`, `context` (a verified
span object), `anchor` (a verified span object or null), `timezone`,
`recording_time`, `availability_time`, `event_linkage`, `context_reasons`,
`method` and `rule_version`. The four clock/linkage fields are null in this
increment. Polarity is `affirmed`, `negated`, `uncertain` or `unknown`.
Kind values are `date`, `date_range`, `time`, `time_range`, `quantity`,
`quantity_range`, `relative_time` and `assertion`. `observation_count` counts
every retained candidate, including unresolved statuses;
`no_supported_observation` is exactly `len(observations) == 0`. Span/kind
precision and recall include those candidates; resolved useful output and
normalisation coverage are reported separately. Thus an invalid expression
does not become a no-event control. Assertion lexical recognition can be
resolved while polarity remains uncertain or unknown. Unsupported assertion
scope is recorded in `context_reasons`, not hidden by numeric normalisation.
Context excludes surrounding whitespace and terminal clause punctuation.
Only relative observations carry a selected anchor. IDs bind full case/source
identity, version, digest, span and kind. Malformed, cyclic or unencodable
replay-result objects return false rather than escaping serialization errors.

Normalised values use these shapes: date `{year, month, day, iso, alternatives}`
(a missing or undecided value is null); clock `{time, precision}`; date/clock
range `{start, end}`; quantity `{value, unit}`; quantity range
`{lower, upper, unit}`; assertion `{observation}`; integer relative expression
`{offset_seconds, local_datetime}`; day word `{offset_days, date}`. A wholly
invalid or unsupported expression has `normalized=null`; an explicitly partial
expression retains its supported fields. Date alternatives are sorted ISO
strings, or empty when there is no date-order ambiguity.

At most 32 observations per case are returned. Overflow raises `ValueError`;
there is no silent prefix or truncation. Both observation and context spans
are verified through D0. Source ordering cannot choose the surviving account.
Observation IDs depend on source content/version and span, not source-array
position; receipt input fingerprints still expose changed ordering/bytes.

`uv run --no-sync python -m tools.workbench d1-demo` and
`python -m tools.faw08_d1_extraction` emit the same fixed synthetic demonstration
as canonical UTF-8 JSON plus one LF. No input path, URL or model is accepted.
The producer contains no expected labels or precision claims. The receipt
records inspectable inputs/outputs, input/rule/generator/view versions,
input/output fingerprints, actual lock/implementation hashes, counts and
limitations. Two clean processes must agree at identical source/lock versions.
Runtime and resource observations belong in a separately dated execution
receipt. CLI argument, receipt-read and output-write failures are nonzero.

## Independent verification and acceptance

Freeze literal source texts, expected spans, statuses, values, polarity and
attribution independently before running production. Include all twelve
semantic families, with positive/adverse controls and at least 24 development
cases overall. Missing observations remain in the denominator. These visible
development fixtures are not a held-out or clinical population assessment.

Report exact span/kind TP/FP/FN, precision/recall, field errors, correct resolved
output and useful coverage, ambiguity recognition, false blocking, no-event
false positives and execution failures. Undefined ratios are null. Correct
abstention must not inflate normalisation recall. Test every expected field
and retain failures/revisions as an attempt history. All-abstention cannot pass.

Challenge forged case/source/version/digest/view, duplicate identities,
unknown/withdrawn sources, malformed containers/types, UTF-8 and resource bounds,
candidate overflow and one-field output tampering. Use independent Unicode,
source-order, repeatability, anchor-removal, number/polarity/attribution changes
and conflicting-source probes. Keep injected corruption results separate from
natural extraction errors. Replayed equality is not an independent oracle.

Require the unchanged strict engineering suite and zero typing allowances,
three-role agent review, all nine exact-head Quality jobs, dependency review,
privacy/secrets and normal protected merge. Preserve existing conformance path
filters: if the PR run is not triggered, execute the pinned validator locally
and inspect automatic master conformance after merge. Queued offline security
is not a completed scan. Record actual source/check/merge identities before
claiming delivery. Keep FAW08 in progress until acceptance has direct evidence.

Historical D0 receipts remain bound to their original source and lock. New
workbench or lock bytes legitimately change a newly generated D0 artifact;
regression tests preserve D0 behaviour rather than demand its old whole-output
hash. A normal revert of the D1 increment preserves D0, prior studies and other
owner work. D2–D8, broader CAW closure, models and clinical claims stay pending.
