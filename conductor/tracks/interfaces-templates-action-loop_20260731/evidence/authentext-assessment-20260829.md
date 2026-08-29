# Authentext bounded assessment

Observed: 2026-08-29T09:20:00Z (bounded local assessment; raw npm log was not retained)

- Exact vendored gitlink: `ca39b86eb604a6fe4cfa9a0918638195af82c1af`
- Working tree: clean when inspected
- Package version: 3.2.0
- Declared licence: MIT
- Licence SHA-256: `62e62f185161470429df7da28a91d8f04d0a822f6b97e87b2370f585f54338a7`
- Command: `npm test` in `.agents/plugins/authentext`
- Environment: Node `v26.7.0`; npm `11.19.0`
- Package JSON SHA-256: `63f9b3f31330a58bd6b34bbb8c492c3b93504f9467186512c4d2cb0c89126737`
- Package lock SHA-256: `ba1717acd51d31b845d1c77c636c5612b556eda0523ccd176f0d6e67a776ff9c`
- Result: exit 1; initial tests passed, then the suite terminated with `ERR_MODULE_NOT_FOUND` for `js-yaml` in the existing local environment.

No dependency was installed and no formatter was adopted. Authentext is unavailable in the existing environment and remains an unsupported optional contract candidate; this is not a framework-quality rejection. This result does not establish privacy, provenance, document conformance, professional-register suitability or redistribution rights for generated inputs or outputs.
