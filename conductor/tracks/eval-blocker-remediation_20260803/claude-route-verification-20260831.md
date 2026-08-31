# Claude submission-route verification

Read-only first-party verification completed `2026-08-31T09:49:01Z` by agent
`claude_routes`. This supplements the archived Track 11 packet; it is not a
submission, publisher-access receipt or vendor approval. No authentication,
terms acceptance, download, client invocation or account change occurred.

## Current route

Skills-only plugins are supported. Third-party submissions go to
`claude-community`, not the separately curated official marketplace. Individual
authors can use the Console submission form. The claude.ai form requires a
Team/Enterprise organisation and directory-management access; that requirement
does not apply to every author. Local validation precedes vendor review, which
also includes automated safety screening. Strict validation additionally fails
warnings. Approved catalogue entries are commit-pinned, but catalogue CI advances
pins when repository commits arrive; catalogue publication syncs nightly.
Consequently, initial pinning alone is not assurance that future versions remain
inside the repository's exact-candidate admission envelope.
Source: [plugin creation and community submission](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace).

Both [Console](https://platform.claude.com/plugins/submit) and
[claude.ai](https://claude.ai/admin-settings/directory/submissions/plugins/new)
returned the browsing tool's `Internal Error`. This is not an observed login
screen or permission denial. Actual publisher access, form fields, terms,
source-layout acceptance and submission state remain unverified. Do not infer
Claude logo or legal-document requirements from another platform's checklist.

## Package and version distinction

A manifest requires only kebab-case `name`; descriptive metadata and semantic
version are optional. Unknown fields warn, whereas invalid recognised-field
types can prevent loading. Strict validation treats warnings as errors. The
repository's generated Claude manifest uses documented metadata and
`skills: "./skills/"`; this source comparison is not a fresh validation pass.
Source: [manifest reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema).

Marketplace entries require `name` and `source`. Git and git-subdirectory
sources support commit pins. An HTTPS ZIP `archive` source can carry SHA-256
integrity pinning and requires Claude Code 2.1.224 or later. General marketplace
schema support does not prove that the community submission form accepts every
source type. Source: [marketplace sources](https://code.claude.com/docs/en/plugin-marketplaces).

The existing builder's marketplace ZIP uses a relative directory source,
`./plugins/rca-investigation`, not an `archive` source. Do not declare that
artefact broken because of the newer archive-source version requirement. The
[v0.1.1 receipt](../../archive/distribution-registries-plugins_20260731/evidence/hosted-release-v0.1.1-20260829.md)
records historical Claude 2.1.126 local validation and isolated lifecycle, not
current strict validation or hosted catalogue installation. Its exact supported
release remains distinct from current repository HEAD.

## Recommendation and remaining evidence

Prepare a local-only strict check of the exact existing package if the installed
client supports it; record an unsupported flag/version instead of upgrading.
When scoped Console access becomes available, inspect the actual form and
resolve source layout and automatic pin advancement against exact-candidate
admission controls before submission. Reuse v0.1.1 and existing materials where
accepted; do not create a new release, repository or hosting arrangement merely
because the form could not be inspected.

Standing submission approval need not be requested again. Access, exact
candidate eligibility, any new terms/attestation and vendor review remain
separate evidence boundaries. No independent human repository-review gate is
introduced. Route identified; submission readiness not established.
