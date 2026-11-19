# H5 independent HEAPS engineering qualification protocol

This qualification follows [the H4 implementation](https://github.com/edithatogo/rcagent/pull/142) and its [observed acceptance](../../conductor/tracks/qld-heaps-review_20261116/h4-acceptance-20261117.md). Only generated-synthetic, fully local inputs are authorised. A positive result is engineering evidence, not clinical review or organisational approval.

## Independent test surface

The harness in [the H5 test module](../../tests/test_heaps_h5_qualification.py) reads the frozen H3 oracle and raw fixtures itself. It never imports the H4 test adapters, expected-output helpers or internal HEAPS validators. Calls use the public assemble_packet API and the real Python module subprocess. SHA-256 and byte lengths are computed independently from returned files.

H5.1 executes all 38 frozen variants in 25 acceptance cases, plus subprocess positive, negative and abstention controls. H5.2 verifies object-key changes versus raw ingress, changes to canonical array ordering, property-based mutations of captured source bytes, duplicate source identity, unsupported input data classes, stale detached decisions and deterministic replay. H5.3 verifies that unavailable or unsupported findings, participation, local templates, dates and outcomes never create positive authority or submission claims. A full source-head CI matrix is required in addition to focused tests.

## Reproduction and evidence

Using the checked-in environment, run:

    uv sync --locked --extra validate --extra test --extra lint --extra assurance
    uv run --no-sync pytest -q tests/test_heaps_h5_qualification.py

Do not infer success from the test definition alone. Record actual source and output hashes, executed counts, failed cases, separate disagreements, independent reviewer scope and exact hosted job/check identities in the H5 acceptance receipt. Keep any historical failures, queued scans or unavailable runners distinct from successful checks. Never weaken the frozen H3 oracle, CI gates, typing or security allowances to obtain a pass.

## Boundary and handoff

H5 qualifies only synthetic packet engineering against the exact observed revision. Source hashes do not prove source truth, and a synthetic label is not de-identification. D0 exact spans, D1 extraction, D2 timeline composition, AcciMap, the current CHHHS/QHEPS instrument, clinical decision review, statutory protection, system-of-record submission, action effectiveness and patient benefits are not tested by H5. H6 requires separately obtained authorised local instruments and applicable clinical/data/organisational authority. The Conductor coordinator retains portfolio registration and cross-track receiving decisions.
