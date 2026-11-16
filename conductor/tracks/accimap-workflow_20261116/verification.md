# AcciMap verification receipt

Date: 16 November 2026. Implementation commit:
`3f1d143c8ecaba0aad13365dd35afc3701992dd8`; tree:
`20cf409a8c424f61da4edba2c0c9b682524fb99d`.
Base master: `c6892497aa0b03555d5145242c04965471eccc1d`.
The implementation tree uploaded through the GitHub connector exactly matched
the local tree. The final documentation commit adds this receipt and handoff;
it does not change the tested module, schema, tests, fixture or guide bytes.

## Observed result

**All 80 AcciMap tests passed under coverage. The local full repository gate
remains failed because 52 existing socket-dependent tests cannot run correctly
under the executor's AF_UNIX restriction.** Hosted qualification is required.

| Check | Actual result |
|---|---|
| Ruff lint and format, tools/tests | Passed; 156 files formatted |
| ty | Passed |
| Basedpyright, discarded baseline | 0 errors, 0 warnings, 0 notes |
| Strict typing baseline gate | Zero diagnostics; no allowance growth |
| Security, Vulture, gremlin scan | Passed with unchanged baselines |
| Repository/Conductor validation | Passed |
| Deterministic benchmark validation and regression suite | Passed |
| Full pytest with branch coverage | 2,263 passed, 52 failed, 11 skipped in 117.72 seconds |
| Repository coverage | 93.03%; existing 90% floor satisfied |
| AcciMap tests within that full run | 80 passed, 0 failed; three Hypothesis properties |
| Actual validate/render CLI | Passed; repeatable bytes and nonzero invalid-input exits |
| Pinned official skill validator, project profile and live drift check | Current conformance passed |
| Independent code recheck | Three reported defects/gaps repaired and rechecked |
| Mermaid 12.3.0 parser | 10/10 cases passed with jsdom 31.0.1 |
| Browser SVG/layout/DOM verification | Not completed: Chromium socket creation denied |
| Hosted exact-head quality, mutation, profile and conformance | Required; inspect current PR checks |

Runtime: Linux, Python 3.12.14, dependencies from the existing `uv.lock`.
`validate`, `test`, `lint`, `assurance` extras and the existing `conformance`
dependency group were used. No dependency, CI or gate configuration changed.

The 52 remaining failures are in unchanged tests: nine primary-session tests,
17 server-session tests, one study-controller test and 25 Unix HTTP capture
tests. Direct Unix-socket creation returns `PermissionError: [Errno 1]`;
worker exits and missing captures follow that restriction. These are recorded
failures, not converted to skips or passes. The 11 skips are from existing
tests, with no new skip added by this increment.

## Commands and durable evidence

```bash
python -m tools.full_validation
python -m tools.validate_skill skills/rca-investigation
python -m tools.run_skill_conformance --output skill-conformance-receipt.json
python -m tools.accimap validate tests/fixtures/accimap/graph.json \
  --record tests/fixtures/accimap/record.json
python -m tools.accimap render tests/fixtures/accimap/graph.json \
  --record tests/fixtures/accimap/record.json
```

- [Machine-readable verification receipt](../../../evaluation/accimap/verification-receipt.json)
  contains exact source SHA-256 identities, command results, failed-test names,
  log identity and official skill-conformance receipt.
- [Mermaid parser receipt](../../../evaluation/accimap/parser-receipt.json)
  records payloads, input/output identities and parsed topology for each run.
- [Synthetic diagram source](../../../evaluation/accimap/synthetic-example.mmd)
  and [inspection JSON](../../../evaluation/accimap/synthetic-inspection.json)
  were emitted by the actual CLI.
- [Review and repair record](./review.md) preserves failed observations and
  methodological/source-access limitations.

The standalone skill-creator quick validator rejected the pre-existing
`compatibility` frontmatter field. That field is permitted by the
[Agent Skills specification](https://agentskills.io/specification) and accepted
by this repository's pinned official validator. The field and `SKILL.md` were
preserved; the older quick-validator result was not used as the conformance
gate. The official pinned revision was
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`; live drift inspection resolved
`83021e2be457a9b6679148719c1f6074f0ad975e` with only irrelevant upstream changes.

## Parser and visual qualification boundary

An independent agent generated five cases through the public CLI: the ordinary
fixture and four variants targeting syntax, HTML/script, entity and directive
injection. Actual `mermaid.parse` and `getDiagramFromText` accepted each under
strict and loose settings. Each retained 20 parsed vertices (including review
notes), four causal edges, five subgraphs, two dotted connections and two normal
connections. No parsed click link, callback, injected class or configuration
change appeared. Parsed direction/profile order stayed intact.

This is parser evidence, not browser rendering. Chromium 156.0.8078.79 aborted
before Mermaid loaded because the executor denied socket creation. Automatic
approval rejected an escalation attempt; no restriction workaround was used.
No SVG or screenshot was produced. Visual hierarchy, text fidelity after SVG
rendering, readability, crossings and client DOM safety remain open checks.
The temporary Node tooling was isolated outside the repository and introduced
no project dependency or lockfile.

## Acceptance boundary

AM01–AM03 have implemented source, reviewed guidance, a synthetic contract and
parser/CLI evidence. AM04 local source checks pass; whole-repository hosted
qualification and visual review remain pending. AM05 shared registry
integration and merge belong to the existing coordinator. Structural validity,
declared review and passing software checks do not validate causation, source
truth, intervention effectiveness or clinical/organisational approval.
