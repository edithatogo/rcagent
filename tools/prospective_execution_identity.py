"""Bounded on-disk interpreter/dependency identity, never loaded-code attestation."""

from __future__ import annotations

import ast
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import sys
import sysconfig
from pathlib import Path

MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_FILES = 20000
DISTRIBUTIONS = (
    "attrs",
    "jsonschema",
    "jsonschema-specifications",
    "referencing",
    "rpds-py",
    "typing-extensions",
)
MODULES = {
    "attrs": "attrs",
    "jsonschema": "jsonschema",
    "jsonschema-specifications": "jsonschema_specifications",
    "referencing": "referencing",
    "rpds-py": "rpds",
    "typing-extensions": "typing_extensions",
}
OPTIONAL_FORMAT_MODULES = (
    "fqdn",
    "idna",
    "rfc3987",
    "rfc3986_validator",
    "rfc3987_syntax",
    "rfc3339_validator",
    "webcolors",
    "jsonpointer",
    "uri_template",
    "isoduration",
)


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    ).hexdigest()


def project_closure(root: Path, sources: tuple[str, ...], expected: dict[str, str]) -> None:
    """Check every statically imported project module is in the fixed source set."""
    allowed = set(sources)
    if len(sources) > MAX_FILES:
        raise ValueError("identity_file_limit")
    total = 0
    if "tools/__init__.py" not in allowed:
        raise ValueError("incomplete_project_closure")
    for source in sources:
        path = root / source
        if path.resolve() != path or not path.is_file():
            raise ValueError("unsafe_identity_file")
        with path.open("rb") as stream:
            raw = stream.read(MAX_FILE + 1)
        if len(raw) > MAX_FILE:
            raise ValueError("identity_byte_limit")
        total += len(raw)
        if total > MAX_TOTAL:
            raise ValueError("identity_byte_limit")
        if hashlib.sha256(raw).hexdigest() != expected[source]:
            raise ValueError("project_source_changed")
        module_name = source[:-3].replace("/", ".")
        module_name = "tools" if module_name == "tools.__init__" else module_name
        module = sys.modules.get(module_name)
        if module is not None:
            origins = (
                getattr(module, "__file__", None),
                getattr(getattr(module, "__spec__", None), "origin", None),
            )
            if any(type(origin) is not str or Path(origin).resolve() != path for origin in origins):
                raise ValueError("project_import_origin_mismatch")
        try:
            tree = ast.parse(raw)
        except (SyntaxError, UnicodeError):
            raise ValueError("invalid_project_source") from None
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [item.name for item in node.names if item.name.startswith("tools.")]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise ValueError("unsupported_relative_project_import")
                if node.module == "tools":
                    names = ["tools." + item.name for item in node.names]
                elif node.module and node.module.startswith("tools."):
                    names = [node.module]
            if any(name.replace(".", "/") + ".py" not in allowed for name in names):
                raise ValueError("incomplete_project_closure")


def _files(paths: list[Path], base: Path, budget: list[int] | None = None) -> list[dict]:
    if len(paths) > MAX_FILES:
        raise ValueError("identity_file_limit")
    result = []
    budget = [0, 0] if budget is None else budget
    for path in sorted(set(paths)):
        if path.is_symlink() or not path.is_file() or path.resolve() != path:
            raise ValueError("unsafe_identity_file")
        relative = path.relative_to(base).as_posix()
        size = path.stat().st_size
        budget[0] += size
        budget[1] += 1
        if size > MAX_FILE or budget[0] > MAX_TOTAL or budget[1] > MAX_FILES:
            raise ValueError("identity_byte_limit")
        with path.open("rb") as stream:
            raw = stream.read(MAX_FILE + 1)
        if len(raw) != size:
            raise ValueError("identity_file_changed")
        result.append({"path": relative, "bytes": size, "sha256": hashlib.sha256(raw).hexdigest()})
    return result


