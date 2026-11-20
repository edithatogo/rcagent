# Evidence Receipt: PR #191 independent visual and method assurance

- **Evidence ID:** `rcagent-pr191-independent-visual-method-20261120`
- **Scope and issues:** read-only independent visual/method receiving review of [PR #191](https://github.com/edithatogo/rcagent/pull/191), [#162](https://github.com/edithatogo/rcagent/issues/162), and [#189](https://github.com/edithatogo/rcagent/issues/189).
- **Receiving source commit:** [`6026771b9dc26e61eeb7debe11ed06d1ba89158f`](https://github.com/edithatogo/rcagent/commit/6026771b9dc26e61eeb7debe11ed06d1ba89158f); PR base `c59b1a1cb98136c4d3243eba6a4949d680dad3ce`.
- **Conductor reconciliation baseline:** `master` at `f118562b0945b7691cce8130daadbebc2a22acc2` when this document-only branch was created.
- **Observed:** 20 November 2026, 05:11 UTC (15:11 AEST).
- **Review ownership:** independent assurance only. The existing PR #191 implementation owner exclusively retains the ten SVGs, the checked-in validator, its tests, source corrections, integration and acceptance.
- **Data and rights:** public repository source and synthetic examples only; no patient, employee, real operational, model-scored, or rights-sensitive data.
- **Disposition:** **RETURN / NOT ACCEPTED** for PR #191; independent review and handoff evidence prepared, but **implementation-owner acknowledgement has not been observed**. This is not a claim that the implementation, method, accessibility or security is accepted.
- **Related Conductor boundary:** #162 and #189 are proposal/representation issues; no new Conductor implementation track or change to Track 13/D0, canonical record contracts, jurisdiction packs, released skill, or method parser is authorised by this receipt.

## Confirmed source and bounded execution findings

1. **Blocking chart geometry:** `docs/proposals/investigation-visuals/issue-178-xmr.svg` blob `e09c37653e50b8a8a5f370c664cdf72558e9198b` has adjacent `x,y` polyline tuples concatenated without a pair delimiter. Chromium 144.0.7559.96 parsing of the unmodified attribute strings (isolated minimal reproduction, not full-artwork screenshot) found **9 path vertices for 10 Individuals markers** and **8 path vertices for 9 Moving Range markers**. Paths collapse leftwards (~x 0–81) rather than joining markers across x 81–1196. The existing production validator does not inspect `polyline points` pairs. The synthetic point values and annotated mean/upper limits independently reconcile; that does not establish a valid or stable SPC baseline.
2. **Contrast:** six normal-weight 12-unit footer strings do not meet **4.5:1** normal-text contrast against the artwork's white canvas: `#657b8e` ≈**4.40:1** on AcciMap and Swiss Cheese; `#687a89` ≈**4.44:1** on SEIPS, STAMP, XmR and FRAM. This is a bounded source-colour calculation, not a comprehensive renderer or accessibility audit.
3. **320 CSS-pixel width:** all ten source SVGs are `1280×680` with fixed coordinate layouts and no responsive alternate. If fitted to a 320px container, minimum 12-unit text becomes **3 CSS pixels**; typical 17–18-unit labels become 4.25–4.5px. This is a fit-to-width calculation, **not** a successful 320px browser screenshot/reflow inspection.
4. **Dark and zoom:** SVGs paint explicit white backgrounds. Compatibility in a dark host, visual clipping/overflow, alternate text, reading order and actual 100%/200% zoom behaviour **remain unverified**. An external read-only FTA browser inspection could view a desktop graphic, but screenshot and 320px viewport control timed out; do not infer full-artwork visual acceptance.
5. **Method/meaning:** independent source review identified specialist sign-off questions for Swiss Cheese barrier openings/path, STAMP absent-versus-present feedback, Bowtie preventive/recovery barrier flow, FRAM six-aspect port endpoints, CLD signed loop identity, FTA Boolean gate semantics, ETA ordered conditional histories, and the remaining AcciMap/SEIPS evidence and context bindings. These are **review questions**, not clinical findings.

The complete ten-asset Git blob register, the limited numerical known-answer comparison, and earlier evidence are in [#189 independent review comment](https://github.com/edithatogo/rcagent/issues/189#issuecomment-7009332819) and [the PR #191 owning-lane return](https://github.com/edithatogo/rcagent/pull/191#issuecomment-7009319944). The catalogue disposition is [#162 comment](https://github.com/edithatogo/rcagent/issues/162#issuecomment-7009340155). Those comments are **independent-review publications**, not a receiving reply from the implementation owner.

## Commands actually run and artefact provenance

| Observation | Exact execution or source | Result / limitation |
| --- | --- | --- |
| Re-run independent fixtures 20 Nov | `cd /mnt/data/rcagent_pr191_qa_local && python -m pytest -q test_rcagent_visual_audit.py`, Python 3.13.5 | **5 passed in 0.05s**; isolated synthetic audit helper, not rcagent's full test suite |
| Fixture/helper integrity | SHA-256 helper `d4b9c440722df659e6e8b5af832065bf3ae66cf48729eda50d16d09a00d0440f`, test `b1ce382293e59ac01dc373104eca3e47ad93159c0531feae7f7cfcef392fc498` | SHA-256 of locally executed helper and test in previous evidence ZIP |
| Previous browser reproduction | Chromium 144.0.7559.96; minimal exact XmR `points` strings | Delimiter and left-collapse defect observed; no complete ten-asset render suite |
| Browser screenshot asset | SHA-256 `7af11d8b7b79da60723751a9428419cf5e651a6eaee61bde9e229d0fc480c4ff` | Minimal reproduction PNG only, not proof of responsive or dark rendering |
| Prior evidence ZIP | SHA-256 `0037dfc1c80b51397f5187c42fedc1d2992269f92192716609ec71fc25e15e63` | Local user-facing evidence package; not asserted as a GitHub-hosted downloadable artefact |
| Source check | GitHub pinned SVG/README/validator/test blobs and exact PR metadata | Read-only; no production source edits |
| Full local rcagent test suite | Not run; no complete checkout in this environment | **Unverified** |
| Full screenshot/accessibility grid | Not run | **Unverified** |

### Exact-head hosted checks verified on 20 November 2026

| Gate | Workflow run | Verified conclusion |
| --- | --- | --- |
| Quality | [44308793954](https://github.com/edithatogo/rcagent/actions/runs/44308793954) | **success** |
| Dependency Review | [44308794029](https://github.com/edithatogo/rcagent/actions/runs/44308794029) | **success** |
| Privacy and secrets | [44308793953](https://github.com/edithatogo/rcagent/actions/runs/44308793953) | **success** |
| Offline AI security | [44308794841](https://github.com/edithatogo/rcagent/actions/runs/44308794841) | **completed / cancelled**; **not a pass and not waived** |

These hosted checks refer to the **original PR #191 source head** only. An evidence-documentation PR or later repair head needs its own applicable validation. A green source validator does not imply the illustration looks or reads correctly.

## Receiving-owner handoff and remaining dependency

The existing PR #191 owner must:

1. **Acknowledge receipt explicitly** in PR #191, referring to this document and independent-return comment, indicating that the outstanding items remain with that owner. A reviewer's own comment or a review comment from the same linked GitHub account is **not** proof of independent receiving acknowledgement. Until an owner's separate reply is observed, record `acknowledgement=pending`.
2. Repair owned XmR `points` strings by separating `x,y` pairs and add a focused negative/positive regression that checks the 10/9 vertex counts **and ordered coordinates against marker centres**. Retain all current fail-closed source/privacy gates.
3. Repair the six footer colours; independently inspect **all ten full SVGs** for clipping, line/node alignment and labels at desktop, 320px, light/dark appearances, and 100%/200% zoom. Store actual render inputs, viewport, browser/renderer version, screenshot hashes and test outcomes against the **new exact head**. No inferred browser pass from source geometry.
4. Route the specialist interpretation questions to existing method owners. Preserve hypothesis labels, disagreement, unknowns and conditional semantics; do not treat illustrations as evidence or implemented native Mermaid parser capabilities.
5. Re-run and verify **all required new-head CI**, including a successful security workflow rather than relying on the cancelled run. Obtain independent method/accessibility receiving review before changing draft/release disposition, merging, or promoting to the skill.

**Wake condition:** a pushed repair on PR #191 at a new SHA **plus** explicit owner acknowledgement and complete actual-render/security/method evidence. Independent assurance should then re-qualify that new SHA. This receipt is the independent lane's bounded evidence handoff; it does **not** clear the receiving or security gates.

**Rollback:** discard the separate document-only review branch/PR if not admitted. Do not revert or modify PR #191 implementation, protected checks, or historical evidence.
