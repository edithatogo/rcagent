"""Synthetic-only adversarial identity checks; never enumerate the host runtime."""

import hashlib
import io
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import TypeAlias

import pytest

from tools import prospective_execution_identity as identity

Project: TypeAlias = tuple[Path, tuple[str, ...], dict[str, str]]
WalkEntry: TypeAlias = tuple[str, list[str], list[str]]


@dataclass
class SyntheticDistribution:
    files: list[Path]
    requires: list[str]
    version: str
    packages: Path

    def locate_file(self, item: str | Path) -> Path:
        return self.packages / item


@dataclass
class SyntheticImplementation:
    name: str
    cache_tag: str


@dataclass
class SyntheticRuntime:
    executable: str
    version: str
    version_info: tuple[int, int]
    implementation: SyntheticImplementation
    platform: str
    modules: dict[str, object]


@dataclass
class SyntheticEnvironment:
    root: Path
    executable: Path
    stdlib: Path
    packages: Path
    distributions: dict[str, SyntheticDistribution]
    runtime: SyntheticRuntime
    configuration: dict[str, int | str]


environment_identity = identity.environment_identity

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


def symlink_or_skip(path: Path, target: Path, *, directory: bool = False) -> None:
    try:
        path.symlink_to(target, target_is_directory=directory)
    except OSError:
        pytest.skip("host does not permit synthetic symlink creation")


@pytest.fixture
def synthetic_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SyntheticEnvironment:
    root = tmp_path.resolve()
    executable = root / "python"
    executable.write_bytes(b"exec")
    stdlib = root / "stdlib"
    stdlib.mkdir()
    (stdlib / "module.py").write_bytes(b"pass")
    packages = root / "packages"
    packages.mkdir()
    distributions: dict[str, SyntheticDistribution] = {}
    for name in identity.DISTRIBUTIONS:
        member = Path(identity.MODULES[name] + ".py")
        (packages / member).write_bytes(b"pass")
        distributions[name] = SyntheticDistribution(
            files=[member], requires=[], version="1.0", packages=packages
        )

    def distribution(name: str) -> SyntheticDistribution:
        if name not in distributions:
            raise identity.importlib.metadata.PackageNotFoundError(name)
        return distributions[name]

    runtime = SyntheticRuntime(
        executable=str(executable),
        version="synthetic-python-3.14",
        version_info=(3, 14),
        implementation=SyntheticImplementation(name="cpython", cache_tag="synthetic"),
        platform="synthetic",
        modules={},
    )
    configuration: dict[str, int | str] = {"Py_ENABLE_SHARED": 0}

    def get_path(name: str) -> str:
        return str(stdlib)

    def find_spec(name: str) -> None:
        return None

    monkeypatch.setattr(identity, "sys", runtime)
    monkeypatch.setattr(
        identity,
        "sysconfig",
        SimpleNamespace(get_path=get_path, get_config_var=configuration.get),
    )
    monkeypatch.setattr(identity.importlib.metadata, "distribution", distribution)
    monkeypatch.setattr(identity.importlib.util, "find_spec", find_spec)
    return SyntheticEnvironment(
        root=root,
        executable=executable,
        stdlib=stdlib,
        packages=packages,
        distributions=distributions,
        runtime=runtime,
        configuration=configuration,
    )


def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, bodies: dict[str, bytes]) -> Project:
    root = tmp_path.resolve()
    (root / "tools").mkdir()
    bodies = {"tools/__init__.py": b"", **bodies}
    for name, content in bodies.items():
        (root / name).write_bytes(content)
    monkeypatch.setattr(identity, "sys", SimpleNamespace(modules={}))
    return (
        root,
        tuple(bodies),
        {name: hashlib.sha256(content).hexdigest() for name, content in bodies.items()},
    )


def test_synthetic_environment_success(synthetic_environment: SyntheticEnvironment) -> None:
    result = environment_identity()
    assert result["platform"] == "synthetic"
    assert result["stdlib"][0]["path"] == "module.py"
    assert len(result["distributions"]) == len(identity.DISTRIBUTIONS)


