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
Linux and macOS enforce that floor on their own runs. Windows runs every applicable
test and collects branch coverage, deferring its percentage floor to a required
combined matrix gate because Unix-only paths are not executable there. The combined
gate requires all four nonempty branch databases, validates their source paths,
combines executed branches and enforces 90%; missing or corrupt inputs fail. This
is a union of executed coverage, not an average of platform percentages.
Expected failures must be strict: an unexpected pass fails the suite. Full
socket/process tests stay enabled on supported CI runners.

## Strict typing has no active debt allowance

The initial strict typing measurement contained **9,801 diagnostics in 117 legacy
files** after adding upstream type stubs and cleaning lint. FAW06 removes the
remaining 3,198 diagnostics across the active `tools` and `tests` scope. All 153
Python files pass an empty external baseline with zero errors, warnings or
information diagnostics. The committed basedpyright baseline is empty and every
allowance in `quality/typing-debt.json` is removed. Keep both files as a zero-debt
ratchet: CI rejects new files/rules/counts and growth against the PR base or
previous master commit. Preserve the original measurement and rollout provenance.

Explicit `Any` annotations are errors. Raw external values enter as `object` or
checked structural containers; validate domain fields before using them or
issuing typed receipts. Do not conceal uncertainty with ignores, blanket schema
casts, exclusions or disabled rules. Do not run `--writebaseline` to absorb new
failures. New code and tests have the same zero allowance. The completion receipt
records the empty-baseline measurement and a failing explicit-`Any` fault probe.

Static checking does not prove runtime input validity or scientific correctness.
The retained ty check, adversarial tests and code review remain necessary.
Ruff deliberately does not enforce annotation/docstring volume or arbitrary
complexity limits. Legacy `pytest.raises` rejection matrices retain the PT011
exception; new boundary regressions should check the intended error precisely.

## Security and dead code

Bandit scans all production tools at all severities and confidence levels.
Import-only B404 findings are excluded; reviewed subprocess argv calls, the
private `mkdtemp` socket directory, allowlisted SQL identifiers with bound values,
and the fixed HTTPS source fetch have individual rule-specific explanations.
Two argv findings in the current descendants of historically frozen source use
the native external baseline instead of source comments. A pre-scan hash gate
binds that baseline and both current source files to their reviewed bytes; any
change fails and requires revalidation. The historical source, protocol, review
and negative results keep their original identities. Current runtime profiles
have distinct engineering identities and do not requalify a consumed study.
See [the source review](quality/frozen-source-bandit-review.md).
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
Run the complete release test file for every mutant with
`--gremlin-no-coverage-filter`; test-selection filtering is not acceptance evidence
for this small boundary. The typing pass adds one mutant and requires all 24 kills.

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
