# Agent Skill Conformance

## Architecture

`skills/rca-investigation/` is the client-neutral source of truth. Its
`SKILL.md`, workflows, method references, and assets are independently
copyable. Client manifests under `adapters/` install that same directory; they
do not contain a second copy of healthcare investigation instructions.

The portable core deliberately omits experimental `allowed-tools`. Codex,
Claude Code, and other clients retain their ordinary permission controls.
Licence metadata remains omitted until the owner selects a licence.

## Local validation

Install the validation profile and run:

```powershell
uv run --python 3.13 --extra validate --extra test python -m tools.validate_skill skills/rca-investigation
uv run --python 3.13 --extra validate --extra test python -m tools.check_skill_drift
uv run --python 3.13 --extra validate --extra test pytest --cov=tools
```

For offline validation, use:

```powershell
uv run --python 3.13 --extra validate python -m tools.check_skill_drift --offline
```

Offline success proves only that the recorded local contracts pass. It cannot
establish that the upstream specification or validator is current.

## Optional client installation

Install into an isolated destination first:

```powershell
uv run --python 3.13 python -m tools.install_skill_adapter codex --destination-root <root>
uv run --python 3.13 python -m tools.install_skill_adapter claude-code --destination-root <root>
```

Use `--replace` only after reviewing the exact destination. The installer
rejects absolute and escaping manifest targets.

## Extension governance

`conductor/tracks/agent-skills-living-conformance_20260731/extensions.json`
records stable, experimental, unsupported, inapplicable, and decision-pending
fields. Promote an experimental field only after exact client-version tests,
safe fallback verification, and a receipt. Never weaken privacy or human
review because a client supports broader tool permissions.

## Drift response

The scheduled workflow compares the live upstream revision with the reviewed
baseline. A changed revision requires:

1. inspect specification, guidance, and validator changes;
2. update the compliance matrix and negative fixtures;
3. run the pinned old and candidate validators;
4. review diagnostics and client compatibility;
5. update the baseline only after evidence passes; and
6. preserve both receipts.

Network failure is `upstream_unavailable`; revision change is
`normative_review_required`. Neither is a current-conformance pass.

## Limitations

Structural and deterministic validation do not prove clinical correctness,
trigger performance, output quality, legal applicability, or universal client
support. Those require their separate evaluation and human-review evidence.
