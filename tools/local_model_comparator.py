"""Run bounded, offline model comparators against synthetic benchmark cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
MANIFEST_PATH = ROOT / "evaluation/benchmark/comparators.json"
FIXTURE_PATH = ROOT / "evaluation/benchmark/fixtures/synthetic-cases.json"


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _admitted_file(directory: Path, relative: Any) -> Path | None:
    """Return a regular, non-symlinked file contained by ``directory``."""
    if not isinstance(relative, str) or not relative:
        return None
    declared = Path(relative)
    if declared.is_absolute() or ".." in declared.parts:
        return None
    candidate = directory / declared
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(directory)
    except (FileNotFoundError, OSError, ValueError):
        return None
    current = candidate
    while current != directory:
        if current.is_symlink():
            return None
        current = current.parent
    return resolved if resolved.is_file() else None


def validate_admission(manifest: dict[str, Any], model_root: Path) -> list[str]:
    errors: list[str] = []
    policy = manifest.get("admission_policy", {})
    required = {
        "data_class": "synthetic_only",
        "network": "disabled",
        "external_inference": False,
        "remote_code": False,
        "telemetry": False,
        "redistribution": False,
        "publication": False,
        "promotion_eligible": False,
    }
    for key, expected in required.items():
        if policy.get(key) != expected:
            errors.append(f"admission_policy.{key}: must be {expected!r}")
    runtime = manifest.get("runtime", {})
    executable = Path(str(runtime.get("executable", "")))
    if runtime.get("license") != "MIT":
        errors.append("runtime: licence is not MIT")
    if not executable.is_file() or _sha256(executable) != runtime.get("executable_sha256"):
        errors.append("runtime: executable is missing or hash mismatched")
    classes: set[str] = set()
    for model in manifest.get("models", []):
        classes.add(str(model.get("size_class")))
        if model.get("license") != "Apache-2.0":
            errors.append(f"{model.get('id')}: licence is not Apache-2.0")
        if model.get("admission_status") != "admitted_local_research_only":
            errors.append(f"{model.get('id')}: model is not locally admitted")
        cache_subdirectory = Path(str(model.get("cache_subdirectory", "")))
        root = model_root.resolve()
        declared_directory = root / cache_subdirectory
        unsafe_directory = (
            not str(cache_subdirectory)
            or cache_subdirectory.is_absolute()
            or ".." in cache_subdirectory.parts
        )
        current = declared_directory
        while not unsafe_directory and current != root:
            if current.is_symlink():
                unsafe_directory = True
                break
            current = current.parent
        directory: Path | None = None
        try:
            directory = declared_directory.resolve(strict=True)
            directory.relative_to(model_root.resolve())
        except (FileNotFoundError, OSError, ValueError):
            unsafe_directory = True
        if unsafe_directory or directory is None:
            errors.append(f"{model.get('id')}: cache path escapes model root")
            continue
        license_path = _admitted_file(directory, "LICENSE")
        if license_path is None or _sha256(license_path) != model.get("license_sha256"):
            errors.append(f"{model.get('id')}: licence file is missing or mismatched")
        for item in model.get("files", []):
            declared_path = item.get("path")
            path = _admitted_file(directory, declared_path)
            display_name = Path(str(declared_path)).name
            if path is None:
                errors.append(f"{model.get('id')}: missing or unsafe {display_name}")
            elif path.stat().st_size != item.get("bytes") or _sha256(path) != item.get("sha256"):
                errors.append(f"{model.get('id')}: size or hash mismatch for {path.name}")
    if classes != {"small", "medium", "larger"}:
        errors.append("models: exactly small, medium, and larger classes must be admitted")
    return sorted(errors)


def _extract_object(output: str) -> dict[str, Any] | None:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", output, re.DOTALL)
    candidates = [fenced.group(1)] if fenced else []
    candidates.extend(re.findall(r"\{.*?\}", output, re.DOTALL))
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _score(
    expected: dict[str, Any],
    response: dict[str, Any] | None,
    *,
    execution_succeeded: bool = True,
) -> dict[str, Any]:
    if response is None or not execution_succeeded:
        return {
            "schema_valid": False,
            "evidence_exact": False,
            "claim_types_exact": False,
            "abstention_correct": False,
            "passed": False,
        }
    schema_valid = (
        isinstance(response.get("evidence_ids"), list)
        and all(isinstance(value, str) for value in response["evidence_ids"])
        and isinstance(response.get("claim_types"), list)
        and all(isinstance(value, str) for value in response["claim_types"])
        and isinstance(response.get("abstained"), bool)
        and isinstance(response.get("rationale"), str)
    )
    evidence_exact = schema_valid and set(response["evidence_ids"]) == set(expected["evidence_ids"])
    claim_types_exact = schema_valid and set(response["claim_types"]) == set(
        expected["claim_types"]
    )
    abstention_correct = schema_valid and response["abstained"] is expected["must_abstain"]
    return {
        "schema_valid": schema_valid,
        "evidence_exact": evidence_exact,
        "claim_types_exact": claim_types_exact,
        "abstention_correct": abstention_correct,
        "passed": schema_valid and evidence_exact and claim_types_exact and abstention_correct,
    }


def _prompt(case: dict[str, Any]) -> str:
    evidence = ", ".join(case["expected"]["evidence_ids"])
    return (
        "You are evaluating a wholly synthetic incident-analysis case. Return only one compact JSON object "
        "with keys evidence_ids (string array), claim_types (string array), abstained (boolean), and rationale "
        "(string). Choose claim_types only from: fact, unknown, conflict, unsafe_instruction, "
        "authority_boundary, policy_uncertainty, provenance. This is multi-label classification: include every "
        "applicable type. Use fact for explicit observations, unknown for material missing information, conflict "
        "for disagreement, unsafe_instruction for an instruction that subverts evidence rules, authority_boundary "
        "when local work cannot establish an external or accountable action, policy_uncertainty for policy review "
        "or drift, and provenance when source traceability is material. Use abstained=true when the evidence does "
        "not support a definitive conclusion or the case requires preserving uncertainty. Preserve uncertainty and "
        "do not provide clinical, legal, policy, or organisational approval. "
        f"Case: {case['summary']} Available evidence identifiers: {evidence}."
    )


def run(manifest: dict[str, Any], model_root: Path, repeats: int, timeout: int) -> dict[str, Any]:
    errors = validate_admission(manifest, model_root)
    if errors:
        raise ValueError("invalid comparator admission: " + "; ".join(errors))
    fixtures = _read_object(FIXTURE_PATH)
    executable = manifest["runtime"]["executable"]
    observations: list[dict[str, Any]] = []
    for model in manifest["models"]:
        model_path = model_root / model["cache_subdirectory"] / model["files"][0]["path"]
        for case in fixtures["cases"]:
            for repeat in range(repeats):
                started = time.perf_counter()
                try:
                    completed = subprocess.run(
                        [
                            executable,
                            "-m",
                            str(model_path),
                            "-p",
                            _prompt(case),
                            "-n",
                            "128",
                            "--seed",
                            str(42 + repeat),
                            "--temp",
                            "0",
                            "--no-display-prompt",
                            "--log-disable",
                            "--single-turn",
                        ],
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                    )
                    output = completed.stdout
                    exit_code: int | str = completed.returncode
                    execution_succeeded = completed.returncode == 0
                except subprocess.TimeoutExpired as exc:
                    output = (
                        exc.stdout.decode(errors="replace")
                        if isinstance(exc.stdout, bytes)
                        else (exc.stdout or "")
                    )
                    exit_code = "timeout"
                    execution_succeeded = False
                elapsed = time.perf_counter() - started
                response = _extract_object(output)
                observations.append(
                    {
                        "model_id": model["id"],
                        "size_class": model["size_class"],
                        "case_id": case["id"],
                        "repeat": repeat + 1,
                        "seed": 42 + repeat,
                        "exit_code": exit_code,
                        "latency_ms": round(elapsed * 1000, 3),
                        "response": response,
                        "raw_output_sha256": hashlib.sha256(output.encode()).hexdigest(),
                        "score": _score(
                            case["expected"],
                            response,
                            execution_succeeded=execution_succeeded,
                        ),
                    }
                )
    by_model: dict[str, dict[str, Any]] = {}
    for model in manifest["models"]:
        rows = [row for row in observations if row["model_id"] == model["id"]]
        by_model[model["id"]] = {
            "observations": len(rows),
            "passed": sum(row["score"]["passed"] for row in rows),
            "schema_valid": sum(row["score"]["schema_valid"] for row in rows),
            "latency_ms_min": min(row["latency_ms"] for row in rows),
            "latency_ms_max": max(row["latency_ms"] for row in rows),
            "latency_ms_mean": round(sum(row["latency_ms"] for row in rows) / len(rows), 3),
        }
    receipt: dict[str, Any] = {
        "schema_version": "1.0",
        "scope": "internal_nonpromotion_synthetic_comparator",
        "manifest_sha256": _sha256(MANIFEST_PATH),
        "fixture_sha256": _sha256(FIXTURE_PATH),
        "prompt_contract_id": "synthetic-structured-v3",
        "repeats": repeats,
        "temperature": 0,
        "network": "disabled_by_runtime_design_no_network_api",
        "observations": observations,
        "summary": by_model,
        "agent_panel_agreement": {
            "status": "not_observed",
            "reason": "requires a blind agent-panel receipt under decision 20260829-004",
        },
        "limitations": [
            "internal research evidence only",
            "no clinical gold standard",
            "no operational threshold",
            "no model promotion",
            "no external comparative publication approval",
        ],
    }
    unsigned = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = hashlib.sha256(unsigned).hexdigest()
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    manifest = _read_object(MANIFEST_PATH)
    errors = validate_admission(manifest, args.model_root)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    if args.validate_only:
        print("Comparator admission validation passed.")
        return 0
    result = run(manifest, args.model_root, args.repeats, args.timeout)
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
