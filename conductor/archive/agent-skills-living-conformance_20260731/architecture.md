# Track 00 Architecture

`skills/rca-investigation/` is the canonical, independently copyable package.
It may depend only on its own `SKILL.md`, `references/`, `scripts/`, and
`assets/`. References are skill-root-relative; the core cannot read
repository-root agents, adapters, tests, Conductor files, or credentials.

Canonical healthcare procedures live under `references/workflows/`. Method
knowledge lives under `references/methods/`. Static output resources live
under `assets/`. Repeated deterministic operations belong under `scripts/`.
Adapters consume these resources through relative linkage or installation;
they do not copy authoritative clinical content.

Portability is proven by validating the repository copy, a clean isolated
copy, and an extracted archive. Client support, triggering, and output quality
require separate evidence and cannot be inferred from structural portability.
