"""Detect invisible, directional, and confusable characters ("gremlins") in text files.

Gremlins are characters that render invisibly or reorder surrounding text
(zero-width spaces, soft hyphens, bidirectional overrides). They break diffs,
hide exfiltration channels inside commits, and corrupt conformance fixtures,
so every governable text file in the repository scans clean by default.

Exit codes:
    0 — no gremlins found (or only explicitly allowed findings)
    1 — one or more gremlins found, or a scanned file was not valid UTF-8
    2 — usage error
"""

from __future__ import annotations

import argparse
import configparser
import sys
from pathlib import Path

GREMLINS: dict[str, str] = {
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\u2060": "WORD JOINER",
    "\u00ad": "SOFT HYPHEN",
    "\ufeff": "BYTE ORDER MARK",
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202c": "POP DIRECTIONAL FORMATTING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
}

# Non-breaking spaces are legitimate typography in prose but hostile in code.
NBSP = "\u00a0"

SCAN_EXTENSIONS: frozenset[str] = frozenset(
    {".md", ".json", ".py", ".toml", ".yml", ".yaml", ".mmd", ".csv", ".cfg", ".ini", ".txt"}
)

SKIP_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".uv",
        ".capability-preflight-test",
    }
)


def _gitlink_paths(root: Path) -> set[str]:
    """Return submodule working-tree paths declared in root/.gitmodules."""
    config_path = root / ".gitmodules"
    if not config_path.is_file():
        return set()
    try:
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        return {
            section.get("path", "").strip()
            for section in parser.values()
            if section.get("path", "").strip()
        }
    except (OSError, configparser.Error):
        # Fail open for scanning but never crash the scan itself.
        return set()


def _iter_scannable_files(root: Path, excluded_roots: set[str]) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SCAN_EXTENSIONS
        and not any(part in SKIP_DIRS for part in path.parts)
        and not any(str(path).startswith(prefix) for prefix in excluded_roots)
    )


def scan(root: Path) -> list[str]:
    """Return one human-readable finding line per offending character."""
    findings: list[str] = []
    excluded_roots = {
        str(root / rel) for rel in _gitlink_paths(root)
    }
    for path in _iter_scannable_files(root, excluded_roots):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{path}:0:0: file is not valid UTF-8")
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for col, char in enumerate(line, start=1):
                if char in GREMLINS:
                    label = GREMLINS[char]
                    findings.append(f"{path}:{lineno}:{col}: {label} (U+{ord(char):04X})")
                elif char == NBSP and path.suffix.lower() not in {".md", ".txt"}:
                    findings.append(f"{path}:{lineno}:{col}: NO-BREAK SPACE in code file (U+00A0)")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect invisible, directional, and confusable characters in text files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        type=Path,
        help="repository root to scan (default: current directory)",
    )
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2
    findings = scan(args.root.resolve())
    for finding in findings:
        print(finding)
    if findings:
        print(f"\n{len(findings)} gremlin(s) found.", file=sys.stderr)
        return 1
    print("No gremlins found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
