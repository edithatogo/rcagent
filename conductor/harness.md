# Workbench Harness Contract

The deterministic command surface is `python -m tools.workbench`.

| Entry point | Contract | External effects |
|---|---|---|
| `doctor` | Report local governance and runtime readiness as JSON | None |
| `context INPUT.json` | Validate bounded context, privacy mode, ownership, freshness, exclusions, handoff, and rollback fields | None |
| `queue INPUT.json` | Select the next dependency-ready, lane-safe, path-safe item | None |
| `validate` | Run repository governance diagnostics | None |
| `evaluate` | Fail closed as unavailable until model or human execution evidence is separately admitted | None |
| `receipt INPUT.json` | Validate the minimum durable receipt contract | None |
| `reconcile` | Validate local governance while explicitly reporting that hosted and external completion were not checked | None |

The harness never downloads weights, uses credentials, performs inference, acquires or takes over a lease, mutates Git, contacts an external system, or converts a local pass into release, approval, or hosted-completion evidence.

Recovery classification is implemented in `tools.autonomy_harness`. Transient and deterministic actions receive at most two attempts. External waits and decisions release their lane. Material risk trips the circuit breaker. Repeated identical attempts without new evidence are prohibited by the project workflow.

Local pytest and the hosted Quality workflow remain the coverage-producing regression gates. Renovate, dependency review, Codecov, and Agent Skill Conformance are hosted evidence sources whose configuration does not itself prove execution.
