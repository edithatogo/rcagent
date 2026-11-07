# Cognitive-autopsy planning cross-review: engineering

Reviewer: process-dependencies agent, 2026-11-07. This is a bounded cross-review using existing conversation/repository context, **not fresh-context, blinded or independent-model review**. I authored process-mining.md and did not review that file. Scope: verification-and-reuse.md, work-packages.md, experiment-catalogue.json, integration-contract.md and the corpus cognitive-autopsy-source-contract.md. No repository files were changed by this review.

## Findings

### P2 — Optional work becomes a hard execution dependency

In work-packages.md and experiment-catalogue.json, **CAW22 depends on CAW13**, although the declared starting set excludes CAW13 and the equivalent-framing study is priority 2. Thus the first analysis/paper cannot finish using the stated starting set. **CAW23 also depends on optional CAW06**, so a deliberately omitted compact encoder blocks a fine-tuning decision. Remove these optional prerequisites from the hard DAG, or record explicit conditional study dependencies. Keep the Markdown and JSON synchronized. If framing is intentionally mandatory, include it in the starting set and explain the change in scope.

### P2 — Semantic calibration can start before split freezing

**CAW09 depends only on CAW08**. That permits fitting/calibrating a semantic verifier before **CAW03** freezes development/calibration/test family grouping, despite the separation required by verification-and-reuse.md. Add CAW03 as a hard prerequisite to CAW09 and name the frozen calibration manifest in its inputs. This makes the leakage protection enforceable for a coding agent following the DAG rather than relying on prose elsewhere.

### P2 — Dataset registry references lack a resolvable location

The catalogue's `source_register: "component-datasets.json"` does not resolve relative to evaluation/cognitive-autopsy/; the register lives under conductor/research/cognitive-autopsy/. Use the correct repository-relative/relative path or declare an explicit registry-name resolver and check it. Also replace the corpus contract's `blob/master/.../dataset-citations.md` link with the coordinated branch/commit while the new documents remain unmerged. This avoids a broken cross-repository handoff and ambiguous evidence provenance.

## Checks and positive findings

- Parsed the catalogue: 25 unique package IDs, no dependency cycles and no unknown dependency IDs.
- All five documents consistently describe proposed work and avoid promoting existing adapters into clinical capability.
- Source/derived ownership, immutable originals, local sensitive-data boundaries, offline schemas and bounded repair are explicit.
- Licence compatibility is retained for PM4Py/PROVED; no claim that subprocess isolation removes licence duties.
- SourceRight linkage is correctly distinguished from semantic entailment, and process/scaffold repositories are not presented as validated clinical engines.

No blocking privacy, licence or ownership-boundary defect was found in this bounded scope. Resolve the three execution/provenance findings before handing these leaves to implementation agents. This review did not execute dependencies, inspect patient data, validate clinical rubrics, or establish runtime support.

## Reviewed snapshot

- verification-and-reuse.md SHA-256: b67262bb04d69db6ffef269f308f02ebb489383a92d975f97b17394a1f7c903c
- work-packages.md SHA-256: 1841f9ef08b87510b457171e29b6f6f0a928e13fde62f19701d099d582439386
- experiment-catalogue.json SHA-256: b1c1685ae651f4c5bba9b84cd54d55d02f76d7a3511a8572d743f4160fd7befb
- integration-contract.md SHA-256: dbbc3ea2f2b69e7cca6a031c96064c3ba53a4513be626fb1148e9b9c52cf4a2b
- corpus source contract SHA-256: 88b35b5e6365d2b3c0cd2a821c5538ef4cf3e5dda6447feeb345c39e15d5bf06

## Closure check — engineering acceptance and reproducibility

Existing-context cross-review limitation remains; this is not fresh, blinded or independent-model validation. The three original P2 findings are resolved in the reviewed contracts: CAW22/23 retain optional evidence outside hard prerequisites, CAW09 requires frozen grouping through CAW03, and explicit repository-root registry/primary-source paths resolve. The corpus source-contract and research project-index links use the coordinated branch. Simple availability/risk fixtures are distinct from later mechanism worlds.

Rechecked JSON parsing, 25 package IDs, an acyclic hard DAG, valid optional-evidence IDs, existing register paths and resolvable primary-source JSON pointers. Accept the revised planning contracts within this bounded engineering/reproducibility scope; no runtime or clinical capability was evaluated.

Minor adjacent-index cleanup was reported to the coordinator: two master links in the learningfromharm cognitive-autopsy track index and one in the corpus source-integration track index still need branch reconciliation. No repository edits were made by this reviewer.

Current SHA-256 receipts:

- verification-and-reuse.md: 41a7d8a01b9c94fb475163acfee1c6e96f15e39da27780ec256977e473705fcf
- work-packages.md: 59a2377ed326ea08cea96b8d2d37afae71cb7e38c61d31ce9e0259ba914df582
- experiment-catalogue.json: 589dd68b37327acab6a76f3c1b74b87a9d20ef07e08582eb3237f3921ce3f832
- integration-contract.md: dbbc3ea2f2b69e7cca6a031c96064c3ba53a4513be626fb1148e9b9c52cf4a2b
- corpus source contract: e30d8defe6aa19157950ca9e280db695702c670c8d64b0bf8bc5beb5dc5bf5d5
