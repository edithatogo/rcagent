# Capability Installer Preflight Receipt — 2026-08-11

The capability installer now defaults to a read-only JSON preflight. Installation
requires explicit network authorization, an absent repository-contained target,
an implemented registry profile, and successful checked native commands.

Verified controls:

- separator-aware repository boundary and repository-root rejection;
- refusal to modify existing or unowned paths;
- `validate` is the only accepted implemented install profile;
- explicit `-AllowNetwork` acknowledgement before package installation;
- fail-closed `$LASTEXITCODE` handling;
- machine-readable preflight and completion output;
- preflight creates no environment and performs no network action.

Verification: direct Windows PowerShell preflight passed and the complete test
suite reported 62 passed.

Rollback, update, independent verification, ownership markers, and uninstall
remain pending. This receipt does not claim those lifecycle operations exist.