def environment_identity() -> dict:
    """Hash supported interpreter/stdlib and installed validator distributions.

    This enumerates disk bytes; sys.modules contents and OS libraries are not
    attested. Run from a clean reviewed interpreter, not an injected environment.
    """
    if any(
        name in sys.modules or importlib.util.find_spec(name) is not None
        for name in OPTIONAL_FORMAT_MODULES
    ):
        raise ValueError("unsupported_optional_format_dependency")
    executable = Path(sys.executable).resolve(strict=True)
    stdlib = Path(sysconfig.get_path("stdlib")).resolve(strict=True)
    paths = []
    visited = 0

    def walk_error(error: OSError) -> None:
        raise ValueError("identity_directory_unavailable") from error

    for directory, folders, files in os.walk(stdlib, followlinks=False, onerror=walk_error):
        folders[:] = [name for name in folders if name not in {"site-packages", "__pycache__"}]
        visited += len(folders) + len(files) + 1
        if visited > MAX_FILES:
            raise ValueError("identity_file_limit")
        if any((Path(directory) / name).is_symlink() for name in folders):
            raise ValueError("unsafe_identity_file")
        paths.extend(Path(directory) / name for name in files if not name.endswith(".pyc"))
    budget = [0, 0]
    if not paths:
        raise ValueError("stdlib_inventory_unavailable")
    packages = {}
    required = set()
    for name in DISTRIBUTIONS:
        try:
            dist = importlib.metadata.distribution(name)
        except importlib.metadata.PackageNotFoundError:
            if (
                name == "typing-extensions"
                and sys.version_info >= (3, 13)
                and "typing_extensions" not in sys.modules
            ):
                continue
            raise ValueError("dependency_inventory_unavailable") from None
        if not dist.files:
            raise ValueError("dependency_inventory_unavailable")
        base = Path(str(dist.locate_file(""))).resolve(strict=True)
        members = []
        for member in dist.files:
            if "__pycache__" in member.parts or str(member).endswith(".pyc"):
                continue
            if ".." in member.parts:
                # Installed console wrappers are not imported; record package code only.
                continue
            members.append(base / member)
        records = _files(members, base, budget)
        roots = ("attr", "attrs") if name == "attrs" else (MODULES[name],)
        loaded = [
            module
            for module_name, module in tuple(sys.modules.items())
            if any(
                module_name == prefix or module_name.startswith(prefix + ".") for prefix in roots
            )
        ]
        for module in loaded:
            origin = getattr(module, "__file__", None)
            spec_origin = getattr(getattr(module, "__spec__", None), "origin", None)
            if (
                type(origin) is not str
                or type(spec_origin) is not str
                or Path(origin).resolve() not in members
                or Path(spec_origin).resolve() != Path(origin).resolve()
            ):
                raise ValueError("dependency_import_origin_mismatch")
        for requirement in dist.requires or []:
            if re.search(r";\s*extra\s*==\s*['\"][a-zA-Z0-9_-]+['\"]\s*$", requirement):
                continue
            if ";" in requirement:
                _, marker = requirement.split(";", 1)
                if re.fullmatch(r"\s*python_version\s*<\s*['\"]3\.13['\"]\s*", marker) is None:
                    raise ValueError("unsupported_dependency_marker")
                if sys.version_info >= (3, 13):
                    continue
            dependency = (
                re.split(r"[ (<>=!~;\[]", requirement, maxsplit=1)[0].lower().replace("_", "-")
            )
            if dependency not in DISTRIBUTIONS:
                raise ValueError("unsupported_dependency_closure")
            required.add(dependency)
        packages[name] = {"version": dist.version, "files": records}
    if not required.issubset(packages):
        raise ValueError("dependency_inventory_unavailable")
    library_dir, library_name = (
        sysconfig.get_config_var("LIBDIR"),
        sysconfig.get_config_var("LDLIBRARY"),
    )
    libraries = []
    if sysconfig.get_config_var("Py_ENABLE_SHARED"):
        if not library_dir or not library_name:
            raise ValueError("interpreter_library_unavailable")
        library = (Path(str(library_dir)) / str(library_name)).resolve(strict=True)
        libraries = _files([library], library.parent, budget)
    return {
        "path_bindings": {
            "executable_alias": sys.executable,
            "executable_resolved": str(executable),
            "stdlib": str(stdlib),
            "library_directory": str(library_dir),
            "library_name": str(library_name),
        },
        "python_version": sys.version,
        "implementation": sys.implementation.name,
        "cache_tag": sys.implementation.cache_tag,
        "platform": sys.platform,
        "executable": _files([executable], executable.parent, budget),
        "interpreter_library": libraries,
        "stdlib": _files(paths, stdlib, budget),
        "distributions": packages,
        "limitations": [
            "on-disk-files-only",
            "optional-format-dependencies-required-absent",
            "static-supported-import-closure-only",
            "loaded-code-and-os-not-attested",
        ],
    }
