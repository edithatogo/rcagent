"""Small fail-closed adapters for upstream typing and mutation reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from tools.evidence_core import fingerprint

ROOT = Path(__file__).parents[1]
BASELINE = ".basedpyright/baseline.json"
BUDGET = "quality/typing-debt.json"
BANDIT_BASELINE = "quality/bandit-reviewed.json"
BANDIT_BASELINE_SHA256 = "550bd037fc3580d1081f294bf50f06ecb36fd83859c4ec68e55717a32b78e647"
FROZEN_SCAN_SOURCES = ("tools/darwin_runtime_profile.py", "tools/local_model_comparator.py")
MUTATION_TARGET = "tools/release_admission.py"
STATUSES = ("zapped", "survived", "timeout", "error", "pardoned")
PROFILE_TARGET = "tools/profile_workload.py"
PROFILE_SOURCE = "tools/evidence_core.py"
PROFILE_FIXTURE = "tests/fixtures/safety-work/valid-case.json"
PROFILE_ITERATIONS = 300
PROFILE_WORKLOAD = "schema-validation-and-provenance-round-trip"


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast("dict[str, object]", value)


def _array(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return cast("list[object]", value)


def _count(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def baseline_counts(value: object) -> Counter[str]:
    """Count the upstream baseline by file/rule, independent of line movement."""
    files = _object(_object(value, "baseline").get("files"), "baseline files")
    result: Counter[str] = Counter()
    for name, entries in files.items():
        name = Path(name).as_posix()
        if not name.startswith(("tools/", "tests/")) or ".." in Path(name).parts:
            raise ValueError("baseline contains a path outside tools/tests")
        for raw in _array(entries, "baseline entries"):
            entry = _object(raw, "baseline entry")
            code = entry.get("code")
            if not isinstance(code, str) or not code.startswith("report"):
                raise ValueError("baseline contains an invalid diagnostic code")
            result[f"{name}:{code}"] += 1
    return result


def check_baseline(root: Path, *, base: str | None = None) -> int:
    """Refuse new baseline files/rules/counts; compare the PR base when supplied."""
    current = baseline_counts(json.loads((root / BASELINE).read_text(encoding="utf-8")))
    policy = _object(json.loads((root / BUDGET).read_text(encoding="utf-8")), "typing policy")
    limits = _object(policy.get("limits"), "typing limits")
    caps = Counter({key: _count(value, key) for key, value in limits.items()})
    if current - caps:
        raise ValueError("strict typing baseline exceeds its measured legacy budget")
    if base:
        if not re.fullmatch(r"[0-9a-f]{40}", base):
            raise ValueError("baseline comparison requires a full commit SHA")
        result = subprocess.run(  # nosec B603, B607 # trusted read-only Git; SHA is validated
            ["git", "show", f"{base}:{BASELINE}"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode:
            # The one initial rollout has no baseline in its parent commit.
            if base != policy.get("origin_commit"):
                raise ValueError("could not read the comparison baseline")
        else:
            previous = baseline_counts(json.loads(result.stdout))
            if current - previous:
                raise ValueError("strict typing baseline grows relative to the comparison commit")
    return current.total()


def check_mutation_report(value: object, *, root: Path) -> tuple[int, int]:
    """Require every reported mutant to be killed without timeouts or pardons.

    pytest-gremlins itself does not fail CI for surviving mutants. Its percentage
    also counts timeouts as kills, so independently validate the raw verdicts.
    """
    report = _object(value, "mutation report")
    summary = _object(report.get("summary"), "mutation summary")
    counts = {name: _count(summary.get(name), name) for name in STATUSES}
    total = _count(summary.get("total"), "total")
    if total == 0 or total != sum(counts.values()):
        raise ValueError("mutation totals are empty or inconsistent")
    if report.get("skipped_files") or report.get("timeout_warning"):
        raise ValueError("mutation instrumentation or timeout warning")
    expected = (root / MUTATION_TARGET).resolve()
    files = _object(report.get("files"), "mutation files")
    if len(files) != 1 or Path(next(iter(files))).resolve() != expected:
        raise ValueError("mutation scope differs from the required release boundary")
    entries = _array(report.get("results"), "mutation results")
    observed: Counter[str] = Counter()
    identifiers: set[str] = set()
    for raw in entries:
        entry = _object(raw, "mutation result")
        status, identifier, path = (
            entry.get("status"),
            entry.get("gremlin_id"),
            entry.get("file_path"),
        )
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError("unknown mutation verdict")
        if not isinstance(identifier, str) or not identifier or identifier in identifiers:
            raise ValueError("mutation identities are missing or duplicated")
        if not isinstance(path, str) or Path(path).resolve() != expected:
            raise ValueError("mutation result is outside the required scope")
        identifiers.add(identifier)
        observed[status] += 1
    if len(entries) != total or any(observed[name] != count for name, count in counts.items()):
        raise ValueError("mutation summary does not match the individual verdicts")
    if counts["zapped"] != total:
        raise ValueError(
            "release boundary requires 100% killed mutants with no survivors, timeouts, "
            "errors or pardons"
        )
    return counts["zapped"], total


def check_security_baseline(root: Path) -> None:
    """Bind two native Bandit exceptions to reviewed, historically frozen bytes.

    Bandit's baseline matching does not compare source text or line numbers.
    Refuse any baseline/source drift before using those narrow exceptions.
    """
    payload = (root / BANDIT_BASELINE).read_bytes()
    if hashlib.sha256(payload).hexdigest() != BANDIT_BASELINE_SHA256:
        raise ValueError("reviewed Bandit baseline changed; revalidation required")
    baseline = _object(json.loads(payload), "Bandit baseline")
    review = _object(baseline.get("review"), "Bandit review")
    sources = _object(review.get("sources"), "reviewed sources")
    for name in FROZEN_SCAN_SOURCES:
        record = _object(sources.get(name), "reviewed source")
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != record.get("sha256"):
            raise ValueError(f"reviewed Bandit source changed; revalidation required: {name}")


def run_security_scan(root: Path) -> int:
    """Run Bandit after fixity checks, adapting only native filename separators."""
    check_security_baseline(root)
    baseline = _object(
        json.loads((root / BANDIT_BASELINE).read_text(encoding="utf-8")), "Bandit baseline"
    )
    # Bandit matches filename strings literally and uses os.path.join during
    # discovery. Keep the reviewed source/report bytes fixed while making the
    # same two exceptions usable on Windows as well as POSIX.
    for raw in _array(baseline.get("results"), "Bandit findings"):
        finding = _object(raw, "Bandit finding")
        filename = finding.get("filename")
        if not isinstance(filename, str) or filename not in FROZEN_SCAN_SOURCES:
            raise ValueError("Bandit exception is outside the reviewed source scope")
        finding["filename"] = str(Path(filename))
    with TemporaryDirectory(prefix="rcagent-bandit-") as directory:
        native_baseline = Path(directory) / "reviewed.json"
        native_baseline.write_text(json.dumps(baseline), encoding="utf-8")
        result = subprocess.run(  # nosec B603 # fixed interpreter/module/argv; hash-verified baseline; no shell
            [
                sys.executable,
                "-m",
                "bandit",
                "-r",
                "tools",
                "-c",
                "pyproject.toml",
                "--baseline",
                str(native_baseline),
                "-q",
            ],
            cwd=root,
            check=False,
            timeout=180,
        )
    return result.returncode


def _measurement(value: object, label: str, *, positive: bool = False) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
        or (positive and value == 0)
    ):
        raise ValueError(f"{label} measurement is invalid or missing")
    return float(value)


def _profile_path(value: object, root: Path) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("profile source path is invalid or missing")
    path = Path(value)
    return (path if path.is_absolute() else root / path).resolve()


def check_profile_report(value: object, *, workload: object, root: Path) -> tuple[float, float]:
    """Require measured production code and a completed, fixture-bound workload."""
    report = _object(value, "Scalene report")
    files = _object(report.get("files"), "profile files")
    if report.get("memory") is not True or not files:
        raise ValueError("Scalene must collect memory and non-empty file measurements")
    elapsed = _measurement(report.get("elapsed_time_sec"), "elapsed time", positive=True)
    footprint = _measurement(report.get("max_footprint_mb"), "allocation footprint")
    if _count(report.get("alloc_samples"), "allocation samples") == 0:
        raise ValueError("Scalene allocation samples are missing")
    if _profile_path(report.get("program"), root) != (root / PROFILE_TARGET).resolve():
        raise ValueError("profile program differs from the required synthetic workload")
    measured = {
        _profile_path(name, root): _object(data, "profile file measurements")
        for name, data in files.items()
    }
    source = _object(measured.get((root / PROFILE_SOURCE).resolve()), "evidence-core CPU profile")
    if _measurement(source.get("percent_cpu_time"), "evidence-core CPU", positive=True) > 100:
        raise ValueError("evidence-core CPU percentage exceeds 100")
    cpu_total = 0.0
    cpu_samples = 0
    for raw in _array(source.get("lines"), "CPU profile lines"):
        line = _object(raw, "CPU profile line")
        for field in ("n_cpu_percent_python", "n_cpu_percent_c", "n_sys_percent"):
            percent = _measurement(line.get(field), field)
            if percent > 100:
                raise ValueError("CPU percentage exceeds 100")
            cpu_total += percent
        for sample in _array(line.get("cpu_samples_list"), "CPU samples"):
            _measurement(sample, "CPU sample timestamp")
            cpu_samples += 1
    if cpu_total <= 0 or cpu_samples == 0:
        raise ValueError("evidence-core CPU samples are missing")

    receipt = _object(workload, "completed workload receipt")
    if (
        receipt.get("schema_version") != "1.0"
        or receipt.get("data_class") != "synthetic"
        or receipt.get("workload") != PROFILE_WORKLOAD
        or _count(receipt.get("iterations"), "workload iterations") != PROFILE_ITERATIONS
    ):
        raise ValueError("completed workload receipt has an invalid schema or scope")
    _measurement(receipt.get("wall_seconds"), "workload wall time", positive=True)
    fixture = _object(
        json.loads((root / PROFILE_FIXTURE).read_text(encoding="utf-8")), "profile fixture"
    )
    if receipt.get("fixture_sha256") != fingerprint(fixture):
        raise ValueError("completed workload receipt does not match the current synthetic fixture")
    return elapsed, footprint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    baseline = commands.add_parser("baseline")
    baseline.add_argument("--base", help="Full PR base or previous master commit SHA")
    commands.add_parser("security-baseline")
    commands.add_parser("security")
    mutation = commands.add_parser("mutation")
    mutation.add_argument("report", type=Path)
    profile = commands.add_parser("profile")
    profile.add_argument("report", type=Path)
    profile.add_argument(
        "--workload", required=True, type=Path, help="Completed workload JSON receipt"
    )
    args = parser.parse_args()
    try:
        if args.command == "baseline":
            count = check_baseline(ROOT, base=args.base)
            print(
                f"Strict typing: {count} explicitly baselined legacy diagnostics; no budget growth"
            )
        elif args.command == "security-baseline":
            check_security_baseline(ROOT)
            print("Bandit exceptions: exactly two reviewed findings bound to frozen source bytes")
        elif args.command == "security":
            return run_security_scan(ROOT)
        elif args.command == "mutation":
            report = json.loads(Path(args.report).read_text(encoding="utf-8"))
            killed, total = check_mutation_report(report, root=ROOT)
            print(f"Mutation gate: {killed}/{total} killed (100%); no excluded verdicts")
        else:
            report = json.loads(Path(args.report).read_text(encoding="utf-8"))
            workload = json.loads(Path(args.workload).read_text(encoding="utf-8"))
            elapsed, footprint = check_profile_report(report, workload=workload, root=ROOT)
            print(
                f"Scalene measurement: {PROFILE_ITERATIONS} completed synthetic round-trips; "
                f"{elapsed:.3f}s; reported allocation footprint {footprint:.3f} MB"
            )
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
