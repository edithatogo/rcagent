# Track 04 Fit-Gap and Source Verification Receipt

- Track: `nsw-health-jurisdiction-pack_20260731`
- Retrieval time: `2026-08-29T00:54:13Z`
- Data boundary: public official sources and synthetic tests only
- Network use: read-only HTTPS retrieval from issuing-body websites

## Selected systems and smallest gap

The Australian Commission on Safety and Quality in Health Care owns the national standards and frameworks. NSW Health's Policy Distribution System and Queensland Health's policy and directive pages own state policy publication. ims+ and Queensland Health RiskMan, or another organisation-approved system, remain authoritative for incident state. CEC, ACI and coronial websites remain source catalogues.

The smallest project-owned gap is a data-only, versioned mapping of authority, status, rights, workflow transitions and drift state. No incident system, policy store, template library, workflow engine, legal interpreter or external connector was built. No Architecture Decision Record is required.

## Verified source changes

- The NSQHS Standards second edition updated May 2021 remains the recorded current accreditation baseline while third-edition material is in consultation.
- The 2026 National Model for Clinical Governance replaces the 2017 National Model Clinical Governance Framework. The legacy framework remains registered as superseded and cannot drive rules.
- The Australian Open Disclosure Framework was revised in June 2026 and replaces the older framework reference for current mappings.
- NSW `PD2020_047` is still served from Active PDS Documents but its cover reports status `Review` and a review date of 14 June 2026. It is represented as `under_review`, not silently current or superseded.
- NSW `PD2023_034`, `PD2025_032`, `PD2022_023`, `PD2025_031` and `PD2026_001` were retrieved from Active PDS Documents and their cover metadata and replacement history were recorded.
- Queensland `QH-HSD-032` dated 9 October 2024 and `QH-HSDGDL-032-2` effective 1 July 2024 were verified on Queensland Health. Guideline statements remain advisory unless they restate a directive requirement.

## Downloaded-byte evidence

| Source | Bytes | SHA-256 |
|---|---:|---|
| NSQHS second edition, May 2021 | 2,794,382 | `f9432f4b52e8465d36f4ec5ff9c7bbc849d98f2877df05b3f6a37b16784d0f97` |
| National Model for Clinical Governance 2026 | 601,636 | `8f227cd0025834e98582ae6a80c263db9ba5a85986625e6e1eadf4f97f328f3c` |
| Australian Open Disclosure Framework, June 2026 | 878,362 | `d0d3e5ce3b2cd470707c956157d99c723847c802ef706a65ce2b9fa54aec0fac` |
| `PD2020_047` | 1,282,397 | `206514440bf425ccb5fc0dc1743ea546f8b81d89f5007e27db4f988795d5d560` |
| `PD2023_034` | 1,462,655 | `1b3f77c93e4ff4173c1ab7f243f8a509e7521c99fd85ac58caa85350e9c327e6` |
| `PD2025_032` | 407,577 | `849ba3bff69c66b0f2e674fb0c0dd965fbfa3604be33443a3bb34ad81e677e55` |
| `PD2022_023` | 756,226 | `132d306e2d9eea945052152f14282c955386a9c5ac0e1f34c493be825e0b0695` |
| `PD2025_031` | 443,548 | `e7a067301e7ebdbd9e3ee90bb5ff7269379e120520238aaad1fbdfc7ed10a598` |
| `PD2026_001` | 532,230 | `df195661fa3ec35e2a7eaa2c0225e756845a7ee85be558194a5bd9391ada3416` |

The downloaded files were temporary and were removed after hashing and bounded metadata inspection. Repository artefacts link to source material and do not reproduce external templates or documents.

## Dependency lifecycle

| Dependency | Class | Compatibility and drift | Safe fallback | Replacement |
|---|---|---|---|---|
| National and state authority sources | Standard and authority source | Exact registry version, source metadata, checksums where possible and cadence-based comparison | Retain last verified snapshot; unavailable is not passed | Adopt issuer-provided equivalent machine-readable profiles |
| ims+ and RiskMan | Enterprise authority | No connector or credentials; bounded field and state mappings only | Never infer external notification or closure | Organisation-approved connector may replace a future adapter |
| Evidence and privacy contracts | Locked core | Archived Track 02 schema 1.1 and Track 03 assurance schema 1.1 | Fail closed on invalid state, authority, privacy or provenance | Versioned migration only after compatibility tests |
| Local jurisdiction mapping | Optional data-only adapter | Schema 1.0, semantic validation and synthetic negative fixtures | Retain generic core and report jurisdiction profile unavailable | Remove when authoritative systems expose equivalent mappings |

No local shim, upstream code gap or permanent fork was introduced. Generic publication and incident-system changes remain owned by the issuers and organisations rather than this repository.

## Limitations and owner boundaries

- The mapping is not clinical, legal, policy or organisational approval.
- No statutory privilege or legal applicability conclusion is made.
- No real incident, patient, family, staff, credential or organisation data was used.
- No restricted template was copied and no local procedure was adopted.
- Material semantic drift requires accountable human review; the tool only opens a reviewable context and invalidates affected receipts.
