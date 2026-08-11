# Changelog

## 2026-08-11

- Reviewed upstream Agent Skills normative drift through revision
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`.
- Confirmed that skill metadata keys and values are strings and that the
  clarified optional-directory convention requires no package migration.
- Advanced the live-conformance baseline and CI validator pin after review.

## 2026-08-01

- Added a unified, receipt-producing Agent Skill conformance command.
- Made upstream drift classification fail closed for specification and official
  validator changes while retaining honest guidance-only advisories.
- Fixed cross-platform redaction of JSON-escaped Windows workspace paths.
- Recorded the Track 00 implementation review and its remaining owner licence
  gate.

## Unreleased

- Refactored `rca-investigation` into a self-contained Agent Skill.
- Added evidence, privacy, jurisdiction, uncertainty, and human-review gates.
- Added optional Codex and Claude Code adapters with a shared installer.
- Added deterministic conformance fixtures, evaluation contracts, and
  fail-closed upstream drift monitoring.
- Preserved historical evaluation and root-agent material pending governed
  migration.
