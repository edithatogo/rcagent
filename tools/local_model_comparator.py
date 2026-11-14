"""Run bounded, offline model comparators against synthetic benchmark cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from collections.abc import Mapping
from pathlib import Path
from typing import TypedDict, TypeGuard

from tools import json_shapes

# These two compatibility names are already shared by the admission modules.
# Their contracts inspect bytes and paths only; they confer no execution authority.
__all__ = [
    "ComparatorReceipt",
    "ModelSummary",
    "Observation",
    "Score",
    "_admitted_file",
    "_sha256",
    "build_prompt",
    "extract_response",
    "main",
    "read_object",
    "run",
    "score_response",
    "validate_admission",
]

ROOT = Path(__file__).parents[1]
MANIFEST_PATH = ROOT / "evaluation/benchmark/comparators.json"
FIXTURE_PATH = ROOT / "evaluation/benchmark/fixtures/synthetic-cases.json"


class Score(TypedDict):
    schema_valid: bool
    evidence_exact: bool
    claim_types_exact: bool
    abstention_correct: bool
    passed: bool


class Observation(TypedDict):
    model_id: str
    size_class: str
    case_id: str
    repeat: int
    seed: int
    exit_code: int | str
    latency_ms: float
    response: json_shapes.JsonObject | None
    raw_output_sha256: str
    score: Score


class ModelSummary(TypedDict):
    observations: int
    passed: int
    schema_valid: int
    latency_ms_min: float
    latency_ms_max: float
    latency_ms_mean: float


class _ReceiptFields(TypedDict):
    schema_version: str
    scope: str
    manifest_sha256: str
    fixture_sha256: str
    prompt_contract_id: str
    repeats: int
    temperature: int
    network: str
    observations: list[Observation]
    summary: dict[str, ModelSummary]
    agent_panel_agreement: dict[str, str]
    limitations: list[str]


class ComparatorReceipt(_ReceiptFields):
    receipt_sha256: str


def _strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context}: expected a nonempty string")
    return value


def _objects(value: object, context: str) -> list[json_shapes.JsonObject]:
    if not json_shapes.is_array(value) or not all(json_shapes.is_object(item) for item in value):
        raise ValueError(f"{context}: expected an array of objects")
    return [json_shapes.require_object(item, context=context) for item in value]


def read_object(path: Path) -> json_shapes.JsonObject:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not json_shapes.is_object(value):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _admitted_file(directory: Path, relative: object) -> Path | None:
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


def validate_admission(manifest: Mapping[str, object], model_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        policy = json_shapes.require_object(
            manifest.get("admission_policy", {}), context="admission_policy"
        )
        runtime = json_shapes.require_object(manifest.get("runtime", {}), context="runtime")
        models = _objects(manifest.get("models", []), "models")
    except ValueError as exc:
        return [str(exc)]
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
    executable = Path(str(runtime.get("executable", "")))
    if runtime.get("license") != "MIT":
        errors.append("runtime: licence is not MIT")
    if not executable.is_file() or _sha256(executable) != runtime.get("executable_sha256"):
        errors.append("runtime: executable is missing or hash mismatched")
    classes: set[str] = set()
    for model in models:
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
        try:
            files = _objects(model.get("files", []), "model.files")
        except ValueError as exc:
            errors.append(f"{model.get('id')}: {exc}")
            continue
        for item in files:
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


def extract_response(output: str) -> json_shapes.JsonObject | None:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", output, re.DOTALL)
    candidates = [fenced.group(1)] if fenced else []
    candidates.extend(re.findall(r"\{.*?\}", output, re.DOTALL))
    for candidate in candidates:
        try:
            value: object = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if json_shapes.is_object(value):
            return value
    return None


def score_response(
    expected: Mapping[str, object],
    response: Mapping[str, object] | None,
    *,
    execution_succeeded: bool = True,
) -> Score:
    if response is None or not execution_succeeded:
        return {
            "schema_valid": False,
            "evidence_exact": False,
            "claim_types_exact": False,
            "abstention_correct": False,
            "passed": False,
        }
    evidence_ids = response.get("evidence_ids")
    claim_types = response.get("claim_types")
    expected_evidence = expected.get("evidence_ids")
    expected_claims = expected.get("claim_types")
    if not _strings(expected_evidence) or not _strings(expected_claims):
        raise ValueError("expected evidence_ids and claim_types must be string arrays")
    schema_valid = (
        _strings(evidence_ids)
        and _strings(claim_types)
        and isinstance(response.get("abstained"), bool)
        and isinstance(response.get("rationale"), str)
    )
    evidence_exact = (
        schema_valid and _strings(evidence_ids) and set(evidence_ids) == set(expected_evidence)
    )
    claim_types_exact = (
        schema_valid and _strings(claim_types) and set(claim_types) == set(expected_claims)
    )
    abstention_correct = schema_valid and response["abstained"] is expected["must_abstain"]
    return {
        "schema_valid": schema_valid,
        "evidence_exact": evidence_exact,
        "claim_types_exact": claim_types_exact,
        "abstention_correct": abstention_correct,
        "passed": schema_valid and evidence_exact and claim_types_exact and abstention_correct,
    }


def build_prompt(case: Mapping[str, object]) -> str:
    expected = json_shapes.require_object(case.get("expected"), context="case.expected")
    evidence_ids = expected.get("evidence_ids")
    if not _strings(evidence_ids):
        raise ValueError("case.expected.evidence_ids must be a string array")
    evidence = ", ".join(evidence_ids)
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


def run(
    manifest: Mapping[str, object], model_root: Path, repeats: int, timeout: int
) -> ComparatorReceipt:
    errors = validate_admission(manifest, model_root)
    if errors:
        raise ValueError("invalid comparator admission: " + "; ".join(errors))
    if repeats < 1 or timeout < 1:
        raise ValueError("repeats and timeout must be positive")
    fixtures = read_object(FIXTURE_PATH)
    runtime = json_shapes.require_object(manifest.get("runtime"), context="runtime")
    executable = _string(runtime.get("executable"), "runtime.executable")
    models = _objects(manifest.get("models"), "models")
    cases = _objects(fixtures.get("cases"), "cases")
    observations: list[Observation] = []
    for model in models:
        model_id = _string(model.get("id"), "model.id")
        size_class = _string(model.get("size_class"), "model.size_class")
        files = _objects(model.get("files"), "model.files")
        if not files:
            raise ValueError("model.files must not be empty")
        model_path = (
            model_root
            / _string(model.get("cache_subdirectory"), "model.cache_subdirectory")
            / _string(files[0].get("path"), "model.files.path")
        )
        for case in cases:
            case_id = _string(case.get("id"), "case.id")
            expected = json_shapes.require_object(case.get("expected"), context="case.expected")
            if (
                not _strings(expected.get("evidence_ids"))
                or not _strings(expected.get("claim_types"))
                or not isinstance(expected.get("must_abstain"), bool)
            ):
                raise ValueError("case.expected has invalid scoring fields")
            _string(case.get("summary"), "case.summary")
            prompt = build_prompt(case)
            for repeat in range(repeats):
                started = time.perf_counter()
                try:
                    completed = subprocess.run(
                        [
                            executable,
                            "-m",
                            str(model_path),
                            "-p",
                            prompt,
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
                response = extract_response(output)
                observations.append(
                    {
                        "model_id": model_id,
                        "size_class": size_class,
                        "case_id": case_id,
                        "repeat": repeat + 1,
                        "seed": 42 + repeat,
                        "exit_code": exit_code,
                        "latency_ms": round(elapsed * 1000, 3),
                        "response": response,
                        "raw_output_sha256": hashlib.sha256(output.encode()).hexdigest(),
                        "score": score_response(
                            expected,
                            response,
                            execution_succeeded=execution_succeeded,
                        ),
                    }
                )
    by_model: dict[str, ModelSummary] = {}
    for model in models:
        model_id = _string(model.get("id"), "model.id")
        rows = [row for row in observations if row["model_id"] == model_id]
        if not rows:
            raise ValueError("comparator fixtures must not be empty")
        by_model[model_id] = {
            "observations": len(rows),
            "passed": sum(row["score"]["passed"] for row in rows),
            "schema_valid": sum(row["score"]["schema_valid"] for row in rows),
            "latency_ms_min": min(row["latency_ms"] for row in rows),
            "latency_ms_max": max(row["latency_ms"] for row in rows),
            "latency_ms_mean": round(sum(row["latency_ms"] for row in rows) / len(rows), 3),
        }
    receipt: _ReceiptFields = {
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
    return {**receipt, "receipt_sha256": hashlib.sha256(unsigned).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    manifest = read_object(MANIFEST_PATH)
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
