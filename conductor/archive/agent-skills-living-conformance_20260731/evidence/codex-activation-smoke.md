# Codex Activation Smoke Receipt

- Checked: `2026-07-31`
- Codex CLI: `0.145.0`
- Mode: ephemeral, read-only, isolated temporary workspace
- Adapter: `adapters/codex/adapter.json`
- Thread: `019fb73b-d18f-76a0-bba7-4e8c13cb7d1b`
- Prompt case: `held-positive-implicit`
- Result: smoke pass; not a formal held-out evaluation

## Direct observations

- Codex explicitly stated that it was using the installed
  `rca-investigation` skill.
- It read the installed `SKILL.md` and relevant investigation references.
- It produced a provisional chronology and evidence-gap plan.
- It preserved disagreement between accounts, separated evidence states,
  stated uncertainty, declined causal and severity conclusions, used
  systems-focused language, and required authorised human decisions.
- One attempted broad file-enumeration command was rejected by the read-only
  execution policy; the agent recovered with narrower reads.

## Limitations

- Only one positive case and one trial ran.
- The raw JSONL stream was observed in the execution log but was not retained
  as a repository artefact.
- Codex reported that skill descriptions were shortened to meet a two-percent
  skills context budget because unrelated globally installed skills remained
  visible.
- Usage was 168,453 input tokens, of which 136,704 were cached, and 2,088
  output tokens.
- `--ignore-user-config` did not isolate global skill/plugin discovery.
- The run also surfaced unrelated global skill/plugin errors outside this
  repository.

The result proves that the Codex adapter can discover and execute the portable
skill in this environment. It does not satisfy repeated trigger thresholds,
held-out evaluation, cross-client compatibility, or output-quality acceptance.
The full matrix requires a bounded context-isolation and compute decision.
