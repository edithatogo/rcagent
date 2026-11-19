# Generated synthetic signal properties

This Track 13 assurance leaf adds five properties over the existing model-free
signal contracts at baseline `f118562b0945b7691cce8130daadbebc2a22acc2`.
No source interface, scientific model, clinical decision rule or admission
authority changes.

The independent affine-signal oracle checks resampling coordinates and endpoints.
Other properties check sample-count conservation, rejection of invalid allocation
dimensions, identifier-metadata rejection, and the invariant that recomputing a
receipt digest cannot enable clinical interpretation. All data are generated
synthetically; no patient records or model access are used.

`synthetic-properties.yml` runs up to 100 examples per property on relevant PRs and
up to 1,000 weekly or manually. It reuses the uv lock on exact Python 3.15.2 and
limits test time to eight minutes, address space to 4 GiB and job time to twelve
minutes. Hypothesis statistics, the run seed and synthetic failure artifacts are
retained for reproduction. Counterexamples must be reduced to readable regression
tests before any production repair.

## Executed evidence

- New properties plus existing signal contract tests: 18 passed, seed 20261120.
- Five properties at the 1,000-example budget: 5 passed in 89.18 seconds, seed
  20261122, exact repository-local Python 3.15.2.
- Ruff check/format and basedpyright on the new file: passed; zero type diagnostics.
- `python -m tools.full_validation` reached and executed the full test suite after
  passing the preceding quality, typing, security, repository and benchmark gates.
  Result: 3,261 passed, 53 failed, 11 skipped. Socket/session tests cannot establish
  their required local transport in this execution environment. One additional
  historical-source test initially lacked its shallow-clone Git object; fetching
  `e6c1453d68b562829b99f40b925de6d287496601` and rerunning that exact test passed.
  The remaining transport gates are not waived or described as full-suite success.

Existing Track 12/14 scientific ownership and release/clinical admission remain
unchanged. This record establishes only the executed synthetic software evidence;
the PR records current hosted status and the candidate commit.
