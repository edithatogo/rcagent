# Decision: Portable Skill Licence

- **Decision ID:** 20260731-001-skill-licence
- **Status:** Accepted
- **Date raised:** 2026-07-31
- **Owner:** Repository owner
- **Track:** agent-skills-living-conformance_20260731
- **GitHub issue:** https://github.com/edithatogo/rcagent/issues/5
- **Decision needed by:** Before Track 00 completion or external distribution

## Decision Needed

Select the licence for the portable RCA investigation skill and associated
project code. The Agent Skills `license` field is optional, but this project's
approved specification requires an owner-approved declaration before Track 00
can complete or distribution work can claim readiness.

## Recommendation

**Recommend: Apache-2.0**

Apache-2.0 supports broad reuse and registry distribution, includes an express
patent grant and contribution terms, is widely understood by software and AI
tooling ecosystems, and matches the licence used by the upstream Agent Skills
reference validator. It does not imply clinical validation, warranty, or
fitness; those limitations remain explicit in product documentation.

## Options

| Option | Benefits | Risks and trade-offs | Reversibility | Cost and effort | Dependency impact |
|---|---|---|---|---|---|
| Apache-2.0 (recommended) | Permissive reuse, patent grant, mature ecosystem support | Requires preserving notices; does not prevent unsafe downstream use | Future versions can change, but existing releases retain their licence | Low | Unblocks Track 00 and later registry preparation |
| MIT | Very short and broadly compatible | No express patent grant; less explicit contribution protection | Same prospective-only limitation | Low | Unblocks Track 00 but provides a thinner legal framework |
| Proprietary / all rights reserved | Maximum distribution control | Conflicts with broad community reuse and many registry expectations; requires bespoke terms | Can later open future versions | High legal and maintenance effort | Delays distribution and contribution workflows |
| Defer licence | Avoids a premature legal choice | No external distribution or licence-readiness claim; Track 00 remains incomplete | Fully reversible | No immediate effort | Blocks Track 00 completion and downstream distribution |

## Evidence and Assumptions

- Agent Skills permits a short licence name or bundled licence-file reference.
- The upstream `skills-ref` code is Apache-2.0.
- The roadmap intends later submission to skills and client-plugin registries.
- Assumption: the owner controls the copyright in the repository content or
  will resolve contributions and third-party material before release.

## Privacy, Safety, Legal, and Maintenance Impact

Licence selection does not authorise release, disclose private data, or prove
clinical suitability. Third-party policies, templates, terminology, and other
materials still require rights review. The skill retains explicit no-warranty,
human-authority, privacy, and clinical-safety boundaries regardless of licence.

## Safe Default if Deferred

Keep the `license` field absent, make no distribution or reuse claim, and leave
Track 00 incomplete.

## Execution Impact

- **Paused scope:** Licence file, frontmatter declaration, final Track 00
  completion, and downstream distribution readiness.
- **Work continuing autonomously:** Hosted CI reconciliation and preparation
  of the remaining evaluation and clinical-review decisions.
- **Schedule and dependency effect:** Track 01 and Track 11 remain formally
  blocked until Track 00 acceptance passes.
- **Wake condition:** Owner selects Apache-2.0, MIT, proprietary terms, defer,
  or another specified licence.

## Response Requested

Select exactly one licence option.

## Owner Decision

- **Decision:** Apache-2.0
- **Conditions:** Licence selection does not authorise a release, registry submission, distribution of third-party material, or any clinical-validity claim.
- **Date:** 2026-08-29
- **Recorded by:** Repository owner, recorded by Codex from explicit task instruction

## Follow-up

- [x] Update affected specifications, plans, metadata, risks, ADRs, tests, and receipts
- [x] Reconcile GitHub labels and dependencies
