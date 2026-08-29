# Operator-owned offline lifecycle

Track 08 does not download, redistribute, install or remove runtime/model
bytes. The bundle verifier accepts an operator-supplied directory only when a
versioned manifest declares offline operation and no redistribution, every
relative path remains under the bundle root, names do not collide, entries are
regular non-symlink files, and byte counts and SHA-256 digests match.

The verifier is idempotent and makes no filesystem changes. A future installer
must stage into a new bounded directory, verify before atomic promotion,
retain the previous inventory for rollback, and remove only paths owned by the
selected inventory. Archives, partial shards, unexpected files and mutable
revisions require a separately specified admission path; none is claimed here.

This verified dry-run contract is the offline path for the currently supported
profile set, which is empty. Positive installation, update, rollback or
uninstall claims require exact runtime/model evidence and applicable rights.
