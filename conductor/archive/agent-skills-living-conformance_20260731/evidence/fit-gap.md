# Track 00 Fit-Gap Receipt

## Receipt

- Checked: `2026-07-31T17:51:19+10:00`
- Base revision: `629e8c0dfdbb0c68bedc130a67ab54af0451ea44`
- Privacy mode: public repository metadata and public skill content only
- System of record: the Agent Skills specification and its upstream repository
- Upstream revision: `38a2ff82958afee88dadf4831509e6f7e9d8ef4e`

## Acquisition-Ladder Result

| Capability | Existing owner | Result | Smallest intervention |
|---|---|---|---|
| Skill package format | Agent Skills specification | Adopt | Use `SKILL.md` and standard resource directories |
| Baseline validation | upstream `skills-ref` | Adopt with limits | Pin the checked revision and preserve its raw result |
| Domain procedure | This project | Retain and refactor | Move RCA workflows inside the portable skill root |
| Portability and privacy assurance | No complete upstream owner | Project extension | Deterministic checks and negative fixtures |
| Client-specific behaviour | Codex and Claude Code contracts | Adapt | Thin adapters with capability declarations |
| Upstream change detection | Git and authoritative documentation | Adapt | Compare recorded normative inputs and validator behaviour |

No organisational incident system is displaced. The skill produces bounded
assistive material; an approved incident or records system remains
authoritative for operational cases.

## Dependency and Risk Assessment

- The specification is a standard target and introduces no runtime dependency.
- `skills-ref` is evaluation/development tooling. Its upstream README says it
  is demonstrative and not intended for production use, so its success cannot
  be the project's only assurance evidence.
- The canonical skill must remain dependency-free and usable offline after
  installation.
- Live conformance requires network access to resolve the authoritative
  sources. Network failure yields `unverified`, never `pass`.
- `allowed-tools` remains experimental and is omitted from the portable core
  until each adapter has compatibility evidence.
- Licence declaration remains an owner decision. Its absence is recorded,
  without blocking other phases.

## Project-Owned Gap and Exit

The project owns only healthcare incident-investigation content, additional
privacy and evidence-integrity gates, deterministic portability checks,
governed extension evidence, and thin adapters. It does not fork the format or
validator.

Any local validator rule must identify its upstream source or project policy,
have a negative fixture, and remain removable. When upstream provides an
equivalent production-grade check, replace the local rule after contract
tests show equal or stronger behaviour.

## Result

**Adapt.** Use the official format and reference validator, then add bounded
project assurance for demonstrated gaps. No new subsystem or ADR is required.
