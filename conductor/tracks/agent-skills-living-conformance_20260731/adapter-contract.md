# Client Adapter Contract

An adapter declares its client, tested client revision, discovery location,
supported frontmatter, experimental fields, install method, fallback,
validation command, and evidence receipt. It references the canonical skill
root and contains no healthcare workflow text.

Claude Code and Codex adapters must prove discovery, activation metadata,
skill-root resolution, unsupported-field behaviour, and removal without
damage to the core. Experimental `allowed-tools` may appear only in a tested
adapter. An unknown client receives the unmodified portable core with no
pre-approved tools and all human-review gates intact.
