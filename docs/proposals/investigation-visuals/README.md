# Synthetic investigation-diagram proposal illustrations

This directory contains **design references**, not compiled Mermaid diagram types, clinical evidence, clinical recommendations, accepted causal models, or an operational rcagent capability. The ten SVGs are illustrative diagrams proposed under [rcagent #162](https://github.com/edithatogo/rcagent/issues/162) and its specialist child issues.

The current portable skill's twelve Mermaid templates remain separate under `skills/rca-investigation/assets/templates/mermaid/`. Do not promote these SVGs into admitted skill templates or copy their illustrative assertions into a real investigation.

## Figure register

| SVG | rcagent issue | Intended representation |
| --- | --- | --- |
| `issue-139-accimap.svg` | [#139](https://github.com/edithatogo/rcagent/issues/139) | Cross-level sociotechnical conditions and hypothesised links |
| `issue-167-seips.svg` | [#167](https://github.com/edithatogo/rcagent/issues/167) | Interacting work-system components |
| `issue-168-swiss-cheese.svg` | [#168](https://github.com/edithatogo/rcagent/issues/168) | Defence layers and possible vulnerabilities |
| `issue-169-bowtie.svg` | [#169](https://github.com/edithatogo/rcagent/issues/169) | Threat, preventive barrier, top event, mitigation and consequence |
| `issue-174-stamp.svg` | [#174](https://github.com/edithatogo/rcagent/issues/174) | Controllers, controlled process and feedback |
| `issue-175-fta.svg` | [#175](https://github.com/edithatogo/rcagent/issues/175) | Top event, Boolean gates, intermediate and basic events |
| `issue-176-eta.svg` | [#176](https://github.com/edithatogo/rcagent/issues/176) | Initiating event, conditional branch stages and outcomes |
| `issue-177-cld.svg` | [#177](https://github.com/edithatogo/rcagent/issues/177) | Signed, provisional feedback relationships |
| `issue-178-xmr.svg` | [#178](https://github.com/edithatogo/rcagent/issues/178) | Individuals and moving-range exploratory monitoring |
| `issue-179-fram.svg` | [#179](https://github.com/edithatogo/rcagent/issues/179) | Function-aspect couplings, not causal fault pathways |

## Validation

The repository's `tools.validate_proposal_visuals` verifies the **complete expected figure set** and checks:

- XML is well formed, with no DTD/entity declaration, script, event-handler attribute, external URI or unsupported SVG element.
- Root SVG contains an accessible image role and nonempty alternative description.
- Dimensions and basic shape coordinates are finite and within the viewBox.
- Local SVG marker references resolve to unique elements.
- A synthetic-data notice and a visible interpretation boundary appear.

Run from the repository root with locked development dependencies:

```sh
uv run --no-sync python -m tools.validate_proposal_visuals
uv run --no-sync python -m pytest -q tests/test_validate_proposal_visuals.py
```

**This is a source-level gate only.** It does not establish acceptable layout, complete text visibility, screen-reader reading order, contrast, mobile legibility, correct specialist notation, numerical accuracy, clinical validity or Mermaid parser support. It is not a sanitiser for arbitrary untrusted SVG inputs. Do not use this tool to approve third-party uploads.

Before merging the illustration PR, review all ten figures at 100% and 200% scale, narrow-screen presentation, and light/dark GitHub themes, then review each against its method definition, including the associated boundary case. Any unresolved notation or accessibility defect blocks visual acceptance. Preserve any uncertainty and limitations in the relevant issue.

## Integration

Only the diagram source and its acceptance checks are in scope here. Do not change the shared evidence schema, skill package/admission manifests, clinical process, Conductor track ownership, current jurisdiction packs or historical qualification evidence.

No SVG in this directory is an approved native Mermaid grammar. Cross-repository upstream discussions remain referenced from the rcagent issues, but those upstream repositories are outside this implementation branch.
