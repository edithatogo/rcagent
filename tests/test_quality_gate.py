"""Adversarial tests for assurance reports that must not manufacture a green gate."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tools import profile_workload, quality_gate
from tools.evidence_core import fingerprint


def mutation_report(root: Path, statuses: list[str]) -> dict[str, object]:
    path = str(root / quality_gate.MUTATION_TARGET)
    counts = Counter(statuses)
    return {
        "summary": {"total": len(statuses), **dict.fromkeys(quality_gate.STATUSES, 0), **counts},
        "files": {path: {"total": len(statuses)}},
        "results": [
            {"gremlin_id": f"g{index}", "status": status, "file_path": path}
            for index, status in enumerate(statuses)
        ],
    }


@given(st.lists(st.sampled_from(quality_gate.STATUSES), min_size=1, max_size=40))
def test_mutation_gate_accepts_only_real_kills(statuses: list[str]) -> None:
    root = Path.cwd()
    report = mutation_report(root, statuses)
    if set(statuses) == {"zapped"}:
        assert quality_gate.check_mutation_report(report, root=root) == (
            len(statuses),
            len(statuses),
        )
    else:
        with pytest.raises(ValueError, match="100% killed"):
            quality_gate.check_mutation_report(report, root=root)


@pytest.mark.parametrize("bad", [None, [], 0, True, "100%"])
def test_missing_or_wrong_report_structure_is_not_success(bad: object) -> None:
    with pytest.raises(ValueError, match="must be an object"):
        quality_gate.check_mutation_report(bad, root=Path.cwd())


@pytest.mark.parametrize("flag", ["skipped_files", "timeout_warning"])
def test_incomplete_mutation_instrumentation_fails(flag: str) -> None:
    report = mutation_report(Path.cwd(), ["zapped"])
    report[flag] = {"reason": "instrumentation unavailable"}
    with pytest.raises(ValueError, match="instrumentation or timeout"):
        quality_gate.check_mutation_report(report, root=Path.cwd())


def test_empty_mutation_run_cannot_claim_100_percent() -> None:
    with pytest.raises(ValueError, match="empty or inconsistent"):
        quality_gate.check_mutation_report(mutation_report(Path.cwd(), []), root=Path.cwd())


def test_summary_cannot_replace_or_hide_individual_results() -> None:
    report = mutation_report(Path.cwd(), ["zapped"])
    report["results"] = []
    with pytest.raises(ValueError, match="does not match"):
        quality_gate.check_mutation_report(report, root=Path.cwd())


def test_unrelated_mutation_target_cannot_satisfy_release_gate() -> None:
    report = mutation_report(Path.cwd(), ["zapped"])
    report["files"] = {str(Path.cwd() / "tools/unrelated.py"): {"total": 1}}
    with pytest.raises(ValueError, match="scope differs"):
        quality_gate.check_mutation_report(report, root=Path.cwd())


def test_duplicate_mutants_cannot_inflate_score() -> None:
    root = Path.cwd()
    report = mutation_report(root, ["zapped", "zapped"])
    result = {
        "gremlin_id": "same",
        "status": "zapped",
        "file_path": str(root / quality_gate.MUTATION_TARGET),
    }
    report["results"] = [result, result]
    with pytest.raises(ValueError, match="duplicated"):
        quality_gate.check_mutation_report(report, root=root)


def test_baseline_budget_rejects_new_files_and_diagnostic_growth(tmp_path: Path) -> None:
    (tmp_path / ".basedpyright").mkdir()
    (tmp_path / "quality").mkdir()
    baseline = {"files": {"./tools/legacy.py": [{"code": "reportUnknownVariableType"}]}}
    (tmp_path / quality_gate.BASELINE).write_text(json.dumps(baseline))
    policy = {"limits": {"tools/legacy.py:reportUnknownVariableType": 1}}
    (tmp_path / quality_gate.BUDGET).write_text(json.dumps(policy))
    assert quality_gate.check_baseline(tmp_path) == 1
    baseline["files"]["./tools/new.py"] = [{"code": "reportUnknownVariableType"}]
    (tmp_path / quality_gate.BASELINE).write_text(json.dumps(baseline))
    with pytest.raises(ValueError, match="exceeds"):
        quality_gate.check_baseline(tmp_path)


def test_typing_comparison_rejects_non_commit_input(tmp_path: Path) -> None:
    (tmp_path / ".basedpyright").mkdir()
    (tmp_path / "quality").mkdir()
    (tmp_path / quality_gate.BASELINE).write_text('{"files": {}}')
    (tmp_path / quality_gate.BUDGET).write_text('{"limits": {}}')
    with pytest.raises(ValueError, match="full commit SHA"):
        quality_gate.check_baseline(tmp_path, base="--exec=untrusted")


def test_profile_runs_actual_validated_synthetic_round_trip(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(profile_workload, "ITERATIONS", 1)
    result = profile_workload.run_workload()
    assert result["schema_version"] == "1.0"
    assert result["data_class"] == "synthetic"
    assert result["iterations"] == 1
    assert str(result["fixture_sha256"]).startswith("sha256:")


def profile_report(root: Path, *, source: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "program": str(root / quality_gate.PROFILE_TARGET),
        "memory": True,
        "files": {
            str(root / quality_gate.PROFILE_SOURCE): (
                source
                if source is not None
                else {
                    "percent_cpu_time": 99.0,
                    "lines": [
                        {
                            "n_cpu_percent_python": 90.0,
                            "n_cpu_percent_c": 8.0,
                            "n_sys_percent": 1.0,
                            "cpu_samples_list": [0.1],
                        }
                    ],
                }
            )
        },
        "elapsed_time_sec": 2.0,
        "max_footprint_mb": 1.0,
        "alloc_samples": 1,
    }


def profile_receipt(root: Path) -> dict[str, object]:
    fixture: object = json.loads((root / quality_gate.PROFILE_FIXTURE).read_text())
    return {
        "schema_version": "1.0",
        "data_class": "synthetic",
        "workload": "schema-validation-and-provenance-round-trip",
        "iterations": 300,
        "wall_seconds": 1.9,
        "fixture_sha256": fingerprint(fixture),
    }


def test_profile_gate_accepts_measured_completed_workload() -> None:
    root = quality_gate.ROOT
    assert quality_gate.check_profile_report(
        profile_report(root), workload=profile_receipt(root), root=root
    ) == (2.0, 1.0)


@pytest.mark.parametrize("elapsed", [None, 0, -1, float("nan"), float("inf"), True, "1"])
def test_profile_rejects_missing_or_invalid_measurements(elapsed: object) -> None:
    root = quality_gate.ROOT
    report = profile_report(root)
    report["elapsed_time_sec"] = elapsed
    with pytest.raises(ValueError, match="measurement is invalid"):
        quality_gate.check_profile_report(report, workload=profile_receipt(root), root=root)


def test_cpu_only_profile_cannot_claim_memory_measurement() -> None:
    with pytest.raises(ValueError, match="must collect memory"):
        quality_gate.check_profile_report(
            {"memory": False, "files": {}}, workload={}, root=quality_gate.ROOT
        )


@pytest.mark.parametrize("program", [None, "", "tools/unrelated.py", True])
def test_unrelated_or_missing_profile_program_is_rejected(program: object) -> None:
    root = quality_gate.ROOT
    report = profile_report(root)
    report["program"] = program
    with pytest.raises(ValueError, match=r"profile (source path|program)"):
        quality_gate.check_profile_report(report, workload=profile_receipt(root), root=root)


def test_profile_of_unrelated_code_cannot_satisfy_workload_gate() -> None:
    root = quality_gate.ROOT
    report = profile_report(root)
    report["files"] = {str(root / "tools/unrelated.py"): {}}
    with pytest.raises(ValueError, match="evidence-core CPU profile"):
        quality_gate.check_profile_report(report, workload=profile_receipt(root), root=root)


@pytest.mark.parametrize(
    ("cpu", "samples"),
    [
        (0, []),
        (0, [0.1]),
        (5, []),
        (float("nan"), [0.1]),
        (101, [0.1]),
        (True, [0.1]),
        (5, [float("inf")]),
        (5, [True]),
    ],
)
def test_empty_or_invalid_cpu_line_samples_fail(cpu: object, samples: list[object]) -> None:
    root = quality_gate.ROOT
    source: dict[str, object] = {
        "percent_cpu_time": 99.0,
        "lines": [
            {
                "n_cpu_percent_python": cpu,
                "n_cpu_percent_c": 0,
                "n_sys_percent": 0,
                "cpu_samples_list": samples,
            }
        ],
    }
    with pytest.raises(ValueError, match=r"(CPU|n_cpu_percent_python)"):
        quality_gate.check_profile_report(
            profile_report(root, source=source), workload=profile_receipt(root), root=root
        )


@pytest.mark.parametrize(
    "source", [{}, {"percent_cpu_time": 1, "lines": []}, {"percent_cpu_time": 101, "lines": []}]
)
def test_nonempty_profile_file_without_measurements_is_not_success(
    source: dict[str, object],
) -> None:
    root = quality_gate.ROOT
    with pytest.raises(ValueError, match=r"(evidence-core CPU|CPU samples)"):
        quality_gate.check_profile_report(
            profile_report(root, source=source), workload=profile_receipt(root), root=root
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", None),
        ("schema_version", "2.0"),
        ("data_class", "private"),
        ("workload", "unrelated"),
        ("iterations", 0),
        ("iterations", 299),
        ("iterations", True),
        ("wall_seconds", 0),
        ("wall_seconds", float("nan")),
        ("wall_seconds", True),
        ("fixture_sha256", "sha256:" + "0" * 64),
    ],
)
def test_incomplete_or_unrelated_workload_receipt_fails(field: str, value: object) -> None:
    root = quality_gate.ROOT
    receipt = profile_receipt(root)
    receipt[field] = value
    with pytest.raises(ValueError, match=r"(workload|synthetic fixture)"):
        quality_gate.check_profile_report(profile_report(root), workload=receipt, root=root)


@pytest.mark.parametrize("receipt", [None, {}, [], "completed"])
def test_missing_completed_workload_receipt_fails(receipt: object) -> None:
    root = quality_gate.ROOT
    with pytest.raises(ValueError, match="completed workload receipt"):
        quality_gate.check_profile_report(profile_report(root), workload=receipt, root=root)


def test_workload_receipt_cannot_be_reused_after_fixture_changes(tmp_path: Path) -> None:
    fixture = tmp_path / quality_gate.PROFILE_FIXTURE
    fixture.parent.mkdir(parents=True)
    fixture.write_bytes((quality_gate.ROOT / quality_gate.PROFILE_FIXTURE).read_bytes())
    receipt = profile_receipt(tmp_path)
    fixture.write_text('{"synthetic": "changed fixture"}')
    with pytest.raises(ValueError, match="current synthetic fixture"):
        quality_gate.check_profile_report(profile_report(tmp_path), workload=receipt, root=tmp_path)


def test_reviewed_bandit_exceptions_match_frozen_sources() -> None:
    quality_gate.check_security_baseline(quality_gate.ROOT)


def test_bandit_baseline_change_requires_revalidation(tmp_path: Path) -> None:
    (tmp_path / "quality").mkdir()
    (tmp_path / quality_gate.BANDIT_BASELINE).write_text('{"results": []}')
    with pytest.raises(ValueError, match="baseline changed"):
        quality_gate.check_security_baseline(tmp_path)


@pytest.mark.parametrize("changed", quality_gate.REVIEWED_SCAN_SOURCES)
def test_bandit_source_change_cannot_reuse_older_exception(tmp_path: Path, changed: str) -> None:
    (tmp_path / "quality").mkdir()
    (tmp_path / "tools").mkdir()
    for name in (quality_gate.BANDIT_BASELINE, *quality_gate.REVIEWED_SCAN_SOURCES):
        (tmp_path / name).write_bytes((quality_gate.ROOT / name).read_bytes())
    with (tmp_path / changed).open("ab") as stream:
        stream.write(b"\n# changed source cannot silently inherit an exception\n")
    with pytest.raises(ValueError, match="source changed"):
        quality_gate.check_security_baseline(tmp_path)


@pytest.mark.parametrize("exit_code", [0, 1, 2])
def test_bandit_adapter_preserves_review_and_propagates_exit(
    monkeypatch: pytest.MonkeyPatch, exit_code: int
) -> None:
    captured: list[Path] = []

    def scan(
        command: list[str], *, cwd: Path, check: bool, timeout: int
    ) -> subprocess.CompletedProcess[str]:
        assert command[:3] == [sys.executable, "-m", "bandit"]
        assert cwd == quality_gate.ROOT
        assert check is False
        assert timeout == 180
        path = Path(command[command.index("--baseline") + 1])
        captured.append(path)
        original = cast(
            "dict[str, object]",
            json.loads((cwd / quality_gate.BANDIT_BASELINE).read_text()),
        )
        native = cast("dict[str, object]", json.loads(path.read_text()))
        original_findings = cast("list[dict[str, object]]", original["results"])
        for finding in original_findings:
            finding["filename"] = str(Path(str(finding["filename"])))
        assert native == original
        return subprocess.CompletedProcess(command, exit_code)

    monkeypatch.setattr(quality_gate.subprocess, "run", scan)
    assert quality_gate.run_security_scan(quality_gate.ROOT) == exit_code
    assert len(captured) == 1
    assert not captured[0].exists()


def test_bandit_scan_is_never_started_for_unreviewed_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "quality").mkdir()
    (tmp_path / quality_gate.BANDIT_BASELINE).write_text('{"results": []}')

    def forbidden_scan(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        pytest.fail("unreviewed exceptions must fail before starting the scanner")

    monkeypatch.setattr(quality_gate.subprocess, "run", forbidden_scan)
    with pytest.raises(ValueError, match="baseline changed"):
        quality_gate.run_security_scan(tmp_path)
