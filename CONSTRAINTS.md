# Engineering constraints

These constraints support one developer and an agent review panel. They do not
add routine approval steps. The user's current authority and the Conductor
workflow govern external actions and reserved clinical, legal and privacy
decisions.

## Reproducible quality gates

Use `uv sync --locked --extra validate --extra test --extra lint --extra assurance`
and `uv run --no-sync python -m tools.full_validation`. CI installs pinned uv and
uses the committed dependency lock, including the official conformance validator
in its separate `conformance` dependency group. Changing dependencies requires a
reviewable lock diff, not a new owner approval.

Ruff correctness rules and formatting, ty, basedpyright strict, Bandit, Vulture,
repository contracts, seven deterministic benchmark cases, and pytest with
branch coverage all gate the platform matrix. Coverage must remain at least 90%.
Expected failures must be strict: an unexpected pass fails the suite. Full
socket/process tests stay enabled on supported CI runners.

## Legacy debt is explicit

The initial strict typing measurement contains **9,801 diagnostics in 117 legacy
files** after adding upstream type stubs and cleaning lint. This is substantial
unfinished work, not strict type completeness. The upstream basedpyright baseline
records the diagnostics; `quality/typing-debt.json` caps each existing file/rule
count. CI rejects new baseline files/rules and growth against the PR base or
previous master commit. The new quality helpers and tests have no baseline
allowance. Fix affected types incrementally; reduce the baseline with ordinary
basedpyright, then commit the decrease. Do not routinely run `--writebaseline`.

Basedpyright's baseline matches code positions, not semantic proofs. The retained
ty check, tests, code review, and later typed-boundary migration remain necessary.
Ruff deliberately does not enforce annotation/docstring volume or arbitrary
complexity limits. Legacy `pytest.raises` rejection matrices retain the PT011
exception; new boundary regressions should check the intended error precisely.

## Security and dead code

Bandit scans all production tools at all severities and confidence levels.
Import-only B404 findings are excluded; reviewed subprocess argv calls, the
private `mkdtemp` socket directory, allowlisted SQL identifiers with bound values,
and the fixed HTTPS source fetch have individual rule-specific explanations.
Two argv findings in historically frozen source use the native external
baseline instead of source comments. A pre-scan hash gate binds that baseline
and both source files to their reviewed bytes; any change fails and requires
revalidation. See [the frozen-source review](quality/frozen-source-bandit-review.md).
New suppression comments require a concrete reason and code review; never use
bare `nosec`. These checks are not sandboxing or proof that an executable is safe.
Runtime type guards use explicit failures, so optimized Python does not remove
them. Vulture gates findings at 80% confidence; dynamic public APIs are not
automatically deleted because of a static tool's guess.

## Tests must discriminate

Hypothesis belongs in the normal test environment. Use generated adversarial
inputs for provenance, referential integrity, privacy invariants and report
integrity; do not suppress health checks or narrow inputs to manufacture passes.
Use synthetic fixtures and bounded examples. Reproduce failures before changing
the implementation, and retain the minimized counterexample as a regression.

The first mutation gate covers `tools/release_admission.py` with pytest-gremlins.
All generated mutants must be killed by the release tests. Empty runs, scope
changes, survivors, instrumentation failures, timeouts, errors and pardons fail
the report gate. Ordinary tests run first. This is a 23-mutant initial boundary
measurement, not repository-wide mutation coverage. Expand next to typed
references, public export, archive admission and deadline/process cleanup.

## Performance claims require measurements

The Linux/Python 3.12 profiling job runs Scalene with CPU and memory measurement
on 300 actual synthetic schema-validation/provenance round-trips. It retains a
JSON profile and workload receipt for 14 days. Missing or invalid measurements
fail. The gate requires the intended workload program, positive CPU measurements
and samples in the evidence core, and allocation samples. Its versioned
completion receipt must identify the synthetic workload, all 300 iterations,
finite positive wall time and the current fixture fingerprint. Timings and
sampled allocation footprints are observations, not a release
latency or resident-memory guarantee. Establish repeated comparable-run budgets
before enforcing performance regression thresholds. Do not infer Rust migration
benefits from one instrumented Python sample.

Profiling and mutation use separate bounded jobs. They do not require network
access, model calls, credentials or real case data after dependency installation.
Artifacts contain synthetic/public inputs only. Keep private data out of test
logs, caches, profiles and uploaded receipts.

## Review and maintenance

See [the quality guide](quality/README.md) for commands, primary tool references,
scope and verification evidence. Required branch checks should include the full
Quality matrix, mutation and profile jobs. Repository settings and any hosted
run must be verified separately; a YAML change alone does not enable branch
protection or prove a green hosted build.
