# Existing-system fit and gap

## Acquisition ladder and smallest gap

The existing organisational incident system remains the record of reporting and closure. Use the authorised local HEAPS process and template when available. rcagent adds a profile and preparation/validation layer around its existing canonical records; it does not introduce a competing incident-management system.

| Need | Reuse | Remaining project-specific gap |
| --- | --- | --- |
| QLD policy/source applicability | Existing jurisdiction registry and tools/jurisdiction_pack.py | HEAPS source links, local-instrument intake and explicit mapping state |
| Case/evidence/statement integrity | safety-work v1.1 and tools/evidence_core.py | Small profile envelope referencing existing entities |
| Participation and human review | tools/interface_actions.py contracts | HEAPS process-specific references and whole-packet manifest |
| Recommendations/actions/effects | Existing recommendation, action and outcome contracts | HEAPS report mapping and review presentation |
| Portable workflow | Existing four skill modes and death-review profile pattern | Original HEAPS guidance across those modes |
| Template integrity | tools/template_admission.py | An original reviewed draft asset; later authorised local mapping |
| Optional diagram | Active AcciMap #139 | Thin mapping only after its interface is accepted |
| Validation and tests | jsonschema, PyYAML, standard library, pytest and Hypothesis already declared | HEAPS-specific schemas/fixtures/assertions |

No dependency adoption, manifest change or new runtime is required. The declared compatibility baseline is the existing Python >=3.11 project and exact committed dependency lock at the implementation revision; this plan has not executed a new compatibility matrix. Preserve strict typing and quality gates.

## Ownership, replacement and fallback

H3/H4 own only the new HEAPS profile contract and thin adapter after assignment. Shared schema, serialization, source verification, method heuristics, workbench and policy code remain with existing owners. Generic defects go to the owner with a synthetic reproducer; do not fork or copy the component.

The exit path is removal/reversion of the HEAPS adapter and mapping while retaining canonical case records, source history and prior receipts. The safe fallback is an original draft packet and explicit unanswered questions. Missing official-template access withholds conformity claims; missing optional model/graph support removes that feature. A failed reference/hash invariant rejects the affected packet.

## Shared corrections proposed

The generic method matrix's mandatory SAC bundles and indicative timings conflict with its own advisory context. Its London/Yorkshire combination guidance also disagrees across files. The coordinator should make jurisdiction/local process selection primary and keep analytical heuristics source-labelled and advisory. This planning PR does not edit those shared files or the active AcciMap guide.

Current report-view and participation functions deliberately admit generated_synthetic only. Preserve that boundary. A future live pathway is a separately assessed change, not a permissive HEAPS configuration value.

## H1 observed consumption gaps

The [H1 diagnostic](./h1.md) reproduces PR #143's renderer/domain-validation mismatch and an absent date-time checker in the unchanged lock. It also establishes separate Unicode hash domains and the lack of a heaps_packet approval scope. These are concrete interface/qualification inputs, not a reason to fork the core. The coordinator owns generic validator/renderer/dependency repairs and approval-contract changes; H3 freezes explicit bindings and H4 qualifies the actual composition after allocation.
