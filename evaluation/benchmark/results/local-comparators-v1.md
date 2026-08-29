# Local comparator pilot

- Scope: internal, synthetic-only, non-promotion research evidence
- Prompt contract: `synthetic-structured-v3`
- Repeats: 3 fixed-seed runs for each of 7 cases and 3 model size classes
- Receipt SHA-256: `9a78e0bb746ffc4957f93a37b8cd5a59f3e22958f6086fc051a0c351d7344ed7`

| Locally admitted comparator | Strict passes | Schema-valid outputs | Mean latency |
| --- | ---: | ---: | ---: |
| Qwen2.5 0.5B Instruct Q4_K_M | 0/21 | 21/21 | 3260.205 ms |
| Qwen2.5 1.5B Instruct Q4_K_M | 3/21 | 21/21 | 5151.230 ms |
| Qwen2.5 7B Instruct Q4_K_M | 0/21 | 21/21 | 10830.342 ms |

All fixed-seed responses were identical within each model and case. Across the 63 observations, all evidence identifiers were exact; 57 missed the strict claim-type set and 12 missed the expected abstention state. These are negative pilot findings under this prompt and rubric, not a universal ranking or a model-suitability conclusion.

## Boundaries

- No comparator is promoted or declared suitable for operational use.
- No clinical gold standard or operational threshold is established.
- Human agreement is not observed; independent authorised raters remain required.
- Weights remain in an isolated local cache and are not redistributed.
- No external comparative publication has been approved.
- This report is not clinical advice or clinical, policy, legal, regulatory, organisational, procurement, deployment, or accountable-human approval.
