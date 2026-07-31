# Codex Trigger Candidate v3 Training and Regression

- Skill revision evaluated: `a3d9fd4`
- Client: Codex CLI `0.145.0`
- Partitions: `train`, `regression_exposed`
- Trials: 9, three per case
- Completed: 9
- Overall result: **fail**

| Case | Expected rate | Observed rate | Result |
|---|---:|---:|---|
| train-positive-explicit | 1.0 | 1.0 | pass |
| train-negative-clinical | 0.0 | 0.33 | **fail** |
| held-negative-legal | 0.0 | 1.0 | **fail** |

Requiring an “established healthcare safety investigation” remained
insufficiently precise. Codex inferred investigation relevance from
safety-critical medication dosing and from a privilege question concerning an
incident report.

Candidate v4 requires explicit RCA/SAE workflow intent and states that a
healthcare topic or review document alone does not satisfy activation.
