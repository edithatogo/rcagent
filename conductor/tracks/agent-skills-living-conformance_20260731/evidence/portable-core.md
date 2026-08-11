# Portable-Core Receipt

- Checked: `2026-07-31`
- Canonical root: `skills/rca-investigation/`
- Official validator revision:
  `38a2ff82958afee88dadf4831509e6f7e9d8ef4e`
- `SKILL.md`: 111 lines, 5,584 characters
- Explicit skill-root references checked: 11
- Missing references: 0
- Absolute or repository-root reference hits: 0
- Isolated temporary-directory validation: pass
- ZIP archive extraction validation: pass

The canonical skill now contains triage, investigation, report, and action
tracking workflows under `references/workflows/`. Repository-root `agents/`
remain preserved as historical/client material but are not required by the
portable core.

The core now explicitly:

- separates evidence, accounts, analysis, findings, decisions, and uncertainty;
- defaults to de-identified placeholders;
- prevents automatic legal-privilege claims;
- reserves clinical, legal, policy, employment, notification, disclosure, and
  approval decisions for authorised humans;
- treats severity schemes as jurisdiction-dependent; and
- distinguishes implementation from effectiveness.

This receipt proves structural portability for the checked revision. It does
not prove trigger quality, clinical validation, universal client support, or
current conformance after upstream changes.
