# Vendored Plugin Pin Receipt

Recorded: 2026-08-27. Method: `git ls-remote --heads <url> main` compared with
the gitlink SHA carried in `.agents/plugins/<name>`.

| Plugin | Pinned SHA | Upstream main | Drift | Licence |
|---|---|---|---|---|
| conductor (`gemini-cli-extensions/conductor`) | `f06add33b598f4262a190f234828dda551db70d7` | `f06add33b598f4262a190f234828dda551db70d7` | none | Apache-2.0 |
| sourceright (`edithatogo/sourceright`) | `c5fa583431390eee1bf5eae04dc47b01c50d4a1e` | `c5fa583431390eee1bf5eae04dc47b01c50d4a1e` | none | MIT OR Apache-2.0 |
| authentext (`edithatogo/authentext`) | `ca39b86eb604a6fe4cfa9a0918638195af82c1af` | `ca39b86eb604a6fe4cfa9a0918638195af82c1af` | none | MIT |

Upstream findings logged for issue filing: sourceright commits `AGENTS.md.backup`
artefacts; conductor pins for consumers float on `main` rather than release
tags. Registry of record: `vendored_plugins` in
`conductor/integration-map.json`; contributor procedure:
`docs/vendored-plugins.md`.

Environment note (non-blocking): local capability-script tests require pwsh to
initialise; homebrew pwsh on this machine cannot durably create its user module
path through the `~/.local` symlink. GitHub-hosted runners are unaffected; the
5 affected tests pass there.