def test_file_reader_is_bounded_even_if_file_grows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path.resolve() / "changing.py"
    path.write_bytes(b"x")
    monkeypatch.setattr(identity, "MAX_FILE", 4)
    reads: list[int | None] = []

    class GrowingFile(io.BytesIO):
        def read(self, size: int | None = -1) -> bytes:
            reads.append(size)
            assert size == 5
            return super().read(size)

    def open_growing(*args: object, **kwargs: object) -> GrowingFile:
        return GrowingFile(b"x" * 20)

    monkeypatch.setattr(Path, "open", open_growing)
    with pytest.raises(ValueError, match="identity_file_changed"):
        identity._files([path], path.parent)
    assert reads == [5]


def test_file_budget_accumulates_between_calls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = [tmp_path.resolve() / name for name in ("a", "b")]
    for path in paths:
        path.write_bytes(b"123")
    monkeypatch.setattr(identity, "MAX_TOTAL", 5)
    budget = [0, 0]
    identity._files(paths[:1], tmp_path.resolve(), budget)
    with pytest.raises(ValueError, match="identity_byte_limit"):
        identity._files(paths[1:], tmp_path.resolve(), budget)


def test_environment_budget_includes_packages_executable_and_stdlib(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    total = 4 * (len(identity.DISTRIBUTIONS) + 2)
    monkeypatch.setattr(identity, "MAX_TOTAL", total - 1)
    with pytest.raises(ValueError, match="identity_byte_limit"):
        environment_identity()


def test_environment_global_file_count(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(identity, "MAX_FILES", len(identity.DISTRIBUTIONS) + 1)
    with pytest.raises(ValueError, match=r"identity_byte_limit|identity_file_limit"):
        environment_identity()


def test_symlink_member_rejected(synthetic_environment: SyntheticEnvironment) -> None:
    env = synthetic_environment
    member = env.packages / "attrs.py"
    member.unlink()
    symlink_or_skip(member, env.stdlib / "module.py")
    with pytest.raises(ValueError, match="unsafe_identity_file"):
        environment_identity()


def test_symlink_stdlib_directory_rejected(synthetic_environment: SyntheticEnvironment) -> None:
    env = synthetic_environment
    symlink_or_skip(env.stdlib / "alias", env.packages, directory=True)
    with pytest.raises(ValueError, match="unsafe_identity_file"):
        environment_identity()


def test_stdlib_prunes_only_non_runtime_caches(synthetic_environment: SyntheticEnvironment) -> None:
    env = synthetic_environment
    for directory in ("site-packages", "__pycache__"):
        child = env.stdlib / directory
        child.mkdir()
        (child / "ignored.py").write_bytes(b"excluded")
    (env.stdlib / "ignored.pyc").write_bytes(b"excluded")
    assert [item["path"] for item in environment_identity()["stdlib"]] == ["module.py"]


def test_unreadable_stdlib_walk_cannot_silently_pass(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    env = synthetic_environment

    def unreadable_walk(
        top: str | Path,
        *,
        followlinks: bool = False,
        onerror: Callable[[OSError], object] | None = None,
    ) -> Iterator[WalkEntry]:
        assert Path(top) == env.stdlib
        assert followlinks is False
        if onerror is not None:
            onerror(PermissionError("synthetic unreadable stdlib"))
        return iter(())

    monkeypatch.setattr(identity.os, "walk", unreadable_walk)
    with pytest.raises((ValueError, OSError)):
        environment_identity()


def test_incomplete_empty_stdlib_walk_rejected(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    def empty_walk(*args: object, **kwargs: object) -> Iterator[WalkEntry]:
        return iter(())

    monkeypatch.setattr(identity.os, "walk", empty_walk)
    with pytest.raises(ValueError):
        environment_identity()


@pytest.mark.parametrize(
    ("version", "loaded", "passes"),
    [((3, 11), False, False), ((3, 14), False, True), ((3, 14), True, False)],
)
def test_typing_extensions_conditional_identity(
    synthetic_environment: SyntheticEnvironment,
    version: tuple[int, int],
    loaded: bool,
    passes: bool,
) -> None:
    env = synthetic_environment
    del env.distributions["typing-extensions"]
    env.runtime.version_info = version
    if loaded:
        env.runtime.modules["typing_extensions"] = SimpleNamespace(__file__="/synthetic/untrusted")
    if passes:
        assert "typing-extensions" not in environment_identity()["distributions"]
    else:
        with pytest.raises(ValueError, match="dependency_inventory_unavailable"):
            environment_identity()


@pytest.mark.parametrize("origin_field", ["__file__", "spec"])
def test_imported_dependency_origin_must_match_inventory(
    synthetic_environment: SyntheticEnvironment, origin_field: str
) -> None:
    env = synthetic_environment
    outside = env.root / "foreign.py"
    outside.write_bytes(b"pass")
    member = str(env.packages / "attrs.py")
    env.runtime.modules["attrs"] = SimpleNamespace(
        __file__=str(outside) if origin_field == "__file__" else member,
        __spec__=SimpleNamespace(origin=str(outside)),
    )
    with pytest.raises(ValueError, match="dependency_import_origin_mismatch"):
        environment_identity()


@pytest.mark.parametrize("missing", ["config", "file"])
def test_shared_python_library_must_be_available(
    synthetic_environment: SyntheticEnvironment, missing: str
) -> None:
    env = synthetic_environment
    env.configuration["Py_ENABLE_SHARED"] = 1
    if missing == "file":
        env.configuration.update(LIBDIR=str(env.root), LDLIBRARY="missing-python.dylib")
    with pytest.raises((ValueError, OSError)):
        environment_identity()


@pytest.mark.parametrize(
    "body",
    [
        b"import tools.missing\n",
        b"from tools import missing\n",
        b"from tools.missing import thing\n",
    ],
)
def test_static_project_closure_rejects_missing_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, body: bytes
) -> None:
    args = project(tmp_path, monkeypatch, {"tools/main.py": body})
    with pytest.raises(ValueError, match="incomplete_project_closure"):
        identity.project_closure(*args)


def test_project_closure_rejects_malformed_ast_safely(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = project(tmp_path, monkeypatch, {"tools/main.py": b"def broken(\n"})
    with pytest.raises(ValueError):
        identity.project_closure(*args)


@pytest.mark.parametrize("field", ["__file__", "spec"])
def test_project_import_origin_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    root, sources, pins = project(tmp_path, monkeypatch, {"tools/main.py": b"pass\n"})
    name = str(root / "tools/main.py")
    foreign = str(root / "foreign.py")
    module = ModuleType("tools.main")
    module.__file__ = foreign if field == "__file__" else name
    module.__spec__ = ModuleSpec(
        "tools.main", loader=None, origin=foreign if field == "spec" else name
    )
    identity.sys.modules["tools.main"] = module
    with pytest.raises(ValueError, match="project_import_origin_mismatch"):
        identity.project_closure(root, sources, pins)


def test_project_closure_enforces_total_read_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = project(tmp_path, monkeypatch, {"tools/a.py": b"pass\n", "tools/b.py": b"pass\n"})
    monkeypatch.setattr(identity, "MAX_TOTAL", 9)
    with pytest.raises(ValueError, match="identity_byte_limit"):
        identity.project_closure(*args)


def test_project_closure_enforces_source_count_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = project(tmp_path, monkeypatch, {"tools/a.py": b"pass\n", "tools/b.py": b"pass\n"})
    monkeypatch.setattr(identity, "MAX_FILES", 2)
    with pytest.raises(ValueError, match="identity_file_limit"):
        identity.project_closure(*args)


def test_project_source_symlink_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, sources, pins = project(tmp_path, monkeypatch, {"tools/main.py": b"pass\n"})
    target = root / "foreign.py"
    target.write_bytes(b"pass\n")
    path = root / "tools/main.py"
    path.unlink()
    symlink_or_skip(path, target)
    with pytest.raises(ValueError, match="unsafe_identity_file"):
        identity.project_closure(root, sources, pins)


def test_project_source_per_file_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = project(tmp_path, monkeypatch, {"tools/main.py": b"pass\n"})
    monkeypatch.setattr(identity, "MAX_FILE", 4)
    with pytest.raises(ValueError, match="identity_byte_limit"):
        identity.project_closure(*args)


def test_unknown_required_dependency_fails_closed(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    synthetic_environment.distributions["attrs"].requires = ["synthetic-unlisted>=1"]
    with pytest.raises(ValueError, match="unsupported_dependency_closure"):
        environment_identity()


def test_missing_required_distribution_fails_closed(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    del synthetic_environment.distributions["attrs"]
    with pytest.raises(ValueError, match="dependency_inventory_unavailable"):
        environment_identity()


def test_oversized_file_rejected_before_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path.resolve() / "large.py"
    path.write_bytes(b"12345")
    monkeypatch.setattr(identity, "MAX_FILE", 4)

    def forbidden_open(*args: object, **kwargs: object) -> None:
        pytest.fail("oversized file must fail before opening")

    monkeypatch.setattr(Path, "open", forbidden_open)
    with pytest.raises(ValueError, match="identity_byte_limit"):
        identity._files([path], path.parent)


@pytest.mark.parametrize(
    ("requirement", "passes"),
    [
        ("typing-extensions>=4", False),
        ('typing-extensions>=4; python_version < "3.13"', True),
        ('typing-extensions>=4; python_version >= "3.13"', False),
    ],
)
def test_missing_typing_extensions_must_honour_active_requirements(
    synthetic_environment: SyntheticEnvironment, requirement: str, passes: bool
) -> None:
    env = synthetic_environment
    del env.distributions["typing-extensions"]
    env.distributions["referencing"].requires = [requirement]
    if passes:
        assert "typing-extensions" not in environment_identity()["distributions"]
    else:
        with pytest.raises(ValueError):
            environment_identity()


@pytest.mark.parametrize("module_name", OPTIONAL_FORMAT_MODULES)
@pytest.mark.parametrize("state", ["loaded", "discoverable"])
def test_optional_format_dependency_rejected_before_enumeration(
    synthetic_environment: SyntheticEnvironment,
    monkeypatch: pytest.MonkeyPatch,
    module_name: str,
    state: str,
) -> None:
    env = synthetic_environment
    if state == "loaded":
        env.runtime.modules[module_name] = ModuleType(module_name)
    else:

        def find_spec(name: str) -> ModuleSpec | None:
            return ModuleSpec(name, loader=None) if name == module_name else None

        monkeypatch.setattr(identity.importlib.util, "find_spec", find_spec)

    def forbidden_walk(*args: object, **kwargs: object) -> None:
        pytest.fail("unsupported optional dependency must fail before stdlib enumeration")

    monkeypatch.setattr(identity.os, "walk", forbidden_walk)
    with pytest.raises(ValueError, match="unsupported_optional_format_dependency"):
        environment_identity()


def test_optional_dependency_discovery_error_fails_closed(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    def unavailable(name: str) -> None:
        raise ValueError("synthetic spec unavailable")

    monkeypatch.setattr(identity.importlib.util, "find_spec", unavailable)
    with pytest.raises(ValueError):
        environment_identity()


def test_project_missing_initializer_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _, pins = project(tmp_path, monkeypatch, {"tools/main.py": b"pass\n"})
    with pytest.raises(ValueError, match="incomplete_project_closure"):
        identity.project_closure(root, ("tools/main.py",), pins)


def test_project_relative_import_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = project(tmp_path, monkeypatch, {"tools/main.py": b"from . import hidden\n"})
    with pytest.raises(ValueError, match="unsupported_relative_project_import"):
        identity.project_closure(*args)


def test_project_changed_source_digest_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, sources, pins = project(tmp_path, monkeypatch, {"tools/main.py": b"pass\n"})
    (root / "tools/main.py").write_bytes(b"pass; pass\n")
    with pytest.raises(ValueError, match="project_source_changed"):
        identity.project_closure(root, sources, pins)


def test_file_count_limit_precedes_file_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(identity, "MAX_FILES", 1)
    with pytest.raises(ValueError, match="identity_file_limit"):
        identity._files([tmp_path / "absent-a", tmp_path / "absent-b"], tmp_path)


def test_stdlib_walk_entry_limit(
    synthetic_environment: SyntheticEnvironment, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(identity, "MAX_FILES", 1)
    with pytest.raises(ValueError, match="identity_file_limit"):
        environment_identity()


def test_distribution_without_file_inventory_rejected(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    synthetic_environment.distributions["attrs"].files = []
    with pytest.raises(ValueError, match="dependency_inventory_unavailable"):
        environment_identity()


def test_distribution_prunes_bytecode_and_console_wrapper_paths(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    env = synthetic_environment
    env.distributions["attrs"].files.extend(
        [Path("__pycache__/attrs.pyc"), Path("attrs.pyc"), Path("../bin/console")]
    )
    records = environment_identity()["distributions"]["attrs"]["files"]
    assert [record["path"] for record in records] == ["attrs.py"]


def test_unknown_optional_extra_not_activated(synthetic_environment: SyntheticEnvironment) -> None:
    synthetic_environment.distributions["attrs"].requires = ['synthetic-optional; extra == "test"']
    assert "attrs" in environment_identity()["distributions"]


def test_python311_active_supported_requirement(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    env = synthetic_environment
    env.runtime.version_info = (3, 11)
    env.distributions["referencing"].requires = ['typing-extensions; python_version < "3.13"']
    assert "typing-extensions" in environment_identity()["distributions"]


def test_unknown_requirement_marker_rejected(synthetic_environment: SyntheticEnvironment) -> None:
    synthetic_environment.distributions["attrs"].requires = ['attrs; sys_platform == "unknown"']
    with pytest.raises(ValueError, match="unsupported_dependency_marker"):
        environment_identity()


def test_shared_python_library_bytes_in_inventory(
    synthetic_environment: SyntheticEnvironment,
) -> None:
    env = synthetic_environment
    library = env.root / "libpython-synthetic.dylib"
    library.write_bytes(b"synthetic-shared-python")
    env.configuration.update(Py_ENABLE_SHARED=1, LIBDIR=str(env.root), LDLIBRARY=library.name)
    records = environment_identity()["interpreter_library"]
    assert records == [
        {
            "path": library.name,
            "bytes": len(b"synthetic-shared-python"),
            "sha256": hashlib.sha256(b"synthetic-shared-python").hexdigest(),
        }
    ]


@pytest.mark.parametrize("module_name", ["attr", "jsonschema.submodule"])
def test_loaded_known_alias_or_submodule_foreign_origin_rejected(
    synthetic_environment: SyntheticEnvironment, module_name: str
) -> None:
    env = synthetic_environment
    foreign = env.root / "foreign-loaded-module.py"
    foreign.write_bytes(b"pass")
    module = ModuleType(module_name)
    module.__file__ = str(foreign)
    module.__spec__ = ModuleSpec(module_name, loader=None, origin=str(foreign))
    env.runtime.modules[module_name] = module
    with pytest.raises(ValueError, match="dependency_import_origin_mismatch"):
        environment_identity()


@pytest.mark.parametrize(
    ("distribution", "module_name", "relative"),
    [
        ("attrs", "attr", "attr.py"),
        ("jsonschema", "jsonschema.submodule", "jsonschema/submodule.py"),
    ],
)
def test_loaded_known_alias_or_submodule_in_inventory_accepted(
    synthetic_environment: SyntheticEnvironment, distribution: str, module_name: str, relative: str
) -> None:
    env = synthetic_environment
    member = Path(relative)
    source = env.packages / member
    source.parent.mkdir(exist_ok=True)
    source.write_bytes(b"pass")
    env.distributions[distribution].files.append(member)
    module = ModuleType(module_name)
    module.__file__ = str(source)
    module.__spec__ = ModuleSpec(module_name, loader=None, origin=str(source))
    env.runtime.modules[module_name] = module
    files = environment_identity()["distributions"][distribution]["files"]
    assert relative in {item["path"] for item in files}
