"""Install a canonical skill through a declarative client adapter."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def install_adapter(
    repository: Path,
    client: str,
    destination_root: Path,
    *,
    replace: bool = False,
) -> Path:
    repository = repository.resolve()
    manifest_path = repository / "adapters" / client / "adapter.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = (manifest_path.parent / manifest["canonical_skill"]).resolve()
    if repository not in source.parents or not (source / "SKILL.md").is_file():
        raise ValueError("adapter canonical_skill must resolve inside the repository")

    targets = manifest.get("discovery_targets", [])
    if len(targets) != 1 or not isinstance(targets[0], str):
        raise ValueError("adapter must declare exactly one installation target")
    relative = Path(targets[0])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("adapter installation target must be relative and non-escaping")

    destination = destination_root.resolve() / relative
    if destination.exists():
        if not replace:
            raise FileExistsError(f"destination already exists: {destination}")
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    return destination


def available_clients(repository: Path) -> list[str]:
    """Discover adapter clients from the adapters directory."""
    adapters = repository / "adapters"
    if not adapters.is_dir():
        return []
    return sorted(
        path.parent.name
        for path in adapters.glob("*/adapter.json")
        if path.is_file()
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("client")
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--destination-root", type=Path, required=True)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    if args.client not in available_clients(args.repository):
        parser.error(
            f"unknown client: {args.client} (available: {', '.join(available_clients(args.repository))})"
        )
    try:
        destination = install_adapter(
            args.repository, args.client, args.destination_root, replace=args.replace
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
