# Hosted release receipt — v0.1.1

Date: 2026-08-29  
Supported release: https://github.com/edithatogo/rcagent/releases/tag/v0.1.1  
Published: `2026-08-29T11:55:06Z`

PR #67 merged as `651a9c4`; the fail-closed inventory correction in PR #68 merged as `af5777bdefa2cb0052ee80c1c5fac9ed972568a4`. Annotated tag object `7c58551339dd5fe1f4010ea977ef8ce7ea66bb9b` peels exactly to `af5777bdefa2cb0052ee80c1c5fac9ed972568a4`. GitHub's `targetCommitish: master` was not used as identity evidence.

The release was rebuilt from that exact clean merged commit. Codex plugin validation, Claude Code 2.1.126 plugin validation, and Claude marketplace validation passed before upload. The tag is annotated but not cryptographically signed; no signature or attestation is claimed.

| Asset | GitHub SHA-256 |
|---|---|
| `MANIFEST.sha256` | `96f8cf32b6eba4d8cfd161b1c482224a10c956c30cc524121391e3aaf182c1e6` |
| `distribution-manifest.json` | `7324c23779b88fda3ea60cee7c46d4f0883c1ec831c9524170f90635d93ad167` |
| `rca-investigation-0.1.1.zip` | `d578ad61da4ba9200c74e2b2f26bf9776e40d47a1fe7e11da108a6be62903ae6` |
| `rca-investigation-claude-code-0.1.1.zip` | `dcb6113edd3aebf9c300917344f6cd3767383d3c9fc2749e64037eb898d1a30e` |
| `rca-investigation-claude-marketplace-0.1.1.zip` | `782def8da0cbb8169ed70273bef866682d2acbaef4b3551f5101ccf48f654055` |
| `rca-investigation-codex-0.1.1.zip` | `96bb06f43e7c1771bee5284ccd44609ef52a45949e6a68cf621d87705ee001a7` |
| `release-candidate.json` | `8c81e2e842d8e85bbc3b143a2e8f4a7d32afd84c27cec4c46100d31f958dc0d8` |
| `sbom.cdx.json` | `73713f13421c380121c66bfe21ad82d3da20e35cb1dba20835ff9202a3e08e69` |

All hosted assets were downloaded with `gh release download v0.1.1`. `shasum -a 256 -c MANIFEST.sha256` passed every listed asset. In fresh temporary directories, the core archive passed `validate_skill`; the hosted Codex and Claude archives installed through the safe isolated lifecycle, exposed the expected versioned manifest, and were removed without residue.

`v0.1.0` remains observable with unchanged assets and is marked prerelease/superseded because its lifecycle fields were ambiguous. It is retained as negative lifecycle evidence, not a supported install target.

Rollback is removal of the installed directory and installation of a separately verified supported release. Directory submission, screening, approval, and publication are not implied by this GitHub release.
