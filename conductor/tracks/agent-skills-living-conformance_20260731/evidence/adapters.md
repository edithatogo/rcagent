# Client Adapter Receipt

- Checked: `2026-07-31`
- Canonical skill: `skills/rca-investigation/`
- Codex manifest: `adapters/codex/adapter.json`
- Claude Code manifest: `adapters/claude-code/adapter.json`
- Additional-client template: `adapters/template/adapter.json`
- Shared installer: `tools/install_skill_adapter.py`
- Contract tests: pass
- Installed-byte equivalence with canonical `SKILL.md`: pass
- Overwrite without explicit `--replace`: rejected
- Escaping destination: rejected
- Canonical source outside repository: rejected
- Experimental `allowed-tools`: unsupported in both adapters

Both adapters install the unmodified portable core. Client permission controls
remain authoritative. Removing either adapter does not modify the core.
