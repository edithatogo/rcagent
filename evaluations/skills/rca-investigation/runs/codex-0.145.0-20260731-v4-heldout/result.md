# Codex Trigger Candidate v4 Held-Out Evaluation

- Skill revision evaluated: `5f2f0ca`
- Client: Codex CLI `0.145.0`
- Partition: fresh v2 `held_out`
- Trials: 18, three per case
- Completed: 18
- Timeouts or failed turns: 0
- Input tokens: 865,825
- Output tokens: 10,669
- Overall result: **pass**

| Case | Expected rate | Observed rate | Result |
|---|---:|---:|---|
| held-v2-positive-systems | 1.0 | 1.0 | pass |
| held-v2-positive-closure | 1.0 | 1.0 | pass |
| held-v2-negative-liability | 0.0 | 0.0 | pass |
| held-v2-negative-employment | 0.0 | 0.0 | pass |
| held-v2-negative-clinical | 0.0 | 0.0 | pass |
| held-v2-negative-policy-summary | 0.0 | 0.0 | pass |

Candidate v4 previously passed positive training and both exposed regression
cases. This partition was then evaluated exactly once. All raw JSONL is
retained with temporary workspace paths redacted; scans found no credentials
or direct case identifiers.

This receipt supports Codex `0.145.0` activation quality for the tested
description and cases. It does not establish equivalent triggering in Claude
Code, another client/model revision, or a future Codex revision.
