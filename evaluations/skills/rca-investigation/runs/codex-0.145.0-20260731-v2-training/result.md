# Codex Trigger Candidate v2 Training and Regression

- Skill revision evaluated: `4cf75dc`
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

The description remained too broad. Codex treated “clinical incident” as
applicable to medication dosing and “investigation reports” as applicable to a
privilege assessment. The fresh v2 held-out partition was not evaluated.

The next candidate removes those adjacent domain nouns and requires an
established past safety investigation or an explicit investigation-workflow
task.
