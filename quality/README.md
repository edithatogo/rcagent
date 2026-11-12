# Strict quality harness

The harness combines different failure detectors, with explicit scope and
bounded runtime. It does not claim clinical validity, zero hallucinations,
complete static typing, or independent model agreement.

| Check | Enforced behavior | Remaining limitation |
| --- | --- | --- |
| Locked uv environment | Exact direct and transitive dependencies; Python 3.11 floor plus Linux/macOS/Windows 3.15 matrix | A lock is reproducibility, not a vulnerability or provenance guarantee |
| Ruff + format | Broad correctness/style families, unused suppressions, debugger checks and deterministic formatting | PT011 legacy rejection-matrix exception; not all optional style rules are useful gates |
| ty + basedpyright strict | Two static engines; no new strict debt beyond measured legacy baseline | 9,801 baselined diagnostics in 117 files remain to migrate |
| Bandit | All production tools; all severities/confidence levels; narrow reviewed exceptions | Static patterns cannot prove authorization, privacy or runtime isolation |
| Vulture | Fail findings at 80% confidence | Dynamic entry points need manual interpretation at lower confidence |
| pytest + Hypothesis | Deterministic regressions, generated adversarial report invariants; 90% branch-enabled coverage floor | Coverage alone does not prove an assertion is useful |
| pytest-gremlins | 100% real kills for the public release admission boundary; raw verdict gate | 23 initial mutants in one module; other boundaries remain planned |
| Scalene | Real CPU/memory profile of a synthetic validation/hash workload; validated artifacts | Platform-specific sample; performance budgets need repeated measurements |

The [frozen-source Bandit review](frozen-source-bandit-review.md) explains two
exact B603 exceptions outside source files whose bytes were consumed by the
historical prospective protocol. Their baseline and source hashes are enforced
before scanning. The protocol, its historical review and its failed outcome
remain unchanged; this quality work does not create a new study declaration.

## Commands

```bash
python -m pip install uv==0.13.8
uv sync --locked --extra validate --extra test --extra lint --extra assurance
uv run --no-sync python -m tools.full_validation

# Before interpreting mutation scores, the unmodified suite must pass.
uv run --no-sync python -m pytest tests/test_release_admission.py -q
uv run --no-sync python -m pytest tests/test_release_admission.py -q --gremlins --gremlin-targets=tools/release_admission.py --gremlin-report=json --gremlin-workers=2 --gremlin-mutant-timeout=10 --gremlin-coverage-timeout=60 --strict-pardons --max-pardons=0
uv run --no-sync python -m tools.quality_gate mutation coverage/gremlins/gremlins.json

# Scalene's native memory instrumentation is scoped to Linux/macOS. CI uses Linux.
uv sync --locked --extra validate --extra profile
mkdir -p quality-artifacts
uv run --no-sync python -m scalene run -o quality-artifacts/scalene-profile.json tools/profile_workload.py > quality-artifacts/workload.json
uv run --no-sync python -m tools.quality_gate profile quality-artifacts/scalene-profile.json --workload quality-artifacts/workload.json

# The existing official skills-ref revision and all dependencies are locked too.
uv sync --locked --extra validate --extra test --group conformance
uv run --no-sync python -m tools.run_skill_conformance --output skill-conformance-receipt.json
```

Each `uv sync` selects a complete environment for that job. Re-run the full
development sync before using the local full-validation command after profiling.
Python 3.11.0 remains admitted by the project but is excluded from the optional
Scalene extra because upstream Scalene excludes that exact interpreter release.

The profile gate checks the expected workload program, positive CPU measurements
and samples in `tools/evidence_core.py`, and actual allocation samples. The
versioned workload receipt must record 300 completed synthetic round-trips,
finite positive wall time and the current fixture's canonical fingerprint.
Unrelated profiles, empty CPU measurements, missing receipts and stale fixture
fingerprints fail; the gate does not impose an unmeasured performance budget.

The existing branch rule requires the check names `validate (ubuntu-latest)`,
`validate (macos-latest)` and `validate (windows-latest)`. The latter two names
remain on their platform jobs. The Linux name belongs to an always-running
aggregate that requires every platform/Python matrix job, mutation job and
profile job to succeed. Failed, cancelled or skipped dependencies fail that
aggregate. This preserves the existing required checks while adding the new
Python-floor, mutation and profiling gates without repository-setting changes.

## Initial observations

The first mutation run killed 20/23 mutants. New regression assertions for an
invalid inventory path type, an invalid hash type/error stage, and the returned
validated inventory killed all 23 without pardons. A generic "hash" error match
had allowed a later hash mismatch to conceal a missing early type guard.

On the local Linux/Python 3.12.14 environment, Scalene 2.4.0 recorded 300 actual
synthetic validation/hash round-trips, 11.955 seconds of profiler elapsed time
and a 5.020 MB reported sampled allocation footprint. This is not process peak
RSS, a clinical workload estimate, or a performance acceptance threshold.
`quality/verification-20261113.json` captures the bounded measurement metadata.

The initial full local regression reached 93.25% coverage, but this workspace
forbids Unix-domain sockets; 52 pre-existing socket-dependent failures require
normal hosted runners. Tests remain enabled. Hosted status must be observed
after the combined change is committed and submitted; local checks do not prove
hosted success.

## Primary references

- [uv lock and sync](https://docs.astral.sh/uv/concepts/projects/sync/)
- [Ruff rules](https://docs.astral.sh/ruff/rules/)
- [basedpyright baseline](https://docs.basedpyright.com/latest/benefits-over-pyright/baseline/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/)
- [pytest-gremlins configuration](https://pytest-gremlins.readthedocs.io/en/latest/guide/configuration/)
- [pytest-gremlins verdicts](https://pytest-gremlins.readthedocs.io/en/latest/guide/verdicts/)
- [Scalene source and usage](https://github.com/plasma-umass/scalene)
- [Bandit configuration](https://bandit.readthedocs.io/en/latest/config.html)
- [Vulture confidence levels](https://github.com/jendrikseipp/vulture)

The installed tool help and actual generated reports were checked against the
pinned versions. `pytest-gremlins` is the package name; the Unicode gremlins
scanner in the repository is a separate check. Upstream pytest-gremlins does
not itself fail CI merely because mutants survive, and counts timeouts toward
its displayed score. The small local report adapter closes those specific gaps.
