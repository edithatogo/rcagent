# HEAPS synthetic contract fixtures

This directory contains the H3 contract for a generated-synthetic Queensland
HEAPS preparation profile: four standalone Draft 2020-12 JSON Schemas. The H4
consumer is implemented separately in `tools/heaps.py`; its public interface and
limits are described in [the usage guide](./h4-usage.md). These are original
engineering artifacts, not an official Queensland Health form.

| File | Object and boundary |
| --- | --- |
| `heaps-profile.schema.json` | Process metadata and typed references to a separate safety-work 1.1 case. No embedded case, own digest or future manifest, decision or status receipt. |
| `packet-manifest.schema.json` | Detached inventory binding the exact bytes of the case, profile, sources, mapping, template, reports and all supporting inputs consumed. Its own digest is external. |
| `review-decision.schema.json` | A detached decision about a synthetic draft packet. Its distinct scope is not an accepted scope of the shared approval API and establishes no substantive or actual authority. |
| `status-receipt.schema.json` | Separate preparation, structure, source-check scope, template mapping, review and submission observations. Empty and all-abstain preparation remain explicit. |

The normative semantics, encoding domains, state transitions and H4 obligations
are in [the H3 contract](../../conductor/tracks/qld-heaps-review_20261116/h3-contract.md).
The independent fixture author owns [tests/fixtures/heaps](../../tests/fixtures/heaps/).
Structural checks live in [test_heaps_profile_contract.py](../../tests/test_heaps_profile_contract.py).
Schema examples and fixture-design checks do not qualify an H4 consumer or H5
composed behaviour. H4 implementation observations are recorded separately from
the immutable H3 design oracle.

## What these schemas check

All objects are closed. The schemas check required fields, enum values, local
reference kinds, lexical identifier and digest shapes, finite collection bounds
and several explicit within-object conditions. Canonical references use
`{kind, id}`. A statement kind such as `reported_account`, `finding` or
`recommendation` distinguishes its meaning without creating another statement
collection. Chronology references statements; canonical workflow events do not
become clinical timeline entries.

The schemas intentionally do not claim cross-record integrity, actual content
hash verification, genuine reviewer authority, strict date parsing, calendar
calculation, causal support or template conformity. A reference with a valid
identifier shape can still point to the wrong case or entity. A digest with the
right shape can still be false. A timestamp matching the pattern can still be
an impossible date. The H4 consumer must reject those conditions at the
appropriate boundary. JSON Schema `integer` also admits integral JSON numbers;
the consumer must apply the exact integer-type rule to versions and offsets.

## Data and authority limits

Every object declares generated-synthetic data and fully local handling. Those
declarations do not themselves prove the input's origin. H4 must enforce the
synthetic input boundary. Actual authority remains unverified, substantive
approval is not established, external submission is `not_submitted` and clinical
review is `not_established`.

Template mapping states are `original`, `unavailable`, `mapped_unverified` and
`stale`. There is no official-conformity state in this version. Current local
instrument access, rights and field-level conformity remain H6 work. Public
policy metadata may be referenced without making an invented synthetic rule an
actual Queensland obligation.

## Optional accepted components

Accepted D0 may later supply exact source/span evidence. The profile stores only
an optional component artifact reference; it does not reproduce D0's input or
receipt schema. AcciMap is likewise optional and requires its separately accepted
interface. Every consumed optional artifact belongs in the detached manifest's
`supporting_artifacts` group. A profile reference alone does not admit the
component's result.

The shared canonical schema and helpers remain unchanged. H1's renderer/domain
validation mismatch and absent date-time checker remain current at the H4 base
`6f9cd9627adc52782a67fa6693f1cdb90c3c84a7`. The H4 consumer applies canonical
domain admission and strict time parsing at its own boundary. This does not
repair or qualify other callers of the shared renderer.
