# Review and repair record

Date: 16 November 2026. Reviews below are agent implementation/method reviews
and generated-case exercises. They are not independent human, clinical or
organisational acceptance.

## Method and fresh workflow trial

Primary-source checking distinguished the original Rasmussen/Svedung hierarchy
from rcagent's six-level healthcare adaptation and the separately published
five-level healthcare facilitation guide. The Branford chapter year was corrected
to 2009 using its institutional publication record; full chapter download was
unavailable. The guide identifies that access limit and does not reproduce the
third-party chapter or templates.

A fresh agent received the guide and literal synthetic fixture without the
expected topology file or the implementation conversation. Its facilitator
handoff retained the unreviewed map, candidate factors, contested/hypothetical
links, missing chronology, proposed-action status and unanswered placement
questions. It distinguished metadata timestamps from incident chronology and
did not treat empty upper levels as proof that upstream influences were absent.
This was one qualitative exercise, not a scored benchmark or inter-rater study.

The exercise found that the policy evidence mentioned an omitted backup owner
while a graph rationale additionally asserted an absent fallback route. The
invented policy evidence/statement was made explicit about both omissions.
Source/evidence hashes and the exact-record binding were recomputed; expected
topology and acceptance labels were unchanged. No historical or real evidence
was edited.

## Independent code findings and resolution

Initial reviewed module SHA-256:
`7854bbd7f0aefa401930b6afd683dfceaea0a0768575e4a6b002a294b9f5c347`.

| Finding | Independent reproduction | Repair and recheck |
|---|---|---|
| Legacy 1.0 admission bypassed the companion's 1.1 provenance contract | A 1.0 record with an absent external statement source validated and rendered | Explicitly require 1.1 before companion semantics; both 1.0 variants now reject and cannot render; shared legacy validation unchanged |
| Recommendation uncertainty disappeared from the standalone diagram | A distinctive warning about proposed routing was absent from labels and findings | Preserve the original uncertainty in both; independent reproduction and new regression pass |
| Excluded statement-source provenance was silently admitted | Excluding the disconnected context statement's source still admitted the node | Reject excluded provenance sources for represented nodes and recommendations, independently of edge evidence; both isolated cases now reject |

The follow-up also checked a missing provenance source under 1.1, stale declared
review identity and repeated rendering. No unexpected missing-source exception
occurred; changed graphs invalidated review identity and repeated inputs produced
identical source bytes.

The implementation additionally displays canonical case state, statement source
and review state, and linked action status/effectiveness. An adverse recorded
effectiveness state produces a review finding. A withdrawn whole case remains
available for historical synthetic inspection with its state visible, while
excluded sources and rejected/withdrawn represented statements, factors and
evidence remain inadmissible. The contract documents this distinction.

Rechecked module SHA-256:
`a5be10ced6b4148d1d1221f7c834113ff9621ddf0a2f18285bb306018068d127`.
Schema SHA-256 remained
`300e3137d2f92a34b0502f40af16817c76ee6eecc6c1e51983136d6b7dedf511`.
The independent reviewer reported all three findings resolved at those bytes.

## Failed observations retained

- Initial focused run: 62 passed, four failed assertions. The schema rejected an
  unknown level earlier than the test expected; two target-reference diagnostics
  used singular names; `flowchart TB` was a valid synonym for the expected `TD`.
  Assertions were corrected to precise diagnostics and both documented direction
  spellings without changing acceptance semantics. The subsequent shared run
  passed 274 tests.
- During repair, a presentation test changed case state without changing the
  final event and used a nonexistent statement review state. The canonical
  validator correctly rejected it. The test now uses a consistent withdrawn
  event and the existing `unreviewed` vocabulary.
- A concurrent broad implementation-agent run observed a Hypothesis deadline
  flake: 314.61 ms initially versus 131.70 ms on replay at the default 200 ms
  deadline. There was no failing topology assertion. No health check or deadline
  was suppressed. Root's subsequent focused run passed all 72 tests; the full
  gate outcome is recorded separately.
- The first full-gate attempt found one unescaped regex in a new regression.
  It was corrected to the literal `1.1` diagnostic.
- A second attempt scanned third-party packages in the nonstandard
  `.venv-py312` directory and found their intentional test/text characters. The
  environment was moved to the repository's standard `.venv` location, already
  excluded by its scanner. No scanner rule, baseline or quality allowance changed.

See [verification.md](./verification.md) for the final tested identities and
actual gate/parser/render outcomes. Do not infer a hosted, client-rendering or
operational pass from these bounded source reviews.
