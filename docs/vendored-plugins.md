# Vendored Plugin Submodules

This repository vendors three governed plugins as git submodules under
`.agents/plugins/`. Their pins, licences, roles, and update policy are the
source of truth in [`conductor/integration-map.json`](../conductor/integration-map.json)
(`vendored_plugins`); this page is the contributor-facing surface.

## Fetching

```bash
git clone https://github.com/edithatogo/rcagent.git && cd rcagent
git submodule update --init   # fetches .agents/plugins/{conductor,sourceright,authentext}
```

CI does not need submodule contents for validation; contributors working on
skill conformance or plugin integration do.

## Updating a pin

1. Read the upstream repository's own governance signals first (for conductor:
   its `conductor/tracks.md`; for authentext: `npm run sync`/`npm test` must be
   clean at the target revision; for sourceright: its hardening tracks and CI).
2. Advance the pin: `git -C .agents/plugins/<name> fetch origin && git -C .agents/plugins/<name> checkout <sha>`.
3. Record the new pin against upstream main with evidence in the owning track's
   receipt (No-LLM programme Phase 1 until that track closes).
4. Commit the updated gitlink plus any registry/receipt changes together.

## Why pins are reviewed by hand

GitHub dependency graph, Dependabot, and code scanning **cannot see inside
submodules**. CVE monitoring for vendored code is therefore an owner-checked
duty on the cadence set in each entry's `update_policy`. Never widen repo
safeguards through a plugin bump without re-running the full local stack:

```bash
uv run --extra validate --extra test --extra lint python -m pytest tests/ -q
uv run --extra lint python -m ruff check tools tests
```

## Known upstream findings

- sourceright ships committed backup artefacts (`AGENTS.md.backup`).
- conductor consumers pin floating `main`; release tags would give stronger
  reproducibility.

Both are recorded as authorised-issue tasks in the No-LLM implementation
programme plan.
