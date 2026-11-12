# Frontier assurance delivery evidence

Status: implementation and bounded local verification complete; hosted checks and merge pending. No clinical validation, model run or qualified component is implied.

## Scope and starting evidence

- Assessment: `a895d42a8738d2937f849b65e3b892042f64b979`.
- Integration base: `50c8a81` from `master` on 12 November 2026 UTC (13 November in Australia/Brisbane).
- Upstream subsequently advanced to `414b7fc9395b454e6ec39b228068605c40d0fc59` (basedpyright1.40.2); merged at `02c05d7`. The first baseline rollout is bound to that actual base while retaining the original measurement provenance and caps.
- Authorised increment: typed evidence and relationship repair; public-export privacy repair; current template/style/Just Culture admission; strict CI and quality tools; source-aware death-review planning; staged component/frontier programme and selective Rust ADR.
- Scientific implementation remains Track 12. New tracks are [#125](https://github.com/edithatogo/rcagent/issues/125) and [#126](https://github.com/edithatogo/rcagent/issues/126).

Historical releases and negative model studies are preserved. This source increment does not retroactively repair a released archive or qualify a local model.

## Environment limitation

This remote development environment denies AF_UNIX socket creation used by some existing concurrency/socket tests. The baseline had the same failure class. No such test is deleted, weakened or marked passing because of that restriction. Hosted CI on the supported platforms must supply the corresponding evidence.

## Implemented behaviour

- Typed ID and relationship resolution, including the schema1.0 migration edge; private records rejected by public export; explicit metadata-only public summary.
- Forty current draft rendering/support assets admitted by exact hash; both builders validate the bytes they package. Historical quarantine remains untouched. Reserved archive names and output inside the skill source fail before writing.
- Locked quality/conformance environments, strict basedpyright, broad Ruff+format, ty, Bandit, Vulture, Hypothesis, real pytest-gremlins and Scalene jobs. The initial 9,801-diagnostic baseline has decreased to 9,713; no new module or per-file/rule budget was added.
- Two reviewed Bandit subprocess findings remain bound to frozen source/report bytes; temporary native-path adaptation preserves their narrow scope on Windows. The consumed prospective protocol and its negative result remain unchanged.
- Current NSW incident rules withheld using `pending_source_verification`, with no deadline and no fabricated owner-approval request. QLD directive-supported deadlines retain their direct authoritative source while the guideline's metadata conflict is recorded.
- Track13/#125 and Track14/#126 registered in Conductor; parent workstreams#2/#3 reopened for the new work. Track12 remains scientific owner and deterministic CAW16/20 no longer wait for an LLM.

## Local verification

| Check | Observed result |
| --- | --- |
| Locked dependency resolution, Ruff+format, ty, basedpyright1.40.2, non-growth baseline, hash-bound Bandit scan, Vulture, Unicode, repository and benchmark contracts | Passed on integrated code; seven deterministic benchmark cases passed |
| Complete local `tools.full_validation` run | 1,890 passed, 11 skipped, 53 failed; 52 belong to the known AF_UNIX restriction, one was a Hypothesis timing flake described below; coverage about93%, above90% floor |
| Evidence/template/release focused implementation checks | 179 passed before the small legacy-reference follow-up; follow-up evidence/properties54 passed; integration privacy review80 packaging/admission and50 evidence tests passed |
| Report-gate and validation-command tests after platform adapter | 67 passed; actual scanner returned0 with the two frozen exceptions |
| pytest-gremlins | 23/23 real kills for `tools/release_admission.py`; no survivors/timeouts/errors/pardons. Initial20/23 exposed three missing assertions, then fixed |
| Fresh integrated Scalene run | 300 completed synthetic validation/hash round-trips;11.869760513305664s profiler elapsed;2.0069217681884766MB sampled allocation footprint;5 allocation samples; strengthened program/CPU/memory/completion/fixture checks passed |
| Live Agent Skills conformance | Official pinned validator, complete project profile and monitored upstream drift passed; observed upstream83021e2 changed only unmonitored governance/style files |
| Agent review | [Four recorded roles and resolved findings](./review.md); three substantive cross-review scopes plus integration review |

The Hypothesis failure was a timing flake, not a different output: the same Unicode input took269ms and124ms against the default200ms limit under coverage. Schema-heavy properties now use a finite1,000ms correctness budget, retain the observed input as an explicit example and keep generated data/counts/health checks. The separate Scalene job measures performance; no latency target is inferred from this budget. Focused coverage rerun evidence is recorded in the delivery follow-up.

The fresh raw profile SHA-256 is `7f8de628cb2d4bc38477587428dec6f2ad49ea20eb55ac1cd158d87d40c0a5bb`; completion receipt SHA-256 is `b8e19213ade9904ce6ecdd4bd3c207636676dfc869e1fc014144be541389271d`. Its fixture fingerprint is `sha256:25f159bebf270234e21ba3bba6efd13a6bf522157eb323cacef4511b53345f88`. Instrumented allocation footprint is not peak RSS or a cross-machine performance claim.

## Hosted enforcement

Live ruleset21834601 (`master-stable-automated-checks`) is active with zero required approving reviews and requires dependency-review plus the three platform validation contexts. The existing macOS/Windows contexts are preserved. The always-running `validate (ubuntu-latest)` aggregate requires the entire Python/platform matrix, mutation and profile jobs to succeed; skipped/cancelled dependencies fail. The actual aggregate shell passed all-success and rejected nine failure/skip/cancel combinations in local checks. No new approval count or ruleset bypass was introduced.

Hosted checks and final delivery state will be appended after observation. Local socket denial is not a hosted pass.

## Remaining work

The D0–D8 ladder, actual independent model/modality comparisons, isolated deployment tests, Rust benchmark, external holdout and clinical workflow observations are planned work. Existing strict typing debt remains explicitly baselined and must decrease through FAW06. A passing engineering increment is not completion of Track 13's scientific qualification programme.
