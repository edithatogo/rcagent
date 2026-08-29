"""Verify drift-sensitive first-party distribution guidance and emit a receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

SOURCES = [
    {"id": "agent-skills", "url": "https://agentskills.io/specification", "markers": ["SKILL.md", "name", "description"]},
    {"id": "agent-skills-client", "url": "https://agentskills.io/client-implementation/adding-skills-support", "markers": ["skills", "client"]},
    {"id": "agent-skills-licence", "url": "https://github.com/agentskills/agentskills/blob/main/LICENSE", "markers": ["Apache", "License"]},
    {"id": "github-releases", "url": "https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases", "markers": ["release", "tag"]},
    {"id": "github-immutable-releases", "url": "https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases", "markers": ["immutable", "release"]},
    {"id": "github-release-integrity", "url": "https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity", "markers": ["verify", "integrity"]},
    {"id": "claude-plugins", "url": "https://code.claude.com/docs/en/plugins", "markers": ["plugin", "Claude Code"]},
    {"id": "claude-plugin-reference", "url": "https://code.claude.com/docs/en/plugins-reference", "markers": ["plugin.json", ".claude-plugin"]},
    {"id": "claude-marketplaces", "url": "https://code.claude.com/docs/en/plugin-marketplaces", "markers": ["marketplace.json", ".claude-plugin"]},
    {"id": "claude-discovery", "url": "https://code.claude.com/docs/en/discover-plugins", "markers": ["plugin", "marketplace"]},
    {"id": "claude-submit", "url": "https://platform.claude.com/plugins/submit", "markers": ["plugin", "submit"]},
    {"id": "openai-plugins", "url": "https://developers.openai.com/plugins/build/plugins", "markers": ["plugin.json", ".codex-plugin"]},
    {"id": "openai-submission", "url": "https://developers.openai.com/plugins/deploy/submission", "markers": ["submit", "review"]},
    {"id": "openai-security-privacy", "url": "https://developers.openai.com/plugins/guides/security-privacy", "markers": ["security", "privacy"]},
    {"id": "openai-skills", "url": "https://developers.openai.com/codex/build-skills", "markers": ["skill", "SKILL.md"]},
]


def _fetch(url: str) -> tuple[str, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "rcagent-source-verifier/0.1"})
    with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310 - fixed HTTPS allowlist
        return response.geturl(), response.read()


def verify_sources(
    *, fetch: Callable[[str], tuple[str, bytes]] = _fetch, retrieved_at: str | None = None
) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for source in SOURCES:
        try:
            final_url, payload = fetch(str(source["url"]))
        except Exception as error:
            raise ValueError(f"first-party source unavailable: {source['id']}") from error
        if not final_url.startswith("https://"):
            raise ValueError(f"first-party source redirected outside HTTPS: {source['id']}")
        text = payload.decode("utf-8", errors="replace").lower()
        missing = [marker for marker in source["markers"] if str(marker).lower() not in text]
        if missing:
            raise ValueError(f"first-party source markers drifted: {source['id']}")
        records.append({
            "id": source["id"],
            "requested_url": source["url"],
            "final_url": final_url,
            "content_sha256": hashlib.sha256(payload).hexdigest(),
            "markers": source["markers"],
            "status": "verified",
        })
    return {
        "schema_version": "1.0",
        "retrieved_at": retrieved_at or datetime.now(UTC).isoformat(),
        "normative_scope": "point-in-time route and packaging guidance; reverify immediately before submission",
        "sources": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = verify_sources()
    except ValueError as error:
        parser.error(str(error))
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
