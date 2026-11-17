# Decision models: specification and qualification plan

Status: **track in progress; DM01 merged (#147), DM02 opt-in model-free contracts under verification (#153)**. The 17 November 2026 instructions authorise both named increments and their own checked merges. Decision-model execution, shared registry admission and DM03–DM11 remain pending.

- [Specification](./spec.md)
- [Proposed interface contracts](./contracts.md)
- [Implementation and verification plan](./plan.md)
- [Metadata](./metadata.json)
- [Primary-source register](./sources.md)
- [Planning evidence and integration handoff](./planning-evidence.md)
- [DM01 bounded context and receiving map](./dm01/context-pack.md)
- [DM01 source-admission receipt](./dm01/source-admission.md) and [candidate manifest](./dm01/candidate-admission.json)
- [DM01 frozen study protocol](./dm01/study-protocol.md) and [machine-readable protocol](./dm01/study-protocol.json)
- [DM01 decisions](./dm01/decisions.md) and [verification receipt](./dm01/verification.md)
- [DM02 source/port mapping and rollback](./dm02/contract-mapping.md), [JSON Schema](../../schemas/decision-models-0.1.schema.json), [Python boundary](../../../tools/decision_model_contracts.py) and [synthetic matrix](../../../tests/test_decision_model_contract_matrix.py)

Repository baseline: `edithatogo/rcagent` at `37ca41fa2e7eeee8cc79e24efd5d7c0f915269f3`.
The request's `edithagoto/recagent` returned 404; the accessible repository and the existing project context identify `edithatogo/rcagent`.

Track 12 retains scientific ownership; Track 13 retains shared assurance and integration; Track 14 retains death-review applicability. AcciMap #141 and HEAPS #142 retain their current owners. The existing coordinator, `6af6164f-cf84-8321-9f96-8b7d685aabe5`, retains shared-contract acceptance. DM01 merged through [PR #147](https://github.com/edithatogo/rcagent/pull/147); DM02's bounded standalone PR is [#153](https://github.com/edithatogo/rcagent/pull/153). The shared-interface receiving proposal is [issue #125](https://github.com/edithatogo/rcagent/issues/125#issuecomment-6943868352); no production mapping acceptance is claimed. Neither increment transfers unrelated implementation ownership. The stable track ID is sufficient; portfolio numbering and machine-readable roadmap registration remain for coordinator reconciliation.
