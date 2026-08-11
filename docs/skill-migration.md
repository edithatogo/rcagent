# RCA Investigation Skill Migration

## Mapping

| Former dependency | Canonical destination |
|---|---|
| `agents/rca-triage.md` | `skills/rca-investigation/references/workflows/triage.md` |
| `agents/rca-investigate.md` | `skills/rca-investigation/references/workflows/investigate.md` |
| `agents/rca-report.md` | `skills/rca-investigation/references/workflows/report.md` |
| `agents/rca-track.md` | `skills/rca-investigation/references/workflows/track.md` |

The root agents remain historical material until adapter consumers have
migrated. They are no longer required by the portable core.

## Compatibility changes

- Severity and notification rules are explicitly jurisdiction-dependent.
- Confidentiality or quality-improvement context no longer implies legal
  privilege.
- Evidence, accounts, analysis, findings, decisions, and uncertainty are
  distinct.
- Codex and Claude Code use optional manifests and the shared installer.
- No client receives experimental pre-approved tools from the portable core.

## Rollback

Revert the focused Track 00 commits in reverse order or reinstall the last
reviewed skill archive. Do not delete historical root agents until consumer
and Git-history recovery tests pass. A rollback must not reintroduce automatic
privilege claims or bypass de-identification and human-review gates.
